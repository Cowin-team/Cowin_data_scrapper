# -*- coding: utf-8 -*-
"""Madhya Pradesh_Beds.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QfxENZ9VMZZMqq5gchfsI9UkvMqMIX9Z
"""
import json
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep

# %%
# post API url:
post_api_url = 'http://127.0.0.1:5000/updateBulk'
j=0
k=0
district_list = {'agar malwa':46,'alirajpur':14, 'anuppur':43, 'ashoknagar':10, 'balaghat':22, 'barwani':15, 'betul':30, 'bhind':8, 'bhopal':1, 'burhanpur':16, 'chhatarpur':37, 'chhindwara':23, 'damoh': 38, 'datia':12, 'dewas':47, 'dhar':18, 'dindori':29, 'guna':13, 'gwalior':9, 'harda':31, 'hoshangabad':32, 'indore':17, 'jabalpur':24, 'jhabua':19, 'katni':25, 'khandwa':20, 'khargone':21, 'mandla':26, 'mandsaur':48, 'morena': 6, 'narsinghpur':27, 'neemuch': 49, 'niwari':42, 'panna':39, 'raisen':2, 'rajgarh':3, 'ratlam':50, 'rewa':33, 'sagar':40, 'satna':34, 'sehore':4, 'seoni':28, 'shahdol':44, 'shajapur':51, 'sheopur':7,'shivpuri':11,'sidhi':35,'singrauli':36, 'tikamgarh':41, 'ujjain':52, 'umaria':45, 'vidisha':5}
for key,value in district_list.items():
  HospitalName=[]
  Map=[]
  BedStatus=[]
  IsolationBeds=[]
  OxygenSupported=[]
  ICUavailable=[]
  last_updated=[]
  sheetname=[]
  address = []
  contactInfo=[]

  url="http://sarthak.nhmmp.gov.in/covid/facility-bed-occupancy-details/?show=200&pagenum=1&district_id="+str(value)+"&facility_org_type=0&facility=0"
  r=requests.get(url)
  page=r.content
  
  soup=BeautifulSoup(page,'html.parser')
  row=soup.find_all('td')
  #print(row)
  hospitalname=soup.find_all('div',{'class':"hospitalname"})
  for hospital in hospitalname:
    HospitalName.append(hospital.text.split('/')[0])
    sheetname.append(key+' beds')
    address.append(hospital.text.split('/')[0]+", "+key+", Madhya Pradesh, India")
    # print(sheetname)

  ## ref=soup.find_all("a",{'class':'btn btn-primary btn-sm'})
  ref=soup.find_all("a",{'style':"text-transform: uppercase;text-align: left"})
  for href in ref:
    map=href.attrs['href'] if href is not None else ' '
    Map.append(map)
    # print(Map)

  BedStats=soup.find_all("span",{'class':"badge bed-status"})
  for bed in BedStats:
    Bedstatus=bed.text if bed is not None else " "
    BedStatus.append(Bedstatus)
    ## print(BedStatus)

  desc=soup.find_all("div",{'class':"deecriptions"})
  for numbers in desc:
    # num=numbers.find_all("label")[0]
    # nums=numbers.find_all("label")[1]

    num=numbers.find_all('li')[0]
    num_t=num.text.split('\n')
    IsolationBeds.append(num_t[2])
    # #print(IsolationBeds)

    num_o=numbers.find_all('li')[1]
    num_oxy=num_o.text.split('\n')
    OxygenSupported.append(num_oxy[2])
    ##print(OxygenSupported)
    
    icu=numbers.find_all("li")[2]
    num_icu=icu.text.split('\n')
    ICUavailable.append(num_icu[2])
    # # print(ICUavailable)

    last=soup.find("div",class_="last-updated")
    last_up=last.find("span")
    last_update=last_up.text.split(" ")
    #print(last_update[21],last_update[22])
    # print(last_update[22])
    last_updated.append(last_update[21].split(',')[0]+" "+last_update[22].split(',')[0])

    cont=soup.find("div",{"class":"card card-body contact-body"})
    contact=cont.find_all("span",{"class":"contact"})
    # j+=1
    # print(j)
    contact1=[]
    for call in contact:
      con=call.text.split(":")
      if (con[0]!="\n"):
        # print(con)
        contact1.append(con[1])
    contactInfo.append(contact1)

  # print(len(HospitalName), len(Map), len(BedStatus),len(IsolationBeds),len(OxygenSupported),len(ICUavailable),len(last_updated),len(contactInfo))
  mp_bedlist=pd.DataFrame({"Name":HospitalName,"Map Link":Map,"Bed Status":BedStatus,"COVID Beds":IsolationBeds,"Oxygen Beds":OxygenSupported,"ICU":ICUavailable,"LAST UPDATED":last_updated,"Sheet Name":sheetname,"Address": address,"ContactInformation":contactInfo,"Check LAST UPDATED":False})
## "Last Updated":last_updated
# print(len(HospitalName), len(Map), len(BedStatus),len(IsolationBeds),len(OxygenSupported),len(ICUavailable),len(last_updated),len(contactInfo))


  # print(mp_bedlist)
  APIInput = mp_bedlist.to_json(orient='records', indent=2)
  print(APIInput)
  try:
    api_response = requests.post(
          post_api_url, json=json.loads(APIInput), verify=False)
    print(api_response.text)
    if api_response.status_code != 200:
      raise Exception(f"bulkupdate failed: {api_response.text}")
  except Exception as err:
    print(err)
  finally:
    print("Exiting program!")

  #mp_bedlist.to_excel('MadhyaPradesh_cowinmap.xlsx')
