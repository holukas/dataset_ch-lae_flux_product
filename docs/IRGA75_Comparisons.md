# Comparisons of the LI-7500 years

::: {.callout-note title="For FP2026.2, in progress"}
The LI-7500 fluxes of 2004-2015 are in progress for FP2026.2 and are not part of FP2026.1. The
numbers on this page come from the run of 1 November 2026 of
[05_FPPC_IRGA75_NEE_OPCO_2004-2017](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/05_FPPC_IRGA75_NEE_OPCO_2004-2017.html)
(`CUT_50`, XGBoost gap-filling), with the u* threshold of FP2026.2 (0.436 m s-1 for the LI-7500,
[Level 3.3](L3.3.md)), the 31-day Hampel filter `HAMPEL_3` and the current tests of negative
nighttime values ([Level 3.2](L3.2.md)). FP2026.1 used 0.304 m s-1. The correction of the
LI-7500 flux ([Level 1.1](L1.1.md)) is used as it is for FP2026.2; improving it for the early
years is planned for a later version.
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
  its nights further, in every season. By day the two products agree.
- **@etzold_carbon_2011** used a self-heating correction about a third the size of the one in this
  product. With their correction, the flux of this product comes close to their annual sum and
  follows their seasonal pattern.
- **The early years show little net uptake.** 2005-2009 average +27 gC m-2 per year, a small net
  release, against a biometric net ecosystem production of +307 to +514 for 2006-2009. Against the
  LI-7200 years the shortfall is in the daytime uptake. The analyser measured correctly; the cause
  is either a real loss of uptake or a correction that is too large for those years.

## Annual sums

| Year | This product | FLUXNET | @etzold_carbon_2011 (Fig. 3) |
|---|---|---|---|
| 2004 (from 14 March) | -167 | -444 | |
| 2005 | +92 | -158 | -340 |
| 2006 | +140 | -124 | -330 |
| 2007 | -112 | -352 | -435 |
| 2008 | +12 | -201 | -354 |
| 2009 | +4 | -270 | -633 |
| 2005-2009 mean | +27 | -221 | -418 (published -415) |
| 2010 | -97 | -441 | |
| 2011 | -175 | -517 | |
| 2012 | -319 | -680 | |
| 2013 | -290 | -545 | |
| 2014 | -148 | -592 | |
| 2015 | -116 | -335 | |

