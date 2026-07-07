const rawData = window.trafficData || [];
const els = {
  location: document.getElementById('locationFilter'),
  weather: document.getElementById('weatherFilter'),
  day: document.getElementById('dayFilter'),
  vehicle: document.getElementById('vehicleFilter'),
  total: document.getElementById('totalTraffic'),
  peak: document.getElementById('peakHour'),
  avg: document.getElementById('avgTraffic'),
  records: document.getElementById('recordCount'),
  topLocations: document.getElementById('topLocations'),
  reset: document.getElementById('resetFilters')
};

let charts = {};

function fillSelect(select, values, allLabel) {
  select.innerHTML = '';
  [allLabel, ...values].forEach(v => {
    const op = document.createElement('option');
    op.value = v;
    op.textContent = v;
    select.appendChild(op);
  });
}

function uniqueValues(key) {
  return [...new Set(rawData.map(d => d[key]))];
}

function initFilters() {
  fillSelect(els.location, uniqueValues('location'), 'All Locations');
  fillSelect(els.weather, uniqueValues('weather'), 'All Weather');
  fillSelect(els.day, uniqueValues('day'), 'All Days');
  fillSelect(els.vehicle, uniqueValues('vehicle'), 'All Vehicle Types');
  [els.location, els.weather, els.day, els.vehicle].forEach(el => el.addEventListener('change', updateDashboard));
  els.reset.addEventListener('click', () => {
    els.location.selectedIndex = 0;
    els.weather.selectedIndex = 0;
    els.day.selectedIndex = 0;
    els.vehicle.selectedIndex = 0;
    updateDashboard();
  });
}

function getFiltered() {
  return rawData.filter(d =>
    (els.location.value === 'All Locations' || d.location === els.location.value) &&
    (els.weather.value === 'All Weather' || d.weather === els.weather.value) &&
    (els.day.value === 'All Days' || d.day === els.day.value) &&
    (els.vehicle.value === 'All Vehicle Types' || d.vehicle === els.vehicle.value)
  );
}

function groupByHour(data) {
  const map = Array.from({ length: 24 }, (_, h) => ({ hour: h, count: 0 }));
  data.forEach(d => { map[d.hour].count += d.count; });
  return map;
}

function destroyCharts() {
  Object.values(charts).forEach(c => c.destroy());
}

function buildCharts(data) {
  destroyCharts();
  const hours = groupByHour(data);
  const ctxBar = document.getElementById('hourlyBar');
  const ctxLine = document.getElementById('trafficLine');
  const ctxPie = document.getElementById('vehiclePie');
  const ctxDough = document.getElementById('weatherDoughnut');

  charts.bar = new Chart(ctxBar, {
    type: 'bar',
    data: {
      labels: hours.map(x => x.hour),
      datasets: [{ label: 'Traffic', data: hours.map(x => x.count), backgroundColor: '#3b82f6', borderRadius: 8 }]
    },
    options: commonOptions(false)
  });

  charts.line = new Chart(ctxLine, {
    type: 'line',
    data: {
      labels: hours.map(x => x.hour),
      datasets: [{ label: 'Traffic Trend', data: hours.map(x => x.count), borderColor: '#10d3a0', backgroundColor: 'rgba(16,211,160,.15)', tension: .35, fill: true }]
    },
    options: commonOptions(true)
  });

  const vehicleCounts = countBy(data, 'vehicle');
  charts.pie = new Chart(ctxPie, {
    type: 'pie',
    data: {
      labels: Object.keys(vehicleCounts),
      datasets: [{ data: Object.values(vehicleCounts), backgroundColor: ['#4f8ef7','#1dbb84','#f59e0b','#8b5cf6','#ef4444'] }]
    },
    options: pieOptions()
  });

  const weatherCounts = countBy(data, 'weather');
  charts.dough = new Chart(ctxDough, {
    type: 'doughnut',
    data: {
      labels: Object.keys(weatherCounts),
      datasets: [{ data: Object.values(weatherCounts), backgroundColor: ['#40a9db','#22c55e','#9f85ec','#f97316'] }]
    },
    options: pieOptions()
  });
}

function commonOptions(fillArea) {
  return {
    maintainAspectRatio: false,
    plugins: { legend: { labels: { color: '#d6e5ff' } } },
    scales: {
      x: { ticks: { color: '#d6e5ff' }, grid: { color: 'rgba(255,255,255,.06)' } },
      y: { ticks: { color: '#d6e5ff' }, grid: { color: 'rgba(255,255,255,.06)' } }
    }
  };
}

function pieOptions() {
  return {
    maintainAspectRatio: false,
    plugins: { legend: { labels: { color: '#d6e5ff' } } }
  };
}

function countBy(data, key) {
  return data.reduce((acc, item) => {
    acc[item[key]] = (acc[item[key]] || 0) + 1;
    return acc;
  }, {});
}

function updateSummary(data) {
  const total = data.reduce((sum, x) => sum + x.count, 0);
  const avg = data.length ? (total / data.length).toFixed(1) : 0;
  const byHour = groupByHour(data);
  const peakRow = byHour.reduce((a, b) => b.count > a.count ? b : a, { hour: 0, count: 0 });

  els.total.textContent = total.toLocaleString();
  els.avg.textContent = avg;
  els.peak.textContent = `${String(peakRow.hour).padStart(2,'0')}:00`;
  els.records.textContent = data.length;

  const locCounts = data.reduce((acc, x) => {
    acc[x.location] = (acc[x.location] || 0) + x.count;
    return acc;
  }, {});

  els.topLocations.innerHTML = Object.entries(locCounts)
    .sort((a,b) => b[1]-a[1])
    .slice(0,3)
    .map(([name, value]) => `<div class="summary-item"><span>${name}</span><span>${value.toLocaleString()}</span></div>`)
    .join('') || '<div class="summary-item"><span>No matching data</span><span>0</span></div>';
}

function updateDashboard() {
  const filtered = getFiltered();
  updateSummary(filtered);
  buildCharts(filtered);
}

initFilters();
updateDashboard();
