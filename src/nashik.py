# %%
# !/usr/bin/python3
import pandas as pd
import json
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime

# regex compile:
_CONTACT_CLEAN_PATTERN = re.compile(r"(\s|\n|\-)")
_ADDRESS_CLEAN_PATTERN = re.compile(r"(\n|\-)")

# %%
if __name__ == '__main__':
    # define the website url to be scraped:
    site_url = 'http://covidcbrs.nmc.gov.in/home/searchHosptial'

    # read site html table using pandas:
    df = pd.read_html(site_url)

    # get contacts & addresses from the URL response
    # this piece can be optimized to get all the information
    # from single URL call but due to lack of time adding
    # separate calls to get clean Hospital contact number
    res = requests.post(site_url, data={"bed_aval": "all", "hosptype": "all", "search": "Search"})
    soup = bs(res.content, 'html.parser')
    _get_rows = [s.text for s in soup.find_all('tr', recursive=True)]
    _hosp_contacts = []
    _addresses = []

    # skipping 2 header and 2 footer rows
    # these rows are not within our interest:
    for i, row in enumerate(_get_rows[2:-2], 1):
      _hosp_contacts.append(_CONTACT_CLEAN_PATTERN.sub('', [r.split(':')[1] if len(r.split(':')) > 1 else r for r in row.split('\n\n')][12]).strip())
      _addresses.append(_ADDRESS_CLEAN_PATTERN.sub('', [r.split(':')[1] if len(r.split(':')) > 1 else r for r in row.split('\n\n')][10]).strip())

    # initialize result dict:
    result = OrderedDict()

    # define the update url:
    update_api_url = 'http://127.0.0.1:5000/updateBulk'
    now = datetime.now()
    # iterate rows from output list
    # skipping last two rows in df
    # as it contains total counts:
    for row, _contacts, _addresses in zip(df, [_hosp_contacts], [_addresses]):
        result['Name'] = row.get('Hospital Name').get(
            'Hospital Name').tolist()[:-2]
        result['COVID Beds'] = row.get(
            'General Beds').get('Vacant').tolist()[:-2]
        result['Oxygen Beds'] = row.get(
            'Oxygen Beds').get('Vacant').tolist()[:-2]
        result['ICU'] = row.get('ICU Beds').get('Vacant').tolist()[:-2]
        result['Ventilator Beds'] = row.get(
            'Ventilator Beds').get('Vacant').tolist()[:-2]
        result['LAST UPDATED'] = [now.strftime("%Y-%m-%d %H:%M:%S")]*int(len(row) - 2)
        result['Contact'] = _contacts
        result['Check LAST UPDATED'] = ['False']*int(len(row) - 2)
        result['Address'] = _addresses
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
