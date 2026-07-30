/* ==============================================================================================
   CH-LAE meteo calendar explorer - rendering engine
   ----------------------------------------------------------------------------------------------
   Three views over one payload: the grid of every month, one month with its days, and one day with
   its diurnal course. No external libraries - the page has to open from disk, so everything it
   needs travels inside it.

   The conventions are the dashboards' own, for the same reasons.
   - Colours come from CSS custom properties, never from literals here, so the light and the dark
     token sets are the only place a colour is decided and the toggle recolours every mark.
   - Every chart is re-rendered from its data on resize and on a theme change rather than scaled,
     so text stays one size at every viewport width.
   - A tooltip enhances a mark, it never gates a value: the month view carries the same numbers as
     a table.

   One addition of its own: the colour domains are computed in Python and shipped, so the scale bar,
   the tiles and the micro-strips inside them all read one scale, and hiding part of the grid with a
   badge filter does not repaint the months that remain.
   ============================================================================================== */

(function () {
  'use strict';

  const DATA = JSON.parse(document.getElementById('payload').textContent);
  const M = DATA.meta;
  const VARS = {};
  DATA.variables.forEach(v => { VARS[v.key] = v; });
  const METRICS = {};
  DATA.metrics.forEach(m => { METRICS[m.key] = m; });
  const BADGES = {};
  DATA.badges.forEach(b => { BADGES[b.key] = b; });
  const FLAGS = DATA.flags;
  const MONTHS = DATA.months;
  const DAYS = DATA.days;
  const NORM = DATA.normals;
  const CLIM = DATA.climatology;
  const HOURLY = DATA.hourly;

  const MONTH_ABBR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const MONTH_NAME = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'];
  const WEEKDAY = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const WEEKDAY_LONG = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
    'Sunday'];

  /* Which day tests are worth a mark on a day cell, in the order a cell fills its three slots.
     The frequent ones (a summer day, a wet day) are left out: a mark that is on half the cells of
     a July separates nothing, and a wet day already has its own bar along the bottom. Records come
     first because they are the rarest thing a day can be. */
  const DAY_MARKS = [
    ['recwarm', { icon: 'star', tone: 'warm', label: 'warmest for its date' }],
    ['reccold', { icon: 'star', tone: 'cold', label: 'coldest for its date' }],
    ['recwet', { icon: 'star', tone: 'wet', label: 'wettest for its date' }],
    ['verywet', { icon: 'cloud-rain', tone: 'wet', label: 'above 30 mm' }],
    ['hot', { icon: 'flame', tone: 'warm', label: 'hot day' }],
    ['ice', { icon: 'icicles', tone: 'cold', label: 'ice day' }],
    ['tropical', { icon: 'moon', tone: 'warm', label: 'tropical night' }],
    ['heavy', { icon: 'cloud-rain', tone: 'wet', label: 'above 10 mm' }],
    ['coldprec', { icon: 'snow-cloud', tone: 'cold', label: 'precipitation below 1 °C' }],
    ['frost', { icon: 'snowflake', tone: 'cold', label: 'frost day' }],
    ['freezethaw', { icon: 'thermo-swing', tone: 'cold', label: 'crossed freezing' }],
    ['clear', { icon: 'sun', tone: 'sun', label: 'in the brightest tenth for its date' }],
    ['saturated', { icon: 'fog', tone: 'dull', label: 'mean humidity above 95 %' }]
  ];

  /* ------------------------------------------------------------------------------------------
     Icons
     ------------------------------------------------------------------------------------------
     Drawn rather than fetched, and named by the badge registry in Python, which asserts that every
     badge's icon exists here - a badge whose icon is missing would render as an empty box.
     Keep the four-space indentation of the keys: the build reads them from this file.
     ------------------------------------------------------------------------------------------ */

  const ICONS = {
    'flame': '<path d="M12 3c3.2 4 5 5.8 5 8.9A5 5 0 0 1 7 12c0-1.7.6-3 1.6-4.2C9.6 9.3 11.2 6.2 12 3z"/>',
    'flames': '<path d="M9.5 3c2.4 3 3.8 4.4 3.8 6.7a3.8 3.8 0 0 1-7.6 0c0-1.3.5-2.3 1.2-3.2.8 1.1 2 .4 2.6-3.5z"/><path d="M17 10.5c1.4 1.9 2.3 2.6 2.3 4a2.3 2.3 0 0 1-4.6 0c0-.8.3-1.4.7-1.9.5.7 1.2.2 1.6-2.1z"/>',
    'snowflake': '<path d="M12 2v20M4.2 7l15.6 10M19.8 7L4.2 17M12 6l-2.4-2.4M12 6l2.4-2.4M12 18l-2.4 2.4M12 18l2.4 2.4"/>',
    'icicles': '<path d="M3 5h18M7 5v5l1.4 4.5L9.8 10V5M14 5v7l1.4 5 1.4-5V5"/>',
    'moon': '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/>',
    'droplets': '<path d="M8.4 2.5s3.9 4.2 3.9 6.5a3.9 3.9 0 1 1-7.8 0c0-2.3 3.9-6.5 3.9-6.5z"/><path d="M16.2 11.2s3.2 3.5 3.2 5.4a3.2 3.2 0 1 1-6.4 0c0-1.9 3.2-5.4 3.2-5.4z"/>',
    'droplet-off': '<path d="M12 3.2s5.2 5.6 5.2 8.8a5.2 5.2 0 0 1-10.4 0C6.8 8.8 12 3.2 12 3.2z"/><path d="M3.5 3.5l17 17"/>',
    'cloud-rain': '<path d="M17.5 16H9a6 6 0 1 1 5.7-7.8h2.8a4 4 0 1 1 0 7.8z"/><path d="M8.5 19v2.5M12 19v3M15.5 19v2.5"/>',
    'calendar-dry': '<rect x="3" y="4.5" width="18" height="17" rx="2.5"/><path d="M8 2.5v4M16 2.5v4M3 10h18M8.5 15.5h7"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2.4M12 19.6V22M4.2 4.2l1.7 1.7M18.1 18.1l1.7 1.7M2 12h2.4M19.6 12H22M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/>',
    'cloud': '<path d="M17.5 19H9a6.5 6.5 0 1 1 6.2-8.5h2.3a4.25 4.25 0 1 1 0 8.5z"/>',
    'gauge': '<path d="M3.6 18.5a10 10 0 1 1 16.8 0"/><path d="M12 14.5l4.2-4.7"/><circle cx="12" cy="15.5" r="1.6"/>',
    'soil': '<path d="M3.5 11h17v9.5h-17z"/><path d="M12 11V6.5"/><path d="M12 8.5c-2.2 0-3.4-1.2-3.4-3 1.9 0 3.4 1.2 3.4 3zM12 8.5c2.2 0 3.4-1.2 3.4-3-1.9 0-3.4 1.2-3.4 3z"/>',
    'award': '<circle cx="12" cy="8.5" r="5.6"/><path d="M15.4 13.4 17 22l-5-2.9L7 22l1.6-8.6"/>',
    'arrow-up': '<path d="M12 20V4M5 11l7-7 7 7"/>',
    'arrow-down': '<path d="M12 4v16M19 13l-7 7-7-7"/>',
    'alert': '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9.5v4.2M12 17.4h.01"/>',
    'sprout': '<path d="M7 20.5h10"/><path d="M12 20.5c0-5 0-7 0-9"/><path d="M12 11.5c-2.6 0-4.2-1.4-4.8-4.2 2.8-.3 4.6.9 4.8 4.2zM12 11.5c2.6 0 4.2-1.9 4.8-5.2-2.8.3-4.6 1.9-4.8 5.2z"/>',
    'leaf-fall': '<path d="M11.5 19.5A6.5 6.5 0 0 1 10.4 6.6C15.7 5.5 17.1 5 19 2.7c.9 1.9 1.8 3.9 1.8 7.4 0 5.1-4.4 9.4-9.3 9.4z"/><path d="M2.5 21.5c0-2.8 1.7-5 4.7-5.6 2.2-.4 4.5-1.9 5.4-2.9"/>',
    'star': '<path d="m12 2.6 2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3-5.8 3 1.1-6.5-4.7-4.6 6.5-.9z"/>',
    'snow-cloud': '<path d="M17.5 15.5H9a6 6 0 1 1 5.7-7.8h2.8a4 4 0 1 1 0 7.8z"/><path d="M8.5 18.5v2.4M7.3 19.1l2.4 1.2M9.7 19.1l-2.4 1.2M15.5 18.5v2.4M14.3 19.1l2.4 1.2M16.7 19.1l-2.4 1.2"/>',
    'thermo-swing': '<path d="M12 3.2v17.6"/><path d="m7.5 7.7 4.5-4.5 4.5 4.5"/><path d="m7.5 16.3 4.5 4.5 4.5-4.5"/>',
    'fog': '<path d="M3 7.5h18M6 11.5h13M3.5 15.5h14M8 19.5h11"/>'
  };

  function glyph(name) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
      + 'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
      + (ICONS[name] || '') + '</svg>';
  }

  /** A badge as a solid chip: the family in the background, the badge in the symbol. */
  function chip(key, size) {
    const b = BADGES[key];
    if (!b) return '';
    return '<span class="chip chip-' + b.tone + (size ? ' ' + size : '') + '" role="img" '
      + 'aria-label="' + b.label + '">' + glyph(b.icon) + '</span>';
  }

  /** The same chip for a day mark, which has no badge entry of its own. */
  function markChip(mark, size) {
    return '<span class="chip chip-' + mark.tone + (size ? ' ' + size : '') + '" role="img" '
      + 'aria-label="' + mark.label + '">' + glyph(mark.icon) + '</span>';
  }

  /* ------------------------------------------------------------------------------------------
     Formatting
     ------------------------------------------------------------------------------------------ */

  const isNum = v => v !== null && v !== undefined && !Number.isNaN(v);
  const nf = (v, d = 1) => isNum(v) ? v.toFixed(d) : '–';
  const nfs = (v, d = 1) => isNum(v) ? (v > 0 ? '+' : '') + v.toFixed(d) : '–';
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const ord = n => {
    if (!isNum(n)) return '–';
    const s = ['th', 'st', 'nd', 'rd'], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  };

  function token(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function palette() {
    return {
      series: [token('--series-1'), token('--series-2'), token('--series-3'), token('--series-4')],
      cold: token('--pole-cold'), warm: token('--pole-warm'), mid: token('--neutral-mid'),
      bandOuter: token('--band-outer'), bandInner: token('--band-inner'),
      ink: token('--text-primary'), ink2: token('--text-secondary'), muted: token('--text-muted'),
      axis: token('--axis'), grid: token('--grid'), surface: token('--surface')
    };
  }

  /* ------------------------------------------------------------------------------------------
     Colour
     ------------------------------------------------------------------------------------------ */

  function hex2rgb(h) {
    h = h.replace('#', '');
    if (h.length === 3) h = h.split('').map(c => c + c).join('');
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }
  const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);

  function rampRGB(stops, t) {
    t = Math.max(0, Math.min(1, t));
    const pos = t * (stops.length - 1);
    const i = Math.min(stops.length - 2, Math.floor(pos));
    return mix(stops[i], stops[i + 1], pos - i);
  }
  const css = c => 'rgb(' + c.map(v => Math.round(v)).join(',') + ')';

  /* Relative luminance, so a tile's ink is chosen against the tile rather than against the page.
     Both ends of a sequential ramp end up on a tile, and one ink cannot serve both. */
  function luminance(rgb) {
    const c = rgb.map(v => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }

  /**
   * The colour of one value on one metric's scale, as [rgb, inkClass].
   * `which` selects the monthly domain or the wider one the daily strips need.
   */
  function metricColor(metric, value, which) {
    if (!isNum(value)) return null;
    const domain = which === 'day' ? metric.day_domain : metric.domain;
    if (metric.scale === 'div') {
      const center = metric.center === null ? 0 : metric.center;
      const absmax = Math.max(domain[1] - center, center - domain[0]) || 1;
      const t = (value - center) / absmax;
      const mid = hex2rgb(token('--neutral-mid'));
      const pole = hex2rgb(token(metric.poles[t >= 0 ? 1 : 0]));
      return rampRGB([mid, pole], Math.min(1, Math.abs(t)));
    }
    const stops = metric.stops.map(s => hex2rgb(token(s)));
    const t = (value - domain[0]) / ((domain[1] - domain[0]) || 1);
    return rampRGB(stops, t);
  }

  const inkClass = rgb => luminance(rgb) < 0.45 ? 'on-dark' : 'on-light';

  /* ------------------------------------------------------------------------------------------
     Scales, ticks, SVG
     ------------------------------------------------------------------------------------------ */

  function linear(d0, d1, r0, r1) {
    const span = (d1 - d0) || 1;
    const f = v => r0 + (v - d0) / span * (r1 - r0);
    f.domain = [d0, d1];
    f.range = [r0, r1];
    return f;
  }

  function niceTicks(min, max, count) {
    if (min === max) { min -= 1; max += 1; }
    const raw = (max - min) / Math.max(1, count);
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const norm = raw / mag;
    const step = (norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10) * mag;
    const out = [];
    for (let v = Math.ceil(min / step) * step; v <= max + step * 1e-9; v += step) {
      out.push(Math.abs(v) < step * 1e-9 ? 0 : +v.toFixed(10));
    }
    return out;
  }

  function extent(arrays) {
    let lo = Infinity, hi = -Infinity;
    arrays.forEach(a => a.forEach(v => {
      if (!isNum(v)) return;
      if (v < lo) lo = v;
      if (v > hi) hi = v;
    }));
    if (!isFinite(lo)) { lo = 0; hi = 1; }
    if (lo === hi) { lo -= 1; hi += 1; }
    return [lo, hi];
  }

  const NS = 'http://www.w3.org/2000/svg';

  function el(tag, attrs, parent) {
    const node = document.createElementNS(NS, tag);
    for (const k in attrs) {
      if (attrs[k] === null || attrs[k] === undefined) continue;
      node.setAttribute(k, attrs[k]);
    }
    if (parent) parent.appendChild(node);
    return node;
  }

  function svgText(parent, x, y, str, cls, extra) {
    const t = el('text', Object.assign({ x: x, y: y, class: cls || 'ax-text' }, extra || {}), parent);
    t.textContent = str;
    return t;
  }

  function pathFrom(xs, ys, sx, sy) {
    let d = '', pen = false;
    for (let i = 0; i < xs.length; i++) {
      if (!isNum(ys[i])) { pen = false; continue; }
      d += (pen ? 'L' : 'M') + sx(xs[i]).toFixed(2) + ' ' + sy(ys[i]).toFixed(2);
      pen = true;
    }
    return d;
  }

  function areaFrom(xs, lo, hi, sx, sy) {
    const up = [], down = [];
    for (let i = 0; i < xs.length; i++) {
      if (!isNum(lo[i]) || !isNum(hi[i])) continue;
      up.push(sx(xs[i]).toFixed(2) + ' ' + sy(hi[i]).toFixed(2));
      down.unshift(sx(xs[i]).toFixed(2) + ' ' + sy(lo[i]).toFixed(2));
    }
    return up.length ? 'M' + up.join('L') + 'L' + down.join('L') + 'Z' : '';
  }

  /* ------------------------------------------------------------------------------------------
     Tooltip
     ------------------------------------------------------------------------------------------ */

  const tipNode = document.getElementById('tooltip');
  const tip = {
    show(html, x, y) {
      tipNode.innerHTML = html;
      tipNode.classList.add('on');
      const box = tipNode.getBoundingClientRect();
      const left = Math.max(8 + box.width / 2, Math.min(window.innerWidth - 8 - box.width / 2, x));
      const top = y - 12 < box.height + 8 ? y + box.height + 24 : y - 12;
      tipNode.style.left = left + 'px';
      tipNode.style.top = top + 'px';
    },
    hide() { tipNode.classList.remove('on'); }
  };

  function tipRows(title, rows) {
    let html = '<div class="tt-title">' + title + '</div>';
    rows.forEach(r => {
      if (r.rule) { html += '<div class="tt-row"><span class="k">' + r.k + '</span></div>'; return; }
      html += '<div class="tt-row">'
        + (r.color ? '<span class="sw" style="background:' + r.color + '"></span>' : '')
        + '<span class="k">' + r.k + '</span><span class="v">' + r.v + '</span></div>';
    });
    return html;
  }

  /* ------------------------------------------------------------------------------------------
     Chart frame
     ------------------------------------------------------------------------------------------ */

  function frame(host, spec) {
    const p = palette();
    const width = Math.max(260, host.clientWidth || 640);
    const height = spec.height
      || Math.round(Math.max(170, Math.min(400, width * (spec.aspect || 0.42))));
    const m = Object.assign({ top: 12, right: 14, bottom: 30, left: 46 }, spec.margin || {});
    const svg = el('svg', {
      viewBox: '0 0 ' + width + ' ' + height, width: width, height: height,
      role: 'img', 'aria-label': spec.ariaLabel || ''
    });
    host.innerHTML = '';
    host.appendChild(svg);
    return { svg: svg, p: p, width: width, height: height, m: m,
      iw: width - m.left - m.right, ih: height - m.top - m.bottom };
  }

  function drawAxes(f, sx, sy, spec) {
    const { svg, m, iw, ih } = f;
    const g = el('g', {}, svg);
    const yTicks = spec.yTicks || niceTicks(sy.domain[0], sy.domain[1], spec.yTickCount || 4);
    yTicks.forEach(v => {
      const y = sy(v);
      if (y < m.top - 1 || y > m.top + ih + 1) return;
      el('line', { x1: m.left, x2: m.left + iw, y1: y, y2: y, class: 'gridline' }, g);
      svgText(g, m.left - 8, y + 4, nf(v, spec.yDigits === undefined ? 0 : spec.yDigits),
        'ax-text', { 'text-anchor': 'end' });
    });
    el('line', { x1: m.left, x2: m.left + iw, y1: m.top + ih, y2: m.top + ih, class: 'ax-line' }, g);
    (spec.xTicks || []).forEach(t => {
      const x = sx(t.v);
      if (x < m.left - 1 || x > m.left + iw + 1) return;
      el('line', { x1: x, x2: x, y1: m.top + ih, y2: m.top + ih + 4, class: 'ax-line' }, g);
      svgText(g, x, m.top + ih + 16, t.label, 'ax-text', { 'text-anchor': 'middle' });
    });
    if (spec.yLabel) {
      const t = svgText(g, 0, 0, spec.yLabel, 'ax-title', { 'text-anchor': 'middle' });
      t.setAttribute('transform',
        'translate(' + (m.left - 33) + ',' + (m.top + ih / 2) + ') rotate(-90)');
    }
    return g;
  }

  /* Charts redraw from their data on a resize and on a theme change rather than being scaled, so
     text stays one size at every width. A chart whose host has left the document - the month view
     is rebuilt whole - drops out of the registry instead of being redrawn into nothing. */
  let charts = [];

  function mountChart(host, draw) {
    charts.push({ host: host, draw: draw });
    let last = 0;
    new ResizeObserver(() => {
      if (!host.isConnected || host.hidden) return;
      if (Math.abs(host.clientWidth - last) > 6) { last = host.clientWidth; draw(host); }
    }).observe(host);
    draw(host);
  }

  function compactCharts() { charts = charts.filter(c => c.host.isConnected); }
  function redrawAll() {
    compactCharts();
    charts.forEach(c => c.draw(c.host));
  }

  /* ------------------------------------------------------------------------------------------
     Cards
     ------------------------------------------------------------------------------------------ */

  function cardEl(parent, def) {
    const node = document.createElement('section');
    node.className = 'card ' + (def.width || 'w-6');
    node.innerHTML = '<div class="card-head"><div><h3 class="card-title">' + def.title + '</h3>'
      + (def.sub ? '<p class="card-sub">' + def.sub + '</p>' : '') + '</div></div>'
      + '<div class="card-body"></div>'
      + (def.foot ? '<p class="card-foot">' + def.foot + '</p>' : '');
    parent.appendChild(node);
    return node.querySelector('.card-body');
  }

  function legendHTML(items) {
    return '<div class="legend">' + items.map(i =>
      '<span class="legend-item"><span class="legend-swatch ' + (i.line ? 'line' : '')
      + '" style="background:' + i.color + '"></span>' + i.label + '</span>').join('') + '</div>';
  }

  function chartCard(parent, def) {
    const body = cardEl(parent, def);
    const host = document.createElement('div');
    host.className = 'chart';
    body.appendChild(host);
    if (def.legend) body.insertAdjacentHTML('beforeend', legendHTML(def.legend));
    mountChart(host, def.draw);
    return body;
  }

  function tableHTML(columns, rows) {
    let html = '<div class="tablewrap"><table><thead><tr>';
    columns.forEach(c => { html += '<th>' + c + '</th>'; });
    html += '</tr></thead><tbody>';
    rows.forEach(row => {
      html += '<tr>';
      row.forEach(cell => {
        if (cell && typeof cell === 'object') {
          html += '<td class="' + (cell.cls || '') + '">' + cell.v + '</td>';
        } else {
          html += '<td>' + (cell === null || cell === undefined ? '–' : cell) + '</td>';
        }
      });
      html += '</tr>';
    });
    return html + '</tbody></table></div>';
  }

  /* ------------------------------------------------------------------------------------------
     Indexing helpers
     ------------------------------------------------------------------------------------------ */

  const DAY0 = Date.parse(DAYS.start + 'T00:00:00Z');
  const YEARS = [];
  for (let y = M.first_year; y <= M.last_year; y++) YEARS.push(y);

  const monthIndex = {};
  MONTHS.forEach((mo, i) => { monthIndex[mo.y + '-' + mo.m] = i; });
  const monthAt = (y, m) => MONTHS[monthIndex[y + '-' + m]];

  const dayIndex = (y, m, d) => Math.round((Date.UTC(y, m - 1, d) - DAY0) / 86400000);
  const isLeap = y => (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;

  /** Day of year with 29 February folded onto 1 March, matching how the normals were built. */
  function doy365(y, m, d) {
    const doy = Math.round((Date.UTC(y, m - 1, d) - Date.UTC(y, 0, 1)) / 86400000) + 1;
    return (isLeap(y) && doy > 59) ? doy - 1 : doy;
  }

  const dayStat = (v, stat, i) => {
    const arr = DAYS.series[v + '_' + stat];
    return arr ? arr[i] : null;
  };
  const dayNormal = (v, stat, y, m, d) => {
    const n = NORM[v] && NORM[v][stat];
    return n ? n.mean[doy365(y, m, d)] : null;
  };
  const flagSet = (word, key) => {
    const f = FLAGS.find(x => x.key === key);
    return f ? (word & (1 << f.bit)) !== 0 : false;
  };

  /** The daily quantity a metric shows inside a tile, for one day index. */
  function dayValue(metric, i, y, m, d) {
    const spec = metric.day;
    if (spec.kind === 'none') return null;
    if (spec.kind === 'meas') return DAYS.meas[metric.var][i];
    if (spec.kind === 'flag') return flagSet(DAYS.flags[i], spec.flag) ? 1 : 0;
    if (spec.kind === 'range') {
      const lo = dayStat(metric.var, spec.stats[0], i);
      const hi = dayStat(metric.var, spec.stats[1], i);
      return isNum(lo) && isNum(hi) ? hi - lo : null;
    }
    const v = dayStat(metric.var, spec.stat, i);
    if (!isNum(v)) return null;
    if (spec.kind === 'anom') {
      const n = dayNormal(metric.var, spec.stat, y, m, d);
      return isNum(n) ? v - n : null;
    }
    return v;
  }

  function dayColor(metric, value) {
    if (!isNum(value)) return null;
    if (metric.day.kind === 'flag') {
      return value ? hex2rgb(token(metric.stops[metric.stops.length - 1])) : null;
    }
    return metricColor(metric, value, 'day');
  }

  /** The value a tile shows, and the number that belongs beside it. */
  function monthValue(metric, mo) {
    if (metric.field === 'count') return mo.c[metric.count];
    if (metric.field === 'spell') return mo.sp[metric.spell];
    if (metric.field === 'extra') {
      const v = mo.x[metric.extra];
      return v === undefined ? null : v;
    }
    const short = { value: 'v', anom: 'a', pctn: 'p', meas: 'meas' }[metric.field];
    return mo[metric.var] ? mo[metric.var][short] : null;
  }

  /* A departure is written with its sign wherever it appears: "2.8" and "+2.8" are the same number
     only if the reader already knows which of the two the tile is showing. */
  const metricFormat = (metric, value) =>
    metric.field === 'anom' ? nfs(value, metric.digits) : nf(value, metric.digits);

  function monthSub(metric, mo) {
    const rec = mo[metric.var];
    if (!rec) return '';
    if (metric.field === 'anom') return nf(rec.v, metric.digits) + ' ' + metric.units;
    if (metric.field === 'pctn') return nf(rec.v, 0) + ' ' + VARS[metric.var].units;
    if (metric.field === 'value' && isNum(rec.a)) return nfs(rec.a, metric.digits);
    return '';
  }

  /* ------------------------------------------------------------------------------------------
     State
     ------------------------------------------------------------------------------------------ */

  const state = {
    metric: DATA.metrics[0].key,
    strips: true,
    filters: new Set(),
    y: null, m: null, d: null
  };
  const metric = () => METRICS[state.metric];

  /* ------------------------------------------------------------------------------------------
     Level 1: the grid
     ------------------------------------------------------------------------------------------ */

  function buildControls() {
    const host = document.getElementById('controls');
    let html = '<div class="control"><label for="metric-pick">Colour the months by</label>'
      + '<select class="picker" id="metric-pick">';
    DATA.metrics.forEach(m => {
      html += '<option value="' + m.key + '">' + m.label + '</option>';
    });
    html += '</select></div>'
      + '<div class="control"><span class="control-label">Detail</span><div class="switchrow">'
      + '<label class="switch"><input type="checkbox" id="strip-toggle" checked>'
      + 'Show each day inside the tile</label></div></div>'
      + '<p class="control-note" id="metric-about"></p>';
    host.innerHTML = html;

    const pick = document.getElementById('metric-pick');
    pick.value = state.metric;
    pick.addEventListener('change', () => {
      state.metric = pick.value;
      renderGrid();
    });
    document.getElementById('strip-toggle').addEventListener('change', ev => {
      state.strips = ev.target.checked;
      renderGrid();
    });
  }

  function cellTooltip(mo) {
    const rows = [];
    DATA.variables.forEach(v => {
      const rec = mo[v.key];
      if (!rec || !isNum(rec.v)) return;
      let line = nf(rec.v, v.digits) + ' ' + v.units;
      if (isNum(rec.a)) line += ' (' + nfs(rec.a, v.digits) + ')';
      rows.push({ k: v.short, v: line });
    });
    if (mo.c.hot || mo.c.frost || mo.c.wet) {
      rows.push({ k: 'Threshold days',
        v: [mo.c.hot ? mo.c.hot + ' hot' : null, mo.c.frost ? mo.c.frost + ' frost' : null,
          mo.c.wet ? mo.c.wet + ' wet' : null].filter(Boolean).join(', ') });
    }
    if (mo.b.length) rows.push({ k: mo.b.map(b => BADGES[b.k].label).join(' · '), rule: true });
    return tipRows(MONTH_NAME[mo.m - 1] + ' ' + mo.y, rows);
  }

  function stripSVG(mo, met) {
    const parts = [];
    const w = 100 / mo.n;
    for (let d = 1; d <= mo.n; d++) {
      const i = mo.i0 + d - 1;
      const value = dayValue(met, i, mo.y, mo.m, d);
      const rgb = dayColor(met, value);
      if (!rgb) continue;
      parts.push('<rect x="' + ((d - 1) * w).toFixed(2) + '" y="0" width="'
        + (w * 0.84).toFixed(2) + '" height="10" fill="' + css(rgb) + '"/>');
    }
    return '<svg class="cell-strip" viewBox="0 0 100 10" preserveAspectRatio="none" '
      + 'aria-hidden="true">' + parts.join('') + '</svg>';
  }

  function matchesFilter(mo) {
    if (!state.filters.size) return true;
    return mo.b.some(b => state.filters.has(b.k));
  }

  function renderGrid() {
    const met = metric();
    const host = document.getElementById('calgrid');
    const parts = [];

    parts.push('<div class="calhead corner">Year</div>');
    MONTH_ABBR.forEach(a => parts.push('<div class="calhead">' + a + '</div>'));
    parts.push('<div class="calhead">Year</div>');

    YEARS.forEach(y => {
      parts.push('<div class="calyear">' + y + '</div>');
      const yearValues = [];
      for (let m = 1; m <= 12; m++) {
        const mo = monthAt(y, m);
        const value = mo ? monthValue(met, mo) : null;
        if (isNum(value)) yearValues.push(value);
        if (!mo || !isNum(value)) {
          parts.push('<div class="cell empty" aria-hidden="true"></div>');
          continue;
        }
        const rgb = metricColor(met, value, 'month');
        const sparse = isNum(mo[met.var] && mo[met.var].meas)
          && mo[met.var].meas < M.sparse_coverage;
        const shown = mo.b.slice(0, 4);
        const cls = ['cell', inkClass(rgb)];
        if (sparse) cls.push('sparse');
        if (!matchesFilter(mo)) cls.push('dim');
        else if (state.filters.size) cls.push('hit');

        let inner = '<span class="cell-value">' + metricFormat(met, value) + '</span>';
        const sub = monthSub(met, mo);
        if (sub) inner += '<span class="cell-sub">' + sub + '</span>';
        inner += '<span class="cell-badges">'
          + shown.map(b => chip(b.k, 'sm')).join('')
          + (mo.b.length > shown.length
            ? '<span class="more">+' + (mo.b.length - shown.length) + '</span>' : '')
          + '</span>';
        if (state.strips) inner += stripSVG(mo, met);

        parts.push('<button type="button" class="' + cls.join(' ') + '" style="background:'
          + css(rgb) + '" data-y="' + y + '" data-m="' + m + '" '
          + 'aria-label="' + MONTH_NAME[m - 1] + ' ' + y + '">' + inner + '</button>');
      }
      const summary = summarise(met, yearValues);
      parts.push('<div class="calsummary"><span class="v">' + metricFormat(met, summary)
        + '</span><span class="k">' + (met.field === 'count' || VARS[met.var].agg === 'sum'
          ? 'total' : 'mean') + '</span></div>');
    });

    host.innerHTML = parts.join('');
    host.querySelectorAll('.cell:not(.empty)').forEach(node => {
      const y = +node.dataset.y, m = +node.dataset.m;
      node.addEventListener('click', () => { location.hash = y + '-' + String(m).padStart(2, '0'); });
      node.addEventListener('mousemove', ev => tip.show(cellTooltip(monthAt(y, m)), ev.clientX, ev.clientY));
      node.addEventListener('mouseleave', tip.hide);
      node.addEventListener('focus', () => {
        const box = node.getBoundingClientRect();
        tip.show(cellTooltip(monthAt(y, m)), box.left + box.width / 2, box.top);
      });
      node.addEventListener('blur', tip.hide);
    });

    document.getElementById('metric-about').textContent = met.about;
    renderScaleBar();
    renderGridNote();
  }

  /** A year's figure on the active metric: summed where the quantity sums, averaged otherwise. */
  function summarise(met, values) {
    if (!values.length) return null;
    const sums = met.field === 'count' || (met.field === 'value' && VARS[met.var].agg === 'sum');
    const total = values.reduce((a, b) => a + b, 0);
    return sums ? total : total / values.length;
  }

  function renderScaleBar() {
    const met = metric();
    const host = document.getElementById('scalebar');
    host.innerHTML = '';
    const width = Math.max(240, host.clientWidth || 320);
    const height = 44;
    const svg = el('svg', { viewBox: '0 0 ' + width + ' ' + height, width: width, height: height,
      role: 'img', 'aria-label': 'Colour scale for ' + met.label }, host);
    svgText(svg, 0, 11, met.label + (met.units ? ' (' + met.units + ')' : ''), 'ax-title',
      { 'text-anchor': 'start' });
    const n = 44, y0 = 18, h = 12;
    const [lo, hi] = met.domain;
    for (let i = 0; i < n; i++) {
      const v = lo + (hi - lo) * (i / (n - 1));
      const rgb = metricColor(met, v, 'month');
      el('rect', { x: (i * width / n).toFixed(2), y: y0, width: (width / n + 0.6).toFixed(2),
        height: h, fill: css(rgb) }, svg);
    }
    const mid = met.scale === 'div' && met.center !== null ? met.center : (lo + hi) / 2;
    [[lo, 'start', 0], [mid, 'middle', width / 2], [hi, 'end', width]].forEach(t => {
      svgText(svg, t[2], y0 + h + 13, metricFormat(met, t[0]), 'scalebar-text', { 'text-anchor': t[1] });
    });
  }

  function renderGridNote() {
    const met = metric();
    const shown = MONTHS.filter(mo => isNum(monthValue(met, mo))).length;
    const filtered = state.filters.size ? MONTHS.filter(matchesFilter).length : null;
    let note = shown + ' of ' + MONTHS.length + ' months carry a value on this metric.';
    if (filtered !== null) {
      note += ' ' + filtered + ' month' + (filtered === 1 ? '' : 's') + ' carry the selected badge'
        + (state.filters.size === 1 ? '' : 's') + '; the rest are dimmed.';
    }
    note += ' Hatched tiles are below ' + nf(M.sparse_coverage, 0)
      + ' % measured. Select a month to open it.';
    document.getElementById('gridnote').textContent = note;
  }

  /* ------------------------------------------------------------------------------------------
     Badge legend, which is also the filter
     ------------------------------------------------------------------------------------------ */

  function renderBadgeLegend() {
    const host = document.getElementById('badgelegend');
    const groups = [];
    DATA.badges.forEach(b => {
      let g = groups.find(x => x.name === b.group);
      if (!g) { g = { name: b.group, items: [] }; groups.push(g); }
      g.items.push(b);
    });
    host.innerHTML = groups.map(g =>
      '<div class="badgegroup"><h3>' + g.name + '</h3>' + g.items.map(b =>
        '<button type="button" class="badgetoggle" data-badge="' + b.key + '" '
        + 'aria-pressed="false">' + chip(b.key, 'lg')
        + '<span class="bt"><span class="bl">' + b.label + '</span> '
        + '<span class="bn">' + b.n + ' month' + (b.n === 1 ? '' : 's') + '</span>'
        + '<div class="bd">' + b.about + '</div></span></button>').join('') + '</div>').join('');

    host.querySelectorAll('.badgetoggle').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.badge;
        if (state.filters.has(key)) state.filters.delete(key); else state.filters.add(key);
        btn.setAttribute('aria-pressed', String(state.filters.has(key)));
        renderGrid();
      });
    });

    document.getElementById('badge-lede').textContent =
      'A badge marks something notable about a month, and states the numbers it rests on. '
      + 'Select one to keep only the months that carry it. A badge is withheld where less than '
      + nf(M.min_badge_coverage, 0) + ' % of the variable it reads is measured, so a tile without '
      + 'a badge means either that nothing was notable or that it could not be judged - the month '
      + 'itself says which.';
  }

  /* ------------------------------------------------------------------------------------------
     Hero
     ------------------------------------------------------------------------------------------ */

  function bestMonth(varKey, field, want) {
    let best = null;
    MONTHS.forEach(mo => {
      const rec = mo[varKey];
      if (!rec || !isNum(rec[field])) return;
      if (!isNum(rec.meas) || rec.meas < M.normal_min_coverage) return;
      if (!best || (want === 'max' ? rec[field] > best[varKey][field]
        : rec[field] < best[varKey][field])) best = mo;
    });
    return best;
  }

  function tile(label, value, unit, sub, accent) {
    return '<div class="tile' + (accent ? ' tile-accent-' + accent : '') + '">'
      + '<span class="tile-label">' + label + '</span>'
      + '<span class="tile-value">' + value + (unit ? '<span class="unit">' + unit + '</span>' : '')
      + '</span><span class="tile-sub">' + sub + '</span></div>';
  }

  function renderHero() {
    document.getElementById('brand-site').textContent = M.site;
    document.getElementById('page-lede').textContent =
      'Every month of the ' + M.site + ' meteo record on one grid, ' + M.first_year + ' to '
      + M.last_year + '. Each tile is coloured by the selected metric, carries badges for what was '
      + 'notable in that month, and can show its own days. Open a month to walk it day by day. '
      + 'The values are the exported products; this page aggregates and compares them and corrects '
      + 'nothing.';

    const chips = [
      '<li><b>' + M.n_months + '</b> months</li>',
      '<li><b>' + M.n_days.toLocaleString() + '</b> days</li>',
      '<li><b>' + DATA.variables.length + '</b> variables</li>',
      '<li><b>' + DATA.badges.length + '</b> badge types</li>',
      '<li>30 min products, aggregated here</li>'
    ];
    document.getElementById('page-chips').innerHTML = chips.join('');

    const warm = bestMonth('TA', 'v', 'max'), cold = bestMonth('TA', 'v', 'min');
    const wet = bestMonth('PREC', 'v', 'max'), dry = bestMonth('PREC', 'v', 'min');
    const badged = MONTHS.filter(mo => mo.b.length).length;
    const anom = bestMonth('TA', 'a', 'max');
    const tiles = [];
    if (warm) {
      tiles.push(tile('Warmest month', nf(warm.TA.v, 1), VARS.TA.units,
        MONTH_NAME[warm.m - 1] + ' ' + warm.y, 'warm'));
    }
    if (cold) {
      tiles.push(tile('Coldest month', nf(cold.TA.v, 1), VARS.TA.units,
        MONTH_NAME[cold.m - 1] + ' ' + cold.y, 'cold'));
    }
    if (anom) {
      tiles.push(tile('Largest warm anomaly', nfs(anom.TA.a, 1), VARS.TA.units,
        MONTH_NAME[anom.m - 1] + ' ' + anom.y + ', against its calendar-month normal', 'warm'));
    }
    if (wet) {
      tiles.push(tile('Wettest month', nf(wet.PREC.v, 0), VARS.PREC.units,
        MONTH_NAME[wet.m - 1] + ' ' + wet.y));
    }
    if (dry) {
      tiles.push(tile('Driest month', nf(dry.PREC.v, 0), VARS.PREC.units,
        MONTH_NAME[dry.m - 1] + ' ' + dry.y));
    }
    tiles.push(tile('Months with a badge', String(badged), '',
      'of ' + MONTHS.length + ', ' + nf(100 * badged / MONTHS.length, 0) + ' % of the record'));
    document.getElementById('tiles').innerHTML = tiles.join('');

    document.getElementById('footer-text').innerHTML =
      M.site + ' — ' + M.site_long + '. Built ' + M.generated + ' from the products in '
      + '<code>10_METEO/30_PRODUCTS</code>. Normals use the months at least '
      + nf(M.normal_min_coverage, 0) + ' % measured, and need at least ' + M.min_normal_years
      + ' such years; daily normals pool a ±' + M.clim_window + ' day window across all years.';
  }

  function renderAbout() {
    const host = document.getElementById('g-about');
    host.innerHTML = '';

    let body = cardEl(host, {
      title: 'How to read the grid', width: 'w-4',
      sub: 'Three levels: the record, a month, a day.'
    });
    body.innerHTML = '<p class="card-sub" style="max-width:none">Each tile is one month. Its '
      + 'colour is the selected metric, and the strip along its bottom is that month\'s days on '
      + 'the same scale, so a heat wave or a wet spell is visible before anything is opened. '
      + 'Badges mark what was notable. Selecting a tile opens the month, where the days become a '
      + 'calendar and the daily course is drawn against the climatological band; selecting a day '
      + 'there opens the day itself.</p>'
      + '<p class="card-sub" style="max-width:none">Keyboard: arrow keys move between tiles, '
      + 'Enter opens one, Escape goes back.</p>';

    body = cardEl(host, { title: 'Threshold days', width: 'w-4',
      sub: 'The definitions are the ones the per-variable dashboards use, read from the same '
        + 'registry rather than restated here.' });
    body.innerHTML = tableHTML(['Threshold', 'Variable'],
      FLAGS.map(f => [cap(f.label), VARS[f.var].short]));

    body = cardEl(host, { title: 'Products behind this page', width: 'w-4',
      sub: 'A value here is exactly what the product notebook exported.' });
    body.innerHTML = tableHTML(['Variable', 'Column', 'Period'],
      DATA.variables.map(v => [v.short, '<code>' + v.column + '</code>',
        v.first_year + '–' + v.last_year]));

    body = cardEl(host, { title: 'What a badge rests on', width: 'w-6',
      sub: 'Coverage rules, stated once and applied everywhere.' });
    body.innerHTML = '<p class="card-sub" style="max-width:none">A badge is a claim about a month, '
      + 'so a month that was not measured cannot make one. Every badge names the variables it '
      + 'reads and is withheld where less than ' + nf(M.min_badge_coverage, 0) + ' % of them is '
      + 'measured; the month view lists what was withheld and why. A calendar-month normal — and '
      + 'every anomaly, standard score and rank taken from it — uses only the years whose month is '
      + 'at least ' + nf(M.normal_min_coverage, 0) + ' % measured, and is not computed at all below '
      + M.min_normal_years + ' such years. A sparse month is therefore ranked against nothing and '
      + 'can never be the driest on record.</p>';

    body = cardEl(host, { title: 'Coverage across the record', width: 'w-6',
      sub: 'The measured share of each variable, by year. Filled and reconstructed records are '
        + 'not counted as measured.' });
    const host2 = document.createElement('div');
    host2.className = 'chart';
    body.appendChild(host2);
    body.insertAdjacentHTML('beforeend', legendHTML(DATA.variables.map((v, i) => ({
      color: 'var(--series-' + (i % 4 + 1) + ')', label: v.short, line: true
    }))));
    mountChart(host2, drawCoverage);
  }

  function drawCoverage(host) {
    const f = frame(host, { aspect: 0.34, margin: { top: 10, right: 14, bottom: 30, left: 42 } });
    const sx = linear(YEARS[0], YEARS[YEARS.length - 1], f.m.left, f.m.left + f.iw);
    const sy = linear(0, 100, f.m.top + f.ih, f.m.top);
    const every = Math.max(1, Math.ceil(YEARS.length / Math.max(3, Math.floor(f.iw / 62))));
    drawAxes(f, sx, sy, {
      yTicks: [0, 25, 50, 75, 100], yDigits: 0, yLabel: 'measured (%)',
      xTicks: YEARS.filter((y, i) => i % every === 0 || i === YEARS.length - 1)
        .map(y => ({ v: y, label: String(y) }))
    });
    DATA.variables.forEach((v, i) => {
      const values = YEARS.map(y => {
        const rows = MONTHS.filter(mo => mo.y === y && isNum(mo[v.key].meas));
        if (!rows.length) return null;
        return rows.reduce((a, mo) => a + mo[v.key].meas, 0) / rows.length;
      });
      el('path', { d: pathFrom(YEARS, values, sx, sy), fill: 'none',
        stroke: 'var(--series-' + (i % 4 + 1) + ')', 'stroke-width': 2,
        'stroke-linejoin': 'round' }, f.svg);
    });
  }

  /* ------------------------------------------------------------------------------------------
     Level 2: one month
     ------------------------------------------------------------------------------------------ */

  function monthTiles(mo) {
    const out = [];
    DATA.variables.forEach(v => {
      const rec = mo[v.key];
      if (!rec || !isNum(rec.v)) return;
      const bits = [];
      if (isNum(rec.a)) {
        bits.push(nfs(rec.a, v.digits) + ' ' + v.units + ' against the normal');
      }
      if (isNum(rec.r) && isNum(rec.n)) {
        bits.push(ord(rec.r) + ' of ' + rec.n + ' such months');
      }
      if (isNum(rec.meas) && rec.meas < 99.5) bits.push(nf(rec.meas, 0) + ' % measured');
      const accent = v.key === 'TA' && isNum(rec.a) ? (rec.a > 0 ? 'warm' : 'cold') : null;
      out.push(tile(v.short + (v.agg === 'sum' ? ', total' : ', mean'), nf(rec.v, v.digits),
        v.units, bits.join(' · ') || 'complete', accent));
    });
    const counts = FLAGS.filter(f => mo.c[f.key]).map(f => mo.c[f.key] + ' ' + f.key);
    out.push(tile('Threshold days', String(FLAGS.reduce((a, f) => a + mo.c[f.key], 0)), '',
      counts.join(', ') || 'none in this month'));
    return out.join('');
  }

  /**
   * The extremes of a month and the statistics that belong to the month rather than to one of its
   * variables. A monthly mean says what the month was like on average, which is exactly what a
   * reader looking for the hot Tuesday does not want.
   */
  function monthHighlights(mo) {
    const rows = [];
    const best = (key, stat, how) => {
      let bd = null, bv = null;
      for (let d = 1; d <= mo.n; d++) {
        const v = dayStat(key, stat, mo.i0 + d - 1);
        if (!isNum(v)) continue;
        if (bv === null || (how === 'max' ? v > bv : v < bv)) { bv = v; bd = d; }
      }
      return bd === null ? null : { d: bd, v: bv };
    };
    const line = (label, hit, key, digits) => {
      if (!hit) return;
      rows.push('<dt>' + label + '</dt><dd>' + nf(hit.v, digits) + ' ' + VARS[key].units
        + ' <span class="muted">on the ' + ord(hit.d) + '</span></dd>');
    };
    if (VARS.TA) {
      line('Warmest day', best('TA', 'max', 'max'), 'TA', 1);
      line('Coldest night', best('TA', 'min', 'min'), 'TA', 1);
      let wd = null, wv = null;
      for (let d = 1; d <= mo.n; d++) {
        const lo = dayStat('TA', 'min', mo.i0 + d - 1), hi = dayStat('TA', 'max', mo.i0 + d - 1);
        if (!isNum(lo) || !isNum(hi)) continue;
        if (wv === null || hi - lo > wv) { wv = hi - lo; wd = d; }
      }
      if (wd) {
        rows.push('<dt>Largest day-night range</dt><dd>' + nf(wv, 1) + ' ' + VARS.TA.units
          + ' <span class="muted">on the ' + ord(wd) + '</span></dd>');
      }
      if (isNum(mo.x.dtr)) {
        rows.push('<dt>Mean day-night range</dt><dd>' + nf(mo.x.dtr, 1) + ' ' + VARS.TA.units
          + '</dd>');
      }
      if (isNum(mo.x.gdd)) {
        rows.push('<dt>Degree days above 5 ' + VARS.TA.units + '</dt><dd>' + nf(mo.x.gdd, 0)
          + ' K d</dd>');
      }
    }
    if (VARS.PREC) line('Wettest day', best('PREC', 'sum', 'max'), 'PREC', 1);
    if (VARS.SW_IN) line('Brightest day', best('SW_IN', 'mean', 'max'), 'SW_IN', 0);

    let html = '<dl class="kv">' + rows.join('') + '</dl>';
    const notes = [];
    if (mo.x.nrec) {
      notes.push(mo.x.nrec + ' day' + (mo.x.nrec === 1 ? '' : 's') + ' in this month set a record '
        + 'for its own calendar date. A day that was largely gap-filled cannot set one.');
    }
    Object.keys(mo.ev || {}).forEach(name => {
      const ev = mo.ev[name];
      const label = { gs_start: 'The growing season began', gs_end: 'The growing season ended',
        last_frost: 'The last frost of spring fell', first_frost: 'The first frost of autumn fell'
      }[name];
      notes.push(label + ' on ' + ev.date + (isNum(ev.delta) && ev.delta !== 0
        ? ', ' + Math.abs(ev.delta) + ' days ' + (ev.delta < 0 ? 'earlier' : 'later')
          + ' than the median date of the record.' : ', the median date of the record.'));
    });
    if (notes.length) html += '<p class="smallnote">' + notes.join(' ') + '</p>';
    return html;
  }

  function monthBadges(mo) {
    if (!mo.b.length) {
      return '<ul class="badgelist none"><li><span class="bt"><span class="bd">Nothing in this '
        + 'month met a badge threshold.</span></span></li></ul>';
    }
    return '<ul class="badgelist">' + mo.b.map(b => {
      const meta = BADGES[b.k];
      return '<li>' + chip(b.k, 'lg') + '<span class="bt">'
        + '<span class="bl">' + meta.label + '</span>'
        + '<div class="bd">' + b.t + '.</div></span></li>';
    }).join('') + '</ul>';
  }

  function suppressedNote(mo) {
    /* Only the badges withheld for coverage are worth reporting: a badge withheld because the
       variable is not in this build says nothing about the month. */
    const rows = mo.sup.filter(s => /measured|no .* data/.test(s.why));
    if (!rows.length) return '';
    const seen = {};
    rows.forEach(s => { seen[s.why] = (seen[s.why] || []).concat(BADGES[s.key].label); });
    return '<p class="smallnote">Withheld for want of measurement: '
      + Object.keys(seen).map(why => seen[why].join(', ') + ' (' + why + ')').join('; ') + '.</p>';
  }

  function drawMonthTemperature(mo) {
    return function (host) {
      const days = [], tmin = [], tmax = [], tmean = [], nlo = [], nhi = [], nmean = [];
      for (let d = 1; d <= mo.n; d++) {
        const i = mo.i0 + d - 1, doy = doy365(mo.y, mo.m, d);
        days.push(d);
        tmin.push(dayStat('TA', 'min', i));
        tmax.push(dayStat('TA', 'max', i));
        tmean.push(dayStat('TA', 'mean', i));
        nlo.push(NORM.TA.mean.p10[doy]);
        nhi.push(NORM.TA.mean.p90[doy]);
        nmean.push(NORM.TA.mean.mean[doy]);
      }
      const f = frame(host, { aspect: 0.36, ariaLabel: 'Daily temperature' });
      const ext = extent([tmin, tmax, nlo, nhi]);
      const sx = linear(0.5, mo.n + 0.5, f.m.left, f.m.left + f.iw);
      const sy = linear(ext[0] - 1, ext[1] + 1, f.m.top + f.ih, f.m.top);
      drawAxes(f, sx, sy, { yDigits: 0, yLabel: VARS.TA.units, xTicks: dayTicks(mo, f.iw) });
      el('path', { d: areaFrom(days, nlo, nhi, sx, sy), fill: f.p.bandOuter }, f.svg);
      el('path', { d: areaFrom(days, tmin, tmax, sx, sy), fill: f.p.bandInner, opacity: 0.85 },
        f.svg);
      el('path', { d: pathFrom(days, nmean, sx, sy), fill: 'none', stroke: f.p.muted,
        'stroke-width': 1.5, 'stroke-dasharray': '4 3' }, f.svg);
      el('path', { d: pathFrom(days, tmean, sx, sy), fill: 'none', stroke: f.p.series[1],
        'stroke-width': 2, 'stroke-linejoin': 'round' }, f.svg);
      hover(f, sx, days, d => {
        const i = d - 1;
        return tipRows(d + ' ' + MONTH_ABBR[mo.m - 1] + ' ' + mo.y, [
          { k: 'minimum', v: nf(tmin[i], 1) + ' ' + VARS.TA.units },
          { k: 'mean', v: nf(tmean[i], 1) + ' ' + VARS.TA.units, color: f.p.series[1] },
          { k: 'maximum', v: nf(tmax[i], 1) + ' ' + VARS.TA.units },
          { k: 'normal', v: nf(nmean[i], 1) + ' ' + VARS.TA.units, color: f.p.muted }
        ]);
      }, d => selectDay(d));
    };
  }

  function drawMonthPrecip(mo) {
    return function (host) {
      const days = [], sums = [], norm = [];
      for (let d = 1; d <= mo.n; d++) {
        const i = mo.i0 + d - 1, doy = doy365(mo.y, mo.m, d);
        days.push(d);
        sums.push(dayStat('PREC', 'sum', i));
        norm.push(NORM.PREC.sum ? NORM.PREC.sum.mean[doy] : null);
      }
      const f = frame(host, { aspect: 0.36, ariaLabel: 'Daily precipitation' });
      const ext = extent([sums, norm]);
      const sx = linear(0.5, mo.n + 0.5, f.m.left, f.m.left + f.iw);
      const sy = linear(0, ext[1] * 1.08 || 1, f.m.top + f.ih, f.m.top);
      drawAxes(f, sx, sy, { yDigits: 0, yLabel: VARS.PREC.units, xTicks: dayTicks(mo, f.iw) });
      const bw = Math.max(2, f.iw / mo.n - 2);
      days.forEach((d, i) => {
        if (!isNum(sums[i]) || sums[i] <= 0) return;
        el('rect', { x: sx(d) - bw / 2, y: sy(sums[i]), width: bw,
          height: Math.max(1, sy(0) - sy(sums[i])), rx: Math.min(3, bw / 2),
          fill: f.p.series[0] }, f.svg);
      });
      el('path', { d: pathFrom(days, norm, sx, sy), fill: 'none', stroke: f.p.muted,
        'stroke-width': 1.5, 'stroke-dasharray': '4 3' }, f.svg);
      hover(f, sx, days, d => {
        const i = d - 1;
        return tipRows(d + ' ' + MONTH_ABBR[mo.m - 1] + ' ' + mo.y, [
          { k: 'total', v: nf(sums[i], 1) + ' ' + VARS.PREC.units, color: f.p.series[0] },
          { k: 'normal for the date', v: nf(norm[i], 1) + ' ' + VARS.PREC.units, color: f.p.muted }
        ]);
      }, d => selectDay(d));
    };
  }

  function drawMonthCumulative(mo) {
    return function (host) {
      const days = [], run = [], runNorm = [];
      let a = 0, b = 0, seen = false;
      for (let d = 1; d <= mo.n; d++) {
        const i = mo.i0 + d - 1, doy = doy365(mo.y, mo.m, d);
        const v = dayStat('PREC', 'sum', i);
        const n = NORM.PREC.sum ? NORM.PREC.sum.mean[doy] : null;
        days.push(d);
        if (isNum(v)) { a += v; seen = true; }
        run.push(seen ? a : null);
        if (isNum(n)) b += n;
        runNorm.push(b);
      }
      const f = frame(host, { aspect: 0.36, ariaLabel: 'Cumulative precipitation' });
      const sx = linear(1, mo.n, f.m.left, f.m.left + f.iw);
      const sy = linear(0, extent([run, runNorm])[1] * 1.08 || 1, f.m.top + f.ih, f.m.top);
      drawAxes(f, sx, sy, { yDigits: 0, yLabel: VARS.PREC.units, xTicks: dayTicks(mo, f.iw) });
      el('path', { d: pathFrom(days, runNorm, sx, sy), fill: 'none', stroke: f.p.muted,
        'stroke-width': 1.5, 'stroke-dasharray': '4 3' }, f.svg);
      el('path', { d: pathFrom(days, run, sx, sy), fill: 'none', stroke: f.p.series[0],
        'stroke-width': 2.2, 'stroke-linejoin': 'round' }, f.svg);
      hover(f, sx, days, d => tipRows('to ' + d + ' ' + MONTH_ABBR[mo.m - 1], [
        { k: 'this month', v: nf(run[d - 1], 1) + ' ' + VARS.PREC.units, color: f.p.series[0] },
        { k: 'normal by this date', v: nf(runNorm[d - 1], 1) + ' ' + VARS.PREC.units,
          color: f.p.muted }
      ]), d => selectDay(d));
    };
  }

  function drawAcrossYears(mo) {
    const met = metric();
    return function (host) {
      const rows = MONTHS.filter(x => x.m === mo.m);
      const years = rows.map(x => x.y);
      const values = rows.map(x => monthValue(met, x));
      const f = frame(host, { aspect: 0.34, ariaLabel: met.label + ' in every ' + MONTH_NAME[mo.m - 1] });
      const ext = extent([values]);
      const lo = Math.min(0, ext[0]), hi = ext[1];
      const sx = linear(years[0] - 0.5, years[years.length - 1] + 0.5, f.m.left, f.m.left + f.iw);
      const sy = linear(lo, hi * 1.06 || 1, f.m.top + f.ih, f.m.top);
      const every = Math.max(1, Math.ceil(years.length / Math.max(3, Math.floor(f.iw / 54))));
      drawAxes(f, sx, sy, { yDigits: met.digits > 1 ? 1 : 0, yLabel: met.units,
        xTicks: years.filter((y, i) => i % every === 0 || i === years.length - 1)
          .map(y => ({ v: y, label: String(y) })) });
      const bw = Math.max(3, f.iw / years.length - 4);
      years.forEach((y, i) => {
        if (!isNum(values[i])) return;
        const top = Math.min(sy(values[i]), sy(0)), bottom = Math.max(sy(values[i]), sy(0));
        el('rect', { x: sx(y) - bw / 2, y: top, width: bw, height: Math.max(1, bottom - top),
          rx: Math.min(3, bw / 2), fill: y === mo.y ? f.p.series[1] : f.p.series[0],
          opacity: y === mo.y ? 1 : 0.55 }, f.svg);
      });
      const nm = CLIM[met.var] && CLIM[met.var][String(mo.m)];
      if (nm && met.field === 'value') {
        el('line', { x1: f.m.left, x2: f.m.left + f.iw, y1: sy(nm.mean), y2: sy(nm.mean),
          stroke: f.p.muted, 'stroke-width': 1.5, 'stroke-dasharray': '4 3' }, f.svg);
      }
      hover(f, sx, years, y => {
        const i = years.indexOf(y);
        return tipRows(MONTH_NAME[mo.m - 1] + ' ' + y, [
          { k: met.short, v: nf(values[i], met.digits) + ' ' + met.units,
            color: y === mo.y ? f.p.series[1] : f.p.series[0] }
        ]);
      }, y => { if (y !== mo.y) location.hash = y + '-' + String(mo.m).padStart(2, '0'); });
    };
  }

  function dayTicks(mo, width) {
    const every = width < 420 ? 5 : width < 700 ? 2 : 1;
    const out = [];
    for (let d = 1; d <= mo.n; d++) {
      if (d === 1 || d % every === 0) out.push({ v: d, label: String(d) });
    }
    return out;
  }

  /** A crosshair over a discrete x axis, with a click that hands the value back. */
  function hover(f, sx, values, tipFor, onClick) {
    const line = el('line', { class: 'crosshair', y1: f.m.top, y2: f.m.top + f.ih,
      opacity: 0 }, f.svg);
    const hit = el('rect', { class: 'hit', x: f.m.left, y: f.m.top, width: f.iw, height: f.ih },
      f.svg);
    const nearest = ev => {
      const box = f.svg.getBoundingClientRect();
      const px = (ev.clientX - box.left) * (f.width / box.width);
      let best = values[0], bestD = Infinity;
      values.forEach(v => {
        const d = Math.abs(sx(v) - px);
        if (d < bestD) { bestD = d; best = v; }
      });
      return best;
    };
    hit.addEventListener('mousemove', ev => {
      const v = nearest(ev);
      line.setAttribute('x1', sx(v));
      line.setAttribute('x2', sx(v));
      line.setAttribute('opacity', 1);
      tip.show(tipFor(v), ev.clientX, ev.clientY);
    });
    hit.addEventListener('mouseleave', () => { line.setAttribute('opacity', 0); tip.hide(); });
    if (onClick) hit.addEventListener('click', ev => onClick(nearest(ev)));
  }

  function dayCalendar(mo) {
    const met = metric();
    const first = (new Date(Date.UTC(mo.y, mo.m - 1, 1)).getUTCDay() + 6) % 7;
    const parts = WEEKDAY.map(w => '<div class="dayhead">' + w + '</div>');
    for (let i = 0; i < first; i++) parts.push('<div class="daycell blank"></div>');

    let maxRain = 0;
    for (let d = 1; d <= mo.n; d++) {
      const v = dayStat('PREC', 'sum', mo.i0 + d - 1);
      if (isNum(v) && v > maxRain) maxRain = v;
    }

    for (let d = 1; d <= mo.n; d++) {
      const i = mo.i0 + d - 1;
      const value = dayValue(met, i, mo.y, mo.m, d);
      const rgb = dayColor(met, value);
      const cls = ['daycell'];
      let style = '';
      if (rgb) { cls.push(inkClass(rgb)); style = ' style="background:' + css(rgb) + '"'; }
      const meas = DAYS.meas[met.var] ? DAYS.meas[met.var][i] : null;
      if (isNum(meas) && meas < M.sparse_coverage) cls.push('sparse');

      const flags = DAY_MARKS.filter(m => flagSet(DAYS.flags[i], m[0]))
        .slice(0, 3).map(m => markChip(m[1], 'sm')).join('');
      const rain = dayStat('PREC', 'sum', i);
      const sub = met.var === 'TA'
        ? nf(dayStat('TA', 'min', i), 0) + ' / ' + nf(dayStat('TA', 'max', i), 0)
        : (isNum(rain) && rain > 0 ? nf(rain, 1) + ' ' + VARS.PREC.units : '');

      parts.push('<button type="button" class="' + cls.join(' ') + '"' + style
        + ' data-day="' + d + '" aria-label="' + d + ' ' + MONTH_NAME[mo.m - 1] + ' ' + mo.y + '">'
        + '<span class="dnum">' + d + '</span>'
        + '<span class="dval">' + (met.day.kind === 'flag' ? nf(value, 0) : metricFormat(met, value))
        + '</span>'
        + (sub ? '<span class="dsub">' + sub + '</span>' : '')
        + '<span class="dflags">' + flags + '</span>'
        + (isNum(rain) && maxRain > 0 && rain > 0
          ? '<span class="drain" style="width:' + (100 * rain / maxRain).toFixed(0) + '%"></span>'
          : '')
        + '</button>');
    }
    return '<div class="daygrid">' + parts.join('') + '</div>';
  }

  function dayTable(mo) {
    const columns = ['Day'];
    DATA.variables.forEach(v => v.ship.forEach(s => {
      columns.push(v.short + ' ' + (s === 'sum' ? 'total' : s));
    }));
    const rows = [];
    for (let d = 1; d <= mo.n; d++) {
      const i = mo.i0 + d - 1;
      const row = [d + ' ' + MONTH_ABBR[mo.m - 1]];
      DATA.variables.forEach(v => v.ship.forEach(s => {
        row.push(nf(dayStat(v.key, s, i), v.digits));
      }));
      rows.push(row);
    }
    return tableHTML(columns, rows);
  }

  function renderMonth() {
    const mo = monthAt(state.y, state.m);
    const host = document.getElementById('month-body');
    compactCharts();
    document.getElementById('month-title').textContent = MONTH_NAME[state.m - 1] + ' ' + state.y;

    const idx = monthIndex[state.y + '-' + state.m];
    document.getElementById('month-prev').disabled = idx <= 0;
    document.getElementById('month-next').disabled = idx >= MONTHS.length - 1;
    document.getElementById('year-prev').disabled = !monthAt(state.y - 1, state.m);
    document.getElementById('year-next').disabled = !monthAt(state.y + 1, state.m);

    host.innerHTML = '<div class="tiles" id="month-tiles"></div>'
      + '<h2 class="section">What was notable</h2><div id="month-badges"></div>'
      + '<div class="grid" id="month-highlights"></div>'
      + '<h2 class="section">Day by day</h2><div class="grid" id="month-charts"></div>'
      + '<h2 class="section">The days</h2><div class="grid" id="month-days"></div>'
      + '<div id="day-panel"></div>'
      + '<h2 class="section">Every day of this month</h2><div class="grid" id="month-table"></div>';

    document.getElementById('month-tiles').innerHTML = monthTiles(mo);
    document.getElementById('month-badges').innerHTML = monthBadges(mo) + suppressedNote(mo);

    const hl = document.getElementById('month-highlights');
    hl.innerHTML = '';
    cardEl(hl, {
      title: 'The month in single days', width: 'w-4',
      sub: 'The days a monthly mean does not show.'
    }).innerHTML = monthHighlights(mo);

    const charts = document.getElementById('month-charts');
    if (VARS.TA) {
      chartCard(charts, {
        title: 'Daily temperature against the normal', width: 'w-6',
        sub: 'The daily minimum-to-maximum range and the daily mean, over the ±' + M.clim_window
          + ' day climatological band for the same date.',
        legend: [
          { color: 'var(--band-outer)', label: 'normal 10th–90th percentile' },
          { color: 'var(--band-inner)', label: 'daily minimum to maximum' },
          { color: 'var(--series-2)', label: 'daily mean', line: true },
          { color: 'var(--text-muted)', label: 'normal daily mean', line: true }
        ],
        draw: drawMonthTemperature(mo)
      });
    }
    if (VARS.PREC) {
      chartCard(charts, {
        title: 'Daily precipitation', width: 'w-6',
        sub: 'Daily totals, with the normal for each date.',
        legend: [
          { color: 'var(--series-1)', label: 'daily total' },
          { color: 'var(--text-muted)', label: 'normal for the date', line: true }
        ],
        draw: drawMonthPrecip(mo)
      });
      chartCard(charts, {
        title: 'Precipitation accumulated through the month', width: 'w-6',
        sub: 'The running total against the running total of the daily normals.',
        legend: [
          { color: 'var(--series-1)', label: 'this month', line: true },
          { color: 'var(--text-muted)', label: 'normal', line: true }
        ],
        draw: drawMonthCumulative(mo)
      });
    }
    chartCard(charts, {
      title: 'Every ' + MONTH_NAME[state.m - 1] + ' in the record', width: 'w-6',
      sub: metric().label + '. This month is highlighted; selecting another opens it.',
      legend: [
        { color: 'var(--series-2)', label: MONTH_NAME[state.m - 1] + ' ' + state.y },
        { color: 'var(--series-1)', label: 'the other years' },
        { color: 'var(--text-muted)', label: 'normal', line: true }
      ],
      draw: drawAcrossYears(mo)
    });

    const daysHost = document.getElementById('month-days');
    const body = cardEl(daysHost, {
      title: 'The days of ' + MONTH_NAME[state.m - 1] + ' ' + state.y, width: 'w-8',
      sub: 'Coloured by ' + metric().label.toLowerCase() + '. Marks show the thresholds a day set '
        + 'and the bar along the bottom is its precipitation. Select a day to open it.'
    });
    body.innerHTML = dayCalendar(mo);
    body.querySelectorAll('.daycell[data-day]').forEach(node => {
      node.addEventListener('click', () => selectDay(+node.dataset.day));
    });

    document.getElementById('month-table').innerHTML = '';
    const tbody = cardEl(document.getElementById('month-table'), {
      title: 'Daily values', width: 'w-8',
      sub: 'The same numbers the charts and the calendar above are drawn from.'
    });
    tbody.innerHTML = dayTable(mo);

    if (state.d) renderDay();
  }

  /* ------------------------------------------------------------------------------------------
     Level 3: one day
     ------------------------------------------------------------------------------------------ */

  function selectDay(d) {
    if (d === null) return;
    location.hash = state.y + '-' + String(state.m).padStart(2, '0') + '-'
      + String(d).padStart(2, '0');
  }

  function drawDiurnal(varKey, values, kind) {
    return function (host) {
      const hours = values.map((v, i) => i + 0.5);
      const f = frame(host, { aspect: 0.62, margin: { top: 10, right: 12, bottom: 28, left: 40 },
        ariaLabel: 'Diurnal course of ' + VARS[varKey].short });
      const ext = extent([values]);
      // A quantity drawn as bars or as a filled area is read against zero; a line is not.
      const lo = (kind === 'bars' || kind === 'area') ? 0 : ext[0] - (ext[1] - ext[0]) * 0.08;
      const sy = linear(lo, ext[1] + (ext[1] - ext[0]) * 0.08 || 1, f.m.top + f.ih, f.m.top);
      const sx = linear(0, 24, f.m.left, f.m.left + f.iw);
      drawAxes(f, sx, sy, { yDigits: VARS[varKey].digits > 1 ? 1 : 0, yTickCount: 3,
        xTicks: [0, 6, 12, 18, 24].map(h => ({ v: h, label: h + 'h' })) });
      if (kind === 'bars') {
        const bw = Math.max(2, f.iw / 24 - 2);
        values.forEach((v, i) => {
          if (!isNum(v) || v <= 0) return;
          el('rect', { x: sx(i + 0.5) - bw / 2, y: sy(v), width: bw,
            height: Math.max(1, sy(0) - sy(v)), rx: Math.min(2, bw / 2),
            fill: f.p.series[0] }, f.svg);
        });
      } else if (kind === 'area') {
        el('path', { d: areaFrom(hours, values.map(() => 0), values, sx, sy),
          fill: f.p.series[3], opacity: 0.55 }, f.svg);
        el('path', { d: pathFrom(hours, values, sx, sy), fill: 'none', stroke: f.p.series[3],
          'stroke-width': 2 }, f.svg);
      } else {
        el('path', { d: pathFrom(hours, values, sx, sy), fill: 'none', stroke: f.p.series[1],
          'stroke-width': 2.2, 'stroke-linejoin': 'round' }, f.svg);
      }
      hover(f, sx, hours, h => {
        const k = Math.floor(h);
        return tipRows(String(k).padStart(2, '0') + ':00–' + String(k + 1).padStart(2, '0') + ':00',
          [{ k: VARS[varKey].short,
            v: nf(values[k], VARS[varKey].digits) + ' ' + VARS[varKey].units }]);
      });
    };
  }

  function hourlyFor(varKey, i) {
    if (!HOURLY || !HOURLY.vars[varKey]) return null;
    const h = HOURLY.vars[varKey];
    const start = i * 24;
    const out = [];
    for (let k = 0; k < 24; k++) {
      const raw = h.values[start + k];
      out.push(raw === null || raw === undefined ? null : raw / h.scale);
    }
    return out.some(isNum) ? out : null;
  }

  function renderDay() {
    const mo = monthAt(state.y, state.m);
    const d = state.d;
    const i = mo.i0 + d - 1;
    const host = document.getElementById('day-panel');
    const weekday = WEEKDAY_LONG[(new Date(Date.UTC(state.y, state.m - 1, d)).getUTCDay() + 6) % 7];

    host.innerHTML = '<h2 class="section">The day</h2><div class="grid daypanel" id="day-grid"></div>';
    const grid = document.getElementById('day-grid');

    const body = cardEl(grid, {
      title: weekday + ', ' + d + ' ' + MONTH_NAME[state.m - 1] + ' ' + state.y, width: 'w-4',
      sub: 'Day ' + doy365(state.y, state.m, d) + ' of the year.'
    });
    let kv = '<dl class="kv">';
    DATA.variables.forEach(v => {
      v.ship.forEach(s => {
        const value = dayStat(v.key, s, i);
        if (!isNum(value)) return;
        const label = v.short + ' ' + (s === 'sum' ? 'total' : s);
        let line = nf(value, v.digits) + ' ' + v.units;
        const n = dayNormal(v.key, s, state.y, state.m, d);
        if (isNum(n)) line += ' (' + nfs(value - n, v.digits) + ')';
        kv += '<dt>' + label + '</dt><dd>' + line + '</dd>';
      });
      const meas = DAYS.meas[v.key] ? DAYS.meas[v.key][i] : null;
      if (isNum(meas) && meas < 99.5) {
        kv += '<dt>' + v.short + ' measured</dt><dd>' + nf(meas, 0) + ' %</dd>';
      }
    });
    kv += '</dl>';
    /* A record is stated first and in words, because it is the one thing about a day that a
       reader cannot work out from the numbers above it. */
    const records = [
      ['recwarm', 'the warmest'], ['reccold', 'the coldest'], ['recwet', 'the wettest']
    ].filter(x => flagSet(DAYS.flags[i], x[0]));
    const dateName = d + ' ' + MONTH_NAME[state.m - 1];
    const set = FLAGS.filter(f => flagSet(DAYS.flags[i], f.key)
      && !f.key.startsWith('rec'));
    body.innerHTML = kv
      + (records.length
        ? '<p class="smallnote"><b>This is ' + records.map(x => x[1]).join(' and ')
          + ' ' + dateName + ' in the record.</b> Days that were largely gap-filled are left out '
          + 'of that comparison.</p>'
        : '')
      + '<p class="smallnote">' + (set.length
        ? 'This day also counts as: ' + set.map(f => f.label).join(', ') + '.'
        : 'This day met none of the thresholds on this page.')
      + ' Departures in brackets are against the ±' + M.clim_window
      + ' day normal for the same date.</p>';

    if (!HOURLY) {
      const nb = cardEl(grid, { title: 'Diurnal course', width: 'w-8' });
      nb.innerHTML = '<p class="card-sub" style="max-width:none">This page was built without the '
        + 'hourly arrays, so the day is available as statistics only. Rebuild without '
        + '<code>--no-hourly</code> for the diurnal charts.</p>';
      return;
    }

    const facets = cardEl(grid, {
      title: 'Through the day', width: 'w-8',
      sub: 'Hourly means, and hourly totals for precipitation, from the 30-minute products.'
    });
    const wrap = document.createElement('div');
    wrap.className = 'dayfacets';
    facets.appendChild(wrap);
    let drawn = 0;
    Object.keys(HOURLY.vars).forEach(key => {
      const values = hourlyFor(key, i);
      if (!values) return;
      drawn++;
      const box = document.createElement('div');
      box.innerHTML = '<p class="facet-title">' + VARS[key].short + ' (' + VARS[key].units
        + ')</p><div class="chart"></div>';
      wrap.appendChild(box);
      const kind = key === 'PREC' ? 'bars' : (key === 'SW_IN' ? 'area' : 'line');
      mountChart(box.querySelector('.chart'), drawDiurnal(key, values, kind));
    });
    if (!drawn) {
      wrap.innerHTML = '<p class="card-sub">No hourly record survives for this day.</p>';
    }
  }

  /* ------------------------------------------------------------------------------------------
     Routing
     ------------------------------------------------------------------------------------------ */

  function showView(which) {
    document.getElementById('view-grid').hidden = which !== 'grid';
    document.getElementById('view-month').hidden = which !== 'month';
    const crumbs = document.getElementById('crumbs');
    if (which === 'grid') {
      crumbs.innerHTML = '<b>' + M.first_year + '–' + M.last_year + '</b>';
    } else {
      crumbs.innerHTML = '<span>' + M.first_year + '–' + M.last_year + '</span>'
        + '<span class="sep">›</span><b>' + MONTH_NAME[state.m - 1] + ' ' + state.y + '</b>'
        + (state.d ? '<span class="sep">›</span><b>' + state.d + '</b>' : '');
    }
  }

  function route() {
    const hash = location.hash.replace('#', '');
    const m = /^(\d{4})-(\d{2})(?:-(\d{2}))?$/.exec(hash);
    if (!m || !monthAt(+m[1], +m[2])) {
      state.y = state.m = state.d = null;
      showView('grid');
      tip.hide();
      window.scrollTo({ top: 0 });
      return;
    }
    const sameMonth = state.y === +m[1] && state.m === +m[2];
    state.y = +m[1];
    state.m = +m[2];
    state.d = m[3] ? +m[3] : null;
    showView('month');
    tip.hide();
    if (sameMonth && state.d) {
      renderDay();
      const panel = document.getElementById('day-panel');
      if (panel) panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      renderMonth();
      window.scrollTo({ top: 0 });
    }
  }

  function setupNav() {
    document.getElementById('month-back').addEventListener('click', () => {
      location.hash = 'grid';
    });
    const step = delta => {
      const idx = monthIndex[state.y + '-' + state.m] + delta;
      const target = MONTHS[idx];
      if (target) location.hash = target.y + '-' + String(target.m).padStart(2, '0');
    };
    document.getElementById('month-prev').addEventListener('click', () => step(-1));
    document.getElementById('month-next').addEventListener('click', () => step(1));
    document.getElementById('year-prev').addEventListener('click', () => step(-12));
    document.getElementById('year-next').addEventListener('click', () => step(12));

    /* Arrow keys walk the grid, Enter opens a month, Escape goes back. A tile is a button, so the
       browser already gives it focus; the arrows only have to move that focus. */
    document.addEventListener('keydown', ev => {
      if (ev.key === 'Escape' && state.y) { location.hash = 'grid'; return; }
      if (state.y && !document.getElementById('view-month').hidden) {
        if (ev.key === 'ArrowLeft') { step(-1); }
        if (ev.key === 'ArrowRight') { step(1); }
        return;
      }
      const active = document.activeElement;
      if (!active || !active.classList.contains('cell')) return;
      const y = +active.dataset.y, m = +active.dataset.m;
      let ty = y, tm = m;
      if (ev.key === 'ArrowLeft') tm -= 1;
      else if (ev.key === 'ArrowRight') tm += 1;
      else if (ev.key === 'ArrowUp') ty -= 1;
      else if (ev.key === 'ArrowDown') ty += 1;
      else return;
      if (tm === 0) { tm = 12; ty -= 1; }
      if (tm === 13) { tm = 1; ty += 1; }
      const next = document.querySelector('.cell[data-y="' + ty + '"][data-m="' + tm + '"]');
      if (next) { next.focus(); ev.preventDefault(); }
    });
  }

  function setupTheme() {
    const root = document.documentElement;
    const btn = document.getElementById('theme-toggle');
    const label = btn.querySelector('.theme-label');
    const stored = (() => {
      try { return localStorage.getItem('meteo-dashboard-theme'); } catch (e) { return null; }
    })();
    if (stored === 'light' || stored === 'dark') root.setAttribute('data-theme', stored);
    const isDark = () => root.getAttribute('data-theme') === 'dark'
      || (root.getAttribute('data-theme') === 'auto'
        && window.matchMedia('(prefers-color-scheme: dark)').matches);
    function sync() {
      label.textContent = isDark() ? 'Light mode' : 'Dark mode';
      btn.setAttribute('aria-label', 'Switch to ' + (isDark() ? 'light' : 'dark') + ' mode');
    }
    /* A theme change repaints every mark, including the charts of whichever view is not on screen
       and the ones the view being rebuilt does not own - the coverage chart sits on the grid view
       and is not touched by renderGrid. */
    function repaint() {
      sync();
      if (document.getElementById('view-grid').hidden) { renderMonth(); } else { renderGrid(); }
      redrawAll();
    }
    btn.addEventListener('click', () => {
      const next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('meteo-dashboard-theme', next); } catch (e) { /* private mode */ }
      repaint();
    });
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (root.getAttribute('data-theme') === 'auto') repaint();
    });
    sync();
  }

  /* ------------------------------------------------------------------------------------------
     Go
     ------------------------------------------------------------------------------------------ */

  renderHero();
  buildControls();
  renderBadgeLegend();
  renderAbout();
  renderGrid();
  setupNav();
  setupTheme();
  route();
  window.addEventListener('hashchange', route);

  let resizeTimer = null;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      redrawAll();
      renderScaleBar();
    }, 140);
  });
})();
