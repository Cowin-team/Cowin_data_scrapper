# %%
#!/usr/bin/python3
import pandas as pd
import json
from collections import OrderedDict
import requests

# %%
if __name__ == '__main__':
  # define the website url to be scraped:
  site_url = 'http://covidcbrs.nmc.gov.in/home/searchHosptial'

  # read site html table using pandas:
  df = pd.read_html(site_url)

  # initialize result dict:
  result = OrderedDict()

  # define the update url:
  update_api_url = 'http://127.0.0.1:5000/updateBulk'

  # iterate rows from output list
  # skipping last two rows as it contains cumulative total:
  for row in df:
    result['Name'] = row.get('Hospital Name').get(
          'Hospital Name').tolist()[:-2]
    result['COVID Beds'] = row.get(
          'General Beds').get('Vacant').tolist()[:-2]
    result['Oxygen Beds'] = row.get(
          'Oxygen Beds').get('Vacant').tolist()[:-2]
    result['ICU'] = row.get('ICU Beds').get('Vacant').tolist()[:-2]
    result['Ventilator'] = row.get(
          'Ventilator Beds').get('Vacant').tolist()[:-2]
    result['LAST UPDATED'] = ['N/A']*int(len(row) - 2)
    result['Contact'] = ['N/A']*int(len(row) - 2)
    result['Check LAST UPDATED'] = ['False']*int(len(row) - 2)
    result['Sheet Name'] = ['Nashik Beds']*int(len(row) - 2)

  # create normalized dataframe from result dict:
  norm_df = pd.DataFrame.from_dict(result)

  # clean hospital name:
  norm_df['Name'] = norm_df['Name'].apply(
      lambda x: x.replace("(Click here for contact details)", ""))

  # update sheets using the api call:
  try:
    APIInput = norm_df.to_json(orient='records', indent=2)
    print(APIInput)
    api_response = requests.post(
          update_api_url, json=json.loads(APIInput), verify=False)
    print(api_response.text)
    if api_response.status_code != 200:
      raise Exception(f"bulkupdate failed: {api_response.text}")
  except Exception as err:
    print(err)
