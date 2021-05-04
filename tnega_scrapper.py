name = 'pudukkottai'

import json

# Opening JSON file
with open(name+'.json') as json_file:
	data = json.load(json_file)

city = data['result'][0]['District']['Name']

result = []
header = ['Name', 'Address', 'Lat', 'Long', 'URL', 'COVID Beds', 'Oxygen Beds', 'ICU','Ventilator Beds', 'LAST UPDATED', 'Contact']                 
for i in range(len(data['result'])):
    row = []
    row.append(data['result'][i]['Name'])
    row.append('')
    row.append('')
    row.append('')
    row.append('')
    row.append(data['result'][i]['CovidBedDetails']['VaccantNonO2Beds'])
    row.append(data['result'][i]['CovidBedDetails']['VaccantO2Beds'])
    row.append(data['result'][i]['CovidBedDetails']['VaccantICUBeds'])
    row.append('')
    row.append(datetime.fromtimestamp(data['result'][i]['CovidBedDetails']['LastUpdatedTime']))
    result.append(row)
    
with open(name+'.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(header)
    write.writerows(result)
    
