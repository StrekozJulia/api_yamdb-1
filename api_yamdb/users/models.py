from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

SLUG_LEN = 50
NAME_LEN = 256
USER_LEN = 150


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
