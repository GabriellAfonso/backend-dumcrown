
from django.contrib import admin
from django.urls import path, include
from dumcrown.views import teste


urlpatterns = [
    path('', teste,),
]
