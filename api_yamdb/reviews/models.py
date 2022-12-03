from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

SLUG_LEN = 50
NAME_LEN = 256
USER_LEN = 150


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

    username = models.CharField('Имя пользователя', max_length=USER_LEN,
                                unique=True, blank=False, null=False)
    email = models.EmailField('Электронная почта', max_length=NAME_LEN,
                              unique=True, blank=False, null=False)
    first_name = models.CharField('Имя', max_length=USER_LEN, blank=True)
    last_name = models.CharField('Фамилия', max_length=NAME_LEN,
                                 blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль',
                            max_length=max(len(role) for role, _ in ROLES),
                            choices=ROLES, default=USER)


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
