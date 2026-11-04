"""Figures of the docs page L3.3_Constraints.md, drawn from the outputs of the USTAR detection notebook.

Reads the tables that USTAR_THRESHOLD_DETECTION_2004-2026.09.ipynb shows in its committed outputs, so it
needs neither the external data folder nor a rerun of the notebook. Rerun this script after the notebook.
Writes three PNG files to docs/images/.

Usage, from the repository root:  python workflow/30_FLUX_POST-PROCESSING_CHAIN/USTAR_THRESHOLD_DETECTION_docs_figures.py
"""
import html
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
NB = ROOT / 'workflow' / '30_FLUX_POST-PROCESSING_CHAIN' / 'USTAR_THRESHOLD_DETECTION_2004-2026.09.ipynb'
OUT = ROOT / 'docs' / 'images'

# Thresholds (m s-1), as declared in the detection notebook (USTAR_THRESHOLDS, USTAR_THRESHOLDS_FP1)
FP2 = {'LI-7200': [0.4155, 0.5264, 0.6472], 'LI-7500': [0.3182, 0.4350, 0.5459]}
FP1 = [0.2716, 0.3036, 0.3397]

INK, MUTED, GRID = '#1F2623', '#5A6460', '#E4E7E4'
TA_COLORS = ['#F2C18A', '#E59A55', '#C96F2B', '#9C4A16', '#66290A']  # one hue, light to dark
SEASON_COLORS = {'May-Oct': '#B5561A', 'Nov-Apr': '#2B6CA3'}
BAND = '#2E6A4E'

plt.rcParams.update({'font.size': 10, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.spines.top': False,
                     'axes.spines.right': False, 'savefig.dpi': 150, 'figure.dpi': 100})


def table_after(nb, heading_id):
    """Rows of the first HTML table in the outputs of the cell after the markdown cell `heading_id`."""
    ids = [c.get('id') for c in nb['cells']]
    cell = nb['cells'][ids.index(heading_id) + 1]
    for o in cell.get('outputs', []):
        h = o.get('data', {}).get('text/html')
        if h:
            rows = re.findall(r'<tr>(.*?)</tr>', ''.join(h), re.S)
            return [[html.unescape(re.sub('<.*?>', '', x)).strip()
                     for x in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)] for r in rows]
    raise ValueError(f'no table after {heading_id}')


def mid(label):
    lo, hi = (float(v) for v in label.split('-'))
    return (lo + hi) / 2


def thresholds(ax, fp2, ymax_label=True):
    ax.axvspan(fp2[0], fp2[2], color=BAND, alpha=0.12, lw=0)
    ax.axvline(fp2[1], color=BAND, lw=1.5)
    ax.axvline(FP1[1], color=MUTED, lw=1.2, ls='--')
    if ymax_label:
        y = ax.get_ylim()[1]
        ax.text(fp2[1] + 0.01, y, 'FP2026.2\nCUT_50', va='top', ha='left', fontsize=8.5, color=BAND)
        ax.text(FP1[1] - 0.01, y, 'FP2026.1\nCUT_50', va='top', ha='right', fontsize=8.5, color=MUTED)


def fig_nee_by_ta(nb):
    rows = table_after(nb, 'ustd-curve_tab_md')
    header, body = rows[0], [r for r in rows[2:] if r[0] != '1.2-3.0']
    x = [mid(r[0]) for r in body]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    for ax, (name, first) in zip(axes, [('LI-7200 (2016-2025)', 1), ('LI-7500 (2004-2017)', 7)]):
        for k in range(5):
            col = first + k
            label = header[col].split(', TA ')[1]
            ax.plot(x, [float(r[col]) for r in body], color=TA_COLORS[k], lw=2, marker='o', ms=4, label=label)
        ax.set_title(name, loc='left', fontsize=10.5, color=INK)
        ax.set_xlabel('USTAR (m s$^{-1}$)')
        ax.grid(axis='y', color=GRID, lw=0.8)
        ax.set_xlim(0, 1.2)
        ax.set_ylim(-0.5, 11)
        thresholds(ax, FP2[name.split(' ')[0]])
    axes[0].set_ylabel('mean night-time NEE (µmol m$^{-2}$ s$^{-1}$)')
    axes[1].legend(title='air temperature', frameon=False, loc='lower right', fontsize=8.5, title_fontsize=8.5)
    fig.tight_layout()
    fig.savefig(OUT / 'USTAR_night_NEE_by_TA_class.png')
    plt.close(fig)


