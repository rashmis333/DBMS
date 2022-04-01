from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hi,name='home-page'),
    path('output',views.output,name='output')
    #,path('url_list',views.url_list,name='url_list')
]