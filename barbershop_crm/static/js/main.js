/* ===== CRM Global JS ===== */

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
  var toggle  = document.getElementById('sidebarToggle');
  var sidebar = document.querySelector('.crm-sidebar');
  var overlay = document.getElementById('sidebarOverlay');

  function openSidebar() {
    sidebar.classList.add('show');
    if (overlay) overlay.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('show');
    if (overlay) overlay.classList.remove('show');
    document.body.style.overflow = '';
  }

  if (toggle && sidebar) {
    toggle.addEventListener('click', function() {
      sidebar.classList.contains('show') ? closeSidebar() : openSidebar();
    });
  }

  // Click overlay to close
  if (overlay) {
    overlay.addEventListener('click', closeSidebar);
  }

  // Close sidebar on nav link click (mobile)
  if (sidebar) {
    sidebar.querySelectorAll('.nav-link').forEach(function(link) {
      link.addEventListener('click', function() {
        if (window.innerWidth <= 768) closeSidebar();
      });
    });
  }

  // Auto-dismiss django messages after 4s
  document.querySelectorAll('.auto-dismiss').forEach(function(el) {
    setTimeout(function() { el.remove(); }, 4000);
  });
});
