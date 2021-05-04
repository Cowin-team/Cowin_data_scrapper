import pandas as pd
import numpy as np
import csv
from pandas import DataFrame,Series
pd.set_option("display.max_columns", 100)

df=pd.read_html('https://stopcorona.tn.gov.in/beds.php')
#df[0].info()
result = []
header = ['Name', 'Address', 'Lat', 'Long', 'URL', 'COVID Beds', 'Oxygen Beds', 'ICU','Ventilator Beds', 'LAST UPDATED', 'Contact']                 

for i in range(len(df[0])):
    row = []
    row.append(df[0]['District']['District'][i])
    row.append(df[0]['Institution']['Institution'][i])
    row.append('')
    row.append('')
    row.append('')
    row.append('')
    row.append(df[0]['COVID BEDS']['Vacant'][i])
    row.append(df[0]['OXYGEN SUPPORTED BEDS']['Vacant'][i])
    row.append(df[0]['ICU BEDS']['Vacant'][i])
    row.append(df[0]['VENTILATOR']['Vacant'][i])
    row.append(df[0]['Last updated']['Last updated'][i])
    result.append(row)
    
with open('complete.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(header)
    write.writerows(result)
