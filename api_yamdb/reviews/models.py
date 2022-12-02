from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

SLUG_LEN = 50
NAME_LEN = 256


class UserManager(BaseUserManager):
    """Кастомный юзер менеджер"""
    def create_user(self, email, username, **extra_fields):
        """Создаём пользователя с username и email."""
        if User.objects.get(email=email):
            raise ValueError(_('Такой email уже существует'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password, username, **extra_fields):
        """Создаём суперпользователя и присваиваем ему роль админ."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if User.objects.get(email=email):
            raise ValueError(_('Такой email уже существует'))
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.role = 'admin'
        user.save()
        return user


class User(AbstractUser):
    """Кастомная модель для юзера"""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField('Имя пользователя', max_length=150,
                                unique=True, blank=False, null=False)
    email = models.EmailField('Электронная почта', max_length=254, unique=True,
                              blank=False, null=False)
    first_name = models.CharField('Имя', max_length=150, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=150,
                                 null=True, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль',
                            max_length=max(len(role) for role, _ in ROLES),
                            choices=ROLES, default=USER)
    objects = UserManager()


class Characteristic(models.Model):
    """Абстрактная модель характеристики произведения"""

    class Meta:
        abstract = True
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    name = models.CharField('Название', max_length=NAME_LEN,
                            unique=True, blank=False, null=False,
                            db_index=True)
    slug = models.SlugField('Слаг', max_length=SLUG_LEN,
                            unique=True, blank=False, null=False)

    def __str__(self):
        return self.name


class Category(Characteristic):
    """Модель категории произведения"""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(Characteristic):
    """Модель жанра произведения"""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField('Название', max_length=NAME_LEN,
                            blank=False, null=False, db_index=True)
    year = models.IntegerField('Год выпуска', blank=False,
                               null=False, db_index=True)
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связи произведений с их жанрами"""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['genre', 'title'], name='unique_genre_title'
        )]

    def __str__(self):
        return f'{self.genre} {self.title}'
