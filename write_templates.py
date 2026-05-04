"""Write all Django templates for the Barbershop CRM."""
import os
BASE = r"D:\CRM\barbershop_crm"

def w(rel, content):
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  OK: {rel}")

# ── base.html ───────────────────────────────────────────────────────────────
w("templates/base.html", """{% load static %}<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{% block title %}BarberCRM{% endblock %} | The Cut</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <link rel="stylesheet" href="{% static 'css/theme.css' %}">
  {% block extra_head %}{% endblock %}
</head>
<body>
  {% include 'partials/_sidebar.html' %}
  <div class="crm-main" id="mainContent">
    {% include 'partials/_navbar.html' %}
    {% include 'partials/_messages.html' %}
    <main class="crm-content p-4">
      {% block content %}{% endblock %}
    </main>
  </div>
  <div id="toastContainer" class="toast-container"></div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="{% static 'js/main.js' %}"></script>
  {% block extra_scripts %}{% endblock %}
</body>
</html>
""")

# ── _sidebar.html ────────────────────────────────────────────────────────────
w("templates/partials/_sidebar.html", """{% load static %}
<aside class="crm-sidebar" id="sidebar">
  <div class="sidebar-logo">
    <div class="d-flex align-items-center gap-2">
      <div class="logo-icon"><i class="bi bi-scissors"></i></div>
      <div>
        <div class="logo-text">THE CUT</div>
        <div class="logo-sub">Barbershop CRM</div>
      </div>
    </div>
  </div>
  <nav class="sidebar-nav">
    <span class="sidebar-section-label">Главное</span>
    <a href="{% url 'core:dashboard' %}" class="nav-link {% if active_section == 'core' %}active{% endif %}">
      <i class="bi bi-speedometer2"></i> Дашборд
    </a>
    <a href="{% url 'appointments:calendar' %}" class="nav-link {% if active_section == 'appointments' %}active{% endif %}">
      <i class="bi bi-calendar3"></i> Календарь
    </a>
    <a href="{% url 'appointments:list' %}" class="nav-link">
      <i class="bi bi-list-ul"></i> Записи
    </a>
    <span class="sidebar-section-label">Клиенты и Мастера</span>
    <a href="{% url 'clients:list' %}" class="nav-link {% if active_section == 'clients' %}active{% endif %}">
      <i class="bi bi-people"></i> Клиенты
    </a>
    <a href="{% url 'staff:list' %}" class="nav-link {% if active_section == 'staff' %}active{% endif %}">
      <i class="bi bi-person-badge"></i> Мастера
    </a>
    <span class="sidebar-section-label">Услуги и Финансы</span>
    <a href="{% url 'services:list' %}" class="nav-link {% if active_section == 'services' %}active{% endif %}">
      <i class="bi bi-scissors"></i> Услуги
    </a>
    <a href="{% url 'billing:list' %}" class="nav-link {% if active_section == 'billing' %}active{% endif %}">
      <i class="bi bi-cash-coin"></i> Платежи
    </a>
    <a href="{% url 'billing:reports' %}" class="nav-link">
      <i class="bi bi-bar-chart-line"></i> Отчёты
    </a>
  </nav>
  <div class="sidebar-footer">
    {% if user.is_authenticated %}
    <div class="d-flex align-items-center gap-2">
      <div class="avatar-initials" style="width:32px;height:32px;font-size:.7rem">{{ user.username|slice:':2'|upper }}</div>
      <div class="flex-1" style="min-width:0">
        <div style="font-size:.8rem;color:var(--crm-text-primary);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ user.get_full_name|default:user.username }}</div>
        <a href="{% url 'logout' %}" style="font-size:.7rem;color:var(--crm-text-muted)">Выйти</a>
      </div>
    </div>
    {% endif %}
  </div>
</aside>
""")

# ── _navbar.html ─────────────────────────────────────────────────────────────
w("templates/partials/_navbar.html", """<nav class="navbar crm-navbar d-flex align-items-center">
  <button class="btn btn-ghost d-md-none me-2" id="sidebarToggle">
    <i class="bi bi-list" style="font-size:1.25rem"></i>
  </button>
  <div class="ms-auto d-flex align-items-center gap-3">
    <a href="{% url 'appointments:create' %}" class="btn btn-gold btn-sm">
      <i class="bi bi-plus-lg me-1"></i>Новая запись
    </a>
    {% if user.is_authenticated %}
    <span style="font-size:.8rem;color:var(--crm-text-muted)">{{ user.username }}</span>
    {% endif %}
  </div>
</nav>
""")

# ── _messages.html ────────────────────────────────────────────────────────────
w("templates/partials/_messages.html", """{% if messages %}
<div style="padding:0 1.5rem;margin-top:.5rem">
  {% for message in messages %}
  <div class="alert alert-dismissible auto-dismiss d-flex align-items-center gap-2
    {% if message.tags == 'error' %}alert-danger
    {% elif message.tags == 'warning' %}alert-warning
    {% elif message.tags == 'success' %}alert-success
    {% else %}alert-info{% endif %}"
    style="background:var(--crm-bg-elevated);border-color:var(--crm-border);color:var(--crm-text-primary)">
    {% if message.tags == 'success' %}<i class="bi bi-check-circle-fill text-success"></i>
    {% elif message.tags == 'error' %}<i class="bi bi-x-circle-fill text-danger"></i>
    {% else %}<i class="bi bi-info-circle-fill text-warning"></i>{% endif %}
    {{ message }}
    <button type="button" class="btn-close btn-close-white ms-auto" data-bs-dismiss="alert"></button>
  </div>
  {% endfor %}
</div>
{% endif %}
""")

# ── _pagination.html ──────────────────────────────────────────────────────────
w("templates/partials/_pagination.html", """{% if is_paginated %}
<nav class="d-flex justify-content-center mt-4">
  <ul class="pagination">
    {% if page_obj.has_previous %}
    <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for k,v in request.GET.items %}{% if k != 'page' %}&{{ k }}={{ v }}{% endif %}{% endfor %}"><i class="bi bi-chevron-left"></i></a></li>
    {% endif %}
    {% for num in page_obj.paginator.page_range %}
    {% if page_obj.number == num %}
    <li class="page-item active"><span class="page-link">{{ num }}</span></li>
    {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
    <li class="page-item"><a class="page-link" href="?page={{ num }}{% for k,v in request.GET.items %}{% if k != 'page' %}&{{ k }}={{ v }}{% endif %}{% endfor %}">{{ num }}</a></li>
    {% endif %}
    {% endfor %}
    {% if page_obj.has_next %}
    <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}{% for k,v in request.GET.items %}{% if k != 'page' %}&{{ k }}={{ v }}{% endif %}{% endfor %}"><i class="bi bi-chevron-right"></i></a></li>
    {% endif %}
  </ul>
</nav>
{% endif %}
""")

