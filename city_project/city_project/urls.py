# city_project/urls.py
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Главная страница
    path('', views.home, name='home'),
    
    # Новости города
    path('news/', views.news, name='news'),
    
    # Руководство города
    path('government/', views.government, name='government'),
    
    # Факты о городе
    path('facts/', views.facts, name='facts'),
    
    # Контактные телефоны городских служб
    path('contacts/', views.contacts, name='contacts'),
    # Раздел История - с подразделами
    path('history/', views.history_main, name='history_main'),
    path('history/people/', views.history_people, name='history_people'),
    path('history/photos/', views.history_photos, name='history_photos.html'),
]