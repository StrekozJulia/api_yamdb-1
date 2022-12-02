from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, views, viewsets, mixins, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Title, Category, Genre, User 

from .serializers import (TitleSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          ReceiveTokenSerializer,
                          SingUpSerializer)
from .permissions import AdminOrReadOnly


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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
