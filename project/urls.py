from django.urls import path
from .views import show_profiles

urlpatterns = [
    path('', show_profiles, name='show_profiles'),
]
