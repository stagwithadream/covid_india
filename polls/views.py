from django.http import HttpResponse, HttpResponseRedirect,JsonResponse # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from datetime import datetime
#import statements
import requests
from bs4 import BeautifulSoup
import json
import csv
from django.shortcuts import render


from .models import count_table,state_table,place_table,contact

def index(request):
    #state_table.objects.raw('select * from (select a.* from polls_state_table a inner join (select date,state_name, max(time) time from polls_state_table group by date,state_name) b on a.state_name=b.state_name and a.date=b.date and a.time=b.time)as T where date=(select max(date) from polls_state_table) order by state_count DESC ;')
    
    return render(request, 'polls/index.html')
    
def getData(request):
    name=[]
    count=[]
    delta=[]
    
    total_count=[]
    total_active=[]
    total_deaths=[]
    total_recovered=[]
    total_delta=[]
    date=[]
    time=[]
    unknown=0
    for p in state_table.objects.raw('select * from (select a.* from polls_state_table a inner join (select date,state_name, max(time) time from polls_state_table group by date,state_name) b on a.state_name=b.state_name and a.date=b.date and a.time=b.time)as T where date=(select max(date) from polls_state_table) order by state_count DESC ;'):
        if p.state_name!='Unknown':
            name.append(p.state_name)
            count.append(p.state_count)
            delta.append(p.delta)
            
        else:
            unknown=p.state_count
    query=count_table.objects.raw('select a.* from polls_count_table a inner join (select date,max(time) time from polls_count_table group by date) b on a.date=b.date and a.time=b.time order by date;')        
    for q in query :
        total_count.append(q.total_count)
        total_active.append(q.total_active)
        total_deaths.append(q.total_deaths)
        date.append(q.date.strftime("%d-%b"))
        
        time.append(q.time)
        total_delta.append(q.total_delta)
        total_recovered.append(q.total_recovered)
    today_confirmed=query[len(query)-1].total_count
    today_recovered=query[len(query)-1].total_recovered
    today_active=query[len(query)-1].total_active
    today_deaths=query[len(query)-1].total_deaths
    today_delta=query[len(query)-1].total_delta
    today_world_count=query[len(query)-1].total_world_count
    today_world_deaths=query[len(query)-1].total_world_deaths
    today_world_count_delta=query[len(query)-1].total_world_count_delta
    today_world_deaths_delta=query[len(query)-1].total_world_deaths_delta
    today_time=query[len(query)-1].time.strftime(" %H:%M:%S")
    yestar_confirmed=query[len(query)-2].total_count
    yestar_recovered=query[len(query)-2].total_recovered
    yestar_active=query[len(query)-2].total_active
    yestar_deaths=query[len(query)-2].total_deaths
    yestar_delta=query[len(query)-2].total_delta
    yestar_world_count=query[len(query)-2].total_world_count
    yestar_world_deaths=query[len(query)-2].total_world_deaths
    yestar_world_count_delta=query[len(query)-2].total_world_count_delta
    yestar_world_deaths_delta=query[len(query)-2].total_world_deaths_delta
    
    
    state_data={
        "label" : name,
        "data": count,
        "delta": delta,
        "unknown": unknown,
        
        "total_deaths":total_deaths,
        "total_active":total_active,
        "total_count":total_count,
        "total_delta":total_delta,
        "total_recovered":total_recovered,
        "date": date,
        "time":time,

        "today_confirmed": today_confirmed,
        "today_recovered":today_recovered,
        "today_deaths":today_deaths,
        "today_delta":today_delta,
        "today_active":today_active,

        "today_world_count":today_world_count,
        "today_world_deaths":today_world_deaths,
        "today_world_count_delta":today_world_count_delta,
        "today_world_deaths_delta":today_world_deaths_delta,


        "yestar_confirmed": yestar_confirmed,
        "yestar_recovered":yestar_recovered,
        "yestar_deaths":yestar_deaths,
        "yestar_delta":yestar_delta,
        "yestar_active":yestar_active,

        "yestar_world_count":yestar_world_count,
        "yestar_world_deaths":yestar_world_deaths,
        "yestar_world_count_delta":yestar_world_count_delta,
        "yestar_world_deaths_delta":yestar_world_deaths_delta,

        "today_time":today_time,
        }
    return JsonResponse(state_data)
    
def my_background_job(request):
    response = requests.get('https://api.covid19india.org/state_district_wise.json')
    soup=BeautifulSoup(response.text,'html.parser')

    res2 = requests.get("https://www.worldometers.info/coronavirus/country/india/")
    soup2=BeautifulSoup(res2.text,'html.parser')
    mydivs = soup2.findAll("div", {"class": "maincounter-number"})
    listtmp=[]
    for link in mydivs:
       listtmp.append(link.get_text())


    res3 = requests.get("https://www.worldometers.info/coronavirus/")
    soup3=BeautifulSoup(res3.text,'html.parser')
        
    rowstmp = soup3.find('tr', attrs={'class': 'total_row'}).findAll('td')

    world_count_delta=rowstmp[2].get_text().replace("+","").replace(",","")
    world_count=rowstmp[1].get_text().replace("+","").replace(",","")
    world_death=rowstmp[3].get_text().replace("+","").replace(",","")
    world_death_delta=rowstmp[4].get_text().replace("+","").replace(",","")




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
            if state!='Unknown':
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
    q=count_table(total_count=total_records[0][0],total_delta=total_records[0][1],total_deaths=int(listtmp[1]),total_recovered=int(listtmp[2]),total_active=int(total_records[0][0])-int(listtmp[1])-int(listtmp[2]),total_world_count=int(world_count),total_world_count_delta=int(world_count_delta),total_world_deaths=int(world_death),total_world_deaths_delta=int(world_death_delta))
    q.save()
    for v in range(len(state_records)):
        r=state_table(state_name=state_records[v][0],state_count=state_records[v][1],delta=state_records[v][2])
        r.save()
    return HttpResponse(status="200")


def create_post(request):
    data={}
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        qtext = request.POST.get('qtext')
        
        print(name)
        s=contact(name=name,email=email,qtext=qtext)
        s.save()
        return render(request, 'polls/contact2.html')

    return render(request, 'polls/contact.html')  