# Soil heat flux at the forest floor

Half-hourly soil heat flux from the three Hukseflux HFP01 plates of the `FF1` forest-floor
station at CH-LAE, 2004-2025. The file is `11_METEO_G_FF1_2004-2025` (parquet and CSV):
**373,728 records** on a continuous 30-minute middle-timestamp index (named `TIMESTAMP_MIDDLE`
in the file) in local time (UTC+1, no daylight saving), from 2004-09-07 00:15 to
2025-12-31 23:45. Values are in **W m^-2^**, and **positive means heat moving down into the
soil**. The index begins with the plate record rather than on 1 January, because there is no
soil heat flux at this plot before September 2004.

Method, evidence and checks:

- [`11_METEO_G_FF1`](notebooks/10_METEO/30_PRODUCTS/11_METEO_G_FF1_2004-2025.html) — builds the
  product: it separates the acquisition changes from the archive's field renames, tests the
  declared depth, derives the two-term scale correction and measures what the correction leaves
  behind.
- The screening notebooks of the two plates that survive the 2021 rebuild:
  [plate 1](notebooks/10_METEO/20_SCREENING/G/G_FF1_0.05_1_2021-2025.html) and
  [plate 2](notebooks/10_METEO/20_SCREENING/G/G_FF1_0.05_2_2021-2025.html), which apply each
  plate's absolute limits to the raw record before this product reads it.
- [`10_METEO_TS_FF1`](notebooks/10_METEO/30_PRODUCTS/10_METEO_TS_FF1_2004-2025.html) and
  [`09_METEO_SWC_FF1`](notebooks/10_METEO/30_PRODUCTS/09_METEO_SWC_FF1_2004-2025.html) — the
  soil temperature and soil water content of the same profile. They supply the depth test and
  the storage-term estimate, and neither contributes a value to this product.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the chain.

::: {.callout-important title="Which column to use"}

The record spans three acquisition setups, and **their boundaries are not the dates on which the
archive renamed the fields**. The measurement changes at the March/April 2012 reconfiguration of
the forest-floor logger and at the March 2021 logger-box rebuild; the field names change at the
end of 2011 and at the 2021 rebuild. The 2021 rebuild is the one date at which the two
coincide.

- Inside one setup, use `G_FF1_0.05_1`, `_2` or `_3`, which is what each plate recorded.
- Across the 2012 or the 2021 boundary, use `G_FF1_0.05_HOMOGENIZED`, but read *The reconciled
  column* below first: it averages **two** plates after putting each non-reference setup onto
  the modern setup's scale and zero point, and it is a derived estimate rather than a
  measurement.
- **Exclude source flag `4`** from anything you compute. It marks 519 records of the 2012
  reconfiguration itself, which sit on neither setup's scale.

**Nothing in this product is gap-filled**, and a missing record is `NaN`, never `0`: for a
signed flux, `0` means that no heat crossed the plate. **The heat stored in the soil above the
plates is not added either**, so an energy-balance closure computed from these columns is a
closure at 0.05 m rather than at the surface.

:::

## Columns

Eight columns: a value and a source flag for each of the three plates, grouped so that a number
and its provenance stay adjacent, then the reconciled column and its composition flag. `<n>` is
one of `1`, `2`, `3`.

