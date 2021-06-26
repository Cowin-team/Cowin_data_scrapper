import time
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

UPDATE_URL = "http://127.0.0.1:5000/updateVaccinationCenterBulk"

def get_request(url):

    response = requests.get(
        url=url,
        headers={"user-agent": ""},
        verify=False
    )
    
    return response.json()

def get_states():

    response_json = get_request('https://cdn-api.co-vin.in/api/v2/admin/location/states')

    states = response_json['states']

    return states

def get_districts(state):

    response_json = get_request('https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(state['state_id']))

    districts = response_json['districts']

    return districts

def clean_vaccination_centers(sheet_name, vaccination_center):

    todays_sessions = []
    
    for session in vaccination_center["sessions"]:
        if session["date"] == time.strftime('%d-%m-%Y'):
            todays_sessions.append(session)

    clean_vaccination_center = {
        "Sheet Name": sheet_name,
        "Center ID": vaccination_center["center_id"],
        "Name": vaccination_center["name"],
        "Address": vaccination_center["address"],
        "Lat": vaccination_center["lat"],
        "Long": vaccination_center["long"],
        "LAST UPDATED": time.strftime('%d-%m-%Y %H:%M:%S'),
        "Check LAST UPDATED": True,
        "District": vaccination_center["district_name"],
        "State": vaccination_center["state_name"],
        "Pincode": vaccination_center["pincode"],
        "Block Name": vaccination_center["block_name"],
        "Fee Type": vaccination_center["fee_type"],
        "Opening Time": vaccination_center["from"],
        "Closing Time": vaccination_center["to"],
    }
    
    for todays_session in todays_sessions:
        vaccine_type = todays_session["vaccine"]
        age_limit = todays_session["min_age_limit"]
        clean_vaccination_center["{} Min Age {} Dose-1 Availability".format(vaccine_type, age_limit)] = todays_session["available_capacity_dose1"]
        clean_vaccination_center["{} Min Age {} Dose-2 Availability".format(vaccine_type, age_limit)] = todays_session["available_capacity_dose2"]

    return clean_vaccination_center

def get_vaccination_centers(state):

    sheet_name = '{} Vaccination Centers'.format(state["state_name"])

    districts = get_districts(state)
    
    usable_vaccination_centers = []

    for district in districts:
        try:
            response_json = get_request('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}'.format(district["district_id"], time.strftime('%d-%m-%Y')))
            vaccination_centers = response_json["centers"]
            usable_vaccination_centers.extend(
                map(lambda x: clean_vaccination_centers(sheet_name, x), vaccination_centers)
            )
        except Exception as err:
            print(err)

    return usable_vaccination_centers

def update_state_centers_sheet(vaccination_centers):
    
	response = requests.post(UPDATE_URL, json=vaccination_centers)

	if response.status_code != 200:
		raise Exception(f"cowin_vaccination_slots.py failed: {response.text}")

def main():
    states = get_states()
    for state in states:
        print("getting centers for", state["state_name"])
        vaccination_centers = get_vaccination_centers(state)
        print("updating")
        update_state_centers_sheet(vaccination_centers)

if __name__ == '__main__':
    main()