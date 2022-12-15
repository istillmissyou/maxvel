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
SECRET_KEY=<...>
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=example_password
TELEGRAM_TOKEN=TELEGRAM_TOKEN
CHAT_ID=CHAT_ID
EMAIL_USER=Почта куда будут приходить сообщения
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

* Во втором терминале запустить Celery в директории где находиться manage.py предварительно запустив Redis:
```bash
celery -A maxvel worker -l info -P gevent
```

## Запуск проекта в Docker контейнере


---
## Техническая информация
