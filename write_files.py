"""One-shot script to write all CRM static files and templates."""
import os, sys
BASE = r"D:\CRM\barbershop_crm"

def w(rel, content):
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  OK: {rel}")

# ── theme.css ──────────────────────────────────────────────────────────────
w("static/css/theme.css", r"""/* ===== BARBERSHOP CRM - DARK GOLD THEME ===== */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');
:root{--crm-bg-primary:#0a0a0a;--crm-bg-secondary:#111111;--crm-bg-card:#161616;--crm-bg-elevated:#1e1e1e;--crm-bg-hover:#252525;--crm-gold:#c9a84c;--crm-gold-light:#e0c06a;--crm-gold-dark:#a07830;--crm-gold-muted:rgba(201,168,76,.12);--crm-gold-border:rgba(201,168,76,.25);--crm-text-primary:#f0ead6;--crm-text-muted:#7a7060;--crm-text-dim:#4a4540;--crm-text-inverse:#0a0a0a;--crm-sidebar-width:260px;--crm-border:rgba(201,168,76,.15);--crm-border-subtle:rgba(255,255,255,.06);--crm-shadow-sm:0 2px 8px rgba(0,0,0,.4);--crm-shadow:0 4px 24px rgba(0,0,0,.6);--crm-shadow-lg:0 8px 40px rgba(0,0,0,.8);--crm-radius:12px;--crm-radius-sm:8px;--crm-transition:all .22s cubic-bezier(.4,0,.2,1)}
*{box-sizing:border-box}html,body{height:100%}
body{background:var(--crm-bg-primary);color:var(--crm-text-primary);font-family:'Inter',system-ui,sans-serif;font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:var(--crm-bg-secondary)}::-webkit-scrollbar-thumb{background:var(--crm-gold-dark);border-radius:4px}::-webkit-scrollbar-thumb:hover{background:var(--crm-gold)}

/* LAYOUT */
.crm-sidebar{position:fixed;left:0;top:0;width:var(--crm-sidebar-width);height:100vh;background:var(--crm-bg-secondary);border-right:1px solid var(--crm-border);overflow-y:auto;overflow-x:hidden;z-index:1000;display:flex;flex-direction:column;transition:var(--crm-transition)}
.crm-main{margin-left:var(--crm-sidebar-width);min-height:100vh;display:flex;flex-direction:column}
.crm-content{flex:1;max-width:1600px;width:100%}
.crm-navbar{background:var(--crm-bg-secondary)!important;border-bottom:1px solid var(--crm-border)!important;padding:0 1.5rem;height:60px;position:sticky;top:0;z-index:900}

/* SIDEBAR LOGO */
.sidebar-logo{padding:1.5rem 1.25rem 1rem;border-bottom:1px solid var(--crm-border);flex-shrink:0}
.sidebar-logo .logo-icon{width:40px;height:40px;background:var(--crm-gold-muted);border:1px solid var(--crm-gold-border);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:var(--crm-gold)}
.sidebar-logo .logo-text{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--crm-gold);letter-spacing:.03em}
.sidebar-logo .logo-sub{font-size:.65rem;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.12em}

/* SIDEBAR NAV */
.sidebar-nav{padding:.75rem 0;flex:1}
.sidebar-section-label{font-size:.6rem;text-transform:uppercase;letter-spacing:.15em;color:var(--crm-text-dim);padding:1rem 1.25rem .35rem;font-weight:600;display:block}
.sidebar-nav .nav-link{display:flex;align-items:center;gap:.75rem;color:var(--crm-text-muted);border-radius:8px;margin:1px 10px;padding:10px 14px;font-size:.875rem;font-weight:500;transition:var(--crm-transition);border-left:3px solid transparent;text-decoration:none;white-space:nowrap}
.sidebar-nav .nav-link i{font-size:1rem;flex-shrink:0;width:18px;text-align:center}
.sidebar-nav .nav-link:hover,.sidebar-nav .nav-link.active{background:var(--crm-gold-muted);color:var(--crm-gold);border-left-color:var(--crm-gold)}
.sidebar-footer{padding:1rem;border-top:1px solid var(--crm-border);flex-shrink:0}

/* CARDS */
.crm-card{background:var(--crm-bg-card);border:1px solid var(--crm-border-subtle);border-radius:var(--crm-radius);box-shadow:var(--crm-shadow-sm);transition:var(--crm-transition)}
.crm-card:hover{border-color:var(--crm-gold-border);box-shadow:0 6px 28px rgba(201,168,76,.12);transform:translateY(-1px)}
.crm-card .card-header{background:transparent;border-bottom:1px solid var(--crm-border-subtle);padding:1rem 1.25rem}
.card-title-gold{font-family:'Playfair Display',serif;color:var(--crm-gold);margin:0}

/* KPI CARDS */
.kpi-card{background:var(--crm-bg-card);border:1px solid var(--crm-border-subtle);border-radius:var(--crm-radius);padding:1.5rem;position:relative;overflow:hidden;transition:var(--crm-transition)}
.kpi-card::before{content:'';position:absolute;top:0;right:0;width:80px;height:80px;background:var(--crm-gold-muted);border-radius:50%;transform:translate(30%,-30%)}
.kpi-card:hover{border-color:var(--crm-gold-border);box-shadow:0 8px 32px rgba(201,168,76,.15);transform:translateY(-2px)}
.kpi-icon{width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;margin-bottom:1rem}
.kpi-value{font-size:2.25rem;font-weight:700;color:var(--crm-gold);line-height:1;font-family:'JetBrains Mono',monospace;letter-spacing:-.02em}
.kpi-label{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--crm-text-muted);margin-top:.35rem;font-weight:600}

/* BUTTONS */
.btn-gold{background:linear-gradient(135deg,var(--crm-gold),var(--crm-gold-dark));border:none;color:var(--crm-text-inverse);font-weight:600;font-size:.875rem;padding:.5rem 1.25rem;border-radius:8px;transition:var(--crm-transition);box-shadow:0 2px 8px rgba(201,168,76,.3)}
.btn-gold:hover{background:linear-gradient(135deg,var(--crm-gold-light),var(--crm-gold));color:var(--crm-text-inverse);box-shadow:0 4px 16px rgba(201,168,76,.4);transform:translateY(-1px)}
.btn-ghost{background:transparent;border:1px solid var(--crm-border);color:var(--crm-text-muted);font-size:.875rem;padding:.5rem 1.25rem;border-radius:8px;transition:var(--crm-transition)}
.btn-ghost:hover{border-color:var(--crm-gold-border);color:var(--crm-gold);background:var(--crm-gold-muted)}

/* TABLES */
.crm-table{width:100%;border-collapse:separate;border-spacing:0}
.crm-table thead th{background:var(--crm-bg-elevated);color:var(--crm-text-muted);font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;font-weight:600;padding:.75rem 1rem;border-bottom:1px solid var(--crm-border-subtle);white-space:nowrap}
.crm-table thead th:first-child{border-radius:8px 0 0 0}.crm-table thead th:last-child{border-radius:0 8px 0 0}
.crm-table tbody tr{transition:var(--crm-transition)}.crm-table tbody tr:hover td{background:var(--crm-bg-elevated)}
.crm-table tbody td{padding:.875rem 1rem;vertical-align:middle;color:var(--crm-text-primary);border-bottom:1px solid var(--crm-border-subtle)}

/* STATUS BADGES */
.badge-status{display:inline-flex;align-items:center;gap:4px;font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;padding:4px 10px;border-radius:20px;font-weight:600}
.status-pending{background:rgba(108,117,125,.2);color:#adb5bd}
.status-confirmed{background:rgba(201,168,76,.2);color:var(--crm-gold)}
.status-in_progress{background:rgba(13,202,240,.15);color:#0dcaf0}
.status-done{background:rgba(25,135,84,.2);color:#20c997}
.status-cancelled{background:rgba(220,53,69,.2);color:#f66}
.status-no_show{background:rgba(111,66,193,.2);color:#b189f5}

/* LOYALTY TIERS */
.tier-badge{display:inline-flex;align-items:center;gap:4px;font-size:.68rem;font-weight:700;padding:3px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:.08em}
.tier-bronze{background:rgba(205,127,50,.2);color:#cd7f32}
.tier-silver{background:rgba(192,192,192,.2);color:#c0c0c0}
.tier-gold{background:rgba(201,168,76,.2);color:var(--crm-gold)}
.tier-platinum{background:rgba(229,228,226,.15);color:#e5e4e2}

/* AVATARS */
.avatar{width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid var(--crm-gold-border)}
.avatar-initials{width:40px;height:40px;border-radius:50%;background:var(--crm-gold-muted);border:1px solid var(--crm-gold-border);display:inline-flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;color:var(--crm-gold);text-transform:uppercase;flex-shrink:0}
.avatar-lg{width:80px!important;height:80px!important;font-size:1.5rem!important}
.avatar-xl{width:120px!important;height:120px!important;font-size:2rem!important}

/* FORMS */
.form-control,.form-select{background:var(--crm-bg-elevated)!important;border-color:var(--crm-border-subtle)!important;color:var(--crm-text-primary)!important;border-radius:8px!important;font-size:.875rem;transition:var(--crm-transition)}
.form-control:focus,.form-select:focus{border-color:var(--crm-gold-border)!important;box-shadow:0 0 0 3px var(--crm-gold-muted)!important;background:var(--crm-bg-hover)!important}
.form-control::placeholder{color:var(--crm-text-muted)!important}
.form-label{font-size:.78rem;font-weight:600;color:var(--crm-text-muted);text-transform:uppercase;letter-spacing:.07em;margin-bottom:.4rem}

/* PAGE HEADERS */
.page-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.75rem;padding-bottom:1rem;border-bottom:1px solid var(--crm-border-subtle)}
.page-title{font-family:'Playfair Display',serif;font-size:1.75rem;font-weight:700;color:var(--crm-text-primary);margin:0;line-height:1.2}
.page-title span{color:var(--crm-gold)}

/* SEARCH */
.search-input-group{position:relative}
.search-input-group .search-icon{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--crm-text-muted);pointer-events:none;z-index:5}
.search-input-group input{padding-left:2.2rem}

/* LINKS */
a{color:var(--crm-gold);text-decoration:none}a:hover{color:var(--crm-gold-light)}

/* PAGINATION */
.page-item .page-link{background:var(--crm-bg-elevated);border-color:var(--crm-border-subtle);color:var(--crm-text-muted);border-radius:6px!important;margin:0 2px}
.page-item.active .page-link{background:var(--crm-gold);border-color:var(--crm-gold);color:var(--crm-text-inverse)}
.page-item .page-link:hover{background:var(--crm-gold-muted);color:var(--crm-gold);border-color:var(--crm-gold-border)}

/* TOASTS */
.toast-container{position:fixed;top:70px;right:20px;z-index:9999}
.crm-toast{background:var(--crm-bg-elevated)!important;border:1px solid var(--crm-border)!important;border-radius:10px!important;box-shadow:var(--crm-shadow)!important;color:var(--crm-text-primary)!important;min-width:300px}

/* APPOINTMENT ROWS */
.appt-row{display:flex;align-items:center;gap:1rem;padding:.75rem 1rem;border-radius:8px;border:1px solid var(--crm-border-subtle);background:var(--crm-bg-elevated);margin-bottom:.5rem;transition:var(--crm-transition)}
.appt-row:hover{border-color:var(--crm-gold-border);background:var(--crm-bg-hover)}
.appt-time{font-family:'JetBrains Mono',monospace;font-size:.85rem;color:var(--crm-gold);min-width:50px;font-weight:500}

/* MASTER CARDS */
.master-card{background:var(--crm-bg-card);border:1px solid var(--crm-border-subtle);border-radius:var(--crm-radius);padding:1.5rem;text-align:center;transition:var(--crm-transition);position:relative;overflow:hidden}
.master-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;background:var(--master-color,var(--crm-gold));opacity:0;transition:var(--crm-transition)}
.master-card:hover{border-color:var(--crm-gold-border);transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,.5)}
.master-card:hover::after{opacity:1}

/* STATS MINI */
.stat-mini{text-align:center;padding:.75rem;background:var(--crm-bg-elevated);border-radius:8px}
.stat-mini .stat-val{font-size:1.4rem;font-weight:700;color:var(--crm-gold);font-family:'JetBrains Mono',monospace}
.stat-mini .stat-lbl{font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:var(--crm-text-muted);font-weight:600}

/* SERVICE ITEMS */
.service-item{display:flex;align-items:center;padding:.875rem 1rem;border:1px solid var(--crm-border-subtle);border-radius:8px;background:var(--crm-bg-elevated);margin-bottom:.5rem;transition:var(--crm-transition)}
.service-item:hover{border-color:var(--crm-gold-border)}
.service-price{font-family:'JetBrains Mono',monospace;color:var(--crm-gold);font-weight:700;font-size:1rem}

/* RECEIPT */
.receipt{max-width:480px;margin:0 auto;background:var(--crm-bg-card);border:1px solid var(--crm-border);border-radius:var(--crm-radius);padding:2rem}
.receipt-divider{border:none;border-top:1px dashed var(--crm-border);margin:1rem 0}

/* DARK OVERRIDES */
.dropdown-menu{background:var(--crm-bg-elevated)!important;border-color:var(--crm-border)!important}
.dropdown-item{color:var(--crm-text-primary)!important}
.dropdown-item:hover{background:var(--crm-gold-muted)!important;color:var(--crm-gold)!important}
.modal-content{background:var(--crm-bg-card)!important;border-color:var(--crm-border)!important}
.modal-header,.modal-footer{border-color:var(--crm-border-subtle)!important}
.input-group-text{background:var(--crm-bg-elevated)!important;border-color:var(--crm-border-subtle)!important;color:var(--crm-text-muted)!important}
.alert{border-radius:10px!important}
.text-gold{color:var(--crm-gold)!important}
.bg-gold-muted{background:var(--crm-gold-muted)!important}
.border-gold{border-color:var(--crm-gold-border)!important}

/* CALENDAR OVERRIDES */
.fc{background:var(--crm-bg-card);color:var(--crm-text-primary)}
.fc-theme-standard td,.fc-theme-standard th,.fc-theme-standard .fc-scrollgrid{border-color:var(--crm-border-subtle)}
.fc-col-header-cell-cushion,.fc-datagrid-cell-main{color:var(--crm-text-primary)}
.fc-button-primary{background:var(--crm-bg-elevated)!important;border-color:var(--crm-border)!important;color:var(--crm-text-primary)!important}
.fc-button-primary:hover,.fc-button-primary:focus{background:var(--crm-gold-muted)!important;border-color:var(--crm-gold-border)!important;color:var(--crm-gold)!important}
.fc-button-primary.fc-button-active{background:var(--crm-gold)!important;border-color:var(--crm-gold)!important;color:var(--crm-text-inverse)!important}
.fc-toolbar-title{font-family:'Playfair Display',serif;color:var(--crm-text-primary)!important;font-size:1.1rem!important}
.fc-resource-timeline-divider{background:var(--crm-border)}
.fc-datagrid-header,.fc-timeline-header{background:var(--crm-bg-elevated)!important}
.fc-event{border-radius:6px!important;border:none!important;padding:2px 6px;font-size:.75rem}
.fc-event-inner{display:flex;flex-direction:column;gap:1px;padding:2px 0}
.fc-event-name{font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fc-event-phone{font-size:.65rem;opacity:.8}
.fc-now-indicator-line{border-color:var(--crm-gold)!important}
.fc-timegrid-slot-minor{border-top-style:dotted}
.fc-datagrid-cell-cushion{color:var(--crm-text-primary)!important;font-weight:500!important}

/* MOBILE */
@media (max-width:768px){
  .crm-sidebar{transform:translateX(-100%);z-index:1050}
  .crm-sidebar.show{transform:translateX(0)}
  .crm-main{margin-left:0}
  .kpi-value{font-size:1.75rem!important}
  .page-title{font-size:1.3rem}
  .crm-table{font-size:.8rem}
}
""")

