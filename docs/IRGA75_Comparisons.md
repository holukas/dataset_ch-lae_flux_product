# Comparisons of the LI-7500 years

::: {.callout-warning title="Preliminary, for FP2026.2"}
The LI-7500 fluxes of 2004-2015 are in progress for FP2026.2 and are not part of FP2026.1. The
numbers on this page come from the run of 30 October 2026 of
[05_FPPC_IRGA75_NEE_OPCO_2004-2017](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/05_FPPC_IRGA75_NEE_OPCO_2004-2017.html)
(`CUT_50`, XGBoost gap-filling), which still used the stricter tests of negative nighttime values.
With the current tests the annual sums are lower: by 42 to 100 gC m-2 in 2004-2006 and by 80 to
163 gC m-2 in 2012-2014 (test runs `T2` and `T3`). The page will be updated after the next run.
:::

The annual `NEE` of the LI-7500 years in this product is less negative than in two earlier
estimates for the same years: FLUXNET and @etzold_carbon_2011. This page shows where each
difference comes from. The reference for plausibility is the LI-7200 (`IRGA72`), measured from
2016 and not affected by self-heating.

In short:

- **FLUXNET** has far lower winter nights. Its input kept strongly negative winter night values,
  and its gap-filling spread them to the 75-80 % of the nights that are filled.
- **@etzold_carbon_2011** used a self-heating correction about a third the size of the one in
  this product (+210 against +640 gC m-2 per year). With their correction in place of ours, the
  flux of this product gives -362 gC m-2 per year against their -415, with the same seasonal
  pattern.
- **Winter:** the LI-7200 years agree with this product. FLUXNET and the smaller correction of
  @etzold_carbon_2011 both give less winter respiration.
- **Open:** in summer the LI-7200 years lie between the two corrections. This product has about
  120 gC m-2 less summer uptake than the LI-7200 years. It is not yet known whether this is real
  or whether the correction is too large in summer for the early years.

## Annual sums

| Year | This product | FLUXNET | @etzold_carbon_2011 |
|---|---|---|---|
| 2004 | +161 | -444 | |
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
FLUXNET: `NEE_VUT_REF` of the ONEFlux v1.3 release for CH-Lae. 2004 starts on 30 March in this
product and is not a complete year. {#tbl-annual}

The LI-7200 years 2016-2025 average -105 gC m-2 per year in FP2026.1 (range -336 to +76).

## Seasonal pattern, 2005-2009

| | Nov-Mar | Apr and Oct | May-Sep | Year |
|---|---|---|---|---|
| @etzold_carbon_2011 | about +170 | about 0 | about -570 | -415 |
| This product, `IRGA75` | +393 | +72 | -399 | +66 |
| This product, `IRGA75` before correction | +91 | -27 | -635 | -572 |
| This product, with the correction of @etzold_carbon_2011 | +192 | +3 | -558 | -362 |
| FLUXNET | +184 | +20 | -422 | -221 |
| LI-7200, 2016-2025 (FP2026.1) | +374 | +38 | -516 | -105 |

: Mean `NEE` per season in gC m-2, sums of the monthly means. The values of
@etzold_carbon_2011 are read from their Fig. 5 and are accurate to about ±10 gC m-2 per month.
"Before correction" removes the mean correction of each month, by day and by night, from every
half-hour; "with the correction of @etzold_carbon_2011" then adds theirs in the same way. Both
rows are approximations. {#tbl-seasons}

The correction of the LI-7500 flux in this product ([Level 1.1](L1.1.md)) adds about
+640 gC m-2 per year, spread over the year at +42 to +67 gC m-2 per month. It raises the daytime
flux by 2.0 to 3.9 µmol m-2 s-1 and the nighttime flux by 0.4 to 1.3 µmol m-2 s-1, most in
winter. The correction of @etzold_carbon_2011 adds about +210 gC m-2 per year: 0.7 to
1.2 µmol m-2 s-1 by day and 0.4 to 1.0 µmol m-2 s-1 at night.

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

The correction of @etzold_carbon_2011 was recomputed for this comparison from an R
implementation used in the group, which applies the equation of @burba_addressing_2008 with the
fraction of @jarvi_comparison_2009 to the EddyPro output. It is assumed to be the version that
was used for CH-LAE; the agreement below supports this.

Their correction adds a fixed fraction (0.085, the default of @jarvi_comparison_2009) of the
heat-flux term of @burba_addressing_2008, with the instrument surface temperature estimated
from air temperature. That fraction was derived for a vertically mounted analyser; the LI-7500
at CH-LAE is inclined. The correction in this product is instead fitted to the LI-7200.

Applied to the flux of this product, their correction reproduces their result (@tbl-seasons):
-362 against -415 gC m-2 per year, about -558 against -570 in May-September, +192 against +170
in November-March, and +3 against about 0 in April and October. Of the difference of about
480 gC m-2 per year between their study and this product, about 430 come from the size of the
correction. The rest, about 50, comes from the other processing steps, which is within the
accuracy of the comparison.

The LI-7200 years decide between the two corrections only in part:

- **Winter:** the LI-7200 years (+374) agree with this product (+393), not with the smaller
  correction (+192).
- **Summer:** the LI-7200 years (-516) lie between this product (-399) and the smaller correction
  (-558). In the 2016-2017 overlap the uncorrected LI-7500 overestimated the summer uptake of the
  LI-7200 by 19 %, so a correction is needed in summer as well.

## Open question

In winter this product agrees with the LI-7200 years. In summer it has about 120 gC m-2 less
uptake than the LI-7200 years (-399 against -516). The correction was fitted on 2016-2017 and is
applied unchanged to the earlier years, where it raises the summer daytime flux by about
2.5 µmol m-2 s-1. If the self-heating of the analyser was weaker in the early years, the
correction is too large there and the early summers are biased towards release. The difference
may also be real, from weather or from changes in the stand. A check is whether the
correction behaves the same against air temperature, radiation and u* in both periods. Until
this is settled, the annual sums of the LI-7500 years carry an uncertainty of this size.

## References

::: {#refs}
:::
