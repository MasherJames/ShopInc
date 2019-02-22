from rest_framework import status
from django.test import TestCase
from .base_test import BaseTest
from shopinc.apps.authentication.models import User


class ModelUserTest(TestCase):
    def setUp(self):
        self.user = User(
            username="James", email="james@gmail.com",
            password="Password123"
        )

    def test_model_can_create_a_product(self):
        """Test the bucketlist model can create a bucketlist."""
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)


class UserTest(BaseTest):
    def test_register_user(self):
        res = self.create_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', res.data)
        self.assertIn('email', res.data)
        self.assertIn('username', res.data)

    def test_register_with_invalid_username(self):
        res = self.create_user_with_invalid_username()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['Message'],
            "Username should start with a letter, can have digits or underscore and be > 3 chars")

    def test_register_with_invalid_email(self):
        res = self.create_user_with_invalid_email()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['Message'],
            "Invalid email entered"
        )

    def test_register_with_invalid_password(self):
        res = self.create_user_with_invalid_password()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['Message'],
            "Incorrect password => 1 caps, digit and small"
        )

    def test_login_user(self):
        self.create_user()
        res = self.login_user()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_nonexisting_user(self):
        data = {"email": "noemail@gmail.com", "password": "Validpass123"}
        res = self.client.post("/api/login/", data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
