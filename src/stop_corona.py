import pandas as pd
import os
import numpy as np
from collections import OrderedDict
import requests
import json
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)

# set os path separator:
#sep = os.path.sep

# get abspath:
#srcdir = os.path.dirname(os.path.abspath(__file__))

# reading data from URL
df = pd.read_html('https://stopcorona.tn.gov.in/beds.php')
# initialize ordered dict:
APIlist = []
url = 'http://127.0.0.1:5000/updateBulk'#'https://true-source-312806.et.r.appspot.com/update'
city = 'Krishnagiri' #Thiruchirappalli

for r in df:
    city_index = np.where(np.array(r['District']['District'].tolist())==city)
    for i in range(len(city_index[0])):
        result = OrderedDict()
        result['Name'] = r['Institution']['Institution'][city_index[0]].tolist()[i]
        result['COVID Beds'] = r['COVID BEDS']['Vacant'][city_index[0]].tolist()[i]
        result['Oxygen Beds'] = r['OXYGEN SUPPORTED BEDS']['Vacant'][city_index[0]].tolist()[i]
        result['ICU'] = r['ICU BEDS']['Vacant'][city_index[0]].tolist()[i]
        result['Ventilator Beds'] = r['VENTILATOR']['Vacant'][city_index[0]].tolist()[i]
        result['LAST UPDATED'] = r['Last updated']['Last updated'][city_index[0]].tolist()[i]
        result['Contact'] = r['Contact Number']['Contact Number'][city_index[0]].tolist()[i]
        result['Check LAST UPDATED']=True 
        result['Sheet Name'] = city+" Beds"#  'Nagercoil Beds'#

        APIlist.append((result))

    df1 = pd.DataFrame.from_dict(APIlist)        #print(result)
    APIInput = df1.to_json(orient='records', indent=2)
    response=requests.post(url, json=json.loads(APIInput), verify=False)
    print(response.text)

