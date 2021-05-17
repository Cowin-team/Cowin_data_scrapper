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


result = OrderedDict()
for r in df:
    city_index = np.where(np.array(r['District']['District'].tolist())=='Kanyakumari')[0]
    city_index2 = np.where(np.array(r['District']['District'].tolist())=='TheNilgiris')[0]
    result['Name'] = (r['Institution']['Institution'].tolist())
    result['COVID Beds'] = (r['COVID BEDS']['Vacant'].tolist())
    result['Oxygen Beds'] = (r['OXYGEN SUPPORTED BEDS']['Vacant'].tolist())
    result['ICU'] = (r['ICU BEDS']['Vacant'].tolist())
    result['Ventilator Beds'] = r['VENTILATOR']['Vacant'].tolist()
    result['LAST UPDATED'] =  r['Last updated']['Last updated'].tolist()
    result['Contact'] =  r['Contact Number']['Contact Number'].tolist()
    result['Check LAST UPDATED']=True 
    result['Sheet Name'] = np.array([x + ' Beds' for x in r['District']['District'].tolist()])
    
    result['Sheet Name'][city_index] = 'Nagercoil Beds'
    result['Sheet Name'][city_index2] = 'Nilgiris Beds'
        #APIlist.append((result))
    
    df1 = pd.DataFrame.from_dict(result)        
    APIInput = df1.to_json(orient='records', indent=2)
    response=requests.post(url, json=json.loads(APIInput), verify=False)
    print(response.text)