# ── calendar.css ────────────────────────────────────────────────────────────
w("static/css/calendar.css", """/* FullCalendar additional dark overrides */
.fc-resource-area-header { background: var(--crm-bg-elevated) !important; }
.fc-resource-group-cell { background: var(--crm-bg-elevated) !important; }
.fc-timegrid-slot { border-color: var(--crm-border-subtle) !important; }
.fc-scrollgrid-section > td { background: var(--crm-bg-card); }
.fc-non-business { background: rgba(0,0,0,.25) !important; }
.fc-today { background: rgba(201,168,76,.04) !important; }
""")

# ── main.js ─────────────────────────────────────────────────────────────────
w("static/js/main.js", r"""/* ===== CRM Global JS ===== */

// Show Bootstrap toast
function showToast(message, type) {
  type = type || 'info';
  var colors = {success:'#20c997', danger:'#f66', warning:'#c9a84c', info:'#0dcaf0'};
  var icons  = {success:'bi-check-circle-fill', danger:'bi-x-circle-fill', warning:'bi-exclamation-circle-fill', info:'bi-info-circle-fill'};
  var container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  var id = 'toast_' + Date.now();
  var html = '<div id="'+id+'" class="toast crm-toast align-items-center show" role="alert" aria-live="assertive" aria-atomic="true" style="margin-bottom:8px">'
    + '<div class="d-flex">'
    + '<div class="toast-body d-flex align-items-center gap-2">'
    + '<i class="bi ' + (icons[type]||icons.info) + '" style="color:' + (colors[type]||colors.info) + '"></i>'
    + '<span>' + message + '</span>'
    + '</div>'
    + '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>'
    + '</div></div>';
  container.insertAdjacentHTML('beforeend', html);
  setTimeout(function() {
    var el = document.getElementById(id);
    if (el) { el.remove(); }
  }, 4000);
}

// CSRF helper
function getCsrf() {
  var m = document.cookie.match(/csrftoken=([^;]+)/);
  return m ? m[1] : '';
}

// Sidebar toggle for mobile
document.addEventListener('DOMContentLoaded', function() {
  var toggle = document.getElementById('sidebarToggle');
  var sidebar = document.querySelector('.crm-sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', function() {
      sidebar.classList.toggle('show');
    });
  }

  // Auto-dismiss django messages after 4s
  document.querySelectorAll('.auto-dismiss').forEach(function(el) {
    setTimeout(function() { el.remove(); }, 4000);
  });
});
""")

