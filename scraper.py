
#import statements
import requests
from bs4 import BeautifulSoup
import json
import csv

response = requests.get('https://api.covid19india.org/state_district_wise.json')
soup=BeautifulSoup(response.text,'html.parser')
#creating an instance of soup from the input data

data = json.loads(str(soup))





states=[]
place_records=[]
state_records=[]
total_records=[]
count=0
state_count=0
delta_count=0
delta_state_count=0

for state in data:
    states.append(state)

count=0
for state in states:
    for district in data[state]['districtData']:
        place_records.append((state,district,data[state]['districtData'][district]['confirmed'],data[state]['districtData'][district]['delta']['confirmed']))
        delta_count=delta_count+int(data[state]['districtData'][district]['delta']['confirmed'])
        count=count+int(data[state]['districtData'][district]['confirmed'])
        delta_state_count=delta_state_count+int(data[state]['districtData'][district]['delta']['confirmed'])
        state_count=state_count+int(data[state]['districtData'][district]['confirmed'])
    state_records.append((state,state_count,delta_state_count))
    state_count=0
    delta_state_count=0
total_records.append((count,delta_count)) 



res2 = requests.get("https://www.worldometers.info/coronavirus/country/india/")
soup2=BeautifulSoup(res2.text,'html.parser')
    #creating an instance of soup from the input data
mydivs = soup2.findAll("div", {"class": "maincounter-number"})
list=[]

for link in mydivs:
   list.append(link.get_text())
print(list[2])