# Known Issues

Open points that affect users of FP2026.1 and of FP2026.2, which is in progress. Sections that
concern only the LI-7500 years of FP2026.2 say so. Limitations of a single meteorological variable
are on that variable's page under [Meteorological data](Meteo_Data.md), and release details under
[Dataset versions](Dataset_Versions.md). Planned work is tracked in the
[Issues](https://github.com/holukas/dataset_ch-lae_flux_product/issues) of the repository.

## No measured `H` from 10 January to 20 March 2019

There is no measured sensible heat flux from 10 January 2019 15:15 to 20 March 2019 18:45
(`TIMESTAMP_MIDDLE`), 3320 half-hours. The gas fluxes `FC`, `NEE` and `LE` have the same gap. The
gap-filled series `H_L3.1_L3.3_CUT_NONE_QCF_gfXG` covers the period with values from the model
alone, which `FLAG_H_L3.1_L3.3_CUT_NONE_QCF_gfXG_ISFILLED` marks.

The gap has two causes:

- Setup period `2019_2` (10 to 17 January 2019), in which both LI-7200 units were defective, has
  no Level-1 run, so its sonic data were not processed.
- In `2019_3` (17 January to 20 March 2019) the open-path LI-7500 stood in for the LI-7200. Its run
  is processed with the other `IRGA75` fluxes but is used in neither release: the merged record of
  FP2026.2 takes this period from the LI-7200, gap-filled.

The same sonic was in operation throughout, so `H` could be computed for both setup periods. This
is under review. The other long gaps are listed under [Level-4.1](L4.1.md).

## `H` in 2024 is lower than in the other years

| Annual mean `H` (W m^-2^) | 2024 | Other full years, 2016 to 2025 |
|---|---|---|
| Level-1, before quality control | 25.8 | 33.9 to 51.8 |
| Gap-filled | 25.1 | 32.4 to 45.4 |

: Annual mean sensible heat flux of 2024 against the other full years. {#tbl-h-2024}

The Level-1 `H` of 2024 is about a third lower than in the other years. The cause is the weather:
in 2024 incoming shortwave radiation was 12 % below the other years, the rain sum was the highest
of the period (1151 mm), and `VPD` was the lowest. No instrument fault was found, so the low `H`
of 2024 is not an artefact.

## MDS in spring 2016

The measurements of the start-up period, 1 March to 25 May 2016, were removed, so the gap
includes the leaf-out. MDS fills this gap from records far away in time and gives a much larger
uptake than XGBoost:

| April-May 2016 `NEE` (`CUT_50`, gC m^-2^) | MDS | XGBoost |
|---|---|---|
| Current processing | -274 | -82 |
| FP2026.1 | -235 | -113 |

: Sum of `NEE` over April and May 2016 by gap-filling method. {#tbl-mds-2016}

In the other years the April-May sums of both methods lie between -16 and -188 gC m^-2^. XGBoost
is the gap-filling method of this dataset, and MDS is included for comparison only. Use the
XGBoost series (`_gfXG`). See [Level-4.1](L4.1.md).

## The LI-7500 fluxes are not part of FP2026.1

FP2026.1 contains fluxes of the enclosed-path LI-7200 (`IRGA72`) only, from 11 January 2016.
FP2026.2, in progress, adds the fluxes of the open-path LI-7500 (`IRGA75`) for 2004-2015, with the
CO~2~ flux corrected at [Level-1.1](L1.1.md). It will contain FP2026.1 in full and supersede it. In
its merged record, `FLAG_FLUX_SOURCE` gives the analyser of each half-hour; which LI-7500 data the
record leaves out is listed under [FP2026.2](Version_FP2026.2.md#what-it-adds).

## The storage term of the LI-7500 drifts

This concerns `NEE` and the storage term of 2004-2017 in the LI-7500 processing of FP2026.2. The
LI-7200 storage term is not affected. Over a year, a storage term should sum to about zero:

| Storage term (gC m^-2^ per year) | Annual sums | 2016-2017 overlap |
|---|---|---|
| LI-7500, single-point (`SC_SINGLE_gfRMED_L3.1`), 2004-2017 | -25 to -196 | -159 |
| LI-7200 | -23 to +15 | +0.7 |

: Annual sums of the storage term of the two analysers. {#tbl-storage-drift}

The cause lies in the CO~2~ concentration of the LI-7500. With wet or blocked windows, at an AGC
above 55 or after rain, it reads 33 to 106 ppm too high. Across its gaps the concentration rises by
12.4 ppm (median). The rise falls into the gap and is not counted, while the return after the gap
enters the storage term as a negative flux. This accounts for about 130 of the 160 gC m^-2^ per
year of the drift. The concentration error changes the flux itself by less than 1 %, so it does
not explain the low fluxes of the LI-7500 in humid conditions described in the next sections.

A screen of the concentration readings is set for the next processing run and is not yet in the
data. Its conditions are listed under [FP2026.2](Version_FP2026.2.md#prepared-for-the-next-run);
the method, the evidence and the tests are on
[Level 3.1](L3.1.md#drift-of-the-li-7500-storage-term). In a test with the chain (`CUT_50`), the
screen gives:

- a storage term of -5 to +39 gC m^-2^ per year in 2004-2015, robust to the settings;
- an annual `NEE` higher by about 70 gC m^-2^ per year in 2004-2015 and by 118 in 2016-2017;
- an overlap gap to the LI-7200 smaller by about 120 of about 400 gC m^-2^ per year.

In the current processing, the storage term of the LI-7500 and its `NEE` still contain the drift.

## The LI-7500 misses the wet half-hours

This concerns `NEE` of 2004-2015 in FP2026.2. The correction of [Level-1.1](L1.1.md) works on the
half-hours the LI-7500 measured. Most of the remaining difference to the LI-7200 lies in the
half-hours it did not measure.

The LI-7500 loses many half-hours in wet weather (rain, fog, dew, water on the windows), when the
LI-7200 still measures. Gap-filling learns only from the conditions the LI-7500 measured, so it
fills these gaps with too much uptake. Open-path analysers are known to lose data in wet weather,
but no published study was found that quantifies the resulting bias against a co-located
enclosed-path analyser.

In the 2016-2017 overlap the LI-7500 shows 436 gC m^-2^ (2016) and 370 gC m^-2^ (2017) more uptake
than the LI-7200. About 96 % of this gap lies in the half-hours that at least one analyser
gap-filled, so it is mostly a property of the gap-filling, not of the measured flux. The full split
is on [Comparisons of the LI-7500 years](IRGA75_Comparisons.md#the-2016-2017-overlap).

The humid half-hours show where the gap comes from. At a relative humidity of 99.5 % or more, the
LI-7500 measures only 8 to 9 % of the half-hours, and the two gap-filling models fill the others
very differently:

| Filled `NEE` at 99.5 % RH or more (µmol m^-2^ s^-1^) | LI-7500 | LI-7200 |
|---|---|---|
| Current processing | 0.1 to 0.5 | 3.0 to 3.5 |
| With the storage correction of the next run | 0.95 | 3.33 |

: `NEE` that the gap-filling model of each analyser gives for the humid half-hours the LI-7500 did
not measure, 2016-2017. {#tbl-humid-filled}

The humid half-hours the LI-7500 does measure read only 0.3 to 1.1 µmol m^-2^ s^-1^ low (medians,
not stable between the two years). The deficit therefore lies mostly in the gaps where the LI-7500
measured nothing, mostly in rain: its model never sees a flux during rain, while the LI-7200
measures it. The effect on the LI-7500 years 2004-2015 is described under
[Biases of the LI-7500 NEE against a climate baseline](#biases-of-the-li-7500-nee-against-a-climate-baseline).

## Nighttime NEE of the LI-7500 is too low on cold and humid nights

This concerns nighttime `NEE` of 2004-2015 in FP2026.2. The measured nighttime `NEE` of the
LI-7500 falls with humidity and cold. In 2016-2017, below 5 °C and at a relative humidity of 99.5 %
or more, its median after all quality tests is +0.9 µmol m^-2^ s^-1^, and 39 % of the values are
negative, which would mean uptake in the dark. The LI-7200 stays near +2 µmol m^-2^ s^-1^ (+1.8 to
+2.4) in every humidity class, with 10 to 13 % negative values.

An analysis of November 2026 (scratch analysis; a notebook is to follow) compared the cold nights
(November to March, below 2 °C) of the LI-7500 with a model of the LI-7200 nights of 2016-2025 under
the same conditions:

- **The bias is in the measured covariance** of vertical wind and CO~2~ density. The density (WPL)
  terms, the storage term, the calibration of the CO~2~ and H~2~O readings, the spectral correction
  and the time lag together account for at most about 0.1 µmol m^-2^ s^-1^.
- **It has three nearly independent parts:** overcast or foggy nights (cloud cover estimated from
  incoming longwave radiation and air temperature), calm air, and a wet window (AGC above 50). Clear
  cold nights are about unbiased from 2008. The correction of [Level-1.1](L1.1.md) removes most of
  the calm-air part, because it depends on wind; the overcast and wet-window parts remain.
- **It does not change over time.** Under the same conditions the bias is the same from 2005/06 to
  2016/17. It appears larger before 2016 because the winters were colder and because a selection by
  relative humidity picks different nights before and after the humidity probe was changed in
  January 2016 ([RH](Meteo_Data_RH.md#known-limitations)).
- **Its size in the product:** cold-night `NEE` of 2004-2015 is about 1.2 µmol m^-2^ s^-1^ too low,
  about 53 gC m^-2^ per year towards uptake. About 90 % of it lies in gap-filled overcast nights.
  Nights above 2 °C were not analysed.

Fog or rime on the windows explains the wet-window part only. The cause of the overcast and calm-air
parts is not known: heat entering the optical path that the sonic anemometer does not register is
possible, but cannot be tested without the raw data.

Many of these nights pass the quality tests, and gap-filling learns from them.
[Level-3.2](L3.2.md) removes the clearest cases: four fog episodes in 2004, 2013 and 2014 by hand,
and, by a test, whole nights whose median is clearly below zero. Nights that read too low without a
clearly negative median remain. Calm and cold nights also remain too low after the correction of
[Level-1.1](L1.1.md#known-limitations).

In the 2016-2017 overlap, with both analysers on the same sonic anemometer, the median difference
of nighttime `NEE`, LI-7500 minus LI-7200, in µmol m^-2^ s^-1^, is:

- at a relative humidity of 99.5 % or more, about -1.1 below 0 °C and -0.4 at 0-5 °C;
- at 97-99.5 %, -0.6 to -0.9 (below 0 °C and at 5-10 °C);
- below 97 % and below 10 °C, +0.2 to +0.9.

The automatic gain control (AGC) value of the LI-7500 does not separate these records. Removing
every LI-7500 nighttime record below 5 °C at 99.5 % relative humidity or more, whatever its sign,
was tested and is not adopted. It removes about 4 % of the nighttime records but widens the gap to
the LI-7200 in the overlap by 29 to 127 gC m^-2^ per year, because the gap-filling then
extrapolates the humid nights even lower.

What this means for the data:

- Measured and gap-filled nighttime `NEE` of the LI-7500 years is likely biased towards uptake on
  cold overcast, foggy and calm nights, by about 53 gC m^-2^ per year in 2004-2015. This is part of
  the night deficit under
  [Biases of the LI-7500 NEE against a climate baseline](#biases-of-the-li-7500-nee-against-a-climate-baseline),
  not an addition to it. Most of the bias of the annual sums lies in the humid gaps rather than in
  the measured nights (see [The LI-7500 misses the wet half-hours](#the-li-7500-misses-the-wet-half-hours)).
- `RECO` from the nighttime partitioning is fitted on these nights and is likely too low in winter.
- Do not compare LI-7500 and LI-7200 nights selected by a relative humidity near saturation: the
  selection differs between the two humidity probes.

Not yet resolved. A nighttime term of the Level-1.1 correction driven by cloud cover, a cloud-cover
driver for the gap-filling and a screen of wet-window records are under test.

## Biases of the LI-7500 NEE against a climate baseline

This concerns `NEE` of 2004-2015 in FP2026.2. The LI-7500 years cannot be checked against a second
analyser. They are compared instead with a climate baseline: a model of daytime and nighttime `NEE`
trained on the LI-7200 years 2016-2025, with meteorological drivers only. Applied to the weather of
another year, it gives the `NEE` that the forest of 2016-2025 would have exchanged under that
weather.

| Period | Night | Day |
|---|---|---|
| LI-7500, 2004-2009 | about -200 to -250 | about +230 (single years +200 to +370 with the storage correction) |
| LI-7500, 2010-2015 | about -200 to -250 | about 0 |
| LI-7500, 2016-2017 overlap | about -200 to -250 | -105 (-34 with the storage correction) |
| LI-7200 years | -40 to +30 | -280 to +150 |

: Difference of the gap-filled `NEE` (`CUT_50`) to the climate baseline, in gC m^-2^ per year.
{#tbl-baseline-bias}

- **Night: about -200 in every LI-7500 period.** This is the deficit of the humid gaps described
  under [The LI-7500 misses the wet half-hours](#the-li-7500-misses-the-wet-half-hours).
- **Day: about +230 in 2004-2009.** The uncorrected LI-7500 flux of these years matches the
  baseline, so the correction of [Level 1.1](L1.1.md) probably over-corrects their daytime flux
  ([evidence](IRGA75_Comparisons.md#does-the-correction-hold-for-the-early-years)). An estimate
  from the LI-7500 data alone, on frozen winter days, puts the over-correction at about 15 % of the
  heating part of the correction in 2004-2015 (factor 0.84, 16-84 % range 0.69-0.99), without a
  step between 2007 and 2008, or about 80 to 150 gC m^-2^ per year
  ([Approaches to the correction](L1.1_Approaches.md#investigations-at-ch-lae)). It covers frozen
  days only, so it does not settle the summers.

In 2004-2009 the two biases largely offset each other in the annual sum; in 2010-2015 the night
deficit remains. This is why the annual sums show no clear step at the change of analyser:
2004-2015 average -82 gC m^-2^ per year, 2016-2025 -18
([overview of the merged NEE record](notebooks/90_OVERVIEW/FLUX_NEE.html)).

The baseline describes the forest of the LI-7200 years, so it cannot settle whether the forest
itself changed: a real difference of the forest in 2004-2009 would appear against it as a bias of
the same kind. Checks of the analyser, the raw data and the calibration found no fault of the
measured flux. Whether the forest changed, and how the early years compare with FLUXNET,
@etzold_carbon_2011 and the biometric estimates, is discussed on
[Comparisons of the LI-7500 years](IRGA75_Comparisons.md#what-this-means).

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
  200 gC m^-2^ per year, and that of 2004-2009 a daytime bias towards release of about
  230 gC m^-2^ per year. FP2026.2 states both as uncertainties and does not correct them.
  Differences between years smaller than these are not resolved. Where a result depends on the
  absolute sink strength, prefer the LI-7200 years.
- The nighttime partitioning fits `RECO` on measured `NEE` only, so the missing wet nights bias
  `RECO` and `GPP` low.
- Shortwave radiation was measured from 14 September 2005, so the daytime partitioning gives no
  result before that date ([Level 4.2](L4.2.md)). In 2005 most of the meteorological drivers are
  gap-filled.
- The LI-7500 record starts on 30 March 2004, so `NEE`, `LE` and `H` of January to March 2004 are
  entirely gap-filled. Their `SW_IN` driver is unreliable in January 2004, about 2.7 times the mean
  January total (see [SW_IN](Meteo_Data_SW_IN.md)).

## Calibration of the LI-7500 in 2004-2010

This concerns `NEE` and `LE` of 2004-2010 in FP2026.2. The field checks in the fieldbook and a
comparison of the mean concentrations with reference records (scratch analysis of November 2026; a
notebook is to follow) show two calibration errors of the LI-7500 that FP2026.2 does not correct:

- **CO~2~ read too low** by about 6 ppm in 2004-2005, 21 ppm from 7 February 2006 to 25 September
  2007, and 44 ppm from 26 September to 19 December 2007, the dates of the field calibrations. The
  covariance is hardly affected, but the density (WPL) terms are too small, and on balance the
  CO~2~ flux shows too much uptake. Correcting it would raise annual `NEE` by about 11 to 55 gC m^-2^ per year in
  2004-2007.
- **H~2~O read about 30 % high** from May 2008 to December 2010. `LE` of this period is likely too
  high by a similar fraction: with the reading corrected, the summer midday energy balance closure
  of 2008-2010 falls from 1.10 to 0.93, the level of the other years. Through the density
  correction, the CO~2~ flux of this period shows too little uptake, by about
  0.5 µmol m^-2^ s^-1^ at summer midday. Correcting it would lower annual `NEE` by about 27 to
  38 gC m^-2^ per year in 2008-2010.

Neither error explains the cold-night or the daytime biases described above.

## LE of the two gas analysers differs in humid and cold conditions

This concerns `LE` and `ET` across the change of gas analyser on 1 January 2016. In 2016-2017, when
both analysers ran, the open-path LI-7500 (`IRGA75`) measured a higher `LE` than the enclosed-path
LI-7200 (`IRGA72`): about 9 % higher overall on the half-hours both measured. The difference grows
with humidity (@tbl-le-ratio) and with cold: the ratio is 2.7 below 0 °C and 1.03 above 20 °C. The
gap-filled `LE` of the parallel period is 20 % higher with the LI-7500.

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

The likely cause lies in the LI-7200, not in the open-path analyser. In the tube and cell of an
enclosed-path analyser, water vapour adsorbs on the walls, which damps the H2O fluctuations more
the higher the humidity. The `IRGA72` runs correct for this (Fratini et al. 2012), but such
corrections often fall short above about 90 % relative humidity. Self-heating of the open-path
analyser would bias its flux the other way.

The energy balance supports this (@tbl-le-ratio). In dry air both analysers close it to about the
same degree. With rising humidity the closure of the LI-7200 falls faster: at 99.5 % relative
humidity or more it is 0.45, that of the LI-7500 0.69. At high humidity the LI-7500 `LE` is
therefore the more complete one.

What this means for the data:

- The `LE` and `ET` of the LI-7200 (FP2026.1, and FP2026.2 from 2016) are likely too low in humid
  and cold conditions.
- In the merged record of FP2026.2, the step in `LE` and `ET` at 1 January 2016 is instrumental.
  The gap-filled `ET` averages about 740 mm per year in 2004-2015 (LI-7500) and about 615 mm in
  2016-2025 (LI-7200), a step of about -126 mm per year. Do not read this difference as a change of
  the ecosystem.
- `H` comes from the same sonic anemometer for both analysers and is homogeneous across 2016: the
  ratio of the two is 0.99 in the overlap, and they agree to within 2 % in 2016 and 2017.

The `LE` of the two analysers is not homogenized in FP2026.2.

## Faulty sample flow of the LI-7200 in December 2022

From 5 to 20 December 2022 the logged sample flow of the LI-7200 was low and intermittent, mostly
0 to 3 l min^-1^ from 8 to 19 December. At this flow the measuring cell is not flushed with ambient
air, as in the other flow faults of [Level 3.2](L3.2.md). The nighttime `NEE` kept after all quality
tests in this period is +5 to +16 µmol m^-2^ s^-1^ at about -8 °C, far above a plausible winter
respiration. These values are still in FP2026.1 and in the current processing of FP2026.2. Their
removal, of `NEE` and `LE` from 5 December 17:15 to 20 December 11:15 (`TIMESTAMP_MIDDLE`), is set
for the next run. Until then, do not use the measured fluxes of the LI-7200 of this period.

The logged flow cannot be used to search for further faults in 2022: from March to November 2022
the flow channel reads 0.0 while the fluxes are normal, a logging fault of the channel.

## Night-time NEE keeps rising above the USTAR thresholds

At the same air temperature, night-time `NEE` of both analysers keeps rising with `USTAR` up to
about 0.9 to 1.0 m s^-1^, well above the thresholds of either release ([Level 3.3](L3.3.md)). It
does not reach the plateau above the threshold that the USTAR filter assumes. Two explanations are
possible, and the tower data cannot separate them: at moderate turbulence part of the respired CO2
still leaves the site without passing the sensor, or wind draws additional CO2 out of the soil and
the litter.

The respiration of the daytime partitioning (`RECO_DT`, [Level 4.2](L4.2.md)) is not independent of
the threshold. Its temperature sensitivity comes from the night records above the threshold
applied in the chain, so `RECO_DT` moves with that threshold. At the thresholds of FP2026.2:

- night `NEE` divided by `RECO_DT` of the same half-hour reaches 1 at a `USTAR` of about 0.7 to
  0.9 m s^-1^ and keeps rising, from May to October to about 1.5, for both analysers;
- the nights kept at the median thresholds lie 7 % (LI-7200) and 2 % (LI-7500) below `RECO_DT`;
- the two agree at 0.64 (LI-7200) and 0.46 m s^-1^ (LI-7500), for the LI-7200 near `CUT_84`.

With the thresholds of FP2026.1 in the chain, the kept nights agreed with `RECO_DT` near `CUT_16`.
The comparison therefore does not constrain the threshold.

Part of the high night `NEE` at high `USTAR` may be CO2 flushed out of the canopy air: when the wind
rises after calm hours, CO2 that collected in the canopy passes the sensor. @tbl-flushing compares
the nights after 3 calm hours (mean `USTAR` below 0.3 m s^-1^) with those after 3 windy hours
(above 0.7 m s^-1^).

| Analyser | `USTAR` (m s^-1^) | After calm hours | After windy hours |
|---|---|---|---|
| LI-7500 | 0.7 to 0.9 | 1.4 | 1.05 |
| LI-7500 | above 0.9 | 1.5 | 1.4 |
| LI-7200 | above 0.9 | 1.15 to 1.2 (moderately calm hours) | 1.1 |

: Night `NEE` as a multiple of `RECO_DT`, by the turbulence of the previous 3 hours. {#tbl-flushing}

For the LI-7500 the excess after calm hours appears from a `USTAR` of 0.7 m s^-1^. For the LI-7200
it appears only above 0.9 m s^-1^, and not for the few records after the calmest hours; from 0.5 to
0.9 m s^-1^ its night `NEE` lies further below `RECO_DT` after calm hours. The calm cases are few
(11 to 75 half-hours in the calmest class). After sustained wind an excess over `RECO_DT` remains,
which flushing does not explain. Right above the threshold, the kept night records after calm hours
read low rather than high: 0.92 to 0.96 of `RECO_NT`, the respiration of the nighttime
partitioning, at the `CUT_50` of the record of the site, against 1.02 to 1.10 after mixed hours. No
release of stored CO2 shows there.

The storage term does not capture this release, which is a known limitation. The storage term of
[Level 3.1](L3.1.md) comes from the CO2 concentration at one height, 47 m. In the flush cases it is
not clearly negative, although CO2 leaving the canopy air should make it so, and the flushed CO2
enters `NEE`.

The measured night-time `NEE` and the night-time respiration therefore depend on the threshold. A
higher threshold keeps only the windier nights, whose `NEE` is higher, and the gap-filled nights and
the night-time partitioning follow them. FP2026.2 uses the lowest defensible thresholds (the moving
point method). Estimated from the measured nights alone, the night-time respiration at the FP2026.2
median thresholds is 26 % (LI-7200) and 20 % (LI-7500) higher than at the threshold of FP2026.1.
The `USTAR` uncertainty of [Level 4.1](L4.1.md), from the `CUT_16` and `CUT_84` series, covers only
part of this dependence.

::: {.callout-tip title="Notebook"}

[USTAR threshold detection](notebooks/30_FLUX_POST-PROCESSING_CHAIN/USTAR_THRESHOLD_DETECTION_2004-2026.09.html),
sections 4, 6, 9, 10 and 11

:::

## USTAR thresholds compared with FLUXNET

FLUXNET detects USTAR thresholds per year with the method of @pastorello_fluxnet2015_2020. For
CH-LAE, the thresholds it detects change markedly after 2015 (@fig-ustar-fluxnet1). The cause is
not known. The change coincides with a change of gas analyser. Until 11 January 2016 the fluxes
come only from the open-path LI-7500. A quantum cascade laser in 2005 and 2008 and, probably, an
LI-7200 from about December 2010 to June 2011 measured beside it for limited periods
([Yearly Notes](Yearly_Notes.md#probable-li-7200-measurements-december-2010-to-june-2011)), but
they are not part of the flux record. From 14 December 2017 the fluxes come only from the
enclosed-path LI-7200, except from 17 January to 20 March 2019, when the LI-7500 stood in for it. From 11 January 2016 to
12 December 2017 the two ran in parallel. Before 2016 the threshold detection therefore used LI-7500 `NEE`, corrected for
self-heating in a similar way to @kittler_high-quality_2017.

This dataset does not use the FLUXNET thresholds. It filters `NEE` at three constant thresholds per
analyser ([Level 3.3](L3.3.md)). FLUXNET (ONEFlux v1.3) pools the moving point and the change point
methods, while the thresholds of FP2026.2 come from the moving point method alone
(@tbl-ustar-fluxnet).

| Thresholds for half-hourly `NEE` | m s^-1^ |
|---|---|
| FP2026.1, LI-7200 (`CUT_50`) | 0.304 |
| FP2026.2, LI-7200 (`CUT_50`) | 0.523 |
| FP2026.2, LI-7500 (`CUT_50`) | 0.436 |
| FLUXNET, constant threshold (`CUT_REF`) | 0.43 |
| FLUXNET, per year (`VUT_REF`) | 0.23 to 0.35 until 2015, 0.46 to 0.60 from 2016 |

: USTAR thresholds of this dataset and of FLUXNET. The FP2026.2 thresholds are those applied in the
processing of 1 November 2026. {#tbl-ustar-fluxnet}

The two FP2026.2 sets differ because of the years each record covers, not because of the
instruments: on the records both analysers measured in 2016-2017, the method gives the same
`CUT_50` (0.311 and 0.301 m s^-1^). One set from the merged record of the site is computed but not
adopted ([FP2026.2](Version_FP2026.2.md#prepared-for-the-next-run)).

The thresholds explain the differences in the annual sums from 2016, but only part of them before:

- **2016-2024, LI-7200.** At the thresholds of FP2026.2 the two products agree on average. Over
  2018-2024 this product averages -32 gC m^-2^ per year, FLUXNET +3 (`VUT_REF`) and -48
  (`CUT_REF`); the night sums are 844 and 830 gC m^-2^. Single years still differ by up to about
  200 gC m^-2^. On the half-hours both measured, the two agree. FLUXNET keeps 10 to 19 % of the
  nights as measured, this product 15 to 25 % (28 to 43 % with the thresholds of FP2026.1). With
  the thresholds of FP2026.1 this product showed more net uptake than FLUXNET; the higher
  thresholds keep fewer and windier nights, with higher `NEE`, and remove most of this difference.
- **2005-2015, LI-7500.** FLUXNET shows more net uptake: -437 gC m^-2^ per year in 2007-2015
  against -138 here, and -141 against +116 in 2005-2006. The difference lies at night, where the
  sums are about 680 gC m^-2^ here and 350 in FLUXNET; by day the two agree. It comes from the
  different corrections of the open-path flux and the low winter nights of FLUXNET. The threshold
  of this product, above the FLUXNET thresholds of these years, adds to it (see
  [Comparisons of the LI-7500 years](IRGA75_Comparisons.md#comparison-with-fluxnet)).

Within FLUXNET the same dependence shows: `VUT_REF` gives more uptake than `CUT_REF` where its
yearly thresholds lie below the constant one (to 2015), and less uptake where they lie above it
(from 2016).

![USTAR thresholds detected by FLUXNET, based on data 2004-2023, from the file `FLX_CH-Lae_FLUXNET2015_AUXNEE_2004-2023_1-3.csv`.](images/USTAR_thresholds_from_FLUXNET_NEE_VUT_2004-2023.png){#fig-ustar-fluxnet1}

::: {.callout-tip title="Notebook"}

[USTAR threshold detection](notebooks/30_FLUX_POST-PROCESSING_CHAIN/USTAR_THRESHOLD_DETECTION_2004-2026.09.html),
section 7; [Sonic anemometer data](notebooks/90_OVERVIEW/Sonic_Anemometer.html)

:::

## Time shift in incoming shortwave radiation from 2022

From 2022 onwards, the daily cycle of incoming shortwave radiation at 47 m (`SW_IN_T1_47_1`) lags
behind potential radiation by a few minutes (@fig-phaseshiftfft-16-25). The shift is already
present in the raw data, and no error was found in the processing. Its cause is not known. The
product page is [Incoming shortwave radiation at 47 m](Meteo_Data_SW_IN.md).

### Method

The shift was detected from the phase of the 24-hour component (FFT) of measured and potential
radiation on clear days, on which the measured radiation reached at least 70 % of the potential.
The 2016-2024 record has a median offset of +1.93 min; from 2022 the daily shifts are larger.

### Checks of the processing

Each processing step was checked at the half-hour of 1 August 2022, 09:00 to 09:30
(@tbl-swin-checks). The value does not change through resampling, the change to the middle
timestamp, gap-filling or the merge with the flux data, so none of these steps introduces a shift.
Air temperature at 09:15, averaged by hand from the 1-minute raw files, matches as well.

| Stage | `SW_IN` (W m^-2^) |
|---|---|
| 1-minute raw values from 09:01 to 09:30, averaged by hand | 654.8015067 |
| Meteo screening, which reads the database and resamples to 30 minutes | 654.801507 |
| With the correction of negative nighttime values (an offset of about -10 W m^-2^), in the screening output and in the screened data downloaded from the database | 665.219439 |
| Offset correction run again on the merged record of all `SW_IN` sources | 664.929319 |
| At 09:15 after conversion to `TIMESTAMP_MIDDLE` for gap-filling, after gap-filling, and after the merge with the flux data | 664.929319 |

: Value of the half-hour of 1 August 2022, 09:00 to 09:30, at each processing stage. {#tbl-swin-checks}

The FFT analysis was also repeated on data from different stages. It gives identical results on
the 1-minute raw file of August 2022 and on the 1-minute data downloaded from the database: a
median shift of 6.39 min at 30-minute resolution and 5.90 min at 1-minute resolution. The same
holds for July 2021, at both resolutions.

![Time shift in incoming shortwave radiation, 2016-2024, from the phase of the 24-hour FFT component of measured against potential radiation, 30-minute data. Top: daily shifts with a 15-day rolling median, showing a lag from 2022. Middle: distribution of all shifts, median +1.93 min. Bottom: monthly distributions.](images/CH-LAE_2016-2024_phase_shift_fft_SWINvsSWINPOT.png){#fig-phaseshiftfft-16-25}

## Corrected for FP2026.2

Two problems of earlier processing versions of the LI-7500 record are corrected in FP2026.2:

- **Clock shift of July 2013.** The raw files of 6 to 12 July 2013 carry names 7 hours late. The
  flux records of this week are moved back by 7 hours before post-processing; 12 July 2013 from
  13:15 to 19:45 has no flux. See
  [Yearly Notes, 2013](Yearly_Notes.md#shifted-timestamps-in-july-2013).
- **`VPD` as a driver of the Level-1.1 correction.** The correction is now fitted without `VPD`,
  because the humidity probes before and after 2016 differ near saturation. With `VPD`, the cold
  nights of 2004-2015 were corrected too little. See [Level-1.1](L1.1.md).

## References

::: {#refs}
:::