# ── appointments.js ──────────────────────────────────────────────────────────
w("static/js/appointments.js", r"""/* ===== Appointment status toggle ===== */
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('[data-status-btn]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var apptId  = btn.dataset.apptId;
      var status  = btn.dataset.status;
      var url     = '/appointments/api/' + apptId + '/status/';
      fetch(url, {
        method: 'POST',
        headers: {'Content-Type':'application/json','X-CSRFToken': getCsrf()},
        body: JSON.stringify({status: status})
      })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.success) {
          // Update badge on page
          var badge = document.querySelector('[data-status-badge="' + apptId + '"]');
          if (badge) {
            badge.className = 'badge-status status-' + data.status;
            badge.textContent = data.label;
          }
          showToast('Статус обновлён: ' + data.label, 'success');
          // Close modal if open
          var modal = document.getElementById('statusModal');
          if (modal) bootstrap.Modal.getInstance(modal).hide();
        } else {
          showToast('Ошибка обновления', 'danger');
        }
      })
      .catch(function() { showToast('Сетевая ошибка', 'danger'); });
    });
  });
});
""")

# ── calendar.js ──────────────────────────────────────────────────────────────
w("static/js/calendar.js", r"""/* ===== FullCalendar Resource Timeline ===== */
document.addEventListener('DOMContentLoaded', function() {
  var calEl = document.getElementById('barber-calendar');
  if (!calEl) return;

  var mastersEl = document.getElementById('masters-data');
  var resources = mastersEl ? JSON.parse(mastersEl.textContent) : [];

  var calendar = new FullCalendar.Calendar(calEl, {
    schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
    initialView: 'resourceTimelineDay',
    headerToolbar: {
      left:   'prev,next today',
      center: 'title',
      right:  'resourceTimelineDay,resourceTimelineWeek'
    },
    slotMinTime: '08:00:00',
    slotMaxTime: '22:00:00',
    slotDuration: '00:30:00',
    height: 'auto',
    nowIndicator: true,
    resources: resources,
    resourceAreaHeaderContent: 'Мастера',
    resourceAreaWidth: '180px',
    events: {
      url: '/appointments/api/events/',
      method: 'GET',
      failure: function() { showToast('Ошибка загрузки записей', 'danger'); }
    },
    editable: true,
    droppable: true,
    eventDrop: function(info) {
      moveAppt(info.event.id, info.event.startStr, info.event.endStr,
        info.event.getResources()[0] ? info.event.getResources()[0].id : null,
        info.revert);
    },
    eventResize: function(info) {
      moveAppt(info.event.id, info.event.startStr, info.event.endStr, null, info.revert);
    },
    eventContent: function(arg) {
      var p = arg.event.extendedProps;
      return { html: '<div class="fc-event-inner"><span class="fc-event-name">' +
        arg.event.title + '</span><span class="fc-event-phone">' + p.phone + '</span></div>' };
    },
    eventClick: function(info) {
      window.location.href = '/appointments/' + info.event.id + '/';
    }
  });
  calendar.render();

  function moveAppt(id, start, end, resourceId, revert) {
    var payload = {start: start, end: end};
    if (resourceId) payload.resourceId = resourceId;
    fetch('/appointments/api/' + id + '/move/', {
      method: 'POST',
      headers: {'Content-Type':'application/json','X-CSRFToken': getCsrf()},
      body: JSON.stringify(payload)
    })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (d.success) showToast('Запись перенесена', 'success');
      else { revert(); showToast('Ошибка переноса', 'danger'); }
    })
    .catch(function() { revert(); showToast('Сетевая ошибка', 'danger'); });
  }
});
""")

print("\nAll static files written successfully.")
