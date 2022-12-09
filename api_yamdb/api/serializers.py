import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .validators import UsernameValidator


class SingUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True,
    )
    username = serializers.CharField(
        required=True,
        validators=[UsernameValidator()]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не может быть 'me'"
            )
        return value

    def validate(self, attrs):
        if User.object.filter(
                username=attrs.get('username'),
                email=attrs.get('email')).exists():
            pass
        elif (User.object.filter(username=attrs.get('username')).exists()
                and not User.object.filter(email=attrs.get('email')).exists()):
            raise serializers.ValidationError(
                "Пользователь с таким username уже есть."
            )
        elif (User.object.filter(email=attrs.get('email')).exists()
                and not User.object.filter(
                    username=attrs.get('username')).exists()):
            raise serializers.ValidationError(
                "Пользователь с таким email уже есть."
            )
        return attrs


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


class ReadTitleSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category')


class WriteTitleSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField(required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        return ReadTitleSerializer(instance=instance).data

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

    def validate(self, attrs):
        request = self.context.get('request')

        if not self.instance:
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                    author=request.user, title__id=title_id).exists():
                raise serializers.ValidationError(
                    'Вы можете написать только один отзыв '
                    'к данному произведению.'
                )
        return attrs

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
