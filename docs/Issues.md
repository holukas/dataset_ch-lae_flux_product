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
gives 25.0 W m^-2^ against 32.4 to 45.4 W m^-2^. Incoming shortwave radiation was also lower in
2024 than in the other years, but the cause has not been checked yet. Treat annual `H` in 2024 with
caution until it is.

## MDS in spring 2016

In spring 2016 the measurements of the start-up period were removed (1 March to 25 May 2016), and
the gap includes the leaf-out. MDS fills this gap from records far away in time and gives a much
larger uptake than XGBoost: the April-May sum of `NEE` (`CUT_50`) is -240 gC m^-2^ with MDS and
-132 gC m^-2^ with XGBoost (-235 and -113 in FP2026.1). In the other years the April-May sums of
both methods lie between -31 and -192 gC m^-2^. XGBoost is the gap-filling method of this dataset, and MDS is included for
comparison only. Use the XGBoost series (`_gfXG`). See [Level-4.1](L4.1.md).

## The LI-7500 fluxes are not part of FP2026.1

FP2026.1 contains fluxes of the enclosed-path LI-7200 (`IRGA72`) only, from 11 January 2016.
FP2026.2, in progress, adds the fluxes of the open-path LI-7500 (`IRGA75`) for 2004-2015, with the
CO~2~ flux corrected at [Level-1.1](L1.1.md). Its merged record takes the fluxes from the LI-7500
until 31 December 2015 and from the LI-7200 from 1 January 2016; `FLAG_FLUX_SOURCE` gives the
analyser of each half-hour (`75` or `72`). The LI-7500 data of the parallel period 2016-2017 train
and check the correction. They are not in the merged record, and neither is the stand-in run of 2019.
FP2026.2 will contain FP2026.1 in full and supersede it.

## Annual NEE of the LI-7500 years may show too much uptake

This concerns `NEE` of 2004-2015 in FP2026.2. The correction of [Level-1.1](L1.1.md) works on the
half-hours the LI-7500 measured. The remaining uncertainty lies in the half-hours it did not
measure.

The LI-7500 loses many half-hours in wet weather (rain, fog, dew, water on the windows), when the
LI-7200 still measures. Gap-filling learns only from the conditions the LI-7500 measured, so it fills
these gaps as if they were dry, with too much uptake. Open-path analysers are known to lose data in
wet weather, but no published study was found that quantifies the resulting bias against a
co-located enclosed-path analyser. From 11 January 2016 to 12 December 2017, when both analysers
ran:

- on the half-hours both measured, the corrected LI-7500 shows 45 gC m^-2^ more uptake than the
  LI-7200 over the whole period;
- the gap-filled `NEE` of the LI-7500 shows 235 gC m^-2^ (2016) and 289 gC m^-2^ (2017) more
  uptake than that of the LI-7200.

For 2004-2015 the size of this effect is unknown. A correction calibrated in 2016-2017 would add
100 to 200 gC m^-2^ per year, but the annual sums of the LI-7500 years show no step of that size
against those of the LI-7200 years: 2004-2015 average -152 gC m^-2^ per year, 2016-2025 -117
([overview of the merged NEE record](notebooks/90_OVERVIEW/FLUX_NEE.html)). FP2026.2 therefore
keeps the gap-filled series without such a correction.

What this means for the data:

- The annual `NEE` of 2004-2015 may show too much uptake, by up to 100 to 200 gC m^-2^ per year.
  Differences between years smaller than that are not resolved.
- The nighttime partitioning fits `RECO` on measured `NEE` only. The missing wet nights therefore
  bias `RECO` and `GPP` low.
- In 2004 no shortwave radiation was measured, so the daytime partitioning gives no result for that
  year. In 2005 most of the meteorological drivers are gap-filled.
- The LI-7500 record starts on 30 March 2004, so `NEE`, `LE` and `H` of January to March 2004 are
  entirely gap-filled. Their `SW_IN` driver is unreliable in January 2004, about 2.7 times the mean
  January total (see [SW_IN](Meteo_Data_SW_IN.md)).

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

What this means for the data:

- Measured and gap-filled nighttime `NEE` of the LI-7500 years is likely biased towards uptake in
  cold and humid conditions. The effect on the annual sums is not quantified. It adds to the bias
  from the wet-weather gaps described under *Annual NEE of the LI-7500 years may show too much
  uptake*.
