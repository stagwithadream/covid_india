
#import statements
import requests
from bs4 import BeautifulSoup
import json
import csv

response = requests.get('https://www.worldometers.info/coronavirus/country/india/')
soup=BeautifulSoup(response.text,'html.parser')
#creating an instance of soup from the input data
mydivs = soup.findAll("div", {"class": "maincounter-number"})
list=[]

for link in mydivs:
    list.append(link.get_text())