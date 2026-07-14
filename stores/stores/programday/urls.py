# urls.py
from django.urls import path
from . import views

app_name = 'app3'

urlpatterns = [
    # Главная страница - текущий год
    path('', views.programmer_day, name='current'),

    # Страница для конкретного года
    path('<int:year>/', views.programmer_day_by_year, name='by_year'),
]