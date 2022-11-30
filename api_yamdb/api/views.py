from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail
from rest_framework import status, views
from rest_framework.response import Response
from reviews.models import User

from .serializers import SingUpSerializer


class SignUp(views.APIView):

    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email')
        )
        confirmation_code = default_token_generator.make_token(user)
        email = EmailMessage(
            'Код подтверждения api_yamdb',
            f'Ваш код подтверждения: "{confirmation_code}"',
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.send()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
