(function () {
  const current = window.location.pathname.split('/').pop();
  if (current !== 'index.html' && !localStorage.getItem('traffic_auth')) {
    window.location.href = 'index.html';
  }
})();

document.getElementById('logoutBtn')?.addEventListener('click', function () {
  localStorage.removeItem('traffic_auth');
  localStorage.removeItem('traffic_user');
  window.location.href = 'index.html';
});
