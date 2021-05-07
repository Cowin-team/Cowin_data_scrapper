
import requests
import json
from datetime import datetime
import os
from tnega_districtmapping import sheet_district_map

# define os separator:
sep = os.path.sep

# get src dir:
srcdir = os.path.dirname(os.path.abspath(__file__))

# initialize output list:
APIinput = []

# iterate the district map:
for sheetName in sheet_district_map:
  fetch_data = {
                "District": f"{sheetName}",
                "FacilityTypes": ["CHO", "CHC", "CCC"],
                "IsGovernmentHospital": True,
                "IsPrivateHospital": True,
                "pageLimit": 1
              }
  res = requests.post('https://tncovidbeds.tnega.org/api/hospitals', data = json.dumps(fetch_data), headers={'Content-Type': 'application/json', 'Accept': 'text/plain'})
  res_json = res.json()
  for rec in res_json['result']:
    stack = {}
    stack['Sheet Name']=f"{sheetName}"
    stack['Name']=rec.get('Name','N/A')
    stack['URL']=""
    stack['COVID Beds']=rec['CovidBedDetails'].get('VaccantNonO2Beds','N/A')
    stack['Oxygen Beds']=rec['CovidBedDetails'].get('VaccantO2Beds','N/A')
    stack['ICU']=rec['CovidBedDetails'].get('VaccantICUBeds','N/A')
    stack['LAST UPDATED']=datetime.fromtimestamp(rec['CovidBedDetails'].get('UpdatedOn', 'N/A')).strftime('%Y-%m-%d %H:%M:%S')
    APIinput.append(stack)

# write output to JSON file:
json.dump(APIinput, open(f'{srcdir}{sep}output{sep}APIinput_tnega.json', mode='w'), indent=2)
