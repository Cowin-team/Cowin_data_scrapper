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
    
    districtkey =[ "5ea0abd3d43ec2250a483a4f",  "5ea0abd4d43ec2250a483a61", "5ea0abd2d43ec2250a483a40",  "5ea0abd3d43ec2250a483a4a","5ea0abd3d43ec2250a483a50","5ea0abd2d43ec2250a483a43",   "5ea0abd3d43ec2250a483a4b", "5ea0abd2d43ec2250a483a48", "5ea0abd4d43ec2250a483a5f", "5ea0abd2d43ec2250a483a41", "5ea0abd3d43ec2250a483a5c", "5ea0abd3d43ec2250a483a4c", "5ea0abd3d43ec2250a483a5d", "5ea0abd3d43ec2250a483a56", "60901c5f2481a4362891d572",  "5ea0abd3d43ec2250a483a51", "5ea0abd2d43ec2250a483a47", "5ea0abd3d43ec2250a483a49", "5ea0abd3d43ec2250a483a4e", "5ea0abd3d43ec2250a483a54",
"5ea0abd3d43ec2250a483a59",  "5ea0abd4d43ec2250a483a63","5ea0abd2d43ec2250a483a46", "5ea0abd3d43ec2250a483a55", "5ea0abd4d43ec2250a483a60", "5ea0abd3d43ec2250a483a53","5ea0abd3d43ec2250a483a57", "5ea0abd3d43ec2250a483a57", "5ea0abd4d43ec2250a483a62",  "5ea0abd3d43ec2250a483a52","5ea0abd3d43ec2250a483a5a", "5ea0abd3d43ec2250a483a5b","5ea0abd4d43ec2250a483a5e", "5ea0abd1d43ec2250a483a3f",
 "5ea0abd2d43ec2250a483a44", "5ea0abd2d43ec2250a483a42", "5ea0abd2d43ec2250a483a45", "5ea0abd3d43ec2250a483a58"]

    # API url:
    api_url = 'http://127.0.0.1:5000/updateBulk'

    # iterate the district map:
    for district_key in districtkey:
      fetch_data = {
                    "Districts": [f"{district_key}"],
                    "FacilityTypes": ["CHO", "CHC", "CCC"],
                    "IsGovernmentHospital": True,
                    "IsPrivateHospital": True,
                    "pageLimit": 50000
                  }
      res = requests.post('https://tncovidbeds.tnega.org/api/hospitals', data = json.dumps(fetch_data), headers={'Content-Type': 'application/json', 'Accept': 'text/plain'})
      res_json = res.json()
      APIinput = []
      for rec in res_json['result']:
           
           stack = {}
           if rec.get('District','N/A').get('Name','N/A') == 'Kanniyakumari':
              stack['Sheet Name']='Nagercoil Beds'
           else:
              stack['Sheet Name']=' '.join([rec.get('District','N/A').get('Name','N/A'),'Beds']) ##
           stack['Name']=rec.get('Name','N/A')
           stack['COVID Beds']=rec.get('CovidBedDetails', 'N/A').get('VaccantNonO2Beds','N/A')
           stack['Oxygen Beds']=rec.get('CovidBedDetails','N/A').get('VaccantO2Beds','N/A')
           stack['ICU']=rec['CovidBedDetails'].get('VaccantICUBeds','N/A')
           stack['LAST UPDATED']=datetime.fromtimestamp(rec.get('CovidBedDetails','N/A').get('UpdatedOn', 'N/A')).strftime('%Y-%m-%d %H:%M:%S')
           stack['Check LAST UPDATED'] = True
           stack['Contact'] = rec.get('MobileNumber','N/A')
           APIinput.append(stack)
      result = json.dumps(APIinput)
      api_response = requests.post(api_url, json=json.loads(result), verify=False)
      print(api_response.text)
    # write output to JSON file:
    #json.dump(APIinput, open(f'{srcdir}{sep}output{sep}APIinput_tnega.json', mode='w'), indent=2)
    # invoke the api to update sheet:
    #for _json in APIinput:
      
     # if api_response.status_code != 200:
      #  raise APICallFailure(api_response.text)
  except APICallFailure as err:
    print(err)
  except Exception as err:
    print(err)
