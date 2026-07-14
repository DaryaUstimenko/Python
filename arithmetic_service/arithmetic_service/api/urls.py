from django.urls import path
from .views import ArithmeticOperationsView
from .views import PowerOperationView

urlpatterns = [
    path('operations/', ArithmeticOperationsView.as_view(), name='arithmetic_operations'),
    path('power/', PowerOperationView.as_view(), name='power_operation'),
]
