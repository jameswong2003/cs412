from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import random
from datetime import timedelta

MENU_ITEMS = [
    {"name": "Spicy Post", "price": 12.00, "options": ["Meat", "Seafood", "Vegetables"]},
    {"name": "Spicy Cold Noodles", "price": 7.00},
    {"name": "Soup Dumplings", "price": 10.00},
    {"name": "Sour Fish", "price": 10.00}
]

DAILY_SPECIAL = [
    {"name": "Spicy Pig Ears", "price": 15.00},
    {"name": "Fried Frog Legs", "price": 12.00},
    {"name": "Popcorn Chicken", "price": 8.00}
]

def main(request):
    '''
    the page with basic information about the restaurant. the main page should include the name, location, hours of operation (displayed as a list or table), and one or more photos appropriate to such a page.
    '''
    return render(request, 'main.html')

def order(request):
    '''
    the view for the ordering page. This view will need to create a “daily special” item (choose randomly from a list), and add it to the context dictionary for the page.
    Finally, delegate presentation to the order.html HTML template for display.
    '''
    daily_special = random.choice(DAILY_SPECIAL)
    context = {
        "menu_items": MENU_ITEMS,
        "daily_special": daily_special
    }

    return render(request, 'order.html', context)

def confirmation(request):
    '''
    the confirmation page to display after ordering
    '''
    if request.method == 'POST':
        ordered_items = []
        total_price = 0.0
        for item in MENU_ITEMS:
            if request.POST.get(item['name']):
                ordered_items.append(item['name'])
                total_price += item['price']
        
        ready_time = timezone.now() + timedelta(minutes=random.randint(30, 60))
        
        context = {
            'ordered_items': ordered_items,
            'total_price': total_price,
            'customer_name': request.POST.get('name'),
            'customer_phone': request.POST.get('phone'),
            'customer_email': request.POST.get('email'),
            'special_instructions': request.POST.get('instructions'),
            'ready_time': ready_time
        }
        
        return render(request, 'confirmation.html', context)
    else:
        return redirect('order')