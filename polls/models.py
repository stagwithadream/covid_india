import datetime

from django.db import models
from django.utils import timezone


    
class state_table(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    state_count=models.IntegerField(default=0)
    state_name=models.CharField(max_length=250)
    counter=models.IntegerField(default=0)
    
class count_table(models.Model):
    date=models.DateTimeField(auto_now_add=True)  
    total_count=models.IntegerField(default=0)
    total_recovered=models.IntegerField(default=0)
    total_active=models.IntegerField(default=0)
    total_deaths=models.IntegerField(default=0)
    counter=models.IntegerField(default=0)
    
    
    
    