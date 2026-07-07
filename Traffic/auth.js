document.getElementById('loginForm')?.addEventListener('submit', function (e) {
  e.preventDefault();
  localStorage.setItem('traffic_auth', 'true');
  localStorage.setItem('traffic_user', document.getElementById('username').value || 'admin');
  window.location.href = 'dashboard.html';
});
