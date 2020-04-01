from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
#import statements
import requests
from bs4 import BeautifulSoup
import json
import csv
from django.shortcuts import render

from .models import count_table,state_table,place_table

def index(request):
    
    
    return render(request, 'polls/index.html')
    
    

   
    
    
def my_background_job(request):
    response = requests.get('https://api.covid19india.org/state_district_wise.json')
    soup=BeautifulSoup(response.text,'html.parser')

    res2 = requests.get("https://www.worldometers.info/coronavirus/country/india/")
    soup2=BeautifulSoup(res2.text,'html.parser')
    mydivs = soup2.findAll("div", {"class": "maincounter-number"})
    listtmp=[]
    for link in mydivs:
       listtmp.append(link.get_text())

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
    for t in range(len(place_records)):
        p = place_table(state_name=place_records[t][0],place_name=place_records[t][1],place_count=place_records[t][2],delta_count=place_records[t][3])
        p.save()
    q=count_table(total_count=total_records[0][0],total_delta=total_records[0][1],total_deaths=int(listtmp[1]),total_recovered=int(listtmp[2]),total_active=int(total_records[0][0])-int(listtmp[1])-int(listtmp[2]))
    q.save()
    for v in range(len(state_records)):
        r=state_table(state_name=state_records[v][0],state_count=state_records[v][1],delta=state_records[v][2])
        r.save()
    return HttpResponse(status="200")
