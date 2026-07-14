from django.urls import path
from . import views

urlpatterns = [
    path('rec/', views.recipe_view, name='recipe_view'),
]
