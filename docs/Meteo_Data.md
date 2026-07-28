# Meteo Data

TODO IN PROGRESS

## Meteo products (notebooks `01`-`10`)

Ten notebooks turn the screened tower and soil measurements into one file per variable, written as parquet and CSV. Each file holds its value columns plus a provenance flag saying, half hour by half hour, whether the number was measured, corrected, reconstructed or modelled.

Two conventions apply to every product.

**Timestamps are `TIMESTAMP_MID`, local time (UTC+1), on a continuous 30-minute index with no daylight saving.** The label sits in the middle of the averaging period, so `09:15` covers 09:00 to 09:30.

**The provenance flag distinguishes a measurement from an estimate and should be applied before analysis.** `PA` and `LW_IN` are the only products without one, as neither is gap-filled; their gaps are retained.

: Meteo variables currently available. Coverage is the share of that file's own period carrying a value; flag columns are defined at every record. `<d>` is the depth in metres. {#tbl-meteo-vars}

| variable | unit | period | coverage | provenance flag |
|---|---|---|---|---|
| `SW_IN_T1_47_1_gfXG` | W m^-2^ | 2004-2025 | 100 % | `ISFILLED` |
| `TA_T1_47_1_gfXG` | °C | 2004-2025 | 100 % | `ISFILLED` + `SOURCE` |
| `TA_T1_47_1_HOMOGENIZED_gfXG` | °C | 2004-2025 | 100 % | `ISFILLED` + `SOURCE` |
| `PPFD_IN_T1_47_1_gfXG` | µmol m^-2^ s^-1^ | 2004-2025 | 100 % | `ISFILLED` |
| `RH_T1_47_1` | % | 2004-2025 | 100 % | `MISSING` |
| `PA_T1_47_1` | kPa | 2005-2025 | 98.9 % | none, gaps left in |
| `LW_IN_T1_47_1` | W m^-2^ | 2005-2025 | 98.6 % | none, gaps left in |
| `VPD_T1_47_1` | kPa | 2004-2025 | 100 % | `ISFILLED` |
| `PREC_TOT_T1_47_1` | mm (30 min) | 2004-2025 | 99.4 % | `SOURCE` + `ISFILLED` |
| `PREC_TOT_T1_47_1_HOMOGENIZED` | mm (30 min) | 2004-2025 | 99.4 % | `SOURCE` + `ISFILLED` |
| `SWC_FF1_<d>_1`, depths 0.05 / 0.1 / 0.2 / 0.3 / 0.5 m | % VWC | 2004-2025 | 26-96 % | `SOURCE` |
| `SWC_FF1_<d>_1_HOMOGENIZED`, the four depths above 0.5 m | % VWC | 2004-2025 | 81-96 % | `SOURCE` |
| `TS_FF1_<d>_HOMOGENIZED_GAPFILLED`, depths 0.05 / 0.1 / 0.15 / 0.2 / 0.3 / 0.5 / 0.6 m | °C | 2004-2025 | 27-94 % | `METHOD` + `SUSPECT` |
| eighteen individual `TS_FF1_*` / `TS_PRF_FF1_*` channels | °C | 2004-2025 | 21-72 % | none, raw as screened |

Flag names are given by their suffix; the full column is `FLAG_<variable>_<suffix>`.

### The derived columns

A `_HOMOGENIZED` or `_GAPFILLED` column sits beside the measured one rather than replacing it, so the measured record remains recoverable.

**`_HOMOGENIZED`** rescales an earlier era onto the level of the later one where a hardware change produced a step in the raw values. This makes the two eras comparable; it does not make either era more accurate, and the instrument's own biases are unaffected. `TA` carries one because its sensor and acquisition system were replaced together in January 2016, `PREC` one because its acquisition system changed in 2018, `SWC` one per depth because the soil profile was replaced in 2020.

**`_GAPFILLED`** indicates that a model produced some of the values. For `TS` the model is a regression on the remaining depths of the profile, and the `METHOD` flag identifies which values are measured and which are modelled.

### Known limitations

