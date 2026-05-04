/* ===== Appointment status toggle ===== */
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
