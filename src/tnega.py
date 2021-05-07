#!/usr/bin/python3
import requests
import json
from datetime import datetime
import os
from tnega_districtmapping import sheet_district_map

class APICallFailure(Exception):
  pass

if __name__ == '__main__':
  try:

    # define os separator:
    sep = os.path.sep

    # get src dir:
    srcdir = os.path.dirname(os.path.abspath(__file__))

    # initialize output list:
    APIinput = []

    # API url:
    api_url = 'http://127.0.0.1:5000/update'

    # iterate the district map:
    for sheetName, districtKey in sheet_district_map.items():
      fetch_data = {
                    "District": f"{districtKey}",
                    "FacilityTypes": ["CHO", "CHC", "CCC"],
                    "IsGovernmentHospital": True,
                    "IsPrivateHospital": True,
                    "pageLimit": 500
                  }
      res = requests.post('https://tncovidbeds.tnega.org/api/hospitals', data = json.dumps(fetch_data), headers={'Content-Type': 'application/json', 'Accept': 'text/plain'})
      res_json = res.json()
      for rec in res_json['result']:
        stack = {}
        stack['Sheet Name']=' '.join([rec.get('District','N/A').get('Name','N/A'),'Beds'])
        stack['Name']=rec.get('Name','N/A')
        stack['URL']=""
        stack['COVID Beds']=rec.get('CovidBedDetails', 'N/A').get('VaccantNonO2Beds','N/A')
        stack['Oxygen Beds']=rec.get('CovidBedDetails','N/A').get('VaccantO2Beds','N/A')
        stack['ICU']=rec['CovidBedDetails'].get('VaccantICUBeds','N/A')
        stack['LAST UPDATED']=datetime.fromtimestamp(rec.get('CovidBedDetails','N/A').get('UpdatedOn', 'N/A')).strftime('%Y-%m-%d %H:%M:%S')
        APIinput.append(stack)

    # write output to JSON file:
    #json.dump(APIinput, open(f'{srcdir}{sep}output{sep}APIinput_tnega.json', mode='w'), indent=2)
    # invoke the api to update sheet:
    for _json in APIinput:
      api_response = requests.post(api_url, json=json.loads(_json), verify=False)
      if api_response.status_code != 200:
        raise APICallFailure(api_response.text)
  except APICallFailure as err:
    print(err)
  except Exception as err:
    print(err)