- **`TA` is not homogeneous across 21 January 2016.** The 47 m sensor and its acquisition system were replaced together on that date, and the measured column reads approximately 1.3 °C too cold before it. Use `TA_T1_47_1_HOMOGENIZED_gfXG` for anything crossing that date, and see [Air temperature at 47 m](Meteo_Data_TA.html) for the columns, flag codes and the limitations of the correction.
- **`PREC` provides two value columns serving different purposes.** Use the measured column for the recorded gauge amounts, and the `_HOMOGENIZED` column for analyses spanning mid-2018, where the acquisition change causes the earlier era to read approximately 25 % low.
- **`SWC` spans two sensor generations that changed in 2020 without an overlap period.** The resulting step is approximately +8 to +11 % VWC. The `_HOMOGENIZED` columns remove it on the basis of climatology rather than a measured offset. No such column is provided at 0.5 m, which has a single era.
- **`TS` diurnal and seasonal amplitudes are not comparable across April 2020.** The earlier sensors were more closely coupled to the surface than the present ones at the same nominal depth, so the amplitude changes with the hardware. Levels are reconciled between eras; amplitudes are not.
- **`TS` records between January 2009 and May 2012 carry the `SUSPECT` flag.** The three early channels differ from one another by 1.5 to 3.5 K over this period, and the available evidence cannot establish which is in error. Filter on the flag before using these years quantitatively.
- **`TS` values are stored on a 0.1 K grid.** At 0.5 and 0.6 m the median summer daily amplitude equals one grid step, so an apparent diurnal cycle at these depths reflects quantisation rather than soil temperature.
- **Soil depths are not replicates.** They share a logger, power supply and bus, and therefore fail together, but they do not measure the same soil volume. Differences between depths are informative.

### How they are built

Every product pulls the quality-screened half-hourly record from the database, joins the older `mst` screening to the newer `diive` one with `combine_first`, converts timestamps, applies the site's shared 2012 repairs where the variable sat on that logger, and writes out after a set of checks. Independent references do the validation and, where a product is filled, much of the filling: MeteoSwiss Lägern 2.5 km away, NABEL at 49 m on the same tower until 2018, the MeteoSwiss gauge at Ehrendingen for rain, and for `PREC` alone every MeteoSwiss station within 21 km. The soil products have no external reference and are checked against the other depths of their own profile instead.

Each notebook documents its own decisions and the evidence behind them: [`SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2025.html), [`TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2025.html), [`PPFD_IN`](notebooks/10_METEO/30_PRODUCTS/03_METEO_PPFD_IN_2004-2025.html), [`RH`](notebooks/10_METEO/30_PRODUCTS/04_METEO_RH_2004-2025.html), [`PA`](notebooks/10_METEO/30_PRODUCTS/05_METEO_PA_2004-2025.html), [`LW_IN`](notebooks/10_METEO/30_PRODUCTS/06_METEO_LW_IN_2005-2025.html), [`VPD`](notebooks/10_METEO/30_PRODUCTS/07_METEO_VPD_2004-2025.html), [`PREC`](notebooks/10_METEO/30_PRODUCTS/08_METEO_PREC_2004-2025.html), [`SWC`](notebooks/10_METEO/30_PRODUCTS/09_METEO_SWC_FF1_2004-2025.html), [`TS`](notebooks/10_METEO/30_PRODUCTS/10_METEO_TS_FF1_2004-2025.html).

## Timeshift checks

### Summary
I checked for potential time shifts (wrong timestamps) by comparing the maximum of measured short-wave incoming radiation (SW_IN​) with the maximum potential radiation on clear-sky days (filtered for clear days, 70% of potential, to remove cloudy noise). The results show a small time lag in the `SW_IN_T1_47_1_gfXGB` variable starting in 2022, the same year the `diive` meteoscreening notebooks were deployed. To isolate the source of this offset, I performed numerous diagnostic tests on the processing steps. The extensive testing did not reveal any processing error or bug; all output values were correct.
### Details
**No time shift due to resampling.** I tested the resampling output in the `diive` meteoscreening notebook, which downloads data from the database. I resampled the original 1min data that is stored in the database to 30min for the raw data variable (with name `SW_IN_T1_47_1` in the database). At timestamp `2022-08-01 09:30:00`, the value was `654.801507`. This time range corresponds to the values between `2022-08-01 09:01:00` and `2022-08-01 09:30:00` in the original 1min raw data files. I calculated the average from the original 1min raw data files manually and got `654.8015067`. This means there is no timeshift due to resampling.

