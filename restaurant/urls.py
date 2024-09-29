from django.urls import path
from django.conf import settings
from . import views


# create a list of urls for this app:
urlpatterns = [
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]