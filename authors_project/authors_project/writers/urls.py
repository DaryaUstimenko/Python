from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('writers/', views.writers, name='writers'),
    path('writers/<slug:writer_slug>/', views.writer_detail, name='writer_detail'),
    path('books/', views.books, name='books'),
]