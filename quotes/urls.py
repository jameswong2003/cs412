## quotes/urls.py
## descrption: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views


# create a list of urls for this app:
urlpatterns = [
    path('', views.index, name='index'),
    path('quote/', views.quote, name='quote'),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
]