# ── login.html ────────────────────────────────────────────────────────────────
w("templates/registration/login.html", """{% load static %}<!DOCTYPE html>
<html lang="ru"><head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Войти | The Cut CRM</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <link rel="stylesheet" href="{% static 'css/theme.css' %}">
</head><body style="display:flex;align-items:center;justify-content:center;min-height:100vh;background:var(--crm-bg-primary)">
  <div style="width:100%;max-width:380px;padding:1rem">
    <div class="text-center mb-4">
      <div class="d-inline-flex align-items-center justify-content-center" style="width:64px;height:64px;background:var(--crm-gold-muted);border:1px solid var(--crm-gold-border);border-radius:16px;font-size:1.8rem;color:var(--crm-gold)">
        <i class="bi bi-scissors"></i>
      </div>
      <h1 class="mt-3" style="font-family:'Playfair Display',serif;color:var(--crm-gold);font-size:1.75rem">THE CUT</h1>
      <p style="color:var(--crm-text-muted);font-size:.8rem;text-transform:uppercase;letter-spacing:.15em">Barbershop CRM</p>
    </div>
    <div class="crm-card p-4">
      <form method="post">
        {% csrf_token %}
        {% if form.errors %}
        <div class="alert mb-3" style="background:rgba(220,53,69,.15);border-color:rgba(220,53,69,.3);color:#f66;border-radius:8px;font-size:.85rem">
          <i class="bi bi-exclamation-circle me-2"></i>Неверный логин или пароль
        </div>
        {% endif %}
        <div class="mb-3">
          <label class="form-label">Логин</label>
          <input name="username" type="text" class="form-control" placeholder="admin" autofocus>
        </div>
        <div class="mb-4">
          <label class="form-label">Пароль</label>
          <input name="password" type="password" class="form-control" placeholder="••••••••">
        </div>
        <button type="submit" class="btn btn-gold w-100">
          <i class="bi bi-box-arrow-in-right me-2"></i>Войти
        </button>
      </form>
    </div>
  </div>
</body></html>
""")

# ── core/dashboard.html ───────────────────────────────────────────────────────
w("templates/core/dashboard.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Дашборд{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title"><span>Дашборд</span></h1>
  <div style="font-size:.8rem;color:var(--crm-text-muted)">{{ today|date:'d E Y' }}</div>
</div>

<!-- KPI ROW -->
<div class="row g-3 mb-4">
  <div class="col-6 col-lg-3">
    <div class="kpi-card">
      <div class="kpi-icon" style="background:rgba(201,168,76,.15)"><i class="bi bi-currency-dollar text-warning"></i></div>
      <div class="kpi-value">{{ today_revenue|currency }}</div>
      <div class="kpi-label">Выручка сегодня</div>
    </div>
  </div>
  <div class="col-6 col-lg-3">
    <div class="kpi-card">
      <div class="kpi-icon" style="background:rgba(13,202,240,.1)"><i class="bi bi-calendar-check" style="color:#0dcaf0"></i></div>
      <div class="kpi-value">{{ appointments_today_count }}</div>
      <div class="kpi-label">Записей сегодня</div>
    </div>
  </div>
  <div class="col-6 col-lg-3">
    <div class="kpi-card">
      <div class="kpi-icon" style="background:rgba(25,135,84,.15)"><i class="bi bi-currency-exchange" style="color:#20c997"></i></div>
      <div class="kpi-value">{{ month_revenue|currency }}</div>
      <div class="kpi-label">Выручка за месяц</div>
    </div>
  </div>
  <div class="col-6 col-lg-3">
    <div class="kpi-card">
      <div class="kpi-icon" style="background:rgba(111,66,193,.15)"><i class="bi bi-people" style="color:#b189f5"></i></div>
      <div class="kpi-value">{{ total_clients }}</div>
      <div class="kpi-label">Всего клиентов</div>
    </div>
  </div>
</div>

<!-- TODAY SCHEDULE -->
<div class="crm-card">
  <div class="card-header d-flex justify-content-between align-items-center">
    <h6 class="card-title-gold mb-0"><i class="bi bi-calendar-day me-2"></i>Расписание на сегодня</h6>
    <a href="{% url 'appointments:calendar' %}" class="btn btn-ghost btn-sm">
      <i class="bi bi-grid-3x3-gap me-1"></i>Открыть календарь
    </a>
  </div>
  <div class="p-3">
    {% if today_appointments %}
    {% for appt in today_appointments %}
    <a href="{% url 'appointments:detail' appt.pk %}" style="text-decoration:none">
      <div class="appt-row">
        <span class="appt-time">{{ appt.start_time|date:'H:i' }}</span>
        <div class="avatar-initials">{{ appt.client.initials }}</div>
        <div class="flex-grow-1" style="min-width:0">
          <div style="font-weight:600;color:var(--crm-text-primary)">{{ appt.client.full_name }}</div>
          <div style="font-size:.78rem;color:var(--crm-text-muted)">{{ appt.service.name }} · {{ appt.master.display_name }}</div>
        </div>
        <div>
          <span class="badge-status status-{{ appt.status }}">{{ appt.get_status_display }}</span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace;color:var(--crm-gold);font-weight:700;white-space:nowrap">
          {{ appt.service.price|currency }}
        </div>
      </div>
    </a>
    {% endfor %}
    {% else %}
    <div class="text-center py-5" style="color:var(--crm-text-muted)">
      <i class="bi bi-calendar-x" style="font-size:2.5rem;display:block;margin-bottom:.75rem;opacity:.4"></i>
      На сегодня записей нет
    </div>
    {% endif %}
  </div>
</div>
{% endblock %}
""")

# ── clients/list.html ─────────────────────────────────────────────────────────
w("templates/clients/list.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Клиенты{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Клиент<span>ы</span></h1>
  <a href="{% url 'clients:create' %}" class="btn btn-gold"><i class="bi bi-plus-lg me-1"></i>Добавить</a>
</div>
<!-- Filters -->
<div class="crm-card mb-3 p-3">
  <form method="get" class="d-flex gap-2 flex-wrap">
    <div class="search-input-group flex-grow-1" style="max-width:320px">
      <i class="bi bi-search search-icon"></i>
      <input type="text" name="q" value="{{ q }}" class="form-control" placeholder="Имя, телефон...">
    </div>
    <select name="tier" class="form-select" style="max-width:160px">
      <option value="">Все уровни</option>
      {% for val,lbl in loyalty_tiers %}<option value="{{ val }}" {% if tier_filter == val %}selected{% endif %}>{{ lbl }}</option>{% endfor %}
    </select>
    <button type="submit" class="btn btn-gold"><i class="bi bi-search"></i></button>
    {% if q or tier_filter %}<a href="{% url 'clients:list' %}" class="btn btn-ghost">Сбросить</a>{% endif %}
  </form>
</div>
<!-- Table -->
<div class="crm-card">
  <div class="table-responsive">
    <table class="crm-table">
      <thead><tr>
        <th>Клиент</th><th>Телефон</th><th>Уровень</th>
        <th>Визиты</th><th>Потрачено</th><th>Последний визит</th><th></th>
      </tr></thead>
      <tbody>
        {% for c in clients %}
        <tr>
          <td>
            <div class="d-flex align-items-center gap-2">
              {% if c.photo %}<img src="{{ c.photo.url }}" class="avatar">
              {% else %}<div class="avatar-initials">{{ c.initials }}</div>{% endif %}
              <div>
                <div style="font-weight:600">{{ c.full_name }}</div>
                <div style="font-size:.75rem;color:var(--crm-text-muted)">{{ c.email }}</div>
              </div>
            </div>
          </td>
          <td style="font-family:'JetBrains Mono',monospace;font-size:.85rem">{{ c.phone }}</td>
          <td><span class="tier-badge tier-{{ c.loyalty_tier }}">
            {% if c.loyalty_tier == 'platinum' %}<i class="bi bi-gem"></i>
            {% elif c.loyalty_tier == 'gold' %}<i class="bi bi-star-fill"></i>
            {% elif c.loyalty_tier == 'silver' %}<i class="bi bi-star-half"></i>
            {% else %}<i class="bi bi-star"></i>{% endif %}
            {{ c.get_loyalty_tier_display }}
          </span></td>
          <td>{{ c.visit_count }}</td>
          <td style="font-family:'JetBrains Mono',monospace;color:var(--crm-gold)">{{ c.total_spent|currency }}</td>
          <td style="font-size:.8rem;color:var(--crm-text-muted)">
            {% if c.last_visit %}{{ c.last_visit|date:'d.m.Y' }}{% else %}—{% endif %}
          </td>
          <td>
            <a href="{% url 'clients:detail' c.pk %}" class="btn btn-ghost btn-sm">
              <i class="bi bi-eye"></i>
            </a>
          </td>
        </tr>
        {% empty %}
        <tr><td colspan="7" class="text-center py-4" style="color:var(--crm-text-muted)">Клиентов не найдено</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% include 'partials/_pagination.html' %}
</div>
{% endblock %}
""")

