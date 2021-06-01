import json

import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import datetime

if __name__ == '__main__':

	try:
		url = "https://covid19.uk.gov.in/bedssummary.aspx"
		api_input = []
		
		html_content = requests.get(url).text
		soup = BeautifulSoup(html_content, 'html.parser')
		gdp = soup.find_all("table", attrs={"id" : "grdhospitalbeds"})
		#print(len(gdp))

		table1 = gdp[0]
		body = table1.find_all("tr")
		body_rows = body[1:]


		for row_num in range(len(body_rows)):
			tds = body_rows[row_num].find_all("td")

			data = OrderedDict()

			data['Name'] = tds[1].text.partition("Dedicated")[0].replace("\n", "")
			data['COVID Beds'] = tds[3].text.split("/", 1)[0].replace("\n", "")
			data['Oxygen beds'] = tds[4].text.split("/", 1)[0].replace("\n", "")
			data['ICU'] = tds[5].text.split("/", 1)[0].replace("\n", "")
			data['Ventilator Beds'] = tds[6].text.split("/", 1)[0].replace("\n", "")
			data['Contact'] = (re.findall(r'\d+', tds[2].text))[0].strip()
			lastupdated = tds[7].text.replace("/", "-").replace("\n", "")
			data['LAST UPDATED'] = datetime.datetime.strptime(lastupdated, '%d-%m-%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
			data['Sheet Name'] = tds[0].text.replace("\n", "") + " Beds"
			data['Check LAST UPDATED']=True
			data['Address'] =tds[1].text.partition("Dedicated")[0].replace("\n", "") + ', '+ tds[0].text.replace("\n", "") + ', Uttarakhand'
			api_input.append(data)

		api_url = 'http://127.0.0.1:5000/updateBulk'

		data = json.dumps(api_input)
		print(data)
		api_response = requests.post(api_url, json=json.loads(data), verify=False)

		if api_response.status_code != 200:
			raise Exception(f"bulk update failed: {api_response.text}")

	except Exception as ex:
		print(ex)
