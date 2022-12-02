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
