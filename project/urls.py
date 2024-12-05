from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from project import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('purchase/<int:pk>/', views.purchase_product, name='purchase_product'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_product/', views.add_product, name='add_product'),
    path('create_business/', views.create_business, name='create_business'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]