: Columns of `11_METEO_G_FF1_2004-2025`. {#tbl-g-cols}

| column | unit | description |
|---|---|---|
| `G_FF1_0.05_<n>` | W m^-2^ | Soil heat flux as the plate recorded it, screened. No scale correction is applied to these columns. |
| `FLAG_G_FF1_0.05_<n>_SOURCE` | - | Which acquisition setup produced the value. |
| `G_FF1_0.05_HOMOGENIZED` | W m^-2^ | The mean of plates `1` and `2` after each has been put onto the modern setup's scale and zero point. A derived estimate. |
| `FLAG_G_FF1_0.05_HOMOGENIZED_NPLATES` | - | How many of those two plates went into the mean: `0`, `1` or `2`. |

A plate holds a value exactly where its source flag is greater than `0`, and the reconciled
column holds one exactly where `NPLATES` is greater than `0`.

### `FLAG_G_FF1_0.05_<n>_SOURCE`

The codes name the **acquisition state**, not the field name the record is filed under. Codes
`1`, `2` and `3` are measurements; code `4` is a measurement that belongs to no setup, and code
`0` is no measurement.

: Source codes and their record counts per plate. {#tbl-g-source}

| code | acquisition setup | plate 1 | plate 2 | plate 3 |
|---|---|---|---|---|
| 0 | no measurement: a gap, or after this plate was discarded | 16,418 | 21,571 | 99,069 |
| 1 | original forest-floor acquisition, screened with the MeteoScreeningTool | 120,058 | 116,149 | 120,055 |
| 2 | the same station after the 2012 reconfiguration, still MeteoScreeningTool | 154,604 | 152,837 | 154,604 |
| 3 | after the March 2021 logger-box rebuild, screened with diive | 82,648 | 82,652 | 0 |
| 4 | the 2012 reconfiguration itself: recorded, but on neither setup's scale | 0 | 519 | 0 |

Code `1` runs from the start of the record to 2012-03-22 08:45. Code `2` begins at
2012-04-12 13:45 and runs to 2021-03-24 09:45. Code `3` begins at 2021-03-26 15:15. Plate 3 has
no code `3` at all, because it was discarded at the rebuild. Its flag reads `0` from then on,
which means that there was no instrument rather than that data are missing.

### `FLAG_G_FF1_0.05_HOMOGENIZED_NPLATES`

: How many plates stand behind each record of the reconciled column. {#tbl-g-nplates}

| code | meaning | records | share |
|---|---|---|---|
| 0 | neither contributing plate had a usable value | 16,414 | 4.4 % |
| 1 | one of the two: the other has a gap, or its record belongs to the 2012 reconfiguration | 5,680 | 1.5 % |
| 2 | both plates | 351,634 | 94.1 % |

The count never reaches `3`. Plate 3 is excluded from this column throughout the record, not
only after the rebuild, for the reason given under *The reconciled column*.

## Coverage

: Coverage and range of each exported column over the full 2004-2025 index. {#tbl-g-cov}

| column | coverage | range | mean | sd |
|---|---|---|---|---|
| `G_FF1_0.05_1` | 95.6 % | −90.7 to 84.1 | −1.33 | 5.99 |
| `G_FF1_0.05_2` | 94.2 % | −84.5 to 129.3 | −1.26 | 5.78 |
| `G_FF1_0.05_3` | 73.5 % | −65.9 to 100.6 | −5.03 | 9.93 |
| `G_FF1_0.05_HOMOGENIZED` | 95.6 % | −80.6 to 45.6 | −0.37 | 5.09 |

Plate 3 has the lowest coverage because it has no instrument after March 2021, and its mean sits
furthest from zero because its zero point drifted; both are discussed below. The plates
otherwise fail together, because they share a logger, a power supply and a data bus. The three longest
interruptions are station outages in which no plate measured at all: **92.9 days from
10 March 2009**, **82.9 days from 6 March 2010** and **62.9 days from 18 May 2007**. Counted
across the three plate columns, 31 gaps exceed five days. The forest-floor logger of the early
era ran on a battery, so a flat battery or a slipped fuse takes the whole station out at once.

***

## Three setups, two renames

This is the part of the record a reader is most likely to misread, because the archive's
bookkeeping and the station's history do not line up.

: What the archive does, and when. {#tbl-g-renames}

| event | when |
|---|---|
| `G_FF1_0.05_*` becomes `G_FF1_0.025_*`, at half the declared depth | 2011-12-31 23:45 |
| `G_FF1_0.025_*` becomes `G_FF1_0.05_*` again | 2021-03-26 |

: What the measurement does, and when. This is what the source flag names. {#tbl-g-setups}

| setup | flag | period | plates | screening |
|---|---|---|---|---|
| original forest-floor acquisition | 1 | 2004-09-07 to 2012-03-22 08:45 | 3 | MeteoScreeningTool |
| reconfigured acquisition | 2 | 2012-04-12 13:45 to 2021-03-24 09:45 | 3 | MeteoScreeningTool |
| after the logger-box rebuild | 3 | from 2021-03-26 15:15 | 2 | diive |

The end-of-2011 rename left the measurement alone: the values run through the join without a
step, and the notebook's seam test shows it. The measurement changed **102 days later**, when
the forest-floor logger was reconfigured over several visits in March and April 2012 and a new
program was uploaded with corrected multipliers and offset. The source flag follows the second
of those two dates, because it is the one that moved the values, and @tbl-g-renames is there for
anyone who needs to recover the field name a given record was filed under.

Between the two, plate 2 recorded 519 half-hours at daily means of +19.3 to +34.7 W m^-2^, which
is not soil heat flux at 5 cm. Those records are exported with their values intact, because they
are real readings of a station in a known state, and they carry flag `4` so that they can be
excluded in one filter. They take no part in any fit and never reach the reconciled column.

The 2021 boundary is simpler: the pre-rebuild record ends on 2021-03-24 09:45 and the diive
record begins on 2021-03-26 15:15. The 2 days and 5.5 hours between them are the rebuild itself,
and they are left as a gap.

## The declared depth, and the 2012 change

The archive declares these plates at 0.025 m between 2012 and 2021, which would mean they were
dug up and reburied at half the depth. A daily temperature wave weakens and arrives later the
deeper it travels, so a plate that really moved to 0.025 m should show a daily swing about
1.28 times larger and a peak about 0.95 h earlier. Neither happened. Across the two setups the
mean amplitude ratio is **0.48**, so the daily swing fell instead of growing, and the peak moved
**2.8 h later** instead of earlier. A change of depth can produce neither sign, so the 0.025 m
label has no support in the data and the product treats the plates as sitting at 0.05 m
throughout. What did change in 2012 is not identified: the maintenance record's candidate is the
corrected multipliers in the new logger program, and a plate disturbed while the wiring was
being redone is not ruled out.

Two further questions about the same station have clearer answers. **The sign convention held
across both boundaries**: every plate in every setup reads higher in the
afternoon than before dawn, by 1.1 to 11.1 W m^-2^, which is the direction heat actually moves,
so no plate was rewired backwards. And **25 June 2015, when the forest-floor rewiring stepped
soil water content by about 3.9 % VWC**, left no measurable trace here: the change in each
plate's spread across that date stays inside the band of what late June ordinarily does. The
null behind that verdict holds only twelve to seventeen years, and the question is one-sided,
since a rewiring would raise the spread rather than lower it, so the date is unremarkable rather
than cleared.

***

## The reconciled column

`G_FF1_0.05_HOMOGENIZED` exists so that an analysis can cross the 2012 and 2021 boundaries. It
is the mean of plates 1 and 2 after each of their non-reference setups has been put onto the
scale **and** the zero point of the diive setup, which serves as the reference because it is the
modern one, is still running, and its own annual means sit within a few tenths of a W m^-2^ of
zero.

The correction has two terms, applied in this order.

**A multiplicative gain per calendar month**, fitted on the within-month spread, puts the
amplitudes of the three setups onto one scale. The setups differ strongly here: the original
acquisition's within-month spread is 1.3 to 1.9 times the reference setup's and the reconfigured
acquisition's is about 40 % of it, so the gains run from 0.37 to 1.02 for the first and from
1.50 to 3.05 for the second.

**One additive constant per plate per setup**, fitted afterwards on the season-matched level of
the gained series, puts the zero point where physics requires it. Over a full year the soil ends
up near the temperature it started at, so a soil heat flux record at a few centimetres must
average near zero. The reconfigured and the diive setups meet that constraint on their own, to a
few tenths of a W m^-2^, while the original acquisition sits 3.3 to 3.6 W m^-2^ below the
reference at both plates. The constants that remove what is left are −1.28 and −1.66 W m^-2^ for
the original acquisition and +0.13 and +1.17 W m^-2^ for the reconfigured one. They are smaller
than the level differences above because the gain runs first, and multiplying a series whose
mean is not zero moves that mean as well.

Both terms are fitted on climatology alone. No service measures soil heat flux at this plot, the
setups do not overlap by a single half-hour, and all three plates change together at both
boundaries, so nothing independent anchors either term. The one exception is the near-zero
annual mean, which pins the additive term to something outside the record; the gain has no such
anchor.

**What the correction leaves.** The season-matched level of the reconciled column steps by **+0.71 W m^-2^ at
the 2012 boundary and −0.03 W m^-2^ at the 2021 boundary**, against the same statistic computed
at 33 dates well inside a single setup, where it moves by 0.57 W m^-2^ in the median and up to
1.91 W m^-2^. Both boundaries are therefore inside what this level does when nothing happens.
Read the size of that null before reading the result as zero: a step smaller than 1.91 W m^-2^
is a step this test cannot see rather than a step that is not there. With the gain alone the
2012 boundary failed the same check, which is why the additive term exists.

## The storage term above the plates

A plate at 0.05 m measures the heat crossing that depth. The soil above it also stores heat and
releases it again, and the plate sees none of that. This product exports the plate flux, so the
missing term is estimated rather than added, using soil temperature and soil water content at
0.05 m from products `10` and `09` together with a literature dry heat capacity, since bulk
density is not measured at this site. The notebook reports the estimate at that value and at
30 % above and below it, so the range is visible rather than one number that looks more precise
than it is.

In the reference setup the term has a spread of **2.36 W m^-2^ against 5.09 W m^-2^ for the
measured flux, about 46 %**. It is much larger in the two earlier setups — 2.06 times the
measured flux in the reconfigured setup and 3.44 times in the original one — but those ratios
compare different instruments on both sides, because the plates' own spread and the temperature
reference's diurnal amplitude both change at the setup boundaries. Quote the row of the setup
you are working in rather than an average of the three. The term averages near zero over a long
record, so it is a correction to the daily and seasonal course rather than to the level.

Adding the term properly would need a measured bulk density and a temperature above the plate,
and this site has neither.

## Known limitations

- **The measured columns are exported exactly as recorded, so they step at the setup
  boundaries.** The correction lives only in `G_FF1_0.05_HOMOGENIZED`. A mean or a trend taken
  across 2012 or 2021 from a plate column mixes three scales and three zero points.
- **The gain carries an unknown amount of climate.** Refitted on half the years of a setup and
  scored on the other half, the monthly gains miss by up to 125 %, worst in winter, and within
  one setup they vary by up to a factor of two across the calendar. An instrument gain does not
  know what month it is, so part of what these factors remove is the difference between the
  years the setups cover rather than between their electronics. The per-month form is kept
  because a single flat gain would match each month less closely and the notebook has not
  measured which of the two errors is smaller. The additive constants behave the opposite way:
  held out the same way, they land within 0.25 W m^-2^ of the reference level, which is what a
  property of an instrument should do.
- **A constant cannot follow a zero point that moves, and one is moving.** After the correction,
  the annual means of the corrected setups still drift by up to 0.42 W m^-2^ per year, and the
  reconciled column's annual means over the original acquisition run −1.78 to +1.14 W m^-2^ with
  a slope of −0.38 W m^-2^ per year. An analysis of interannual variability in the early years is
  reading a real signal plus a residual drift, and this product cannot separate them. A per-year
  offset was considered and rejected, because it would force every year's mean onto the reference
  and erase whatever interannual signal the record holds.
- **Plate 3 is corrected by neither term and its zero point walks furthest.** It never reaches
  the reference setup, so no gain and no offset can be fitted for it, and it is exported exactly
  as measured. Its annual means walk monotonically from −6.5 W m^-2^ in 2005 to −20.3 W m^-2^ in
  2011, a trend of −1.76 W m^-2^ per year, which is a plate or its wiring degrading rather than a
  soil storing more heat every year. Do not use this column across the original acquisition. It
  is not in the reconciled column, so none of this reaches anything derived.
- **The plates are not repeat measurements.** They sit metres apart beneath a deciduous canopy,
  so when the leaves are off a patch of sunlight can fall on one and not on another and one plate
  then reads several times the other. Their disagreement describes where the light fell; it is
  information rather than error.
- **Nothing is gap-filled.** There is no soil heat flux reference near this plot to fill from,
  and the gaps are dead loggers, a flat battery and a rebuild rather than weather. Interpolating
  a daily cycle across a three-month outage would produce a record that is smooth, plausible and
  invented, and an energy-balance closure would accept it without complaint.
- **The pre-2021 record was screened once, with the deprecated MeteoScreeningTool, and never
  re-screened.** The two screening notebooks cover the current plates only. Over the records the
  raw 10-minute stream and the screened record share, the two are identical, so that screening
  altered no value there. A plate that stopped responding while still reporting plausible numbers
  would survive it, and the comparison between plates is the only thing that would reveal such a
  failure.
- **The two current plates were screened with different absolute limits**, −20 to 40 W m^-2^ for
  plate 1 and −25 to 999 W m^-2^ for plate 2. Neither limit was ever reached, so no value was
  removed by one, and the threefold difference between the two plates' maxima is a property of
  the plates rather than of the screening. The asymmetry still matters for a future record,
  because the gains are fitted on the within-month spread and a removed sunfleck lowers a spread
  exactly as a genuinely smaller flux would.
- **Sub-daily timestamps in August 2012 carry the same uncertainty as the tower variables.** A
  logger clock error that month is corrected in the tower products. These plates hang off the
  forest-floor logger, and whether it shared the fault is not recorded. Soil heat flux does have
  a daily cycle that could be aligned against a reference, but only against a clock this station
  does not share, so nothing is applied.
- **The site record before 2011 is invisible to a date filter**, having been pasted into the
  maintenance system as a single entry, and 2004 and 2005 have no site record at all. The product
  notebook parses that entry separately; statements about the first years still rest on thinner
  evidence than later ones.
