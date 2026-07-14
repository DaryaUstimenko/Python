from  django.urls import path
from  . import views

urlpatterns = [
    path('date/', views.current_datetime, name = 'current_datetime'),
]
