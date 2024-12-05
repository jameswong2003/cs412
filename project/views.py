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

def transactions(request):
    # Get all transactions and sort them by transaction_date in descending order
    transactions = Transaction.objects.all().order_by('-transaction_date')

    context = {
        'transactions': transactions,
    }
    return render(request, 'project/transactions.html', context)

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
    
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 1))
        Transaction.objects.create(buyer=request.user, product=product, amount=amount)
        
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
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Check if the logged-in user owns the business associated with this product
    if product.business.owner != request.user:
        return redirect('profile')  # Redirect if the user doesn't own the product

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProductForm(instance=product)

    return render(request, 'project/edit_product.html', {'form': form, 'product': product})

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

@login_required
def profile(request):
    try:
        # Get the business owned by the logged-in user
        business = Business.objects.get(owner=request.user)
        # Get all products associated with the business
        products = Product.objects.filter(business=business)
    except Business.DoesNotExist:
        # If the user doesn't own a business, set business and products to None
        business = None
        products = None

    # Get the transactions made by the user
    transactions = Transaction.objects.filter(buyer=request.user)

    context = {
        'business': business,
        'products': products,
        'transactions': transactions,
    }
    return render(request, 'project/profile.html', context)

@login_required
def edit_business(request):
    try:
        business = Business.objects.get(owner=request.user)
    except Business.DoesNotExist:
        return redirect('create_business')

    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = BusinessForm(instance=business)

    return render(request, 'project/edit_business.html', {'form': form})
