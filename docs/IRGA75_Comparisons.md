# Comparisons of the LI-7500 years

::: {.callout-warning title="Preliminary, for FP2026.2"}
The LI-7500 fluxes of 2004-2015 are in progress for FP2026.2 and are not part of FP2026.1. The
numbers on this page come from the run of 30 October 2026 of
[05_FPPC_IRGA75_NEE_OPCO_2004-2017](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/05_FPPC_IRGA75_NEE_OPCO_2004-2017.html)
(`CUT_50`, XGBoost gap-filling), which still used the stricter tests of negative nighttime values.
With the current tests the annual sums are lower: by 42 to 100 gC m-2 in 2004-2006 and by 80 to
163 gC m-2 in 2012-2014 (test runs `T2` and `T3`). The summer daytime results do not depend on
these tests. The page will be updated after the next run.
:::

::: {.callout-tip title="Notebooks"}
- [FLUX_NEE_IRGA75_COMPARISONS](notebooks/90_OVERVIEW/FLUX_NEE_IRGA75_COMPARISONS.html): the
  comparisons with FLUXNET and @etzold_carbon_2011, and the recomputed correction of that study.
- [OPCO_TRANSFER_CHECK_2004-2017](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/OPCO_TRANSFER_CHECK_2004-2017.html):
  whether the correction of the LI-7500 flux holds for the early years.
- [ANALYSER_DAMPING_CHECK_2004-2017](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/ANALYSER_DAMPING_CHECK_2004-2017.html):
  whether the LI-7500 measured too little of the CO2 and H2O fluxes in 2004-2007.
- [FLUX_NEE_IRGA75_INDEPENDENT_ESTIMATES](notebooks/90_OVERVIEW/FLUX_NEE_IRGA75_INDEPENDENT_ESTIMATES.html):
  the early years against the biometric and soil-respiration estimates of @etzold_carbon_2011.
- [FLUX_NEE_IRGA75_PARTITIONING_COMPARISON](notebooks/90_OVERVIEW/FLUX_NEE_IRGA75_PARTITIONING_COMPARISON.html):
  `GPP` and `RECO` of the early years against the LI-7200 years.
- [RAW_DATA_DIAGNOSTICS_IRGA75_SUMMERS](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/RAW_DATA_DIAGNOSTICS_IRGA75_SUMMERS.html):
  time lags, cospectra and instrument noise from the 20 Hz raw data of the summers 2005-2007,
  2010-2012 and 2016.
:::

The annual `NEE` of the LI-7500 years in this product is less negative than in two earlier
estimates for the same years: FLUXNET and @etzold_carbon_2011. This page shows where each
difference comes from, and whether the correction of the LI-7500 flux ([Level 1.1](L1.1.md))
holds for the early years. The reference for plausibility is the LI-7200 (`IRGA72`), measured
from 2016 and not affected by self-heating.

In short:

- **FLUXNET** has far lower winter nights. Its input kept strongly negative winter night values,
  and its gap-filling spread them to the 75-80 % of the nights that are filled.
- **@etzold_carbon_2011** used a self-heating correction about a third the size of the one in
  this product (about +210 against +640 gC m-2 per year). With their correction in place of ours,
  the flux of this product gives -270 to -362 gC m-2 per year against their -415, with the same
  seasonal pattern.
- **Winter:** this product agrees with the LI-7200 years. FLUXNET and the smaller correction of
  @etzold_carbon_2011 both give less winter respiration.
- **Summer:** the correction holds from 2008 on. In the summers of 2005-2007 this product has less
  daytime uptake than the LI-7200 years. The correction may be too large in those three summers;
  the evidence is mixed. If it is, their May-September `NEE` is up to about 200 gC m-2 too
  positive.
- **Against independent estimates** the early years are too weak a sink: by 250 to 380 gC m-2 per
  year against the biometric net ecosystem production of 2006-2009. Respiration agrees with the
  soil respiration measurements; the shortfall is in the daytime uptake (`GPP`). The raw data and
  the calibration records rule out a fault of the analyser.

