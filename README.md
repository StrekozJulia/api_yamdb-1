# Сервис API для взаимодействия с проектом Yatube
____
## Yatube - социальная сеть для блогеров

Создавайте посты от своего имени или в тематических сообществах, комментируйте, подписывайтесь на авторов.
____

### Как запустить проект:

+ Клонировать репозиторий 
git clone https://github.com/StrekozJulia/api_final_yatube.git

+ Перейти в него в командной строке
cd api_final_yatube

+ Cоздать виртуальное окружение
py -3.7 -m venv venv

+ Активировать виртуальное окружение
source venv/scripts/activate

+ Обновить пакетный установщик
py -3.7 -m pip install --upgrade pip

+ Установить зависимости из файла requirements.txt
pip install -r requirements.txt

+ Выполнить миграции
python manage.py migrate

+ Запустить проект
python manage.py runserver
____
## Доступные запросы к API:

+ http://127.0.0.1.8000/api/v1/users/ - создание нового пользователя
    Тип запроса: POST
    Передаваемые данные: {"username": string, "password": string}

+ http://127.0.0.1.8000/api/v1/jwt/create/ - создание токена
    Тип запроса: POST
    Передаваемые данные: {"username": string, "password": string}

+ http://127.0.0.1.8000/api/v1/jwt/refresh/ - получение токена
    Тип запроса: POST
    Передаваемые данные: {"refresh": string}

+ http://127.0.0.1.8000/api/v1/jwt/verify/ - валидация токена
    Тип запроса: POST
    Передаваемые данные: {"token": string}

+ http://127.0.0.1.8000/api/v1/posts/ - доступ к списку публикаций
    Тип запроса: GET, POST
    Передаваемые данные (POST): {"text": string, 
                                "image": string or null,
                                "group": string or null}

+ http://127.0.0.1.8000/api/v1/posts/{id}/ - доступ к одиночной публикации по id
    Тип запроса: GET, PUT, PATCH, DELETE 
    Передаваемые данные (PUT, PATCH): {"text": string, 
                                      "image": string or null,
                                      "group": string or null}

+ http://127.0.0.1.8000/api/v1/posts/{post_id}/comments/ - доступ к списку комментариев к посту 
    Тип запроса: GET, POST
    Передаваемые данные (PUT, PATCH): {"text": string}

+ http://127.0.0.1.8000/api/v1/posts/{post_id}/comments/{id} - доступ к одиночному комментарию к посту по id
    Тип запроса: GET, PUT, PATCH, DELETE 
    Передаваемые данные (PUT, PATCH): {"text": string}

+ http://127.0.0.1.8000/api/v1/groups/ - доступ к списку сообществ
    Тип запроса: GET

+ http://127.0.0.1.8000/api/v1/posts/{id}/ - доступ к одиночному сообществу по id
    Тип запроса: GET

+ http://127.0.0.1.8000/api/v1/follow/ - доступ к подпискам пользователя
    Тип запроса: GET, PUT
    Передаваемые данные (PUT): {"following": string}

+ http://127.0.0.1.8000/api/v1/follow/?search=string - поиск автора среди подписок пользователя
    Тип запроса: GET
