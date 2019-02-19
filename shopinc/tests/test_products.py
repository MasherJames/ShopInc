from rest_framework import status
from django.test import TestCase
from shopinc.apps.product.models import Product
from .base_test import BaseTest


class ModelProductTest(TestCase):
    def setUp(self):
        self.product = Product(
            name="name", slug="name-123456d", description="asdfgh", price=1234,
            added_at="2019-2-19", updated_at="2019-4-12", image_url="sdfgh"
        )

    def test_model_can_create_a_product(self):
        """Test the bucketlist model can create a bucketlist."""
        old_count = Product.objects.count()
        self.product.save()
        new_count = Product.objects.count()
        self.assertNotEqual(old_count, new_count)


class ProductTest(BaseTest):

    def test_create_product(self):
        res = self.create_product()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', res.data)
