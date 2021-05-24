import json

import requests
from collections import OrderedDict
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    try:
        districts = {"Ambala": "1", "Bhiwani": "2", "Chandigarh": "24", "Charki Dadri": "3", "Faridabad": "4", "Fatehabad": "5",
                     "Gurugram": "6", "Hisar": "7", "Jhajjar": "8", "Jind": "9", "Kaithal": "10", "Karnal": "11", "Kurukshetra": "12",
                     "Mahendragarh": "13", "Nuh": "23", "Palwal": "15", "Panchkula": "16", "Panipat": "17", "Rewari": "18",
                     "Rohtak": "19", "Sirsa": "20", "Sonipat": "21", "Yamunanagar": "22"}

        api_input = []
        api_url = 'http://127.0.0.1:5000/updateBulk'

        for district in districts.keys():
            url = "https://coronaharyana.in/?city="+districts[district]
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')
            main_div = soup.find('div', {"class": "tab-pane doc_tab_pane fade show active"})
            all_divs = main_div.find_all('div', {"class": "psahuDiv community-post wow fadeInUp"})

            for div in all_divs:
                
                data = OrderedDict()
                main_content = div.find('div', {"class": "entry-content"})
                meta_data = div.find('ul', {"class": "post-meta-info"})
                divs = main_content.find_all('div')
                data['Name'] = divs[0].find('h6', {"class": "tooltips_one"}).text.split("Facility Name:")[1]
                p = main_content.find('p')
                a = p.find_all('a') if p is not None else None
                data['COVID Beds'] = p.find('b').text if p.find('b') is not None else "0"
                data['Oxygen Beds'] = a[0].text
                data['ICU'] = a[2].text
                data['Ventilator Beds'] = a[3].text
                data['Contact'] = divs[-1].find('span').find('a').text
                last_updated = meta_data.find('li').text.split("Updated On:")[1]
                formatted_date = pd.to_datetime(last_updated)
                data['LAST UPDATED'] = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
                data['Sheet Name'] = district + " Beds"
                data['Check LAST UPDATED']=True
                data['Address'] = data['Name'] +', ' +district
                api_input.append(data)

        data = json.dumps(api_input)
        api_response = requests.post(api_url, json=json.loads(data), verify=False)

        if api_response.status_code != 200:
            raise Exception(f"bulk update failed: {api_response.text}")
    except Exception as ex:
        print(ex)