# ── clients/detail.html ───────────────────────────────────────────────────────
w("templates/clients/detail.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}{{ client.full_name }}{% endblock %}
{% block content %}
<div class="page-header">
  <div class="d-flex align-items-center gap-3">
    {% if client.photo %}<img src="{{ client.photo.url }}" class="avatar avatar-lg">
    {% else %}<div class="avatar-initials avatar-lg">{{ client.initials }}</div>{% endif %}
    <div>
      <h1 class="page-title mb-1">{{ client.full_name }}</h1>
      <div class="d-flex align-items-center gap-2">
        <span class="tier-badge tier-{{ client.loyalty_tier }}">{{ client.get_loyalty_tier_display }}</span>
        <span style="color:var(--crm-text-muted);font-size:.85rem">{{ client.phone }}</span>
      </div>
    </div>
  </div>
  <div class="d-flex gap-2">
    <a href="{% url 'appointments:create' %}?client={{ client.pk }}" class="btn btn-gold">
      <i class="bi bi-plus-lg me-1"></i>Запись
    </a>
    <a href="{% url 'clients:edit' client.pk %}" class="btn btn-ghost">
      <i class="bi bi-pencil me-1"></i>Изменить
    </a>
  </div>
</div>
<!-- Stats row -->
<div class="row g-3 mb-4">
  <div class="col-6 col-md-3"><div class="stat-mini"><div class="stat-val">{{ client.visit_count }}</div><div class="stat-lbl">Визиты</div></div></div>
  <div class="col-6 col-md-3"><div class="stat-mini"><div class="stat-val">{{ client.total_spent|currency }}</div><div class="stat-lbl">Потрачено</div></div></div>
  <div class="col-6 col-md-3"><div class="stat-mini"><div class="stat-val">{{ client.loyalty_points }}</div><div class="stat-lbl">Баллы</div></div></div>
  <div class="col-6 col-md-3"><div class="stat-mini"><div class="stat-val">{% if client.last_visit %}{{ client.last_visit|date:'d.m' }}{% else %}—{% endif %}</div><div class="stat-lbl">Последний визит</div></div></div>
</div>
<div class="row g-3">
  <!-- Info card -->
  <div class="col-md-4">
    <div class="crm-card p-4">
      <h6 class="card-title-gold mb-3"><i class="bi bi-person me-2"></i>Информация</h6>
      {% if client.email %}<div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">EMAIL</span><br>{{ client.email }}</div>{% endif %}
      {% if client.birth_date %}<div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">ДР</span><br>{{ client.birth_date|date:'d.m.Y' }}</div>{% endif %}
      {% if client.preferred_master %}<div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">МАСТЕР</span><br>{{ client.preferred_master.display_name }}</div>{% endif %}
      {% if client.notes %}<div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">ЗАМЕТКИ</span><br><small>{{ client.notes }}</small></div>{% endif %}
      <div style="font-size:.7rem;color:var(--crm-text-dim);margin-top:1rem">Клиент с {{ client.created_at|date:'d.m.Y' }}</div>
    </div>
  </div>
  <!-- Appointments -->
  <div class="col-md-8">
    <div class="crm-card">
      <div class="card-header"><h6 class="card-title-gold mb-0"><i class="bi bi-clock-history me-2"></i>История визитов</h6></div>
      <div class="p-3">
        {% for appt in appointments %}
        <a href="{% url 'appointments:detail' appt.pk %}" style="text-decoration:none">
          <div class="appt-row">
            <span class="appt-time">{{ appt.start_time|date:'d.m' }}</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--crm-text-muted)">{{ appt.start_time|date:'H:i' }}</span>
            <div class="flex-grow-1">
              <div style="font-weight:600;font-size:.875rem">{{ appt.service.name }}</div>
              <div style="font-size:.75rem;color:var(--crm-text-muted)">{{ appt.master.display_name }}</div>
            </div>
            <span class="badge-status status-{{ appt.status }}">{{ appt.get_status_display }}</span>
            {% if appt.price_paid %}<span style="font-family:'JetBrains Mono',monospace;color:var(--crm-gold);font-size:.85rem">{{ appt.price_paid|currency }}</span>{% endif %}
          </div>
        </a>
        {% empty %}
        <div class="text-center py-4" style="color:var(--crm-text-muted)">Визитов пока нет</div>
        {% endfor %}
      </div>
    </div>
  </div>
