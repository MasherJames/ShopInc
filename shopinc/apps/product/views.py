import uuid
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
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


class ProductRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug):
        try:
            data = self.queryset.get(slug=slug)
        except Product.DoesNotExist:
            raise NotFound("Product with this slug does not exist")

        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        try:
            saved_product = self.queryset.get(slug=slug)
        except Product.DoesNotExist:
            raise NotFound("Product with this slug does not exist")

        updated_prod_data = request.data

        serializer = self.serializer_class(
            saved_product, data=updated_prod_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, slug):
        try:
            product_to_destroy = self.queryset.get(slug=slug)
        except Product.DoesNotExist:
            raise NotFound("Product with this slug does not exist")

        self.perform_destroy(product_to_destroy)
        return Response({"Message": "Product deleted successfully"}, status=status.HTTP_200_OK)
