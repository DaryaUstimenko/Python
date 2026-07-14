from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('greetengs.urls')),
    path('', include('sports.urls')),
    path('', include('datetime_app.urls')),
    path('', include('recipes.urls')),
]
