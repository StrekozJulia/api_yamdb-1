from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .managers import CustomUserManager

SLUG_LEN = 50
NAME_LEN = 256
USER_LEN = 150
COM_LEN = 15


class User(AbstractUser):
    """Кастомная модель для юзера"""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    WEB = 'web'
    APP = 'appp'

    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    CREATED = [
        (ADMIN, 'Администратор'),
        (WEB, 'Веб'),
        (APP, 'Приложение'),
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
                            max_length=SLUG_LEN,
                            choices=ROLES, default=USER)
    created_by = models.CharField('Источник создания пользователя',
                                  max_length=SLUG_LEN,
                                  choices=CREATED, default=APP)
    object = CustomUserManager()

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_name_email'
            )
        ]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.username


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


class Review(models.Model):
    """Модель Review, привязанная к определённому произведению."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(
        max_length=2500,
        verbose_name='Текст отзыва',
        help_text='Добавьте Ваш отзыв'
    )
    score = models.PositiveIntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        ),
        default=1,
        error_messages=(
            {'validators': 'Поставьте оценку от 1 до 10.'}
        ),
        verbose_name='Оценка произведения',
        help_text='Поставьте оценку'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review',
            )
        ],
        ordering = ['-pub_date']


class Comment(models.Model):
    """Модель Comment, привязанная к определённому отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст комментария',
        help_text='Добавьте Ваш комментарий'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.text[:COM_LEN]

    class Meta:
        ordering = ['-pub_date']
