# Инструкция по сопровождению
> Руководство для технического обслуживанию
---
## Содержание
1. [Архитектура системы](#1-архитектура-системы)
2. [Структура проекта](#2-структура-проекта)
3. [Резервное копирование](#3-резервное-копирование)
4. [Обновление системы](#4-обновление-системы)
5. [Мониторинг и логирование](#5-мониторинг-и-логирование)
6. [Типичные проблемы и их решение](#6-типичные-проблемы-и-их-решение)
7. [Управление данными](#7-управление-данными)
8. [Безопасность](#8-безопасность)

---
## 1. Архитектура системы
```
┌──────────────────────────────────────────────┐
│                 Браузер клиента               │
└───────────────────────┬──────────────────────┘
                        │ HTTP/HTTPS
┌───────────────────────▼──────────────────────┐
│              Nginx (reverse proxy)            │
│          /static/  →  staticfiles/            │
│          /media/   →  media/                  │
│          /         →  Gunicorn :8000          │
└───────────────────────┬──────────────────────┘
                        │
┌───────────────────────▼──────────────────────┐
│         Django 5.1 (Gunicorn WSGI)            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │accounts  │  │appointments│ │  staff   │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │services  │  │ billing  │  │analytics │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────┬──────────────────────┘
                        │
┌───────────────────────▼──────────────────────┐
│           PostgreSQL 14+                      │
└──────────────────────────────────────────────┘
```
---
## 2. Структура проекта
```
barbershop_crm/
├── apps/
│   ├── accounts/       # Пользователи и роли
│   ├── appointments/   # Записи клиентов, API
│   ├── billing/        # Платежи и сигналы
│   ├── services/       # Услуги и категории
│   ├── staff/          # Мастера и расписание
│   └── analytics/      # Статистика
├── config/
│   ├── settings/
│   │   ├── base.py         # Общие настройки
│   │   ├── development.py  # Dev-overrides
│   │   └── production.py   # Prod-overrides
│   ├── urls.py
│   └── wsgi.py
├── docs/               # Документация (этот файл)
├── static/             # Исходные статические файлы
├── staticfiles/        # Скомпилированная статика
├── media/              # Загруженные файлы
├── templates/          # HTML-шаблоны
└── manage.py
```
### Ключевые модели

| Модель | Приложение | Назначение |
|--------|-----------|-----------|
| `User` + `UserProfile` | accounts | Учётные записи и роли |
| `Master` | staff | Профиль мастера |
| `WorkSchedule` | staff | Расписание мастера по дням |
| `Service` / `ServiceCategory` | services | Услуги |
| `Appointment` | appointments | Записи клиентов |
| `Payment` | billing | Оплата записей |

---
## 3. Резервное копирование
### 3.1. Резервная копия базы данных
```bash
# Создание дампа
pg_dump -U crm_user -F c barbershop_crm > backup_$(date +%Y%m%d).dump
# Восстановление из дампа
pg_restore -U crm_user -d barbershop_crm backup_20260517.dump
```
| Параметр | Значение |
|----------|---------|
| `-F c` | Формат custom (сжатый) |
| `-U` | Пользователь PostgreSQL |
| `-d` | Целевая база данных |

### 3.2. Резервная копия медиафайлов
```bash
# Архивирование папки media/
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
# Восстановление
tar -xzf media_backup_20260517.tar.gz
```
### 3.3. Рекомендуемое расписание бэкапов

| Тип | Частота | Хранение |
|-----|---------|---------|
| БД (полный дамп) | Ежедневно в 03:00 | 30 дней |
| Медиафайлы | Еженедельно | 4 недели |
| Полный сервер | Ежемесячно | 3 месяца |
Пример cron-задания:
```cron
0 3 * * * pg_dump -U crm_user -F c barbershop_crm > /backups/db_$(date +\%Y\%m\%d).dump
```
---
## 4. Обновление системы
### 4.1. Обновление кода
```bash
# Получение изменений
git pull origin master

# Обновление зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Обновление статики
python manage.py collectstatic --noinput

# Перезапуск Gunicorn
sudo systemctl restart gunicorn
```

### 4.2. Создание и применение миграций
При изменении моделей:
```bash
# Создание миграции
python manage.py makemigrations <app_name>
# Предварительный просмотр SQL
python manage.py sqlmigrate <app_name> 0001
# Применение
python manage.py migrate
```
### 4.3. Откат миграции
```bash
# Откат до конкретной миграции
python manage.py migrate <app_name> 0002

# Полный откат приложения
python manage.py migrate <app_name> zero
```
---
## 5. Мониторинг и логирование
### 5.1. Настройка логирования в `base.py`

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```
### 5.2. Полезные команды

```bash
# Просмотр последних ошибок
tail -n 100 logs/django.log

# Поиск ошибок 500
grep "ERROR" logs/django.log | tail -50

# Статус Gunicorn
sudo systemctl status gunicorn

# Перезапуск без прерывания (zero-downtime)
sudo kill -HUP $(cat gunicorn.pid)
```
### 5.3. Метрики для мониторинга

| Метрика | Норма | Действие при превышении |
|---------|-------|------------------------|
| Время ответа `/` | < 200 мс | Проверить БД-запросы |
| Ошибки 500 в сутки | < 5 | Проверить логи |
| Место на диске | > 20% свободно | Очистить старые бэкапы |
| Размер БД | Мониторинг | Архивировать старые записи |

---
## 6. Типичные проблемы и их решение
### Мастер не отображается на странице записи

**Причина:** Не создан профиль `staff_master` или мастер неактивен.

```bash
python manage.py shell
```

```python
from apps.staff.models import Master
# Проверить активных мастеров
Master.objects.filter(is_active=True).values('id', 'display_name', 'user')
```

**Решение:** Убедитесь, что у мастера `is_active=True` и создан `WorkSchedule` хотя бы для одного рабочего дня.

---
### Нет доступных слотов для записи

**Причина:** У мастера нет записей в `WorkSchedule` или все слоты заняты.

```python
from apps.staff.models import WorkSchedule
# Расписание конкретного мастера
WorkSchedule.objects.filter(master_id=1).values(
    'weekday', 'start_time', 'end_time', 'is_day_off'
)
```

---
### Ошибка `500` после обновления

**Шаги диагностики:**

1. Проверить логи:
   ```bash
   tail -n 50 logs/django.log
   ```
2. Убедиться, что миграции применены:
   ```bash
   python manage.py showmigrations | grep "\[ \]"
   ```
3. Проверить статику:
   ```bash
   python manage.py collectstatic --noinput
   ```

---
### Медленная работа календаря

API `/appointments/api/events/` возвращает слишком много записей.

```python
# apps/appointments/views.py
# Проверить, что фильтр по дате работает корректно
Appointment.objects.filter(
    start__date__gte=start_date,
    start__date__lte=end_date
).select_related('master', 'service', 'client')
```

Добавьте индексы при необходимости:

```python
class Appointment(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['master', 'start']),
        ]
```

---
## 7. Управление данными
### 7.1. Django shell — полезные команды

```bash
python manage.py shell
```

```python
# Список всех мастеров
from apps.staff.models import Master
Master.objects.all().values('id', 'display_name', 'is_active')

# Записи за сегодня
from apps.appointments.models import Appointment
from django.utils import timezone
today = timezone.now().date()
Appointment.objects.filter(start__date=today).count()

# Выручка за месяц
from django.db.models import Sum
from apps.billing.models import Payment
Payment.objects.filter(
    created_at__month=timezone.now().month
).aggregate(total=Sum('amount'))
```

### 7.2. Очистка старых записей

```python
# Архивирование записей старше 2 лет
import datetime
cutoff = datetime.date.today() - datetime.timedelta(days=730)
old_appts = Appointment.objects.filter(start__date__lt=cutoff, status='done')
print(f"К архивированию: {old_appts.count()} записей")
# old_appts.delete()  # раскомментировать после проверки
```

---
## 8. Безопасность
### 8.1. Обязательные настройки для продакшна

```python
# config/settings/production.py
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']   # только из переменной окружения
ALLOWED_HOSTS = ['yourdomain.com']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = 'DENY'
```

### 8.2. Ротация SECRET_KEY

При компрометации ключа:

1. Сгенерировать новый:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```
2. Обновить в `.env` или переменных окружения сервера.
3. Перезапустить Gunicorn — все активные сессии будут сброшены.

### 8.3. Обновление зависимостей

```bash
# Проверка уязвимостей
pip install pip-audit
pip-audit

# Обновление конкретного пакета
pip install --upgrade Django

# Фиксация версий
pip freeze > requirements.txt
```

| Компонент | Частота проверки |
|-----------|----------------|
| Django | При каждом минорном релизе |
| psycopg2 | Ежеквартально |
| Pillow | Ежеквартально |
| Все зависимости | Перед каждым деплоем |
