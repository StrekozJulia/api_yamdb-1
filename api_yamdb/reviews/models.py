from django.contrib.auth.models import AbstractUser
from django.db import models


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
