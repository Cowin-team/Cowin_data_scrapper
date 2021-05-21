import pandas as pd
import numpy as np
from pandas import DataFrame,Series
pd.set_option("display.max_columns", 100)

url="https://goaonline.gov.in/beds"
df=pd.read_html(url)


goa = pd.DataFrame(np.array(df[1]),columns=['Hospital Name','Vacant Covid Beds','Vacant ICU Beds','Last Updated on'])

print(goa)
