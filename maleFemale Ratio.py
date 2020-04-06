
#import statements
import requests
from bs4 import BeautifulSoup
import json
import csv

response = requests.get('https://api.covid19india.org/raw_data.json')
soup=BeautifulSoup(response.text,'html.parser')
#creating an instance of soup from the input data

data = json.loads(str(soup))

male=0
female=0
unknown=0
ratio=[]
records=[]

print(len(data['raw_data']))


for i in range(len(data['raw_data'])):
    ratio.append(data['raw_data'][i]['gender'])
    if data['raw_data'][i]['gender']=='' :
        unknown=unknown+1
    if data['raw_data'][i]['gender']=='M':
        male=male+1
        
    if data['raw_data'][i]['gender']=='F':
        female=female+1