</div>
{% endblock %}
""")

# ── clients/form.html ─────────────────────────────────────────────────────────
w("templates/clients/form.html", """{% extends 'base.html' %}
{% block title %}{% if object %}Изменить клиента{% else %}Новый клиент{% endif %}{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">{% if object %}Изменить <span>клиента</span>{% else %}<span>Новый</span> клиент{% endif %}</h1>
  <a href="{% url 'clients:list' %}" class="btn btn-ghost"><i class="bi bi-arrow-left me-1"></i>Назад</a>
</div>
<div class="row justify-content-center">
  <div class="col-lg-7">
    <div class="crm-card p-4">
      <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="row g-3">
          {% for field in form %}
          <div class="col-{% if field.name in 'notes,bio' %}12{% else %}6{% endif %}">
            <label class="form-label">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}<div style="color:#f66;font-size:.75rem;margin-top:.25rem">{{ field.errors.0 }}</div>{% endif %}
          </div>
          {% endfor %}
        </div>
        <div class="d-flex gap-2 mt-4">
          <button type="submit" class="btn btn-gold"><i class="bi bi-check-lg me-1"></i>Сохранить</button>
          <a href="{% url 'clients:list' %}" class="btn btn-ghost">Отмена</a>
        </div>
      </form>
    </div>
  </div>
</div>
{% endblock %}
""")

# ── clients/confirm_delete.html ───────────────────────────────────────────────
w("templates/clients/confirm_delete.html", """{% extends 'base.html' %}
{% block title %}Удалить клиента{% endblock %}
{% block content %}
<div class="row justify-content-center"><div class="col-lg-5">
  <div class="crm-card p-4 text-center">
    <i class="bi bi-exclamation-triangle-fill" style="font-size:2.5rem;color:#f66;display:block;margin-bottom:1rem"></i>
    <h4 style="color:var(--crm-text-primary)">Удалить клиента?</h4>
    <p style="color:var(--crm-text-muted)">{{ object.full_name }} будет удалён без возможности восстановления.</p>
    <form method="post" class="d-flex gap-2 justify-content-center mt-3">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Удалить</button>
      <a href="{% url 'clients:detail' object.pk %}" class="btn btn-ghost">Отмена</a>
    </form>
  </div>
</div></div>
{% endblock %}
""")

# ── staff/list.html ───────────────────────────────────────────────────────────
w("templates/staff/list.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Мастера{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Масте<span>ра</span></h1>
  <a href="{% url 'staff:create' %}" class="btn btn-gold"><i class="bi bi-plus-lg me-1"></i>Добавить</a>
</div>
<div class="row g-3">
  {% for master in masters %}
  <div class="col-sm-6 col-lg-3">
    <a href="{% url 'staff:detail' master.pk %}" style="text-decoration:none">
      <div class="master-card" style="--master-color:{{ master.color }}">
        <div class="d-flex flex-column align-items-center">
          {% if master.photo %}
          <img src="{{ master.photo.url }}" class="avatar avatar-xl mb-3">
          {% else %}
          <div class="avatar-initials avatar-xl mb-3" style="border-color:{{ master.color }}">
            {{ master.display_name|slice:':2'|upper }}
          </div>
          {% endif %}
          <h6 style="color:var(--crm-text-primary);font-weight:700;margin-bottom:.25rem">{{ master.display_name }}</h6>
          <div style="font-size:.75rem;color:var(--crm-text-muted);margin-bottom:.75rem">
            {% for spec in master.specializations.all %}{{ spec.name }}{% if not forloop.last %}, {% endif %}{% endfor %}
          </div>
          <div>{{ master.rating|stars }}</div>
          <div style="font-size:.75rem;color:var(--crm-text-muted);margin-top:.5rem">
            {{ master.appointments.count }} записей
          </div>
        </div>
      </div>
    </a>
  </div>
  {% empty %}
  <div class="col-12 text-center py-5" style="color:var(--crm-text-muted)">Мастеров нет</div>
  {% endfor %}
</div>
{% endblock %}
""")

