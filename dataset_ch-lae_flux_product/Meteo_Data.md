# Meteo Data

## Timeshift checks

I did some timeshift checks to validate whether the maximum of measured short-wave incoming radiation at a given timestamp matches the location of the maximum potential radiation. It seems the variable `SW_IN_T1_47_1_gfXGB`

I tested the resampling output in the `diive` meteoscreening notebook. I resampled the original 1M data to 30M for the raw data variable with name `SW_IN_T1_47_1` in the database at timestamp `2022-08-01 09:30:00`, the value was `654.801507`. This time range corresponds to the values between `2022-08-01 09:01:00` and `2022-08-01 09:30:00` in the original 1M raw data files. I calculated the average from the original 1M raw data files manually and got `654.8015067`. This means there is no timeshift due to resampling.

I then ran the meteoscreening notebook again, but this time I also included the nighttime-offset correction (corrects for values below zero, which also changes values during daytime). The value was `665.219439`, corrected for an approx. -10 offset because of sub-zero nighttime values. The same value was also downloaded from the database. After all different data sources for `SW_IN` were merged, the value was still the same. After the merging of all `SW_IN` variables, the nighttime offset correction is run again, this time on all merged data instead of the individual data sources. After this second offset correction, the value changed to `664.929319`. Since the value became slightly lower, this means that the offset was positive (above zero during nighttime) and the respective positive offset value was subtracted. All data were then stored to a parquet file.

During gap-filling of `SW_IN_T1_47_1` data are loaded from the parquet file. During this loading, the timestamp is converted to `TIMESTAMP_MIDDLE`. The value before gap-filling and after loading all data from the file at the corresponding middle timestamp `2022-08-01 09:15:00` was `664.929319`, so up to here everything is correct. I originally assumed that an error could occur here because of the 15MIN shift of the timestamp. After gap-filling the value was still the same. After the gap-filling of other meteo variables and subsequent merging with flux data the value also remained the same (notebook 22.3). As an additional check, I manually calculated the air temperature value at `9:15` directly from 1M raw data between `09:01` and `09:30`, and the check was OK, values were identical.



`

:::{figure-md} plot-phaseshiftfft-16-25
![](images/CH-LAE_2016-2024_phase_shift_fft_SWINvsSWINPOT.png)

Time shift detection in shortwave radiation (2016–2025) using FFT phase analysis. (Top) Daily shifts (teal) with a 15-day rolling median (red) highlight a sensor lag emerging in 2022. (Middle) Global distribution shows a median offset of +1.93 min and strong phase alignment. (Bottom) Monthly boxplots indicate seasonal stability..
:::