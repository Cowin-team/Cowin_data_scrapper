import json
from collections import OrderedDict
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import Select

if __name__ == '__main__':
    api_input = []
    api_url = 'http://127.0.0.1:5000/updateBulk'
    districts = set()
    html_text = OrderedDict()

    # initialize the selenium web driver
    driver = webdriver.Chrome("/home/nmahesh/Documents/covid-19_India/Cowin_data_scrapper/src/chromedriver_folder/chromedriver")
    driver.get("https://excise.wb.gov.in/CHMS/Public/Page/CHMS_Public_Hospital_Bed_Availability.aspx")

    # get the district names
    select = Select(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddl_District"]'))
    for option in select.options:
        if option.text != '--Select--':
            districts.add(option.text)

    # get the html for each district by selecting the district from thr dropdown
    for district in districts:
        select = Select(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddl_District"]'))
        select.select_by_visible_text(district)
        sleep(10)  # allowing a sleep time of 10 sec to fully load the page
        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        html_text[district] = html

    # get paginated html by clicking on next page if there are more than 1.
    # This currently only supports 2 pages since no district has more than 2.
    for district in html_text.keys():
        html = html_text[district]
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody')
        pages = tbody.find('tr', {'class': 'pagination-ys'})
        if pages:
            print(district)
            try:
                select = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_GridView2"]/tbody/tr[1]/td/table/tbody/tr/td[2]/a')
                select.click()
                sleep(10)  # allowing a sleep time of 10 sec to fully load the page
                html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                html_text[district + "#2"] = html
            except Exception as ex:
                print(f"Could not load next page for {district}: {ex}")

    # parse the html for each district to collect required data
    for district in html_text.keys():
        print(district)
        html = html_text[district]
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody')
        rows = tbody.find_all('tr')
        for row in rows:
            data = OrderedDict()
            header = row.find('div', {'class': 'card-header'})
            if header:
                data['Name'] = header.find('h5').text.strip()
                data['Contact'] = header.find('a').text.strip()
                body = row.find('div', {'class': 'card-body'})
                content = body.find('div', {'id': 'collapseExample'})
                beds = content.find_all('div', {'class': 'col-lg-6 col-md-6 col-sm-12 mb-4'})
                covid_beds = beds[0]
                oxygen_beds = beds[1]
                icu_beds = beds[2]
                ventilator_beds = beds[-1]
                data['COVID Beds'] = covid_beds.find_all('h3')[-1].text
                data['Oxygen Beds'] = oxygen_beds.find_all('h3')[-1].text
                data['ICU'] = icu_beds.find_all('h3')[-1].text
                data['Ventilator Beds'] = ventilator_beds.find_all('h3')[-1].text
                if "#" in district:
                    # paginated html pages have been appended with page number to the district key
                    district = district.split("#")[0]
                data['Sheet Name'] = district + " Beds"
                last_updated = row.find('div', {'class': 'card-footer text-muted'})
                raw_date = last_updated.find('small').text.split('Last Updated On :')[-1]
                formatted_date = pd.to_datetime(raw_date)
                data['LAST UPDATED'] = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
                data['Check LAST UPDATED']=False
                api_input.append(data)

    data = json.dumps(api_input)
    try:
        api_response = requests.post(api_url, json=json.loads(data), verify=False)
        if api_response.status_code != 200:
            raise Exception(f"bulk update failed: {api_response.text}")
    except Exception as ex:
        print(ex)