# ── staff/detail.html ─────────────────────────────────────────────────────────
w("templates/staff/detail.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}{{ master.display_name }}{% endblock %}
{% block content %}
<div class="page-header">
  <div class="d-flex align-items-center gap-3">
    {% if master.photo %}<img src="{{ master.photo.url }}" class="avatar avatar-lg">
    {% else %}<div class="avatar-initials avatar-lg" style="border-color:{{ master.color }}">{{ master.display_name|slice:':2'|upper }}</div>{% endif %}
    <div>
      <h1 class="page-title mb-1">{{ master.display_name }}</h1>
      <div>{{ master.rating|stars }}</div>
    </div>
  </div>
  <a href="{% url 'staff:edit' master.pk %}" class="btn btn-ghost"><i class="bi bi-pencil me-1"></i>Изменить</a>
</div>
<div class="row g-3 mb-4">
  <div class="col-4"><div class="stat-mini"><div class="stat-val">{{ total_appointments }}</div><div class="stat-lbl">Записи</div></div></div>
  <div class="col-4"><div class="stat-mini"><div class="stat-val">{{ total_revenue|currency }}</div><div class="stat-lbl">Выручка</div></div></div>
  <div class="col-4"><div class="stat-mini"><div class="stat-val">{{ master.rating }}</div><div class="stat-lbl">Рейтинг</div></div></div>
</div>
<div class="row g-3">
  <div class="col-md-4">
    <div class="crm-card p-4">
      <h6 class="card-title-gold mb-3"><i class="bi bi-person-badge me-2"></i>Профиль</h6>
      {% if master.phone %}<div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">ТЕЛЕФОН</span><br>{{ master.phone }}</div>{% endif %}
      {% if master.bio %}<div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">О МАСТЕРЕ</span><br><small>{{ master.bio }}</small></div>{% endif %}
      <div class="mb-2">
        <span style="color:var(--crm-text-muted);font-size:.75rem">УСЛУГИ</span><br>
        <div class="d-flex flex-wrap gap-1 mt-1">
          {% for svc in master.services.all %}<span style="background:var(--crm-gold-muted);color:var(--crm-gold);font-size:.7rem;padding:2px 8px;border-radius:20px">{{ svc.name }}</span>{% endfor %}
        </div>
      </div>
      <div class="mt-2" style="width:16px;height:16px;border-radius:50%;background:{{ master.color }};border:1px solid rgba(255,255,255,.2);display:inline-block"></div>
      <span style="font-size:.75rem;color:var(--crm-text-muted);margin-left:.5rem">Цвет в календаре</span>
    </div>
  </div>
  <div class="col-md-8">
    <div class="crm-card">
      <div class="card-header"><h6 class="card-title-gold mb-0"><i class="bi bi-calendar-day me-2"></i>Записи сегодня</h6></div>
      <div class="p-3">
        {% for appt in today_appointments %}
        <a href="{% url 'appointments:detail' appt.pk %}" style="text-decoration:none">
          <div class="appt-row">
            <span class="appt-time">{{ appt.start_time|date:'H:i' }}</span>
            <div class="avatar-initials">{{ appt.client.initials }}</div>
            <div class="flex-grow-1">
              <div style="font-weight:600;font-size:.875rem">{{ appt.client.full_name }}</div>
              <div style="font-size:.75rem;color:var(--crm-text-muted)">{{ appt.service.name }}</div>
            </div>
            <span class="badge-status status-{{ appt.status }}">{{ appt.get_status_display }}</span>
          </div>
        </a>
        {% empty %}
        <div class="text-center py-4" style="color:var(--crm-text-muted)">Нет записей на сегодня</div>
        {% endfor %}
      </div>
    </div>
  </div>
</div>
{% endblock %}
""")

# ── staff/form.html ───────────────────────────────────────────────────────────
w("templates/staff/form.html", """{% extends 'base.html' %}
{% block title %}{% if object %}Изменить мастера{% else %}Новый мастер{% endif %}{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">{% if object %}Изменить <span>мастера</span>{% else %}<span>Новый</span> мастер{% endif %}</h1>
  <a href="{% url 'staff:list' %}" class="btn btn-ghost"><i class="bi bi-arrow-left me-1"></i>Назад</a>
</div>
<div class="row justify-content-center"><div class="col-lg-7">
  <div class="crm-card p-4">
    <form method="post" enctype="multipart/form-data">
      {% csrf_token %}
      <div class="row g-3">
        {% for field in form %}
        <div class="col-{% if field.name in 'bio,specializations' %}12{% else %}6{% endif %}">
          <label class="form-label">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div style="color:#f66;font-size:.75rem;margin-top:.25rem">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
      <div class="d-flex gap-2 mt-4">
        <button type="submit" class="btn btn-gold"><i class="bi bi-check-lg me-1"></i>Сохранить</button>
        <a href="{% url 'staff:list' %}" class="btn btn-ghost">Отмена</a>
      </div>
    </form>
  </div>
</div></div>
{% endblock %}
""")

# ── services/list.html ────────────────────────────────────────────────────────
w("templates/services/list.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Услуги{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Услу<span>ги</span></h1>
  <a href="{% url 'services:create' %}" class="btn btn-gold"><i class="bi bi-plus-lg me-1"></i>Добавить услугу</a>
</div>
{% for category in categories %}
<div class="crm-card mb-3">
  <div class="card-header d-flex align-items-center gap-2">
    {% if category.icon %}<i class="{{ category.icon }}" style="color:var(--crm-gold)"></i>{% endif %}
    <h6 class="card-title-gold mb-0">{{ category.name }}</h6>
    <span style="font-size:.75rem;color:var(--crm-text-muted);margin-left:auto">{{ category.services.count }} услуг</span>
  </div>
  <div class="p-3">
    {% for svc in category.services.all %}
    <div class="service-item">
      <div class="flex-grow-1">
        <div style="font-weight:600">{{ svc.name }}</div>
        {% if svc.description %}<div style="font-size:.78rem;color:var(--crm-text-muted)">{{ svc.description }}</div>{% endif %}
      </div>
      <span style="font-size:.8rem;color:var(--crm-text-muted);margin-right:1.5rem">
        <i class="bi bi-clock me-1"></i>{{ svc.duration_display }}
      </span>
      <span class="service-price me-3">{{ svc.price|currency }}</span>
      {% if not svc.is_active %}<span class="badge-status status-cancelled me-2">Неактивна</span>{% endif %}
      <a href="{% url 'services:edit' svc.pk %}" class="btn btn-ghost btn-sm">
        <i class="bi bi-pencil"></i>
      </a>
    </div>
    {% empty %}
    <div style="color:var(--crm-text-muted);padding:.5rem;font-size:.85rem">Нет услуг в категории</div>
    {% endfor %}
  </div>
</div>
{% empty %}
<div class="crm-card p-5 text-center" style="color:var(--crm-text-muted)">Категорий нет</div>
{% endfor %}
{% endblock %}
""")

# ── services/form.html ────────────────────────────────────────────────────────
w("templates/services/form.html", """{% extends 'base.html' %}
{% block title %}{% if object %}Изменить услугу{% else %}Новая услуга{% endif %}{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">{% if object %}Изменить <span>услугу</span>{% else %}<span>Новая</span> услуга{% endif %}</h1>
  <a href="{% url 'services:list' %}" class="btn btn-ghost"><i class="bi bi-arrow-left me-1"></i>Назад</a>
</div>
<div class="row justify-content-center"><div class="col-lg-6">
  <div class="crm-card p-4">
    <form method="post">
      {% csrf_token %}
      <div class="row g-3">
        {% for field in form %}
        <div class="col-{% if field.name == 'description' %}12{% else %}6{% endif %}">
          <label class="form-label">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div style="color:#f66;font-size:.75rem;margin-top:.25rem">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
      <div class="d-flex gap-2 mt-4">
        <button type="submit" class="btn btn-gold"><i class="bi bi-check-lg me-1"></i>Сохранить</button>
        <a href="{% url 'services:list' %}" class="btn btn-ghost">Отмена</a>
      </div>
    </form>
  </div>
</div></div>
{% endblock %}
""")

# ── appointments/calendar.html ────────────────────────────────────────────────
w("templates/appointments/calendar.html", """{% extends 'base.html' %}
{% load static %}
{% block title %}Календарь{% endblock %}
{% block extra_head %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fullcalendar-scheduler@6.1.11/index.global.min.css">
<link rel="stylesheet" href="{% static 'css/calendar.css' %}">
{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Кален<span>дарь</span></h1>
  <a href="{% url 'appointments:create' %}" class="btn btn-gold">
    <i class="bi bi-plus-lg me-1"></i>Новая запись
  </a>
</div>
<script id="masters-data" type="application/json">
[{% for master in masters %}{"id":"{{ master.pk }}","title":"{{ master.display_name }}","eventColor":"{{ master.color }}"}{% if not forloop.last %},{% endif %}{% endfor %}]
</script>
<div class="crm-card p-3">
  <div id="barber-calendar"></div>
</div>
{% endblock %}
{% block extra_scripts %}
<script src="https://cdn.jsdelivr.net/npm/fullcalendar-scheduler@6.1.11/index.global.min.js"></script>
<script src="{% static 'js/calendar.js' %}"></script>
{% endblock %}
""")

# ── appointments/list.html ────────────────────────────────────────────────────
w("templates/appointments/list.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Записи{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Запи<span>си</span></h1>
  <a href="{% url 'appointments:create' %}" class="btn btn-gold"><i class="bi bi-plus-lg me-1"></i>Новая запись</a>
</div>
<!-- Filters -->
<div class="crm-card mb-3 p-3">
  <form method="get" class="d-flex gap-2 flex-wrap">
    <select name="status" class="form-select" style="max-width:180px">
      <option value="">Все статусы</option>
      {% for val,lbl in statuses %}<option value="{{ val }}" {% if status_filter == val %}selected{% endif %}>{{ lbl }}</option>{% endfor %}
    </select>
    <select name="master" class="form-select" style="max-width:180px">
      <option value="">Все мастера</option>
      {% for m in masters %}<option value="{{ m.pk }}" {% if master_filter == m.pk|stringformat:'s' %}selected{% endif %}>{{ m.display_name }}</option>{% endfor %}
    </select>
    <input type="date" name="date" value="{{ date_filter }}" class="form-control" style="max-width:170px">
    <button type="submit" class="btn btn-gold"><i class="bi bi-funnel"></i></button>
    {% if status_filter or master_filter or date_filter %}<a href="{% url 'appointments:list' %}" class="btn btn-ghost">Сбросить</a>{% endif %}
  </form>
</div>
<div class="crm-card">
  <div class="table-responsive">
    <table class="crm-table">
      <thead><tr><th>Время</th><th>Клиент</th><th>Мастер</th><th>Услуга</th><th>Стоимость</th><th>Статус</th><th></th></tr></thead>
      <tbody>
        {% for appt in appointments %}
        <tr>
          <td style="font-family:'JetBrains Mono',monospace;white-space:nowrap">
            {{ appt.start_time|date:'d.m.Y' }}<br>
            <span style="color:var(--crm-gold)">{{ appt.start_time|date:'H:i' }}</span>
          </td>
          <td>
            <div class="d-flex align-items-center gap-2">
              <div class="avatar-initials">{{ appt.client.initials }}</div>
              <div>
                <div style="font-weight:600">{{ appt.client.full_name }}</div>
                <div style="font-size:.75rem;color:var(--crm-text-muted)">{{ appt.client.phone }}</div>
              </div>
            </div>
          </td>
          <td>{{ appt.master.display_name }}</td>
          <td>
            <div>{{ appt.service.name }}</div>
            <div style="font-size:.75rem;color:var(--crm-text-muted)">{{ appt.service.duration_display }}</div>
          </td>
          <td style="font-family:'JetBrains Mono',monospace;color:var(--crm-gold)">{{ appt.service.price|currency }}</td>
          <td>
            <span class="badge-status status-{{ appt.status }}" data-status-badge="{{ appt.pk }}">
              {{ appt.get_status_display }}
            </span>
          </td>
          <td><a href="{% url 'appointments:detail' appt.pk %}" class="btn btn-ghost btn-sm"><i class="bi bi-eye"></i></a></td>
        </tr>
        {% empty %}
        <tr><td colspan="7" class="text-center py-4" style="color:var(--crm-text-muted)">Записей не найдено</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% include 'partials/_pagination.html' %}
</div>
{% endblock %}
{% block extra_scripts %}<script src="{% load static %}{% static 'js/appointments.js' %}"></script>{% endblock %}
""")

# ── appointments/detail.html ──────────────────────────────────────────────────
w("templates/appointments/detail.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Запись #{{ appointment.pk }}{% endblock %}
{% block content %}
<div class="page-header">
  <div>
    <h1 class="page-title">Запись <span>#{{ appointment.pk }}</span></h1>
    <div style="color:var(--crm-text-muted);font-size:.85rem;margin-top:.25rem">
      {{ appointment.start_time|date:'d E Y, H:i' }}
    </div>
  </div>
  <div class="d-flex gap-2">
    <a href="{% url 'appointments:edit' appointment.pk %}" class="btn btn-ghost"><i class="bi bi-pencil me-1"></i>Изменить</a>
    {% if appointment.status == 'done' and not appointment.payment %}
    <a href="{% url 'billing:create' appointment.pk %}" class="btn btn-gold"><i class="bi bi-cash me-1"></i>Оплата</a>
    {% endif %}
  </div>
</div>
<div class="row g-3">
  <div class="col-md-6">
    <div class="crm-card p-4">
      <h6 class="card-title-gold mb-3"><i class="bi bi-info-circle me-2"></i>Детали записи</h6>
      <div class="mb-3">
        <div style="font-size:.75rem;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.07em">Статус</div>
        <span class="badge-status status-{{ appointment.status }} mt-1" data-status-badge="{{ appointment.pk }}">{{ appointment.get_status_display }}</span>
      </div>
      <div class="mb-3">
        <div style="font-size:.75rem;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.07em">Клиент</div>
        <a href="{% url 'clients:detail' appointment.client.pk %}" style="font-weight:600">{{ appointment.client.full_name }}</a>
        <div style="font-size:.8rem;color:var(--crm-text-muted)">{{ appointment.client.phone }}</div>
      </div>
      <div class="mb-3">
        <div style="font-size:.75rem;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.07em">Мастер</div>
        <a href="{% url 'staff:detail' appointment.master.pk %}" style="font-weight:600">{{ appointment.master.display_name }}</a>
      </div>
      <div class="mb-3">
        <div style="font-size:.75rem;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.07em">Услуга</div>
        <div style="font-weight:600">{{ appointment.service.name }}</div>
        <div style="font-size:.8rem;color:var(--crm-text-muted)">{{ appointment.service.duration_display }}</div>
      </div>
      <div class="mb-3">
        <div style="font-size:.75rem;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.07em">Стоимость</div>
        <div style="font-family:'JetBrains Mono',monospace;color:var(--crm-gold);font-size:1.2rem;font-weight:700">
          {{ appointment.service.price|currency }}
        </div>
      </div>
      {% if appointment.notes %}
      <div class="mb-3">
        <div style="font-size:.75rem;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.07em">Заметки</div>
        <div style="font-size:.875rem">{{ appointment.notes }}</div>
      </div>
      {% endif %}
    </div>
  </div>
  <div class="col-md-6">
    <!-- Status change buttons -->
    <div class="crm-card p-4 mb-3">
      <h6 class="card-title-gold mb-3"><i class="bi bi-arrow-repeat me-2"></i>Сменить статус</h6>
      <div class="d-flex flex-wrap gap-2">
        {% for val,lbl in appointment.status.choices %}
        {% if val != appointment.status %}
        <button class="btn btn-ghost btn-sm" data-status-btn data-appt-id="{{ appointment.pk }}" data-status="{{ val }}">
          <span class="badge-status status-{{ val }}">{{ lbl }}</span>
        </button>
        {% endif %}
        {% endfor %}
        <!-- Manual status buttons -->
        {% with s=appointment.status %}
        {% if s != 'confirmed' %}<button class="btn btn-ghost btn-sm" data-status-btn data-appt-id="{{ appointment.pk }}" data-status="confirmed"><span class="badge-status status-confirmed">Подтвердить</span></button>{% endif %}
        {% if s != 'in_progress' %}<button class="btn btn-ghost btn-sm" data-status-btn data-appt-id="{{ appointment.pk }}" data-status="in_progress"><span class="badge-status status-in_progress">В процессе</span></button>{% endif %}
        {% if s != 'done' %}<button class="btn btn-ghost btn-sm" data-status-btn data-appt-id="{{ appointment.pk }}" data-status="done"><span class="badge-status status-done">Завершить</span></button>{% endif %}
        {% if s != 'cancelled' %}<button class="btn btn-ghost btn-sm" data-status-btn data-appt-id="{{ appointment.pk }}" data-status="cancelled"><span class="badge-status status-cancelled">Отменить</span></button>{% endif %}
        {% if s != 'no_show' %}<button class="btn btn-ghost btn-sm" data-status-btn data-appt-id="{{ appointment.pk }}" data-status="no_show"><span class="badge-status status-no_show">Не явился</span></button>{% endif %}
        {% endwith %}
      </div>
    </div>
    <!-- Payment info -->
    {% if appointment.payment %}
    <div class="crm-card p-4">
      <h6 class="card-title-gold mb-3"><i class="bi bi-receipt me-2"></i>Оплата</h6>
      <div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">ЧЕК</span><br><strong>{{ appointment.payment.receipt_number }}</strong></div>
      <div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">СУММА</span><br><span style="font-family:'JetBrains Mono',monospace;color:var(--crm-gold);font-size:1.1rem">{{ appointment.payment.final_amount|currency }}</span></div>
      <div class="mb-2"><span style="color:var(--crm-text-muted);font-size:.75rem">СПОСОБ</span><br>{{ appointment.payment.get_method_display }}</div>
      <a href="{% url 'billing:detail' appointment.payment.pk %}" class="btn btn-ghost btn-sm mt-2"><i class="bi bi-eye me-1"></i>Открыть чек</a>
    </div>
    {% else %}
    <div class="crm-card p-4 text-center" style="border-style:dashed">
      <i class="bi bi-cash" style="font-size:2rem;color:var(--crm-text-dim);display:block;margin-bottom:.75rem"></i>
      <div style="color:var(--crm-text-muted);margin-bottom:1rem">Оплата не принята</div>
      <a href="{% url 'billing:create' appointment.pk %}" class="btn btn-gold btn-sm">
        <i class="bi bi-cash me-1"></i>Принять оплату
      </a>
    </div>
    {% endif %}
  </div>
</div>
{% endblock %}
{% block extra_scripts %}<script src="{% load static %}{% static 'js/appointments.js' %}"></script>{% endblock %}
""")