: Annual `NEE` in gC m-2 per year. This product: `IRGA75`. FLUXNET: `NEE_VUT_REF` of the ONEFlux
v1.3 release for CH-Lae; it starts on 14 March 2004, so 2004 is compared from that date. The values
of @etzold_carbon_2011 are read from the end points of their Fig. 3 (±10 gC m-2). {#tbl-annual}

The LI-7200 years 2016-2025 average -18 gC m-2 per year in the current processing (-105 in
FP2026.1); 2018-2024 average -32, against +3 in FLUXNET (`NEE_VUT_REF`). The range given by @etzold_carbon_2011 in the text (-366 to -662) cannot be reconciled
with their published mean, and their Fig. 3 shows -330 for 2006; the figure is used here.

## Comparison with FLUXNET

The FLUXNET release for CH-Lae was built from the earlier product FP2021. For 2004-2015 its input
was the LI-7500 flux corrected for self-heating following @kittler_high-quality_2017; for
2016-2017 it was the LI-7200 flux. FLUXNET then applied its own u* filtering and MDS gap-filling.
Over 2005-2015 this product is 291 gC m-2 per year less negative: -6 by day and +298 at night.

| Cause | Size (gC m-2 per year) | Where it acts |
|---|---|---|
| Nights that both products gap-fill | +219 | +131 of it in November-March |
| Negative winter nights that FLUXNET keeps and this product removes as outliers | +40 | +22 of it in November-March |
| Other records measured in one product only | +12 | night +12, day +1 |
| Self-heating corrections, on half-hours both measured | +11 | night +20, day -8 |
| Daytime gap-filling | +7 | +16 in April-October |
| u* filtering, records between the two thresholds | +2 | night +22, day -20 |

: Causes of the difference to FLUXNET, mean of 2005-2015, from the half-hour by half-hour
comparison in the notebook. The rows add up to the total of +291. {#tbl-fluxnet-causes}

- **Winter nights.** From November to March the FLUXNET nights average 1.2 µmol m-2 s-1 where
  measured and 0.5 where filled. A forest at 0-5 °C still respires. This product has 3.1 where
  measured and 2.5 where filled, and the LI-7200 years 3.4 where measured. The values that FLUXNET
  keeps and this product removes average -2.5 µmol m-2 s-1, and half of them are below zero.
- **Corrections.** On the half-hours both products measured, their corrections agree by day from
  February to September. From October to January the FP2021 correction adds more by day. At night
  the correction of this product adds 0.5-1.0 µmol m-2 s-1, the FP2021 correction 0.1-0.5.
- **u* filtering.** The FLUXNET thresholds of 2004-2015 (0.23-0.35 m s-1) lie below the
  0.436 m s-1 of this product. This product therefore keeps fewer nights as measured, 17-24 %
  against 20-26 %, and these are the windier nights with higher `NEE`. On the records between the
  two thresholds the effect is small, +2 gC m-2 per year (night +22, day -20). The larger effect is
  indirect: gap-filling learns from the windier nights and fills the nights higher. The rerun with the threshold of FP2026.2 (0.436
  instead of 0.304 m s-1) and `HAMPEL_3` raised the difference to FLUXNET from +214 to +291 gC m-2
  per year, mostly in the nights both products gap-fill (+131 to +219). Within FLUXNET, its
  constant threshold of 0.43 m s-1 (`CUT_REF`) gives on average 72 gC m-2 per year less uptake than
  its yearly thresholds (`VUT_REF`) over 2005-2015.
- **2016-2017.** FLUXNET uses the LI-7200 in these years. The LI-7200 of this product is
  35 gC m-2 per year less negative than FLUXNET: +52 by day and -17 at night. The two years differ
  in opposite directions (2016 +169, 2017 -100). On half-hours both measured they agree, at night
  4.90 against 4.92 µmol m-2 s-1. FLUXNET's u* thresholds of these years (0.46-0.50 m s-1) lie
  close to the 0.523 m s-1 (`CUT_50`) of this product for the LI-7200. With the 0.304 m s-1 of
  FP2026.1, FLUXNET was 148 gC m-2 per year less negative, mostly at night; with the threshold of
  FP2026.2 this night difference has disappeared.

FLUXNET's larger sink in 2004-2015 therefore comes from lower nighttime `NEE`, not from more
uptake: by day the two products agree within 6 gC m-2 per year, also in summer. About half of the
difference (+159 of +291) falls in November-March, where the FLUXNET nights are implausibly low.
The rest (+133) falls in April-October, mostly in the gap-filled nights, and grew with the higher
u* threshold of this product.

## Comparison with Etzold et al. (2011)

@etzold_carbon_2011 report the `NEE` of 2005-2009 from the same LI-7500. Their processing differs
in four ways that matter for the annual sum:

| Step | @etzold_carbon_2011 | This product |
|---|---|---|
| Self-heating correction | @burba_addressing_2008, with the surface temperatures and the fraction of @jarvi_comparison_2009 | Fitted to the LI-7200 in the 2016-2017 overlap ([Level 1.1](L1.1.md)) |
| Large winter fluxes (±15 µmol m-2 s-1) | kept in the data, left out of the gap-filling fits | removed as outliers ([Level 3.2](L3.2.md)) |
| Negative nighttime values | removed, together with as many positive ones (trimmed mean) | removed only where they lie clearly outside the measurement uncertainty |
| Gap-filling | light response by day, temperature response at night, running mean below 0 °C | XGBoost ([Level 4.1](L4.1.md)) |

: Processing of @etzold_carbon_2011 (p. 1297) compared with this product. The u* threshold also
differs: 0.3 m s-1 in their study, 0.436 m s-1 (`CUT_50`) for the LI-7500 in this product
([Level 3.3](L3.3.md)). In 2005-2009, 8.3 % of the half-hours are nights with u* between the two
thresholds, which this product removes and fills; the effect on the annual sum is not sized. This
product keeps 21 % of the nights of 2005-2009 as measured, their study 24 %. {#tbl-etzold-methods}

Their correction adds a fixed fraction (0.085) of the heat-flux term of @burba_addressing_2008.
That fraction was derived for a vertically mounted analyser; the LI-7500 at CH-LAE is inclined. It
was recomputed here from an R implementation used in the group, which is assumed to be the version
used for CH-LAE; the agreement below supports this.

| 2005-2009 | Nov-Mar | Apr and Oct | May-Sep | Year |
|---|---|---|---|---|
| @etzold_carbon_2011 (Fig. 5) | +156 | 0 | -574 | -418 |
| This product | +344 | +63 | -380 | +27 |
| This product, before correction | +42 | -36 | -617 | -610 |
| This product, with the correction of @etzold_carbon_2011 | +144 to +192 | -5 to +9 | -539 to -510 | -401 to -309 |
| FLUXNET | +183 | +19 | -423 | -221 |
| LI-7200, 2016-2025 | +391 | +57 | -466 | -18 |

: Mean `NEE` per season in gC m-2. The values of @etzold_carbon_2011 are read from their Fig. 5
(±3 gC m-2 per month). "Before correction" removes the mean correction of each month, by day and
by night, from every half-hour; the row below then adds their correction in the same way, with its
monthly median (first value) or mean (second value). Both rows are approximations.
{#tbl-seasons}

- **The correction explains most of the difference.** opco adds about +640 gC m-2 per year, the
  correction of @etzold_carbon_2011 about +210 to +300. With theirs, this product gives -401 to
  -309 per year against their -418, and follows their seasonal pattern. With the monthly median of
  their correction about 20 gC m-2 remain, with the monthly mean about 110. The other processing
  steps change the sum by a few tens of gC m-2.
- **Year to year the two agree only loosely.** 2009 has the most uptake in their study, 2007 in this
  product.
- **The LI-7200 years decide only in part.** In winter they (+391) are closer to this product
  (+344) than to the smaller correction (+144 to +192). In summer they (-466) lie between this
  product (-380) and the smaller correction (-510 to -539). In the 2016-2017 overlap the uncorrected
  LI-7500 overestimated the summer uptake of the LI-7200 by 19 %, so a correction is needed in
  summer as well.

## Does the correction hold for the early years?

The correction is fitted on 2016-2017 and applied unchanged to 2004-2015. Compared with the
LI-7200 years at the same light and air temperature:

- **The model transfers.** The early summers lie within the conditions of the training years, and
  under the same conditions the correction has the same size in both periods. Fitted on 2016 or on
  2017 alone, it corrects the other year to within 0.05 µmol m-2 s-1 of the LI-7200.
- **From 2007 on the summer daytime flux agrees** within the year-to-year spread of the LI-7200
  years: 0.9 to 1.2 µmol m-2 s-1 less uptake in 2007-2009, 0.2 in 2010-2015.
- **2005 and 2006 have clearly less uptake**, by 2.1 and 2.7 µmol m-2 s-1. The difference is
  already in the uncorrected flux.

Whether the correction is too large in 2005-2007 cannot be settled from the LI-7500 data alone. In
summer the self-heating signal depends on wind speed; in 2005-2007 this dependence is much weaker
and suggests a self-heating about 80 % weaker (scaling factor 0.20 ± 0.44, where 1 means as in the
training years). The winter test of the same years finds full-size self-heating (1.49 ± 0.58). If
the summer test is right, the May-September `NEE` of 2005-2007 is 171 to 195 gC m-2 too positive.

## Why the early years show little net uptake

### Independent estimates

| 2006-2009 | This product | @etzold_carbon_2011 |
|---|---|---|
| Net ecosystem production (−`NEE`) | -11 (USTAR scenarios -38 to +75) | +307 to +514 (four biometric methods) |
| Ecosystem respiration (`RECO`) | 1,661-1,763 | 1,383 ± 338 (their eddy covariance, 2005-2009) |
| Soil respiration / `RECO` | 0.50-0.54 | 0.64 (soil respiration 890) |
| `GPP`, 2005-2009 | 1,582 (nighttime method); 1,469 (daytime method, 2006-2009) | 1,830 ± 448 (their eddy covariance) |
| `RECO` / `GPP` | 1.02 (nighttime); 1.20 (daytime) | 0.76 |

: The LI-7500 years against independent estimates in gC m-2 per year (`CUT_50`, nighttime and
daytime partitioning; the daytime method starts on 14 September 2005, so its means use 2006-2009). Values of @etzold_carbon_2011 from their Tables 4 and 5, converted from
Mg C ha-1. Net ecosystem production is positive for a sink. {#tbl-independent}

- **The sink is too weak.** Even the lowest biometric estimate lies 318 gC m-2 above this product.
- **Respiration is high but plausible.** `RECO` exceeds the soil respiration, as it must. The
  share of soil respiration, 0.50-0.54, is lower than theirs but within its stated range
  (0.49-0.90).
- **`GPP` is too low**, by about 250 (nighttime method) to 360 gC m-2 per year (daytime method). It
  explains about half of the difference to their study; the other half is the higher `RECO` of
  this product.

The biometric values are means between the inventories of 2005 and 2009 on a 1.48 ha plot, smaller
than the flux footprint. The shortfall is still far larger than their stated uncertainties.

### Where and when the uptake is missing

Against the LI-7200 years, 2005-2009 take up about 45 gC m-2 per year less, well within the
year-to-year spread of the LI-7200 years (standard deviation 161).

- **The deficit is in the daytime half-hours** (+210 gC m-2 per year), mostly from May to September
  (+148). The nights take up 165 more than in the LI-7200 years. With nighttime partitioning the
  deficit is `GPP` (295 lower), partly offset by a lower `RECO` (251 lower).
- **It is a lower capacity, not a shorter season.** Light-saturated `GPP` is lower in 2005-2009,
  and 2005 and 2006 lie below every LI-7200 year. The seasonal course of `GPP` relative to its peak
  is unchanged, and leaf-out is not later.
- **Weather explains part of it at most.** The early years were cooler and dimmer, and the soils of
  2004-2006 were dry, after the drought of 2003. But 2010-2015 had similar weather and agree by day
  with the LI-7200 years, and in 2004-2006 the summer `GPP` lies below every other year at the same
  weather, including the dry LI-7200 summers 2018 and 2022.

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

### Winter nights since the current tests

With the current tests of negative nighttime values, more low winter values stay in the record,
and the gap-filling fills the LI-7500 winter nights lower: about 2.5 µmol m-2 s-1 from November to
March, against 3.1 for its measured nights and 3.4 for the measured nights of the LI-7200 years
(2016-2024). The nights of 2005-2009
therefore take up more than the LI-7200 nights, which partly offsets the daytime deficit in the
annual sum.

### What this means

The early LI-7500 years show far less net uptake than the biometric estimates allow. Against the
LI-7200 years the deficit is in the daytime uptake; against @etzold_carbon_2011 about half of it is
lower `GPP` and half higher `RECO`. A fault of the analyser is ruled out. What remains is a real loss of capacity,
plausible for 2004-2006 after the drought of 2003 and in line with the less coupled exchange of
2005-2006, or a correction that is too large for those years. Neither covers 2007-2009 or the full
size of the shortfall. The annual sums of 2004-2009 are the least certain of the record; where a
result depends on the absolute sink strength, prefer the LI-7200 years. These are themselves close
to neutral (-18 gC m-2 per year in 2016-2025) and close to FLUXNET.

## References

::: {#refs}
:::