**Reproduce database value at timestamp.** I then ran the meteoscreening notebook again, but this time I also included the nighttime-offset correction (corrects for values below zero, which also changes values during daytime). The value was `665.219439`, corrected for an approx. -10 offset because of sub-zero nighttime values. The same value was also confirmed for quality-screened and nighttime-offset-corrected data downloaded from the database. 

**No error during merging.** After all different data sources for `SW_IN` were merged, the value was still the same (no error due to merging). After the merging of all `SW_IN` variables, the nighttime offset correction is run again, this time on all merged data instead of the individual data sources. After this second offset correction, the value changed to `664.929319`. Since the value became slightly lower, this means that the offset was positive (above zero during nighttime) and the respective positive offset value was subtracted. All data were then stored to a parquet file.

**No error due to middle timestamp.** During gap-filling of `SW_IN_T1_47_1` data are loaded from the parquet file. During this loading, the timestamp is converted to `TIMESTAMP_MIDDLE`. The value before gap-filling and after loading all data from the file at the corresponding middle timestamp `2022-08-01 09:15:00` (corresponding to the half-hour between 9:00 and 9:30) was `664.929319`, so up to here everything is correct. I originally assumed that an error could occur here because of the 15min shift of the middle timestamp compared to the typical timestamp that shows the end of the averaging period. 

**No error due to gap-filling.** After gap-filling `SW_IN`, the value was still the same (there was no gap in this location anyway so the value is not expected to change). After the gap-filling of other meteo variables and subsequent merging with flux data the value also remained the same (notebook 22.3). As an additional check, I manually calculated the **air temperature** value at `9:15` directly from original 1min raw data files between `09:01` and `09:30`, and the check was OK, values were identical.

**Identical results for FFT analysis.** Next I ran the FFT analysis directly using the original data file for Aug 2022, using the 1min raw data file. Then I downloaded data for Aug 2022 from the database and also ran the analysis. The results from both analyses were identical, meaning that the data in the database and in the original raw data files are the same. 

**Same results for file data and database data.** I then resampled the 1min data downloaded from the database to 30min, using the same functions as are used during the meteoscreening in `diive`, and I also created the middle timestamp for the resampled data. I then checked the value of `SW_IN_T1_47_1` at timestamp `2022-08-01 09:15`, it was `654.801507`, the same value as for the very first test described above (*No time shift due to resampling*). Running the FFT analysis on 1min raw data files or 1min data from the database yielded the same results, with a time shift median of 6.39MIN, similar to what can be seen in the figure below (@fig-phaseshiftfft-16-25) in 2022. All steps so far produced the correct results.

**Shift can be seen in original raw data files.** I checked if this offset in 2022 can also be seen in the 1min data instead of the 30min data when downloaded from the database. Above checks already confirmed that data in the database are the same as in the original raw data files. This test also showed an offset of 5.90MIN, similar to the previous test for 30MIN data. This means this shift can be confirmed for the original raw data. I also tested the FFT analysis for data Jul 2021, 1min raw data files vs 1min data from database. Both runs yielded the same result. Also the same result was achieved for 1min raw data files resampled to 30min vs 1min database data resampled to 30min.

I was not able to find any error in any of the processing steps and scripts.


![**Time shift detection in shortwave radiation** (2016–2024) using FFT phase analysis. The time shift wa calculated by comparing the phase angle of the fundamental 24-hour frequency component of measured vs potential radiation. Based on 30MIN data. (Top) Daily shifts (teal) with a 15-day rolling median (red) highlight a sensor lag emerging in 2022. (Middle) Global distribution shows a median offset of +1.93 min and strong phase alignment. (Bottom) Monthly boxplots indicate seasonal stability..](images/CH-LAE_2016-2024_phase_shift_fft_SWINvsSWINPOT.png){#fig-phaseshiftfft-16-25}