# ── appointments/form.html ────────────────────────────────────────────────────
w("templates/appointments/form.html", """{% extends 'base.html' %}
{% block title %}{% if object %}Изменить запись{% else %}Новая запись{% endif %}{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">{% if object %}Изменить <span>запись</span>{% else %}<span>Новая</span> запись{% endif %}</h1>
  <a href="{% url 'appointments:list' %}" class="btn btn-ghost"><i class="bi bi-arrow-left me-1"></i>Назад</a>
</div>
<div class="row justify-content-center"><div class="col-lg-7">
  <div class="crm-card p-4">
    <form method="post">
      {% csrf_token %}
      <div class="row g-3">
        {% for field in form %}
        <div class="col-{% if field.name == 'notes' %}12{% else %}6{% endif %}">
          <label class="form-label">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div style="color:#f66;font-size:.75rem;margin-top:.25rem">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
      <div class="d-flex gap-2 mt-4">
        <button type="submit" class="btn btn-gold"><i class="bi bi-check-lg me-1"></i>Сохранить</button>
        <a href="{% url 'appointments:list' %}" class="btn btn-ghost">Отмена</a>
      </div>
    </form>
  </div>
</div></div>
{% endblock %}
""")

# ── billing/list.html ─────────────────────────────────────────────────────────
w("templates/billing/list.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Платежи{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Плате<span>жи</span></h1>
  <div class="d-flex gap-2">
    <a href="{% url 'billing:reports' %}" class="btn btn-ghost"><i class="bi bi-bar-chart me-1"></i>Отчёты</a>
    <a href="{% url 'billing:export' %}" class="btn btn-ghost"><i class="bi bi-download me-1"></i>CSV</a>
  </div>
</div>
<div class="crm-card">
  <div class="table-responsive">
    <table class="crm-table">
      <thead><tr><th>Чек</th><th>Дата</th><th>Клиент</th><th>Мастер</th><th>Услуга</th><th>Сумма</th><th>Скидка</th><th>Способ</th><th></th></tr></thead>
      <tbody>
        {% for p in payments %}
        <tr>
          <td style="font-family:'JetBrains Mono',monospace;font-size:.8rem">{{ p.receipt_number }}</td>
          <td style="font-size:.8rem;white-space:nowrap">{{ p.paid_at|date:'d.m.Y H:i' }}</td>
          <td>
            <a href="{% url 'clients:detail' p.appointment.client.pk %}">{{ p.appointment.client.full_name }}</a>
          </td>
          <td>{{ p.appointment.master.display_name }}</td>
          <td style="font-size:.85rem">{{ p.appointment.service.name }}</td>
          <td style="font-family:'JetBrains Mono',monospace;color:var(--crm-gold)">{{ p.final_amount|currency }}</td>
          <td>{% if p.discount %}<span style="color:#20c997">-{{ p.discount }}%</span>{% else %}—{% endif %}</td>
          <td><span style="font-size:.8rem">{{ p.get_method_display }}</span></td>
          <td><a href="{% url 'billing:detail' p.pk %}" class="btn btn-ghost btn-sm"><i class="bi bi-receipt"></i></a></td>
        </tr>
        {% empty %}
        <tr><td colspan="9" class="text-center py-4" style="color:var(--crm-text-muted)">Нет платежей</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% include 'partials/_pagination.html' %}
