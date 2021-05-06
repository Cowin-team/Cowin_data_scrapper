#!/usr/bin/python3
import pandas as pd
import os
import json
from collections import OrderedDict


if __name__ == '__main__':
    try:
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

        # store JSON:
        tFile = f'{srcdir}{sep}output{sep}tmpFile.json'
        df.to_json(tFile, orient='records', indent=2)

        # create JSON for API calls:
        with open(tFile) as json_read:
            jconf = json.load(json_read)
            result = []
            for d in jconf:
                d['Sheet Name'] = f"{d['Name']} Beds"
                d['Name'] = d['Address']
                d.pop('Address', None)
                d.pop('Lat', None)
                d.pop('Long', None)
                d.pop('Ventilator', None)
                d.pop('Contact', None)
                result.append(d)

        # write to JSON
        # This can be replaced with making a call to the API for automated updates:
        with open(os.path.join(f'{srcdir}{sep}output', 'APIinput_stopcorona.json'), mode='w') as json_write:
            json.dump(result, json_write, indent=2, sort_keys=True)
    except Exception as err:
      print(err)
    finally:
      if os.path.exists(tFile):
        os.remove(tFile)
