from django.http import HttpResponse
from django.shortcuts import render
import random

QUOTES = [
    "You can't be afraid to fail. It's the only way you succeed - you're not gonna succeed all the time, and I know that.",
    "I like criticism. It makes you strong.",
    "You have to be able to accept failure to get better."
]

IMAGES = [
    "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/1966.png",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkua4zc6vGKg6FGl5tqsmqbbva__CLi84gvQ&s",
    "https://creatorset.com/cdn/shop/files/preview_images/Screenshot_2024-04-30_153708_1200x1200.png?v=1714480757"
]


def index(request):
    '''Handle the Index page'''
    return quote(request)

def quote(request):
    '''Generate random quote and image'''
    quote = random.choice(QUOTES)
    image = random.choice(IMAGES)
    context = {'quote': quote, 'image': image}
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    '''Shows all images and quotes'''
    context = {'quotes': QUOTES, 'images': IMAGES}
    return render(request, 'quotes/show_all.html', context)

def about(request):
    '''Shows name and biography'''
    context = {
        'name': 'Lebron James',
        'biography': "LeBron Raymone James Sr. is an American professional basketball player for the Los Angeles Lakers of the National Basketball Association."
    }
    return render(request, 'quotes/about.html', context)
