import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("User must have a username")

        if email is None:
            raise TypeError("User must have an email")

        user = self.model(
            username=username, email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError("Superuser must have a password")

        user = self.create_user(
            username=username, email=email, password=password)
        user.is_superuser()
        user.is_staff()
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def token(self):
        expiry_date = datetime.now() + timedelta(hours=24)
        token = jwt.encode({
            'id': self.pk,
            'username': self.get_short_name(),
            'exp': int(expiry_date.strftime('%s'))
        }, settings.SECRET_KEY, algorithm="HS256")

        return token.decode('utf-8')
