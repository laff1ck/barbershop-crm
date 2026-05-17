/* ===== FullCalendar Resource Timeline — Barbershop CRM ===== */
document.addEventListener('DOMContentLoaded', function () {
  var calEl = document.getElementById('barber-calendar');
  if (!calEl) return;

  var mastersEl = document.getElementById('masters-data');
  var resources  = mastersEl ? JSON.parse(mastersEl.textContent) : [];

  // ── Status meta ────────────────────────────────────────────────────────────
  var STATUS_LABELS = {
    pending:     'Ожидает',
    confirmed:   'Подтверждён',
    in_progress: 'В процессе',
    done:        'Завершён',
    cancelled:   'Отменён',
    no_show:     'Не явился'
  };
  var STATUS_BADGE = {
    pending:     'secondary',
    confirmed:   'warning',
    in_progress: 'info',
    done:        'success',
    cancelled:   'danger',
    no_show:     'purple'
  };

  // ── Helpers ────────────────────────────────────────────────────────────────
  function formatTime(date) {
    if (!date) return '';
    return date.getHours().toString().padStart(2, '0') + ':' +
           date.getMinutes().toString().padStart(2, '0');
  }

  function escHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  var mobile = window.innerWidth < 768;

  // ── Calendar init ──────────────────────────────────────────────────────────
  var calendar = new FullCalendar.Calendar(calEl, {
    schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',

    initialView: mobile ? 'listDay' : 'resourceTimelineDay',
    headerToolbar: mobile
      ? { left: 'prev,next', center: 'title', right: 'today' }
      : { left: 'prev,next today', center: 'title', right: 'resourceTimelineDay,resourceTimelineWeek,listDay' },
    buttonText: {
      today:                'Сегодня',
      prev:                 '‹',
      next:                 '›',
      resourceTimelineDay:  'День',
      resourceTimelineWeek: 'Неделя',
      listDay:              'Список'
    },

    locale:    'ru',
    firstDay:  1,
    direction: 'ltr',

    slotMinTime:       '10:00:00',
    slotMaxTime:       '22:00:00',
    slotDuration:      '00:30:00',
    slotLabelInterval: '01:00:00',
    slotLabelFormat:   { hour: '2-digit', minute: '2-digit', hour12: false },

    resources:               resources,
    resourceAreaHeaderContent: 'Мастера',
    resourceAreaWidth:       '180px',
    resourceLabelContent: function (arg) {
      return {
        html: '<div class="fc-resource-label">'
          + '<div class="fc-resource-avatar">' + escHtml(arg.resource.title.slice(0, 2).toUpperCase()) + '</div>'
          + '<div class="fc-resource-name">'  + escHtml(arg.resource.title) + '</div>'
          + '</div>'
      };
    },

    events: {
      url:     '/appointments/api/events/',
      method:  'GET',
    },

    height:                'auto',
    nowIndicator:          true,
    nowIndicatorClassNames: ['fc-now-gold'],
    weekNumbers:           false,
    allDaySlot:            false,

    scrollTime: '10:00:00',

    slotMinWidth: 90,

    editable:  true,
    droppable: true,
    eventDrop: function (info) {
      var res = info.event.getResources();
      moveAppt(
        info.event.id,
        info.event.startStr,
        info.event.endStr,
        res.length ? res[0].id : null,
        info.revert
      );
    },
    eventResize: function (info) {
      moveAppt(info.event.id, info.event.startStr, info.event.endStr, null, info.revert);
    },

    // ── Improved event card ──────────────────────────────────────────────────
    eventContent: function (arg) {
      var p          = arg.event.extendedProps;
      var start      = arg.event.start;
      var end        = arg.event.end;
      var startStr   = formatTime(start);
      var endStr     = end ? formatTime(end) : '';
      var clientName = escHtml(p.client_name || arg.event.title.split(' — ')[0]);
      var service    = escHtml(p.service || '');
      var price      = p.price ? p.price + ' ₽' : '';

      // Time rendered as two separate spans so the end time can wrap
      var timeHtml = '<div class="fc-event-card-time">'
        + '<span class="evt-time-start">' + startStr + '</span>'
        + (endStr
            ? '<span class="evt-time-sep">–</span>'
            + '<span class="evt-time-end">' + endStr + '</span>'
            : '')
        + '</div>';

      return {
        html: '<div class="fc-event-card">'
          + '<div class="fc-event-card-header">'
          +   timeHtml
          +   '<span class="fc-event-card-status status-dot-' + p.status + '"></span>'
          + '</div>'
          + '<div class="fc-event-card-name">' + clientName + '</div>'
          + '<div class="fc-event-card-service">' + service + '</div>'
          + (price ? '<div class="fc-event-card-price">' + price + '</div>' : '')
          + '</div>'
      };
    },

    // ── Click → popup panel ──────────────────────────────────────────────────
    eventClick: function (info) {
      info.jsEvent.preventDefault();
      showApptPopup(info.event);
    },

    // ── Adaptive card: only hides price on very narrow cards ────────────────
    eventDidMount: function (info) {
      var card = info.el.querySelector('.fc-event-card');
      if (!card) return;
      var w = info.el.offsetWidth;
      card.classList.remove('card-xs', 'card-xxs');
      if (w < 60)       card.classList.add('card-xxs');
      else if (w < 110) card.classList.add('card-xs');
    },

    loading: function (isLoading) {
      var loader = document.getElementById('calLoader');
      if (loader) loader.style.display = isLoading ? 'flex' : 'none';
    },

    datesSet: function () {
      forceDarkBg();
    }
  });

  calendar.render();
  window._barberCalendar = calendar;

  // ── Force dark bg: overrides any inline style FullCalendar sets ───────────
  var DARK = '#161616';
  var DARK_HDR = '#1e1e1e';

  function forceDarkBg() {
    var bodySelectors = [
      '.fc-scroller', '.fc-scroller-harness',
      '.fc-scroller-liquid', '.fc-scroller-liquid-absolute',
      '.fc-view', '.fc-view-harness', '.fc-view-harness-active',
      '.fc-scrollgrid td', '.fc-scrollgrid th',
      '.fc-timeline-body', '.fc-timeline-lane', '.fc-timeline-lane-frame',
      '.fc-timeline-slot', '.fc-timeline-slot-frame',
      '.fc-datagrid-body', '.fc-datagrid-cell', '.fc-datagrid-cell-frame',
      '.fc-resource-timeline-divider',
    ];
    var hdrSelectors = [
      '.fc-timeline-header', '.fc-timeline-header-row',
      '.fc-resource-area-header', '.fc-resource-group-cell',
    ];
    calEl.querySelectorAll(bodySelectors.join(',')).forEach(function(el) {
      el.style.setProperty('background', DARK, 'important');
      el.style.setProperty('background-color', DARK, 'important');
    });
    calEl.querySelectorAll(hdrSelectors.join(',')).forEach(function(el) {
      el.style.setProperty('background', DARK_HDR, 'important');
      el.style.setProperty('background-color', DARK_HDR, 'important');
    });
  }

  // Watch for any DOM changes FullCalendar makes and reapply dark bg
  var observer = new MutationObserver(function(mutations) {
    var needsFix = false;
    mutations.forEach(function(m) {
      if (m.type === 'attributes' && m.attributeName === 'style') needsFix = true;
      if (m.type === 'childList' && m.addedNodes.length) needsFix = true;
    });
    if (needsFix) forceDarkBg();
  });
  observer.observe(calEl, {
    subtree: true,
    childList: true,
    attributes: true,
    attributeFilter: ['style'],
  });

  // ── Appointment popup ──────────────────────────────────────────────────────
  var popup    = document.getElementById('apptPopup');
  var popupBg  = document.getElementById('apptPopupBg');

  function showApptPopup(event) {
    var p = event.extendedProps;
    var start = event.start;
    var end   = event.end;

    document.getElementById('pp-client').textContent  = event.title.split(' — ')[0];
    document.getElementById('pp-phone').textContent   = p.phone || '—';
    document.getElementById('pp-service').textContent = p.service || '—';
    document.getElementById('pp-master').textContent  =
      (event.getResources && event.getResources().length)
        ? event.getResources()[0].title
        : '—';
    document.getElementById('pp-time').textContent =
      formatTime(start) + (end ? ' – ' + formatTime(end) : '');
    document.getElementById('pp-price').textContent = (p.price || '—') + (p.price ? ' ₽' : '');
    document.getElementById('pp-link').href = '/appointments/' + event.id + '/';

    var badge = document.getElementById('pp-status');
    badge.textContent = STATUS_LABELS[p.status] || p.status;
    badge.className   = 'badge-status status-' + p.status;

    // Status action buttons
    var actionsEl = document.getElementById('pp-actions');
    actionsEl.innerHTML = '';
    Object.entries(STATUS_LABELS).forEach(function(entry) {
      var val = entry[0], label = entry[1];
      if (val === p.status) return;
      var btn = document.createElement('button');
      btn.className   = 'btn btn-ghost btn-sm';
      btn.textContent = label;
      btn.dataset.status = val;
      btn.addEventListener('click', function() {
        changeStatus(event.id, val, function() {
          badge.textContent = STATUS_LABELS[val] || val;
          badge.className   = 'badge-status status-' + val;
          p.status = val;
          // rebuild buttons
          showApptPopup(event);
          calendar.refetchEvents();
        });
      });
      actionsEl.appendChild(btn);
    });

    popup.classList.add('open');
    popupBg.classList.add('open');
  }

  function closePopup() {
    popup.classList.remove('open');
    popupBg.classList.remove('open');
  }

  if (popupBg) popupBg.addEventListener('click', closePopup);
  var closeBtn = document.getElementById('pp-close');
  if (closeBtn) closeBtn.addEventListener('click', closePopup);

  // ── AJAX helpers ──────────────────────────────────────────────────────────
  function moveAppt(id, start, end, resourceId, revert) {
    var payload = { start: start, end: end };
    if (resourceId) payload.resourceId = resourceId;
    fetch('/appointments/api/' + id + '/move/', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
      body:    JSON.stringify(payload)
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.success) showToast('Запись перенесена', 'success');
        else { revert(); showToast('Ошибка переноса', 'danger'); }
      })
      .catch(function () { revert(); showToast('Сетевая ошибка', 'danger'); });
  }

  function changeStatus(id, status, onSuccess) {
    fetch('/appointments/api/' + id + '/status/', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
      body:    JSON.stringify({ status: status })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.success) { showToast('Статус изменён', 'success'); onSuccess && onSuccess(); }
        else showToast('Ошибка', 'danger');
      })
      .catch(function () { showToast('Сетевая ошибка', 'danger'); });
  }

  // ── Date jump buttons ──────────────────────────────────────────────────────
  document.querySelectorAll('[data-cal-date]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      calendar.gotoDate(btn.dataset.calDate);
      calendar.changeView('resourceTimelineDay');
    });
  });
});