- `RECO` from the nighttime partitioning is fitted on these nights and is likely too low in winter.

Not yet resolved.

## The early LI-7500 years are a weak sink

This concerns `NEE` of 2004-2009 in FP2026.2. In 2005-2009 the annual `NEE` averages -38 gC m^-2^
per year. This is far less uptake than the biometric estimates for 2006-2009 and the earlier flux
estimates of FLUXNET and @etzold_carbon_2011. The shortfall lies in the daytime uptake. Checks of
the analyser, the raw data and the calibration found no measurement fault. The cause is either a
real loss of uptake after the drought of 2003 or a correction at [Level 1.1](L1.1.md) that is too
large for these years. FP2026.2 keeps these years unchanged. Where a result depends on the
absolute sink strength, prefer the LI-7200 years. The comparisons and checks are on
[Comparisons of the LI-7500 years](IRGA75_Comparisons.md).

## LE of the two gas analysers differs in humid and cold conditions

This concerns `LE` and `ET` across the change of gas analyser on 1 January 2016. In 2016-2017,
when both analysers ran, the open-path LI-7500 (`IRGA75`) measured a higher `LE` than the
enclosed-path LI-7200 (`IRGA72`). On the half-hours both measured, it is about 9 % higher overall,
and the difference grows with humidity and cold:

| relative humidity | `IRGA75` / `IRGA72` |
|---|---|
| below 60 % | 1.03 |
| 60-80 % | 1.05 |
| 80-90 % | 1.15 |
| 90-95 % | 1.49 |
| 95 % and above | 2.15 |

: Ratio of the `LE` sums of the two analysers on the half-hours both measured after all quality
tests, 11 January 2016 to 12 December 2017, by relative humidity at 47 m. {#tbl-le-ratio}

Below 0 °C the ratio is 2.8, above 20 °C 1.03. The gap-filled annual `LE` is 27 % (2016) and 18 %
(2017) higher with the LI-7500.

The likely cause lies in the LI-7200, not in the open-path analyser. In the tube and cell of an
enclosed-path analyser, water vapour adsorbs on the walls, which damps the H2O fluctuations more the
higher the humidity. The `IRGA72` runs correct for this (Fratini et al. 2012), but such corrections
often fall short above about 90 % relative humidity. Self-heating of the open-path analyser would
bias its flux the other way. In humid and cold conditions, the LI-7500 `LE` may therefore be closer
to the true flux than the LI-7200 `LE`.

What this means for the data:

- The `LE` and `ET` of the LI-7200 (FP2026.1, and FP2026.2 from 2016) may be too low in humid and
  cold conditions.
- In the merged record of FP2026.2, the step in `LE` and `ET` at 1 January 2016 is partly
  instrumental. The gap-filled `ET` averages about 750 mm per year in 2004-2015 (LI-7500) and about
  610 mm in 2016-2025 (LI-7200). Do not read this difference as a change of the ecosystem.
- `H` comes from the same sonic anemometer for both analysers and is not affected: the two agree
  to within 2 % in 2016 and 2017.

Not yet resolved. The planned check compares the energy balance closure, `H + LE` against net
radiation minus the soil heat flux, of both analysers by humidity class: the analyser that closes
better at high humidity has the more realistic `LE`.

## USTAR thresholds lower than those of FLUXNET

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

This dataset does not use the FLUXNET thresholds. Both releases filter `NEE`, of both analysers,
at three constant thresholds: 0.272 (`CUT_16`), 0.304 (`CUT_50`) and 0.340 m s^-1^ (`CUT_84`). For
each scenario the higher of two detections is used, one on the LI-7200 data of 2016-2024 and one
on the LI-7500 data of 2005-2017 and 2019. These thresholds are kept on purpose, although the FLUXNET
thresholds of CH-LAE are much higher from 2016 on. See [Level-3.3](L3.3.md).

![USTAR thresholds detected by FLUXNET, based on data 2004-2023, from the file `FLX_CH-Lae_FLUXNET2015_AUXNEE_2004-2023_1-3.csv`.](images/USTAR_thresholds_from_FLUXNET_NEE_VUT_2004-2023.png){#fig-ustar-fluxnet1}

::: {.callout-tip title="Notebook"}

[Sonic anemometer data](notebooks/90_OVERVIEW/Sonic_Anemometer.html)

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
