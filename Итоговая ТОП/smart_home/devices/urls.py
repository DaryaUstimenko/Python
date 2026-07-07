from django.urls import path
from . import views

app_name = 'devices'

urlpatterns = [
    # Главная панель
    path('', views.dashboard, name='dashboard'),

    # Список устройств
    path('devices/', views.device_list, name='device_list'),

    # Детальная страница устройства (универсальная)
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),

    # Управление устройством (включить/выключить)
    path('device/<int:device_id>/toggle/', views.toggle_device, name='toggle_device'),

    # Универсальное управление устройством (для всех типов)
    path('device/<int:device_id>/control/', views.control_device, name='control_device'),

    # Детальная страница комнаты
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),

    # Активация сценария
    path('scene/<int:scene_id>/activate/', views.activate_scene, name='activate_scene'),

    # Статистика (API)
    path('stats/', views.device_stats, name='device_stats'),
]