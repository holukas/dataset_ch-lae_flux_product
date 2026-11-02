# Known Issues

Open points that affect users of FP2026.1 and of FP2026.2, which is in progress. Sections that
concern only the LI-7500 years of FP2026.2 say so. Limitations of a single meteorological variable are
on that variable's page under [Meteorological data](Meteo_Data.md); release details are in
[Dataset versions](Dataset_Versions.md). Planned work is tracked in the
[Issues](https://github.com/holukas/dataset_ch-lae_flux_product/issues) of the repository.

## No measured `H` from 10 January to 20 March 2019

There is no measured sensible heat flux between 10 January 2019 15:15 and 20 March 2019 18:45
(`TIMESTAMP_MIDDLE`), 3320 half-hours. The gap-filled series
`H_L3.1_L3.3_CUT_NONE_QCF_gfXG` covers the period, so its values there come from the model
alone; `FLAG_H_L3.1_L3.3_CUT_NONE_QCF_gfXG_ISFILLED` marks them.

The gap has two causes. Setup period `2019_2` (10 to 17 January 2019), in which both LI-7200
units were defective, has no Level-1 run, so its sonic data were not processed. In `2019_3`
(17 January to 20 March 2019) the open-path LI-7500 stood in for the LI-7200; its run is processed
with the other `IRGA75` fluxes but is used in neither release: the merged record of FP2026.2 takes
this period from the LI-7200, gap-filled. The same sonic was in operation
throughout, so `H` could be computed for this period from these two setup periods. This is under
review.

The gas fluxes `FC`, `NEE` and `LE` have the same gap, for the reasons above. See
[Level-4.1](L4.1.md) for the other long gaps.

## `H` in 2024 is lower than in the other years

The annual mean of the Level-1 `H`, before quality control, is 25.8 W m^-2^ in 2024, against 33.9
to 51.8 W m^-2^ in the other full years 2016 to 2025, about a third lower. The gap-filled series
gives 25.1 W m^-2^ against 32.4 to 45.4 W m^-2^.

The cause is the weather. In 2024 incoming shortwave radiation was 12 % below the other years, the
rain sum was the highest of the period (1151 mm), and `VPD` was the lowest. No instrument fault was
found. The low `H` of 2024 is therefore not an artefact.

## MDS in spring 2016

In spring 2016 the measurements of the start-up period were removed (1 March to 25 May 2016), and
the gap includes the leaf-out. MDS fills this gap from records far away in time and gives a much
larger uptake than XGBoost: the April-May sum of `NEE` (`CUT_50`) is -274 gC m^-2^ with MDS and
-82 gC m^-2^ with XGBoost (-235 and -113 in FP2026.1). In the other years the April-May sums of
both methods lie between -16 and -188 gC m^-2^. XGBoost is the gap-filling method of this dataset, and MDS is included for
comparison only. Use the XGBoost series (`_gfXG`). See [Level-4.1](L4.1.md).

## The LI-7500 fluxes are not part of FP2026.1

FP2026.1 contains fluxes of the enclosed-path LI-7200 (`IRGA72`) only, from 11 January 2016.
FP2026.2, in progress, adds the fluxes of the open-path LI-7500 (`IRGA75`) for 2004-2015, with the
CO~2~ flux corrected at [Level-1.1](L1.1.md). Its merged record takes the fluxes from the LI-7500
until 31 December 2015 and from the LI-7200 from 1 January 2016; `FLAG_FLUX_SOURCE` gives the
analyser of each half-hour (`75` or `72`). The LI-7500 data of the parallel period 2016-2017 train
and check the correction. They are not in the merged record, and neither is the stand-in run of 2019.
FP2026.2 will contain FP2026.1 in full and supersede it.

## The storage term of the LI-7500 drifts

This concerns `NEE` and the storage term of 2004-2017 in the LI-7500 processing of FP2026.2. Over a
year, a storage term should sum to about zero. The single-point storage term of the LI-7500
(`SC_SINGLE_gfRMED_L3.1`) sums to -25 to -196 gC m^-2^ per year in 2004-2017, and to
-159 gC m^-2^ per year in the 2016-2017 overlap. That of the LI-7200 sums to -23 to +15 gC m^-2^
per year, and to +0.7 in the overlap.

The cause lies in the CO~2~ concentration of the LI-7500. With wet or blocked windows, at an AGC
above 55 or after rain, it reads 33 to 106 ppm too high. Across its gaps the concentration rises by
12.4 ppm (median). The rise falls into the gap and is not counted, while the return after the gap
enters the storage term as a negative flux. This accounts for about 130 of the 160 gC m^-2^ per year
of the drift. The error of the concentration changes the flux itself by less than 1 %, so it does
not explain the low humid fluxes described below.

A screen of the concentration is set for the next processing run and is not yet in the data: a
reading enters the storage term only at an AGC of 55 or less, without rain in the previous 3 hours,
at a relative humidity below 99.5 %, and not among the first 3 records after a gap. In a test with
the chain (`CUT_50`), the storage term then sums to -5 to +39 gC m^-2^ per year in 2004-2015, and
the result is robust to the settings. The method, the evidence and the tests are on
[Level 3.1](L3.1.md#drift-of-the-li-7500-storage-term).

What this means for the data:

- In the current processing, the storage term of the LI-7500 and its `NEE` still contain the drift.
  In the test, the screen raises annual `NEE` by about 70 gC m^-2^ per year in 2004-2015 and by 118
  in 2016-2017, and reduces the overlap gap to the LI-7200 by about 120 of about 400 gC m^-2^ per
  year.
- The LI-7200 storage term is not affected.

## The LI-7500 misses the wet half-hours

This concerns `NEE` of 2004-2015 in FP2026.2. The correction of [Level-1.1](L1.1.md) works on the
half-hours the LI-7500 measured. Most of the remaining difference to the LI-7200 lies in the
half-hours it did not measure.

The LI-7500 loses many half-hours in wet weather (rain, fog, dew, water on the windows), when the
LI-7200 still measures. Gap-filling learns only from the conditions the LI-7500 measured, so it fills
these gaps with too much uptake. Open-path analysers are known to lose data in wet weather, but no
published study was found that quantifies the resulting bias against a co-located enclosed-path
analyser.

From 11 January 2016 to 12 December 2017, when both analysers ran, the annual `NEE` (`CUT_50`,
XGBoost) of the LI-7500 is -349 gC m^-2^ in 2016 and -181 in 2017, that of the LI-7200 +88 and
+188. The LI-7500 therefore shows 436 gC m^-2^ (2016) and 370 gC m^-2^ (2017) more uptake. Of this
gap:

- 16 and 13 gC m^-2^ lie in the half-hours both analysers measured;
- about 80 % lies in the half-hours neither analyser measured, and about 96 % in the half-hours
  that at least one of them gap-filled.

The full split is on [Comparisons of the LI-7500 years](IRGA75_Comparisons.md#the-2016-2017-overlap).
The gap is therefore mostly a property of the gap-filling, not of the measured flux.

The humid half-hours show where it comes from. At a relative humidity of 99.5 % or more, the
LI-7500 measures only 8 to 9 % of the half-hours. Its gap-filling model fills the others at 0.1 to
0.5 µmol m^-2^ s^-1^, that of the LI-7200 at 3.0 to 3.5 µmol m^-2^ s^-1^. With the storage
correction of the next run the filled values of the LI-7500 rise only to 0.95, against 3.33, while
the humid half-hours the LI-7500 does measure read only 0.3 to 1.1 µmol m^-2^ s^-1^ low (medians,
not stable between the two years). The deficit therefore lies mostly in the gaps where the LI-7500
measured nothing, mostly in rain: its model never sees a flux during rain, while the LI-7200
measures it. The effect on the LI-7500 years 2004-2015 is described under
[Biases of the LI-7500 NEE against a climate baseline](#biases-of-the-li-7500-nee-against-a-climate-baseline).

## Nighttime NEE of the LI-7500 is too low on cold and humid nights

This concerns nighttime `NEE` of 2004-2015 in FP2026.2. The measured nighttime `NEE` of the
LI-7500 falls with humidity and cold. In 2016-2017, below 5 °C and at a relative humidity of 99.5 %
or more, its median after all quality tests is +0.9 µmol m^-2^ s^-1^, and 39 % of the values are
negative, which would mean uptake in the dark. The LI-7200 stays near +2 µmol m^-2^ s^-1^ (+1.8 to
+2.4) in every humidity class, with 10 to 13 % negative values. The likely cause is fog and rime on
the windows of the open-path analyser.

Many of these nights pass the quality tests, and gap-filling learns from them. [Level-3.2](L3.2.md)
removes the clearest cases: four fog episodes in 2004, 2013 and 2014 are removed by hand, and a test
removes whole nights whose median is clearly below zero. Nights that read too low without a clearly
negative median remain. Calm and cold nights also remain too low after the correction of
[Level-1.1](L1.1.md): at wind speeds below 2 m s^-1^ and below 0 °C, the corrected LI-7500 reads
about 1 µmol m^-2^ s^-1^ below the LI-7200.

In the 2016-2017 overlap, with both analysers on the same sonic anemometer, the median difference
of nighttime `NEE`, LI-7500 minus LI-7200, is:

- about -1.1 µmol m^-2^ s^-1^ below 0 °C and -0.4 at 0-5 °C, at a relative humidity of 99.5 % or
  more;
- -0.6 to -0.9 at 97-99.5 % (below 0 °C and at 5-10 °C);
- +0.2 to +0.9 below 97 % and below 10 °C.

The automatic gain control (AGC) value of the LI-7500 does not separate these records. Removing
every LI-7500 nighttime record below 5 °C at 99.5 % relative humidity or more, whatever its sign,
was tested and is not adopted. It removes about 4 % of the nighttime records but widens the gap to
the LI-7200 in the overlap by 29 to 127 gC m^-2^ per year, because the gap-filling then
extrapolates the humid nights even lower.

What this means for the data:

- Measured and gap-filled nighttime `NEE` of the LI-7500 years is likely biased towards uptake in
  cold and humid conditions. Most of the bias of the annual sums lies in the humid gaps rather than
  in the measured nights (see [The LI-7500 misses the wet half-hours](#the-li-7500-misses-the-wet-half-hours)).
- `RECO` from the nighttime partitioning is fitted on these nights and is likely too low in winter.

Not yet resolved.

## Biases of the LI-7500 NEE against a climate baseline

This concerns `NEE` of 2004-2015 in FP2026.2. The LI-7500 years cannot be checked against a
second analyser. They are compared instead with a climate baseline: a model of daytime and
nighttime `NEE` trained on the LI-7200 years 2016-2025, with meteorological drivers only. Applied to
the weather of another year, it gives the `NEE` that the forest of 2016-2025 would have exchanged
under that weather. The numbers below are the differences of the gap-filled `NEE` (`CUT_50`) to
this baseline, in gC m^-2^ per year.

- **Night: about -200 in every LI-7500 year.** The LI-7500 lies about 200 to 250 below the baseline
  in 2004-2009, in 2010-2015 and in the overlap 2016-2017. The LI-7200 years lie within -40 to +30.
  This is the deficit of the humid gaps described above.
- **Day: about +230 in 2004-2009.** By day the LI-7500 lies about 230 above the baseline in
  2004-2009 (single years +200 to +370 with the storage correction), about 0 in 2010-2015, and -105
  in 2016-2017 (-34 with the storage correction). The LI-7200 years scatter from -280 to +150. The
  uncorrected LI-7500 flux of 2004-2009 matches the baseline, so the correction of
  [Level 1.1](L1.1.md) probably over-corrects the daytime flux of these years (see the
  limitations on that page).

In 2004-2009 the two biases largely offset each other in the annual sum; in 2010-2015 the night
deficit remains. This is why the annual sums show no clear step at the change of analyser:
2004-2015 average -82 gC m^-2^ per year, 2016-2025 -18
([overview of the merged NEE record](notebooks/90_OVERVIEW/FLUX_NEE.html)).

The baseline cannot settle whether the forest itself changed. It describes the forest of the
LI-7200 years. A real difference of the forest in 2004-2009, for example a lower uptake capacity
after the drought of 2003, would appear against it as a bias of the same kind. In 2005-2009 the
annual `NEE` averages +27 gC m^-2^ per year, a small net release, far less uptake than the
biometric estimates for 2006-2009 and the earlier flux estimates of FLUXNET and
@etzold_carbon_2011. A loss of capacity after 2003 is plausible for 2004-2006 at most; it does not
explain 2007-2009 or the whole size of the difference. Checks of the analyser, the raw data and the
calibration found no fault of the measured flux. An independent closed-path measurement of these
years, which could decide it, is not available.

Tested and not adopted:

- **Scaling the daytime correction of 2004-2007 by 0.2.** It brings those days to the baseline but
  leaves 2008-2009 high, and the annual sum then jumps from -393 gC m^-2^ in 2007 to +51 in 2008.
- **Filling the humid gaps from a LI-7200 model.** It halves the night deficit and closes the
  overlap gap to about -100 gC m^-2^ per year, but adds +85 to +120 by day, and its effect in
  2004-2015 cannot be checked.
- **All corrections together**, with the storage correction, give a record that is homogeneous
  against the baseline. This is largely by construction: the baseline comes from the LI-7200 years,
  and the corrections would also remove a real change of the forest.
- **A variant of the Level-1.1 correction with a nighttime heat term from incoming longwave
  radiation** changes little.

What this means for the data:

- The annual `NEE` of all LI-7500 years carries a nighttime bias towards uptake of about
  200 gC m^-2^ per year, and that of 2004-2009 a daytime bias towards release of about 230 gC m^-2^
  per year. FP2026.2 states both as uncertainties and does not correct them. Differences between
  years smaller than these are not resolved, and where a result depends on the absolute sink
  strength, prefer the LI-7200 years.
- The nighttime partitioning fits `RECO` on measured `NEE` only. The missing wet nights therefore
  bias `RECO` and `GPP` low.
- Shortwave radiation was measured from 14 September 2005, so the daytime partitioning gives no
  result before that date ([Level 4.2](L4.2.md)). In 2005 most of the meteorological drivers are
  gap-filled.
- The LI-7500 record starts on 30 March 2004, so `NEE`, `LE` and `H` of January to March 2004 are
  entirely gap-filled. Their `SW_IN` driver is unreliable in January 2004, about 2.7 times the mean
  January total (see [SW_IN](Meteo_Data_SW_IN.md)).

The comparisons with FLUXNET, @etzold_carbon_2011 and the biometric estimates are on
[Comparisons of the LI-7500 years](IRGA75_Comparisons.md).

## LE of the two gas analysers differs in humid and cold conditions

This concerns `LE` and `ET` across the change of gas analyser on 1 January 2016. In 2016-2017,
when both analysers ran, the open-path LI-7500 (`IRGA75`) measured a higher `LE` than the
enclosed-path LI-7200 (`IRGA72`). On the half-hours both measured, it is about 9 % higher overall,
and the difference grows with humidity and cold:

| relative humidity | `LE` `IRGA75` / `IRGA72` | closure `IRGA75` | closure `IRGA72` |
|---|---|---|---|
| below 60 % | 1.03 | 0.93 | 0.91 |
| 60-80 % | 1.05 | 0.90 | 0.88 |
| 80-90 % | 1.14 | 0.85 | 0.81 |
| 90-95 % | 1.47 | 0.80 | 0.69 |
| 95 % and above | 2.11 | 0.72 | 0.51 |

: Ratio of the `LE` sums of the two analysers on the half-hours both measured after all quality
tests, and the daytime energy balance closure of each, (`H + LE`) / (`NETRAD - G`) as a ratio of
sums, 11 January 2016 to 12 December 2017, by relative humidity at 47 m
([overview of `ET`](notebooks/90_OVERVIEW/FLUX_ET.html)). {#tbl-le-ratio}

Below 0 °C the ratio is 2.7, above 20 °C 1.03. The gap-filled `LE` of the parallel period is 20 %
higher with the LI-7500.

The likely cause lies in the LI-7200, not in the open-path analyser. In the tube and cell of an
enclosed-path analyser, water vapour adsorbs on the walls, which damps the H2O fluctuations more the
higher the humidity. The `IRGA72` runs correct for this (Fratini et al. 2012), but such corrections
often fall short above about 90 % relative humidity. Self-heating of the open-path analyser would
bias its flux the other way.

The energy balance supports this (@tbl-le-ratio). In dry air both analysers close it to about the
same degree. With rising humidity the closure of the LI-7200 falls faster: at 99.5 % relative
humidity or more it is 0.45, that of the LI-7500 0.69. The LI-7500 `LE` is therefore the more
complete one at high humidity.

What this means for the data:

- The `LE` and `ET` of the LI-7200 (FP2026.1, and FP2026.2 from 2016) are likely too low in humid and
  cold conditions.
- In the merged record of FP2026.2, the step in `LE` and `ET` at 1 January 2016 is instrumental.
  The gap-filled `ET` averages about 740 mm per year in 2004-2015 (LI-7500) and about 615 mm in
  2016-2025 (LI-7200), a step of about -126 mm per year. Do not read this difference as a change of
  the ecosystem.
- `H` comes from the same sonic anemometer for both analysers and is homogeneous across 2016: the
  ratio of the two is 0.99 in the overlap, and they agree to within 2 % in 2016 and 2017.

The `LE` of the two analysers is not homogenized in FP2026.2.

## Faulty sample flow of the LI-7200 in December 2022

From 8 to 19 December 2022 the logged sample flow of the LI-7200 was 0 to 3 l min^-1^. At this
flow the measuring cell is not flushed with ambient air, as in the other flow faults of
[Level 3.2](L3.2.md). The nighttime `NEE` kept after all quality tests in this period is +5 to
+16 µmol m^-2^ s^-1^ at about -8 °C, far above a plausible winter respiration. These values are
still in FP2026.1 and in the current processing of FP2026.2. Their removal, of `NEE` and `LE`, is
planned for the next run. Until then, do not use the measured fluxes of the LI-7200 from 8 to
19 December 2022.

The logged flow cannot be used to search for further faults in 2022: from March to November 2022 the
flow channel reads 0.0 while the fluxes are normal, a logging fault of the channel.

## Night-time NEE keeps rising above the USTAR thresholds

At the same air temperature, night-time `NEE` keeps rising with `USTAR` up to about 0.9 to
1.0 m s^-1^, for both analysers, well above the thresholds of either release
([Level 3.3](L3.3.md)). A plateau above the threshold, which the USTAR filter assumes, is therefore
not reached. Two explanations are possible, and the tower data cannot separate them: at moderate
turbulence part of the respired CO2 still leaves the site without passing the sensor, or wind draws
additional CO2 out of the soil and the litter.

The respiration of the daytime partitioning (`RECO_DT`, [Level 4.2](L4.2.md)) is not independent of
the threshold: its temperature sensitivity comes from the night records above the threshold applied
in the chain, so `RECO_DT` moves with that threshold. At the thresholds of FP2026.2, night `NEE`
divided by `RECO_DT` of the same half-hour reaches 1 at a `USTAR` of about 0.7 to 0.9 m s^-1^ and
keeps rising, from May to October to about 1.5 for both analysers. The nights kept at the FP2026.2
median thresholds lie 7 % (LI-7200) and 2 % (LI-7500) below `RECO_DT`; the two agree at 0.64 and
0.46 m s^-1^, near `CUT_84` for the LI-7200. With the thresholds of FP2026.1 in the chain, the kept
nights agreed with `RECO_DT` near `CUT_16`. The comparison therefore does not constrain the
threshold.

Part of the high night `NEE` at high `USTAR` may be CO2 flushed out of the canopy air: when the wind
rises after calm hours, CO2 that collected in the canopy passes the sensor. For the LI-7500, from a
`USTAR` of 0.7 m s^-1^, night `NEE` exceeds `RECO_DT` more after 3 calm hours (mean `USTAR` below
0.3 m s^-1^) than after 3 windy hours (above 0.7 m s^-1^): 1.4 against 1.05 times `RECO_DT` at a
`USTAR` of 0.7 to 0.9 m s^-1^, and 1.5 against 1.4 above 0.9 m s^-1^. For the LI-7200 this holds
only above 0.9 m s^-1^ (1.15 to 1.2 after moderately calm hours against 1.1 after windy ones), and
not for the few records after the calmest hours; from 0.5 to 0.9 m s^-1^ its night `NEE` lies
further below `RECO_DT` after calm hours. The calm cases are few (11 to 75 half-hours in the calmest
class). After sustained wind an excess over `RECO_DT` remains, which flushing does not explain.
Right above the threshold, the kept night records after calm hours read low rather than high: 0.92
to 0.96 of `RECO_NT`, the respiration of the nighttime partitioning, at the `CUT_50` of the record
of the site, against 1.02 to 1.10 after mixed hours. No release of stored CO2 shows there.

**Known limitation: the storage term.** The storage term of [Level 3.1](L3.1.md) comes from the CO2
concentration at one height, 47 m. In the flush cases it is not clearly negative, although CO2
leaving the canopy air should make it so. It therefore does not capture this release, and the
flushed CO2 enters `NEE`.

The measured night-time `NEE` and the night-time respiration therefore depend on the threshold. A
higher threshold keeps only the windier nights, whose `NEE` is higher, and the gap-filled nights and
the night-time partitioning follow them. For FP2026.2 the lowest defensible thresholds are chosen
(the moving point method). Estimated from the measured nights alone, the night-time respiration at
the FP2026.2 median thresholds is 26 % (LI-7200) and 20 % (LI-7500) higher than at the threshold of
FP2026.1. The
`USTAR` uncertainty of [Level 4.1](L4.1.md), from the `CUT_16` and `CUT_84` series, covers only part
of this dependence.

::: {.callout-tip title="Notebook"}

[USTAR threshold detection](notebooks/30_FLUX_POST-PROCESSING_CHAIN/USTAR_THRESHOLD_DETECTION_2004-2026.09.html),
sections 4, 6, 9, 10 and 11

:::

## USTAR thresholds compared with FLUXNET

FLUXNET detects USTAR thresholds per year with the method of @pastorello_fluxnet2015_2020. For
CH-LAE, the thresholds it detects change markedly after 2015 (@fig-ustar-fluxnet1). The cause is
not known. The change coincides with a change of gas analyser:

- until 11 January 2016, only the open-path LI-7500 was in operation;
- from 11 January 2016 to 12 December 2017, the LI-7500 and the enclosed-path LI-7200 ran in
  parallel;
- from 14 December 2017, only the LI-7200 was in operation, except from 17 January to
  20 March 2019, when the LI-7500 stood in for it.

Before 2016, the threshold detection therefore used LI-7500 `NEE`, corrected for self-heating in
a similar way to @kittler_high-quality_2017.

This dataset does not use the FLUXNET thresholds. It filters `NEE` at three constant thresholds
per analyser ([Level 3.3](L3.3.md)). FP2026.1 used 0.304 m s^-1^ (`CUT_50`) for the LI-7200. In
FP2026.2 the thresholds come from the moving point method alone: 0.523 m s^-1^ for the LI-7200 and
0.436 m s^-1^ for the LI-7500 (`CUT_50`), applied in the processing of 1 November 2026. The two
sets differ because of the years each record covers, not because of the instruments: on the
records both analysers measured in 2016-2017, the method gives the same `CUT_50` (0.311 and
0.301 m s^-1^). One set from the merged record of the site, 0.352, 0.486 and 0.599 m s^-1^, is
computed but not adopted ([Level 3.3](L3.3.md)). FLUXNET
(ONEFlux v1.3) pools the moving point and the change point methods. Its reference thresholds for
half-hourly `NEE` are 0.43 m s^-1^ as a constant threshold (`CUT_REF`) and, per year (`VUT_REF`),
0.23 to 0.35 m s^-1^ until 2015 and 0.46 to 0.60 m s^-1^ from 2016.

The thresholds explain the differences in the annual sums from 2016, but only part of them before:

- **2016-2024, LI-7200.** At the thresholds of FP2026.2 the two products agree on average. Over
  2018-2024 this product averages -32 gC m^-2^ per year, FLUXNET +3 (`VUT_REF`) and -48
  (`CUT_REF`); the night sums are 844 and 830 gC m^-2^. Single years still differ by up to about
  200 gC m^-2^. On the half-hours both measured, the two agree. FLUXNET keeps 10 to 19 % of the
  nights as measured, this product 15 to 25 % (28 to 43 % with the thresholds of FP2026.1). With
  the thresholds of FP2026.1 this product showed more net uptake than FLUXNET; the higher
  thresholds keep fewer and windier nights, with higher `NEE`, and remove most of this difference.
- **2005-2015, LI-7500.** FLUXNET shows more net uptake: -437 gC m^-2^ per year in 2007-2015
  against -138 here, and -141 against +116 in 2005-2006. Its thresholds of these years lie below
  the 0.436 m s^-1^ of this product, which keeps 17 to 24 % of the nights as measured against 20 to
  26 % in FLUXNET. The difference lies at night: the night sums are about 680 gC m^-2^ here and 350
  in FLUXNET, while by day the two agree. It comes from the different corrections of the open-path
  flux and the low winter nights of FLUXNET, and the higher threshold of this product adds to it
  (see [Comparisons of the LI-7500 years](IRGA75_Comparisons.md)).

Within FLUXNET the same dependence shows: `VUT_REF` gives more uptake than `CUT_REF` where its yearly
thresholds lie below the constant one (to 2015), and less uptake where they lie above it (from 2016).

![USTAR thresholds detected by FLUXNET, based on data 2004-2023, from the file `FLX_CH-Lae_FLUXNET2015_AUXNEE_2004-2023_1-3.csv`.](images/USTAR_thresholds_from_FLUXNET_NEE_VUT_2004-2023.png){#fig-ustar-fluxnet1}

::: {.callout-tip title="Notebook"}

[USTAR threshold detection](notebooks/30_FLUX_POST-PROCESSING_CHAIN/USTAR_THRESHOLD_DETECTION_2004-2026.09.html),
section 7; [Sonic anemometer data](notebooks/90_OVERVIEW/Sonic_Anemometer.html)

:::

## Time shift in incoming shortwave radiation from 2022

The daily cycle of incoming shortwave radiation at 47 m (`SW_IN_T1_47_1`) lags behind potential
radiation by a few minutes from 2022 onwards (@fig-phaseshiftfft-16-25). No error was found in
the processing, and the shift is already present in the raw data. Its cause is not known. The
product page is [Incoming shortwave radiation at 47 m](Meteo_Data_SW_IN.md).

### Method

The shift was detected by comparing the phase of the 24-hour component (FFT) of measured and
potential radiation on clear days, selected as days on which the measured radiation reached at
least 70 % of the potential. The 2016-2024 record has a median offset of +1.93 min; from 2022 the
daily shifts are larger.

### Checks of the processing

Each processing step was checked at the half-hour of 1 August 2022, 09:00 to 09:30, and by
repeating the FFT analysis on data from different stages:

- **Resampling.** The 1-minute raw values from 09:01 to 09:30, averaged by hand, give
  654.8015067 W m^-2^. The meteo screening, which reads the database and resamples to 30 minutes,
  gives 654.801507 W m^-2^. Resampling introduces no shift.
- **Nighttime offset correction.** With the correction of negative nighttime values (an offset of
  about -10 W m^-2^), the value is 665.219439 W m^-2^, the same in the screening output and in the
  screened data downloaded from the database. After all `SW_IN` sources are merged, the offset
  correction runs again on the merged record and gives 664.929319 W m^-2^.
- **Middle timestamp.** When the record is loaded for gap-filling, its timestamp is converted to
  `TIMESTAMP_MIDDLE`. The value at 09:15 is 664.929319 W m^-2^, unchanged.
- **Gap-filling and merging.** The value is unchanged after gap-filling and after the merge with
  the flux data. Air temperature at 09:15, averaged by hand from the 1-minute raw files, matches as
  well.
- **Database against raw files.** The FFT analysis gives identical results on the 1-minute raw
  file of August 2022 and on the 1-minute data downloaded from the database, with a median shift of
  6.39 min at 30-minute resolution and 5.90 min at 1-minute resolution. The same holds for
  July 2021, at both resolutions.

![Time shift in incoming shortwave radiation, 2016-2024, from the phase of the 24-hour FFT component of measured against potential radiation, 30-minute data. Top: daily shifts with a 15-day rolling median, showing a lag from 2022. Middle: distribution of all shifts, median +1.93 min. Bottom: monthly distributions.](images/CH-LAE_2016-2024_phase_shift_fft_SWINvsSWINPOT.png){#fig-phaseshiftfft-16-25}

## Corrected for FP2026.2

Two problems of earlier processing versions of the LI-7500 record are corrected in FP2026.2:

- **Clock shift of July 2013.** The raw files of 6 to 12 July 2013 carry names 7 hours late. The
  flux records of this week are moved back by 7 hours before post-processing; 12 July 2013 from
  13:15 to 19:45 has no flux. See
  [Yearly Notes, 2013](Yearly_Notes.md#shifted-timestamps-in-july-2013).
- **`VPD` as a driver of the Level-1.1 correction.** The correction is now fitted without `VPD`.
  Near saturation the humidity probes before and after 2016 differ, and with `VPD` as a driver the
  correction of the cold nights of 2004-2015 was only about a third of that of 2016-2017. See
  [Level-1.1](L1.1.md).

## References

::: {#refs}
:::
