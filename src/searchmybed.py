import json
import base64
import datetime
import requests
from urllib.parse import urlparse, parse_qs

def clean_data(raw_hospital_info):

    # raw hospital example
	# {
    	# 'name': 'Cratis Hospitals Pvt Ltd',
    	# 'address': '4-4/1 Hennur Main Road\nGeddalahalli\nBangalore - 56077',
    	# 'lastUpdatedAt': '10-05-2021 21:08:09',
    	# 'hospitalPhone': 8028444733,
    	# 'phone': 8884411041,
    	# 'location': 'https://maps.google.com/?q=12.9893351,77.5092028&z=5',
    	# 'type': 'Private Hospital',
    	# 'total': 15,
    	# 'vacant': 0,
    	# 'vrb': 0,
    	# 'vbo': 0,
    	# 'vvb': 0,
    	# 'vib': 0,
    # }
	# table headers
	#[
	# 	{'label': 'Name', 'key': 'name'},
	# 	{'label': 'Vacant Regular Beds', 'key': 'vrb'},
	# 	{'label': 'Vacant Beds with Oxygen', 'key': 'vbo'},
	# 	{'label': 'Vacant Beds with Ventilator', 'key': 'vvb'},
	# 	{'label': 'Vacant ICU Beds', 'key': 'vib'},
	# 	{'label': 'Total Vacant', 'key': 'vacant'}
	# ]
	
	usable_hospital_list = []
	
	for raw_hospital in raw_hospital_info:
		usable_hospital = {
			"Name": raw_hospital["name"],
			"Address": raw_hospital["address"],
			'COVID Beds': raw_hospital["vrb"],
			'Oxygen beds': raw_hospital["vbo"],
			'ICU': raw_hospital["vib"],
			'Ventilator Beds': raw_hospital["vvb"],
			"Contact": raw_hospital["phone"],
			"Last Updated": datetime.datetime.strptime(raw_hospital["lastUpdatedAt"], "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
			"Sheet Name": "Bangalore Beds",
			"Check LAST UPDATED": True,
		}
		coords = parse_qs(urlparse(raw_hospital["location"]).query)["q"][0]
		if coords != '0,0':
			lat, long = coords.split(',')
			usable_hospital["lat"] = float(lat)
			usable_hospital["Long"] = float(long)
		usable_hospital_list.append(usable_hospital)
	
	return usable_hospital_list

def get_hospital_info():
    
	response = requests.post(
		url="https://searchmybed.com/patientTracking/fetch_hospitals_list",
		# this is just base64 encoded string of {"userID":null,"userName":null,"userType":null,"userRole":null,"type":""}
		data="eyJ1c2VySUQiOm51bGwsInVzZXJOYW1lIjpudWxsLCJ1c2VyVHlwZSI6bnVsbCwidXNlclJvbGUiOm51bGwsInR5cGUiOiIifQ==",
		verify=False
	)
	base64_encoded_response = response.text
	json_response = json.loads(base64.b64decode(base64_encoded_response))
	raw_json_hospital_info = json_response["data"]["tableData"]["bodyContent"]
	usable_hospital_info = clean_data(raw_json_hospital_info)
	return usable_hospital_info

def update_hospital_info(hospital_info):

	response = requests.post("http://127.0.0.1:5000/updateBulk", json=hospital_info)

	if response.status_code != 200:
		raise Exception(f"searchmybed.py failed: {response.text}")
	
if __name__ == "__main__":
	hospital_info = get_hospital_info()
	print(hospital_info)
	update_hospital_info(hospital_info)