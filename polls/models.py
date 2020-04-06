import datetime

from django.db import models
from django.utils import timezone
import datetime

    
class place_table(models.Model):
    
    state_name=models.CharField(max_length=250)
    place_name=models.CharField(max_length=250)
    place_count=models.IntegerField(default=0)
    delta_count=models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)

class state_table(models.Model):

    state_name=models.CharField(max_length=250)
    state_count=models.IntegerField(default=0)
    active_count=models.IntegerField(default=0)
    recovered_count=models.IntegerField(default=0)
    deaths_count=models.IntegerField(default=0)
    delta=models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    
    
class count_table(models.Model):
      
    total_count=models.IntegerField(default=0)
    total_recovered=models.IntegerField(default=0)
    total_active=models.IntegerField(default=0)
    total_deaths=models.IntegerField(default=0)
    total_delta=models.IntegerField(default=0)
    total_world_count=models.IntegerField(default=0)
    total_world_deaths=models.IntegerField(default=0)
    total_world_count_delta=models.IntegerField(default=0)
    total_world_deaths_delta=models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)


class contact (models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    qtext= models.TextField()
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)