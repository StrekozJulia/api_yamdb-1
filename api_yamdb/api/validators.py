from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя."""

    regex = r'^[\w.@+-]+\Z'
    MAX_LEN = 150
    max_length = MAX_LEN
    message = ('Введите правильное имя пользователя. Оно может содержать'
               ' только буквы, цифры и знаки @/./+/-/_.'
               f' Длина не более {MAX_LEN} символов')
