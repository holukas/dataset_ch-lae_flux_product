"""Raw-data diagnostics of the LI-7500 (IRGA75) for summer midday, 2005-2016.

Reads the 20 Hz raw files of the EddyPro runs and writes one row per 30-minute block to
`30_FLUX_POST-PROCESSING_CHAIN/IRGA75/RAW_DATA_DIAGNOSTICS_IRGA75_SUMMERS.parquet` in the external
data folder. The notebook `RAW_DATA_DIAGNOSTICS_IRGA75_SUMMERS.ipynb` beside this script reads
that table; it does not read the raw data.

The raw files are a hard dependency of this script. They are not shared with the repository and
not part of the external data folder; their location is `RAWROOT`.

Selection: June and July, blocks starting 11:00 to 14:30 (CET, the time of the file names), i.e.
11:00-15:00. Per block, in this order:

1. Sample screening: missing values, absolute limits, the diagnostic bits of the LI-7500 (chopper,
   detector, PLL and sync, `GA_DIAG_CODE`), and spikes (a simplified test after Vickers and Mahrt
   1997: deviation from a centred 5-minute running mean by more than 3.5 standard deviations, 5 for
   w, in runs of at most 3 samples). Flagged samples are interpolated linearly. A block is skipped
   when more than 10 % of its samples are flagged in any variable, when its mean AGC exceeds 70 %,
   or when the raw file does not cover it.
2. Double rotation and block averaging.
3. Covariance of w with CO2, H2O and sonic temperature as a function of lag, -2 to +3 s.
4. Cospectra of w with CO2 and H2O (shifted by the lag EddyPro used) and with sonic temperature,
   and the power spectra of w, Ts, CO2 and H2O, summed in log-spaced frequency bins.
5. Instrument noise from the autocovariance at small lags (Lenschow et al. 2000): white noise
   adds to the autocovariance at lag 0 only, so the noise variance is the variance minus the
   autocovariance extrapolated to lag 0. Three estimates are stored: a straight line through
   lags 1-3 samples (the main estimate), the inertial-subrange form a - b tau^(2/3) through lags
   1-5, and the variance minus the autocovariance at lag 1 (an upper bound).
6. Drop-out and signal diagnostics: repeated values, the AGC, the data size and status code.

Run from the repository root:

    uv run python workflow/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/raw_data_diagnostics.py
    uv run python workflow/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/raw_data_diagnostics.py --test OUT.parquet

`--test` processes two days of 2006 only and writes to the given path.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
import pandas as pd
import pyarrow.csv as pacsv

# --- Sources and output ------------------------------------------------------------------------
RAWROOT = r"F:\CURRENT\LAE_FP2026"
DATADIR = r"F:\Sync\luhk_work\dev-data\datasets-data\dataset_ch-lae_flux_product-data\workflow"
EPFILE = rf"{DATADIR}\30_FLUX_POST-PROCESSING_CHAIN\IRGA75\01_FPPC_IRGA75_INPUT_OPCO_2004-2017_2019.parquet"
OUTFILE = rf"{DATADIR}\30_FLUX_POST-PROCESSING_CHAIN\IRGA75\RAW_DATA_DIAGNOSTICS_IRGA75_SUMMERS.parquet"

# Setup period folder per year. Each holds the raw files of a whole year (2005_1+4 holds 2005).
PERIODS = {2005: '2005_1+4', 2006: '2006', 2007: '2007', 2010: '2010', 2011: '2011', 2012: '2012',
           2016: '2016_2+3_IRGA75'}
MONTHS = (6, 7)
FIRST_BLOCK, LAST_BLOCK = '11:00', '14:30'   # block starts, CET

# --- Raw data ----------------------------------------------------------------------------------
FS = 20                     # Hz
N_BLOCK = 30 * 60 * FS      # samples per 30-minute block
FILE_HOURS = 6
COLS = {'U_[HS50-B]': 'u', 'V_[HS50-B]': 'v', 'W_[HS50-B]': 'w', 'T_SONIC_[HS50-B]': 'ts',
        'DATA_SIZE_[IRGA75-A]': 'data_size', 'STATUS_CODE_[IRGA75-A]': 'status',
        'GA_DIAG_CODE_[IRGA75-A]': 'diag', 'AGC_[IRGA75-A]': 'agc',
        'H2O_CONC_[IRGA75-A]': 'h2o', 'CO2_CONC_[IRGA75-A]': 'co2',
        'T_BOX_[IRGA75-A]': 't_box', 'PRESS_BOX_[IRGA75-A]': 'p_box', 'COOLER_V_[IRGA75-A]': 'cooler_v'}
NULLS = ['NaN', 'nan', 'NAN', '-9999', '-9999.0', '-9999.00', '']

# --- Screening ---------------------------------------------------------------------------------
# Absolute limits of the EddyPro runs. The gas limits there are mole fractions (CO2 200-900
# umol mol-1, H2O 0-40 mmol mol-1); with a molar density of air of 36-42 mol m-3 they become the
# density limits below (mmol m-3).
LIMITS = {'u': (-30, 30), 'v': (-30, 30), 'w': (-5, 5), 'ts': (233.15, 323.15),
          'co2': (7.2, 37.8), 'h2o': (0.0, 1680.0)}
SPIKE_SD = {'u': 3.5, 'v': 3.5, 'w': 5.0, 'ts': 3.5, 'co2': 3.5, 'h2o': 3.5}
SPIKE_WIN = 5 * 60 * FS     # centred running window of the spike test (samples)
SPIKE_MAXRUN = 3            # longer runs are not spikes and are left in place
MAX_FLAGGED = 0.10          # share of flagged samples above which a block is skipped
MAX_AGC = 70.0              # % : block mean AGC above which a block is skipped
DIAG_OK_MASK = 0xF0         # LI-7500 diagnostic byte: bits 4-7 (sync, PLL, detector, chopper) are 1 when OK

# --- Analysis ----------------------------------------------------------------------------------
LAG_MIN, LAG_MAX = -40, 60          # lag scan, samples (-2 to +3 s)
WIN_MIN, WIN_MAX = 1, 15            # EddyPro lag window, samples (0.05-0.75 s)
LAGS = np.arange(LAG_MIN, LAG_MAX + 1)
SHIFT_MAX = 20                      # samples cut from the end of w for the lag-shifted cospectra
M_SPEC = N_BLOCK - SHIFT_MAX        # length of the series of the cospectra
N_BINS = 30
FREQ = np.arange(1, M_SPEC // 2 + 1) * FS / M_SPEC
BIN_EDGES = np.logspace(np.log10(FREQ[0] * 0.999), np.log10(FS / 2 * 1.001), N_BINS + 1)
BIN_CENTRES = np.sqrt(BIN_EDGES[:-1] * BIN_EDGES[1:])
BIN_INDEX = np.digitize(FREQ, BIN_EDGES) - 1
NOISE_TAUS = np.arange(1, 6)        # samples, Lenschow et al. (2000)
Z_MEAS = 47.0 - 24.79               # m, measurement height minus displacement height
KARMAN, GRAV = 0.41, 9.81


def raw_file_index(year):
    """Start time and path of every raw file of the period of `year`."""
    pattern = os.path.join(RAWROOT, PERIODS[year], '2-FLUXRUN', '**', '1-0_rawdata_files_ascii', 'CH-LAE_*.csv')
    files = glob.glob(pattern, recursive=True)
    out = {}
    for f in files:
        m = re.search(r'CH-LAE_(\d{12})\.csv$', f)
        if m:
            out[pd.Timestamp(datetime_str(m.group(1)))] = f
    return pd.Series(out).sort_index()


def datetime_str(s):
    return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]}:{s[10:12]}"


def read_raw(path):
    names = open(path, encoding='latin1').readline().strip().split(',')
    tb = pacsv.read_csv(path, read_options=pacsv.ReadOptions(skip_rows=3, column_names=names),
                        convert_options=pacsv.ConvertOptions(include_columns=list(COLS), null_values=NULLS,
                                                             strings_can_be_null=True))
    d = tb.to_pandas().rename(columns=COLS)
    return {k: d[k].to_numpy(dtype=float) for k in COLS.values()}


def running_mean_std(x, win):
    """Centred running mean and standard deviation, ignoring NaN."""
    n = len(x)
    ok = np.isfinite(x)
    x0 = np.where(ok, x - np.nanmean(x), 0.0)
    c1 = np.concatenate([[0.0], np.cumsum(x0)])
    c2 = np.concatenate([[0.0], np.cumsum(x0 * x0)])
    cn = np.concatenate([[0], np.cumsum(ok)])
    i = np.arange(n)
    lo, hi = np.clip(i - win // 2, 0, n), np.clip(i + win // 2 + 1, 0, n)
    m = np.maximum(cn[hi] - cn[lo], 1)
    mean = (c1[hi] - c1[lo]) / m
    var = np.maximum((c2[hi] - c2[lo]) / m - mean ** 2, 0.0)
    return mean + np.nanmean(x), np.sqrt(var)


def run_lengths(mask):
    """Start and length of the runs of True in a boolean array."""
    d = np.diff(np.concatenate([[0], mask.astype(np.int8), [0]]))
    starts, ends = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    return starts, ends - starts


def despike(x, sd):
    """Set spikes to NaN. Returns the number of spike samples and of samples in longer runs."""
    mean, std = running_mean_std(x, SPIKE_WIN)
    out = np.isfinite(x) & (np.abs(x - mean) > sd * std)
    starts, lens = run_lengths(out)
    n_spike = n_long = 0
    for s, L in zip(starts, lens):
        if L <= SPIKE_MAXRUN:
            x[s:s + L] = np.nan
            n_spike += L
        else:
            n_long += L
    return n_spike, n_long


def interpolate(x):
    bad = ~np.isfinite(x)
    if bad.any() and (~bad).sum() > 1:
        idx = np.arange(len(x))
        x[bad] = np.interp(idx[bad], idx[~bad], x[~bad])
    return x


def noise_variance(acov):
    """Noise variance from the autocovariance at lags 0..5 (Lenschow et al. 2000).

    Returns the estimates from a straight line through lags 1-3, from the form a - b tau^(2/3)
    through lags 1-5, and the upper bound acov(0) - acov(1).
    """
    lin = np.polyfit(NOISE_TAUS[:3], acov[NOISE_TAUS[:3]], 1)[1]
    p23 = np.polyfit(NOISE_TAUS ** (2 / 3), acov[NOISE_TAUS], 1)[1]
    return acov[0] - lin, acov[0] - p23, acov[0] - acov[1]


def binned(values):
    return np.bincount(BIN_INDEX, weights=values, minlength=N_BINS)[:N_BINS]


def process_block(raw, i0, t0, lag_used):
    """All diagnostics of the block that starts at sample i0 of the raw arrays."""
    rec = {'TIMESTAMP_START': t0, 'TIMESTAMP_MIDDLE': t0 + pd.Timedelta('15min'), 'skipped': False,
           'skip_reason': ''}
    seg = {k: v[i0:i0 + N_BLOCK].copy() for k, v in raw.items()}

    # --- Analyser status, before screening ---
    diag = seg['diag']
    agc = seg['agc']
    rec['agc_mean'] = np.nanmean(agc)
    rec['agc_max'] = np.nanmax(agc)
    rec['agc_above70_share'] = np.mean(agc > MAX_AGC)
    diag_bad = ~np.isfinite(diag) | ((np.nan_to_num(diag).astype(np.int64) & DIAG_OK_MASK) != DIAG_OK_MASK)
    rec['diag_bad_share'] = diag_bad.mean()
    rec['agc_from_diag_mean'] = np.nanmean((np.nan_to_num(diag).astype(np.int64) & 0x0F) * 6.25)
    rec['status_nonzero_share'] = np.mean(np.nan_to_num(seg['status']) != 0)
    _st = seg['status'][np.isfinite(seg['status']) & (seg['status'] != 0)]
    rec['status_nonzero_mode'] = float(pd.Series(_st).mode().iloc[0]) if len(_st) else np.nan
    _ds = seg['data_size'][np.isfinite(seg['data_size'])]
    rec['data_size_mode'] = float(pd.Series(_ds).mode().iloc[0]) if len(_ds) else np.nan
    rec['data_size_other_share'] = np.mean(seg['data_size'] != rec['data_size_mode'])
    for k in ('t_box', 'p_box', 'cooler_v'):
        rec[f'{k}_median'] = np.nanmedian(seg[k])

    # --- Drop-outs: repeated (held) values and the resolution of the gas readings ---
    for k in ('co2', 'h2o', 'w', 'ts'):
        x = seg[k]
        dx = np.diff(x)
        rec[f'{k}_repeat_share'] = np.mean(dx == 0)
        _, lens = run_lengths(np.concatenate([[False], dx == 0]))
        rec[f'{k}_repeat_maxrun'] = int(lens.max()) if len(lens) else 0
        nz = np.abs(dx[np.isfinite(dx) & (dx != 0)])
        rec[f'{k}_resolution'] = nz.min() if len(nz) else np.nan

    # --- Screening ---
    flagged = {}
    for k in ('u', 'v', 'w', 'ts', 'co2', 'h2o'):
        x = seg[k]
        missing = ~np.isfinite(x)
        lo, hi = LIMITS[k]
        outside = np.isfinite(x) & ((x < lo) | (x > hi))
        bad = missing | outside
        if k in ('co2', 'h2o'):
            bad |= diag_bad
        x[bad] = np.nan
        rec[f'{k}_missing'] = int(missing.sum())
        rec[f'{k}_abslim'] = int(outside.sum())
        rec[f'{k}_diagflag'] = int((diag_bad & ~missing & ~outside).sum()) if k in ('co2', 'h2o') else 0
        n_spike, n_long = despike(x, SPIKE_SD[k])
        rec[f'{k}_spikes'] = n_spike
        rec[f'{k}_outlier_runs'] = n_long
        flagged[k] = int((~np.isfinite(x)).sum())
        rec[f'{k}_flagged'] = flagged[k]
    worst = max(flagged.values()) / N_BLOCK
    reasons = []
    if worst > MAX_FLAGGED:
        reasons.append(f'flagged samples above {100 * MAX_FLAGGED:.0f} %')
    if not rec['agc_mean'] <= MAX_AGC:
        reasons.append(f'mean AGC above {MAX_AGC:.0f} %')
    if reasons:
        rec['skipped'] = True
        rec['skip_reason'] = '; '.join(reasons)
        return rec
    for k in ('u', 'v', 'w', 'ts', 'co2', 'h2o'):
        seg[k] = interpolate(seg[k])

    # --- Double rotation ---
    u, v, w = seg['u'], seg['v'], seg['w']
    yaw = np.arctan2(v.mean(), u.mean())
    u1 = u * np.cos(yaw) + v * np.sin(yaw)
    v1 = -u * np.sin(yaw) + v * np.cos(yaw)
    pitch = np.arctan2(w.mean(), u1.mean())
    u2 = u1 * np.cos(pitch) + w * np.sin(pitch)
    w2 = -u1 * np.sin(pitch) + w * np.cos(pitch)
    rec['wind_speed'] = u2.mean()
    rec['pitch_deg'] = np.degrees(pitch)
    up, vp, wp = u2 - u2.mean(), v1 - v1.mean(), w2 - w2.mean()
    s = {'w': wp, 'ts': seg['ts'] - seg['ts'].mean(), 'co2': seg['co2'] - seg['co2'].mean(),
         'h2o': seg['h2o'] - seg['h2o'].mean()}
    rec['ts_mean'] = seg['ts'].mean()
    rec['co2_mean'] = seg['co2'].mean()
    rec['h2o_mean'] = seg['h2o'].mean()
    cov_uw, cov_vw = np.mean(up * wp), np.mean(vp * wp)
    rec['ustar'] = (cov_uw ** 2 + cov_vw ** 2) ** 0.25
    rec['sigma_u'] = up.std()

    # --- Covariance-lag functions and autocovariances (FFT, zero padded) ---
    nfft = 1 << int(np.ceil(np.log2(2 * N_BLOCK)))
    F = {k: np.fft.rfft(x, nfft) for k, x in s.items()}
    overlap = N_BLOCK - np.abs(LAGS)
    lagcov = {}
    for k in ('ts', 'co2', 'h2o'):
        cc = np.fft.irfft(np.conj(F['w']) * F[k], nfft)
        lagcov[k] = cc[LAGS % nfft] / overlap
    acov = {k: np.fft.irfft(np.abs(F[k]) ** 2, nfft)[:NOISE_TAUS.max() + 1] / (N_BLOCK - np.arange(NOISE_TAUS.max() + 1))
            for k in s}
    cc_cq = np.fft.irfft(np.conj(F['co2']) * F['h2o'], nfft)
    rec['cov_cq'] = cc_cq[0] / N_BLOCK

    k0 = -LAG_MIN   # index of lag 0
    inwin = (LAGS >= WIN_MIN) & (LAGS <= WIN_MAX)
    for k, tag in (('ts', 'wt'), ('co2', 'wc'), ('h2o', 'wq')):
        c = lagcov[k]
        rec[f'lagcov_{tag}'] = c.astype(np.float32)
        j = int(np.argmax(np.abs(c)))
        rec[f'lag_ext_{tag}'] = LAGS[j] / FS
        rec[f'cov_ext_{tag}'] = c[j]
        jw = np.flatnonzero(inwin)[int(np.argmax(np.abs(c[inwin])))]
        rec[f'lag_win_{tag}'] = LAGS[jw] / FS
        rec[f'cov_win_{tag}'] = c[jw]
        rec[f'cov0_{tag}'] = c[k0]
    for k, tag in (('co2', 'wc'), ('h2o', 'wq')):
        L = lag_used.get(k)
        if L is None or not np.isfinite(L):
            L = rec[f'lag_win_{tag}']
            rec[f'lag_used_source_{tag}'] = 'own'
        else:
            rec[f'lag_used_source_{tag}'] = 'EddyPro'
        Ls = int(round(L * FS))
        rec[f'lag_used_{tag}'] = Ls / FS
        rec[f'cov_used_{tag}'] = lagcov[k][Ls - LAG_MIN]
    rec['cov_used_wt'] = lagcov['ts'][k0]

    # --- Variances, noise, correlation coefficients ---
    for k in s:
        rec[f'var_{k}'] = acov[k][0]
        nv, nv_p23, nv_max = noise_variance(acov[k])
        rec[f'noise_var_{k}'] = nv
        rec[f'noise_var_p23_{k}'] = nv_p23
        rec[f'noise_var_max_{k}'] = nv_max
    sw, st, sc, sq = (np.sqrt(rec[f'var_{k}']) for k in ('w', 'ts', 'co2', 'h2o'))
    rec['r_wt'] = rec['cov_used_wt'] / (sw * st)
    rec['r_wc'] = -rec['cov_used_wc'] / (sw * sc)
    rec['r_wq'] = rec['cov_used_wq'] / (sw * sq)
    rec['r_cq'] = -rec['cov_cq'] / (sc * sq)
    obukhov = -rec['ustar'] ** 3 * rec['ts_mean'] / (KARMAN * GRAV * rec['cov_used_wt'])
    rec['zL'] = Z_MEAS / obukhov

    # --- Cospectra and spectra ---
    shifted = {'w': wp[:M_SPEC], 'ts': s['ts'][:M_SPEC]}
    for k, tag in (('co2', 'wc'), ('h2o', 'wq')):
        Ls = int(round(rec[f'lag_used_{tag}'] * FS))
        Ls = min(max(Ls, 0), SHIFT_MAX)
        shifted[k] = s[k][Ls:Ls + M_SPEC]
    G = {k: np.fft.rfft(x - x.mean())[1:M_SPEC // 2 + 1] for k, x in shifted.items()}
    scale = np.full(M_SPEC // 2, 2.0 / M_SPEC ** 2)
    if M_SPEC % 2 == 0:
        scale[-1] = 1.0 / M_SPEC ** 2
    for k, tag in (('ts', 'wt'), ('co2', 'wc'), ('h2o', 'wq')):
        rec[f'cosp_{tag}'] = binned(scale * np.real(np.conj(G['w']) * G[k])).astype(np.float32)
    for k in ('w', 'ts', 'co2', 'h2o'):
        rec[f'spec_{k}'] = binned(scale * np.abs(G[k]) ** 2).astype(np.float32)
    return rec


def process_day(year, day, files, lags):
    """All blocks of one day. `files` maps file start times to paths, `lags` block starts to used lags."""
    t_first = pd.Timestamp(f"{day} {FIRST_BLOCK}")
    t_last = pd.Timestamp(f"{day} {LAST_BLOCK}")
    blocks = pd.date_range(t_first, t_last, freq='30min')
    out = []
    raw_cache = {}
    for t0 in blocks:
        # The file whose nominal span contains the block.
        cand = [s for s in files if s <= t0 and t0 + pd.Timedelta('30min') <= s + pd.Timedelta(hours=FILE_HOURS)]
        rec_base = {'year': year}
        if not cand:
            out.append({**rec_base, 'TIMESTAMP_START': t0, 'TIMESTAMP_MIDDLE': t0 + pd.Timedelta('15min'),
                        'skipped': True, 'skip_reason': 'no raw file'})
            continue
        fstart = max(cand)
        if fstart not in raw_cache:
            raw_cache[fstart] = read_raw(files[fstart])
        raw = raw_cache[fstart]
        i0 = int(round((t0 - fstart).total_seconds() * FS))
        nrows = len(raw['w'])
        if i0 + N_BLOCK > nrows:
            out.append({**rec_base, 'TIMESTAMP_START': t0, 'TIMESTAMP_MIDDLE': t0 + pd.Timedelta('15min'),
                        'skipped': True, 'skip_reason': 'raw file shorter than the block', 'file_rows': nrows,
                        'raw_file': os.path.basename(files[fstart])})
            continue
        rec = process_block(raw, i0, t0, lags.get(t0, {}))
        rec.update(rec_base)
        rec['raw_file'] = os.path.basename(files[fstart])
        rec['file_rows'] = nrows
        out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test', metavar='OUT', help='process two days of 2006 and write to OUT')
    ap.add_argument('--workers', type=int, default=6)
    args = ap.parse_args()

    ep = pd.read_parquet(EPFILE, columns=['CO2_TLAG_USED', 'H2O_TLAG_USED'])
    jobs = []
    years = {2006: PERIODS[2006]} if args.test else PERIODS
    for year in years:
        idx = raw_file_index(year)
        if idx.empty:
            print(f"{year}: no raw files found", flush=True)
            continue
        days = pd.date_range(f'{year}-{MONTHS[0]:02d}-01', f'{year}-{MONTHS[-1]:02d}-31', freq='D')
        if args.test:
            days = days[:2]
        for day in days:
            w0 = pd.Timestamp(f"{day.date()} {FIRST_BLOCK}")
            w1 = pd.Timestamp(f"{day.date()} {LAST_BLOCK}") + pd.Timedelta('30min')
            sel = idx[(idx.index + pd.Timedelta(hours=FILE_HOURS) >= w0 + pd.Timedelta('30min'))
                      & (idx.index <= w1 - pd.Timedelta('30min'))]
            sel = sel[(sel.index >= w0 - pd.Timedelta(hours=FILE_HOURS))]
            _ep = ep.loc[w0 + pd.Timedelta('15min'):w1]
            lags = {t - pd.Timedelta('15min'): {'co2': r['CO2_TLAG_USED'], 'h2o': r['H2O_TLAG_USED']}
                    for t, r in _ep.iterrows()}
            jobs.append((year, str(day.date()), sel.to_dict(), lags))
    print(f"{len(jobs)} days to process with {args.workers} workers", flush=True)

    rows = []
    t_start = time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(process_day, *j): j[:2] for j in jobs}
        for n, fut in enumerate(as_completed(futs), 1):
            try:
                rows.extend(fut.result())
            except Exception as e:   # one bad day must not stop the run; it is reported
                print(f"FAILED {futs[fut]}: {e!r}", flush=True)
            if n % 20 == 0 or n == len(jobs):
                print(f"{n}/{len(jobs)} days, {time.time() - t_start:.0f} s", flush=True)

    df = pd.DataFrame(rows).sort_values('TIMESTAMP_START').reset_index(drop=True)
    df.attrs = {'lags_samples': LAGS.tolist(), 'fs_hz': FS, 'bin_edges_hz': BIN_EDGES.tolist(),
                'bin_centres_hz': BIN_CENTRES.tolist(), 'months': list(MONTHS),
                'blocks': f'{FIRST_BLOCK}-{LAST_BLOCK} block starts, CET',
                'script': 'workflow/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/raw_data_diagnostics.py'}
    out = args.test or OUTFILE
    df.to_parquet(out, index=False)
    print(f"{len(df)} blocks ({int(df['skipped'].sum())} skipped) written to {out}", flush=True)


if __name__ == '__main__':
    sys.exit(main())
