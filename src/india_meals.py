import json

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
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
        count = 0

        for ultag in soup.find_all('ul', {'class': 'MuiList-root MuiMenu-list MuiList-padding'}):
            for index, litag in enumerate(ultag.find_all('li')):
                if(litag.text == "Select State"):
                    continue
                # print(litag.text, index)
                if(index != 1):
                    openDropdown()
                    
                try:
                    # elem = browser.switch_to.active_element
                    webElement = browser.find_element(By.XPATH, "/html/body/div[2]/div[3]/ul/li[{}]".format(index+1))
                    time.sleep(1)
                    actions = ActionChains(browser)
                    actions.move_to_element(webElement).click(on_element=webElement).perform()
                    # WebDriverWait(browser,2).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/ul/li[{}]".format(index+1)))).click()
                except ElementClickInterceptedException:
                    print("Err 1 ", litag.text)
                    time.sleep(10)
                
                try:    
                    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[2]/div/button/span[1]/button/span[1]"))).click()
                    time.sleep(5)
                except ElementClickInterceptedException:
                    print("Err 2 ", litag.text)
                    time.sleep(10)

                last_height = browser.execute_script("return document.body.scrollHeight")
                while True:
                    # Scroll down to bottom
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # Wait to load page
                    time.sleep(1)
                    # Calculate new scroll height and compare with last scroll height
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                
                results = browser.find_elements_by_xpath("/html/body/div/div/div/div[4]/div[2]/button")
                # print(litag.text, len(results))
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
                        serviceType = "N/A"
                    try:    
                        pickup = soup.find("div", {"class" : "Style_pickup__195UR"}).find('p').text.strip()
                    except:
                        pickup = "N/A"
                    try:
                        hours = soup.find("div", {"class" : "Style_time__Eefwi"}).text.encode("ascii", "ignore").decode()
                    except:
                        hours = "N/A"
                    data['Comments'] = "Service type: " + serviceType + ", Pickup: " + pickup + ", Hours: " + hours
                    count += 1
                    api_input.append(data)
                    
                html = browser.find_element_by_tag_name('html')
                html.send_keys(Keys.UP)        

        browser.close()
        print("All done ", count)
        data = json.dumps(api_input)
        # print(data)
        
        # api_response = requests.post(api_url, json=json.loads(data), verify=False)
        # if api_response.status_code != 200:
        #     raise Exception(f"bulk update failed: {api_response.text}")
        
    except Exception as ex:
        print("Oh no!")
        print(ex)
        browser.quit()
