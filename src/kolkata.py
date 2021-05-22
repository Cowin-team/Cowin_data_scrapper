import json
from collections import OrderedDict
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import Select


def getPaginatedPages(web_driver, html, html_text):
    soups = BeautifulSoup(html, 'html.parser')
    tb = soups.find('tbody')
    pagination = tb.find('tr', {'class': 'pagination-ys'})
    if pagination:
        tds = pagination.find_all('td')
        for i in range(2, len(tds)):
            if tds[i].find('a'):
                page = web_driver.find_element_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_GridView2"]/tbody/tr[1]/td/table/tbody/tr/td[{i}]/a')
                page.click()
                sleep(15)
                html_p = web_driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                html_text.append(html_p)

        page = web_driver.find_element_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_GridView2"]/tbody/tr[1]/td/table/tbody/tr/td[{1}]/a')
        page.click()
        sleep(15)


if __name__ == '__main__':
    api_input = []
    api_url = 'http://127.0.0.1:5000/updateBulk'
    html_text = list()
    district = 'KOLKATA METROPOLITAN AREA'

    # initialize the selenium web driver
    driver = webdriver.Chrome("/home/nmahesh/Documents/covid-19_India/Cowin_data_scrapper/src/chromedriver_folder/chromedriver")
    driver.get("https://excise.wb.gov.in/CHMS/Public/Page/CHMS_Public_Hospital_Bed_Availability.aspx")

    select = Select(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddl_District"]'))
    select.select_by_visible_text(district)
    sleep(10)  # allowing a sleep time of 10 sec to fully load the page

    # get govt requisitioned private hospital data
    select_govt_pvt = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rdo_Govt_Flag"]/label[2]')
    select_govt_pvt.click()
    sleep(15)
    html_govt_pvt = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    html_text.append(html_govt_pvt)
    # check pagination
    getPaginatedPages(driver, html_govt_pvt, html_text)

    # get private hospital data
    select_pvt = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rdo_Govt_Flag"]/label[3]')
    select_pvt.click()
    sleep(15)
    html_pvt = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    html_text.append(html_pvt)
    getPaginatedPages(driver, html_pvt, html_text)

    # get govt hospital data
    select_govt = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rdo_Govt_Flag"]/label[1]')
    select_govt.click()
    sleep(15)
    html_govt = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    html_text.append(html_govt)
    getPaginatedPages(driver, html_govt, html_text)

    # parse the html for each district to collect required data
    for html in html_text:
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody')
        if not tbody:
            continue
        rows = tbody.find_all('tr')
        for row in rows:
            data = OrderedDict()
            header = row.find('div', {'class': 'card-header'})
            if header:
                #print(header)
                data['Address']=header.find('div', {'class': 'card-text col-md-12 col-lg-12 col-sm-12 col-xs-12'}).text.strip()
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
                data['Sheet Name'] = district + " Beds"
                last_updated = row.find('div', {'class': 'card-footer text-muted'})
                raw_date = last_updated.find('small').text.split('Last Updated On :')[-1]
                formatted_date = pd.to_datetime(raw_date)
                data['LAST UPDATED'] = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
                data['Check LAST UPDATED']=True
                api_input.append(data)

    data = json.dumps(api_input)
    try:
        api_response = requests.post(api_url, json=json.loads(data), verify=False)
        if api_response.status_code != 200:
            raise Exception(f"bulk update failed: {api_response.text}")
    except Exception as ex:
        print(ex)
