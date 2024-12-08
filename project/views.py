from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q

from .models import Product, Transaction, Business
from .forms import ProductForm, BusinessForm

def index(request):
    """Index page to show all available products on the marketplace"""
    products = Product.objects.all()

    search_query = request.GET.get('search', '')
    business_query = request.GET.get('business', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if business_query:
        products = products.filter(business__name__icontains=business_query)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'project/index.html', {
        'products': products,
        'search_query': search_query,
        'business_query': business_query,
        'min_price': min_price,
        'max_price': max_price
    })

def product_detail(request, pk):
    """Shows a specific product detail"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'project/product_detail.html', {'product': product})

def transactions(request):
    """Shows all transactions made under the service"""
    transactions = Transaction.objects.all()

    company_name = request.GET.get('company_name', '')
    buyer_name = request.GET.get('buyer_name', '')
    sort = request.GET.get('sort', '-transaction_date')

    if company_name:
        transactions = transactions.filter(product__business__name__icontains=company_name)

    if buyer_name:
        transactions = transactions.filter(buyer__username__icontains=buyer_name)

    transactions = transactions.order_by(sort)

    context = {
        'transactions': transactions,
        'company_name': company_name,
        'buyer_name': buyer_name,
        'sort': sort,
    }
    return render(request, 'project/transactions.html', context)

def businesses(request):
    """Shows all businesses under the service"""
    businesses = Business.objects.all()

    name_query = request.GET.get('name', '')
    owner_query = request.GET.get('owner', '')

    if name_query:
        businesses = businesses.filter(name__icontains=name_query)
    if owner_query:
        businesses = businesses.filter(
            Q(owner__first_name__icontains=owner_query) | Q(owner__last_name__icontains=owner_query)
        )

    return render(request, 'project/businesses.html', {
        'businesses': businesses,
        'name_query': name_query,
        'owner_query': owner_query,
    })

def business_detail(request, pk):
    """Shows details of a specific business"""
    business = get_object_or_404(Business, pk=pk)
    products = Product.objects.filter(business=business)
    return render(request, 'project/business_detail.html', {
        'business': business,
        'products': products
    })

def signup(request):
    """Signs a user up"""
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
    """Purchase a product and save it to the transaction table"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 1))
        Transaction.objects.create(buyer=request.user, product=product, amount=amount)
        
    return redirect('index')

@login_required
def add_product(request):
    """Creates a new product under the specific business"""
    try:
        business = Business.objects.get(owner=request.user)
    except Business.DoesNotExist:
        return redirect('create_business')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = business
            product.save()
            return redirect('index')
    else:
        form = ProductForm()

    return render(request, 'project/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    """Edits a specific product"""
    product = get_object_or_404(Product, pk=pk)

    if product.business.owner != request.user:
        return redirect('profile')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProductForm(instance=product)

    return render(request, 'project/edit_product.html', {'form': form, 'product': product})

@login_required
def create_business(request):
    """Create a business"""
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
    """Page to look at the specific profile"""
    try:
        business = Business.objects.get(owner=request.user)
        products = Product.objects.filter(business=business)
    except Business.DoesNotExist:
        business = None
        products = None

    transactions = Transaction.objects.filter(buyer=request.user)

    context = {
        'business': business,
        'products': products,
        'transactions': transactions,
    }
    return render(request, 'project/profile.html', context)

@login_required
def edit_business(request):
    """Edits a business"""
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
