# Инструкция по развёртыванию — The Cut Barbershop CRM

> Пошаговое руководство по установке и запуску системы в локальной среде и на продакшн-сервере.

---

## Содержание

1. [Требования к окружению](#1-требования-к-окружению)
2. [Локальная установка (разработка)](#2-локальная-установка-разработка)
3. [Настройка базы данных](#3-настройка-базы-данных)
4. [Переменные окружения](#4-переменные-окружения)
5. [Первоначальное заполнение данных](#5-первоначальное-заполнение-данных)
6. [Развёртывание на продакшн-сервере](#6-развёртывание-на-продакшн-сервере)
7. [Статика и медиафайлы](#7-статика-и-медиафайлы)
8. [Запуск и проверка](#8-запуск-и-проверка)

---

## 1. Требования к окружению

### Программное обеспечение

| Компонент | Версия | Назначение |
|-----------|--------|-----------|
| Python | 3.12+ | Интерпретатор |
| PostgreSQL | 14+ | База данных |
| pip | 23+ | Менеджер пакетов |
| Git | любая | Клонирование репозитория |

### Аппаратные требования (минимум)

| Ресурс | Значение |
|--------|---------|
| CPU | 1 ядро |
| RAM | 512 МБ |
| Диск | 2 ГБ |

---

## 2. Локальная установка (разработка)

### 2.1. Клонирование репозитория

```bash
git clone https://github.com/laff1ck/barbershop-crm.git
cd barbershop-crm
```

### 2.2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 2.3. Установка зависимостей

```bash
pip install -r requirements.txt
```

Основные пакеты из `requirements.txt`:

| Пакет | Версия | Назначение |
|-------|--------|-----------|
| Django | 5.1 | Web-фреймворк |
| psycopg2-binary | 2.9+ | Драйвер PostgreSQL |
| Pillow | 10+ | Обработка изображений |
| django-widget-tweaks | 1.5+ | Кастомизация форм |

### 2.4. Копирование файла конфигурации

```bash
cp barbershop_crm/config/settings/development.py.example \
   barbershop_crm/config/settings/development.py
```

Отредактируйте `development.py` — укажите параметры БД (см. раздел 4).

---

## 3. Настройка базы данных

### 3.1. Создание базы данных в PostgreSQL

```sql
-- Подключитесь к PostgreSQL
psql -U postgres

-- Создайте пользователя и базу
CREATE USER crm_user WITH PASSWORD 'your_password';
CREATE DATABASE barbershop_crm OWNER crm_user;
GRANT ALL PRIVILEGES ON DATABASE barbershop_crm TO crm_user;
\q
```

### 3.2. Применение миграций

```bash
python barbershop_crm/manage.py migrate
```

Вывод успешного выполнения:

```
Operations to perform:
  Apply all migrations: accounts, admin, appointments, ...
Running migrations:
  Applying accounts.0001_initial... OK
  Applying staff.0001_initial... OK
  ...
```

---

## 4. Переменные окружения

Создайте файл `.env` в корне проекта (рядом с `manage.py`):

```ini
# Django
SECRET_KEY=your-very-long-random-secret-key
DEBUG=True

# База данных
DB_NAME=barbershop_crm
DB_USER=crm_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Файл `base.py` читает эти значения:

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-for-dev')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ.get('DB_NAME',     'barbershop_crm'),
        'USER':     os.environ.get('DB_USER',     'crm_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST':     os.environ.get('DB_HOST',     'localhost'),
        'PORT':     os.environ.get('DB_PORT',     '5432'),
    }
}
```

> **Никогда не коммитьте `.env` в репозиторий.** Он включён в `.gitignore`.

---

## 5. Первоначальное заполнение данных

### 5.1. Создание суперпользователя

```bash
python barbershop_crm/manage.py createsuperuser
```

Введите логин, email и пароль.

### 5.2. Сбор статики

```bash
python barbershop_crm/manage.py collectstatic --noinput
```

Статика копируется в директорию `staticfiles/`.

### 5.3. Добавление начальных данных (опционально)

```bash
python barbershop_crm/manage.py loaddata fixtures/initial_data.json
```

Фикстура содержит примеры категорий услуг и услуг.

---

## 6. Развёртывание на продакшн-сервере

### 6.1. Настройки продакшна

Создайте `config/settings/production.py`:

```python
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Безопасность
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

Запустите сервер с переменной `DJANGO_SETTINGS_MODULE`:

```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
```

### 6.2. Gunicorn

Установите Gunicorn:

```bash
pip install gunicorn
```

Запуск:

```bash
gunicorn config.wsgi:application \
  --workers 3 \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

| Параметр | Рекомендуемое значение |
|----------|----------------------|
| `--workers` | 2 × CPU + 1 |
| `--timeout` | 120 секунд |
| `--bind` | 0.0.0.0:8000 |

### 6.3. Nginx (reverse proxy)

Пример конфигурации `/etc/nginx/sites-available/barbershop`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /var/www/barbershop/staticfiles/;
    }

    location /media/ {
        alias /var/www/barbershop/media/;
    }

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
```

---

## 7. Статика и медиафайлы

| Директория | Содержимое |
|-----------|-----------|
| `static/` | Исходные CSS, JS, изображения |
| `staticfiles/` | Скомпилированная статика (после `collectstatic`) |
| `media/` | Загружаемые файлы (фото мастеров) |

В разработке статика раздаётся Django автоматически (`DEBUG=True`).

В продакшне — через Nginx (см. блок `location /static/` выше).

---

## 8. Запуск и проверка

### 8.1. Запуск в режиме разработки

```bash
python barbershop_crm/manage.py runserver
```

Откройте в браузере:

```
http://127.0.0.1:8000/        # CRM-панель
http://127.0.0.1:8000/book/   # Страница записи
```

### 8.2. Проверочный чек-лист

| Проверка | URL | Ожидаемый результат |
|----------|-----|---------------------|
| Стартовая страница | `/` | Дашборд без ошибок |
| Страница записи | `/book/` | Список мастеров |
| API событий | `/appointments/api/events/` | JSON-массив |
| Статика | `/static/css/main.css` | HTTP 200 |

### 8.3. Просмотр логов

```bash
# Django development server
python manage.py runserver 2>&1 | tee logs/django.log

# Gunicorn
gunicorn ... --log-file logs/gunicorn.log --log-level info
```
