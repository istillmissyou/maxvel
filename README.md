# Проект maxvel

## Описание

## Установка бекэнда локально

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/istillmissyou/maxvel.git
```
```bash
cd backend
```

- Создать и заполнить по образцу .env-файл
```
secret_key=<...>
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

* Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

* Выполните миграции:
```bash
python manage.py migrate
```

* Создайте суперпользовтеля:
```bash
python manage.py createsuperuser
```

* Запустите сервер:
```bash
python manage.py runserver
```

## Запуск проекта в Docker контейнере


---
## Техническая информация