def fig_ratio_reco_dt(nb):
    rows = table_after(nb, '49b947af')
    data, analyser, season = {}, None, None
    for r in rows[1:]:
        if len(r) == 7:
            analyser, season = r[0], r[1]
        elif len(r) == 6:
            season = r[0]
        bin_label, ratio = r[-5], r[-1]
        if bin_label == '1.2-3.0':
            continue
        data.setdefault((analyser, season), []).append((mid(bin_label), float(ratio)))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    for ax, name in zip(axes, ['LI-7200', 'LI-7500']):
        for season, color in SEASON_COLORS.items():
            pts = data[(name, season)]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=2, marker='o', ms=4, label=season)
        ax.axhline(1, color=INK, lw=1)
        ax.set_title(name, loc='left', fontsize=10.5, color=INK)
        ax.set_xlabel('USTAR (m s$^{-1}$)')
        ax.grid(axis='y', color=GRID, lw=0.8)
        ax.set_xlim(0, 1.2)
        ax.set_ylim(-0.1, 1.7)
        thresholds(ax, FP2[name])
    axes[0].set_ylabel('night-time NEE / RECO_DT')
    axes[1].legend(frameon=False, loc='lower right', fontsize=8.5)
    fig.tight_layout()
    fig.savefig(OUT / 'USTAR_night_NEE_vs_RECO_DT.png')
    plt.close(fig)


def fig_thresholds(nb):
    rows = table_after(nb, 'ustd-det_cut_md')
    det, record = {}, None
    for r in rows[2:]:
        if len(r) == 6:
            record, r = r[0], r[1:]
        det[(record, r[0])] = [float(v) for v in r[1:4]]
    flx = table_after(nb, 'ustd-flx_thr_md')[2:]
    vut = {int(r[0]): float(r[1]) for r in flx}
    names = {'oneflux_mp': 'moving point', 'oneflux_cp': 'change point', 'oneflux': 'ONEFlux (both)',
             'reddyproc': 'REddyProc'}
    items = [('FP2026.1 (REddyProc, 30 classes)', FP1, MUTED),
             ('FP2026.2 LI-7500: own record, moving point', FP2['LI-7500'], BAND),
             ('FP2026.2 LI-7200: own record, moving point', FP2['LI-7200'], BAND),
             ('merged record, moving point (not used)', det[('merged record', 'oneflux_mp')], MUTED)]
    for rec in ['LI-7200', 'LI-7500']:
        for m in ['oneflux_cp', 'oneflux', 'reddyproc']:
            items.append((f'{rec} record, {names[m]}', det[(rec, m)], INK))
    lo7500 = [v for y, v in vut.items() if y <= 2015]
    lo7200 = [v for y, v in vut.items() if y >= 2016]
    items.append(('FLUXNET VUT_REF, 2004-2015 (min-max)', [min(lo7500), None, max(lo7500)], '#6F7FA6'))
    items.append(('FLUXNET VUT_REF, 2016-2024 (min-max)', [min(lo7200), None, max(lo7200)], '#6F7FA6'))
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.axvspan(0.9, 1.0, color=MUTED, alpha=0.15, lw=0)
    ax.text(0.95, -0.9, 'night-time NEE\nincreases up to here', ha='center', va='bottom', fontsize=8.5, color=MUTED)
    for i, (label, (lo, med, hi), color) in enumerate(items):
        y = len(items) - 1 - i
        ax.plot([lo, hi], [y, y], color=color, lw=4, solid_capstyle='round', alpha=0.85)
        if med is not None:
            ax.plot(med, y, 'o', color='white', ms=7, mec=color, mew=2)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([it[0] for it in reversed(items)], fontsize=9)
    ax.set_xlim(0.15, 1.05)
    ax.set_ylim(-1, len(items))
    ax.set_xlabel('USTAR threshold (m s$^{-1}$): CUT_16 to CUT_84 (REddyProc: 5th to 95th percentile), dot = median')
    ax.grid(axis='x', color=GRID, lw=0.8)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    fig.tight_layout()
    fig.savefig(OUT / 'USTAR_thresholds_by_method.png')
    plt.close(fig)


if __name__ == '__main__':
    nb = json.loads(NB.read_text(encoding='utf-8'))
    fig_nee_by_ta(nb)
    fig_ratio_reco_dt(nb)
    fig_thresholds(nb)
    print('written to', OUT)
