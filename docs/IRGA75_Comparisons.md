# Comparisons of the LI-7500 years

::: {.callout-note title="For FP2026.2, in progress"}
The LI-7500 fluxes of 2004-2015 are in progress for FP2026.2 and are not part of FP2026.1. The
numbers on this page come from the run of 10 November 2026 of
[05_FPPC_IRGA75_NEE_OPCO_2004-2017](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/05_FPPC_IRGA75_NEE_OPCO_2004-2017.html)
(`CUT_50`, XGBoost gap-filling with a Lloyd-Taylor model for the wet nights, `_gfXGWN`), with:

- the u* threshold of FP2026.2, 0.435 m s-1 for the LI-7500 ([Level 3.3](L3.3.md)); FP2026.1 used
  0.304 m s-1;
- the 31-day Hampel filter `HAMPEL_3` and the current tests of negative nighttime values
  ([Level 3.2](L3.2.md));
- the correction of the LI-7500 flux ([Level 1.1](L1.1.md)) with its daytime heating part scaled
  by 0.6 before 2008;
- the storage term with its drift corrected
  ([Level 3.1](L3.1.md#drift-of-the-li-7500-storage-term)).
:::

::: {.callout-tip title="Notebooks"}
- [FLUX_NEE_IRGA75_EVALUATION](notebooks/90_OVERVIEW/FLUX_NEE_IRGA75_EVALUATION.html): the whole
  evaluation in one place: the size of the gap, the causes ruled out, the size of the open-path
  correction (self-heating scale per year, respiration, the correction of @etzold_carbon_2011) and
  where the remaining difference lies. It links the notebooks below.
- [FLUX_NEE_IRGA75_COMPARISONS](notebooks/90_OVERVIEW/FLUX_NEE_IRGA75_COMPARISONS.html): the
  comparisons with FLUXNET and @etzold_carbon_2011, overall, by day and by night, per year, season
  and month, with the reasons for each difference.
- [OPCO_TRANSFER_CHECK_2004-2017](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/OPCO_TRANSFER_CHECK_2004-2017.html):
  whether the correction of the LI-7500 flux holds for the early years.
- [ANALYSER_DAMPING_CHECK_2004-2017](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/ANALYSER_DAMPING_CHECK_2004-2017.html)
  and [RAW_DATA_DIAGNOSTICS_IRGA75_SUMMERS](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/RAW_DATA_DIAGNOSTICS_IRGA75_SUMMERS.html):
  whether the LI-7500 measured too little of the CO2 and H2O fluxes in 2004-2007.
- [FLUX_NEE_IRGA75_INDEPENDENT_ESTIMATES](notebooks/90_OVERVIEW/FLUX_NEE_IRGA75_INDEPENDENT_ESTIMATES.html):
  the early years against the biometric and soil-respiration estimates of @etzold_carbon_2011.
- [FLUX_NEE_IRGA75_PARTITIONING_COMPARISON](notebooks/90_OVERVIEW/FLUX_NEE_IRGA75_PARTITIONING_COMPARISON.html):
  `GPP` and `RECO` of the early years against the LI-7200 years.
:::

The LI-7500 years of this product take up less CO2 than two earlier estimates for the same years,
FLUXNET and @etzold_carbon_2011. This page explains each difference and summarises the checks of
the early years. The reference for plausibility is the LI-7200 (`IRGA72`), measured from 2016 and
not affected by self-heating.

In short:

- **FLUXNET** has far lower nights. Its input kept strongly negative winter values, and its
  gap-filling carried them into the filled nights. The higher u* threshold of this product raises
  its nights further, in every season. By day the two products agree closely on average.
- **@etzold_carbon_2011** used a self-heating correction about half the size of the one in this
  product as applied in 2005-2009 (214-308 against 526 gC m-2 per year). With their correction,
  the flux of this product follows their seasonal pattern, and its annual sum moves from +102 to
  between -210 and -116 gC m-2 per year, against their -418.
- **The early years show little net uptake.** 2005-2009 average +102 gC m-2 per year, a small net
  release, against a biometric net ecosystem production of +307 to +514 for 2006-2009. Against the
  LI-7200 years the shortfall is in the daytime uptake. The analyser measured correctly. The
  correction was probably too large by day before 2008: FP2026.2 scales its daytime heating part
  by 0.6 in those years, with 0.4 to 1.0 as the stated uncertainty
  ([Level 1.1](L1.1.md#known-limitations)). With the scale, the daytime flux of the growing seasons
  of 2004-2006 and 2008-2009 still lies about 180 to 220 gC m-2 per year above the LI-7200 years; a
  real loss of uptake cannot be ruled out.
- **The LI-7500 nights are probably too low.** Including the gap-filled nights, they lie below the
  respiration expected from the LI-7200 years in most years, by up to about 230 gC m-2 per year. A
  climate baseline from the LI-7200 years, computed with the correction at full size, gives about
  200 gC m-2 per year in every LI-7500 period. The deficit lies mostly in the humid half-hours that
  the LI-7500 does not measure.

FP2026.2 scales the daytime correction before 2008 but corrects neither the remaining daytime gap
nor the night bias, and states both as uncertainties of the LI-7500 years (see
[Issues](Issues.md#biases-of-the-li-7500-nee-against-a-climate-baseline)). The annual sums of
2004-2009 are the least certain of the record. Where a result depends on the absolute sink
strength, prefer the LI-7200 years, which are themselves close to neutral and close to FLUXNET.

## Annual sums

| Year | This product | FLUXNET | @etzold_carbon_2011 (Fig. 3) |
|---|---|---|---|
| 2004 (from 14 March) | -148 | -444 | |
| 2005 | +54 | -158 | -340 |
| 2006 | +271 | -124 | -330 |
| 2007 | -41 | -352 | -435 |
| 2008 | +126 | -201 | -354 |
| 2009 | +99 | -270 | -633 |
| 2005-2009 mean | +102 | -221 | -418 (published -415) |
| 2010 | +32 | -441 | |
| 2011 | +8 | -517 | |
| 2012 | -32 | -680 | |
| 2013 | -34 | -545 | |
| 2014 | +3 | -592 | |
| 2015 | -13 | -335 | |

: Annual `NEE` in gC m-2 per year. This product: `IRGA75`. FLUXNET: `NEE_VUT_REF` of the ONEFlux
v1.3 release for CH-Lae; it starts on 14 March 2004, so 2004 is compared from that date. The values
of @etzold_carbon_2011 are read from the end points of their Fig. 3 (±10 gC m-2). {#tbl-annual}

The LI-7200 years 2016-2025 average -23 gC m-2 per year in the current processing (-105 in
FP2026.1); the comparison of these years with FLUXNET is on
[Issues](Issues.md#ustar-thresholds-compared-with-fluxnet). The range given by @etzold_carbon_2011
in the text (-366 to -662) cannot be reconciled with their published mean, and their Fig. 3 shows
-330 for 2006; the figure is used here.

## The 2016-2017 overlap

From 11 January 2016 to 12 December 2017 both analysers ran on the same sonic anemometer. The
annual `NEE` of the LI-7500 is -138 gC m-2 in 2016 and -9 in 2017, that of the LI-7200 +48 and
+211. The LI-7500 therefore shows 186 and 220 gC m-2 more uptake. @tbl-overlap-split splits this
gap by which analyser measured each half-hour.

| Half-hours | 2016 | 2017 |
|---|---|---|
| measured by both | -6 | +1 |
| measured by the LI-7200 only | -34 | -37 |
| measured by the LI-7500 only | +8 | +8 |
| measured by neither | -153 | -191 |
| total | -185 | -219 |

: Difference of the annual `NEE`, LI-7500 minus LI-7200, in gC m-2, by which analyser measured the
half-hour (`CUT_50`; LI-7500 `_gfXGWN`, LI-7200 `_gfXG`). The rows add up to the total within
rounding. {#tbl-overlap-split}

About 85 % of the gap lies in the half-hours neither analyser measured, and nearly all of it in the
half-hours that at least one of them gap-filled. The measured fluxes agree closely; the gap is a
property of the gap-filling. It comes mainly from the humid half-hours, mostly in rain, which the
LI-7500 rarely measures ([Issues](Issues.md#the-li-7500-misses-the-wet-half-hours)). The correction
of the storage drift, applied in this run, reduced the gap
([Issues](Issues.md#the-storage-term-of-the-li-7500-drifts)).

## Comparison with FLUXNET

The FLUXNET release for CH-Lae was built from the earlier product FP2021. For 2004-2015 its input
was the LI-7500 flux corrected for self-heating following @kittler_high-quality_2017; for
2016-2017 it was the LI-7200 flux. FLUXNET then applied its own u* filtering and MDS gap-filling.
Over 2005-2015 this product is 426 gC m-2 per year less negative: +31 by day and +395 at night.

| Cause | Size (gC m-2 per year) | Where it acts |
|---|---|---|
| Nights that both products gap-fill | +308 | +189 of it in November-March |
| Daytime gap-filling | +45 | +46 in April-October |
| Negative winter nights that FLUXNET keeps and this product removes as outliers | +43 | +26 of it in November-March |
| Other records measured in one product only | +16 | night +12, day +4 |
| Self-heating corrections, on half-hours both measured | +7 | night +21, day -14 |
| u* filtering, records between the two thresholds | +7 | night +25, day -18 |

: Causes of the difference to FLUXNET, mean of 2005-2015, from the half-hour by half-hour
comparison in the notebook. The rows add up to the total of +426. {#tbl-fluxnet-causes}

- **Winter nights.** From November to March the FLUXNET nights average 1.2 µmol m-2 s-1 where
  measured and 0.5 where filled, although a forest at 0-5 °C still respires. This product has 3.2
  where measured and 3.4 where filled, and the LI-7200 years (2016-2024) 3.3 where measured. The
  values that FLUXNET keeps and this product removes average -2.0 µmol m-2 s-1, and half of them
  are below zero.
- **Corrections.** On the half-hours both products measured, the FP2021 correction adds more by
  day in every month, slightly from March to September and clearly from October to February. In
  2004-2007, where the daytime heating part of the correction of this product is scaled by 0.6, it
  adds 1.0-1.4 µmol m-2 s-1 more by day. At night the correction of this product adds
  0.4-1.1 µmol m-2 s-1, the FP2021 correction 0.2-0.5.
- **u* filtering.** The FLUXNET thresholds of 2004-2015 (0.23-0.35 m s-1) lie below the
  0.435 m s-1 of this product. This product therefore keeps fewer nights as measured, 17-24 %
  against 20-26 %, and these are the windier nights with higher `NEE`. On the records between the
  two thresholds the effect is small (@tbl-fluxnet-causes). The larger effect is indirect:
  gap-filling learns from the windier nights and fills the nights higher. Within FLUXNET, its
  constant threshold of 0.43 m s-1 (`CUT_REF`) gives on average 72 gC m-2 per year less uptake
  than its yearly thresholds (`VUT_REF`) over 2005-2015.
- **2016-2017.** FLUXNET uses the LI-7200 in these years. The LI-7200 of this product is
  26 gC m-2 per year less negative than FLUXNET: +51 by day and -25 at night. The two years differ
  in opposite directions (2016 +129, 2017 -78). On half-hours both measured they agree, at night
  4.91 against 4.94 µmol m-2 s-1. FLUXNET's u* thresholds of these years (0.46-0.50 m s-1) lie
  close to the 0.526 m s-1 (`CUT_50`) of this product for the LI-7200. With the 0.304 m s-1 of
  FP2026.1, FLUXNET was 148 gC m-2 per year less negative, mostly at night; with the threshold of
  FP2026.2 the night difference is small.

FLUXNET's larger sink in 2004-2015 therefore comes from lower nighttime `NEE`, not from more
uptake: by day the two products differ by +31 gC m-2 per year on average, +22 in summer. About half
of the difference (+228 of +426) falls in November-March, where the FLUXNET nights are implausibly
low. The rest (+198) falls in April-October, mostly in the gap-filled nights (+119) and the
gap-filled days (+46).

## Comparison with Etzold et al. (2011)

@etzold_carbon_2011 report the `NEE` of 2005-2009 from the same LI-7500. Their processing differs
in four ways that matter for the annual sum:

| Step | @etzold_carbon_2011 | This product |
|---|---|---|
| Self-heating correction | @burba_addressing_2008, with the surface temperatures and the fraction of @jarvi_comparison_2009 | Fitted to the LI-7200 in the 2016-2017 overlap, daytime heating part scaled by 0.6 before 2008 ([Level 1.1](L1.1.md)) |
| Large winter fluxes (±15 µmol m-2 s-1) | kept in the data, left out of the gap-filling fits | removed as outliers ([Level 3.2](L3.2.md)) |
| Negative nighttime values | removed, together with as many positive ones (trimmed mean) | removed only where they lie clearly outside the measurement uncertainty |
| Gap-filling | light response by day, temperature response at night, running mean below 0 °C | XGBoost, with a Lloyd-Taylor model for the wet nights ([Level 4.1](L4.1.md)) |

: Processing of @etzold_carbon_2011 (p. 1297) compared with this product. The u* threshold also
differs: 0.3 m s-1 in their study, 0.435 m s-1 (`CUT_50`) for the LI-7500 in this product
([Level 3.3](L3.3.md)). In 2005-2009, 8.2 % of the half-hours are nights with u* between the two
thresholds, which this product removes and fills; the effect on the annual sum is not sized. This
product keeps 21 % of the nights of 2005-2009 as measured, their study 24 %. {#tbl-etzold-methods}

Their correction adds a fixed fraction (0.085) of the heat-flux term of @burba_addressing_2008.
That fraction was derived for a vertically mounted analyser, while the LI-7500 at CH-LAE is
inclined. It was recomputed here from an R implementation used in the group, which is assumed to be
the version used for CH-LAE; the agreement below supports this.

| 2005-2009 | Nov-Mar | Apr and Oct | May-Sep | Year |
|---|---|---|---|---|
| @etzold_carbon_2011 (Fig. 5) | +156 | 0 | -574 | -418 |
| This product | +394 | +71 | -363 | +102 |
| This product, before correction | +145 | -11 | -559 | -424 |
| This product, with the correction of @etzold_carbon_2011 | +249 to +298 | +21 to +36 | -480 to -450 | -210 to -116 |
| FLUXNET | +183 | +19 | -423 | -221 |
| LI-7200, 2016-2025 | +385 | +57 | -465 | -23 |

: Mean `NEE` per season in gC m-2. The values of @etzold_carbon_2011 are read from their Fig. 5
(±3 gC m-2 per month). "Before correction" removes the mean correction of each month, by day and
by night, from every half-hour, separately before and from 2008; the row below then adds their
correction in the same way, with its monthly median (first value) or mean (second value). Both
rows are approximations. {#tbl-seasons}

- **The correction explains most of the difference.** opco as applied adds about
  +526 gC m-2 per year, the correction of @etzold_carbon_2011 about +214 to +308. With theirs,
  this product gives -210 to -116 per year against their -418 and follows their seasonal pattern,
  so about 60 % of the difference of 520 gC m-2 per year is the size of the correction. About 210
  remain with the monthly median of their correction, about 300 with the monthly mean. The other
  processing steps sized in the notebook explain only part of this remainder.
- **Year to year the two agree only loosely.** 2009 has the most uptake in their study, 2007 in
  this product.
- **The LI-7200 years decide only in part.** In winter they (+385) lie at the level of this
  product (+394), above the smaller correction (+249 to +298). In summer they (-465) lie at the
  level of the smaller correction (-450 to -480), below this product (-363). In the 2016-2017
  overlap the uncorrected LI-7500 overestimated the summer daytime uptake of the LI-7200 by 15 %,
  so a correction is needed in summer as well.

## Does the correction hold for the early years?

The correction is fitted on 2016-2017 and applied to 2004-2015; before 2008 its daytime heating
part is scaled by 0.6 ([Level 1.1](L1.1.md#how)). The checks below take the correction at the size
learned in 2016-2017 and compare with the LI-7200 years at the same light and air temperature:

- **The model transfers.** The early summers lie within the conditions of the training years.
  Under the same conditions the correction is about 10 % larger in 2005-2009 than in 2016-2017
  (ratio 1.10), mostly from a higher ratio of u* to wind speed. Fitted on 2016 or on 2017 alone, it
  changes the correction of 2005-2009 by at most 0.06 µmol m-2 s-1.
- **From 2007 on the summer daytime flux agrees** within the year-to-year spread of the LI-7200
  years: 0.6 to 1.2 µmol m-2 s-1 less uptake in 2007-2009, 0.1 in 2010-2015.
- **2005 and 2006 have clearly less uptake**, by 2.5 and 3.5 µmol m-2 s-1. The difference is
  already in the uncorrected flux.

The LI-7500 data alone indicate a weaker self-heating in 2005-2007. In summer the self-heating
signal depends on wind speed. In 2005-2007 this dependence is much weaker and suggests a
self-heating about 80 % weaker (scaling factor 0.22 ± 0.33, where 1 means as in the training
years). Single years give -0.05 to 0.40 in 2005-2007 and 0.93 to 1.00 in 2008-2009, with a
standard error of about 0.5 per year. The winter test of the same years gives 0.64 ± 0.32 against
the training winters. A comparison of the raw data with a reference analyser in October 2005 gives
0.4 to 0.7 ([Approaches to the correction](L1.1_Approaches.md#investigations-at-ch-lae)).
FP2026.2 therefore scales the daytime heating part by 0.6 before 2008, which makes the
May-September `NEE` of 2005-2007 92 to 103 gC m-2 more negative than at full size; the value of
the wind test would add about another 100. The range 0.4 to 1.0 is the stated uncertainty of the
annual `NEE` of 2004-2007 ([Level 1.1](L1.1.md#known-limitations)).

The climate baseline, a model of `NEE` trained on the LI-7200 years 2016-2025 with meteorological
drivers only, gives a second view (all periods under
[Issues](Issues.md#biases-of-the-li-7500-nee-against-a-climate-baseline)). It was computed with the
correction at full size, before the scale. On that basis the corrected LI-7500 lies about
+230 gC m-2 per year above the baseline by day in 2004-2009, while the uncorrected flux of these
years matches it; from 2010 the uncorrected flux lies 2 to 3 µmol m-2 s-1 below the baseline. The
baseline places the step at 2010, the wind test and the raw data at the recalibration of December
2007, which FP2026.2 follows. The baseline describes the forest of 2016-2025, so it would also count
a real change of the forest as a bias. A daytime scale of 0.2 for 2004-2007, which would bring those
days to the baseline, was tested and is not adopted (see the same section of Issues). With the
scale of 0.6, the daytime flux of the growing seasons of 2004-2006 and 2008-2009 still lies about
180 to 220 gC m-2 per year above the LI-7200 years.

## Why the early years show little net uptake

### Independent estimates

| 2006-2009 | This product | @etzold_carbon_2011 |
|---|---|---|
| Net ecosystem production (−`NEE`) | -114 (USTAR scenarios -180 to -2) | +307 to +514 (four biometric methods) |
| Ecosystem respiration (`RECO`) | 1,692-1,842 | 1,383 ± 338 (their eddy covariance, 2005-2009) |
| Soil respiration / `RECO` | 0.48-0.53 | 0.64 (soil respiration 890) |
| `GPP`, 2005-2009 | 1,526 (nighttime method); 1,518 (daytime method, 2006-2009) | 1,830 ± 448 (their eddy covariance) |
| `RECO` / `GPP` | 1.07 (nighttime); 1.21 (daytime) | 0.76 |

: The LI-7500 years against independent estimates in gC m-2 per year (`CUT_50`, nighttime and
daytime partitioning; the daytime method starts on 14 September 2005, so its means use 2006-2009). Values of @etzold_carbon_2011 from their Tables 4 and 5, converted from
Mg C ha-1. Net ecosystem production is positive for a sink. {#tbl-independent}

- **The sink is too weak.** Even the lowest biometric estimate lies 421 gC m-2 above this product.
- **Respiration is high but plausible.** `RECO` exceeds the soil respiration, as it must. The share
  of soil respiration is lower than theirs: 0.53 with the nighttime method, within its stated range
  (0.49-0.90), and 0.48 with the daytime method, just below it.
- **`GPP` is too low**, by about 300 gC m-2 per year with both methods. It explains about half of
  the difference to their study (55 % with the nighttime method, 40 % with the daytime method); the
  rest is the higher `RECO` of this product.

The biometric values are means between the inventories of 2005 and 2009 on a 1.48 ha plot, smaller
than the flux footprint. The shortfall is still far larger than their stated uncertainties.

### Where and when the uptake is missing

Against the LI-7200 years, 2005-2009 take up about 125 gC m-2 per year less, within the
year-to-year spread of the LI-7200 years (standard deviation 159).

- **The deficit is in the daytime half-hours** (+196 gC m-2 per year), mostly from May to September
  (+144). The nights take up 71 more than in the LI-7200 years. With nighttime partitioning the
  deficit is `GPP` (359 lower), partly offset by a lower `RECO` (234 lower).
- **It is a lower capacity, not a shorter season.** Light-saturated `GPP` is lower in 2005-2009,
  and 2005 and 2006 lie below every LI-7200 year. The seasonal course of `GPP` relative to its peak
  is unchanged, and leaf-out is not later.
- **Weather explains part of it at most.** The early years were cooler and dimmer, and the soils of
  2004-2006 were dry, after the drought of 2003. But 2010-2015 had similar weather and take up
  about as much as the LI-7200 years over the year, and in 2004-2006 the summer `GPP` lies below
  every other year at the same weather, including the dry LI-7200 summers 2018 and 2022.

### No measurement fault

- **Settings and lags.** The EddyPro settings, the time-lag window and the detected time lags are
  the same in all years; the spectral correction factor is 1.03 in every year.
- **Raw data.** The 20 Hz data of June and July 2005-2007, 2010-2012 and 2016 lose no covariance: at
  the time lag EddyPro used it is 99.9-100 % of its maximum, the cospectra match those of the
  reference years, and instrument noise is below 1 % of the variance. The correlation between CO2
  and H2O is 8-13 % lower in 2005-2006, which neither the time lag nor noise can cause: the exchange
  itself was less coupled in those summers.
- **Calibration.** Until a recalibration in December 2007 the LI-7500 read CO2 about 2 % low in
  2004-2005 and 6 % low in 2006-2007. The field check before the recalibration shows a zero offset
  (zero gas -46.6 ppm, 567.5 ppm reference read as 526 ppm), with the slope within 1 % of the true
  one. A zero offset does not change the measured covariance; through the density correction it
  changes the summer daytime flux by about +0.6 µmol m-2 s-1, away from more uptake. No check is
  recorded for 2004-2006.
- **Concentration in wet conditions.** With wet or blocked windows the LI-7500 reads CO2 too high.
  This makes its storage term drift, which is corrected in this run
  ([Issues](Issues.md#the-storage-term-of-the-li-7500-drifts),
  [Level 3.1](L3.1.md#drift-of-the-li-7500-storage-term)), but changes the flux itself by less
  than 1 %.

### Winter nights since the current tests

With the current tests of negative nighttime values, more low winter values stay in the record.
The gap-filling of this run fills the wet nights of the LI-7500 with a Lloyd-Taylor model. Its
gap-filled winter nights lie on average 0.23 µmol m-2 s-1 above its measured winter nights, close
to the LI-7200 (0.15); the plain XGBoost fill, which filled them lower, is not used (values under
[Comparison with FLUXNET](#comparison-with-fluxnet)). Over the whole year the nights of 2005-2009
still take up about 70 gC m-2 per year more than the LI-7200 nights, which partly offsets the
daytime deficit in the annual sum. Including the gap-filled nights, the LI-7500 nights lie below
the respiration expected from the LI-7200 years in most years. Against the climate baseline,
computed with the correction at full size, the nights of every LI-7500 period lie about 200 to
250 gC m-2 per year low ([Issues](Issues.md#biases-of-the-li-7500-nee-against-a-climate-baseline)).

### What this means

Against the LI-7200 years the deficit of the early years is in the daytime uptake; against
@etzold_carbon_2011 about half of it is lower `GPP` and half higher `RECO`. A fault of the analyser
is ruled out. Before 2008 part of the daytime deficit came from a correction that was too large:
the raw data of October 2005 give 0.4 to 0.7 of the size learned in 2016-2017, and FP2026.2 scales
the daytime heating part by 0.6 before 2008, with 0.4 to 1.0 as the stated uncertainty. The
remaining daytime gap of about 180 to 220 gC m-2 per year in the growing seasons of 2004-2006 and
2008-2009 is not explained. A real loss of capacity cannot be ruled out. Such a loss is plausible
for 2004-2006 after the drought of 2003, in line with the less coupled exchange of 2005-2006, but it
does not explain 2008-2009 or the whole size of the difference to the biometric estimates, FLUXNET
and @etzold_carbon_2011. An independent closed-path measurement of these years, which could decide
it, is not available.

## References

::: {#refs}
:::
