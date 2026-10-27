# Soil heat flux at the forest floor

Half-hourly soil heat flux from the three Hukseflux HFP01 plates of the `FF1` forest-floor station
at CH-LAE, 2004-2025. The file is `11_METEO_G_FF1_2004-2025` (parquet and CSV): **373,728
records** on a continuous 30-minute index, `TIMESTAMP_MIDDLE` (middle of the half-hour), in local
time (UTC+01:00, no daylight saving), from 2004-09-07 00:15 to 2025-12-31 23:45. Values are in
**W m^-2^**, and **positive means heat moving down into the soil**. The index begins in September
2004 because the plate record begins then.

The series ends on 31 December 2025. It is part of [FP2026.1](Dataset_Versions.html) and of the
[merged meteo product](notebooks/10_METEO/30_PRODUCTS/99_METEO_MERGED_2004-2026.09.html), where it
is `NaN` from 1 January 2026; the extension to 30 September 2026 is in progress. Both carry the
reconciled column `G_FF1_0.05_HOMOGENIZED` and its `NPLATES` flag, not the three plate columns.

The [interactive dashboard](dashboards/METEO_G_dashboard.html) summarises the reconciled column
(coverage, provenance, seasonality, distributions, extremes and trends). The three plate columns
are shown in the notebook only.

Notebooks:

- [`11_METEO_G_FF1`](notebooks/10_METEO/30_PRODUCTS/11_METEO_G_FF1_2004-2025.html): builds the
  product. It separates the acquisition changes from the field renames in the database, tests the
  declared depth, derives the scale correction and measures what the correction leaves.
- The screening notebooks of the two plates still in use after the 2021 rebuild,
  [plate 1](notebooks/10_METEO/20_SCREENING/G/G_FF1_0.05_1_2021-2025.html) and
  [plate 2](notebooks/10_METEO/20_SCREENING/G/G_FF1_0.05_2_2021-2025.html), which apply each
  plate's absolute limits to the raw record.
- [`10_METEO_TS_FF1`](notebooks/10_METEO/30_PRODUCTS/10_METEO_TS_FF1_2004-2025.html) and
  [`09_METEO_SWC_FF1`](notebooks/10_METEO/30_PRODUCTS/09_METEO_SWC_FF1_2004-2025.html): soil
  temperature and soil water content of the same profile. They are used for the depth test and the
  storage-term estimate and contribute no values to this product.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html): where this product sits in the chain.

::: {.callout-important title="Which column to use"}

The record spans three acquisition setups. **Their boundaries are not the dates on which the
fields were renamed in the database.** The measurement changes at the March/April 2012
reconfiguration of the forest-floor logger and at the March 2021 logger-box rebuild. The field
names change at the end of 2011 and at the 2021 rebuild.

- Within one setup, use `G_FF1_0.05_1`, `_2` or `_3`, which is what each plate recorded.
- Across the 2012 or 2021 boundary, use `G_FF1_0.05_HOMOGENIZED`. Read *The reconciled column*
  first: it averages **two** plates after putting each earlier setup onto the scale and zero point
  of the current setup, and it is a derived estimate, not a measurement.
- **Exclude source flags `4` and `5`** from any calculation. Flag `4` marks 519 records of the 2012
  reconfiguration itself. Flag `5` marks 18,911 records in which a plate read with reversed sign.
  Neither is on the scale of any setup.

**Nothing is gap-filled.** A missing record is `NaN`, never `0`; for a signed flux, `0` means that
no heat crossed the plate. **Heat storage in the soil above the plates is not added**, so an
energy-balance closure computed from these columns is a closure at 0.05 m, not at the surface.

:::

## Columns

Eight columns: a value and a source flag for each of the three plates, then the reconciled column
and its plate-count flag. `<n>` is one of `1`, `2`, `3`.

