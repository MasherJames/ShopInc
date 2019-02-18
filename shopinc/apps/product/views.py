import uuid
from rest_framework import generics, status
from rest_framework.response import Response
from django.template.defaultfilters import slugify

from .models import Product
from .serializers import ProductSerializer


class ListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request):
        product = request.data

        slug = slugify(product['name']).replace("_", "-")
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        product["slug"] = slug

        serializer = self.serializer_class(data=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data['message'] = "Your product was successfully created"
        return Response(serializer.data, status=status.HTTP_201_CREATED)
