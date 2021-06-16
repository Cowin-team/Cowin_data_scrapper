import json

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
if sys.version_info[0] >= 3:
    unicode = str

def openDropdown():
    a = browser.find_element_by_xpath('//*[@class="MuiSelect-root MuiSelect-select MuiSelect-selectMenu MuiSelect-outlined MuiInputBase-input MuiOutlinedInput-input"]')
    actions = ActionChains(browser)
    actions.click(on_element=a).perform()
    

if __name__ == '__main__':
    try:
        url = "https://covidmealsforindia.com/"
        api_input = []
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get(url)
        openDropdown()
        soup = bs(browser.page_source, 'html.parser')
        actions = ActionChains(browser)

        for ultag in soup.find_all('ul', {'class': 'MuiList-root MuiMenu-list MuiList-padding'}):
            for index, litag in enumerate(ultag.find_all('li')):
                if(litag.text == "Select State"):
                    continue
                # print(litag.text, index)
                if(index != 1):
                    openDropdown()
                    
                # elem = browser.switch_to.active_element
                # webElement = browser.find_element(By.XPATH, "/html/body/div[2]/div[3]/ul/li[{}]".format(index))
                # actions.move_to_element(webElement).click().perform()
                WebDriverWait(browser,1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/ul/li[{}]".format(index)))).click()
                WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[2]/div/button/span[1]/button/span[1]"))).click()
                time.sleep(2)
                results = browser.find_elements_by_xpath("/html/body/div/div/div/div[4]/div[2]/button")
                for result in results:
                    data = OrderedDict()
                    elementHTML = result.get_attribute('outerHTML')
                    soup = bs(elementHTML, 'html.parser')
                    data['Name'] = soup.find("div", {"class": "Style_heading_title__1o14B"}).find('h1').text.strip()
                    data['Address'] = soup.find("div", {"class": "Style_heading_title__1o14B"}).find('p').text.strip()
                    data['Phone Number'] = soup.find("div", {"class": "Style_mobile__2axY1"}).find('p').text.strip()
                    data['State'] = litag.text
                    try:
                        serviceType = soup.find("div", {"class" : "Style_service_type__3JHoA"}).find('p').text.strip()
                    except:
                        "N/A"
                    try:    
                        pickup = soup.find("div", {"class" : "Style_pickup__195UR"}).find('p').text.strip()
                    except:
                        "N/A"
                    try:
                        hours = soup.find("div", {"class" : "Style_time__Eefwi"}).text.encode("ascii", "ignore").decode()
                    except:
                        "N/A"
                    data['Comments'] = "Service type: " + serviceType + ", Pickup: " + pickup + ", Hours: " + hours
                    api_input.append(data)    

        browser.close()
        data = json.dumps(api_input)
        print(data)
        
        # api_response = requests.post(api_url, json=json.loads(data), verify=False)
        # if api_response.status_code != 200:
        #     raise Exception(f"bulk update failed: {api_response.text}")
        
    except Exception as ex:
        print("Oh no!")
        print(ex)
        browser.quit()
