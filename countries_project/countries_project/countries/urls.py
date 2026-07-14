from django.urls import path
from . import views

app_name = 'countries'

urlpatterns = [
    path('', views.country_list, name='country_list'),
    path('regions/', views.region_list, name='region_list'),
    path('regions/<str:region_name>/', views.region_detail, name='region_detail'),
    path('countries/<str:country_name>/', views.country_detail, name='country_detail'),
    path('cities/<str:city_name>/', views.city_detail, name='city_detail'),
    path('language_search/', views.language_search, name='language_search'),
]