## Annual sums

| Year | This product | FLUXNET | @etzold_carbon_2011 |
|---|---|---|---|
| 2004 (from 14 March) | -79 | -444 | |
| 2005 | +164 | -158 | |
| 2006 | +144 | -124 | |
| 2007 | -101 | -352 | |
| 2008 | +64 | -201 | |
| 2009 | +59 | -270 | |
| 2005-2009 mean | +66 | -221 | -415 (range -366 to -662) |
| 2010 | -44 | -441 | |
| 2011 | -218 | -517 | |
| 2012 | -219 | -680 | |
| 2013 | -163 | -545 | |
| 2014 | -221 | -592 | |
| 2015 | -167 | -335 | |

: Annual `NEE` in gC m-2 per year. This product: `IRGA75`, preliminary (see the box above).
FLUXNET: `NEE_VUT_REF` of the ONEFlux v1.3 release for CH-Lae. FLUXNET starts on 14 March 2004,
so 2004 is compared from that date; the LI-7500 measures from 31 March 2004. {#tbl-annual}

The LI-7200 years 2016-2025 average -105 gC m-2 per year in FP2026.1 (range -336 to +76).

## Seasonal pattern, 2005-2009

| | Nov-Mar | Apr and Oct | May-Sep | Year |
|---|---|---|---|---|
| @etzold_carbon_2011 | about +175 | about 0 | about -570 | -415 |
| This product, `IRGA75` | +393 | +72 | -399 | +66 |
| This product, `IRGA75` before correction | +91 | -27 | -635 | -572 |
| This product, with the correction of @etzold_carbon_2011 | +192 to +241 | +3 to +18 | -558 to -529 | -362 to -270 |
| FLUXNET | +183 | +19 | -423 | -221 |
| LI-7200, 2016-2025 (FP2026.1) | +374 | +38 | -517 | -105 |

: Mean `NEE` per season in gC m-2, sums of the monthly means. The values of
@etzold_carbon_2011 are read from their Fig. 5 and are accurate to about ±10 gC m-2 per month;
their published annual mean is -415. "Before correction" removes the mean correction of each
month, by day and by night, from every half-hour; "with the correction of @etzold_carbon_2011"
then adds theirs in the same way, using its monthly median (first value) or mean (second value).
Both rows are approximations. {#tbl-seasons}

The correction in this product adds about +640 gC m-2 per year, at +42 to +67 gC m-2 per month.
It raises the daytime flux by 2.0 to 3.9 µmol m-2 s-1 and the nighttime flux by 0.4 to
1.3 µmol m-2 s-1, most in winter. The correction of @etzold_carbon_2011 adds about +210 to
+300 gC m-2 per year: 0.6 to 1.2 µmol m-2 s-1 by day and 0.2 to 1.0 µmol m-2 s-1 at night.

## Comparison with FLUXNET

The FLUXNET release for CH-Lae was built from the earlier product FP2021. For 2004-2015 that
was the LI-7500 flux, corrected for self-heating following @kittler_high-quality_2017; for
2016-2017 it was the LI-7200 flux. FLUXNET then applied its own u* filtering and gap-filling
(MDS). The two datasets were compared half-hour by half-hour:

- **Half-hours measured in both** (about 30 % of each year): the annual sums agree within -14 to
  +25 gC m-2. At night this product is 0.5 to 0.9 µmol m-2 s-1 higher, because its correction
  adds more at night (+0.5 to +0.9 against +0.2 to +0.4). By day both corrections add about
  +3 µmol m-2 s-1.
- **Nights FLUXNET keeps and this product removes:** +13 to +52 gC m-2 per year. From October to
  May these FLUXNET values average -2 to -8 µmol m-2 s-1: apparent nighttime uptake, which this
  product removes as outliers ([Level 3.2](L3.2.md)).
- **Nights both datasets fill:** +150 to +275 gC m-2 per year, most of the difference. From
  November to March FLUXNET fills them 1.8 to 2.9 µmol m-2 s-1 lower than this product. Its
  December nights average +0.06 µmol m-2 s-1 where measured and -0.12 where filled.

Nighttime respiration of a forest at 0-5 °C does not fall to zero. In this product the filled
winter nights (+2.7 µmol m-2 s-1) agree with its measured ones (+2.9 to +3.2) and with the
LI-7200 nights of 2016-2026 (+2.5 to +3.2). The low FLUXNET winter nights of 2004-2015 are
therefore the less plausible values, and the difference is not a check of this product.

In 2016-2017 FLUXNET uses the LI-7200 and differs in the other direction: its sums (-81 and
+288 gC m-2) are 38 and 212 gC m-2 above those of the LI-7200 in FP2026.1 (-119 and +76), and
its nights average +4.2 and +5.4 µmol m-2 s-1 against +3.7. The cause has not been
investigated.

## Comparison with Etzold et al. (2011)

@etzold_carbon_2011 report the `NEE` of 2005-2009 from the same LI-7500. Their processing
differs from this product in four ways that matter for the annual sum:

| Step | @etzold_carbon_2011 | This product |
|---|---|---|
| Self-heating correction | @burba_addressing_2008, with the surface temperatures of @jarvi_comparison_2009 | Fitted to the LI-7200 in the 2016-2017 overlap ([Level 1.1](L1.1.md)) |
| Large winter fluxes (±15 µmol m-2 s-1) | kept in the data, left out of the gap-filling fits | removed as outliers ([Level 3.2](L3.2.md)) |
| Negative nighttime values | removed, together with as many positive ones (trimmed mean) | removed only where they lie clearly outside the measurement uncertainty |
| Gap-filling | light response by day, temperature response at night, running mean below 0 °C | XGBoost ([Level 4.1](L4.1.md)) |

: Processing of @etzold_carbon_2011 (p. 1297) compared with this product. Both use a u*
threshold of about 0.3 m s-1 ([Level 3.3](L3.3.md)). {#tbl-etzold-methods}

Their correction adds a fixed fraction (0.085, the default of @jarvi_comparison_2009) of the
heat-flux term of @burba_addressing_2008, with the instrument surface temperature estimated
from air temperature. That fraction was derived for a vertically mounted analyser; the LI-7500
at CH-LAE is inclined. It was recomputed for this comparison from an R implementation used in
the group, which is assumed to be the version used for CH-LAE; the agreement below supports this.

Applied to the flux of this product, their correction reproduces their result (@tbl-seasons):
-270 to -362 against -415 gC m-2 per year, -529 to -558 against about -570 in May-September,
+192 to +241 against about +175 in November-March. Of the difference of about 480 gC m-2 per
year between their study and this product, about 340 to 430 come from the size of the
correction. The rest comes from the other processing steps.

## Does the correction hold for the early years?

The correction is fitted on 2016-2017 and applied unchanged to 2004-2015. Compared with the
LI-7200 years at the same light and air temperature:

- **The model transfers.** The drivers of the early summers lie within the range of the training
  years (at most 1.1 % of the records outside). Under the same conditions the correction is the
  same in both periods (2.23 against 2.16 µmol m-2 s-1). Fitted on 2016 alone or 2017 alone, the
  model corrects the other year to within 0.05 µmol m-2 s-1 of the LI-7200 and gives the same
  correction for the early years.
- **Nights agree.** Summer nighttime `NEE` of 2005-2009 (+4.9 µmol m-2 s-1) equals that of the
  LI-7200 years (+5.0).
- **2008 and later agree by day.** At the same light and temperature, the summer daytime flux of
  2010-2015 is within 0.2 µmol m-2 s-1 of the LI-7200 years. 2007-2009 have 0.9 to 1.2 less
  uptake, within the year-to-year spread of the LI-7200 years (standard deviation 1.2).
- **2005 and 2006 have clearly less daytime uptake**, by 2.1 and 2.7 µmol m-2 s-1. The
  correction is about the same in every year, so the difference is already in the uncorrected
  flux. In 2006 even the uncorrected flux has less uptake than the LI-7200 years.

Whether the correction is too large in 2005-2007 cannot be settled from the LI-7500 data alone:

- **For a too large correction:** in summer the self-heating error grows at low wind speed. In the
  uncorrected flux of 2005-2007 this wind dependence is much weaker than in 2008-2017; taken at
  face value it implies a self-heating about 80 % weaker in those summers (scaling factor
  0.20 ± 0.44, where 1 means as in the training years).
- **Against:** in the winters of 2004/05 to 2006/07 the contrast between sunny half-hours and
  nights implies full-size self-heating (1.49 ± 0.58). The 2005-2006 deficit is partly present
  without any correction. Dry summers alone do not explain it: the dry LI-7200 summers 2018 and
  2022 show 0.3 and 0.9 µmol m-2 s-1.
- **The setup did not change.** The same LI-7500 head, separation and EddyPro settings were used
  throughout, and the energy balance and turbulence statistics show no step.
- **The low CO2 reading of 2004-2007 does not explain it.** Until a recalibration in December 2007
  the LI-7500 read CO2 about 2 % low in 2004-2005 and about 6 % low in 2006-2007 (section 5 of the
  transfer notebook). A gain error of that size would make the true summer daytime flux 0.5 to
  0.65 µmol m-2 s-1 more negative in 2006-2007; a zero offset would make it about 0.6 more
  positive. Either way this is a fraction of the 2.1-2.7 µmol m-2 s-1 of 2005-2006, and about
  ±50 to ±60 gC m-2 per summer in 2006-2007 (±15 in 2004-2005). The field check before the
  recalibration of 19 December 2007 points to a zero offset: the zero gas read -46.6 ppm and the
  567.5 ppm reference gas 526 ppm, so the slope between the two was within 1 % of the true one. A
  zero offset leaves the measured covariance unchanged, so no gain correction of the flux is
  needed; its effect through the WPL terms is the +0.6 µmol m-2 s-1 above and points away from
  more uptake. The only earlier check, in September 2007, was made right after the chemicals
  were replaced and is less reliable. No record covers 2004-2006.

If the summer wind dependence is right, the May-September `NEE` of 2005-2007 is 171 to
195 gC m-2 per summer too positive (95 % range 0 to 244), and the 2005-2009 mean about 109 too
positive (range 0 to 216). If instead the ecosystem took up as much as in the LI-7200 years, the
2005-2009 mean would change by about 158; that is an upper bound, not an estimate. This product
keeps the correction unchanged; treat the summers of 2005-2007 as uncertain by up to about
200 gC m-2.

## Why the early years are a weak sink

### Independent estimates

@etzold_carbon_2011 give biometric and chamber estimates for the same forest, independent of
eddy covariance.

| 2006-2009 | This product | @etzold_carbon_2011 |
|---|---|---|
| Net ecosystem production (−`NEE`) | -41 (USTAR scenarios -5 to -74) | +307 to +514 (four biometric methods) |
| Ecosystem respiration (`RECO`) | 1,487-1,495 | 1,383 ± 338 (their eddy covariance) |
| Soil respiration | | 890 (chambers) |
| Soil respiration / `RECO` | 0.60 | 0.64 |
| `GPP`, 2005-2009 | 1,378-1,395 | 1,830 ± 448 (their eddy covariance) |
| `RECO` / `GPP` | 1.05-1.09 | 0.76 |

: The LI-7500 years against independent estimates, in gC m-2 per year (`CUT_50`, nighttime and
daytime partitioning). Values of @etzold_carbon_2011 from their Tables 4 and 5, converted from
Mg C ha-1. Net ecosystem production is positive for a sink. {#tbl-independent}

- **The sink is too weak.** Even the lowest biometric estimate (+307) lies 250 to 380 gC m-2 above
  this product. With the current tests of negative nighttime values the gap shrinks by about
  100.
- **Respiration is plausible.** `RECO` exceeds the soil respiration, as it must, and the share of
  soil respiration (0.60) matches theirs.
- **`GPP` is too low.** About 76-88 % of the difference to their study comes from lower `GPP`.
  `RECO` above `GPP` would make the forest a source in every year, which the biometric growth
  rules out.

The biometric values are means between the inventories of 2005 and 2009 on a 1.48 ha plot, smaller
than the flux footprint, and their stated uncertainties leave out method assumptions. The size of
the shortfall is still far beyond these.

### Where and when the uptake is missing

Compared with the LI-7200 years 2016-2025, 2005-2009 take up about 170 gC m-2 per year less.

- **The deficit is in the daytime half-hours** (+201 gC m-2 per year by day, -30 at night). This
  split needs no partitioning model. With nighttime partitioning it is almost entirely `GPP`.
- **It is a lower capacity, not a shorter season.** Light-saturated `GPP` is 5.1 µmol m-2 s-1
  lower in 2005-2007 and 2.6 lower in 2008-2009; 2005 and 2006 lie below every LI-7200 year. The
  seasonal course of `GPP` relative to its peak is unchanged, and leaf-out is not later.
- **2005-2007 lose it mostly in June and July, 2008-2009 spread over January to July.** The gap
  is largest at high light and air temperatures below 20 °C.
- **Weather explains part of it at most.** The early years were cooler and dimmer, and the soils of
  2004-2006 were dry, in the years after the drought of 2003. But 2010-2015 had similar weather and
  agree with the LI-7200 years, and in 2004-2006 the summer `GPP` lies below every other year at
  the same weather, including the dry LI-7200 summers 2018 and 2022.

### No measurement fault found

The analyser could have measured too little of the fluxes. This was checked and not found:

- The EddyPro settings, the time-lag window and the detected time lags are the same in all years;
  the spectral correction factor is 1.03 in every year.
- The correlation of the vertical wind with CO2 and H2O is 4-7 % lower in 2004-2006, while that
  with the sonic temperature is unchanged. The correlation between CO2 and H2O, which a time-lag
  error cannot change, drops by as much, and the drops do not follow the size of the deficit
  (2007 shows none). The dry LI-7200 summer of 2022 shows a larger drop.
- Counting this drop as a loss and the low CO2 reading as a gain error, at most 34-54 % of the
  summer daytime gap of 2005-2007 would close (up to about 110 gC m-2 in 2006). The calibration
  check of December 2007 points to a zero offset rather than a gain error, which lowers this
  upper bound further.

The 20 Hz raw data of June and July 2005-2007, 2010-2012 and 2016 (midday) settle this:

- **No covariance is lost by the measurement.** At the time lag EddyPro used, the covariance is
  99.9-100 % of its maximum over -2 to +3 s; the lag functions have the same shape in all years.
  The cospectra of CO2 and H2O, relative to that of the sonic temperature, are the same as in the
  reference years. Instrument noise is below 1 % of the variance. Together these change the
  covariance of 2005-2006 by -1 to +2 % against 2010-2012.
- **The lower correlations are real.** The correlation between CO2 and H2O is 8-13 % lower in
  2005-2006, and that of the vertical wind with H2O 5-7 % lower, beyond the range of the reference
  years. Neither time lag nor noise can cause this. The CO2 and H2O exchange itself was less
  coupled in those summers. 2007 is at the reference level.

### What this means

The early LI-7500 years are a weaker sink than the biometric estimates allow, because their daytime
uptake is low. A fault of the analyser is ruled out: the raw data lose no covariance, and the
calibration error of 2006-2007 was a zero offset. What remains is a real loss of capacity, which
is plausible for 2004-2006 after the drought of 2003 and fits the less coupled CO2 and H2O
exchange of 2005-2006, or a correction that is too large for those years (above). Neither covers
2007-2009 or the full size of the shortfall. The annual sums of 2004-2009 are therefore
the least certain of the record. Use them with this uncertainty in mind, and prefer the LI-7200
years where the result depends on the absolute sink strength.

## References

::: {#refs}
:::
