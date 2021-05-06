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


url = 'https://true-source-312806.et.r.appspot.com/update'
for r in df:
    city_index = np.where(np.array(r['District']['District'].tolist())=='Thanjavur')
    for i in range(len(city_index[0])):
        result = OrderedDict()
        result['Name'] = r['Institution']['Institution'][city_index[0]].tolist()[i]
        result['COVID Beds'] = r['COVID BEDS']['Vacant'][city_index[0]].tolist()[i]
        result['Oxygen Beds'] = r['OXYGEN SUPPORTED BEDS']['Vacant'][city_index[0]].tolist()[i]
        result['ICU'] = r['ICU BEDS']['Vacant'][city_index[0]].tolist()[i]
        result['Ventilator Beds'] = r['VENTILATOR']['Vacant'][city_index[0]].tolist()[i]
        result['LAST UPDATED'] = r['Last updated']['Last updated'][city_index[0]].tolist()[i]
        result['Contact'] = r['Contact Number']['Contact Number'][city_index[0]].tolist()[i]
        result['Sheet Name'] = "Thanjavur Beds"
        result = json.dumps(result)
        response=requests.post(url, json=json.loads(result), verify=False)
        response.text
