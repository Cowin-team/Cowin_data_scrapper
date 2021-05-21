#!/usr/bin/python3
import pandas as pd
import json
from collections import OrderedDict
import requests
import numpy as np
import datetime
import math

class APICallFailure(Exception):
  pass


if __name__ == '__main__':
  try:

    # read data from URL:
    df = pd.read_html(
        'https://covidinfo.rajasthan.gov.in/Covid-19hospital-wisebedposition-wholeRajasthan.aspx')

    # initialize result dict:
    result = OrderedDict()

    # Update API url:
    api_url = 'http://127.0.0.1:5000/updateBulk'

    # iterate rows:
    for row in df:
        result['Name'] = row.get('Hospital Name').get('Hospital Name').tolist()
        result['COVID Beds'] = row.get('General Beds').get('A').tolist()
        result['Oxygen Beds'] = row.get('Oxygen Beds').get('A').tolist()
        result['ICU'] = row.get(
            'ICU Beds Without ventilator').get('A').tolist()
        result['Ventilator'] = row.get(
            'ICU Beds With ventilator').get('A').tolist()
        result['LAST UPDATED'] = row.get('Last Updation By Hospital').get(
            'Last Updation By Hospital').tolist()
        result['Contact'] = row.get('Hospital Helpline No.').get(
            'Hospital Helpline No.').tolist()
        result['Check LAST UPDATED'] = ['True']*len(row)
        result['Sheet Name'] = [f'{x} Beds' for x in row.get(
            'District').get('District').tolist()]
         
    
    result['LAST UPDATED']=[(datetime.datetime.now()) if pd.isna(x) else x for x in result['LAST UPDATED']]
    
    # convert dict to dataframe for conversion of datetime format:
    df1 = pd.DataFrame.from_dict(result)

    # skipping row 0:
    df1 = df1[1:]
     
    
    # convert LAST UPDATE to %Y-%m-%d %H:%M:%S format:
    df1['LAST UPDATED'] = df1['LAST UPDATED'].apply(
        lambda x: str(pd.to_datetime(x).replace(microsecond=0)))
     
    #print('Name: ' + (df1['LAST UPDATED']))
    # APIInput:
    APIInput = df1.to_json(orient='records', indent=2)
    #print(APIInput)
    # send df as json to update through API call:
    api_response = requests.post(
        api_url, json=json.loads(APIInput), verify=False)
    print(api_response.text)
    if api_response.status_code != 200:
      raise APICallFailure(f"bulkupdate failed: {api_response.text}")
      
  except Exception as err:
    print(err)
  except APICallFailure as err:
    print(err)
