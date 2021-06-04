import json

import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import pandas as pd

if __name__ == '__main__':

	try:
		url = "https://goaonline.gov.in/beds"
		api_input = []
		
		html_content = requests.get(url).text
		soup = BeautifulSoup(html_content, 'html.parser')
		gdp = soup.find_all("table", attrs={"id" : "cphBody_gvBedsAvailable"})
		#print(len(gdp))

		table1 = gdp[0]
		body = table1.find_all("tr")
		body_rows = body[1:]

		for row_num in range(len(body_rows)-2):
			tds = body_rows[row_num].find_all("td")
			data = OrderedDict()

			data['Name'] = tds[1].text.partition(",")[0]
			data['COVID Beds'] = tds[3].text
			data['Oxygen Beds'] = 'N/A'
			data['ICU'] = tds[5].text
			data['Ventilator Beds'] = 'N/A'
			data['Phone Number'] = 'N/A'
			data['LAST UPDATED'] = pd.to_datetime(tds[6].text).strftime("%Y-%m-%d %H:%M:%S")
			data['Sheet Name'] =  "Goa Beds"
			data['Check LAST UPDATED']=True
			data['Address'] = tds[1].text +', ' +'Goa'
			api_input.append(data)

		api_url = 'http://127.0.0.1:5000/updateBulk'

		data = json.dumps(api_input)
		#print(data)
		api_response = requests.post(api_url, json=json.loads(data), verify=False)

		if api_response.status_code != 200:
			raise Exception(f"bulk update failed: {api_response.text}")

	except Exception as ex:
		print(ex)
