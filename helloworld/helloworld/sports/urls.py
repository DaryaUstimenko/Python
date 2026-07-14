from django.urls import path
from . import views

urlpatterns = [
    path('sport/', views.sport, name='sport'),
    path('football/', views.football, name='football'),
    path('hockey/', views.hockey, name='hockey'),
    path('basketball/', views.basketball, name='basketball'),
]

