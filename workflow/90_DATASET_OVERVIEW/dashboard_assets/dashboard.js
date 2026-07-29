/* ==============================================================================================
   CH-LAE meteo dashboard - rendering engine
   ----------------------------------------------------------------------------------------------
   A small SVG chart engine and the card definitions that use it. No external libraries: the page
   has to open from disk, so everything it needs travels inside it.

   Three conventions hold throughout.
   - Colours come from CSS custom properties, never from literals here, so the light and the dark
     token sets are the only place a colour is decided and the toggle recolours every chart.
   - Every chart is re-rendered from its spec on resize and on a theme change, rather than being
     scaled. Text therefore stays at one size at every viewport width.
   - Every chart card carries a table view of the same numbers. A tooltip enhances a chart, it
     never gates a value.
   ============================================================================================== */

(function () {
  'use strict';

  const DATA = JSON.parse(document.getElementById('payload').textContent);
  const M = DATA.meta;
  const U = M.units;

  /* ------------------------------------------------------------------------------------------
     Formatting
     ------------------------------------------------------------------------------------------ */

  const nf = (v, d = 1) => (v === null || v === undefined || Number.isNaN(v))
    ? '–' : v.toFixed(d);
  const nfs = (v, d = 1) => (v === null || v === undefined || Number.isNaN(v))
    ? '–' : (v > 0 ? '+' : '') + v.toFixed(d);
  const val = (v, d = 1) => nf(v, d) + ' ' + U;
  const vals = (v, d = 1) => nfs(v, d) + ' ' + U;

  function token(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  /**
   * The same colour as a live CSS reference rather than a resolved value.
   *
   * Charts are redrawn on a theme change, so a colour resolved inside a render closure is always
   * current. A legend is built once with the card and is not, so a resolved colour there freezes
   * whichever theme happened to be active at load — which is how the neutral band swatch came to
   * read as black in light mode. Legends therefore hand the variable to the browser instead.
   */
  const cv = name => 'var(' + name + ')';

  /* Palette, re-read on every render so a theme change repaints without a reload. */
  function palette() {
    return {
      series: [token('--series-1'), token('--series-2'), token('--series-3'), token('--series-4')],
      cold: token('--pole-cold'),
      warm: token('--pole-warm'),
      mid: token('--neutral-mid'),
      seq: [1, 2, 3, 4, 5, 6, 7].map(i => token('--seq-' + i)),
      coldRamp: [token('--cold-1'), token('--cold-2')],
      warmRamp: [token('--warm-1'), token('--warm-2'), token('--warm-3')],
      bandOuter: token('--band-outer'),
      bandInner: token('--band-inner'),
      ink: token('--text-primary'),
      ink2: token('--text-secondary'),
      muted: token('--text-muted'),
      axis: token('--axis'),
      grid: token('--grid'),
      surface: token('--surface')
    };
  }

  /* ------------------------------------------------------------------------------------------
     Colour interpolation
     ------------------------------------------------------------------------------------------ */

  function hex2rgb(h) {
    h = h.replace('#', '');
    if (h.length === 3) h = h.split('').map(c => c + c).join('');
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }
  const rgb2css = c => 'rgb(' + c.map(v => Math.round(v)).join(',') + ')';
  const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);

  /** Interpolate across an array of hex stops. `t` is clamped to [0, 1]. */
  function ramp(stops, t) {
    if (t === null || Number.isNaN(t)) return null;
    t = Math.max(0, Math.min(1, t));
    const rgb = stops.map(hex2rgb);
    const pos = t * (rgb.length - 1);
    const i = Math.min(rgb.length - 2, Math.floor(pos));
    return rgb2css(mix(rgb[i], rgb[i + 1], pos - i));
  }

  /** Diverging scale: two poles that read as opposite with a neutral midpoint at zero. */
  function diverging(v, absmax, p) {
    if (v === null || v === undefined || Number.isNaN(v)) return 'transparent';
    const t = Math.max(-1, Math.min(1, v / absmax));
    return t >= 0 ? ramp([p.mid, p.warm], t) : ramp([p.mid, p.cold], -t);
  }

  /* ------------------------------------------------------------------------------------------
     Scales and ticks
     ------------------------------------------------------------------------------------------ */

  function linear(d0, d1, r0, r1) {
    const span = (d1 - d0) || 1;
    const f = v => r0 + (v - d0) / span * (r1 - r0);
    f.invert = px => d0 + (px - r0) / ((r1 - r0) || 1) * span;
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
      if (v === null || v === undefined || Number.isNaN(v)) return;
      if (v < lo) lo = v;
      if (v > hi) hi = v;
    }));
    if (!isFinite(lo)) { lo = 0; hi = 1; }
    return [lo, hi];
  }

  function pad(ext, frac) {
    const d = (ext[1] - ext[0]) || 1;
    return [ext[0] - d * frac, ext[1] + d * frac];
  }

  /* ------------------------------------------------------------------------------------------
     SVG helpers
     ------------------------------------------------------------------------------------------ */

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

  function text(parent, x, y, str, cls, extra) {
    const t = el('text', Object.assign({ x: x, y: y, class: cls || 'ax-text' }, extra || {}), parent);
    t.textContent = str;
    return t;
  }

  /* A path from (x, y) pairs, breaking at nulls so a gap stays a gap. */
  function pathFrom(xs, ys, sx, sy) {
    let d = '', pen = false;
    for (let i = 0; i < xs.length; i++) {
      const v = ys[i];
      if (v === null || v === undefined || Number.isNaN(v)) { pen = false; continue; }
      const cmd = pen ? 'L' : 'M';
      d += cmd + sx(xs[i]).toFixed(2) + ' ' + sy(v).toFixed(2);
      pen = true;
    }
    return d;
  }

  function areaFrom(xs, lo, hi, sx, sy) {
    const up = [], down = [];
    for (let i = 0; i < xs.length; i++) {
      if (lo[i] === null || hi[i] === null) continue;
      up.push(sx(xs[i]).toFixed(2) + ' ' + sy(hi[i]).toFixed(2));
      down.unshift(sx(xs[i]).toFixed(2) + ' ' + sy(lo[i]).toFixed(2));
    }
    if (!up.length) return '';
    return 'M' + up.join('L') + 'L' + down.join('L') + 'Z';
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
      html += '<div class="tt-row">'
        + (r.color ? '<span class="sw" style="background:' + r.color + '"></span>' : '')
        + '<span class="k">' + r.k + '</span><span class="v">' + r.v + '</span></div>';
    });
    return html;
  }

  /* ------------------------------------------------------------------------------------------
     Chart frame: margins, axes, gridlines
     ------------------------------------------------------------------------------------------ */

  function frame(host, spec) {
    const p = palette();
    const width = Math.max(260, host.clientWidth || 640);
    const height = spec.height || Math.round(Math.max(200, Math.min(420, width * (spec.aspect || 0.5))));
    const m = Object.assign({ top: 12, right: 14, bottom: 34, left: 46 }, spec.margin || {});

    const svg = el('svg', {
      viewBox: '0 0 ' + width + ' ' + height,
      width: width, height: height,
      role: 'img', 'aria-label': spec.ariaLabel || ''
    });
    host.innerHTML = '';
    host.appendChild(svg);

    return {
      svg: svg, p: p, width: width, height: height, m: m,
      iw: width - m.left - m.right, ih: height - m.top - m.bottom
    };
  }

  function drawAxes(f, sx, sy, spec) {
    const { svg, p, m, iw, ih } = f;
    const g = el('g', {}, svg);

    const yTicks = spec.yTicks || niceTicks(sy.domain[0], sy.domain[1], spec.yTickCount || 5);
    yTicks.forEach(v => {
      const y = sy(v);
      if (y < m.top - 1 || y > m.top + ih + 1) return;
      el('line', { x1: m.left, x2: m.left + iw, y1: y, y2: y, class: 'gridline' }, g);
      text(g, m.left - 8, y + 4, spec.yFormat ? spec.yFormat(v) : nf(v, spec.yDigits === undefined ? 0 : spec.yDigits),
        'ax-text', { 'text-anchor': 'end' });
    });

    el('line', { x1: m.left, x2: m.left + iw, y1: m.top + ih, y2: m.top + ih, class: 'ax-line' }, g);

    (spec.xTicks || []).forEach(t => {
      const x = sx(t.v);
      if (x < m.left - 1 || x > m.left + iw + 1) return;
      el('line', { x1: x, x2: x, y1: m.top + ih, y2: m.top + ih + 4, class: 'ax-line' }, g);
      text(g, x, m.top + ih + 17, t.label, 'ax-text', { 'text-anchor': 'middle' });
    });

    if (spec.yLabel) {
      const t = text(g, 0, 0, spec.yLabel, 'ax-title', { 'text-anchor': 'middle' });
      t.setAttribute('transform', 'translate(' + (m.left - 34) + ',' + (m.top + ih / 2) + ') rotate(-90)');
    }
    if (spec.xLabel) {
      text(g, m.left + iw / 2, f.height - 2, spec.xLabel, 'ax-title', { 'text-anchor': 'middle' });
    }
    return g;
  }

  /** Year ticks that thin out on a narrow card instead of overlapping. */
  function yearTicks(years, width) {
    const every = Math.max(1, Math.ceil(years.length / Math.max(3, Math.floor(width / 62))));
    return years.filter((y, i) => i % every === 0 || i === years.length - 1)
      .map(y => ({ v: y, label: String(y) }));
  }

  /* ------------------------------------------------------------------------------------------
     Renderer: line and band chart
     ------------------------------------------------------------------------------------------ */

  function lineChart(host, spec) {
    const f = frame(host, spec);
    const { svg, p, m, iw, ih } = f;

    const xs = spec.x;
    const all = (spec.bands || []).flatMap(b => [b.lo, b.hi])
      .concat((spec.series || []).map(s => s.values));
    let yd = pad(extent(all), spec.yPad === undefined ? 0.06 : spec.yPad);
    if (spec.yZero) yd = [Math.min(0, yd[0]), yd[1]];
    if (spec.yDomain) yd = spec.yDomain;

    const sx = linear(spec.xDomain ? spec.xDomain[0] : xs[0],
      spec.xDomain ? spec.xDomain[1] : xs[xs.length - 1], m.left, m.left + iw);
    const sy = linear(yd[0], yd[1], m.top + ih, m.top);

    drawAxes(f, sx, sy, spec);

    (spec.bands || []).forEach(b => {
      el('path', { d: areaFrom(xs, b.lo, b.hi, sx, sy), fill: b.color, stroke: 'none' }, svg);
    });

    if (spec.zeroLine) {
      el('line', { x1: m.left, x2: m.left + iw, y1: sy(0), y2: sy(0), class: 'ax-line' }, svg);
    }

    (spec.marks || []).forEach(mk => {
      const x = sx(mk.x);
      el('line', { x1: x, x2: x, y1: m.top, y2: m.top + ih, stroke: p.muted, 'stroke-width': 1 }, svg);
      text(svg, x + 5, m.top + 11, mk.label, 'ax-text');
    });

    (spec.series || []).forEach(s => {
      el('path', {
        d: pathFrom(xs, s.values, sx, sy), fill: 'none', stroke: s.color,
        'stroke-width': s.width || 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round',
        opacity: s.opacity || 1
      }, svg);
      if (s.marker) {
        s.values.forEach((v, i) => {
          if (v === null) return;
          el('circle', {
            cx: sx(xs[i]), cy: sy(v), r: 3.6, fill: s.color,
            stroke: p.surface, 'stroke-width': 2
          }, svg);
        });
      }
    });

    /* Direct label on the endpoint of each labelled series, so identity is never colour alone. */
    (spec.series || []).filter(s => s.directLabel).forEach(s => {
      for (let i = s.values.length - 1; i >= 0; i--) {
        if (s.values[i] === null) continue;
        text(svg, sx(xs[i]) + 7, sy(s.values[i]) + 4, s.directLabel, 'mark-label',
          { fill: s.color, 'text-anchor': 'start' });
        break;
      }
    });

    /* Crosshair: one hit rectangle, nearest index by x. The hit area is the whole plot, so
       there is no pinpoint target to land on. */
    const cross = el('line', { y1: m.top, y2: m.top + ih, class: 'crosshair', opacity: 0 }, svg);
    const dots = el('g', { opacity: 0 }, svg);
    const hit = el('rect', { x: m.left, y: m.top, width: iw, height: ih, class: 'hit' }, svg);

    function move(ev) {
      const box = svg.getBoundingClientRect();
      const px = (ev.clientX - box.left) * (f.width / box.width);
      const xv = sx.invert(px);
      let best = 0, bd = Infinity;
      for (let i = 0; i < xs.length; i++) {
        const d = Math.abs(xs[i] - xv);
        if (d < bd) { bd = d; best = i; }
      }
      const cx = sx(xs[best]);
      cross.setAttribute('x1', cx); cross.setAttribute('x2', cx); cross.setAttribute('opacity', 1);
      dots.innerHTML = '';
      dots.setAttribute('opacity', 1);
      const rows = [];
      (spec.series || []).forEach(s => {
        const v = s.values[best];
        if (v === null || v === undefined) return;
        el('circle', {
          cx: cx, cy: sy(v), r: 4.5, fill: s.color, stroke: p.surface, 'stroke-width': 2
        }, dots);
        rows.push({ color: s.color, k: s.label, v: spec.valueFormat ? spec.valueFormat(v) : val(v) });
      });
      (spec.bands || []).filter(b => b.inTooltip).forEach(b => {
        if (b.lo[best] === null) return;
        rows.push({
          color: b.color, k: b.label,
          v: (spec.valueFormat ? spec.valueFormat(b.lo[best]) : val(b.lo[best])) + ' … '
            + (spec.valueFormat ? spec.valueFormat(b.hi[best]) : val(b.hi[best]))
        });
      });
      tip.show(tipRows(spec.xTooltip ? spec.xTooltip(xs[best], best) : String(xs[best]), rows),
        ev.clientX, ev.clientY);
    }

    hit.addEventListener('mousemove', move);
    hit.addEventListener('mouseleave', () => {
      tip.hide(); cross.setAttribute('opacity', 0); dots.setAttribute('opacity', 0);
    });
  }

  /* ------------------------------------------------------------------------------------------
     Renderer: bars (diverging, grouped, stacked)
     ------------------------------------------------------------------------------------------ */

  function barChart(host, spec) {
    const f = frame(host, spec);
    const { svg, p, m, iw, ih } = f;

    const cats = spec.x;
    const n = cats.length;
    const series = spec.series;
    const mode = spec.mode || 'grouped';

    let yd;
    if (mode === 'stacked') {
      const totals = cats.map((_, i) => series.reduce((a, s) => a + (s.values[i] || 0), 0));
      yd = [0, extent([totals])[1] * 1.06];
    } else {
      /* Whiskers reach beyond their bar, so they belong in the extent. Leaving them out let a
         95 % interval run off the top of the plot and across the text above it. */
      yd = extent(series.map(s => s.values).concat(spec.errors
        ? [spec.errors.map(e => e.lo), spec.errors.map(e => e.hi)] : []));
      yd = mode === 'diverging'
        ? (() => { const a = Math.max(Math.abs(yd[0]), Math.abs(yd[1])) * 1.12; return [-a, a]; })()
        : [Math.min(0, yd[0]), yd[1] * 1.08];
    }
    if (spec.yDomain) yd = spec.yDomain;

    const step = iw / n;
    const sy = linear(yd[0], yd[1], m.top + ih, m.top);
    const sx = i => m.left + step * (i + 0.5);

    drawAxes(f, v => m.left + step * (v + 0.5), sy, Object.assign({}, spec, {
      xTicks: (spec.xTickEvery
        ? cats.map((c, i) => ({ v: i, label: c })).filter((_, i) => i % spec.xTickEvery === 0 || i === n - 1)
        : cats.map((c, i) => ({ v: i, label: c })))
    }));

    const zeroY = sy(Math.max(yd[0], Math.min(yd[1], 0)));
    el('line', { x1: m.left, x2: m.left + iw, y1: zeroY, y2: zeroY, class: 'ax-line' }, svg);

    /* Errors are drawn behind the bars so the bar end stays readable. */
    if (spec.errors) {
      spec.errors.forEach((e, i) => {
        if (e.lo === null) return;
        const x = sx(i);
        el('line', { x1: x, x2: x, y1: sy(e.lo), y2: sy(e.hi), stroke: p.ink2, 'stroke-width': 1 }, svg);
        [e.lo, e.hi].forEach(v => el('line', {
          x1: x - 4, x2: x + 4, y1: sy(v), y2: sy(v), stroke: p.ink2, 'stroke-width': 1
        }, svg));
      });
    }

    /* 2px surface gaps between adjacent fills, not borders. */
    const GAP = 2;
    const inner = Math.max(3, step - GAP * 2);
    const bw = mode === 'grouped' && series.length > 1
      ? Math.max(3, (inner - GAP * (series.length - 1)) / series.length) : inner;

    cats.forEach((cat, i) => {
      let acc = 0;
      series.forEach((s, k) => {
        const v = s.values[i];
        if (v === null || v === undefined) return;
        let x, y, h;
        if (mode === 'stacked') {
          x = sx(i) - inner / 2;
          y = sy(acc + v);
          h = Math.max(0, sy(acc) - sy(acc + v) - GAP);
          acc += v;
        } else {
          x = mode === 'grouped' && series.length > 1
            ? sx(i) - inner / 2 + k * (bw + GAP) : sx(i) - bw / 2;
          y = v >= 0 ? sy(v) : zeroY;
          h = Math.abs(sy(v) - zeroY);
        }
        if (h <= 0) return;
        const fill = typeof s.color === 'function' ? s.color(v, i) : s.color;
        const rect = el('rect', {
          x: x, y: y, width: bw, height: h, fill: fill,
          rx: Math.min(4, bw / 2), ry: Math.min(4, h / 2)
        }, svg);
        rect.addEventListener('mousemove', ev => {
          tip.show(tipRows(spec.catLabel ? spec.catLabel(cat, i) : String(cat), series.map(ss => ({
            color: typeof ss.color === 'function' ? ss.color(ss.values[i], i) : ss.color,
            k: ss.label,
            v: spec.valueFormat ? spec.valueFormat(ss.values[i], i) : nf(ss.values[i], 1)
          }))), ev.clientX, ev.clientY);
        });
        rect.addEventListener('mouseleave', tip.hide);
      });
    });

    (spec.lines || []).forEach(l => {
      el('path', {
        d: pathFrom(cats.map((_, i) => i), l.values, i => sx(i), sy),
        fill: 'none', stroke: l.color, 'stroke-width': l.width || 2
      }, svg);
    });
  }

  /* ------------------------------------------------------------------------------------------
     Renderer: warming stripes
     ------------------------------------------------------------------------------------------ */

  function stripes(host, spec) {
    const f = frame(host, Object.assign({ height: spec.height || 132, margin: { top: 6, right: 6, bottom: 26, left: 6 } }, spec));
    const { svg, p, m, iw, ih } = f;
    const n = spec.values.length;
    const w = iw / n;
    const absmax = Math.max.apply(null, spec.values.map(Math.abs));

    spec.values.forEach((v, i) => {
      const rect = el('rect', {
        x: m.left + i * w, y: m.top, width: Math.ceil(w) + 0.5, height: ih,
        fill: diverging(v, absmax, p)
      }, svg);
      rect.addEventListener('mousemove', ev => {
        tip.show(tipRows(String(spec.labels[i]), [
          { color: diverging(v, absmax, p), k: 'anomaly', v: vals(v, 2) },
          { k: 'mean', v: val(spec.means[i], 2) }
        ]), ev.clientX, ev.clientY);
      });
      rect.addEventListener('mouseleave', tip.hide);
    });

    [0, n - 1].forEach(i => {
      text(svg, m.left + i * w + (i === 0 ? 2 : w - 2), m.top + ih + 16, String(spec.labels[i]),
        'ax-text', { 'text-anchor': i === 0 ? 'start' : 'end' });
    });
  }

  /* ------------------------------------------------------------------------------------------
     Renderer: heatmap
     ------------------------------------------------------------------------------------------ */

  function heatmap(host, spec) {
    const rows = spec.values.length;
    const cols = spec.values[0].length;
    const width = Math.max(260, host.clientWidth || 640);
    const m = Object.assign({ top: 20, right: 12, bottom: 66, left: 42 }, spec.margin || {});
    const cell = Math.max(9, Math.min(spec.maxCell || 56, (width - m.left - m.right) / cols));
    const height = m.top + m.bottom + cell * rows;

    const f = frame(host, { height: height, margin: m, ariaLabel: spec.ariaLabel });
    const { svg, p } = f;
    const iw = cell * cols;

    const flat = spec.values.flat().filter(v => v !== null);
    const lo = spec.min !== undefined ? spec.min : Math.min.apply(null, flat);
    const hi = spec.max !== undefined ? spec.max : Math.max.apply(null, flat);
    const absmax = Math.max.apply(null, flat.map(Math.abs)) || 1;
    const color = v => spec.scale === 'diverging'
      ? diverging(v, absmax, p)
      : (v === null ? 'transparent' : ramp(p.seq, (v - lo) / ((hi - lo) || 1)));

    const GAP = 1;
    for (let r0 = 0; r0 < rows; r0++) {
      for (let c = 0; c < cols; c++) {
        const v = spec.values[r0][c];
        const rect = el('rect', {
          x: m.left + c * cell + GAP / 2, y: m.top + r0 * cell + GAP / 2,
          width: cell - GAP, height: cell - GAP, rx: 2,
          fill: color(v)
        }, svg);
        if (v === null) continue;
        rect.addEventListener('mousemove', ev => {
          tip.show(tipRows(spec.yLabels[r0] + ' · ' + spec.xLabels[c], [
            { color: color(v), k: spec.zLabel, v: spec.valueFormat ? spec.valueFormat(v) : val(v) }
          ]), ev.clientX, ev.clientY);
        });
        rect.addEventListener('mouseleave', tip.hide);
      }
    }

    const everyX = Math.max(1, Math.ceil(cols / Math.max(2, Math.floor(iw / 34))));
    spec.xLabels.forEach((lab, c) => {
      if (c % everyX) return;
      text(svg, m.left + c * cell + cell / 2, m.top - 7, lab, 'ax-text', { 'text-anchor': 'middle' });
    });
    const everyY = Math.max(1, Math.ceil(rows / Math.max(2, Math.floor(cell * rows / 16))));
    spec.yLabels.forEach((lab, r0) => {
      if (r0 % everyY) return;
      text(svg, m.left - 7, m.top + r0 * cell + cell / 2 + 4, lab, 'ax-text', { 'text-anchor': 'end' });
    });

    scaleBar(svg, m.left, m.top + cell * rows + 32, Math.min(iw, 240),
      spec.scale === 'diverging' ? [-absmax, absmax] : [lo, hi],
      spec.scale === 'diverging' ? [p.cold, p.mid, p.warm] : p.seq,
      spec.zLabel, spec.scaleFormat || (v => nf(v, 1)));
  }

  /**
   * The colour scale of a heatmap: what the scale means above the bar, its two ends below it.
   *
   * The label sits above rather than beside the gradient. Beside it, a long label on a narrow card
   * ran off the right edge of the drawing - which the palette validator cannot see, because it is a
   * layout fault rather than a colour one, and only looking at the rendered page finds it.
   */
  function scaleBar(svg, x, y, w, domain, stops, label, fmt) {
    const id = 'grad' + Math.random().toString(36).slice(2, 9);
    const defs = el('defs', {}, svg);
    const lg = el('linearGradient', { id: id, x1: '0', x2: '1', y1: '0', y2: '0' }, defs);
    stops.forEach((c, i) => el('stop', {
      offset: (i / (stops.length - 1) * 100) + '%', 'stop-color': c
    }, lg));
    if (label) text(svg, x, y - 7, label, 'scalebar-text');
    el('rect', { x: x, y: y, width: w, height: 8, rx: 4, fill: 'url(#' + id + ')' }, svg);
    text(svg, x, y + 21, fmt(domain[0]), 'scalebar-text');
    text(svg, x + w, y + 21, fmt(domain[1]), 'scalebar-text', { 'text-anchor': 'end' });
  }

  /* ------------------------------------------------------------------------------------------
     Renderer: dot-and-range (climatology per calendar month)
     ------------------------------------------------------------------------------------------ */

  function rangeChart(host, spec) {
    const f = frame(host, spec);
    const { svg, p, m, iw, ih } = f;
    const rows = spec.rows;
    const n = rows.length;

    const yd = pad(extent([rows.map(r0 => r0.lo), rows.map(r0 => r0.hi),
    rows.map(r0 => r0.outerLo), rows.map(r0 => r0.outerHi)]), 0.05);
    const sx = linear(yd[0], yd[1], m.left, m.left + iw);
    const step = ih / n;

    const g = el('g', {}, svg);
    niceTicks(yd[0], yd[1], 6).forEach(v => {
      const x = sx(v);
      el('line', { x1: x, x2: x, y1: m.top, y2: m.top + ih, class: 'gridline' }, g);
      text(g, x, m.top + ih + 17, nf(v, 0), 'ax-text', { 'text-anchor': 'middle' });
    });
    el('line', { x1: m.left, x2: m.left + iw, y1: m.top + ih, y2: m.top + ih, class: 'ax-line' }, g);
    if (spec.xLabel) text(g, m.left + iw / 2, f.height - 2, spec.xLabel, 'ax-title', { 'text-anchor': 'middle' });

    rows.forEach((row, i) => {
      const y = m.top + step * (i + 0.5);
      text(g, m.left - 8, y + 4, row.label, 'ax-text', { 'text-anchor': 'end' });

      el('line', {
        x1: sx(row.outerLo), x2: sx(row.outerHi), y1: y, y2: y,
        stroke: p.bandInner, 'stroke-width': 3, 'stroke-linecap': 'round'
      }, g);
      el('rect', {
        x: sx(row.lo), y: y - 6, width: Math.max(2, sx(row.hi) - sx(row.lo)), height: 12, rx: 4,
        fill: p.bandInner
      }, g);
      el('circle', { cx: sx(row.mid), cy: y, r: 5, fill: p.series[0], stroke: p.surface, 'stroke-width': 2 }, g);

      const hit = el('rect', { x: m.left, y: y - step / 2, width: iw, height: step, class: 'hit' }, g);
      hit.addEventListener('mousemove', ev => {
        tip.show(tipRows(row.title, [
          { color: p.series[0], k: 'monthly mean', v: val(row.mid, 1) },
          { color: p.bandInner, k: 'coolest / warmest year', v: val(row.lo, 1) + ' … ' + val(row.hi, 1) },
          { color: p.bandInner, k: 'measured record', v: val(row.outerLo, 1) + ' … ' + val(row.outerHi, 1) }
        ]), ev.clientX, ev.clientY);
      });
      hit.addEventListener('mouseleave', tip.hide);
    });
  }

  /* ------------------------------------------------------------------------------------------
     Renderer: small multiples
     Twelve monthly curves cannot each take a hue - past eight, categories fold or facet. They
     are faceted here, one panel per month, each against the record's own mean curve.
     ------------------------------------------------------------------------------------------ */

  function smallMultiples(host, spec) {
    const width = Math.max(260, host.clientWidth || 640);
    const cols = width > 1080 ? 6 : width > 760 ? 4 : width > 460 ? 3 : 2;
    const rows = Math.ceil(spec.panels.length / cols);
    const pw = width / cols;
    const ph = Math.max(96, Math.min(150, pw * 0.72));
    const height = rows * ph + 8;

    const f = frame(host, { height: height, margin: { top: 0, right: 0, bottom: 0, left: 0 }, ariaLabel: spec.ariaLabel });
    const { svg, p } = f;

    const yd = pad(extent(spec.panels.map(x => x.values).concat([spec.reference])), 0.08);
    const xd = [spec.x[0], spec.x[spec.x.length - 1]];
    const yTicks = niceTicks(yd[0], yd[1], 3);

    spec.panels.forEach((panel, i) => {
      const cx = (i % cols) * pw, cy = Math.floor(i / cols) * ph;
      const g = el('g', { transform: 'translate(' + cx + ',' + cy + ')' }, svg);
      const m = { top: 20, right: 10, bottom: 20, left: 30 };
      const iw = pw - m.left - m.right, ih = ph - m.top - m.bottom;
      const sx = linear(xd[0], xd[1], m.left, m.left + iw);
      const sy = linear(yd[0], yd[1], m.top + ih, m.top);

      yTicks.forEach(v => {
        el('line', { x1: m.left, x2: m.left + iw, y1: sy(v), y2: sy(v), class: 'gridline' }, g);
        if (i % cols === 0) text(g, m.left - 5, sy(v) + 4, nf(v, 0), 'ax-text', { 'text-anchor': 'end' });
      });
      [0, 6, 12, 18, 24].forEach(h => {
        if (h > xd[1]) return;
        if (i >= spec.panels.length - cols) {
          text(g, sx(h), m.top + ih + 14, String(h), 'ax-text', { 'text-anchor': 'middle' });
        }
      });
      el('line', { x1: m.left, x2: m.left + iw, y1: m.top + ih, y2: m.top + ih, class: 'ax-line' }, g);

      el('path', {
        d: pathFrom(spec.x, spec.reference, sx, sy), fill: 'none',
        stroke: p.bandInner, 'stroke-width': 1.5
      }, g);
      el('path', {
        d: pathFrom(spec.x, panel.values, sx, sy), fill: 'none',
        stroke: p.series[0], 'stroke-width': 2, 'stroke-linejoin': 'round'
      }, g);
      text(g, m.left, 12, panel.label, 'mark-label');

      const hit = el('rect', { x: m.left, y: m.top, width: iw, height: ih, class: 'hit' }, g);
      hit.addEventListener('mousemove', ev => {
        const box = svg.getBoundingClientRect();
        const px = (ev.clientX - box.left) * (f.width / box.width) - cx;
        const xv = sx.invert(px);
        let best = 0, bd = Infinity;
        spec.x.forEach((v, k) => { const d = Math.abs(v - xv); if (d < bd) { bd = d; best = k; } });
        const hh = Math.floor(spec.x[best]), mm = Math.round((spec.x[best] - hh) * 60);
        tip.show(tipRows(panel.title + ', ' + String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0'), [
          { color: p.series[0], k: panel.label, v: val(panel.values[best], 1) },
          { color: p.bandInner, k: 'all months', v: val(spec.reference[best], 1) }
        ]), ev.clientX, ev.clientY);
      });
      hit.addEventListener('mouseleave', tip.hide);
    });
  }

  /* ------------------------------------------------------------------------------------------
     Cards
     ------------------------------------------------------------------------------------------ */

  const registry = [];

  function legendHTML(items) {
    return '<div class="legend">' + items.map(i =>
      '<span class="legend-item"><span class="legend-swatch ' + (i.line ? 'line' : '') + '" style="background:'
      + i.color + '"></span>' + i.label + '</span>').join('') + '</div>';
  }

  function tableHTML(table) {
    let html = '<div class="tablewrap"><table><thead><tr>';
    table.columns.forEach(c => { html += '<th>' + c + '</th>'; });
    html += '</tr></thead><tbody>';
    table.rows.forEach(row => {
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

  /**
   * Build one card.
   * `def.render(host)` draws the chart; `def.table` is the same numbers as a table, which is what
   * makes the values reachable without a pointer. A card with no `render` is a table-only card.
   */
  function card(parent, def) {
    const node = document.createElement('section');
    node.className = 'card ' + (def.width || 'w-6');

    let head = '<div class="card-head"><div><h3 class="card-title">' + def.title + '</h3>'
      + (def.sub ? '<p class="card-sub">' + def.sub + '</p>' : '') + '</div>';
    if (def.render && def.table) {
      head += '<div class="viewtoggle" role="group" aria-label="View">'
        + '<button type="button" data-view="chart" aria-pressed="true">Chart</button>'
        + '<button type="button" data-view="table" aria-pressed="false">Table</button></div>';
    }
    head += '</div>';

    node.innerHTML = head
      + '<div class="card-body"><div class="chart"></div>'
      + (def.legend ? legendHTML(def.legend) : '')
      + '<div class="tableview" hidden></div></div>'
      + (def.foot ? '<p class="card-foot">' + def.foot + '</p>' : '');

    parent.appendChild(node);

    const chartHost = node.querySelector('.chart');
    const tableHost = node.querySelector('.tableview');
    const legendNode = node.querySelector('.legend');

    if (def.table) tableHost.innerHTML = tableHTML(def.table);
    if (!def.render) {
      chartHost.remove();
      tableHost.hidden = false;
    }

    node.querySelectorAll('.viewtoggle button').forEach(btn => {
      btn.addEventListener('click', () => {
        const wantTable = btn.dataset.view === 'table';
        node.querySelectorAll('.viewtoggle button').forEach(b =>
          b.setAttribute('aria-pressed', String((b.dataset.view === 'table') === wantTable)));
        chartHost.hidden = wantTable;
        if (legendNode) legendNode.hidden = wantTable;
        tableHost.hidden = !wantTable;
        if (!wantTable) draw();
      });
    });

    let lastWidth = 0;
    function draw() {
      if (!def.render || chartHost.hidden) return;
      def.render(chartHost);
      lastWidth = chartHost.clientWidth;
    }

    if (def.render) {
      registry.push(draw);
      new ResizeObserver(() => {
        if (chartHost.hidden) return;
        if (Math.abs(chartHost.clientWidth - lastWidth) > 6) draw();
      }).observe(chartHost);
    }
    return node;
  }

  function renderAll() { registry.forEach(fn => fn()); }


  /* ------------------------------------------------------------------------------------------
     Page

     Everything below is driven by the payload rather than by a particular variable: a section
     whose data are absent removes itself, including its entry in the top navigation. That is what
     lets one engine serve a gap-filled temperature record and a precipitation total.
     ------------------------------------------------------------------------------------------ */

  const years = DATA.years;
  const Y = DATA.yearly;
  const col = k => Y.map(y => y[k]);
  const VAR = M.key;                 // short name, for axis labels
  const AGG = M.agg_label;           // 'mean' or 'total'
  const EX = DATA.extremes;
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);

  /* Ordinal ramps for the threshold-day groups: one hue, ordered by severity. A group carries at
     most as many indices as its ramp has steps, which the registry asserts. */
  const RAMPS = { cold: ['--cold-1', '--cold-2'], warm: ['--warm-1', '--warm-2', '--warm-3'] };

  function dropSection(id) {
    const heading = document.getElementById(id);
    if (heading) heading.remove();
    const grid = document.getElementById('g-' + id.slice(2));
    if (grid) grid.remove();
    const link = document.querySelector('.sectionnav a[href="#' + id + '"]');
    if (link) link.remove();
  }

  function xTicksForYears(host) {
    return yearTicks(years, host.clientWidth);
  }

  function everyNth(host) {
    return Math.max(1, Math.ceil(years.length / Math.max(3, Math.floor(host.clientWidth / 54))));
  }

  /* ---- Header ----------------------------------------------------------------------------- */

  function header() {
    document.getElementById('brand-site').textContent = M.site;
    document.getElementById('brand-sub').textContent =
      M.title.toLowerCase() + ' · ' + M.first_year + '–' + M.last_year;
    document.getElementById('page-title').textContent =
      M.title + ' at ' + M.site + ', ' + M.first_year + '–' + M.last_year;

    document.getElementById('page-lede').innerHTML =
      M.about + ' The product is written by a notebook in <code>10_METEO/30_PRODUCTS/</code>; this '
      + 'page describes what was exported and computes nothing of its own. Every figure below uses '
      + '<code>' + M.varname + '</code>.';

    const chips = [
      ['Period', M.first_year + '–' + M.last_year],
      ['Records', M.n_records.toLocaleString('en-GB')],
      ['Resolution', M.resolution],
      ['Measured', nf(DATA.hero.measured_pct, 1) + ' %'],
      ['Product', M.product]
    ];
    document.getElementById('page-chips').innerHTML =
      chips.map(c => '<li>' + c[0] + ' <b>' + c[1] + '</b></li>').join('');

    const paragraphs = [];
    paragraphs.push(
      '<b>Extremes are taken from measured records only.</b> A gap-filled or reconstructed value is '
      + 'a model result and cannot set a record, which is why the measured share of each year is '
      + 'reported before any statistic. '
      + (M.agg === 'sum'
        ? '<b>Yearly figures are annual totals.</b> A record with no measurement contributes nothing '
        + 'to its year rather than counting as zero, so a year with gaps under-reports; the '
        + 'coverage section says by how much.'
        : '<b>Yearly figures are means of yearly means</b>, so every year carries the same weight.'));
    if (M.correction) paragraphs.push(M.correction.note);
    (M.notes || []).forEach(n => paragraphs.push(n));

    document.getElementById('page-note').innerHTML =
      paragraphs.map(p => '<p>' + p + '</p>').join('');

    document.getElementById('footer-text').innerHTML =
      'Built ' + M.generated + ' from <code>' + M.product + '</code> by '
      + '<code>90_DATASET_OVERVIEW/build_meteo_dashboard.py</code>. The full method narrative, with '
      + 'the evidence behind every correction, is in the product notebook and in the overview '
      + 'notebooks of <code>90_DATASET_OVERVIEW/</code>. ' + M.site + ' flux product · '
      + 'Lukas Hörtnagl, ETH Zurich.';
  }

  /* ---- Stat tiles ------------------------------------------------------------------------- */

  function tiles() {
    const h = DATA.hero;
    const recentLength = h.recent_period[1] - h.recent_period[0] + 1;
    const items = [
      {
        label: cap(AGG) + ' ' + M.first_year + '–' + M.last_year,
        value: nf(h.mean, 2), unit: U,
        sub: '±' + nf(h.sd, 2) + ' ' + U + ' SD between years'
      },
      {
        label: 'Trend', value: nfs(h.slope, 2), unit: U + '/decade',
        sub: 'Theil-Sen, 95 % ' + nfs(h.slope_low, 2) + ' to ' + nfs(h.slope_high, 2)
          + ' · Kendall p = ' + nf(h.p, 4)
      },
      /* A period difference needs both periods. Where a record starts inside the recent window - a
         soil depth whose sensor was installed late - there is nothing to difference, and the tile
         says which period is empty instead of printing a dash. */
      h.period_delta === null ? {
        label: 'Last ' + recentLength + ' years', value: '—', unit: '',
        sub: (h.early_mean === null ? h.early_period[0] + '–' + h.early_period[1]
          : h.recent_period[0] + '–' + h.recent_period[1])
          + ' holds no measurements, so the two periods cannot be compared'
      } : {
        label: 'Last ' + recentLength + ' years', value: nfs(h.period_delta, 2), unit: U,
        sub: h.recent_period[0] + '–' + h.recent_period[1] + ' against '
          + h.early_period[0] + '–' + h.early_period[1]
          + (h.period_delta_pct === null ? '' : ' · ' + nfs(h.period_delta_pct, 1) + ' %')
      },
      {
        label: cap(EX.high_label) + ' year', value: String(h.high_year), unit: '',
        sub: val(h.high_value, 2) + ' · ' + EX.low_label + ' ' + h.low_year + ', '
          + val(h.low_value, 2),
        accent: 'warm'
      },
      {
        label: cap(EX.high_label) + ' half-hour', value: nf(h.record_high, 1), unit: U,
        sub: h.record_high_when, accent: 'warm'
      }
    ];
    /* A scale with a hard floor has no informative low extreme; the payload says so rather than the
       page showing whichever of thousands of tied records happened to come first. */
    if (EX.show_low_halfhour) {
      items.push({
        label: cap(EX.low_label) + ' half-hour', value: nf(h.record_low, 1), unit: U,
        sub: h.record_low_when, accent: 'cold'
      });
    }
    items.push(
      {
        label: 'Measured', value: nf(h.measured_pct, 1), unit: '%',
        sub: M.has_fill_flag ? 'the rest is filled or reconstructed; see Coverage'
          : 'the rest is missing; the record is exported with its gaps'
      });
    if (h.growing_season !== null && h.growing_season !== undefined) {
      items.push({
        label: 'Growing season', value: nf(h.growing_season, 0), unit: 'days',
        sub: 'mean length on a ' + nf(M.growing_season_base, 0) + ' ' + U + ' base'
      });
    }
    document.getElementById('tiles').innerHTML = items.map(i =>
      '<div class="tile' + (i.accent ? ' tile-accent-' + i.accent : '') + '">'
      + '<span class="tile-label">' + i.label + '</span>'
      + '<span class="tile-value">' + i.value
      + (i.unit ? '<span class="unit">' + i.unit + '</span>' : '') + '</span>'
      + '<span class="tile-sub">' + i.sub + '</span></div>').join('');
  }

  /* ---- The record ------------------------------------------------------------------------- */

  function sectionRecord() {
    const g = document.getElementById('g-record');

    card(g, {
      width: 'w-12',
      title: 'Anomaly stripes',
      sub: 'Each year as a departure from the ' + M.first_year + '–' + M.last_year + ' ' + AGG
        + '. One bar per year, colour is the only encoding — the values are in the table view and '
        + 'in the yearly chart below.',
      render: host => stripes(host, {
        values: col('anomaly'), labels: years, means: col('mean'),
        ariaLabel: 'Yearly ' + M.title.toLowerCase() + ' anomaly as coloured stripes'
      }),
      table: {
        columns: ['Year', cap(AGG) + ' (' + U + ')', 'Anomaly (' + U + ')', 'Rank'],
        rows: Y.map(y => [y.year, nf(y.mean, 2),
        { v: nfs(y.anomaly, 2), cls: y.anomaly >= 0 ? 'num-warm' : 'num-cold' }, y.rank])
      },
      foot: 'The reference period is the record itself, which is too short to provide a climate '
        + 'normal such as 1991–2020.'
    });

    const rib = DATA.ribbon;
    const idx = rib.dates.map((_, i) => i);
    const yearStart = {};
    rib.dates.forEach((d, i) => { const y = d.slice(0, 4); if (!(y in yearStart)) yearStart[y] = i; });
    const tickYears = Object.keys(yearStart);

    const legend = [];
    if (rib.lo) legend.push({ color: cv('--band-inner'), label: rib.band_label });
    if (rib.line) legend.push({ color: cv('--series-1'), label: rib.line_label, line: true });
    legend.push({ color: cv('--series-2'), label: '31-day running mean', line: true });

    /* The daily series runs to several thousand records, so the table view carries monthly
       aggregates of it. The daily values themselves are in the product file. */
    const monthAgg = {};
    rib.dates.forEach((d, i) => {
      const key = d.slice(0, 7);
      const a = monthAgg[key] || (monthAgg[key] = { lo: Infinity, hi: -Infinity, sum: 0, n: 0 });
      const low = rib.lo ? rib.lo[i] : (rib.line ? rib.line[i] : null);
      const high = rib.hi ? rib.hi[i] : (rib.line ? rib.line[i] : null);
      if (low !== null) a.lo = Math.min(a.lo, low);
      if (high !== null) a.hi = Math.max(a.hi, high);
      const mid = rib.line ? rib.line[i] : rib.smooth[i];
      if (mid !== null) { a.sum += mid; a.n++; }
    });

    card(g, {
      width: 'w-12',
      title: 'The daily record',
      sub: (rib.lo ? cap(rib.band_label) + ', with a 31-day centred running mean on top. '
        : cap(rib.line_label) + ' with a 31-day centred running mean on top. ')
        + 'Every day of ' + M.first_year + '–' + M.last_year + ' is drawn, filled records '
        + 'included.',
      legend: legend,
      render: host => lineChart(host, {
        height: Math.max(260, Math.min(360, host.clientWidth * 0.26)),
        x: idx,
        bands: rib.lo
          ? [{ lo: rib.lo, hi: rib.hi, color: token('--band-inner'), label: rib.band_label, inTooltip: true }]
          : [],
        series: [].concat(
          rib.line ? [{
            values: rib.line, color: token('--series-1'), label: rib.line_label,
            width: 0.6, opacity: 0.8
          }] : [],
          [{ values: rib.smooth, color: token('--series-2'), label: '31-day running mean', width: 2.2 }]
        ),
        xTicks: tickYears.filter((_, i) => i % (host.clientWidth > 900 ? 1 : 3) === 0)
          .map(y => ({ v: yearStart[y], label: y })),
        yLabel: VAR + ' (' + U + ')', yDigits: 0, yZero: M.agg === 'sum',
        xTooltip: i => rib.dates[i],
        ariaLabel: 'The daily ' + M.title.toLowerCase() + ' record'
      }),
      table: {
        columns: ['Month', 'Mean of days (' + U + ')', 'Lowest day (' + U + ')',
          'Highest day (' + U + ')'],
        rows: Object.keys(monthAgg).map(k => [k, nf(monthAgg[k].sum / monthAgg[k].n, 1),
        { v: nf(monthAgg[k].lo, 1), cls: 'num-cold' }, { v: nf(monthAgg[k].hi, 1), cls: 'num-warm' }])
      },
      foot: 'The table view aggregates the daily series to months; the daily and half-hourly values '
        + 'are in the product file itself.'
    });
  }

  /* ---- Year by year ----------------------------------------------------------------------- */

  function sectionYears() {
    const g = document.getElementById('g-years');
    const h = DATA.hero;

    card(g, {
      width: 'w-8',
      title: 'Yearly ' + AGG + ' and its trend',
      sub: 'Theil-Sen slope ' + nfs(h.slope, 2) + ' ' + U + ' per decade (95 % interval '
        + nfs(h.slope_low, 2) + ' to ' + nfs(h.slope_high, 2) + ', Kendall p = ' + nf(h.p, 4)
        + '). Theil-Sen because one extreme year does not move it; a trend over this record is a '
        + 'statement about these years, not a projection.',
      legend: [
        { color: cv('--series-1'), label: 'yearly ' + AGG, line: true },
        { color: cv('--series-2'), label: 'Theil-Sen fit', line: true }
      ],
      render: host => lineChart(host, {
        aspect: 0.44,
        x: years,
        series: [
          { values: col('mean'), color: token('--series-1'), label: 'yearly ' + AGG, width: 2, marker: true },
          { values: col('fit'), color: token('--series-2'), label: 'Theil-Sen fit', width: 2 }
        ],
        xTicks: xTicksForYears(host),
        yLabel: VAR + ' (' + U + ')', yDigits: 1,
        xTooltip: y => String(y), valueFormat: x => val(x, 2),
        ariaLabel: 'Yearly ' + M.title.toLowerCase() + ' with its Theil-Sen trend'
      }),
      table: {
        columns: ['Year', cap(AGG) + ' (' + U + ')', 'Fit (' + U + ')',
          'Measured minimum (' + U + ')', 'Measured maximum (' + U + ')', 'Not measured (%)'],
        rows: Y.map(y => [y.year, nf(y.mean, 2), nf(y.fit, 2),
        { v: nf(y.min, 1), cls: 'num-cold' }, { v: nf(y.max, 1), cls: 'num-warm' }, nf(y.filled, 1)])
      }
    });

    card(g, {
      width: 'w-4',
      title: 'Anomaly per year',
      sub: 'The same numbers as the stripes, on an axis. Departure from the record ' + AGG + ' of '
        + val(h.mean, 2) + '.',
      render: host => barChart(host, {
        aspect: 0.9,
        x: years.map(String),
        mode: 'diverging',
        series: [{
          values: col('anomaly'), label: 'anomaly',
          color: x => x >= 0 ? token('--pole-warm') : token('--pole-cold')
        }],
        xTickEvery: everyNth(host),
        yLabel: 'anomaly (' + U + ')', yDigits: 1,
        valueFormat: x => vals(x, 2),
        ariaLabel: 'Yearly ' + M.title.toLowerCase() + ' anomaly'
      }),
      table: {
        columns: ['Year', 'Anomaly (' + U + ')', 'Rank'],
        rows: Y.map(y => [y.year,
        { v: nfs(y.anomaly, 2), cls: y.anomaly >= 0 ? 'num-warm' : 'num-cold' }, y.rank])
      }
    });

    /* The yearly figure is drawn beside the percentiles only where the two are the same quantity.
       For a summed variable the annual total and a half-hourly percentile differ by three orders of
       magnitude, and putting both on one axis would be a dual scale in all but name. */
    const withTotal = M.agg !== 'sum';
    card(g, {
      width: 'w-6',
      title: 'Distribution per year',
      sub: 'Percentiles of the ' + M.quantile_basis + '. Bands moving together is a shift of the '
        + 'whole distribution; one edge moving alone is a change in the extremes only.',
      legend: [
        { color: cv('--band-outer'), label: '5th to 95th percentile' },
        { color: cv('--band-inner'), label: '25th to 75th percentile' },
        { color: cv('--series-1'), label: 'median', line: true }
      ].concat(withTotal ? [{ color: cv('--series-2'), label: 'yearly ' + AGG, line: true }] : []),
      render: host => lineChart(host, {
        aspect: 0.5,
        x: years,
        bands: [
          { lo: col('q05'), hi: col('q95'), color: token('--band-outer'), label: '5th–95th', inTooltip: true },
          { lo: col('q25'), hi: col('q75'), color: token('--band-inner'), label: '25th–75th', inTooltip: true }
        ],
        series: [
          { values: col('q50'), color: token('--series-1'), label: 'median', width: 2, marker: true }
        ].concat(withTotal
          ? [{ values: col('mean'), color: token('--series-2'), label: 'yearly ' + AGG, width: 2 }]
          : []),
        xTicks: xTicksForYears(host),
        yLabel: VAR + ' (' + U + ')', yDigits: withTotal ? 0 : 1,
        xTooltip: y => String(y),
        ariaLabel: 'Percentile bands of ' + M.quantile_basis + ' per year'
      }),
      table: {
        columns: ['Year', '5th (' + U + ')', '25th (' + U + ')', 'Median (' + U + ')',
          '75th (' + U + ')', '95th (' + U + ')']
          .concat(withTotal ? [cap(AGG) + ' (' + U + ')'] : []),
        rows: Y.map(y => [y.year, nf(y.q05, 1), nf(y.q25, 1), nf(y.q50, 1), nf(y.q75, 1),
        nf(y.q95, 1)].concat(withTotal ? [nf(y.mean, 2)] : []))
      },
      foot: withTotal ? null
        : 'Computed over the ' + M.quantile_basis + ' only. The annual total is the card above; the '
        + 'two are different quantities and are deliberately not drawn on one axis.'
    });

    card(g, {
      width: 'w-6',
      title: 'Trend per calendar month',
      sub: 'Theil-Sen slope fitted to each calendar month separately, with its 95 % interval. It '
        + 'shows which part of the year carries the yearly trend. Twelve tests on one record, so a '
        + 'single significant month is weak evidence on its own.',
      render: host => barChart(host, {
        aspect: 0.5,
        x: DATA.monthly_trend.map(t => t.label),
        mode: 'diverging',
        series: [{
          values: DATA.monthly_trend.map(t => t.slope), label: 'trend',
          color: x => x >= 0 ? token('--pole-warm') : token('--pole-cold')
        }],
        errors: DATA.monthly_trend.map(t => ({ lo: t.low, hi: t.high })),
        yLabel: U + ' per decade', yDigits: 1,
        valueFormat: (x, i) => nfs(x, 2) + ' ' + U + '/decade · p = ' + nf(DATA.monthly_trend[i].p, 3),
        ariaLabel: 'Trend of monthly ' + M.title.toLowerCase() + ' per calendar month'
      }),
      table: {
        columns: ['Month', 'Trend (' + U + '/decade)', 'Lower 95 %', 'Upper 95 %', 'p', 'Significant'],
        rows: DATA.monthly_trend.map(t => [t.label,
        { v: nfs(t.slope, 2), cls: t.slope >= 0 ? 'num-warm' : 'num-cold' },
        nfs(t.low, 2), nfs(t.high, 2), nf(t.p, 4), t.significant ? 'yes' : 'no'])
      },
      foot: 'Whiskers are the 95 % interval of the slope, not of the yearly values.'
    });
  }

  /* ---- Seasonality ------------------------------------------------------------------------ */

  function sectionSeasons() {
    const g = document.getElementById('g-seasons');
    const ac = DATA.annual_cycle;
    const mo = DATA.monthly;
    const dailyWord = M.agg === 'sum' ? 'daily total' : 'daily mean';

    card(g, {
      width: 'w-8',
      title: 'Mean annual cycle',
      sub: cap(dailyWord) + ' by day of year, with the spread across years behind it and '
        + M.last_year + ' drawn on top. Day 366 rests on the leap years alone and is noisier than '
        + 'its neighbours.',
      legend: [
        { color: cv('--band-outer'), label: 'minimum to maximum across years' },
        { color: cv('--band-inner'), label: '10th to 90th percentile' },
        { color: cv('--series-1'), label: 'mean', line: true },
        { color: cv('--series-2'), label: String(M.last_year), line: true }
      ],
      render: host => lineChart(host, {
        aspect: 0.42,
        x: ac.doy,
        bands: [
          { lo: ac.min, hi: ac.max, color: token('--band-outer'), label: 'range across years', inTooltip: true },
          { lo: ac.p10, hi: ac.p90, color: token('--band-inner'), label: '10th–90th', inTooltip: true }
        ],
        series: [
          { values: ac.mean, color: token('--series-1'), label: 'mean', width: 2 },
          { values: ac.last, color: token('--series-2'), label: String(M.last_year), width: 1.4 }
        ],
        xTicks: [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335].map((d, i) => ({
          v: d, label: mo.months[i]
        })),
        yLabel: VAR + ' (' + U + ')', yDigits: 0,
        xTooltip: d => 'Day of year ' + d,
        ariaLabel: 'Mean annual cycle of ' + dailyWord + ' ' + M.title.toLowerCase()
      }),
      table: {
        columns: ['Day of year', 'Mean (' + U + ')', '10th (' + U + ')', '90th (' + U + ')',
          'Min (' + U + ')', 'Max (' + U + ')', String(M.last_year) + ' (' + U + ')'],
        rows: ac.doy.map((d, i) => [d, nf(ac.mean[i], 1), nf(ac.p10[i], 1), nf(ac.p90[i], 1),
        nf(ac.min[i], 1), nf(ac.max[i], 1), nf(ac.last[i], 1)])
      }
    });

    card(g, {
      width: 'w-4',
      title: 'Climatology per calendar month',
      sub: 'The long-term monthly ' + AGG + ', the span between the lowest and highest year of that '
        + 'month, and the measured half-hourly record either side of it.',
      legend: [
        { color: cv('--series-1'), label: 'long-term monthly ' + AGG },
        { color: cv('--band-inner'), label: 'year-to-year span, and measured records' }
      ],
      render: host => rangeChart(host, {
        height: 400,
        margin: { top: 10, right: 16, bottom: 34, left: 40 },
        xLabel: VAR + ' (' + U + ')',
        rows: DATA.climatology.map(c => ({
          label: c.label, title: c.label + ' ' + M.first_year + '–' + M.last_year,
          mid: c.mean, lo: c.min, hi: c.max, outerLo: c.rec_low, outerHi: c.rec_high
        })),
        ariaLabel: 'Monthly climatology with year spread and measured records'
      }),
      table: {
        columns: ['Month', cap(AGG) + ' (' + U + ')', 'SD (' + U + ')', 'Lowest year',
          'Highest year', 'Record low (' + U + ')', 'Record high (' + U + ')'],
        rows: DATA.climatology.map(c => [c.label, nf(c.mean, 1), nf(c.sd, 1),
        c.min_year + ' (' + nf(c.min, 1) + ')', c.max_year + ' (' + nf(c.max, 1) + ')',
        { v: nf(c.rec_low, 1), cls: 'num-cold' }, { v: nf(c.rec_high, 1), cls: 'num-warm' }])
      },
      foot: 'Records are half-hourly measured values, so they lie outside any monthly ' + AGG + '.'
    });

    card(g, {
      width: 'w-6',
      title: 'Monthly ' + AGG + ' by year and month',
      sub: 'The seasonal cycle dominates this surface; the anomaly card beside it removes it so a '
        + 'single unusual month can be read.',
      render: host => heatmap(host, {
        xLabels: mo.months, yLabels: mo.years.map(String), values: mo.values,
        scale: 'sequential', zLabel: 'monthly ' + AGG + ' (' + U + ')',
        ariaLabel: 'Monthly ' + M.title.toLowerCase() + ' by year and month'
      }),
      table: {
        columns: ['Year'].concat(mo.months),
        rows: mo.years.map((y, i) => [y].concat(mo.values[i].map(x => nf(x, 1))))
      }
    });

    card(g, {
      width: 'w-6',
      title: 'Monthly anomaly by year and month',
      sub: 'Each month against the ' + AGG + ' of that month over ' + M.first_year + '–'
        + M.last_year + '. The two poles are equal distances from zero, so a column compares with '
        + 'any other column and a run of unusual months reads as a block.',
      render: host => heatmap(host, {
        xLabels: mo.months, yLabels: mo.years.map(String), values: mo.anomaly,
        scale: 'diverging', zLabel: 'anomaly (' + U + ')', valueFormat: x => vals(x, 2),
        ariaLabel: 'Monthly ' + M.title.toLowerCase() + ' anomaly by year and month'
      }),
      table: {
        columns: ['Year'].concat(mo.months),
        rows: mo.years.map((y, i) => [y].concat(mo.anomaly[i].map(x =>
          ({ v: nfs(x, 1), cls: x >= 0 ? 'num-warm' : 'num-cold' }))))
      }
    });

    const mh = DATA.month_hour;
    const hourLabels = mh.hours.map(h => String(h).padStart(2, '0'));

    card(g, {
      width: 'w-6',
      title: 'Mean by month and hour',
      sub: 'The seasonal and the diurnal cycle on one surface. Hours are the centre of the '
        + 'averaging window, so 00 covers 00:00 to 01:00.',
      render: host => heatmap(host, {
        xLabels: hourLabels, yLabels: mh.months, values: mh.values,
        scale: 'sequential', zLabel: 'mean (' + U + ')', maxCell: 30,
        ariaLabel: 'Mean ' + M.title.toLowerCase() + ' by calendar month and hour of day'
      }),
      table: {
        columns: ['Month'].concat(hourLabels),
        rows: mh.months.map((m, i) => [m].concat(mh.values[i].map(x => nf(x, 1))))
      }
    });

    card(g, {
      width: 'w-6',
      title: M.last_year + ' against the mean, by month and hour',
      sub: 'The departure of the most recent year from the surface beside it, centred on zero, so '
        + 'it can be read for the time of day at which the year differed.',
      render: host => heatmap(host, {
        xLabels: hourLabels, yLabels: mh.months, values: mh.anomaly,
        scale: 'diverging', zLabel: M.last_year + ' minus mean (' + U + ')', maxCell: 30,
        valueFormat: x => vals(x, 2),
        ariaLabel: 'Departure of the most recent year by month and hour'
      }),
      table: {
        columns: ['Month'].concat(hourLabels),
        rows: mh.months.map((m, i) => [m].concat(mh.anomaly[i].map(x =>
          ({ v: nfs(x, 1), cls: x >= 0 ? 'num-warm' : 'num-cold' }))))
      }
    });

    const di = DATA.diurnal;
    const meanCurve = di.x.map((_, i) =>
      di.values.reduce((a, m) => a + m[i], 0) / di.values.length);

    card(g, {
      width: 'w-12',
      title: 'Mean diurnal cycle, one panel per month',
      sub: 'Twelve series is past the point where colour can carry identity, so the months are '
        + 'faceted instead of overplotted. Every panel shares one vertical scale, and the grey curve '
        + 'behind each is the mean over all months.',
      legend: [
        { color: cv('--series-1'), label: 'the month', line: true },
        { color: cv('--band-inner'), label: 'mean over all months', line: true }
      ],
      render: host => smallMultiples(host, {
        x: di.x, reference: meanCurve,
        panels: di.months.map((m, i) => ({ label: m, title: m, values: di.values[i] })),
        ariaLabel: 'Mean diurnal cycle of ' + M.title.toLowerCase() + ', one panel per calendar month'
      }),
      table: {
        columns: ['Hour'].concat(di.months),
        rows: di.x.map((t, i) => [
          String(Math.floor(t)).padStart(2, '0') + ':' + String(Math.round((t % 1) * 60)).padStart(2, '0')
        ].concat(di.values.map(m => nf(m[i], 1))))
      },
      foot: 'Horizontal axis is the hour of day in local time (' + M.resolution + ').'
    });
  }

  /* ---- Thresholds, spells and records ----------------------------------------------------- */

  function sectionThresholds() {
    const g = document.getElementById('g-thresholds');
    const groups = DATA.index_groups || [];

    groups.forEach(group => {
      const ramp = RAMPS[group.ramp] || RAMPS.cold;
      const first = group.items[0];
      card(g, {
        width: 'w-6',
        title: group.title,
        sub: group.sub + ' The counts come from daily statistics of the full series, filled records '
          + 'included.',
        legend: group.items.map((it, i) => ({ color: cv(ramp[i]), label: it.label, line: true })),
        render: host => lineChart(host, {
          aspect: 0.5,
          x: years, yZero: true,
          series: group.items.map((it, i) => ({
            values: col(it.key), color: token(ramp[i]), label: it.label, width: 2, marker: true
          })),
          xTicks: xTicksForYears(host),
          yLabel: 'days per year', yDigits: 0,
          xTooltip: y => String(y), valueFormat: x => nf(x, 0) + ' days',
          ariaLabel: group.title + ' per year'
        }),
        table: {
          columns: ['Year'].concat(group.items.map(it => it.label))
            .concat(['Longest spell (days)', 'Spell start']),
          rows: Y.map(y => [y.year].concat(group.items.map(it => y[it.key]))
            .concat([y[first.key + '_spell'], y[first.key + '_spell_start']]))
        },
        foot: 'A year can collect many such days without ever holding the threshold for a week, '
          + 'which is why the longest uninterrupted spell of "' + first.label + '" is in the table.'
      });
    });

    if (M.growing_season_base !== null && M.growing_season_base !== undefined) {
      card(g, {
        width: 'w-6',
        title: 'Growing season',
        sub: 'Length per year on a ' + nf(M.growing_season_base, 0) + ' ' + U + ' base. The season '
          + 'starts on the first of six consecutive days above the base and ends on the first of six '
          + 'below it after 1 July. Several conventions are in use, so these numbers only compare '
          + 'against numbers computed the same way.',
        legend: [{ color: cv('--series-3'), label: 'season length' }],
        render: host => barChart(host, {
          aspect: 0.5,
          x: years.map(String),
          series: [{ values: col('gsl'), color: token('--series-3'), label: 'length' }],
          xTickEvery: everyNth(host),
          yLabel: 'days', yDigits: 0,
          catLabel: y => 'Growing season ' + y,
          valueFormat: (x, i) => nf(x, 0) + ' days, ' + Y[i].gs_start_label + ' to ' + Y[i].gs_end_label,
          ariaLabel: 'Growing season length per year'
        }),
        table: {
          columns: ['Year', 'Start', 'End', 'Length (days)', 'Growing degree days (' + U + ' d)'],
          rows: Y.map(y => [y.year, y.gs_start_label, y.gs_end_label, y.gsl, nf(y.gdd, 0)])
        }
      });
    }

    /* A new record low is counted against the daily minimum. Where the scale has a hard floor the
       daily minimum is that floor on nearly every day, so after the first one no day can ever set
       another - a series of zeros that looks like a finding. It is dropped instead. */
    const withLows = EX.show_low_halfhour;
    card(g, {
      width: 'w-6',
      title: 'Days setting a new record',
      sub: 'Read forwards: a record is a record against what came before it, not against the whole '
        + 'dataset. ' + M.first_year + ' is left out because by construction almost every day of it '
        + 'sets one. Records necessarily thin out as the record grows, so a late year holding '
        + 'several is the notable case.'
        + (withLows ? '' : ' Only record highs are counted: the low end of this scale is a floor '
          + 'the record reaches routinely.'),
      legend: [{ color: cv('--pole-warm'), label: 'new record highs' }]
        .concat(withLows ? [{ color: cv('--pole-cold'), label: 'new record lows' }] : []),
      render: host => barChart(host, {
        aspect: 0.5,
        x: years.slice(1).map(String),
        mode: 'grouped',
        series: [
          { values: Y.slice(1).map(y => y.rec_high), color: token('--pole-warm'), label: 'new record highs' }
        ].concat(withLows
          ? [{ values: Y.slice(1).map(y => y.rec_low), color: token('--pole-cold'), label: 'new record lows' }]
          : []),
        xTickEvery: everyNth(host),
        yLabel: 'days', yDigits: 0,
        valueFormat: x => nf(x, 0) + ' days',
        ariaLabel: 'Days setting a new daily record per year'
      }),
      table: {
        columns: ['Year', 'New record highs'].concat(withLows ? ['New record lows'] : []),
        rows: Y.slice(1).map(y => [y.year, { v: y.rec_high, cls: 'num-warm' }]
          .concat(withLows ? [{ v: y.rec_low, cls: 'num-cold' }] : []))
      },
      foot: 'From measured daily extremes only.'
    });

    if (!groups.length) {
      document.getElementById('s-thresholds').textContent = 'Records';
      const link = document.querySelector('.sectionnav a[href="#s-thresholds"]');
      if (link) link.textContent = 'Records';
    }
  }

  /* ---- Coverage and provenance ------------------------------------------------------------ */

  function sectionCoverage() {
    const g = document.getElementById('g-coverage');
    const cov = DATA.coverage;

    card(g, {
      width: 'w-6',
      title: M.has_fill_flag ? 'How each year was filled' : 'What is missing from each year',
      sub: 'Records that are not a measurement, per year'
        + (M.has_fill_flag ? ', by what stands behind them instead. ' : '. ')
        + 'Every statistic on this page is computed on the full series, so this says how far each '
        + 'year can be read as a measurement.',
      legend: cov.methods.map((m, i) => ({ color: cv('--series-' + (i + 1)), label: m })),
      render: host => barChart(host, {
        aspect: 0.5,
        x: cov.years.map(String),
        mode: 'stacked',
        series: cov.methods.map((m, i) => ({
          values: cov.values.map(row => row[i]), color: token('--series-' + (i + 1)), label: m
        })),
        xTickEvery: everyNth(host),
        yLabel: 'records', yDigits: 0,
        catLabel: y => y + ' · ' + nf(Y[years.indexOf(+y)].filled, 1) + ' % not measured',
        valueFormat: x => nf(x, 0) + ' records',
        ariaLabel: 'Records that are not a measurement, per year'
      }),
      table: {
        columns: ['Year', 'Records'].concat(cov.methods)
          .concat(['Not measured (%)', 'Longest gap (h)']),
        rows: cov.years.map((y, i) => [y, Y[i].records.toLocaleString('en-GB')]
          .concat(cov.values[i].map(x => nf(x, 0)))
          .concat([nf(Y[i].filled, 1), nf(Y[i].longest_gap_h, 1)]))
      },
      foot: 'A year interrupted in many short gaps is not the same as a year with one long outage, '
        + 'so the longest uninterrupted run is listed in the table.'
    });

    const src = DATA.source;
    if (src) {
      /* Codes that never occur in this period are dropped rather than drawn as an empty stack
         segment. The slot each surviving code gets is decided once, here, so the legend and the
         chart cannot drift apart when a code disappears from the middle of the list. */
      const used = src.labels.map((_, i) => i).filter(i => src.values.some(row => row[i] > 0));
      const slotName = i => '--series-' + (used.indexOf(i) + 1);

      card(g, {
        width: 'w-6',
        title: 'Which instrument each year came from',
        sub: 'The provenance flag says which sensor or acquisition chain produced each record. A '
          + 'year split between two codes cannot be compared with an undivided one without the '
          + 'homogenisation.',
        legend: used.map(i => ({ color: cv(slotName(i)), label: src.full[i] })),
        render: host => barChart(host, {
          aspect: 0.5,
          x: src.years.map(String),
          mode: 'stacked',
          series: used.map(i => ({
            values: src.values.map(row => row[i]), color: token(slotName(i)), label: src.labels[i]
          })),
          xTickEvery: everyNth(host),
          yLabel: 'share of the year (%)', yDigits: 0, yDomain: [0, 104],
          valueFormat: x => nf(x, 1) + ' %',
          ariaLabel: 'Share of each year by instrument era'
        }),
        table: {
          columns: ['Year'].concat(used.map(i => src.labels[i] + ' (%)')),
          rows: src.years.map((y, r0) => [y].concat(used.map(i => nf(src.values[r0][i], 1))))
        }
      });
    }

    card(g, {
      width: 'w-12',
      title: 'Where the missing records sit',
      sub: 'Share of each month that is not a measurement. It locates the outages behind the '
        + 'coverage chart: a month drawn dark cannot be read as a measurement.',
      render: host => heatmap(host, {
        xLabels: DATA.monthly.months, yLabels: DATA.monthly.years.map(String),
        values: DATA.monthly.filled, scale: 'sequential', min: 0,
        zLabel: 'not measured (%)', valueFormat: x => nf(x, 1) + ' %',
        scaleFormat: x => nf(x, 0) + ' %', maxCell: 40,
        ariaLabel: 'Share of each month that is not a measurement'
      }),
      table: {
        columns: ['Year'].concat(DATA.monthly.months),
        rows: DATA.monthly.years.map((y, i) => [y].concat(DATA.monthly.filled[i].map(x => nf(x, 1))))
      }
    });
  }

  /* ---- Reference station ------------------------------------------------------------------ */

  function sectionReference() {
    const g = document.getElementById('g-reference');
    const R = DATA.reference;
    if (!R) { dropSection('s-reference'); return; }

    const idx = R.dates.map((_, i) => i);
    const breakIdx = R.break_year ? R.dates.findIndex(d => +d.slice(0, 4) === R.break_year) : -1;
    const slot = i => '--series-' + (i + 1);

    card(g, {
      width: R.steps ? 'w-8' : 'w-12',
      title: 'Residual against ' + R.station,
      sub: 'The station is ' + R.distance_km + ' km from the tower at ' + R.elevation_m
        + ' m a.s.l. and is operated by a different institution, so the difference against it '
        + 'removes the weather and leaves the instruments. The elevation difference means a constant '
        + 'offset is expected; what matters is whether that offset stays constant.'
        + (R.note ? ' ' + R.note : ''),
      legend: R.series.map((s, i) => ({
        color: cv(slot(i)), label: s.label + ', monthly mean and 12-month rolling median', line: true
      })),
      render: host => lineChart(host, {
        aspect: 0.42,
        margin: { top: 12, right: 52, bottom: 34, left: 46 },  // room for the endpoint labels
        x: idx,
        series: [].concat(
          R.series.map((s, i) => ({
            values: s.values, color: token(slot(i)), label: s.label + ' (monthly)',
            width: 0.8, opacity: 0.35
          })),
          R.series.map((s, i) => ({
            values: s.smooth, color: token(slot(i)), label: s.label + ' (rolling median)',
            width: 2.4, directLabel: s.label
          }))
        ),
        marks: breakIdx >= 0 ? [{ x: breakIdx, label: 'hardware change ' + R.break_year }] : [],
        xTicks: idx.filter(i => R.dates[i].slice(5) === '01' && +R.dates[i].slice(0, 4) % 3 === 0)
          .map(i => ({ v: i, label: R.dates[i].slice(0, 4) })),
        yLabel: 'product minus reference (' + U + ')', yDigits: 1,
        xTooltip: i => R.dates[i], valueFormat: x => vals(x, 2),
        ariaLabel: 'Residual of the product against the reference station'
      }),
      table: {
        columns: ['Year', 'Mean residual (' + U + ')']
          .concat(R.split ? ['Night (' + U + ')', 'Day (' + U + ')'] : [])
          .concat(['SD (' + U + ')', 'Overlapping half-hours']),
        rows: R.yearly.map(y => [y.year, nfs(y.mean, 2)]
          .concat(R.split ? [nfs(y.night, 2), nfs(y.day, 2)] : [])
          .concat([nf(y.sd, 2), y.n.toLocaleString('en-GB')]))
      },
      foot: R.n.toLocaleString('en-GB') + ' overlapping measured half-hours, ' + R.start + ' to '
        + R.stop + ' · r = ' + nf(R.correlation, 4) + ' · mean residual '
        + vals(R.residual_mean, 2) + ' ± ' + val(R.residual_sd, 2) + ' SD.'
    });

    if (R.steps) {
      card(g, {
        width: 'w-4',
        title: 'The step across the hardware change',
        sub: 'Three complete years either side of ' + R.break_year + ', so an outage at the '
          + 'changeover does not sit inside a compared window. This is the residual step the '
          + 'exported product carries.',
        table: {
          columns: ['Window', 'Before (' + U + ')', 'After (' + U + ')', 'Step (' + U + ')'],
          rows: R.steps.map(s => [s.window, nfs(s.before, 2), nfs(s.after, 2),
          { v: nfs(s.step, 2), cls: Math.abs(s.step) > 0.2 ? 'num-warm' : '' }])
        },
        foot: 'A step that survives the homogenisation is a limitation of the product, not of the '
          + 'comparison; read it before comparing daily statistics across the change.'
      });
    }
  }

  /* ---- Tables ----------------------------------------------------------------------------- */

  function sectionTables() {
    const g = document.getElementById('g-tables');

    /* The yearly table is assembled from whatever the variable actually has, so a product without
       threshold days or a growing season simply carries fewer columns. */
    const columns = ['Year', cap(AGG) + ' (' + U + ')', 'Anomaly (' + U + ')', 'Rank',
      'Measured minimum (' + U + ')', 'Measured maximum (' + U + ')'];
    const cells = [
      y => nf(y.mean, 2),
      y => ({ v: nfs(y.anomaly, 2), cls: y.anomaly >= 0 ? 'num-warm' : 'num-cold' }),
      y => y.rank,
      y => ({ v: nf(y.min, 1), cls: 'num-cold' }),
      y => ({ v: nf(y.max, 1), cls: 'num-warm' })
    ];
    (DATA.index_groups || []).forEach(group => group.items.forEach(it => {
      columns.push(it.label);
      cells.push(y => y[it.key]);
    }));
    if (M.growing_season_base !== null && M.growing_season_base !== undefined) {
      columns.push('Growing season (days)', 'GDD (' + U + ' d)');
      cells.push(y => y.gsl, y => nf(y.gdd, 0));
    }
    columns.push('New highs');
    cells.push(y => y.rec_high);
    if (EX.show_low_halfhour) { columns.push('New lows'); cells.push(y => y.rec_low); }
    columns.push('Not measured (%)');
    cells.push(y => nf(y.filled, 1));

    card(g, {
      width: 'w-12',
      title: 'Year by year',
      sub: 'Everything on this page, per year, in one table. Extremes are measured values; the '
        + AGG + ', the counts and the indices use the full series.',
      table: {
        columns: columns,
        rows: Y.map(y => [y.year].concat(cells.map(f => f(y))))
      }
    });

    const bothHH = EX.show_low_halfhour;
    card(g, {
      width: 'w-6',
      title: bothHH ? 'The ' + EX.high_label + ' and ' + EX.low_label + ' half-hours'
        : 'The ' + EX.high_label + ' half-hours',
      sub: 'Measured records only. Neighbouring windows of a single episode fill this list, which '
        + 'is what an episode looks like at this resolution. The averaging window is given rather '
        + 'than the timestamp, because the product is stored on TIMESTAMP_MIDDLE.'
        + (bothHH ? '' : ' The other end of the scale is a floor this variable reaches routinely, '
          + 'so it is not listed.'),
      table: {
        columns: ['Rank', cap(EX.high_label) + ' — averaging window', U]
          .concat(bothHH ? [cap(EX.low_label) + ' — averaging window', U] : []),
        rows: EX.high_halfhours.map((w, i) => [i + 1, w.window,
        { v: nf(w.value, 1), cls: 'num-warm' }].concat(bothHH
          ? [EX.low_halfhours[i].window, { v: nf(EX.low_halfhours[i].value, 1), cls: 'num-cold' }]
          : []))
      },
      foot: EX.inside_measured
        ? 'The filled values stay inside the measured range.'
        : 'Note: the full series reaches outside the measured range; those values are model results.'
    });

    const dayWord = M.agg === 'sum' ? 'daily total' : 'daily mean';
    const bothDays = EX.show_low_day;
    card(g, {
      width: 'w-6',
      title: bothDays ? 'The ' + EX.high_label + ' and ' + EX.low_label + ' days'
        : 'The ' + EX.high_label + ' days',
      sub: 'By ' + dayWord + ', computed over all records of the day, filled ones included — so the '
        + 'filled share is listed beside each. A day with a large filled share is a model result as '
        + 'much as a measurement.'
        + (bothDays ? '' : ' The other end of the scale is a floor this variable reaches on many '
          + 'days, so it is not listed.'),
      table: {
        columns: ['Rank', cap(EX.high_label) + ' day', U, 'Filled (%)']
          .concat(bothDays ? [cap(EX.low_label) + ' day', U, 'Filled (%)'] : []),
        rows: EX.high_days.map((d, i) => [i + 1, d.date, { v: nf(d.value, 1), cls: 'num-warm' },
        nf(d.filled, 0)].concat(bothDays
          ? [EX.low_days[i].date, { v: nf(EX.low_days[i].value, 1), cls: 'num-cold' },
          nf(EX.low_days[i].filled, 0)]
          : []))
      }
    });
  }

  /* ------------------------------------------------------------------------------------------
     Theme and navigation
     ------------------------------------------------------------------------------------------ */

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

    btn.addEventListener('click', () => {
      const next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('meteo-dashboard-theme', next); } catch (e) { /* private mode */ }
      sync();
      renderAll();
    });

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (root.getAttribute('data-theme') !== 'auto') return;
      sync();
      renderAll();
    });
    sync();
  }

  function setupNav() {
    const links = Array.from(document.querySelectorAll('.sectionnav a'));
    const targets = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
    if (!targets.length) return;
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        links.forEach(a => a.classList.toggle('active',
          a.getAttribute('href') === '#' + e.target.id));
      });
    }, { rootMargin: '-72px 0px -70% 0px' });
    targets.forEach(t => observer.observe(t));
  }

  /* ------------------------------------------------------------------------------------------
     Go
     ------------------------------------------------------------------------------------------ */

  header();
  tiles();
  sectionRecord();
  sectionYears();
  sectionSeasons();
  sectionThresholds();
  sectionCoverage();
  sectionReference();
  sectionTables();
  setupTheme();
  setupNav();
  renderAll();

  let resizeTimer = null;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(renderAll, 140);
  });
})();
