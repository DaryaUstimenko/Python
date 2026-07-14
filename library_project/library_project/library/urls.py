from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('readers/', views.reader_list, name='reader_list'),
    path('readers/<int:pk>/', views.reader_detail, name='reader_detail'),
    path('books/all/', views.all_books, name='all_books'),
    path('books/available/', views.available_books, name='available_books'),
]
