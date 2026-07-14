from  django.urls import path
from  . import views

urlpatterns = [
    path('', views.hello_en, name = 'hello_en'),
    path('fr/', views.hello_fr, name = 'hello_fr' ),
    path('de/', views.hello_de, name='hello_de'),
    path('es/', views.hello_es, name='hello_es')
]