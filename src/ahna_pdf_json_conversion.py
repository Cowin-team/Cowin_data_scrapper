#!/usr/bin/python3
# %%
# import libraries:
import numpy as np
import tabula as tb
import json
from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime

# %%
# post API url:
post_api_url = 'http://127.0.0.1:5000/updateBulk'

# %%
# construct pdf url:
page_url = 'https://ahna.org.in/covid19.html'

resp = requests.get(page_url)
soup = bs(resp.content, 'html.parser')
pdf_context = soup.find('iframe')
last_updated_dttm = pdf_context.get('src')[-30:-11].strip()
pdf_url = str(page_url[:-12] + pdf_context.get('src')).replace(' ', '%20')

# %%
# read pdf data as dataframe :
df = tb.read_pdf(pdf_url
, pages='all'
, format='CSV'
, lattice=True
, output_format='dataframe'
, pandas_options={'header': None,
                  'names': ['sr.no', 'zone/ward', 'hospital', 'ref isolation occupied', 'ref isolation available', 'ref HDU occupied', 'ref HDU available', 'ref ICU w/o Venti occupied', 'ref ICU w/o Venti available', 'ref ICU w/ Venti occupied', 'ref ICU w/ Venti available', 'ref Total', 'pvt isolation occupied', 'pvt isolation available', 'pvt HDU occupied', 'pvt HDU available', 'pvt ICU w/o Venti occupied', 'pvt ICU w/o Venti available', 'pvt ICU w/ Venti occupied', 'pvt ICU w/ Venti available', 'pvt Total'],
                  'skiprows': [0,1,2,3]}
                  , multiple_tables=True)

# %%
# remove empty rows:
df[0].dropna(axis=0, how='all', inplace=True)

# remove nulls from non-nullable columns:
df[0].dropna(axis=0, subset=['sr.no', 'hospital'], how='any', inplace=True)

# %%
# remove bad rows:
for i in range(df[0].shape[0]):
  try:
    int(float(df[0].iloc[i].get('pvt isolation available')))
  except ValueError as err:
    df[0].drop(df[0].iloc[i].name, inplace=True)
  except IndexError as err:
    break

# replace NaN with 0:
df[0].replace({np.nan:0}, inplace=True)

# %%
# convert float to int for summation:
# convert char in numeric fields to 0:
for c in ['ref isolation available', 'pvt isolation available', 'ref ICU w/o Venti available', 'pvt ICU w/o Venti available', 'ref HDU available', 'pvt HDU available', 'ref ICU w/ Venti available', 'pvt ICU w/ Venti available']:
  df[0][c] = df[0][c].apply(lambda x: re.sub(r'[A-Za-z]', '0', str(x)))
  df[0][c] = df[0][c].apply(lambda x: int(float(x)))

# %%
# enrich df with aggregated availability
# aggregate include ref & pvt quota total
# for respective hospitals:
df[0]['COVID Beds'] = df[0]['ref isolation available'].add(df[0]['pvt isolation available'], fill_value=0)
df[0]['ICU'] = df[0]['ref ICU w/o Venti available'].add(df[0]['pvt ICU w/o Venti available'], fill_value=0)
df[0]['HDU'] = df[0]['ref HDU available'].add(df[0]['pvt HDU available'], fill_value=0)
df[0]['Ventilator'] = df[0]['ref ICU w/ Venti available'].add(df[0]['pvt ICU w/ Venti available'], fill_value=0)
df[0]['Address'] = df[0]['hospital'] + ',' + df[0]['zone/ward'].apply(lambda x: x.split('/')[1] if x and len(x.split('/')) > 1 else x) + ', Ahmedabad'
df[0]['Contact'] = 'N/A'
df[0]['LAST UPDATED'] = str(datetime.strptime(last_updated_dttm, '%d-%m-%Y %I.%M %p'))
df[0]['LAST UPDATED checked'] = 'True'
df[0]['Sheet Name'] = 'Ahmedabad Beds'

# %%
# create new df with req columns:
df1 = df[0][['hospital', 'Address', 'COVID Beds', 'ICU', 'HDU', 'Ventilator', 'Contact', 'LAST UPDATED', 'LAST UPDATED checked', 'Sheet Name']]
# %%
# convert the new dataframe to JSON
# call the API & pass JSON to update sheet:
APIInput = df1.to_json(orient='records', indent=2)

try:
  api_response = requests.post(
        post_api_url, json=json.loads(APIInput), verify=False)
  print(api_response.text)
  if api_response.status_code != 200:
    raise Exception(f"bulkupdate failed: {api_response.text}")
except Exception as err:
  print(err)
finally:
  print("Exiting program!")
