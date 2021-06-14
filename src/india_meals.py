import json

import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def openDropdown():
    a = browser.find_element_by_xpath('//*[@class="MuiSelect-root MuiSelect-select MuiSelect-selectMenu MuiSelect-outlined MuiInputBase-input MuiOutlinedInput-input"]')
    actions = ActionChains(browser)
    actions.click(on_element=a)
    actions.perform()
    

if __name__ == '__main__':
    try:
        url = "https://covidmealsforindia.com/"
        api_input = []
        browser = webdriver.Chrome()
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
                WebDriverWait(browser,1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/ul/li[{}]".format(index)))).click()
                WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[2]/div/button/span[1]/button/span[1]"))).click()
                time.sleep(2)
                results = browser.find_elements_by_xpath("/html/body/div/div/div/div[4]/div[2]/button")
                for id in range(len(results)):
                    data = OrderedDict()
                    if(len(results) == 1):
                        data['Name'] = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button/div/div[1]/div/div[1]/h1").text
                        data['Address'] = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button/div/div[1]/div/div[2]/p").text
                        data['Phone Number'] = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button/div/div[3]/p").text
                        data['Type'] = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button/div/div[2]/p").text
                        data['Free'] = "N/A"
                        # delivery = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button/div/div[4]/p").text
                        # timings = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button/div/div[5]/p[1]").text
                        data['Comments'] = "N/A"
                        data['Cost Type'] = "N/A"
                    else:
                        data['Name'] = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button[{}]/div/div[1]/div/div[1]/h1".format(id+1)).text
                        data['Address'] = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button[{}]/div/div[1]/div/div[2]/p".format(id+1)).text
                        data['Phone Number'] = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button[{}]/div/div[3]/p".format(id+1)).text
                        data['Type'] = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button[{}]/div/div[2]/p".format(id+1)).text
                        data['Free'] = "N/A"
                        #ToDo: Needs some cleanup to extract the below properties
                        # delivery = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button[{}]/div/div[4]/p".format(id+1)).text
                        # timings = browser.find_element_by_xpath("/html/body/div/div/div/div[4]/div[2]/button[{}]/div/div[5]/p[1]".format(id+1)).text
                        data['Comments'] = "N/A"
                        data['Cost Type'] = "N/A"
                    api_input.append(data)

        browser.close()
        data = json.dumps(api_input)
        # print(data)
        api_response = requests.post(api_url, json=json.loads(data), verify=False)

	if api_response.status_code != 200:
	    raise Exception(f"bulk update failed: {api_response.text}")
        
    except Exception as ex:
        print(ex)
