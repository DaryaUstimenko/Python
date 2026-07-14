from django.urls import path
from .views import DateTimeView

urlpatterns = [
    path('datetime/', DateTimeView.as_view(), name='datetime'),
    path('greeting/', DateTimeView.as_view(), name='greeting'),
]
