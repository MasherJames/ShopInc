from rest_framework import generics
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class ListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request):
        product = request.data.get('product', {})
        serializer = self.serializer_class(data=product)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        data['message'] = "Your product was successfully created"
        return Response(serializer.data, status=status.HTTP_201_CREATED)
