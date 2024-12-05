from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Product, Transaction, Business
from .forms import ProductForm, BusinessForm

def index(request):
    products = Product.objects.all()
    return render(request, 'project/index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'project/product_detail.html', {'product': product})

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

# LOGIN REQUIRED

@login_required
def purchase_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Transaction.objects.create(buyer=request.user, product=product)
    return redirect('index')

@login_required
def add_product(request):
    try:
        business = Business.objects.get(owner=request.user)
    except Business.DoesNotExist:
        return redirect('create_business')  # Redirect if the user doesn't have a business

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = business  # Assign the business to the product
            product.save()
            return redirect('index')
    else:
        form = ProductForm()

    return render(request, 'project/add_product.html', {'form': form})


@login_required
def create_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            return redirect('index')
    else:
        form = BusinessForm()
    return render(request, 'project/create_business.html', {'form': form})
