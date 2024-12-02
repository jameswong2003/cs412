from django.shortcuts import render
from .models import User

def show_profiles(request):
    profiles = User.objects.all()
    return render(request, 'profiles.html', {'profiles': profiles})