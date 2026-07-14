from django.urls import path
from .views import customer_list, seller_list, product_list, sale_list
from .views import customer_create, seller_create, product_create, sale_create

urlpatterns = [
    path('customers/', customer_list, name='customer_list'),
    path('customers/add/', customer_create, name='customer_create'),
    path('sellers/', seller_list, name='seller_list'),
    path('sellers/add/', seller_create, name='seller_create'),
    path('products/', product_list, name='product_list'),
    path('products/add/', product_create, name='product_create'),
    path('sales/', sale_list, name='sale_list'),
    path('sales/add/', sale_create, name='sale_create'),
]
