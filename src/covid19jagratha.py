# this script parses the data from https://covid19jagratha.kerala.nic.in/home/addHospitalDashBoard
import datetime
import requests
from bs4 import BeautifulSoup

CSRF_TOKEN = ""
DISTRICTS = []
SESSION = requests.Session()

def init_session():
	global CSRF_TOKEN, DISTRICTS
	
	response = SESSION.get("https://covid19jagratha.kerala.nic.in/home/addHospitalDashBoard", verify=False)
	html_page = BeautifulSoup(response.text, "lxml")
	CSRF_TOKEN = html_page.find("input", attrs={"name": "_csrf", "id": "csrf"})["value"]
	DISTRICTS = list(map(lambda o: {"id": o["value"], "name": o.text}, html_page.find(id="distId").find_all("option")))[1:]

def get_district_hospital_info(district):

	raw_hospital_info_dict = {}

	SESSION.post("https://covid19jagratha.kerala.nic.in/home/addHospitalDashBoard", data={"distId": district["id"], "_csrf": CSRF_TOKEN}, verify=False)

	raw_hospitals_info = SESSION.get("https://covid19jagratha.kerala.nic.in/home/getDistHospitalCount", verify=False).json()
	for raw_hospital_info in raw_hospitals_info:
		hospital_name = raw_hospital_info[0].strip()
		raw_hospital_info_dict[hospital_name] = {
			"normal": raw_hospital_info
		}

	raw_hospitals_info = SESSION.get("https://covid19jagratha.kerala.nic.in/home/getOxygenBedCount", verify=False).json()
	for raw_hospital_info in raw_hospitals_info:
		hospital_name = raw_hospital_info[0].strip()
		if hospital_name in raw_hospital_info_dict:
			raw_hospital_info_dict[hospital_name]["oxygen"] = raw_hospital_info
		else:
			raw_hospital_info_dict[hospital_name] = {
				"oxygen": raw_hospital_info
			}

	raw_hospitals_map_info = SESSION.post("https://covid19jagratha.kerala.nic.in/home/listHospitalLocation", data={"distId": district["id"], "_csrf": CSRF_TOKEN}, verify=False).json()
	for raw_hospital_map_info in raw_hospitals_map_info:
		hospital_name = raw_hospital_map_info[1].strip()
		if hospital_name in raw_hospital_info_dict:
			raw_hospital_info_dict[hospital_name]["address_info"] = raw_hospital_map_info
		else:
			raw_hospital_info_dict[hospital_name] = {
				"address_info": raw_hospital_map_info
			}

	usable_hospitals_info = []

	for hospital_name, hospital_info in raw_hospital_info_dict.items():

		skip = True
		usable_hospital_info = {
			"Name": hospital_name,
			"Sheet Name": "{} Beds".format(district["name"]),
		}

		if "normal" in hospital_info:
			skip = False	
			usable_hospital_info['COVID Beds'] = hospital_info["normal"][4]
			usable_hospital_info['ICU'] = hospital_info["normal"][10]
			usable_hospital_info['Ventilator Beds'] = hospital_info["normal"][6]
			if hospital_info["normal"][9] is not None:
				usable_hospital_info["LAST UPDATED"] = datetime.datetime.fromtimestamp(hospital_info["normal"][9]/1000).strftime('%Y-%m-%d %H:%M:%S')
				usable_hospital_info["Check LAST UPDATED"] = True
			else:
				usable_hospital_info["Check LAST UPDATED"] = False

		if "oxygen" in hospital_info:
			skip = False	
			usable_hospital_info['Oxygen beds'] = hospital_info["oxygen"][2]

		if "address_info" in hospital_info:
			usable_hospital_info["Address"] = "{}, {}".format(hospital_info["address_info"][1], hospital_info["address_info"][2])
			usable_hospital_info["Contact"] = hospital_info["address_info"][5]
			usable_hospital_info["lat"] = hospital_info["address_info"][3]
			usable_hospital_info["Long"] = hospital_info["address_info"][4]

		if not skip:
			usable_hospitals_info.append(usable_hospital_info)
		
	return usable_hospitals_info

def get_hospital_info():
	init_session()
	usable_hospitals_info = []
	for district in DISTRICTS:
		usable_hospitals_info.append(get_district_hospital_info(district))
	return usable_hospitals_info

def update_hospital_info(hospital_info):

	response = requests.post("http://127.0.0.1:5000/updateBulk", json=hospital_info)

	if response.status_code != 200:
		raise Exception(f"covid.py failed: {response.text}")

if __name__ == "__main__":
	init_session()
	usable_hospitals_info = get_hospital_info()
	update_hospital_info(usable_hospitals_info)
