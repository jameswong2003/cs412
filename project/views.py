from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def index(request):
    products = Product.objects.all()
    return render(request, 'project/index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'project/product_detail.html', {'product': product})

@login_required
def purchase_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Transaction.objects.create(buyer=request.user, product=product)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'project/signup.html', {'form': form})
