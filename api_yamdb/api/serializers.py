from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import User

from .validators import UsernameValidator


class SingUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True
        # validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UsernameValidator(), ]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не может быть 'me'"
            )
        return value


class ReceiveTokenSerializer(serializers.Serializer):

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
