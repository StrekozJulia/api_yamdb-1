import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User

from .validators import UsernameValidator


class SingUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.filter(
                created_by_admin=False))
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UsernameValidator(),
            UniqueValidator(queryset=User.objects.filter(
                created_by_admin=False))
        ]
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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        """Проверка корректности года выпуска."""
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска произведения позже текущего!'
            )
        return value


class UsersSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='username должен быть уникальным')]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')


class UserProfileSerializer(UsersSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    """Изменение данных отзыва."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        validators=[UniqueTogetherValidator('author', 'title')]
    )

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценкой должна быть в диапазоне от 1 до 10.'
            )
        return value

    def validate(self, data):
        request = self.context.get('request')

        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                    author=request.user, title=title).exists():
                raise serializers.ValidationError(
                    'Вы можете написать только один отзыв '
                    'к данному произведению.'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Изменение данных комментария."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
