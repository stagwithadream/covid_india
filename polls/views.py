from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
#import statements
import requests
from bs4 import BeautifulSoup
import json
import csv

from .models import count_table,state_table
def index(request):
    res = requests.get("https://www.worldometers.info/coronavirus/country/india/")
    soup=BeautifulSoup(res.text,'html.parser')
    #creating an instance of soup from the input data
    mydivs = soup.findAll("div", {"class": "maincounter-number"})
    list=[]

    for link in mydivs:
        list.append(link.get_text())

    
    return HttpResponse("<h1> Total corona Count </h1>" + list[0])

   
    
    
def my_background_job(request):
    
    res = requests.get("https://www.worldometers.info/coronavirus/country/india/")
    soup=BeautifulSoup(res.text,'html.parser')
    #creating an instance of soup from the input data
    mydivs = soup.findAll("div", {"class": "maincounter-number"})
    list=[]

    for link in mydivs:
        list.append(link.get_text())   

    p = count_table(total_count=int(list[0].replace(",","")),total_deaths=int(list[1]),total_recovered=int(list[2]))
    p.save()
    return HttpResponse(status="200")