</div>
{% endblock %}
""")

# ── billing/form.html ─────────────────────────────────────────────────────────
w("templates/billing/form.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Принять оплату{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Принять <span>оплату</span></h1>
  <a href="{% url 'appointments:detail' appointment.pk %}" class="btn btn-ghost"><i class="bi bi-arrow-left me-1"></i>Назад</a>
</div>
<div class="row justify-content-center"><div class="col-lg-6">
  <!-- Summary -->
  <div class="crm-card p-4 mb-3">
    <div class="d-flex justify-content-between mb-2">
      <span style="color:var(--crm-text-muted)">Клиент</span>
      <strong>{{ appointment.client.full_name }}</strong>
    </div>
    <div class="d-flex justify-content-between mb-2">
      <span style="color:var(--crm-text-muted)">Мастер</span>
      <span>{{ appointment.master.display_name }}</span>
    </div>
    <div class="d-flex justify-content-between">
      <span style="color:var(--crm-text-muted)">Услуга</span>
      <span>{{ appointment.service.name }}</span>
    </div>
    <hr style="border-color:var(--crm-border-subtle);margin:1rem 0">
    <div class="d-flex justify-content-between">
      <span style="color:var(--crm-text-muted)">Цена услуги</span>
      <strong style="font-family:'JetBrains Mono',monospace;color:var(--crm-gold)">{{ appointment.service.price|currency }}</strong>
    </div>
  </div>
  <div class="crm-card p-4">
    <form method="post">
      {% csrf_token %}
      <div class="row g-3">
        {% for field in form %}
        <div class="col-{% if field.name == 'notes' %}12{% else %}6{% endif %}">
          <label class="form-label">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div style="color:#f66;font-size:.75rem">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
      <div class="d-flex gap-2 mt-4">
        <button type="submit" class="btn btn-gold w-100"><i class="bi bi-cash me-2"></i>Принять оплату</button>
      </div>
    </form>
  </div>
</div></div>
{% endblock %}
""")