: Columns of `11_METEO_G_FF1_2004-2025`. {#tbl-g-cols}

| column | unit | description |
|---|---|---|
| `G_FF1_0.05_<n>` | W m^-2^ | Soil heat flux as the plate recorded it, screened. No scale correction. |
| `FLAG_G_FF1_0.05_<n>_SOURCE` | - | Which acquisition setup produced the value. |
| `G_FF1_0.05_HOMOGENIZED` | W m^-2^ | The mean of plates `1` and `2`, each put onto the scale and zero point of the current setup. A derived estimate. |
| `FLAG_G_FF1_0.05_HOMOGENIZED_NPLATES` | - | How many of these two plates went into the mean: `0`, `1` or `2`. |

A plate holds a value exactly where its source flag is greater than `0`, and the reconciled column
holds one exactly where `NPLATES` is greater than `0`.

### `FLAG_G_FF1_0.05_<n>_SOURCE`

The codes name the **acquisition state**, not the field name under which the record is stored.
Codes `1`, `2` and `3` are measurements in a settled setup, codes `4` and `5` are measurements that
belong to no setup, and code `0` is no measurement.

: Source codes and their record counts per plate. {#tbl-g-source}

| code | acquisition setup | plate 1 | plate 2 | plate 3 |
|---|---|---|---|---|
| 0 | no measurement: a gap, or after this plate was removed | 16,418 | 21,571 | 99,069 |
| 1 | original forest-floor acquisition, screened with the MeteoScreeningTool | 115,738 | 101,558 | 120,055 |
| 2 | the same station after the 2012 reconfiguration, MeteoScreeningTool | 154,604 | 152,837 | 154,604 |
| 3 | after the March 2021 logger-box rebuild, screened with diive | 82,648 | 82,652 | 0 |
| 4 | the 2012 reconfiguration itself: recorded, but on neither setup's scale | 0 | 519 | 0 |
| 5 | the plate read with reversed sign | 4,320 | 14,591 | 0 |

Code `1` runs from the start of the record to 2012-03-22 08:45, code `2` from 2012-04-12 13:45 to
2021-03-24 09:45, and code `3` from 2021-03-26 15:15. Plate 3 was removed at the rebuild, so it has
no code `3`, and its flag is `0` from then on because there is no instrument.

Code `5` marks three periods, all in the original acquisition: plates 1 and 2 from December 2004
to February 2005, and plate 2 again from June to December 2011 (see *Plates with reversed sign*).

### `FLAG_G_FF1_0.05_HOMOGENIZED_NPLATES`

: How many plates stand behind each record of the reconciled column. {#tbl-g-nplates}

| code | meaning | records | share |
|---|---|---|---|
| 0 | neither contributing plate had a usable value | 20,734 | 5.5 % |
| 1 | one of the two: the other has a gap, or its record belongs to no setup | 15,951 | 4.3 % |
| 2 | both plates | 337,043 | 90.2 % |

The count never reaches `3`. Plate 3 is excluded from this column over the whole record (see *The
reconciled column*).

## Coverage

: Coverage and range of each exported column over the full 2004-2025 index. {#tbl-g-cov}

| column | coverage | range | mean | sd |
|---|---|---|---|---|
| `G_FF1_0.05_1` | 95.6 % | −90.7 to 84.1 | −1.33 | 5.99 |
| `G_FF1_0.05_2` | 94.2 % | −84.5 to 129.3 | −1.26 | 5.78 |
| `G_FF1_0.05_3` | 73.5 % | −65.9 to 100.6 | −5.03 | 9.93 |
| `G_FF1_0.05_HOMOGENIZED` | 94.5 % | −80.6 to 45.6 | −0.37 | 5.15 |

Plate 3 has the lowest coverage because it has no instrument after March 2021, and its mean is
furthest from zero because its zero point drifted. Otherwise the plates fail together, because
they share a logger, a power supply and a data bus. The three longest interruptions are station
outages in which no plate measured: **92.9 days from 10 March 2009**, **82.9 days from 6 March
2010** and **62.9 days from 18 May 2007**. Across the three plate columns, 31 gaps exceed five
days. In the early era the forest-floor logger ran on a battery, so a flat battery or a slipped
fuse stopped the whole station.

***

## Three setups, two renames

The field names in the database and the station's hardware history do not change on the same
dates.

: Field renames in the database. {#tbl-g-renames}

| event | when |
|---|---|
| `G_FF1_0.05_*` becomes `G_FF1_0.025_*`, at half the declared depth | 2011-12-31 23:45 |
| `G_FF1_0.025_*` becomes `G_FF1_0.05_*` again | 2021-03-26 |

: Acquisition setups. These are what the source flag names. {#tbl-g-setups}

| setup | flag | period | plates | screening |
|---|---|---|---|---|
| original forest-floor acquisition | 1 | 2004-09-07 to 2012-03-22 08:45 | 3 | MeteoScreeningTool |
| reconfigured acquisition | 2 | 2012-04-12 13:45 to 2021-03-24 09:45 | 3 | MeteoScreeningTool |
| after the logger-box rebuild | 3 | from 2021-03-26 15:15 | 2 | diive |

The values run through the end-of-2011 rename without a step. The measurement changed **102 days
later**, when the forest-floor logger was reconfigured over several visits in March and April 2012
and a new program with corrected multipliers and offset was uploaded. The source flag follows the
reconfiguration; @tbl-g-renames gives the field name under which a record was stored.

During the reconfiguration, plate 2 recorded 519 half-hours with daily means of +19.3 to
+34.7 W m^-2^, which is not soil heat flux at 5 cm. These records are exported with their values,
carry flag `4`, and are used in no fit and not in the reconciled column.

At the 2021 rebuild the earlier record ends on 2021-03-24 09:45 and the diive record begins on
2021-03-26 15:15. The 2 days and 5.5 hours in between are left as a gap.

## Plates with reversed sign

Three times in the original acquisition a plate reversed its sign and kept recording. The values
stay ordinary in size and keep a daily cycle, so limit tests pass them.

Heat moves into the soil around midday and out at night, so a plate's mean day must be higher at
midday than at night. The product checks this for each plate and calendar month separately.
Twelve plate-months fail, the weakest at −1.16 W m^-2^; the other 673 are all above
−0.34 W m^-2^.

: The three periods in which a plate read with reversed sign. All carry source flag `5`. {#tbl-g-reversed}

| plate | from | to | records | midday minus night |
|---|---|---|---|---|
| 1 | 2004-12 | 2005-02 | 4,320 | −2.35 to −6.85 W m^-2^ |
| 2 | 2004-12 | 2005-02 | 4,320 | −3.70 to −10.43 W m^-2^ |
| 2 | 2011-06 | 2011-12 | 10,271 | −1.16 to −6.17 W m^-2^ |

The check reads each plate on its own. In the winter of 2004/2005 two of the three plates were
reversed at the same time, so a comparison against the other plates would have marked plate 3,
the correct one, as the outlier.

The periods are whole calendar months. Plate 2 actually reverses within one half-hour, on
2011-06-16 between 09:15 and 09:45, when it steps by −17 W m^-2^ while plate 1 does not move; the
month of the change is excluded with the rest.

**The values are not negated.** Negated, these periods lie 5.0 to 10.8 W m^-2^ from the same
plate's readings in the same calendar months of the nearest unaffected years of the same setup.
Over July to December 2011, for example, plate 2 as measured is at −8.4 W m^-2^, close to plate 1
at −9.0; negated it would be +8.4, while the plate normally reads about −4.8. A swapped wire
negates cleanly; a wrong multiplier and offset in the logger program does not, and the maintenance
record has those being corrected in 2012. Removing the offset as well would require fitting the
plate to a neighbour without an independent reference. The records are therefore excluded from
every fit, every per-setup statistic and the reconciled column. As a result, the reconciled
column rests on plate 1 alone in the second half of 2011 and **has no value in the winter of
2004/2005**.

## The declared depth, and the 2012 change

The database declares the plates at 0.025 m between 2012 and 2021, which would mean they were
reburied at half the depth. A daily temperature wave weakens and is delayed with depth, so a plate
moved to 0.025 m should show a daily amplitude about 1.28 times larger and a peak about 0.95 h
earlier. Neither is seen. Across the two setups the mean amplitude ratio is **0.47** and the peak
moves **2.8 h later**. A change of depth cannot produce either sign, so the product treats the
plates as at 0.05 m throughout. The cause of the 2012 change is not identified. The maintenance
record points to the corrected multipliers in the new logger program; a plate disturbed while the
wiring was redone is not ruled out.

**The sign convention held across both boundaries.** With the reversed periods set aside, every
plate in every setup reads higher in the afternoon than before dawn, by 1.1 to 11.1 W m^-2^, so no
plate was rewired backwards at a boundary.

**The forest-floor rewiring of 25 June 2015**, which stepped soil water content by about
3.9 % VWC, left no measurable trace here: the change in each plate's spread across that date stays
within what late June ordinarily shows. The comparison rests on twelve to seventeen years and is
one-sided (a rewiring would raise the spread, not lower it), so the date is unremarkable rather
than cleared.

***

## The reconciled column

`G_FF1_0.05_HOMOGENIZED` allows an analysis to cross the 2012 and 2021 boundaries. It is the mean
of plates 1 and 2, after each of their earlier setups has been put onto the scale **and** the zero
point of the diive setup. The diive setup is the reference because it is current and its annual
means lie within a few tenths of a W m^-2^ of zero.

The correction has two terms, applied in this order.

1. **A multiplicative gain per calendar month**, fitted on the within-month spread, puts the
   amplitudes of the three setups onto one scale. The within-month spread of the original
   acquisition is 1.3 to 1.9 times that of the reference setup, and that of the reconfigured
   acquisition about 40 % of it. The gains run from 0.37 to 1.02 for the original and from 1.50 to
   3.05 for the reconfigured acquisition.
2. **One additive constant per plate and setup**, fitted afterwards on the season-matched level of
   the gained series, sets the zero point. Over a full year the soil returns to about the
   temperature it started at, so the flux at a few centimetres must average near zero. The
   reconfigured and diive setups meet this to a few tenths of a W m^-2^; the original acquisition is
   3.1 to 3.8 W m^-2^ below the reference at both plates. The constants are −1.48 and
   −1.67 W m^-2^ for the original and +0.13 and +1.17 W m^-2^ for the reconfigured acquisition.
   They are smaller than these level differences because the gain, applied first, also moves the
   mean.

Both terms are fitted on climatology alone. No service measures soil heat flux at this plot, the
setups do not overlap by a single half-hour, and all three plates change together at both
boundaries. Only the near-zero annual mean ties the additive term to something outside the
record; the gain has no such anchor.

**What remains.** The season-matched level of the reconciled column steps by **+0.47 W m^-2^ at
2012 and −0.03 W m^-2^ at 2021**. The same statistic at 33 dates inside a single setup moves by
0.46 W m^-2^ in the median and up to 1.89 W m^-2^. Both boundaries are therefore within the
ordinary variation, but a step smaller than 1.89 W m^-2^ cannot be detected by this test. With the
gain alone, the 2012 boundary failed the same check.

## The storage term above the plates

A plate at 0.05 m measures the heat crossing that depth. The soil above it stores and releases
heat that the plate does not see. This product exports the plate flux only. The storage term is
estimated in the notebook, not added, from soil temperature and soil water content at 0.05 m
(products `10` and `09`) and a literature value for the dry heat capacity, because bulk density is
not measured at this site. The notebook reports the estimate at that value and at 30 % above and
below it.

In the reference setup the storage term has a spread of **2.36 W m^-2^ against 5.09 W m^-2^ for
the measured flux, about 46 %**. In the earlier setups it is 2.06 times the measured flux
(reconfigured) and 3.44 times (original), but these ratios compare different instruments, because
the plates' own spread and the diurnal amplitude of the temperature reference both change at the
setup boundaries. Use the value for the setup you work in, not an average of the three. The term
averages near zero over a long record, so it changes the daily and seasonal course, not the level.
Adding it properly would require a measured bulk density and a temperature above the plate, and
neither is available at this site.

## Known limitations

- **The plate columns are exported as recorded and step at the setup boundaries.** The correction
  is only in `G_FF1_0.05_HOMOGENIZED`. A mean or trend across 2012 or 2021 from a plate column mixes
  three scales and three zero points.
- **Amplitudes are not comparable across 2011/2012 in any column.** At the 2012 acquisition change
  the median daily amplitude of plates `_1` and `_2` falls by a factor of three to four, from 8.4
  and 10.3 W m^-2^ in 2011 to 2.6 and 3.3 in 2012 and 1.2 and 1.8 in 2013. Plate `_3` does not
  follow: 15.7, 12.1 and 10.8 over the same years. The change did not affect the three plates
  equally, and the monthly gains do not repair it: the reconciled column's median daily amplitude
  is 4.8 in 2011, 5.7 in 2012, 3.4 in 2013 and 5.5 in 2014. Levels can be used with care, but do not
  use amplitudes, variances or trends through this period, and do not compare the early years with
  the later ones on any of these. The cause is not established. The daily-record panel of the
  [dashboard](dashboards/METEO_G_dashboard.html) shows the effect.
- **The gain includes an unknown amount of climate.** Refitted on half the years of a setup and
  tested on the other half, the monthly gains miss by up to 69 %, most in winter, and within one
  setup they vary by up to a factor of two across the year. An instrument gain does not depend on
  the month, so part of what the factors remove is the difference between the years each setup
  covers, not between the electronics. The monthly form is kept because a single gain would fit
  each month less closely, and which error is smaller has not been measured. The additive
  constants behave as an instrument property should: held out the same way, they land within
  0.42 W m^-2^ of the reference level.
- **A residual zero-point drift remains.** After correction, the annual means of the corrected
  setups still drift by up to 0.35 W m^-2^ per year. Over the original acquisition the reconciled
  column's annual means range from −1.07 to +0.96 W m^-2^, with a slope of −0.30 W m^-2^ per year.
  Interannual variability in the early years is a real signal plus this drift, and the product
  cannot separate them. A per-year offset was rejected, because it would force every year's mean
  onto the reference and remove any interannual signal.
- **Plate 3 is not corrected and its zero point drifts most.** It never reaches the reference
  setup, so no gain or offset can be fitted, and it is exported as measured. Its annual means fall
  steadily from −6.5 W m^-2^ in 2005 to −20.3 W m^-2^ in 2011, a trend of −1.76 W m^-2^ per year,
  which indicates a degrading plate or wiring, not a soil storing more heat each year. Do not use
  this column across the original acquisition. It is not part of the reconciled column.
- **Records with reversed sign are flagged, not repaired.** Plates 1 and 2 from December 2004 to
  February 2005, and plate 2 from June to December 2011, carry source flag `5`. They are exported
  with their values and excluded from every fit and from the reconciled column; filter the flag
  out. Do not negate them: the sign is only part of the fault (see *Plates with reversed sign*).
  The reconciled column has no value in the winter of 2004/2005, because both of its plates were
  affected. These three periods all fall in the first years, which is a further reason to treat
  the early record as less well characterised.
- **The plates are not replicates.** They are metres apart under a deciduous canopy. When the
  leaves are off, a patch of sunlight can fall on one plate and not another, which then reads
  several times higher. Differences between them describe where the light fell.
- **Nothing is gap-filled.** There is no soil heat flux reference near this plot to fill from, and
  the gaps are failed loggers, a flat battery and a rebuild, not weather.
- **The pre-2021 record was screened once, with the deprecated MeteoScreeningTool, and never
  re-screened.** The two screening notebooks cover the current plates only. Where the raw
  10-minute stream and the screened record overlap they are identical, so that screening changed no
  value there. A plate that stopped responding while still reporting plausible values would pass
  it; only the comparison between plates could reveal that.
- **The two current plates were screened with different absolute limits**: −20 to 40 W m^-2^ for
  plate 1 and −25 to 999 W m^-2^ for plate 2. Neither limit was reached, so no value was removed by
  them, and the threefold difference between the two plates' maxima is a property of the plates.
  The difference will matter for a future record, because the gains are fitted on the within-month
  spread, and a removed sunfleck lowers a spread just as a smaller flux would.
- **Sub-daily timestamps in August 2012 are uncertain.** A logger clock error that month is
  corrected in the tower products. These plates are on the forest-floor logger, and whether it had
  the same error is not recorded. The daily cycle could only be aligned against a clock this
  station does not share, so no shift is applied.
- **The site record before 2011 is not found by a date filter**, because it was pasted into the
  maintenance system as one entry, and there is no site record for 2004 and 2005. The product
  notebook parses that entry separately; statements about the first years still rest on less
  evidence than later ones.
