from django.urls import path
from .views import contact_list, contact_create, contact_delete

urlpatterns = [
    path('', contact_list, name='contact_list'),
    path('add/', contact_create, name='contact_create'),
    path('delete/<int:contact_id>/', contact_delete, name='contact_delete'),
]