# ── billing/detail.html ───────────────────────────────────────────────────────
w("templates/billing/detail.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Чек {{ payment.receipt_number }}{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Чек <span>#{{ payment.receipt_number }}</span></h1>
  <button onclick="window.print()" class="btn btn-ghost"><i class="bi bi-printer me-1"></i>Печать</button>
</div>
<div class="receipt" id="receipt">
  <div class="text-center mb-4">
    <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:var(--crm-gold);font-weight:700">THE CUT</div>
    <div style="font-size:.7rem;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.15em">Barbershop</div>
  </div>
  <hr class="receipt-divider">
  <div class="d-flex justify-content-between mb-2">
    <span style="color:var(--crm-text-muted);font-size:.8rem">Чек</span>
    <span style="font-family:'JetBrains Mono',monospace;font-size:.85rem">{{ payment.receipt_number }}</span>
  </div>
  <div class="d-flex justify-content-between mb-2">
    <span style="color:var(--crm-text-muted);font-size:.8rem">Дата</span>
    <span style="font-size:.85rem">{{ payment.paid_at|date:'d.m.Y H:i' }}</span>
  </div>
  <div class="d-flex justify-content-between mb-2">
    <span style="color:var(--crm-text-muted);font-size:.8rem">Клиент</span>
    <span style="font-size:.85rem">{{ payment.appointment.client.full_name }}</span>
  </div>
  <div class="d-flex justify-content-between mb-2">
    <span style="color:var(--crm-text-muted);font-size:.8rem">Мастер</span>
    <span style="font-size:.85rem">{{ payment.appointment.master.display_name }}</span>
  </div>
  <hr class="receipt-divider">
  <div class="d-flex justify-content-between mb-2">
    <span>{{ payment.appointment.service.name }}</span>
    <span style="font-family:'JetBrains Mono',monospace">{{ payment.amount|currency }}</span>
  </div>
  {% if payment.discount %}
  <div class="d-flex justify-content-between mb-2">
    <span style="color:#20c997">Скидка {{ payment.discount }}%</span>
    <span style="font-family:'JetBrains Mono',monospace;color:#20c997">-{{ payment.discount_amount|currency }}</span>
  </div>
  {% endif %}
  <hr class="receipt-divider">
  <div class="d-flex justify-content-between">
    <strong style="font-size:1.1rem">Итого</strong>
    <strong style="font-family:'JetBrains Mono',monospace;font-size:1.3rem;color:var(--crm-gold)">{{ payment.final_amount|currency }}</strong>
  </div>
  <div class="mt-2" style="font-size:.8rem;color:var(--crm-text-muted)">
    Оплата: {{ payment.get_method_display }}
  </div>
  <hr class="receipt-divider">
  <div class="text-center" style="font-size:.75rem;color:var(--crm-text-dim)">Спасибо за визит!</div>
</div>
{% endblock %}
""")

# ── billing/reports.html ──────────────────────────────────────────────────────
w("templates/billing/reports.html", """{% extends 'base.html' %}
{% load crm_tags %}
{% block title %}Отчёты{% endblock %}
{% block extra_head %}<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">Отчё<span>ты</span></h1>
  <a href="{% url 'billing:export' %}" class="btn btn-ghost"><i class="bi bi-download me-1"></i>Скачать CSV</a>
</div>
<!-- Summary cards -->
<div class="row g-3 mb-4">
  <div class="col-6 col-md-3">
    <div class="kpi-card">
      <div class="kpi-icon" style="background:rgba(201,168,76,.15)"><i class="bi bi-cash text-warning"></i></div>
      <div class="kpi-value">{{ month_revenue|currency }}</div>
      <div class="kpi-label">Выручка за месяц</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="kpi-card">
      <div class="kpi-icon" style="background:rgba(13,202,240,.1)"><i class="bi bi-receipt" style="color:#0dcaf0"></i></div>
      <div class="kpi-value">{{ month_count }}</div>
      <div class="kpi-label">Оплат за месяц</div>
    </div>
  </div>
</div>
<!-- Revenue chart -->
<div class="crm-card mb-4 p-4">
  <h6 class="card-title-gold mb-3"><i class="bi bi-bar-chart me-2"></i>Выручка за 30 дней</h6>
  <canvas id="revenueChart" height="80"></canvas>
</div>
<div class="row g-3">
  <!-- Top masters -->
  <div class="col-md-6">
    <div class="crm-card p-4">
      <h6 class="card-title-gold mb-3"><i class="bi bi-trophy me-2"></i>Топ мастера (месяц)</h6>
      {% for row in top_masters %}
      <div class="service-item justify-content-between">
        <span style="font-weight:600">{{ row.appointment__master__display_name }}</span>
        <div class="d-flex align-items-center gap-3">
          <span style="font-size:.75rem;color:var(--crm-text-muted)">{{ row.count }} визитов</span>
          <span class="service-price">{{ row.total|currency }}</span>
        </div>
      </div>
      {% empty %}<div style="color:var(--crm-text-muted)">Нет данных</div>
      {% endfor %}
    </div>
  </div>
  <!-- Top clients -->
  <div class="col-md-6">
    <div class="crm-card p-4">
      <h6 class="card-title-gold mb-3"><i class="bi bi-star me-2"></i>Топ клиенты (месяц)</h6>
      {% for row in top_clients %}
      <div class="service-item justify-content-between">
        <a href="{% url 'clients:detail' row.appointment__client__pk %}" style="font-weight:600">
          {{ row.appointment__client__first_name }} {{ row.appointment__client__last_name }}
        </a>
        <div class="d-flex align-items-center gap-3">
          <span style="font-size:.75rem;color:var(--crm-text-muted)">{{ row.visits }} визитов</span>
          <span class="service-price">{{ row.total|currency }}</span>
        </div>
      </div>
      {% empty %}<div style="color:var(--crm-text-muted)">Нет данных</div>
      {% endfor %}
    </div>
  </div>
</div>
<script>
var labels = {{ daily_labels|safe }};
var data   = {{ daily_totals|safe }};
var ctx = document.getElementById('revenueChart').getContext('2d');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: 'Выручка (руб.)',
      data: data,
      backgroundColor: 'rgba(201,168,76,0.5)',
      borderColor: '#c9a84c',
      borderWidth: 1,
      borderRadius: 4,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {labels: {color:'#7a7060'}},
    },
    scales: {
      x: {ticks:{color:'#7a7060'}, grid:{color:'rgba(255,255,255,.04)'}},
      y: {ticks:{color:'#7a7060'}, grid:{color:'rgba(255,255,255,.04)'}}
    }
  }
});
</script>
{% endblock %}
""")

print("\nAll templates written successfully.")
