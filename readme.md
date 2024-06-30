# Подключение пакета
1. Собрать пакет: в директории diploma-frontend выполнить команду 
```
python setup.py sdist
```
2. Установить полученный пакет в виртуальное окружение:

```
pip install diploma-frontend-X.Y.tar.gz
```

X и Y - числа, они могут изменяться в зависимости от текущей версии пакета.

Если запустить сервер разработки: `python manage.py runserver --settings=mysite.settings.local`, то по адресу `127.0.0.1:8000` должна открыться стартовая страница интернет-магазина

# API Documentation

## Аутентификация

- **POST /sign-in**: 
  - Авторизация пользователя.
  - *Запрос*: `{ "username": "exampleUser", "password": "examplePass" }`
  - *Ответ*: `{ "token": "yourAuthToken" }`

- **POST /sign-up**: 
  - Регистрация нового пользователя.
  - *Запрос*: `{ "name": "Example User", "username": "exampleUser", "password": "examplePass" }`
  - *Ответ*: `{ "id": 1, "username": "exampleUser" }`

- **GET /sign-out**: 
  - Выход из системы.

## Профиль пользователя

- **GET /profile**: 
  - Получение информации о профиле текущего пользователя.
  - *Ответ*: `{ "fullName": "Example User", "email": "user@example.com", "avatar": "http://link.to/avatar.png" }`

- **PUT /profile/password**: 
  - Изменение пароля пользователя.
  - *Запрос*: `{ "oldPassword": "oldPass", "newPassword": "newPass" }`
  - *Ответ*: `{ "status": "success" }`

- **POST /profile/avatar**: 
  - Загрузка аватара пользователя.
  - *Запрос*: `multipart/form-data` с файлом изображения в поле `avatar`.
  - *Ответ*: `{ "src": "http://link.to/new/avatar.png" }`

## Продукты и категории

- **GET /categories**: 
  - Получение списка всех категорий.
  - *Ответ*: `[{"id": 1, "title": "Electronics"},...]`

- **GET /product/<int:id>**: 
  - Получение информации о продукте по его ID.
  - *Ответ*: `{ "id": 1, "title": "iPhone X", "price": 999.99, "description": "Latest iPhone model." }`

- **GET /products/popular**: 
  - Получение списка популярных продуктов.
  - *Ответ*: `[{"id": 1, "title": "iPhone X", "price": 999.99},...]`

## Заказы

- **GET /orders**: 
  - Получение списка заказов для текущего пользователя.
  - *Ответ*: `[{"id": 1, "createdAt": "2024-06-30", "totalCost": 1999.98},...]`

- **POST /order**: 
  - Создание нового заказа.
  - *Запрос*: `{ "products": [{"productId": 1, "quantity": 2}], "deliveryType": "Courier", "paymentType": "Card" }`
  - *Ответ*: `{ "id": 2, "status": "Pending" }`