import json
from rest_framework.test import APIClient, APITestCase
from shopinc.apps.product.models import Product


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = {
            "name": "product1",
            "description": "asdfgh", "slug": "name-123456d", "price": 1234, "added_at": "2019-2-19",
            "updated_at": "2019-4-12", "image_url": "sdfgh"
        }

        self.slug = dict(self.create_product().data)['slug']

    def create_product(self):
        return self.client.post("/api/products/", self.product)

    def get_product(self):
        return self.client.get("/api/products/")

    def get_single_product(self):
        return self.client.get(f"/api/products/{self.slug}")

    def get_nonexisting_product(self):
        return self.client.get("/api/products/$%&*^(&&&&")
