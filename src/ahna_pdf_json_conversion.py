#!/usr/bin/python3
# %%
# import libraries:
import pandas as pd
import numpy as np
import tabula as tb
import json

# %%
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# %%
# read pdf data as dataframe skipping unwanted 
# rows which do not conform with table structure 
# adding meaningful column names using tabula
df = tb.read_pdf('https://ahna.org.in/AMC%20REQUISITIONED%20HOSPITAL%20STATUS%2013-05-2021%205.00%20PM%20ONLINE.pdf'
, pages='all'
, format='CSV'
, lattice=True
, output_format='dataframe'
, pandas_options={'header': None,
                  'names': ['sr.no', 'zone/ward', 'hospital', 'ref isolation occupied', 'ref isolation available', 'ref HDU occupied', 'ref HDU available', 'ref ICU w/o Venti occupied', 'ref ICU w/o Venti available', 'ref ICU w/ Venti occupied', 'ref ICU w/ Venit available', 'ref Total', 'pvt isolation occupied', 'pvt isolation available', 'pvt HDU occupied', 'pvt HDU available', 'pvt ICU w/o Venti occupied', 'pvt ICU w/o Venti available', 'pvt ICU w/ Venti occupied', 'pvt ICU w/ Venit available', 'pvt Total'],
                  'skiprows': [0,1,2,3,4,7,44,45,46,47,48,90,91,92,93,94,134,135,136,137,138,180,181,182,183,184,201,202,203,213,214,215,216,217,244,245,246,247,248,261,262,263,264,265]}
                  , multiple_tables=True)


# %%
# remove empty rows:
df[0].dropna(axis=0, how='all', inplace=True)


# %%
# replace NaN with None:
df[0].replace({np.nan:None}, inplace=True)


# %%
# convert the output dataframe to JSON:

json_data = df[0].to_json(orient='records', indent=2)
print(json_data)

# %%
