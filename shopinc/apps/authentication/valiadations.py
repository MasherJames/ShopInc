import re
from rest_framework import serializers
from .models import User


def validate_registration(data):
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    if not re.match("^[^@]+@[^@]+\.[^@]+$", email):
        raise serializers.ValidationError(
            {
                "Message": "Invalid email entered"
            }
        )

    user = User.objects.filter(email=email)

    if user.exists():
        raise serializers.ValidationError(
            {
                "Message": "User with this email already exists"
            }
        )

    if not re.match("^[A-Za-z]+[\d\w_]{3,}", username):
        raise serializers.ValidationError({
            "Username": "Username should start with a letter, can have digits or underscore and be > 3 chars"
        })

    if not re.match(
        "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{8,15}$", password
    ):
        raise serializers.ValidationError(
            {
                "Message": "Incorrect password => 1 caps, digit and small"
            }
        )

    return{"username": username, "email": email, "password": password}
