#!/usr/bin/python3
import pandas as pd
import os
from collections import OrderedDict
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)

# set os path separator:
sep = os.path.sep

# get abspath:
srcdir = os.path.dirname(os.path.abspath(__file__))

# reading data from URL
df = pd.read_html('https://stopcorona.tn.gov.in/beds.php')

# initialize ordered dict:
result = OrderedDict()

# populate the dict:
for r in df:
    result['Name'] = r['District']['District'].tolist()
    result['Address'] = r['Institution']['Institution'].tolist()
    result['Lat'] = [''] * len(df[0])
    result['Long'] = [''] * len(df[0])
    result['URL'] = [''] * len(df[0])
    result['COVID Beds'] = r['COVID BEDS']['Vacant'].tolist()
    result['Oxygen Beds'] = r['OXYGEN SUPPORTED BEDS']['Vacant'].tolist()
    result['ICU'] = r['ICU BEDS']['Vacant'].tolist()
    result['Ventilator'] = r['VENTILATOR']['Vacant'].tolist()
    result['Last Update'] = r['Last updated']['Last updated'].tolist()
    result['Contact'] = r['Contact Number']['Contact Number'].tolist()

# create dataframe from result dict, sort by Name:
df = pd.DataFrame.from_dict(result).sort_values(['Name'])

# write dataframe to JSON:
df.to_json(os.path.join(f'{srcdir}{sep}output', 'output.json'), orient='records', indent=2)

# write dataframe to CSV:
df.to_csv(os.path.join(f'{srcdir}{sep}output', 'output.csv'), header=True, index=None, encoding='utf8', quoting=0)