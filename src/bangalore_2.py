import json

import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import re
from selenium import webdriver
import time
import pandas as pd
import sys
if sys.version_info[0] >= 3:
    unicode = str


if __name__ == '__main__':

	try:
		url = "https://searchmybed.com/#/p/public-portal"
		api_input = []
		
		browser = webdriver.Chrome()
		browser.get(url)
		time.sleep(10)
		soup = bs(browser.page_source, 'html.parser')
		table = soup.find("table")
		body = table.find_all('tr')
		body_rows = body[1:]

		for row_num in range(len(body_rows)):
			tds = body_rows[row_num].find_all("td")
			data = OrderedDict()
			name = tds[0]
			data['Address'] = name.find('p', attrs={'class':'address'}).text.replace("\r", " ,")
			data['Name'] = name.find('div', attrs={'class':'name'}).find('label').text
			data['COVID Beds'] = tds[1].text
			data['Oxygen beds'] = tds[2].text
			data['ICU'] = tds[4].text
			data['Ventilators'] = tds[3].text
			phone = name.find('p', attrs={'class':'phone'}).text
			if ":" in phone:
				num = phone.split(":", 1)[1]
			else:
				num = phone 
			string_encode = num.encode("ascii", "ignore")
			data['Phone Number'] = string_encode.decode()
			lu = name.find('p', attrs={'class':'last-updated-at'}).text.split(":", 1)[1]
			data['Last Updated'] = pd.to_datetime(lu).strftime("%Y-%m-%d %H:%M:%S")
			data['Sheet Name'] = "Bangalore Beds"
			data['Check LAST UPDATED']=True
			api_input.append(data)
			
		browser.close()
		api_url = 'http://127.0.0.1:5000/updateBulk'

		data = json.dumps(api_input)
		print(data)
		api_response = requests.post(api_url, json=json.loads(data), verify=False)

		if api_response.status_code != 200:
			raise Exception(f"bulk update failed: {api_response.text}")

	except Exception as ex:
		print(ex)
