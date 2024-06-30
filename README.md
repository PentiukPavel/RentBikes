# RentBikes
Бекэнд для сервиса по аренде велосипедов"</br>
[![RentBike](https://github.com/PentiukPavel/RentBikes/actions/workflows/rent_bike.yaml/badge.svg)](https://github.com/PentiukPavel/RentBikes/actions/workflows/rent_bike.yaml/)

## Описание
Приложение для аренды велоспиедов

## Для разработчиков:

### Приложения:
- _config_: основные настройки проекта;
- _core_: общие файлы проекта;
- _api_: API;

- users: управление пользователями;
- bicycles: логика работы с велосипедами;
- orders: логика работы с арендами.

### Пример файла с переменными среды:
".env.example" в корневой папке проекта:

### Линтер:
`black`

### Pre-commit:
Настроен pre-commit для проверки оформления кода.
Для проверки кода перед выполнением операции commit, выполнить команду:

```
pre-commit run --all-files
```

## Как запустить проект:

Клонировать проект
```
git clone https://github.com/PentiukPavel/RentBikes.git
```

Переименовать файл .env.example и изменить содержимое на актуальные данные.
```
mv .env.example .env
```

### 1) Запуск проекта на локальной машине (без Docker):

Создать виртуальное окружение:
```
py -3 -m venv venv
```

Активировать виртуальное окружение:
```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

В папке с файлом manage.py (./src) выполнить следующие команды для миграций:
```
python manage.py migrate
```

Создать суперюзера:
```
python manage.py createsuperuser
```

Запустить проект:
```
python manage.py runserver
```

### 2) Запуск через Docker:
Запустить контейнер c проектом
```
docker-compose up -d
```

Выполнить миграции:
```
docker-compose exec backend python manage.py migrate
```

Проект будет доступен на 8000 порту.
Swager доступен по адресу:
```
http://localhost:8000/api/v1/docs/
```

Если отсутствуют статические файлы, то выполнить
```
docker-compose exec backend python manage.py collectstatic --no-input
```

## Системные требования
### Python==3.12

## Стек
### Django
### Django REST Framework
### PosrgreSQL
