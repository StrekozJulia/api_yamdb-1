from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User

from .permissions import IsAdmin
from .serializers import (ReceiveTokenSerializer, SingUpSerializer,
                          UserProfileSerializer, UsersSerializer)


class SignUp(views.APIView):
    """Получить код подтверждения на переданный email."""

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
        send_mail(
            'Код подтверждения api_yamdb',
            f'Ваш код подтверждения: "{confirmation_code}"',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReceiveToken(views.APIView):
    """Получение токена при регистрации."""

    def post(self, requset):
        serializer = ReceiveTokenSerializer(data=requset.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response({
            'confirmation_code': 'Вы ввели неверный confirmation_code'
        },
            status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdmin]
    lookup_field = ('username')

    @action(
        methods=['get', 'patch'], url_path='me', detail=False,
        permission_classes=[permissions.IsAuthenticated])
    def user_profile(self, request):
        user = User.objects.get(username=request.user)
        if request.method == 'PATCH':
            serializer = UserProfileSerializer(user, data=request.data,
                                               partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
