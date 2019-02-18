from django.urls import path
from .views import ListCreateAPIView

urlpatterns = [
    path('products/', ListCreateAPIView.as_view())
]
