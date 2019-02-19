from django.urls import path
from .views import ListCreateAPIView, ProductRetrieve

urlpatterns = [
    path('products/', ListCreateAPIView.as_view()),
    path('products/<slug>', ProductRetrieve.as_view())
]
