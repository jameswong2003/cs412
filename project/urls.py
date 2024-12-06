from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from project import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('purchase/<int:pk>/', views.purchase_product, name='purchase_product'),

    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),

    path('businesses/', views.businesses, name='businesses'),
    path('business/<int:pk>/', views.business_detail, name='business_detail'),
    path('create_business/', views.create_business, name='create_business'),
    path('edit_business/', views.edit_business, name='edit_business'),
    
    path('transactions/', views.transactions, name='transactions'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]