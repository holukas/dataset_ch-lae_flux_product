# Dataset plan

Working document: what the CH-LAE flux product is to contain, what exists today,
and what is still missing. It is the place to look when picking up the work again.

It lives at the repository root rather than in `docs/` because Quarto renders
every `.md` under `docs/` onto the public website, and this file is internal.
When a section here settles it moves to the site — the variable inventory to
`docs/Variables.md`, the scope and coverage summary to `docs/Overview.md` — and
is deleted from this file so the two cannot drift apart.

Status vocabulary used throughout:

- **done** — exists, checked, and read by something downstream.
- **open** — planned, not started or not finished.
- **verify** — a fact this plan depends on that has not been established yet.
  Nothing marked `verify` may be quoted as settled in the published pages.


## 1. Releases

| release | period | gas analyser | state |
|---|---|---|---|
| `FP2026.1` | 2016 - Sep 2026 | `IRGA72` (LI-7200, enclosed path) | done, released 27 Oct 2026 |
| `FP2026.2` | 2004 - Sep 2026 | `IRGA75` (LI-7500, open path) 2004-2015 + `IRGA72` from 2016 | open: both chains and the merges run 1 Nov 2026 with the FP2026.2 thresholds and `HAMPEL_3` (4.2) |

`FP2026.2` supersedes `FP2026.1` and re-includes it in full. The two releases
differ in the flux record only; the meteorological product is built once over
2004 - 30 Sep 2026 and serves both. The period was extended from 2025 in October
2026; section 3.1 lists which products have been carried along.


## 2. Record boundaries

These are the periods the dataset can cover, and the reason each one starts and
stops. They bound every table below.

| record | period | note |
|---|---|---|
| `IRGA75` fluxes | 2004 - 12 Dec 2017, plus 17 Jan - 20 Mar 2019 | analyser removed Dec 2017; the 2019 window is the stand-in run `2019_3` |
| `IRGA72` fluxes | 11 Jan 2016 - 30 Sep 2026 | two physical LI-7200 units, exchanged inside the 2019 gap; the Level-0 record ends 2026-10-01 00:45 at the run boundary |
| tower meteorology, 47 m | 2004 - 30 Sep 2026 | `PA` and `LW_IN` start Sep 2005 with the CNR1 and the pressure sensor; `PREC`, `SW_OUT` and `LW_OUT` products still end 2025 |
| soil profile FF1 | 2004 - 2025 | sensors replaced as a set on 19 Mar 2020, no overlap across the change; products not yet extended to 2026 |
| radiometer | CNR1 Sep 2005 - Dec 2021, CNR4 from 14 Dec 2021 | logger constants updated 7 Jan 2022, 24 days later |

Setup periods, their notes and the unusable windows are in `docs/Yearly_Notes.md`
and are not repeated here.


## 3. Meteorological variables

### 3.1 In the dataset

One product notebook per variable in `workflow/10_METEO/30_PRODUCTS/`, joined by
`99_METEO_MERGED_2004-2026.09.ipynb` (all thirteen; `08` to `13` still end 2025) and documented on a page under
`docs/Meteo_Data.md`.

| variable | series | period | notebook | page | state |
|---|---|---|---|---|---|
| `SW_IN` | incoming shortwave, 47 m | 2004 - Sep 2026 | `01` | yes | done |
| `TA` | air temperature, 47 m | 2004 - Sep 2026 | `02` | yes | done |
| `PPFD_IN` | photosynthetic photon flux density, 47 m | 2004 - Sep 2026 | `03` | yes | done |
| `RH` | relative humidity, 47 m | 2004 - Sep 2026 | `04` | yes | done |
| `PA` | air pressure, 47 m | 2005 - Sep 2026 | `05` | yes | done |
| `LW_IN` | incoming longwave, 47 m | 2005 - Sep 2026 | `06` | yes | done |
| `VPD` | vapour pressure deficit, 47 m | 2004 - Sep 2026 | `07` | yes | done |
| `PREC` | precipitation | 2004-2025 | `08` | yes | done |
| `SWC` | soil water content, 5 depths | 2004-2025 | `09` | yes | done |
| `TS` | soil temperature, 7 depths | 2004-2025 | `10` | yes | done |
| `G` | soil heat flux, forest floor, 3 plates | 2004-2025 | `11` | yes | done |
| `SW_OUT` | outgoing (reflected) shortwave, 47 m | 2005-2025 | `12` | yes | done |
| `LW_OUT` | outgoing (emitted) longwave, 47 m | 2005-2025 | `13` | yes | done |

Six of these are re-formatted for EddyPro by
`40_EXPORTS/EDDYPRO_BIOMET_CH-LAE_2004-2026.09.ipynb` (`TA`, `RH`, `PA`, `SW_IN`,
`LW_IN`, `PPFD_IN`) and are the biomet input to the final flux runs. The export
reads them from `99_METEO_MERGED_2004-2026.09.parquet`, not from the six product
files, and exports the measured `TA` and `RH`, not the homogenised columns. Over
2004-2025 it differs from the 2025 file only in model fills and reconstructions
of `TA`, `SW_IN`, `PPFD_IN` and `RH` and in the probe half-hour of 16 May 2025;
the notebook asserts this and attributes each difference.

**Extension to 30 September 2026.** The Lägern reference
(`10_REFERENCE/MeteoSwiss_LAE_2004-2026.09`) and products `01` to `06`, the six
biomet inputs, now end at `2026-09-30 23:45` and are named `*_2004-2026.09`
(`05`, `06`: `*_2005-2026.09`). Their 2026
screening notebooks (`20_SCREENING/*/<VAR>_T1_47_1_2026.09`) are committed. What
the extension brought:

- **`02` and `04` carry a new probe history at 47 m.** A Campbell HygroVUE10
  replaced the CS215 on 5 June 2026 (source code `4`). The CS215 itself has two
  states besides normal operation: it read too warm in sun from autumn 2024 until
  it was handled on 16 May 2025, and it carried no daytime shield excess after
  that. Both notebooks put the HygroVUE10 era onto the CS215 level in their
  homogenised columns.
- **`04` now exports `RH_T1_47_1_HOMOGENIZED`**, and reads `02`'s measured and
  homogenised `TA` to build it. This is a new value-changing read: `04` must be
  re-run whenever `02` changes.
- **Re-run done.** `02`, `04` and `06` were re-run on 22 Oct 2026, in that order,
  and the `TA`, `RH` and `LW_IN` pages carry the numbers of that run. `04` (saturation
  ceiling of the MP101A, step 13), `07` and `99` were re-run on 29 Oct 2026.

`07` is extended: it exports `VPD_T1_47_1` from the measured `TA` and `RH` and
`VPD_T1_47_1_HOMOGENIZED` from their homogenised columns, and `99` merges both.

Not yet extended, still reading or writing the `*_2025` files: `08` to
`13`, `RADIATION_SENSOR_CONTINUITY`, `TA_HOMOGENIZATION_OPTIONS` and
`build_meteo_dashboard.py` (whose paths `build_calendar_explorer.py` imports). The
`90_OVERVIEW` notebooks `METEO_TA`, `METEO_SW_IN` and `METEO_VPD` read the `*_2004-2026.09`
products and cover 2004-2025.

Open method items from the review of the extended notebooks:

- `05`: the seasonal-cycle check of the tower-Lägern difference is not cut at
  `LAST_FULL_YEAR`, unlike the other yearly statistics of the notebook.
- `05`: the post-2016 departure from the barometric formula against Lägern keeps
  growing, -0.061 kPa in 2025 and -0.074 kPa in January to September 2026. Section 6.
- `03`: the `PPFD_IN` decline has not continued since 2024; 2025 and 2026 stay
  within the ordinary one-year change of the 2024 level. The `PPFD_IN` page has to
  say so.
- `06`: the overcast ceiling of summer 2026 falls to 0.93-0.95, below every
  earlier year. The notebook attributes it to an exceptionally dry and clear
  summer, not to the instrument; no action beyond the `LW_IN` page.

### 3.2 Recently added

`G`, `SW_OUT` and `LW_OUT` were added in September 2026 and are listed in 3.1. Their
methods live in the notebooks and on their `docs/Meteo_Data_*.md` pages; only what is
still unresolved is kept here, in section 6.

Three things about them are worth knowing before the next variable is added, because
each cost a wrong result first.

- **A field rename is not an instrument change, and the two need not coincide.** The
  archive renamed the `G` fields on 2011-12-31 while the measurement carried on
  unchanged for another three months; the acquisition actually changed in March and
  April 2012. A first version of `11` put the era boundary on the rename and pushed a
  visible artefact into the exported product. Derive an era boundary from the data and
  report the rename separately.
- **A provenance flag must be built from where the values ended up, not from where they
  started.** `12` shifted the August 2012 block onto its corrected time axis without
  moving the masks that record which screening supplied each value, and exported 31
  records under the wrong screening. Anything that moves data in time has to move its
  provenance with it.
- **A threshold derived from an effect size degenerates when the effect is zero.**
  Several checks in `12` and `13` compared a scatter against a fraction of the very
  departure they were testing, so they could not pass when the answer was "no
  difference". Derive a threshold from what the record does when nothing happened, and
  check that such years exist before relying on them: in `13` they do not, and the
  notebook says so rather than pretending otherwise.

### 3.3 Candidates, not yet decided

Measured at the site, plausible for the dataset, no decision taken. Listed so the
scope question is asked once rather than rediscovered.

| candidate | raw database field | note |
|---|---|---|
| `PPFD_OUT` | `PPFD_OUT_T1_47_1`, `PPFD_OUT_T1_47_2` | two sensors; a reflected-PAR channel (`PPFD_refl`) already exists in the 2004 program, so the record may predate the 2016 PAR LITE |
| `PPFD_DIF` | `PPFD_DIF_T1_47_1` | Delta-T BF2 sunshine sensor, total and diffuse PAR, from Aug 2004 |
| second `PPFD_IN` | `PPFD_IN_T1_47_2` | a second incoming sensor at the same level; decide whether it is a replicate or a replacement era |
| `NETRAD` | `NETRAD_FF1_2_1`, `NETRAD_NABEL_T1_49_1` | no tower-level net radiometer field; a 47 m `NETRAD` would be derived from the four components. Only the NABEL sensor is screened (2004-2018), and no product exists |
| `ALB` | derived, `SW_OUT`/`SW_IN` | both components are now products (3.1), so this costs nothing extra. `12` already computes the albedo as a diagnostic and reports a median of 0.112 |
| `WS`, `WD` | — | A100LK cup anemometer from Jan 2016; the sonic series is already in the flux output |
| `SWP` | — | MPS-2 and TEROS 21 water potential, FF1 and FF2; same 19 Mar 2020 generation change as `SWC` |
| subcanopy (`M1_2`) | `SW_IN_BC_M1_2_1`, `SW_OUT_BC_M1_2_1`, `LW_IN_BC_M1_2_1`, `LW_OUT_BC_M1_2_1`, `PPFD_IN_BC_M1_2_1` | a full four-component radiation set below canopy, plus PAR — a second measurement level, not a single variable |
| forest floor | `PPFD_IN_AVG_FF1_2_1`, `NETRAD_FF1_2_1` | the FF1 profile's own radiation |

The database field names above are read from listings cached in the outputs of
the `SW_IN`, `LW_IN`, `PPFD_IN` and `NETRAD` screening notebooks. Field existence
is not coverage: the first and last date of each has still to be checked.

Excluded by an existing decision: the **profile masts** (`T1_17.5`, `T1_35`,
`M2`, `M3`, `M4`). The dataset takes its meteorology from the 47 m level and the
forest floor. See `docs/Instrumentation.md`.


## 4. Fluxes

### 4.1 What the dataset publishes

| flux | from | state |
|---|---|---|
| `NEE` | CO~2~ flux plus storage, u*-filtered, gap-filled | `05_FPPC` (was `01_FPPC`), run on `IRGA72` 2016 - Sep 2026 and `IRGA75` 2004-2017 |
| `LE` | turbulent latent heat flux, no storage, no u* filter, gap-filled | `25_FPPC` (was `11_FPPC`), both analysers |
| `H` | turbulent sensible heat flux from the sonic, no storage, no u* filter, gap-filled | `35_FPPC` (was `15_FPPC`), both analysers |
| `GPP`, `RECO` | Level-4.2 partitioning of gap-filled `NEE` | not in FP2026.1 (decided 26 Oct 2026); run in both `05_FPPC` for FP2026.2 |
| `ET` | derived from gap-filled `LE` in `25_FPPC` | both analysers |

`LE` and `H` follow Pastorello et al. (2020): they are turbulent fluxes without a
storage term and are not u*-filtered (decided 26 Oct 2026). The 2016-2024 chain
published storage-corrected `LE` and `H`; this version does not.

### 4.2 Chain status

