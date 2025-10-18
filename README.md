# WEB HOTEL

Веб-приложение для отеля.

Демонстрация работы приложения:
https://github.com/user-attachments/assets/f050c6a4-4379-4ab6-ac92-194134d2944e

Схема БД:
<img alt="Схема БД" src="https://github.com/user-attachments/assets/7b67ceb5-b104-47ae-a0e1-99b600696fd7" />

## Начало работы

Эти инструкции предоставят вам копию проекта и помогут запустить на вашем локальном компьютере для разработки и тестирования.

### Необходимые условия

Для работы приложения необходимы библиотеки Django и Psycopg2:

```
pip install django psycopg2-binary
```

### Установка

Для установки необходимо скопировать данный репозиторий:

```
git clone https://github.com/fake-stmz/web-hotel
cd web-hotel/hotel_business
```

### Настройка

Укажите в файле settings.py в hotel_business/hotel_business/ настройки подключений к вашей БД. Пример:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.СУБД',
        'NAME': 'ИМЯ_БД',
        'USER': 'ПОЛЬЗОВАТЕЛЬ',
        'PASSWORD': 'ПАРОЛЬ',
        'HOST': 'АДРЕС_ХОСТА',
        'PORT': ПОРТ
    }
}
```

Затем мигрируйте БД:

```
python manage.py migrate
```

### Запуск

Запуск проводится следующей командой:

```
python manage.py runserver
```

После чего сервер веб-приложения будет запущен на порту 8000

## Автор

* **STMZ** - [fake-stmz](https://github.com/fake-stmz)
