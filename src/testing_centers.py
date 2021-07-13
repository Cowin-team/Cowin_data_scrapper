import json

import requests
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from geopy.geocoders import Nominatim
import pandas as pd
import ssl
from pandas.io.json import json_normalize
import math
import time
import sys
if sys.version_info[0] >= 3:
    unicode = str

def execute():
    try:
        executeButton = driver.find_element(By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div.execute-wrapper > button")
        executeButton.location_once_scrolled_into_view
        executeButton.click()
    except NoSuchElementException:
        executeButton = driver.find_element(By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div.btn-group > button.btn.execute.opblock-control__btn")
        executeButton.location_once_scrolled_into_view
        executeButton.click()
    time.sleep(10)

def clear():
    try:
        clearButton = driver.find_element(By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div.btn-group > button.btn.btn-clear.opblock-control__btn")
        clearButton.location_once_scrolled_into_view
        clearButton.click()
    except NoSuchElementException:
        print("-_-")
        
def pagination(page_no):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div:nth-child(2) > div.parameters-container > div > table > tbody > tr:nth-child(3) > td.parameters-col_description > input[type=text]"))).clear()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div:nth-child(2) > div.parameters-container > div > table > tbody > tr:nth-child(3) > td.parameters-col_description > input[type=text]"))).send_keys(page_no)
            
    
if __name__ == '__main__':
    resourceUrl = "https://app.swaggerhub.com/apis-docs/kapil-dhaimade/covisearchapi/0.1#/default/get_covisearchapi"
    cowinApi = "https://cowinmapapis.com/resource/get_details"
    
    try:
        # First extracting cities of interest from cowinApi which will be params for resourceUrl GET requests
        ssl._create_default_https_context = ssl._create_unverified_context
        df = pd.read_json(cowinApi)
        df.index = pd.Index(['COUNTRY', 'LAT', 'LONG', 'RESOURCES', 'STATE'], name='CITY')
        cities = list(df.T.index)
        cityList = [sub.replace(" ", "") for sub in cities]
        
        testing_results_for_api_input = []
        pharma_results_for_api_input = []
        GEOLOCATOR = Nominatim(user_agent='cowinmap')
        
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(resourceUrl)
        time.sleep(5)
        
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#operations-default-get_covisearchapi > div.no-margin > div > div.opblock-section > div.opblock-section-header > span > div > button"))).click()
        except ElementClickInterceptedException:
            time.sleep(5)
        
        for city in cityList:
            count = 0
            # Clear the text field
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div:nth-child(2) > div.parameters-container > div > table > tbody > tr:nth-child(1) > td.parameters-col_description > input[type=text]"))).clear()
            # Propulate city name
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div:nth-child(2) > div.parameters-container > div > table > tbody > tr:nth-child(1) > td.parameters-col_description > input[type=text]"))).send_keys(city)
            # Click resource type dropdown
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div:nth-child(2) > div.parameters-container > div > table > tbody > tr:nth-child(2) > td.parameters-col_description > select"))).click()
            # Select testing center
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div:nth-child(2) > div.parameters-container > div > table > tbody > tr:nth-child(2) > td.parameters-col_description > select > option:nth-child(8)"))).click()
            # Select page number and set it to 0 for pagination
            pagination(1)
            try:
                # Click execute and wait for page to load
                execute()
                # Wait for results to be loaded
                myElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#operations-default-get_covisearchapi > div.no-margin > div > div.responses-wrapper > div.responses-inner > div > div > table > tbody > tr > td.response-col_description > div:nth-child(1) > div > pre > code > span:nth-child(2)")))
            except Exception as ex:
                print("Execute error: ", ex)
                time.sleep(10)
                clear()
                continue  
            
            # Extract test results
            try:
                resultText = driver.find_element_by_css_selector("#operations-default-get_covisearchapi > div.no-margin > div > div.responses-wrapper > div.responses-inner > div > div > table > tbody > tr > td.response-col_description > div:nth-child(1) > div > pre")
            except Exception as ex:
                print("Load error: ", ex)
                time.sleep(10)
                clear()
                continue 
            
            try:    
                totalResults = json.loads(resultText.text)['meta_info']['total_records']
                if totalResults == 0:
                    continue
                #print(city, totalResults)
                entriesPerPage = 12
                pages = math.ceil(totalResults/entriesPerPage)
            except ValueError as ex:    
                print("JSON error: ", ex, " result text: ", resultText.text)
                time.sleep(60)
                clear()
                continue 
            
            try: 
                # Perform pagination
                for page in range(pages):
                    if page != 1:
                        # Update page_no and perform GET
                        pagination(page)
                        execute()
                        
                    resultList = json.loads(resultText.text)['resource_info_data']
                    # Parse test results
                    for result in resultList:
                        test_data = OrderedDict()
                        try:
                            test_data['Name'] = result['name']
                        except:
                            test_data['Name'] = "N/A"    
                        try:
                            address = result['address']  
                            test_data['Address'] = address
                        except:
                            test_data['Address'] = "N/A" 
                        # Get lat/long coordinates from address    
                        try:
                            lastString = address.rsplit(',', 1)[1].strip()
                            if lastString.isnumeric():
                                coordinates = GEOLOCATOR.geocode(lastString) #geocode from pincode
                            else:
                                coordinates = GEOLOCATOR.geocode(city + ', India')
                    
                            # print("Coordinates: ", coordinates, coordinates.latitude, coordinates.longitude)
                            test_data['Latitude'] = coordinates.latitude
                            test_data['Longitude'] = coordinates.longitude
                        except:
                            test_data['Latitude'] = "N/A"
                            test_data['Longitude'] = "N/A"
                        try:
                            test_data['Phone Number'] = result['phones']
                        except:
                            test_data['Phone Number'] = "N/A"   
                        try:
                            test_data['Last verified'] = result['last_verified_utc']
                        except:
                            test_data['Last verified'] = "N/A"    
                        try:
                            test_data['Testing center details'] = result['details']
                        except:
                            test_data['Last verified'] = "N/A" 
                        count += 1    
                        testing_results_for_api_input.append(test_data)                    
            except: 
                clear()
                continue
                    
            #Clear previous results if any
            clear()
            print("City complete: ", city, totalResults, count)

        df = pd.DataFrame(testing_results_for_api_input, columns=testing_results_for_api_input[0].keys())
        df.to_csv('testing_centers.csv')
        # print(data)
        driver.close()
            
    except Exception as ex:
        print("Exception!")
        print(ex)
        driver.quit() 
        
   