# Ключевые фрагменты кода — The Cut Barbershop CRM

> Описание важных технических решений с фрагментами исходного кода.

---

## Содержание

1. [Защита от двойной записи на один слот](#1-защита-от-двойной-записи-на-один-слот)
2. [Автоматический расчёт времени окончания записи](#2-автоматический-расчёт-времени-окончания-записи)
3. [Конвертация часовых поясов при расчёте слотов](#3-конвертация-часовых-поясов-при-расчёте-слотов)

---

## 1. Защита от двойной записи на один слот

**Файл:** `apps/booking/views.py` — `BookingSubmitView`

Если два клиента одновременно выбирают один и тот же слот, оба запроса могут
пройти предварительную проверку свободного времени и попасть в базу данных
одновременно — возникает «гонка запросов».

Для устранения этой ситуации финальная проверка пересечений выполняется внутри
`transaction.atomic()`. Метод `select_for_update()` блокирует затронутые строки на
уровне БД: второй запрос ждёт завершения первого, после чего видит уже созданную
запись и возвращает ошибку 409.

```python
# apps/booking/views.py
with transaction.atomic():
    overlap = Appointment.objects.select_for_update().filter(
        master=master,
        start_time__lt=end_dt,
        end_time__gt=start_dt,
    ).exclude(
        status__in=[AppointmentStatus.CANCELLED, AppointmentStatus.NO_SHOW]
    )

    if overlap.exists():
        return JsonResponse(
            {'error': 'Это время уже занято. Пожалуйста, выберите другой слот.'},
            status=409
        )

    # Создание записи выполняется внутри той же транзакции
    appt = Appointment.objects.create(
        client=client,
        master=master,
        service=service,
        start_time=start_dt,
        status=AppointmentStatus.PENDING,
        notes=data.get('notes', ''),
    )
```

---

## 2. Автоматический расчёт времени окончания записи

**Файл:** `apps/appointments/models.py` — `Appointment.save()`

FullCalendar требует явного поля `end` для каждого события — без него блок записи
не отображается на временной шкале. Вместо того чтобы обязывать пользователя
вводить время окончания вручную, оно рассчитывается автоматически при сохранении:
берётся `start_time` и прибавляется длительность выбранной услуги в минутах.

```python
# apps/appointments/models.py
def save(self, *args, **kwargs):
    if self.service_id and not self.end_time:
        self.end_time = self.start_time + timedelta(minutes=self.service.duration)
    super().save(*args, **kwargs)
```

Пример: услуга «Классическая стрижка» длится 60 минут — запись на 14:00
автоматически получает `end_time = 15:00`.

---

## 3. Конвертация часовых поясов при расчёте слотов

**Файл:** `apps/booking/views.py` — `SlotsAPIView`

PostgreSQL хранит поля `start_time` и `end_time` модели `Appointment` в UTC
(timezone-aware datetime). Расписание мастера (`WorkSchedule.start_time`,
`WorkSchedule.end_time`) — это тип `time` без timezone, задаётся в локальном
времени сервера. При прямом сравнении этих значений слоты сдвигаются на величину
UTC-offset, и уже занятое время может выдаваться клиенту как свободное.

Решение: перед сравнением все datetime из базы данных конвертируются в локальное
время, после чего tzinfo снимается — оба значения становятся «наивными» и
сравниваются корректно.

```python
# apps/booking/views.py
local_existing = []
for appt_start, appt_end in existing:
    if appt_start and appt_start.tzinfo:
        appt_start = timezone.localtime(appt_start).replace(tzinfo=None)
    if appt_end and appt_end.tzinfo:
        appt_end = timezone.localtime(appt_end).replace(tzinfo=None)
    if appt_end is None:
        appt_end = appt_start + timedelta(minutes=30)
    local_existing.append((appt_start, appt_end))

# Проверка пересечения слота с уже занятыми интервалами
overlap = any(
    current < a_end and slot_end > a_start
    for a_start, a_end in local_existing
)
```
