from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('my_background_job/',views.my_background_job,name='my_background_job'),
    path('get_data/',views.getData,name='getData'),
    ]