Levels as defined in `docs/FPC.qmd`. The run-by-run progress of the flux
calculations (versions, settings, what has been run for which year) is logged in
the [flux progress sheet](https://docs.google.com/spreadsheets/d/1kltV0Vuh9L1IR_z9HWqLBzEKpT6-G7C3TUN7H6uvA4A/edit?gid=0#gid=0);
the table below summarizes it per level.

| level | what it does | `IRGA75` | `IRGA72` | site page |
|---|---|---|---|---|
| Raw | binary → ASCII (bico) | done | done | written |
| L0 | preliminary run, per setup period | done, 2004-2019 | done, **through Sep 2026** | written |
| L1 | final run, per setup period | re-run Oct 2026 (`FF-202610`, 19 runs); merged in `20_L1_FLUXES/IRGA75/99` (18 run files) | done, **2016 - Sep 2026** (re-run, 18 runs) | written, with `L1_EddyPro_Settings` |
| L1.1 | open-path correction (opco) | done: `30_.../IRGA75/00` (with the July 2013 clock shift) and `01` (opco without `VPD`), re-run 29 Oct 2026 | n/a | written |
| L2 | quality flags from L1 output | in `30_` chain | in `30_` chain | written |
| L3.1 | storage term added (`NEE` only) | in `30_` chain | in `30_` chain | written |
| L3.2 | outlier detection; u* threshold detection | in `30_` chain, with the manual fog removals; tests 5 and 6 (`NEGNIGHT`, `NEGNIGHTS`) relaxed to uncertainty-based limits in `05`, run 30 Oct 2026; u* detection in `30_.../USTAR_THRESHOLD_DETECTION_2004-2026.09` (item 18) | in `30_` chain; test 5 relaxed in `05`, run 30 Oct 2026; u* detection as for `IRGA75` | written |
| L3.3 | flags from three constant u* thresholds | `NEE`; FP2026.2 thresholds, run 1 Nov 2026 (item 18) | `NEE`; FP2026.2 thresholds, run 1 Nov 2026 (item 18) | written |
| L4.1 | gap-filling (XGBoost, MDS for comparison) | `NEE`, `LE`, `H` | `NEE`, `LE`, `H` | written |
| L4.2 | partitioning into `GPP` / `RECO` | run in `05` (FP2026.2) | run in `05` (FP2026.2 only) | written |
| QCF | overall quality flag | — | — | written |

Both chains run on their full records (`IRGA72` 2016 - Sep 2026, `IRGA75` 2004-2017).
The `IRGA72` chain was re-run on 29 Oct 2026 on the new meteo merge: `NEE`, `H` and `GPP`
unchanged, `LE` keeps more half-hours with the wider absolute limits. The `IRGA75` chain
(`00`, `01`, `05`, `25`, `35`) was re-run the same evening. On the evening of 30 Oct 2026 both `05`
were re-run with the relaxed negative-night tests (item 11), together with `IRGA75/25` and `35`,
and the merges downstream after them (`IRGA72/99`, `IRGA75/99`, the stage merge, `80_FINALIZE/10`,
`90_OVERVIEW`). The test variants `T2`
(2004-2006) and `T3` (2012-2014) of `IRGA75/05` have been re-run with the relaxed tests (results
in item 11). On 1 Nov 2026 both chains (`05`, `25`, `35`, `99`) were re-run with the FP2026.2
USTAR thresholds and `HAMPEL_3`, followed by the stage merge, `80_FINALIZE/10`, the USTAR
detection notebook and the `90_OVERVIEW` flux notebooks. The test variants `T1`-`T3` carry the
new thresholds but were not re-run.

### 4.3 Auxiliary flux-derived series to decide on

Storage terms (`SC`, `SLE`, `SH`), friction velocity `USTAR`, the u* threshold
actually applied, the per-level quality flags and `QCF`, and the sonic wind
series. These exist in the processing output; the decision is which of them the
published file carries and under which names. `docs/Variables.md` is the page
that will state it.


## 5. Where to continue

**Next steps (2 Nov 2026, evening), in order.** Scope of FP2026.2 decided: the storage screen of
the `IRGA75` (item 20) and one USTAR set per analyser (item 18, changed 3 Nov 2026); opco unchanged; the
remaining `IRGA75` biases stated as uncertainties, not corrected (item 21).

**Item 21 against item 22, by day:** the self-heating estimate from the LI-7500 data alone (3 Nov
2026, phase 4, below) finds no step at 2007/2008 and an over-correction of opco's heat part of about
15 % before 2016 (s_day 0.84), about -80 to -150 gC m-2 per year. This argues against the day fix of
item 22 (the correction of Etzold et al. 2011 instead of opco by day before 19 Dec 2007), which
rests on a step at that date; recommended not to adopt it and to state the daytime bias as an
uncertainty (step 3). The wet-night fill of item 22 is tested in the next block.

**Next: gap-filling of the `IRGA75` wet nights** (3 Nov 2026; decides `IRGA75/05` before the rerun).
In 2016-2017 the XGBoost fill of the LI-7500's humid night gaps is 1.48 umol m-2 s-1 where the
LI-7200 measured 4.83 in the same half-hours (item 22). XGBoost learns from the few humid nights the
LI-7500 measured, which read low (item 19) and are not representative (rain nights cannot be
measured). The wet-night fill is gap-filling only: no measured value changes. Test in this order:
- Remove the biased humid LI-7500 nights from the data and from the XGBoost training (the
  quality-control step of item 19), fill with XGBoost as before, and compare its fill of the wet
  night gaps with the LI-7200 on the same half-hours in 2016-2017.
- If it comes close to the LI-7200 (4.8 umol m-2 s-1), keep XGBoost as the only gap-filling method.
- If it stays low, which is expected in part because few wet-condition examples remain, fill the
  LI-7500's wet night gaps (rain in the previous 3 h or RH >= 99.5 %) with Lloyd-Taylor fitted on its
  own dry nights (3.62 in the overlap), as a special case with its own gap-filling flag value.
- Either way, report the XGBoost, Lloyd-Taylor and donor fills side by side as a sensitivity, and
  state that the fill is still about 1.2 umol m-2 s-1 low in the overlap.
- **Include the cold-night findings of item 11 (3 Nov 2026)** in the same test: 89 % of the
  cold-night deficit (about -53 gC m-2 per year in 2004-2015) is in gap-filled overcast nights.
  Test a cloud feature for XGBoost (cloudiness from LW_IN and TA; LW_IN is missing in 2004 and
  changed sensor in 2016), the wet-window screen (AGC >= 56.25), and a night term in opco on
  cloudiness. Use no RH thresholds across 2016 (the RH sensor change makes them select different
  nights); define "humid" or "wet" by rain, cloudiness or AGC instead, also in the steps above.
- **Tested 3-4 Nov 2026** (`research/reports/wetnight_2026-11-03/`, scratch replica of `IRGA75/05`,
  `CUT_50` 0.4294, storage screen on; overlap night gaps where the LI-7200 measured, n 1246, LI-7200
  4.95 umol m-2 s-1; on the nights both measured the two agree, 4.60 against 4.62):
  - XGBoost as in `05` 2.58; with the wet night records (rain 3 h, AGC >= 56.25) removed from data
    and training 2.41; with a cloudiness feature 2.35; both 2.14. Neither helps: the low fill is not
    learnt from biased wet records.
  - Without VPD 3.24: VPD near 0 in rain and fog gaps maps them to the LI-7500's low calm foggy
    nights. Dropping VPD also changes the days (about +40 gC m-2 per year), so not for the whole model.
  - Lloyd-Taylor on the LI-7500's own dry nights (no rain 3 h, no wet window), for the night gaps
    with rain, a wet window or an overcast sky (CI >= 0.8): 3.37, the best LI-7500-only fill; for
    all night gaps it makes the dry clear gaps worse. Effect: night 2004-2015 about +95 gC m-2 per
    year, annual NEE +82 (2004-2009) and +108 (2010-2015).
  - About 1.6 umol m-2 s-1 remains in every LI-7500-only fill: the nights it misses respire more than
    its temperature response predicts. Only the LI-7200 donor model gets closer (4.33, report C).
  - Recommended, not decided: the Lloyd-Taylor fill for the wet or overcast night gaps, with its own
    flag value, XGBoost with VPD for the rest; XGBoost, Lloyd-Taylor and donor side by side as a
    sensitivity; the remaining 1.6 stated as an uncertainty towards less uptake.
  - **Built 4 Nov 2026:** diive `run_level41_xgb_wetnight` / `LongTermGapFillingXGBoostWetNightTS`
    (issue #445, v0.93.0; merged into `indev` 4 Nov 2026, not pushed), columns `_gfXGWN`, flag 3.
    Set in `IRGA75/05` next to the plain XGBoost fill (Settings `RUN_WETNIGHT`, `WETNIGHT_*`;
    Step 7), not run. Partitioning, the annual sums of the merge
    and `99` still use `_gfXG`: decide which fill the product uses.
- **Once decided: a docs page of its own on this gap-filling** (requested 3 Nov 2026), nested under
  `L4.1.md` in the sidebar and the PDF chapters, like `L3.3_Constraints.md` under `L3.3.md`: why the
  LI-7500 wet nights need it, the method chosen, the validation against the LI-7200, the flag value
  and the sensitivity.
Recommended, not decided: the day fix of item 22 stays a sensitivity test, not a correction; keep opco by day and state the
daytime bias of 2004-2007 (possibly to 2009) as an uncertainty, until an internal, year-by-year
heating estimate (report option 5) or the QCL periods (item 17) can test it.

**Next: estimate the self-heating of the LI-7500 from its own data** (3 Nov 2026; to be investigated
in detail over several sessions; report option 5). Aim: a year-by-year heating factor for the
daytime opco correction, from the open-path data and standard meteorology alone, without a
literature factor or a hand-set break, and usable for any long open-path record. Level-1 output is
enough to start; the raw data are needed only for a spectral approach later. Three independent
estimates:
- **A. Frozen winter days.** On frozen days (TA below about -2 degC) the true daytime flux is close
  to respiration, so apparent uptake beyond the respiration of the LI-7500's own nights at the same
  temperature is heating; fit a factor per winter. Signal already seen: opco leaves 2.6-5.5
  umol m-2 s-1 on such days in 2005-2013, the LI-7200 0.6-1.5. Risk: winter photosynthesis of the
  conifers on sunny days; strict selection needed.
- **B. Wind contrast in the growing season.** Fit a light-response model per period and regress
  the remaining daytime flux on the shape of the expected heating term (radiation, temperature,
  wind); the existing wind test of `OPCO_TRANSFER_CHECK` made into an estimator. Pool years, or
  winter and summer, against the noise (about +-0.6 per year). Risk: wind also changes the true
  flux (canopy coupling, advection).
- **C. Mean CO2 density against the profile system.** Warmer air in the path lowers the density the
  LI-7500 reads by about 0.3 % per K; a residual against the LI-7000 profile at the top of the tower
  that follows sun and wind, after removing the slow calibration offset, measures the path warming
  in kelvin. Risk: the analyser's temperature dependence and zero drift.
- **Check:** fit on the LI-7500 alone, including 2016-2017; in the overlap the corrected LI-7500
  must match the LI-7200 on the same half-hours. A and B should give consistent factors per year,
  and C the size of the warming.
- **First:** handle the calibration offsets of 2004-2007, which scale every density-dependent term;
  the fieldbook gives dated checks on 26 Sep 2007 (zero +31 ppm, previous zero 7 Feb 2006, H2O span
  coefficient 0.9364 to 1.2032) and 19 Dec 2007 (zero -46.6 ppm). In GIN these sit in the bulk
  entry dated 3 Jun 2011, which holds all entries of 2006 to mid-2011.
- **Start:** A and B as scratch work with a short report, then C if the profile data hold up.
- **First run, 3 Nov 2026** (`research/reports/selfheating_2026-11-03/`, phases 1-3 and an independent
  review; no LI-7000 profile data exist, so C used other references). CO2 scale: -6 ppm 2004-2005,
  -21 ppm Feb 2006 - Sep 2007, -44 ppm 26 Sep - 19 Dec 2007 (+11 to +55 gC m-2 per year). H2O span
  gain stepped at the calibrations, +30 % in May 2008 - Dec 2010 (FC -0.5 umol m-2 s-1 at summer
  midday, -27 to -38 gC m-2 per year; supported by the energy balance). A (frozen days) about 0.53,
  B (wind contrast) 0.48 after subtracting a failed placebo of 0.42, C no independent estimate.
  Review verdict: opco's heat part over-corrects before 2016 (robust; no step at 2007/2008), but
  the level is about 0.6 +- 0.15, not 0.51 +- 0.12; one factor day and night is not supported
  (overlap nights need about 0.08); the change in annual NEE 2004-2015 is about -200 to -330 gC m-2
  per year (1 sd 120 or more), not -333 +- 80; a non-heating analyser difference of 160-440 gC m-2
  per year in the overlap is as large as the step between the eras. The same head (75H-0640) is
  recorded in Dec 2010 and 2016-2017. Next, ranked: (1) the LI-7200 data of Dec 2010 - Jun 2011
  (fieldbook: calibrated 16 Dec 2010, serviced 3 May 2011, data downloaded from its memory stick on
  3 May and 30 Jun 2011), the only out-of-sample test before 2016; **not found so far** (searched
  4 Nov 2026: not in the data folder, not in the 2011 raw files of the site; search continuing, see
  item 26); (2) retrain opco with part of 2016-2017 held out and run A and B
  there; (3) separate day and night factors; (4) B with the anchored difference instead of the
  placebo subtraction; (5) split the overlap difference into wet records, selection, USTAR and
  gap-filling; (6) s by hour or season; (7) raw-data reprocessing.
- **Second run, 3 Nov 2026 (phase 4, LI-7500 data only).**
  - Refined A (`phase4_A_refined/`): day and night separated, no night heat term, frozen-night
    respiration from u* >= 0.6 and modelled on TA without the cold-night decline. **s_day = 0.84
    for 2004-2015** (systematic 0.79-0.88, 16-84 % 0.69-0.99), 2004-2007 0.76, 2008-2015 0.89, no
    early-late contrast. The 0.53 of phase 3 came from the respiration reference: frozen LI-7500
    nights before 2016 are biased low (negative below u* 0.6; slope 0.63 per K against 0.06 for
    the LI-7200, see item 11). opco therefore over-corrects frozen days by about 15 %, not by half;
    a TA-binned reference (0.63) is the lower bound if the cold-night decline were real. The
    overlap recovers the LI-7200 value within 0.1 on relaxed winter selections. No two-term shape
    fits better.
  - Thermal signals (`phase4_thermal/`): negative. `TA_EP` is the LI-7500 thermistor (EddyPro
    `col_air_t=13` in every run, also used for the LI-7200 runs), 1.9-2.1 K above air at night; the
    cooler voltage follows it. Neither explains the LI-7500 minus LI-7200 difference beyond the
    meteorology in season-held-out tests. The bias grows with cold while the head excess shrinks
    (per K of excess about 10 times larger below 0 degC than above 20 degC), which argues for a
    calibration temperature sensitivity (Deventer et al. 2021) or unseen surfaces rather than
    classic self-heating. The signals show no lower heating before 2016.
  - Consequence: the daytime over-correction before 2016 is about 15 % of opco's heat part, about
    -80 to -150 gC m-2 per year in annual NEE (scaling of the phase 3 sensitivity; not rerun), far
    less than the first run suggested. The larger open problems are the LI-7500 night biases (cold
    nights, wet records), not the daytime heating.
- **Third run, 4 Nov 2026 (phase 5, `phase5_holdout/`; ranked item 2, A only).** opco refitted with
  whole blocks of 2016-2017 held out (a year, a winter, alternating months). Out of sample its own heat
  part no longer matches the LI-7200 on cold days: the matching factor is 0.31-1.08 on the 6 frozen
  days and 0.62-1.12 on the 29 days of Nov-Mar below 0 degC. The refined estimator follows it: within
  about 0.1 on 29-64 days, and 0.2-0.5 high on the 6 frozen days (inside the bootstrap range). The
  method is not biased low, so the 0.84 is not a method artefact. Any bias would put the true factor
  lower, not higher. The cold-night reference choice (0.84 against 0.63) cannot be tested in the
  overlap. One winter alone gives errors up to +-0.9, so per-year values from A are not usable.
  Season: out of sample, opco's factor differs by season by up to 0.15-0.25 (DJF 0.84-0.93, JJA
  0.98-1.00); in 2004-2015 the adjusted factor stays at 0.68-0.87 from November to April. A cannot
  measure summer. Frozen days carry 6 % of the daytime heat part, so the annual -80 to -150 gC m-2
  rests on a transfer that is uncertain by about as much again. H as regressor (sonic H, within
  light x temperature cells): no usable factor. At fixed light opco's heat shape barely varies
  with H, and an extra H slope remains even in sample. In May-Sep 2004-2015 the LI-7500 shows no H
  slope beyond that of the overlap. The higher `k_op` share of 2013-2015 (36-49 % of daytime
  half-hours, against 4-23 % before) does not show in the H slope.
- **Calibration errors, 4 Nov 2026** (`research/reports/calibration_2026-11-04/REPORT.md`): ready to
  adopt for the documented segments (fieldbook dates and check readings): CO2 read 20.9 ppm low with
  span slope 0.9966 (7 Feb 2006 - 26 Sep 2007), 44.2 ppm and 1.0090 (to 19 Dec 2007), -1.8 ppm and
  1.0037 (to 16 May 2008); H2O span gain 1.115, 1.023 and 1.302 (26 Sep 2007 - 16 Dec 2010). Annual
  NEE +38 (2006), +48 (2007), -27, -36, -38 (2008-2010), with opco re-applied +67, +83, -29 to -40;
  mainly by day. The energy balance of May 2008 - Dec 2010 goes from 1.095 to 0.952; zero in the
  overlap. Undocumented segments left uncorrected (about +-12 gC m-2 per year). To do: a pre-step in
  `IRGA75/01` before opco (FC, FH2O, LE, H, CO2 density), using the calibration function being added
  to opco; opco re-evaluated, not refitted.
- **Calibration temperature sensitivity, 4 Nov 2026** (`research/reports/caltemp_2026-11-04/REPORT.md`):
  no basis for a correction. The literature term (S w'T', Deventer et al. 2021) fits at the expected
  size but explains nothing held out; the cold bias sits where w'T' is about 0 (overcast, calm), and
  opco's k term already covers the effect.

1. **Smaller fixes, before the rerun,** so that one rerun covers everything.
   - **Done 4 Nov 2026 (set, not run):**
     - `IRGA72` low sample flow of December 2022 in `REMOVE_DATES` of `IRGA72/05` and `25`, from the
       logged flow: intermittent from 2022-12-05 17:15, mostly 0 to 3 l min-1 from 8 to 19 December,
       normal again from 2022-12-20 12:00.
     - The boom removal of 20-26 Dec 2018 (so far only `H` in `IRGA72/35`) also in `IRGA72/05` and `25`.
     - Both mirrored in the detection notebook; its settings match `05` (checked).
     - The gap-filling settings were already identical in all six chain notebooks (XGBoost, features,
       feature engineering, MDS, L4.1 call); nothing to change.
     - Docs updated 4 Nov 2026: `Issues.md` (December 2022 section, now 5-20 Dec), `Version_FP2026.1.md`
       (December 2022, and its `LE` of 23 Jan - 29 Feb 2016 is unreliable), `Yearly_Notes.md` (2022 section;
       2016 `LE` removal). Docs after the run: `L3.2.md` table (new rows).
   - **Set 4 Nov 2026:** the AGC window of the LI-7500 at Level 2 is 40-65 instead of 40-90 (`IRGA75/05`,
     `25` and the detection notebook): from an AGC of 68.75 the flux is biased against the LI-7200 in
     2016-2017 (by day median -3 to -5 umol m-2 s-1 from 62.5); it removes 0.2-2.3 % of the kept records
     per year. `docs/L2.md` still says 40-90; update it after the run. Not run yet.
   - **Checked 4 Nov 2026 (item 24):** the `IRGA72` `LE` between the removed start-up periods,
     23 Jan - 29 Feb 2016, does not follow the LI-7500 (slope 0.04, r 0.17, means 12 against 29 W m-2
     on 947 paired records; from late May the two agree, r 0.55-0.70). Removed from `LE` in
     `IRGA72/25` (`['2016-01-23', '2016-02-29']`, not run). FP2026.1 as released contains these
     values: note it on `docs/Version_FP2026.1.md` and `docs/Issues.md`.
   - **Product fill of the LI-7500 years: `_gfXGWN` (decided 4 Nov 2026; set, not run).** `IRGA75/05`
     has `PRODUCT_FILL = 'xgbwn'` (if `RUN_WETNIGHT`), and its nighttime and daytime partitioning use
     it. The stage merge `99_FPPC_MERGED` copies the LI-7500 `_gfXGWN` NEE values and flags (CUT_16,
     CUT_50, CUT_84) into the product columns `_gfXG` for 2004-2015 (`LI7500_FILL`, `REPLACED`); flag
     3 marks the Lloyd-Taylor values; its value check compares those columns with their source. The
     LI-7200 years keep plain XGBoost. **It must be stated clearly wherever `_gfXG` is described**
     that the product's NEE `_gfXG` holds the wet-night fill for 2004-2015 (flag 3). Done: the About
     of `99_FPPC_MERGED`, and `80_FINALIZE/variable_info.py`, whose descriptions of the NEE `_gfXG`
     columns and their flags in the merged product (any file with `FLAG_FLUX_SOURCE`) now say so, also
     in the generated `_INFO.md`. After the run: `docs/Variables.md` (the `_gfXG` row, the flag row,
     and the `gfXG` entry of the naming table), `L4.1.md`, `Version_FP2026.2.md`, `Version_Differences.md`
     and the new gap-filling page.
   - **opco options in `IRGA75/01` (set and run 4 Nov 2026, `64f94b5`):** calibration pre-correction of the
     documented segments 2006-2010 (opco `correct_calibration`, no value lost), xi for day and night, and the
     per-half-hour uncertainty `BIAS_UNC_OPCO` (coverage 0.68). A/B test of day/night xi in a replica of the
     chain with partitioning (`research/reports/xidn_2026-11-04/REPORT.md`): NEE changes by no more than the
     gap-filling noise (+-20 gC m-2 per year); in 2017 RECO and GPP are closer to the LI-7200 (RECO_NT -405
     against -499 gC m-2); kept. Decided 4 Nov 2026: the night tests of `IRGA75/05` and the detection notebook
     keep the constant `OPCO_SIGMA` = 1. `BIAS_UNC_OPCO` at night is 0.35-0.5 umol m-2 s-1 in April-October
     and 1.4-1.8 in November-February (median 0.65); in winter it would let more nights of apparent uptake
     pass, and it already contains the random noise of both analysers, which `FS`/`PAS20` count again.
     `BIAS_UNC_OPCO` goes into the uncertainty of the product and of the annual sums instead.
2. **Rerun once, with the decided settings** (both are set, nothing else is to change).
   - **Done 4 Nov 2026, not committed:** detection notebook (declared sets confirmed within
     0.005 m s-1), `05`/`25` of both analysers, `IRGA75/35`, both `99`, `99_FPPC_MERGED`,
     `80_FINALIZE/10`, the detection notebook again and all ten `90_OVERVIEW/FLUX_*`, without errors.
     Fixes made on the way: the value check of `99_FPPC_MERGED` no longer compares dtypes; the
     overviews accept fill flag 3; `FLUX_NEE_IRGA75_INDEPENDENT_ESTIMATES` and `_PARTITIONING_COMPARISON`
     read the LI-7500 `_gfXGWN` under the `_gfXG` names (the fill that `IRGA75/05` partitions);
     `FLUX_GPP` allows the 7 night half-hours without `GPP_DT_OF_CUT_84` in May 2007 (0/0 in float32
     in diive's port of ONEFlux `gpp_vpd`, as in ONEFlux; diive issue holukas/diive#446, v0.93.0).
     The prose of the detection notebook and the overviews was checked against the outputs and
     updated; captions written by code cells show the new text only after the next run.
   - **Open points from the run (next session):**
     - **Done 6 Nov 2026 (not committed):** the parallel section of `FLUX_NEE`,
       `FLUX_NEE_IRGA75_COMPARISONS` and `_EVALUATION` read the product fill `_gfXGWN` for the
       LI-7500 (`FLUX_NEE` keeps plain XGBoost beside it); `FLUX_GPP`, `FLUX_NEE` and `_COMPARISONS`
       leave the partial daytime year 2005 out of all statistics. All rerun, text updated. Results:
       the early LI-7500 years lie further from the LI-7200 years (2004-2006 +349 instead of +268
       gC m-2 per year, 2004-2011 all net sources, 2010-2015 at the LI-7200 level); the gap is now
       almost entirely by day, since the filled winter nights no longer sit below the measured ones.
       Against Etzold et al. (2011), 2005-2009: opco about 640 apart, the Burba-type correction about
       190, no self-heating correction about 25; the biometric sink of 2006-2009 is reached only
       without a correction. This bears on the daytime revisit of step 3. In the parallel period the
       LI-7500 shows 407 gC m-2 more uptake than the LI-7200 with the product fill (528 with XGBoost
       alone). The detection notebook section 7 (FLUXNET) still reads plain `_gfXG`; left as it is.
     - Test run `T2` has no wet-night fill, so its comparison in `_INDEPENDENT_ESTIMATES` overstates
       the effect of the relaxed tests. Rerunning it does not help: the relaxed negative-night tests it
       was made for are part of `05` since 30 Oct 2026, so `T2` is an outdated copy of `05` for
       2004-2006, not a test of anything still open. Drop its comparison from `_INDEPENDENT_ESTIMATES`.
     - **Overnight tests T4-T12 (set up 6 Nov 2026):** `run_tests_T4-T12.sh` in
       `30_FLUX_POST-PROCESSING_CHAIN` runs them in order (logs in the data folder,
       `_logs_T4-T12/`), and `TESTS_T4-T12_COMPARISON_2026-11-06.ipynb` compares them with the product
       run. T4-T6: `IRGA75/01` and `05` with the daytime heating part of opco scaled by 0.84, 0.5 and 0
       (opco `predict(heat_scale=...)`; the daytime revisit of step 3). T7-T8 and T9-T10: `IRGA75/05` and
       `IRGA72/05` with random seeds 1 and 2; T11-T12: `IRGA75/05` with 50 and 200 trees (item 8). Each
       writes its own output file. `T4_01` was checked: daytime heating part 0.84 of the product's,
       night and H part unchanged.
       **Run 6 Nov 2026, all twelve without error; results** (gC m-2 per year, `CUT_50`, product fill):
       - Heat sweep (scale 1 / 0.84 / 0.5 / 0): 2004-2006 minus LI-7200 +349 / +251 / +61 / -231;
         2010-2015 minus LI-7200 +15 / -72 / -258 / -556; 2005-2009 minus Etzold et al. (2011)
         +633 / +548 / +373 / +97; parallel period, half-hours measured by both, LI-7500 minus
         LI-7200 -5 / -48 / -133 / -263 gC m-2. No single scale fits all periods: scale 1 already
         agrees with the LI-7200 in 2016-2017, so the excess of 2004-2006 is not explained by the
         daytime heating part alone but by something that changes over time. The night stays 70 to
         115 below the LI-7200 at every scale. Input to step 3.
       - Seeds: `IRGA75` annual SD 1 to 6, period means within 3; `IRGA72` annual SD 3 to 12, except
         2016 (SD 26, 48 to 98) and 2021 (10); 2016-2025 mean within 5. The model noise is small.
       - Trees (item 8): 50 trees give 20 to 80 less than the 80 chosen by cross-validation, 200 trees
         up to about 40 more (2017: -97 / -15 / +23). About ten times the seed noise, the same order
         as XGBoost minus MDS.
       - CUT order: 2006 (`IRGA75`) and 2017 (`IRGA72`) lie outside `CUT_16`-`CUT_84` in every seed and
         tree run; scale 0 adds 2004, scale 0.5 has none. The unordered scenarios are structural, not
         model noise.
     - **`CUT_50` outside `CUT_16`-`CUT_84` (investigated 6 Nov 2026, scratch):** not a defect. Each
       scenario is gap-filled by its own models, and the threshold also removes daytime records
       (`run_level33_constant_ustar` with its default `nighttime_only=False`), which moves the sum the
       other way than the night records. The annual sum therefore need not rise with the threshold:
       with `_gfXGWN` only 2006 lies outside (457 against 313 to 438), with plain `_gfXG` 2005 and 2006,
       LI-7200 2017; MDS shows the same pattern (r 0.86), so it lies in the data more than in the
       models. To decide: (1) a note on L3.3 or the uncertainty page that the scenario sums are not
       ordered; (2) decided 6 Nov 2026: the USTAR filter keeps applying by day and by night
       (`nighttime_only=False`), as in ONEFlux; `docs/L3.3.md` ("By day as well") already says so; (3) whether the USTAR uncertainty should use the largest
       distance from `CUT_50` instead of half the `CUT_16`-`CUT_84` spread (Pastorello et al. 2020 use
       the latter). Not recommended: one `CUT_50` model for all scenarios.
     - `FLUX_NEE` gives the mean annual `NEE` as +107 (2004-2015) and -23 (2016-2025) gC m-2 per year;
       `docs/Issues.md` (about line 228) still quotes -82 and -18. Update in step 4.
     - Wording not yet decided: the `FLUX_RECO` callout ("most of all in winter", "fewer and
       lower nights"; the outputs show neither, proposed: "at a given temperature the gap is
       largest below 0 degC", "drier and lower nights"); the unsourced "140 to 360 gC m-2" in
       `FLUX_NEE_IRGA72_WET_NIGHTS` cell 1 (the current files give about 200 to 440 with the
       nighttime partitioning); the windy-winter years in
       detection notebook cell 116 (2018 not supported).
   - `IRGA75/01` is already run (4 Nov 2026); start with the USTAR detection notebook.
   - The USTAR detection notebook first. It was switched on 3 Nov 2026 to one set per analyser
     (item 18) and not run since; its check in section 2 and the new table in section 11 must
     confirm the declared sets.
   - `05` and `25` of both analysers, `IRGA75/35`.
   - Then both `99`, the stage merge and `80_FINALIZE/10`.
   - Then the detection notebook a second time, so that its comparisons with the chain show the
     new run and its check of Level 3.2 against `05` passes. Update the text of its sections 6, 7,
     9, 10 and the calm-hours table of section 11, and Main findings.
   - Then the `90_OVERVIEW` notebooks. `FLUX_NEE_IRGA75_COMPARISONS` and `_EVALUATION` and the
     test notebooks `T1`-`T3` declare the per-analyser sets; after the run, update the threshold text of
     the two overview notebooks (0.44, 0.52).
   - The scratch estimate of 2 Nov 2026 (`IRGA75` 2004-2015 about +7 gC m-2 per year, `IRGA72`
     2016-2025 about -38, overlap gap about -250) used the merged USTAR set and no longer applies;
     the run gives the numbers.
3. **State the remaining `IRGA75` biases as uncertainties, per year** (item 21), in
   `docs/Issues.md` and on the version page, as a table; no sensitivity column.
   - Day, 2004-2015: possibly too little uptake, about -80 to -150 gC m-2 per year, from an
     over-correction of opco's heat part by about 15 % (s_day 0.84, phase 4 of the self-heating
     estimate); no step at 2007/2008. **Revisit once the run has new outputs** (agreed 4 Nov 2026):
     compute the daytime bias with the chain instead of the scaling (heat_scale 0.84 as a
     sensitivity run of `IRGA75/01` and `05`), and set it against the climate baseline, which
     showed about +230 for 2004-2009 before the calibration pre-correction. The earlier 0 to -230 for 2004-2009 (climate baseline and
     wind test) is superseded. **Sensitivity run done 6 Nov 2026 (T4-T6, results under step 2):**
     scale 0.84 lowers the annual sums by about 80 to 110 in every year; it closes the 2010-2015 gap
     to the LI-7200 by day but widens the parallel-period gap, so a single scale is not supported.
     To decide: whether the daytime uncertainty is stated as the 0.84 shift (about -80 to -110) or
     as the span to scale 0.5. The investigation of 7 Nov 2026 (item 25) places most of the
     remaining gap in the raw CO2 covariance before 2008, not in opco.
   - Night, 2004-2017: possibly too little respiration, 0 to +200 gC m-2 per year, from the rain
     gaps the LI-7500 does not measure. Of this, the cold (below 2 degC) overcast and wet-window
     nights account for about +53 gC m-2 per year in 2004-2015 (item 11), unless the wet-night step
     above corrects them.
   - The two act in opposite directions and partly cancel.
4. **Bring the docs in line with the run.**
   - Passages of 3 Nov 2026 overtaken by the decisions of 4 Nov (checked 4 Nov 2026):
     - `docs/Issues.md` "Calibration of the LI-7500 in 2004-2010" and its bullet in `L1.1.md` and
       `Version_FP2026.2.md`: they say FP2026.2 does not correct the errors and quote the phase-1
       numbers. Replace with the documented segments now corrected in `IRGA75/01`, the numbers of
       `calibration_2026-11-04/REPORT.md` (closure 1.095 to 0.952), and the uncorrected 2004-2005.
     - `docs/Issues.md` cold-night section: its closing "under test" sentence names a cloud term,
       a cloud driver and a wet-window screen. Replace with what the run applies: xi for day and
       night, the AGC window 40-65, and the Lloyd-Taylor wet-night fill (flag 3).
     - `docs/Version_FP2026.2.md` "Prepared for the next run" lists two changes. Fold in the rest
       set on 4 Nov (calibration pre-correction, xi for day and night, `BIAS_UNC_OPCO`, wet-night
       fill, AGC window, the new LI-7200 removals), or move them to "What changed" once run.
     - `docs/L1.1.md` describes the opco run before the new options; `IRGA75/01` was rerun on
       4 Nov 2026, so check its result table and text against the notebook.
   - `docs/L3.1.md` (storage screen), `docs/L3.3.md` and `L3.3_Constraints.md` (one set per
     analyser, the step after 2017, detection notebook section 12), the version pages
     (`Version_Differences`, `Version_FP2026.2`: the sets and results of the run),
     `docs/IRGA75_Comparisons.md` and the annual sums.
   - Replace the unverified "100 to 200" in `docs/Issues.md`, and its 436 / 370 gC m-2 for
     2016 / 2017 and "fills these gaps with too much uptake", which predate the wet-night fill.
   - `docs/L2.md`: the AGC window of the LI-7500 is 40-65, not 40-90.
   - Docs plots without a notebook (rule of 6 Nov 2026: every plot in the docs is drawn by a
     notebook in `workflow/95_DOCS_FIGURES/`). No code for these exists in the repo or the data
     folder; rebuild each in a notebook and link it from its caption:
     - `CH-LAE_2016_IRGA72_low_flow_Feb2016.png`, `CH-LAE_2021_IRGA72_low_flow_May2021.png`,
       `CH-LAE_2023_IRGA72_low_flow_Aug2023.png` (`Yearly_Notes.md`): FC, LE and H,
       SW_IN, the LI-7200 sample flow and the cell CO2 around each removal.
     - `USTAR_thresholds_from_FLUXNET_NEE_VUT_2004-2023.png` (`Issues.md`): `NEE_VUT_USTAR50` and
       `NEE_VUT_REF` per year from the FLUXNET release (made in a spreadsheet).
     - `CH-LAE_2016-2024_phase_shift_fft_SWINvsSWINPOT.png` (`Issues.md`): daily phase shift of
       `SW_IN` against `SW_IN_POT` (FFT), 2016-2024.
   - Storage drift of the LI-7500 (`docs/L3.1.md` "Drift of the LI-7500 storage term" and its Known
     limitations, `docs/Issues.md` "The storage term of the LI-7500 drifts", `Overview.md`,
     `Version_FP2026.2.md`, `IRGA75_Comparisons.md`): the concentration screen was applied in the
     run of 4 Nov 2026. Replace "set for the next run" and the test-run numbers with the storage
     sums and the `NEE` change of the run. Keep the mechanism (the concentration rises in the gaps
     of the wet periods, the rise is never counted, the decline after the gap enters as a negative
     storage flux), and add a figure of it.
   - Fix the inconsistencies found by the docs agents on 2 Nov 2026 (the names in the
     acknowledgments of `docs/index.md` are fine and stay, decided 4 Nov 2026): the end of the 2016
     removal (25 or 26 May), the uncertainty wording of `Version_FP2026.2`, the end date of the
     LI-7500, and the conflicting values in `Yearly_Notes` (2013 clock shift, 2013/2014 fog,
     2018 obstruction dates).
   - Move the scratch findings of 1-2 Nov 2026 (overlap split, climate baseline, concentration
     check, screen tests; research reports `fppc_insights_2026-11-01`) into a notebook, for
     example an overlap notebook in `90_OVERVIEW`, so that the docs can link to the evidence.
   - Add the search for a dated cause of the daytime excess (report H) to section 5 of
     `IRGA75/OPCO_TRANSFER_CHECK` at its next run.
   - Close items 9, 12, 19 and 20.
5. **Later, outside FP2026.2.**
   - The sensitivity of the gap-filled sums to the number of trees (item 8). The `IRGA72` sum of
     2016 moves from +58 to +188 gC m-2 between 90 and 1000 trees.
   - An independent constraint of the early `IRGA75` years, if QCL or chamber data turn up
     (item 17).
   - **Possible future session: recompute the `IRGA75` fluxes from the 20 Hz raw data** (noted
     3 Nov 2026; the raw data are not on this machine). With the correct zero and span
     coefficients of each calibration period for CO2 and H2O (fieldbook checks of 7 Feb 2006,
     26 Sep 2007, 19 Dec 2007, 16 May 2008 and later; H2O gain +30 % in May 2008 - Dec 2010), so
     that the covariance effect of the CO2 offset (Fratini et al. 2014) is included, which Level-1
     data cannot give. Then look for the heating signature in the cospectra: a part common to the
     CO2 and H2O signals in proportion to their densities, which would estimate the self-heating
     from the open-path data alone (see the self-heating step in this section).

**Runs done (30 Oct 2026).** With the relaxed night tests: `IRGA72/05`, `99`; `IRGA75/05`,
`25`, `35`, `99`; `30_.../99_FPPC_MERGED`; `80_FINALIZE/10` (not `20`: FP2026.1 stays as
released); `90_OVERVIEW/FLUX_NEE`, `METEO_VPD`; the comparison and investigation notebooks of
item 12. Next: the FP2026.2 notebook in `80_FINALIZE` (2004-2026.09; content and release to be
decided).

**Re-run done (31 Oct 2026): the low sample flow of the LI-7200.** `IRGA72/05`, `25`,
`IRGA72/99`, `30_.../99_FPPC_MERGED`, `80_FINALIZE/10` and the overviews were run; no measured
`NEE` or `LE` is left in the removed windows. Against FP2026.1, annual `NEE` 2016-2025 differs by
-21 to +13 gC m-2, 2021 by -101 (`ET` -6 to +12 mm, 2021 +41; after the May 2018 removal;
between two runs without a change in 2016 its NEE moved by about 20, from retraining the models). The note below is kept for the record.
Was: **To re-run: the low sample flow of the LI-7200** (found 30 Oct 2026 in the new overview
notebooks `90_OVERVIEW/FLUX_GPP`, `FLUX_RECO`, `FLUX_ET`, `FLUX_H`, then searched for in the
logged flow rate). `FC` and `LE` were near zero from 28 April to 27 May 2021, in six periods in
February 2016, on 26 May 2016 until 07:45, and from 11 to 14 August 2023. All are now in
`REMOVE_DATES` of `IRGA72/05` and `25` (`docs/Yearly_Notes.md`, 2016, 2021, 2023). Re-run
`IRGA72/05` and `25`, then `IRGA72/99`, `30_.../99_FPPC_MERGED`, `80_FINALIZE/10` and the overview
notebooks. FP2026.1 as released still contains these values. **May 2018 checked (31 Oct 2026):**
the flow fell to zero on 17 May 07:15-16:45 and from 18 May 07:45; `FC` and `LE` of 2018-05-17
07:15-16:45 and 2018-05-18 07:45 to 2018-05-19 11:45 are now in `REMOVE_DATES` of `IRGA72/05` and
`25`. The low `LE` of 13-16 May is weather (normal flow, little radiation) and is kept.

Then, before the release: **the positive early `IRGA75` years** (item 12). Evaluated 30-31 Oct
2026 (`90_OVERVIEW/FLUX_NEE_IRGA75_EVALUATION`): no fault found, opco kept, the difference to
FLUXNET explained. The low gap-filled winter nights are explained by humidity (item 12). Still
open from it: the QCL check (item 17).

**To check (from the docs review of 30 Oct 2026):**

- **opco link**: removed from `docs/Software.md` and `docs/Links.md` because
  `github.com/holukas/opco` returns 404. Re-add it when the repository is public.
- **Photographer's name** in the 2019 photo credit (`docs/Yearly_Notes.md` and the title page).
  `check_no_names.py` does not flag it. Decide whether it stays.
- **Humidity numbers** on `docs/L1.1.md`, `docs/L3.2.md` and `docs/Issues.md` were recomputed
  with the definition 2016-2017, below 5 °C, RH at least 99.5 %. Confirm this is the intended
  comparison.
- **Unverified statement** in `docs/Issues.md`: a correction calibrated in 2016-2017 "would add
  100 to 200 gC m-2 per year". No notebook supports it; check or remove.
- **FP2026.2 notebook** in `80_FINALIZE`: decide its content, then build it.

In order. Each item is blocked by the one above it, except that the flux items
2 to 4 do not depend on the meteo item 1: their biomet input,
`EDDYPRO_BIOMET_CH-LAE_2004-2026.09.csv`, is written.

1. **Extend the rest of the meteo stage**: `08` to `13` (`99` already merges
   them as they are, to December 2025, since 27 Oct 2026; extending one means
   changing its stem in the `99` registry), `RADIATION_SENSOR_CONTINUITY`, `TA_HOMOGENIZATION_OPTIONS`, the
   `90_OVERVIEW` notebooks and `build_meteo_dashboard.py`; then the
   `docs/Meteo_Data_*.md` pages and dashboards of those variables, including
   the `VPD` page for the two columns of `07`. The `05`
   seasonal-cycle cut (section 3.1) goes with this pass.
2. **Settle the open points of the `IRGA72` Level-1 re-run.** The re-run is
   complete: 18 runs over 2016 - Sep 2026, one per setup period, in
   `0_data/IRGA72-Level-1_fluxnet_2016-2026.09/`, with `2022_2`, `2022_3` and
   `2022_4` as separate runs (notes 7, 12). The runs through `2025_1` read
   `EDDYPRO_BIOMET_CH-LAE_2004-2025.csv` and the `2026_1` run reads
   `EDDYPRO_BIOMET_CH-LAE_2004-2026.09.csv`, which over 2004-2025 differs from the
   2025 file only in model fills, reconstructions and the probe half-hour of
   16 May 2025 (`40_EXPORTS`, comparison section). The wrong calibration gas of
   note 15 (factor 0.974 on the CO2 concentration, 14 Dec 2017 - 15 Mar 2019) was
   corrected during the conversion of the raw data to ASCII with bico, so the
   runs read corrected concentrations. Still open: **`H` from 10 January to 20 March
   2019 (revisit later)**. The
   Level-0 file of `2019_2` yields about 289 half-hours of `H`, but `2019_2` has no
   Level-1 run, so the Level-1 input of the flux chain has no `H` at all in this
   period. Decide whether `2019_2` gets a sonic-only run, as `2018_3` did, and
   whether the `H` of the LI-7500 run `2019_3` (17 Jan - 20 Mar 2019, same sonic)
   fills the rest of the gap; `35_FPPC` would then need that run in its input.
3. ~~**Carry `20_L1_FLUXES/IRGA72` to September 2026.**~~ Done 25 Oct 2026.
   `99_IRGA72_L1_MERGED_2016-2026.09` merges the Level-1 runs; where two runs
   overlap at a year boundary it takes each record whole from one run, split at
   midnight, because the runs' values differ there.
   `00_FPPC_IRGA72_INPUT_2016-2026.09` joins it with every column of
   `99` from 1 January 2016 00:15 (the flux columns are empty until 11 January)
   and must be re-run whenever `99` changes. The
   Level-0 merge (`00_L0_CHECKS/IRGA72/01`) still joins its overlapping runs cell
   by cell with `combine_first`; Level 0 is preliminary, so this matters only
   where a Level-0 value is quoted.
4. **Review the `IRGA72` flux chain and the finalize set.** `05_FPPC` (`NEE`, with the
   Pastorello uncertainty), `25_FPPC` (`LE` and `ET`) and `35_FPPC` (`H`) ran on
   2016 - Sep 2026 (26 Oct 2026), all reading
   `00_FPPC_IRGA72_INPUT_2016-2026.09` with the homogenised `TA` and
   `VPD` as drivers; `NEE` uses the fixed 2016-2024 u* thresholds of FP2026.1 until the
   thresholds of FP2026.2 are in place (item 18; decided 1 Nov 2026, replacing the decision
   of 26 Oct 2026 to keep them).
   Each writes only the columns it adds, and `99_FPPC_IRGA72_MERGED_2016-2026.09` in
   the same folder merges these (158 columns). `80_FINALIZE/10_FLUXES_and_METEO_2004-2026.09`
   collects the meteo of `99`, the `IRGA72` Level-1 fluxes of `22.1` and that file
   into one file from 2004 (548 columns); release datasets are cut from it by
   period. `80_FINALIZE/20_CH-LAE_FP2026.1_2016-2026.09` cuts the FP2026.1 dataset
   `CH-LAE_FP2026.1_2016-2026.09` (parquet and CSV, with the `20_` prefix), keeping
   the variables with a value in 2016 - Sep 2026; its column names are not final yet.
   The `_INFO.md` files of both give each variable's unit and description, from
   `80_FINALIZE/variable_info.py`; `*_CORRDIFF` and `FILE_TIME_DURATION` are still
   to be checked against the EddyPro documentation. The meteo reaches it only
   through `99`, which merges all thirteen products; `08` to `13` end in December
   2025 until they are extended. It now also collects the `IRGA75` Level-1 fluxes, the opco
   columns and the stage merge of both analysers (to be re-run, section 4.2). Still
   to check: `H` in 2024
   is about a third lower than in the other years.
   Level-4.2 partitioning is not part of this version of the dataset (decided
   26 Oct 2026). On 29 Oct 2026 the `NEE` notebook was renumbered `01_FPPC` -> `05_FPPC`,
   the number of the `IRGA75` chain (`LE` and `H` became `25_FPPC` and `35_FPPC`), and partitioning was switched on for FP2026.2; it has
   run in both `05`, still with the FP2026.1 thresholds. Before `99` and `80_FINALIZE` run on its output, `variable_info.py` needs
   descriptions of the partitioning columns (`describe_all` stops on undescribed columns), and
   the FP2026.1 cut (`80_FINALIZE/20`) must not be rerun, or must leave those columns out, so
   that the released FP2026.1 stays reproducible.
5. **Decide the candidate list in 3.3**, then freeze the variable inventory and
   write `docs/Variables.md`.
6. **Energy-balance-closure correction of `LE` and `H`** (future session, not part
   of FP2026.1 for now). Pastorello et al. (2020): `EBC_CF = (NETRAD - G)/(H + LE)`
   from half-hours with measured `NETRAD` and `G`, filtered at 1.5 times its IQR, then
   three hierarchical methods (±15-day window at 22:00-02:30 and 10:00-14:30; ±5 days
   and ±1 h; ±5 days in the neighbouring years), giving `LE_CORR`, `H_CORR` and their
   25th and 75th percentiles. The `LE` and `H` random and joint uncertainty of
   ONEFlux belong to the same step (the joint one is built from the `_CORR25` and
   `_CORR75` spread). Needs the `NETRAD` and `G` products at September 2026.
7. **Fill the stub pages**: `Supplementary` is still a stub (out of the sidebar
   since 31 Oct 2026). The other pages,
   including `L1`, `QCF`, `Raw_Data`, `Overview`, `Dataset_Versions`, `Software`
   and `Links`, were written on 27 Oct 2026; `Management_Data` was removed, as
   there are no management data.
8. **Sensitivity of the annual `NEE` sums to the number of XGBoost trees** (future
   session). The number of trees is now chosen by blocked cross-validation (the
   minimum of the error on held-out 14-day blocks; in the runs of 29 Oct 2026, 110, 100
   and 120 trees for `IRGA72` `NEE`, `LE` and `H`, and 90, 100 and 100 for `IRGA75`; the
   count is chosen anew in every run). Between 60 and 110 trees the blocked error changes by less than 1 %,
   but the difference XGBoost - MDS over 2016 - Sep 2026 (`CUT_50`) moves from
   +265 to +685 gC m-2, almost all of it from daytime gaps. Compute the annual sums at
   several numbers of trees (e.g. 60, 80, 110, 150, 250) to see how firm the 110-tree
   result is before publishing; if they spread widely, consider averaging models
   trained with several seeds or tree counts. **First result (T11, T12, 6 Nov 2026, `IRGA75`):**
   50 and 200 trees span about 60 to 120 per year around the 80-tree result, far more than the
   seed spread (results under step 2). No further tree-count runs (decided 7 Nov 2026). Still open:
   whether to state the span as an uncertainty.
9. **Wet-weather gap of the `IRGA75` gap-filling.** Stated in `docs/Issues.md`
   (2016-2017: about 40 gC m-2 apart on shared half-hours, 180-190 gC m-2 per year
   apart gap-filled). Numbers of the first run of chain `05` (29 Oct 2026, before the
   opco fit without `VPD`): -38 gC m-2 shared, 179 (2016) and 194 (2017) gC m-2
   gap-filled. **Superseded (run of 1 Nov 2026, FP2026.2 thresholds):** -16 and -13 on shared
   records, -436 and -370 gap-filled. Of the gap, -347 and -293 lie in records that neither
   analyser measured, and -66 and -75 in records only the LI-7200 measured (item 21). Of the half-hours
   only the `IRGA72` measured, half have no `IRGA75` flux and 30 % an AGC above 90.
   Wetness drivers alone do not help (opco tests). To do: calibrate an adjustment of the filled `IRGA75` values on the
   2016-2017 half-hours where only the `IRGA72` measured (drivers: precipitation in
   the preceding hours, RH, reason for the gap, day or night, `TA`, season), test it
   across years (fit on 2016, check 2017, and the reverse), with and without the
   half-hours with rain, since the shared sonic may be wet then and the `IRGA72`
   fluxes may be affected too. Apply it to 2004-2015 only if it closes most of the
   gap in both directions; otherwise state the bias as an uncertainty of the
   `IRGA75` years (now the state of `docs/Issues.md`). The `RECO` and `GPP` bias of
   the night-time partitioning needs its own adjustment or stays a stated uncertainty.
   Related: the test R² of chain `05` (0.59
   against 0.73 for the `IRGA72`) is lowered by the records with AGC from 50 to 90,
   whose scatter against the `IRGA72` is four to seven times that at AGC 50.
   The QCF 0 and 1 decision (29 Oct 2026) is in `docs/L4.1.md`. Scratch prototypes (29 Oct 2026): gap-filling the `IRGA75` with one
   model over all years plus the `IRGA72` at the `IRGA75` gaps of the other overlap
   year closed 2017 to -13 and 2016 to -92 gC m-2 (cross-year); the rest of 2016 lies
   in cold days of October to December, where the opco correction falls short
   (freezing fog; no opco variant and no fog screen fixed it).
10. **H2O fluxes of the two analysers** (future session; for now both are accepted as
    they are, decided 29 Oct 2026). The difference and its likely cause (tube damping
    in the LI-7200 at high RH) are stated in `docs/Issues.md`. To do: compare the energy balance closure
    (`H + LE` against `NETRAD - G`) of both analysers in 2016-2017, by RH class; the one
    that closes better at high RH has the more realistic `LE`. Also note that the
    `IRGA75` loses more wet half-hours (63 % of half-hours with a valid `LE`, against
    70 %), which biases its gap-filled `LE` low.
    **First result (30 Oct 2026, `90_OVERVIEW/FLUX_ET`):** at RH ≥ 95 % the closure is
    0.74 for the `IRGA75` and 0.52 for the `IRGA72`, and the ratio of `IRGA75` to `IRGA72`
    `LE` rises with RH (2.15 at RH ≥ 95 %). The `IRGA75` `LE` is therefore the more
    complete one at high RH, and its gap-filled `LE` is more likely biased high than low;
    the sentence above needs checking. **Checked (1 Nov 2026):** not supported. Against a climate
    baseline from the LI-7200 years, LI-7500 `ET` lies 131-161 mm per year above, and on shared
    daytime records at RH >= 99.5 % the energy balance closure is 0.69 (LI-7500) against 0.45
    (LI-7200). The `ET` step at the change of analyser (-126 mm) is instrumental. The `ET` anomaly
    of 2008-2010 (+246 to +366 mm) is unexplained. Annual `ET` 2016-2017: 748 mm (`IRGA75`) against
    610 mm (`IRGA72`).
11. **Cold-night `NEE` of the `IRGA75` years** (found 29 Oct 2026 in
    `90_OVERVIEW/FLUX_NEE`; the limitation is now stated in `docs/Issues.md`). Done
    on 29 Oct 2026: opco refitted without `VPD` (with `VPD` it corrected the cold nights
    of 2004-2015 by only about a third of the 2016-2017 value); four fog episodes removed
    by hand in `05`, `25` and `35` (`docs/L3.2.md`); the `NEGNIGHTS` test of whole nights
    added to `IRGA75/05`; it removed 75 nights in the run of 30 Oct 2026, mostly October
    to February. **Relaxed and run on 30 Oct 2026** (both `05`): test 5 removes a record
    below -4 times max(`FC_RANDUNC_HF`, median `PAS20` of the nighttime records of its calendar
    month), for `IRGA75` combined in quadrature with `OPCO_SIGMA` = 1; test 6 removes a night
    whose median lies below -3 standard errors, with n reduced for a lag-1 autocorrelation of 0.2
    and `OPCO_SIGMA` added in quadrature as an error shared by the night (new diive option
    `systematic=`). Removed in the runs: `IRGA72` 43 records (was 182); `IRGA75` 159 records (663)
    and 16 nights, 250 records (75 nights, 1,150 records), all but one night from October to
    February. Annual `CUT_50` XGB sums after the run: `IRGA75` 2004 +40, 2005 +62, 2006 +43,
    2007 -180, 2008 -57, 2009 -57, 2010 -168, 2011-2015 -255 to -338, 2016 -397, 2017 -232;
    `IRGA72` 2016 -159, 2017 +71, 2025 -343. Direct effect on the sums (removed records kept, at
    the current gap-filled values), before any change of the gap-filling models: about -3 gC m-2
    per year for `IRGA72`, -7 to -20 for `IRGA75` (-179 over 2004-2017). In 2016-2017 the new
    night test removes 2 `IRGA75` nights, both with positive `IRGA72` `NEE`, and applied to the
    `IRGA72` none; the old one removed 9, 2 of them on nights where the `IRGA72` was negative too,
    and 11 `IRGA72` nights. It lets through 7 nights (four in December 2016, three in October to
    December 2017) with medians of -0.6 to -5 (one at -7.6 with only 5 values, not tested) on
    which the `IRGA72` read +1 to +4; the uncertainty alone does not single them out (humid-night
    test proposed, item 19). The training screen in `01` keeps the old
    test 5. **Bias checked (1 Nov 2026, on the `05` outputs of 31 Oct, scratch):** after the other
    tests and u* at `CUT_50`, test 5 removes 0.03 % (`IRGA72`) and 0.21 % (`IRGA75`) of the night
    records, test 6 0.09 %, at means of -21, -25 and -9 umol m-2 s-1, far below the noise tail
    (-4 to -8); no measurable upward bias of the night sums (now on `docs/L3.2.md`). A symmetric
    test around `RECO_NT`/`RECO_DT` was rejected (removes 3-4 %, mostly real flushed CO2). **`T2` (2004-2006) re-run with the relaxed tests (30 Oct 2026):** test 5 removes 22
    records (was 160), test 6 5 nights, 71 records (15 nights, 221 records); the inputs to
    Level 3.2 are unchanged. `CUT_50`, XGB, gC m-2: 2004 +36 (was +78), 2005 +69 (+169), 2006
    +44 (+130); `CUT_16` 2006 is -9. The drop of 42 to 100 per year is five times the direct
    effect estimated above: most of it comes through the gap-filling model, which now learns
    from the kept negative night values (62-67 % of the records are filled). 2005 and 2006
    remain sources. **`T3` (2012-2014) re-run the same way:** test 5 removes 26 records (was
    125), test 6 no night (12 nights, 185 records); the lag-1 autocorrelation there is 0.10
    against the 0.2 assumed. `CUT_50`, XGB, gC m-2: 2012 -303 (was -223), 2013 -295 (-155),
    2014 -304 (-141), so -80 to -163 per year, again mostly through the gap-filling. Still open:
    calm cold nights (wind below 2 m s-1,
    below 0 degC) remain about 1 umol m-2 s-1 below the `IRGA72` after the refit; fix in
    opco (cold-night term or more cold training rows) rather than in the chain. The
    period medians in `FLUX_NEE` (+0.08 against +1.67 umol m-2 s-1 below 0 degC) and
    the upper bound of about 50 gC m-2 per year predate the refit; recompute them after
    the merges are re-run (section 4.2).
    **Investigated 3 Nov 2026** (`research/reports/coldnight_2026-11-03/`, parts A-C and a review D;
    cold nights = Nov-Mar, TA < 2 degC; reference an LI-7200 night model trained on 2018-2026
    without RH):
    - **Term:** the spectrally corrected raw covariance w'rho_c' carries the whole bias. The WPL
      terms, storage, CO2 and H2O scale, calibration curvature, mean density, spectral factor,
      time lag and the thermistor air temperature together give at most about 0.1. The WPL thermal
      term has the opposite sign. Not ruled out: heat entering the path that the sonic does not
      see, or a non-thermal signal in the CO2 channel (no raw data to test).
    - **Drivers, in the covariance, nearly independent (r = -0.10):** cloud cover (-2.9 to -3.6 per
      unit of cloudiness from LW_IN and TA), calm air (-2.1 to -2.7 at WS < 1 against 4-6 m s-1)
      and a wet window (AGC >= 56.25, -2.5 to -3.7, 8 % of kept cold records). Frost adds nothing
      robust once cloud is in. opco's heat part depends on wind and removes most of the calm part;
      the cloud and wet-window parts remain in the product. Clear cold nights are about unbiased
      from 2008. The same per-condition bias is present in the overlap.
    - **Time:** with conditions held fixed, no trend or break from 2005/06 to 2016/17 (-0.02 +-
      0.05 per winter). The apparent shrinking to the overlap came from RH-based selections: the RH
      sensor change of January 2016 (Rotronic to CS215) makes RH >= 99.5 % on cold nights 46-78 %
      after and 3-29 % before, also in the homogenised RH. 60-80 % of the low mean of kept
      pre-2016 cold nights is composition (colder winters, which the LI-7200 model also predicts).
    - **Effect in the product:** published cold-night `NEE` 2004-2015 about 1.2 umol m-2 s-1 too
      low, **about -53 gC m-2 per year** (LI-7200 placebo 0 +- 13; an emulator-free cell match
      gives -54); 89 % of it is in gap-filled overcast nights. Nights above 2 degC are not covered
      (the all-night deficit is about -147).
    - **Proposed, not decided:** a night term in opco on cloudiness, zero under a clear sky (about
      +2.2 to +2.5 per unit), fitted on the overlap; a cloud feature for the gap-filler; screen
      wet-window night records (AGC >= 56.25); no RH thresholds across 2016. Without these, state
      about +53 gC m-2 per year as a one-sided uncertainty towards less uptake. To test first: the
      gap-filling rerun with the cloud feature, nights above 2 degC, and why V25 of fppc report B
      (a Burba-type LW night term) nets about 0 on cold nights.
12. **The positive early `IRGA75` years and the size of opco** (evaluated 30-31 Oct 2026). The
    evidence is consolidated in `90_OVERVIEW/FLUX_NEE_IRGA75_EVALUATION` (it links the transfer,
    damping and raw-data notebooks in `30_.../IRGA75/` and the three other
    `90_OVERVIEW/FLUX_NEE_IRGA75_*` notebooks); the full investigation log is in the git history of
    this file (before 31 Oct 2026). Summary (`CUT_50`, XGB, gC m-2 per year):
    - **The gap:** 2004-2006 average +48, 168 above the `IRGA72` years (-120); FLUXNET 175-240
      more negative, Etzold et al. (2011) about 380 more negative; the biometric NEP of 2006-2009
      240-450 above the net uptake of this product.
    - **Ruled out:** analyser damping (at most 34-54 % of the summer daytime gap of 2005-2007), loss
      of covariance in the raw data, the low CO2 reading of 2004-2007 (11-62 per summer, either
      direction), clocks (within ±15 min of MeteoSwiss), opco driver shifts across 2016 (-32 to +5).
      One LI-7500 head (75H-0640) 2004-2017, no exchange or factory recalibration; field
      calibrations, a refastening in December 2010 and two demountings in 2011 are recorded.
    - **opco without `VPD`** is kept: `VPD` = 0 marks the RH probe at its ceiling, not the weather,
      and with `VPD` the cross-year skill is worse. Dropping it is not the main cause of the
      positive early years (with `VPD`, 2004-2006 stay sources).
    - **Size of the correction:** the summer wind test gives s = 0.20 ± 0.48 for 2005-2007 and about
      1 from 2008; the winter test 1.41 ± 0.60 (against the training months) and 1.23 ± 0.30
      (against the middle winters) for 2004/05-2006/07. The wind test is the weaker one. The
      corrected nights lie at 0.79-1.08 of the respiration expected from the `IRGA72` years, the
      uncorrected cold nights at 0.03-0.72; a possible night over-correction (at most 57-118, 2008)
      does not reach the annual sums. The Etzold et al. correction adds 210-302 against 638 for
      opco; with it this product gives -466 to -374 against their -418, so most of the difference
      to them is the size of the correction. The `IRGA72` years support opco in winter.
    - **Against FLUXNET:** +214 in 2005-2015, of which +131 is night gap-filling and +39 the
      negative winter nights FLUXNET keeps; FLUXNET's 2004-2015 winter nights are implausibly low.
    - **Decided for FP2026.2:** opco unchanged; 2004-2009 kept as processed, without flag or added
      uncertainty; the summers May-Sep 2005-2007 stated as uncertain by 0 to about -200 (done on
      `docs/L1.1.md` and `docs/IRGA75_Comparisons.md`). A real loss of uptake capacity after 2003
      is plausible for 2004-2006 only.
    - **Open:** the QCL periods of 2005 and 2008 as an independent check (item 17); the winter
      night gap-filling of `IRGA75/05` (gap-filled winter nights 0.67 umol m-2 s-1 below the
      measured ones). *Cause found 31 Oct 2026 (scratch `winter_nights.py`):* humidity. The
      LI-7500 loses most humid nights (RH >= 99.5 %: 8 % of its measured, 25 % of its filled
      Nov-Mar nights), and the few it measures read near zero (-0.06 umol m-2 s-1, against 3.28
      for the LI-7200 at the same RH). XGB learns "humid = near zero" and fills the many humid
      nights that way; the RH composition explains -0.65 of the -0.68, within RH classes filled
      and measured agree. In the `IRGA72` years filled and measured nights agree (+0.08). Rough
      effect: 50-70 gC m-2 per year towards uptake in 2004-2015. **Superseded (1-2 Nov 2026,
      item 21):** that estimate covered November to March nights only. Against the climate baseline,
      the night deficit is about -200 gC m-2 per year in all `IRGA75` periods, and it lies mostly in
      gaps without any LI-7500 data (rain). The root is the known bias of
      humid cold LI-7500 nights (`docs/Issues.md`), not the gap-filling; foggy cold nights corrected about 0.5 umol m-2 s-1 too little and clear ones
      too strongly without `VPD` (a longwave fog ratio as driver removes most of it, not usable in
      2004-2005); whether 2004, which starts on 30 March, gets an annual sum; possibly a flag for
      May-Sep 2005-2007; a better correction of the early years in a later version (candidates: a
      climate-expected baseline trained on the `IRGA72` years, satellite greenness, dendrometer
      and inventory data).
13. **Partitioning: minimum records per `Rref` window** (found 30 Oct 2026 in
    `90_OVERVIEW/FLUX_RECO`; a fix in diive). The nighttime method refits `Rref` in
    8-day windows and fits a window from as few as 3 nighttime records
    (`diive/flux/partitioning/nighttime_oneflux.py`, `_reanalyse_rref`, as in ONEFlux). In
    winter such windows give `Rref` near zero (floored at 1e-6) or spikes, and the
    interpolation carries them into the days around: 25 windows with near-zero `Rref`, and
    winter spikes such as 12 January 2006, mostly in the `IRGA75` years. To do: count the
    records per window in the CH-LAE years and choose the count from which `Rref` is stable;
    add an optional minimum to diive (default 3, so ONEFlux is still reproduced); set it in
    both `05`. **Not for FP2026.2** (decided 31 Oct 2026): this version keeps the ONEFlux
    default; deferred to a later version.
14. **Implausible fluxes found in the overview notebooks** (30 Oct 2026):
    - Daytime `GPP` of 2005, 1,786 gC m-2 (`90_OVERVIEW/FLUX_GPP`). Cause (31 Oct 2026): the
      daytime method fits only on measured `SW_IN`, which starts on 14 Sep 2005 (CNR1); January
      to August 2005 get the parameters of the first windows after that, extrapolated onto
      modelled light, and 2004 has no fitted window. **Fixed 31 Oct 2026:** `IRGA75/05` sets
      all daytime partitioning columns to missing before the first measured `SW_IN`
      (`DT_VALID_FROM = '2005-09-14 11:15'`, Step 8, right after the partitioning).
    - Nighttime `H` up to about 800 W m-2, mostly 2013-2016, passes all tests
      (`90_OVERVIEW/FLUX_H`). Candidate: a test of positive nighttime `H` in diive.
    - Extreme candidate outliers in `30_.../99_FPPC_MERGED_2004-2026.09` (found 31 Oct 2026). The
      notebook circles measured half-hours more than 7 robust standard deviations from the 31-day
      median of the same hour (`OUTLIER_K`), about 2 to 90 per flux and year, and removes nothing.
      The most extreme are implausible and still in the record: `NEE` of +35 to +48 and -25 to -41
      umol m-2 s-1, mostly in winter of the `IRGA75` years; nighttime `LE` up to about 800 W m-2
      (e.g. 2011-12-16, 2011-08-05); nighttime `H` up to 800 W m-2 (2015-10-14, see above). To do:
      review the top candidates of each flux; if the chain's tests should have caught them, adjust
      or add a test in diive (e.g. a Hampel filter by hour of day) rather than removing them by hand.
      *Why they pass (31 Oct 2026):* the chain already runs `Hampel(by_time_of_day=True)` (`HAMPEL_2`,
      13 days, ±1 half-hour, 5.5 sigma). (1) Records whose window holds fewer than `min_records` = 10
      values are not tested: about 0.5 % of records, but 12 of the 15 most extreme `LE` candidates,
      the three `H` values of 2015-10-14 and 2 of 15 `NEE`. (2) The others are tested against a window
      still full of the noisy records that USTAR and later tests remove (2007-12-27 `NEE` +35.7: robust
      sd 9 at Level 3.2, z 4; 0.8 in the final series, z 46). *Decided:* the absolute limits stay as
      they are (no nighttime limits). *Added 31 Oct 2026, run 1 Nov 2026:* a third by-time-of-day Hampel
      (`HAMPEL_3`, 31 days, 7 sigma) after `HAMPEL_2` in `05`, `25` and `35` of both analysers, and
      in `variable_info.py`, `docs/L3.2.md` and the version pages. A reconstruction at Level 3.2
      caught 13-15 of the 15 most extreme candidates per flux and flagged about 300 (`NEE`), 430
      (`LE`) and 290 (`H`) records more than `HAMPEL_2`. **Run 1 Nov 2026:** it removed 187 (`NEE`),
      251 (`LE`), 211 (`H`) records of the `IRGA72` and 363, 541, 436 of the `IRGA75`. The night `LE`
      and `H` of up to about 800 W m-2 are gone (largest night `LE` left about 220, night `H` about
      490 W m-2, `IRGA75` winters 2013-2014). **Still open:** night `NEE` of about ±40 to ±49
      umol m-2 s-1 remains (e.g. `IRGA72` 2018-06-18 03:45 +40.3, `IRGA75` 2007-11-25 06:45
      -49.2); review the top candidates in `99_FPPC_MERGED`.
15. **Small fixes**: diive `RidgeLinePlot` places its labels too high. (The analyser line of
    the `FLUX_NEE` heatmaps and the About text of `METEO_TA` were fixed on 31 Oct 2026.)
16. **Docs structure** (review of 31 Oct 2026; the sidebar order, the version pages and the
    PDF are done):
    - A "Start here" page in place of `index.md`, with how to obtain the data, a citation
      and a licence. Neither a citation nor a licence exists on the site yet: needs input.
    - One page of bad and gap-filled periods, taking the table of `docs/L3.2.md` and the
      long gaps of `docs/L4.1.md`; the evidence stays in the Yearly Notes.
    - Split `docs/Yearly_Notes.md`: the EC setup table to a page of its own (update
      `workflow/00_L0_CHECKS/CLAUDE.md`, which names its location), the deprecated versions
      into one table under Dataset versions, and delete the unedited FLUXNET template
      blocks.
    - The counts of unreleased runs were removed from `docs/L3.2.md`, `docs/L3.3.md` and
      `docs/QCF.md` (31 Oct 2026); the notebooks report them.
    - The 2018 flow-module failure: settled 31 Oct 2026. `docs/L3.2.md` lists the removal of
      17-19 May and the failure from 19 May; the long gap of `docs/L4.1.md` starts on 18 May,
      with the removal.
    - Merge `docs/References.md` into `docs/Links.md`.
    - A summary box at the top of each meteo page: the column to use and the known
      limitations, as `docs/Meteo_Data_TA.md` already has.
17. **Check opco against the QCL periods of 2005 and 2008** (later session; noted
    31 Oct 2026). The EC setup table in `docs/Yearly_Notes.md` lists a second gas
    analyser, a quantum cascade laser, beside the LI-7500: `QCL-L2` and `QCL-L` in
    `2005_2` and `2005_3` (30 Sep to 12 Nov 2005), `QCL-ISO` in `2008_2` and `2008_3`
    (16 May to 30 Jun 2008). If it measured CO2, it is a closed-path flux without
    self-heating in the early years themselves, and a direct test of the size of opco in
    autumn 2005 and early summer 2008. First: read notes (1) to (6) of the setup table
    (Swiss FluxNet site page) and the raw files of these periods to see what the QCL
    measured; then compute its CO2 flux and compare with the LI-7500, corrected and
    uncorrected.
18. **USTAR thresholds of FP2026.2** (decided 1 Nov 2026). The thresholds of FP2026.1 came from
    REddyProc with `UstarClasses = 30` instead of 20, which lowers them; with the defaults the
    same data give 0.3-0.6 m s-1 per year. Decided: thresholds as low as defensible, from the
    ONEFlux moving point method only (diive `mode='oneflux_mp'`), one set per analyser, as fixed
    values; filter by day and by night. Detection and checks in
    `30_FLUX_POST-PROCESSING_CHAIN/USTAR_THRESHOLD_DETECTION_2004-2026.09`, which runs Levels 2 to
    3.2 of both chains itself (with `HAMPEL_3`; a settings check compares them with the `05`
    notebooks), so it does not need the `05` outputs (run 1 Nov 2026): `IRGA72`
    0.4155/0.5230/0.6451, `IRGA75` 0.3099/0.4356/0.5506. Docs updated (`L3.3`, `Issues`, `Variables`, `Software`, the version
    pages). diive: `UstarReddyProcDetection(ustar_classes=, plateau_fwd=)` added to repeat the
    FP2026.1 runs. **Checks done (1 Nov 2026, sections 8-10 of the detection notebook):** constant
    thresholds per analyser confirmed (the year-to-year spread lies within the bootstrap noise);
    pooling years or seasons rejected; the comparison with `RECO_DT` does not constrain the
    threshold, because `RECO_DT` rises with the threshold of the chain run (kept nights matched it
    near `CUT_16` with the FP2026.1 thresholds, near `CUT_84` with the FP2026.2 ones for the
    `IRGA72`); an independent respiration estimate is still needed; a flush of canopy CO2 after calm
    hours shows for the `IRGA75` only, in few cases (section 6). `USTAR_CUT_50` in `90_OVERVIEW/FLUX_NEE_IRGA75_COMPARISONS`
    and `_EVALUATION` set from 0.304 to 0.4356 and both re-run (1 Nov 2026).
    **Done 1 Nov 2026:** thresholds set in `IRGA72/05`, `IRGA75/05` and `T1`-`T3`; both chains and
    everything downstream re-run (with item 14); the detection notebook confirms the applied
    thresholds, `HAMPEL_3` and an identical Level 3.2. Result: the `IRGA72` years show much less
    uptake (annual `NEE`, `CUT_50`, 2016-2025: +3 to +206 gC m-2 against FP2026.1, mean +88;
    2021 -69), several of them a net source (2016, 2017, 2022-2024); 2018-2024 is now close to
    FLUXNET `VUT_REF`. Docs and notebook findings updated the same day.
    **Changed 2 Nov 2026: one set for both analysers,** detected on the merged record (LI-7500
    2004-2015, LI-7200 2016-2025) with the storage screen: 0.3476 / 0.4811 / 0.6011 m s-1. It
    replaces the per-analyser sets and the set 0.3523 / 0.4860 / 0.5990 detected the same day
    without the screen. Set in both `05` notebooks, the `T` notebooks and
    `90_OVERVIEW/FLUX_NEE_IRGA75_COMPARISONS` and `_EVALUATION`; not run yet. On the records both
    analysers measured they give the same threshold within 0.01 m s-1; the per-analyser sets
    differ only by the years they cover. The clean LI-7500 records (+0.019) and opco V25 (-0.002)
    move `CUT_50` by less than the bootstrap spread (detection notebook section 12).
    **Changed 3 Nov 2026: one set per analyser again,** each from its own complete years: LI-7500
    2004-2017 0.3166 / 0.4294 / 0.5487, LI-7200 2016-2025 0.4155 / 0.5264 / 0.6472 m s-1 (scratch
    run with the notebook's code; the 1 Nov LI-7200 set included 2026). **Updated 4 Nov 2026:** the
    run of the detection notebook with the AGC window 40-65 gives the LI-7500 0.3182 / 0.4350 /
    0.5459 (`CUT_50` +0.0056, above the tolerance of 0.005); declared in the detection notebook, both
    `05`, `T1`-`T3`, the two overview notebooks, the figure script and the docs. The LI-7200 set is
    confirmed exactly. Reason: the annual
    thresholds of the merged record step up after 2017 (mean 0.43 in 2004-2017, 0.55 in 2018-2025,
    Welch p < 0.001); the old criterion (scatter between years below the bootstrap spread) cannot
    see a step. Within the LI-7200 alone, 2016-2017 (0.41) against 2018-2025 (0.55) is not
    significant (two years). Not the analyser, not the sonic change of Dec 2019 (USTAR/WS 6 % lower
    after it), sample size about 0.02 of the 0.11; no fieldbook event. Night `NEE` against `USTAR`
    flattens from about 0.6 m s-1 after 2018 and keeps rising before. Tested settings: the plateau
    criterion 0.99 (Papale et al. 2006) and 0.95 (REddyProc) lower `CUT_50` by 0.002 and 0.011; 9
    TA classes (-0.05) and forward mode 1 (0.22) lower it only by letting noise pass the plateau
    test; not adopted. Scripts and outputs in `research/reports/ustar_step_2026-11-03/` (data folder). Set in both `05`, the
    `T` notebooks, the two overview notebooks (LI-7500 `CUT_50`) and the detection notebook
    (settings, section 2 check, new period table in section 11, text); not run yet.
    **Cause of the step (3 Nov 2026, three scratch investigations, `ustar_jump_*` in the same
    report folder): data composition, not the site.** Not supported: climate (thresholds and night TA
    correlate only through time; no relation within either period or within TA classes; matching
    the TA distribution leaves the step), EddyPro settings (identical in all 37 setup periods),
    measured USTAR (USTAR/sigma_w 0.745-0.757 every year), mounting, night definition, storage,
    slope flows, canopy (no 2018 break). Supported: which nights keep a valid `NEE`. From 2018,
    and most from 2022, the LI-7200 keeps windy nights more often (fewer MISSING and signal-strength
    losses; retention at USTAR >= 0.6 from 0.62-0.66 to 0.74-0.80), while the LI-7500 loses windy
    nights to MISSING, signal strength, SPIKE and ABSLIM. More kept records at high USTAR let the
    plateau test pass later: the season thresholds track the share of kept nights with USTAR >= 0.6
    (Jan-Mar r = 0.89), and thinning 2018-2025 to the 2004-2015 retention per season and USTAR
    class brings the step from about 0.16 to about 0 (main run; random thinning of the same count:
    halfway). On identical records the two analysers agree (2016 0.29 / 0.22, 2017 0.39 / 0.37).
    The LI-7200 2016 value is low because spring 2016 is missing. There is no jump from 2017 to 2018 within the LI-7200
    (0.474 and 0.508, bootstrap spread about 0.09); the split at 2018 was a choice. 2018 is high
    for a windy Jan-Mar (40 % of nights at USTAR >= 0.6, against 30 % in 2017); windy winters give high
    annual thresholds (2007, 2018, 2020, 2022; r = 0.40 over all years). Side finding: SSITC removes the
    low-`NEE` calm nights of the LI-7200 (kept 0.74-0.90 against rejected 0.04-0.37 umol m-2 s-1),
    from 2016 on. Decided 3 Nov 2026: keep the per-analyser sets, although they carry this selection
    (a detection on records harmonised in their USTAR retention would give one set for both). Docs (`L3.3`, `L3.3_Constraints`, `Version_Differences`,
    `Version_FP2026.2`) to be updated after the rerun (section 5, step 4).
19. **Humid-night test for the `IRGA75`** (proposed 1 Nov 2026, not decided). In 2016-2017 the
    LI-7500 night `NEE` lies below the LI-7200 in humid cold nights, whatever its sign (median
    difference about -1.1 umol m-2 s-1 below 0 degC and -0.4 at 0-5 degC at RH >= 99.5 %, -0.6
    to -0.9 at RH 97-99.5 %, +0.2 to +0.9 at RH below 97 % below 10 degC); the AGC does not
    separate these nights. Proposal: a cause-based test in `IRGA75/05` that removes all night
    records with `TA` < 5 degC and RH >= 99.5 %, regardless of sign. It would raise the night
    sum by about 30 gC m-2 per year (0-85 by year) at a cost of about 4 % of the night records,
    and `NEGNIGHTS` would then add almost nothing. Waits for the current run of `IRGA75/05` to
    close. The analysis exists only as scratch scripts and a research report in the external
    data folder: move it into a notebook (the 2016-2017 overlap or `IRGA75/05`) before the docs
    cite it. Related: items 11 and 12. **Not to adopt as proposed** (analyses of 1 Nov 2026, item 20):
    removing these nights widens the gap to the LI-7200 by 29 to 127 gC m-2 per year, because the
    gap-filling then extrapolates even lower. **RH is not homogeneous across 2016 near
    saturation** (item 11, 3 Nov 2026): an RH >= 99.5 % test selects different nights before and
    after the sensor change. With cloudiness from LW_IN instead of RH, the humid-night medians of
    fppc report D are about the same in both eras (-1.06, -1.29, -0.99 instead of -2.0, -2.0, -0.8).
20. **Storage term of the `IRGA75`: concentration screen** (set 1 Nov 2026, **not run yet**). The
    LI-7500 storage term summed to -25 to -196 gC m-2 per year (2004-2017), that of the LI-7200 to
    about zero. Cause: with a wet or blocked optical path the LI-7500 reads 33 to 106 ppm too high
    (AGC above 55, rain), and after the gap that ends such an episode the reading returns over a few
    records; the return entered the storage term as a one-sided flux. New diive options in
    `run_level31`: `concentration_valid` and `restart_screening={'skip_after_gaps': n}`. Runs of
    discarded values between two valid readings are replaced by their mean, which keeps their sum.
    Set in `IRGA75/05` (Settings `STORAGE_*`, Step 3: AGC up to 55, no rain in the previous 3 h, RH
    below 99.5 %, not the first 3 records after a gap) and mirrored in the USTAR detection notebook
    (`CHAIN_INPUT['IRGA75']['storage_screen']`, checked against `05`). Test run of the chain (scratch,
    `CUT_50`): storage sums -5 to +39 per year (mean +13); annual NEE +70 per year in 2004-2015 and
    +118 in 2016-2017, which closes about 120 of the 408 gC m-2 per year gap to the LI-7200 in the
    overlap; 2004-2006 become stronger sources (+125 to +226). To do: rerun `IRGA75/05`, `25`, `35`,
    `99`, the stage merge, `80_FINALIZE/10`, the detection notebook (its Level-3.2 check against the
    `05` output fails until `05` is rerun) and the overviews; then update `docs/L3.1.md` and the
    version pages. The test variants `T1`-`T3` do not have the screen. A lower AGC limit for the flux
    (55 or 60 instead of 90) was tested and not adopted: alone it changes the sums by -88 to +128
    per year with mixed signs. Analyses: research reports `fppc_insights_2026-11-01` in the data folder.
    **Robustness (1-2 Nov 2026):**
    - Over 54 settings (AGC 50-60, rain 1-6 h, with or without RH, skip 2-4), the mean storage sum
      2004-2015 stays within -10 to +9 gC m-2 per year.
    - Settings derived from 2016 alone or from 2017 alone leave both years within -44 to +12 of the
      LI-7200 storage. Without the screen the difference is about -500.
21. **Remaining biases of the `IRGA75` after the storage screen** (tested 1-2 Nov 2026 in scratch,
    not adopted). Reference: a climate baseline of day and night `NEE` trained on the LI-7200 years
    (report E); anomalies in gC m-2 per year.
    - **Night: about -210 in every `IRGA75` period** (LI-7200: -39 to +32). The deficit lies in the
      gaps where the LI-7500 measured nothing, mostly in rain. Its model never sees fluxes in rain,
      while the LI-7200 measures them.
      - The opco variant V25 (night heat term from `LW_IN`) changes little.
      - Filling the humid gaps (RH >= 99.5 %) from a LI-7200 model (donor fill) halves the deficit
        and closes the overlap gap to about -100. It also adds +85 to +120 by day, and its effect
        in 2004-2015 cannot be checked.
    - **Day: +208 to +365 in each year 2004-2009, -109 to +120 from 2010** (LI-7200: -278 to +147).
      - The uncorrected flux of 2004-2009 matches the baseline, so opco probably over-corrects these
        days.
      - The summer wind test of `OPCO_TRANSFER_CHECK` gives s = 0.05-0.40 in 2005-2007 and 1.0-1.2
        in 2008-2009 (noise about ±0.6 per year), so it places the step two years earlier than the
        baseline does. No setup change is recorded at either date.
      - Scaling the daytime opco term of 2004-2007 by 0.2 brings those days to -112 to -8. 2008 and
        2009 stay at +219 and +297, and the annual sum jumps from -393 (2007) to +51 (2008).
      - Search for a dated cause (2 Nov 2026, report H): no recorded change of the sensor or its
        mounting explains the step at 2009/2010. The time lag (+0.05 s in every wind sector) and
        the cooler voltage change in 2009, both from the data acquisition or the electronics; the
        re-fastening of December 2010 shows in no signal. The only dated candidate is the
        maintenance of autumn 2007 for the low wind-test years 2005-2007, without a mechanism and
        against the winter test. Not a basis for a correction. To add to section 5 of
        `OPCO_TRANSFER_CHECK` at its next run.
    - **All three together** (storage screen, daytime scaling, donor fill): +34, +48 and -39 in
      2004-2009, 2010-2015 and 2016-2017, a homogeneous record; `NEE` 2004-2015 averages +62
      against -18 for the LI-7200 years. The homogeneity is largely by construction, since the
      baseline comes from the LI-7200 years and a real change of the forest would be removed too.
    - Recommended for FP2026.2: state both biases as uncertainties. If the corrected series is
      wanted, publish it as a sensitivity column. The QCL data needed to test the early years
      (item 17) are not available.
    - Analyses: `F_concentration/report.md`.
22. **Audit of the open-path corrections and tests of three fixes** (2 Nov 2026, scratch, **not
    decided**). Full record: `research/reports/open_path_audit_2026-11-02/REPORT.md` in the data
    folder, with all scripts and outputs.
    - Five checks (EddyPro Level 1, opco code and target, the LI-7200 2016-2017 as reference, the
      chain Levels 2-4.1, literature): all correct or small (below about +-50 gC m-2 per year),
      except the transfer of the daytime opco correction (about +500 per year, fitted on the
      2016-2017 head), probably +330 to +440 too large in 2004-2007. A CO2 zero step of the LI-7500
      on 19 Dec 2007 is the only measured change of the analyser and coincides with the step of the
      wind test.
    - The LI-7500 years carry a day bias (too high, 2004-2009) and a night bias (too low in every
      period: wet gaps filled at 1.5 against 4.8 umol m-2 s-1 measured by the LI-7200, storage term)
      that cancel.
    - Tested: day fix (the Etzold et al. 2011 correction instead of opco by day before 2007-12-19), storage screen,
      wet-night fill (Lloyd-Taylor on own dry nights, or LI-7200 donor). All three together give
      0 / +24 / -30 gC m-2 per year for 2004-2009 / 2010-2015 / 2016-2017, in line with the
      LI-7200 (-18); 2008-2009 stay at +110 to +140.
    - Open: which fixes to adopt, and 2008-2009 (options in section 6 of the report). Supersedes
      the recommendation of item 21.
23. **Divergence of night-time and daytime partitioning: a link to the USTAR filter** (noted 3 Nov
    2026, hypothesis, not tested). Section 9 of the detection notebook: night `NEE` reaches
    `RECO_DT` at a `USTAR` of 0.6-0.9 m s-1 and exceeds it by up to about 60 % above; at the
    FP2026.2 median threshold the kept nights lie 11 % below `RECO_DT` (LI-7200) and 4 % above
    (LI-7500). Both methods depend on the filtered nights, but differently: `RECO_NT` is fitted
    to them directly, so it takes over their level, which keeps rising with `USTAR`; `RECO_DT`
    takes only its temperature sensitivity from them and its reference respiration from the
    daytime light response. A difference between `RECO_NT` and `RECO_DT` (and between `GPP_NT`
    and `GPP_DT`) may therefore follow from the threshold and from the `USTAR` distribution of
    the kept nights, rather than from the partitioning models.
    - To check after the rerun: `RECO_NT` - `RECO_DT` per year and per `CUT_16`/`_50`/`_84`
      scenario (does the difference change with the threshold?); the same difference per `USTAR`
      class of the kept nights; whether years with more kept nights at high `USTAR` diverge more;
      the part of it from flushing after calm hours (section 10).
    - **Checked 8 Nov 2026** (`research/reports/uptake_2026-11-08/R_reco_ntdt/`, scripts and tables):
      partly confirmed. Kept-night NEE rises with `USTAR` without levelling off (NEE/`RECO_NT` 0.70 to
      1.45 for the LI-7500, 0.85 to 1.21 for the LI-7200, also in summer and under sustained
      turbulence). But `RECO_DT` rises with the threshold by about as much as `RECO_NT` (through
      `RREF_DT`), so `RECO_NT - RECO_DT` stays at about -170 (LI-7500) and -300 to -380 (LI-7200)
      gC m-2 per year for `CUT_16`/`_50`/`_84`. No link across years to the `USTAR` of the kept nights
      (|r| <= 0.31); flushing after calm hours touches 5-8 % of the kept nights and does not explain
      it. About half of the difference sits on daytime records and `E0_DT` is 20-60 % above `E0_NT`,
      so the divergence points to the models. Each threshold step raises both RECO estimates by
      about 15 %.
    - If confirmed, state it in the docs (L4.2 and Known limitations) as a cause of the
      divergence, and as one more reason why `RECO_DT` cannot decide the threshold.
24. **Ambient variables and H2O flux of the `IRGA72` runs 2016-2018** (found 3 Nov 2026,
    `research/reports/coldnight_2026-11-03/D_review/`, scripts `d06*`; affects FP2026.1).
    - The runs `2016_2`, `2016_3`, `2017_1+2` and `2018_1` declare `col_air_t=13`, the LI-7500
      thermistor in the shared raw files, so `TA_EP`, `PA_EP`, `RH_EP`, `AIR_DENSITY`,
      `SPECIFIC_HUMIDITY` and `H2O_MIXING_RATIO` equal those of the `IRGA75` runs. From `2018_2`
      the biomet TA is used. `H2O_MIXING_RATIO` is in every run the biomet RH converted at `TA_EP`,
      not an analyser reading; the LI-7200's own mean is `H2O_MEAS_MEDIAN`. The thermistor reads
      2-3 K warm, so the dry-air density of those runs is about 1 % low, and FC, H and LE about
      1 % low in magnitude. This is small, but it is an inhomogeneity of the reference.
    - **The `IRGA72` H2O flux of `2016_2` (11 Jan - 26 May 2016) is about zero.** Monthly medians:
      `FH2O` 0.002 to 0.024 mmol m-2 s-1, `LE` -0.2 to 1.0 W m-2, against 0.17 to 0.73 and 8 to 32
      for the `IRGA75` (checked 3 Nov 2026 on `IRGA72/00`); from June 2016 both are of the same
      order. **Largely known (checked 3 Nov 2026):** `docs/L3.2.md` lists 11 Jan - 26 May 2016 as
      the LI-7200 start-up (installation, low sample flow, blocked inlet filter), removed from
      `NEE` and `LE` of FP2026.2; FP2026.1 flags the low-flow periods (`Version_FP2026.1.md`), and
      its Level-3 `LE` of March and April 2016 is empty. Left to check: the FP2026.1 `LE` of 22 to
      29 January 2016 (Level-3 median 5.3 W m-2 in January), which neither list covers.
    - Conclusions that used `H2O_MIXING_RATIO` as an LI-7200 reading are void: the phase-1 check
      of the self-heating investigation ("LI-7500 within 1 % of the LI-7200"), part B's "LI-7500
      H2O 15-20 % high", and the H2O anomaly of fppc report F. The phase-3 H2O gain uses
      `H2O_MEAS_MEDIAN` and stands, but its anchor cannot be checked against the LI-7200.
    - To do: decide whether the next Level-1 rerun of these setup periods sets `col_air_t` to the
      biomet TA.
25. **Too little daytime uptake of the `IRGA75` years** (7 Nov 2026, scratch, on the product run of
    4 Nov and T4; **not decided**). Full record: `research/reports/uptake_2026-11-07/REPORT.md` in
    the data folder, scripts `inv1`-`inv5`.
    - Where: `IRGA75` period mean minus the `IRGA72` mean of 2016-2025 (gC m-2 per year, `CUT_50`,
      product fill), May-Oct day / May-Oct night / Nov-Apr day / Nov-Apr night: 2004-2006 +303 /
      -50 / +136 / -40; 2007-2009 +136 / -64 / +87 / -17; 2010-2015 +68 / -69 / +18 / -3; 2016-2017
      +66 / -77 / -2 / -47. A daytime gap, mostly in the growing season; the nights are too low in
      every period and hide part of it. At heat scale 0.84 the Nov-Apr days fall to +73 / +48 / -30 /
      -49; the May-Oct days change by 30-45 only.
    - Cause: at matched summer middays (Jun-Aug, SW_IN 500-800, TA 15-25, VPD 0.5-1.5, u* >= 0.55)
      the raw `W_CO2_MEAS_COV` is about 25 % smaller in 2004-2007 than in 2016-2017, rising
      gradually with a step of about -3 umol m-2 s-1 between 2007 and 2008. The opco bias (-2.6 to
      -3.4) and the WPL terms (about +10) are constant. Present in every wind sector. Whether it is
      real (lower light slope, `ALPHA_DT` 0.05-0.07 against 0.08-0.12, FC/LE 10-15 % lower) or
      instrumental (CO2-channel sensitivity before the 19 Dec 2007 calibration) is not decided;
      Etzold et al. (2011), the biometric NEP and a GPP rise of about 35 % within a decade argue
      against a real change.
    - Ruled out: gap-filling (the fill matches the measured records per light class; seeds and tree
      counts, T7-T12), wind sector, spectral correction, time lag, geometry, WPL. USTAR by day
      leaves 50-65 % of the summer daytime modelled, but the fill is unbiased.
    - Side findings: the head excess `TA_EP - TA`, day minus night, is 1.07-1.13 K in 2004-2007
      against 1.3-1.7 K from 2008, which fits s_day 0.76 for 2004-2007. The `SW_IN` clear-sky ratio
      is about 5 % lower before 2014 with the same CNR1; not explained.
    - **Overnight tests of 8 Nov 2026** (`run_tests_T13-T14.sh`, all without error; comparison in
      `TESTS_T13-T14_COMPARISON_2026-11-08`; analyses in `research/reports/uptake_2026-11-08/`, scripts
      and tables only, no report file). Period mean minus the `IRGA72` mean of 2016-2025 (-23),
      2004-2006 / 2007-2009 / 2010-2015 / 2016-2017:
      - Product: +349 / +142 / +15 / -60. T4 (heat scale 0.84): +251 / +61 / -72 / -152.
      - T13 (heat scale 0.76 before 2008, 0.84 from 2008): +206 / +48 / -72 / -157. The lower early
        scale adds about -45 per year in 2004-2007; the May-Oct days of 2004-2006 stay at +262.
      - T14 (daytime covariance of 2004-2007 divided by the matched-midday gain, 0.74 / 0.80 / 0.83 /
        0.77): -165 / -44 / +18 / -48. Annual NEE 2004 -474 and 2007 -443, against +248 and +123 in
        the product. The gain removes the gap and overshoots by about 160 in 2004-2006, since it is
        applied to all daytime records of the year; an upper bound, as intended. 2005-2009 minus
        Etzold et al. (2011): product +633, T4 +548, T13 +522, T14 +357.
      - (a) Step at 19 Dec 2007 (`A_step2007/`): none that the data resolve, in CO2 or H2O. The
        recovery from 2004-2007 to 2008-2009 fits a single break in May-Jul 2008 (at or after the
        16 May 2008 calibration) or a ramp of about +4 % per year equally well. The deficit is in the
        CO2 fluctuation amplitude (`CO2_MEAS_SIGMA` 12-17 % low), not in the w-c correlation (2-7 %),
        and in CO2 more than H2O (-15 % against -4 %, relative to 2011-2015). The three readings of
        the 19 Dec 2007 check lie on a line, so calibration nonlinearity explains at most 1-3 %.
        Against a gain error: summer nights of 2004-2007 equal 2008-2015 (ratio 1.01 +- 0.11), and
        the winter density slope is not lower before 2008. **New:** from winter 2011/12 the raw
        winter CO2 covariance no longer scales with w'T' (density slope 1.2-1.4 before, 0.0-0.9
        after); this bears on opco's heat term, which uses constant parameters. Cause not identified.
      - (d) `SW_IN` homogeneity (`D_swin/`): the CNR1 steps up by about +4 % (3-5 %) between late
        Oct 2012 and mid-Apr 2013, best estimate late Mar to mid-Apr 2013. The co-located PPFD, the
        MeteoSwiss Laegern station and NABEL do not move, so it is the sensor; the later level
        continues into the CNR4 (Dec 2021). Suggested factor 1.04 on measured `SW_IN` from 14 Sep 2005
        to 1 Apr 2013, none on the 2004-2005 fills. The "5 % lower before 2014" of the clear-sky p95
        is this step plus weather. Not the cause of the uptake gap: it falls inside the `IRGA75`
        years and would act the other way. Side findings: a meteo logger clock drift of up to -14 to
        -17 min in 2011 to Jul 2012, reset on 17 Aug 2012 and apparently uncorrected (check against
        the EC clock); a low-sun excess of 8-17 % in winter 2013/14, gone by May 2014.
    - Still open: the `SW_IN` factor and the clock drift in the meteo stage; the winter density slope
      after 2011. Independent constraints (biometric data of Etzold et al. 2011, TreeNet,
      MODIS/Landsat greenness, FLUXNET2015 CH-Lae) are not available at present (8 Nov 2026), so the
      question real or instrumental cannot be decided from outside data.
    - Options if no mechanism is found: fix the nights together with the days (wet-night fill in
      place, a cloud term proposed), and state the per-year daytime uncertainty in step 3; T14 as the
      bound of a matched-condition scaling of 2004-2007, only as a sensitivity column.
26. **A possible closed-path reference in the `IRGA75` years: LI-7200, Dec 2010 to Jun 2011**
    (recorded 9 Nov 2026 from the fieldbook and e-mails; **data not found yet**). Evidence, with the
    documented and the inferred parts separated: `docs/Yearly_Notes.md`, section 2011. The analyser
    was already running at the 16 Dec 2010 calibration; it was serviced and its data downloaded on
    3 May 2011, and its data were downloaded again on 30 Jun 2011. No removal is recorded; e-mails of
    23 Jun and 18 Jul 2011 suggest that it, or a further unit, went to Davos. The EC setup table
    does not list it.
    - State of the search: **in progress** (9 Nov 2026). The check of 4 Nov 2026 (first run of the
      self-heating investigation above) found nothing in the data folder or in the 2011 raw files
      of the site. The fieldbook records these downloads apart from the eddy data. The search now
      continues on another hard disk and in other places. The data may still exist or may be lost,
      and it is open whether they will be found.
    - To do: look for raw or converted LI-7200 data of Dec 2010 to Jun 2011 in the files downloaded
      from the tower, the memory stick backups and the institute archive, and for the calibration
      documents the entry of 16 Dec 2010 refers to.
    - If they exist: use them as a reference for the LI-7500 gain and self-heating in 2010-2011, as
      with the QCL periods of 2005 and 2008 (item 17) and the LI-7200 of 2016-2017. This needs the
      setup of the period (position, tube, flow), which is not documented so far, and attention to
      the sonic problems noted on 15 Mar 2011.
    - Limits: the period covers winter to early summer only. It starts at the end of the +30 % H2O
      gain of May 2008 - Dec 2010 and lies after the low covariance of 2004-2007 (item 25), so it
      tests neither directly.


## 6. Open questions

Carried here because each blocks a scope decision or a published statement.

- ~~**How far back do `SW_OUT_T1_47_1` and `LW_OUT_T1_47_1` reach?**~~ Answered, and
  the first answer was wrong. Only the **raw** fields begin in 2020; the
  MeteoScreeningTool wrote both channels into `ch-lae_processed` back to
  **2005-09-14**, because it read CSVs rather than the raw bucket. `SW_OUT` and
  `LW_OUT` are therefore 2005-2025 products. The same is likely to hold for any
  other field whose raw record looks short, so check `meteoscreening_mst` before
  concluding a record is recent.
- ~~**Are the raw `G_M1..M3_0.05_1` fields the same plates as the processed
  `G_FF1_0.025_1..3`?**~~ Answered by `11`: they are, and over the timestamps they
  share the screened series is bit-identical to the raw one, so "screened by the
  MeteoScreeningTool" means "passed through unchanged" there. That overlap is only
  about 14 % of the pre-rebuild record.
- ~~**Does `G` carry a storage term above the plate?**~~ Decided: no. `11` estimates
  the term and reports its size instead, because adding it would need a measured bulk
  density and a soil temperature above the plate, and this site has neither. An
  energy-balance closure computed from `G` is therefore a closure at plate depth.
- **`G` around 2011/2012: the correction does not make the record homogeneous, and
  the daily-record panel of the dashboard shows it.** Three facts, all from the
  exported file. At the 2012 acquisition change the median daily amplitude of
  plates 1 and 2 falls by three to four times, from 8.4 and 10.3 W m-2 in 2011 to
  2.6 and 3.3 in 2012 and 1.2 and 1.8 in 2013, while **plate 3 does not follow**:
  it runs 15.7, 12.1, 10.8 across the same years. And the reconciled column swings
  between adjacent years, 4.8 in 2011, 5.7 in 2012, 3.4 in 2013, 5.5 in 2014, which
  no soil does. Part of what this entry originally described in 2011 was a separate
  fault, since found and flagged: plate 2 read backwards from June to December 2011,
  and the reconciled column averaged it with plate 1 and nearly cancelled. Those
  records now carry flag `5` and the 2011 swing reads 4.8 rather than 2.0. The 2012
  change itself is unaffected and still unexplained.
  So whatever happened in 2012 did not happen to all three plates equally, and the
  per-calendar-month gains do not repair it. Notebook `11` already reports the
  symptom from the other side: its gain hold-out, fitted on odd years and scored on
  even ones, misses by up to 69 % inside a single setup, which is what a gain
  contaminated by climatology rather than describing an instrument looks like.
  Until this is understood, treat the amplitude of `G` as not comparable across
  2011/2012 in either the measured or the reconciled columns, and do not read a
  trend through it. Three things to try: whether plate 3 escaping the change
  identifies what changed, since it is the plate discarded in 2021 and the only one
  excluded from the reconciled column; whether the fieldbook's 2012-04-25 program
  "with corrected multipliers and offset" names channels anywhere; and whether the
  amplitude loss is a gain change or a loss of coupling, which the plates' response
  to a rain event or to a clear-sky day would separate. Section 3.2.
- **What is `LW_*_COR_T1_47_1` in `ch-lae_processed`?** A longwave correction from
  earlier work that neither `06` nor `13` uses. `13` established only that the raw
  field is already fed from the logger's temperature-corrected channel; what the
  separately stored series adds is still unknown.
- **The 24-day CNR4 window, 14 Dec 2021 - 7 Jan 2022.** The radiometer was exchanged
  on 14 December and its constants reached the logger program on 7 January, so the
  conversion in force between those dates is not established. It now touches four
  products (`01`, `06`, `12`, `13`), all of which flag the interval rather than
  correcting it. `12` tests it against MeteoSwiss and finds the levels **not**
  consistent with the old constant still being applied, which bounds the error but
  does not identify the constant. A correction has to be applied to all four channels
  together. `docs/Instrumentation.md`.
- **What moved `LW_OUT` at the December 2021 exchange?** `13` measures a step in the
  annual means at the CNR1 to CNR4 change and flags it rather than correcting it,
  because nothing measured through the change. Whether it is the instrument or the
  conversion cannot be separated with what is on site.
- **Does the tower barometer or Lägern drift?** After the January 2016 step, the
  departure of tower `PA` from the barometric formula against Lägern grows from
  +0.017 kPa in 2016 to -0.061 kPa in 2025 and -0.074 kPa in January to September
  2026. The formula is computed from Lägern's own pressure, so `05` cannot say
  which side moves, and after 2018 there is no NABEL barometer to separate them.
  The product is exported as measured. Section 3.1.
- **Which CNR1 was on the tower?** `docs/Instrumentation.md` and `06` give SN 020484,
  which is also what the logger program comments say, but the fieldbook row recording
  the 14 December 2021 exchange names CNR1_020522 at a different location. Probably a
  GIN bookkeeping artefact, unreconciled.
- **Sonic orientation from `2005_2`**: note 5 records a possible change from
  209° to 206° and asks for verification. Unresolved, and it falls in the
  `IRGA75` era. `workflow/00_L0_CHECKS/CLAUDE.md`.
- **Was there ever a CO2 profile at the tower?** The storage term of Level 3.1 comes from the CO2
  concentration at one height, so it may miss CO2 that builds up in the canopy in calm hours and is
  flushed out when turbulence returns (item 18, section 10 of the detection notebook: a sign of it
  for the `IRGA75`, none for the `IRGA72` after the rerun of 1 Nov 2026; few calm cases). A better storage term needs a CO2 profile. Ask whether one ever
  existed, and for which years.
- ~~**Shifted raw-file timestamps, July 2013.**~~ Handled for FP2026.2 in
  `30_.../IRGA75/00`, which moves the flux records back by 7 h (`docs/Yearly_Notes.md`).
  The raw files still carry the wrong names: a new Level-1 run from renamed files
  would need that shift removed from `00`.
- ~~**Is `H` in the dataset?**~~ Yes: `35_FPPC` in both chains. Section 4.1.
