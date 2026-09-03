# Instrumentation

The instruments that produced the measurements in this dataset, and the periods
over which each was in place. Sensor identities here come from three sources,
in order of authority for a given question:

- the **datalogger programs**, which name the channel, its sensor and its
  conversion constants, and are the only source that says how a raw signal became
  a value;
- the **GIN fieldbook** device columns (`Device Name`, `Device Model`), which name
  the physical unit and its serial number at a location;
- [Yearly Notes](Yearly_Notes.md), whose `Setup EC` table is the authority for the
  eddy covariance setup periods, sensor separations and flux-run configuration.

::: {.callout-warning title="Fieldbook dates are entry dates, not deployment dates"}

The GIN export records when an entry was written, which is not when a device was
installed. Entries dated **1 January 2016** (and 2003, 2006) are backdated
inventory imports made when GIN was introduced, so a device whose earliest entry
carries one of those dates was already at the site and its true installation date
is not in the export. Only entries describing an event — a replacement, a repair,
a device marked defective — date anything.

:::

## Eddy covariance system, 47 m

Two gas analysers were operated at this level, and the dataset is built per
analyser rather than per year.

| instrument | role | period |
|---|---|---|
| Gill HS-50 sonic anemometer | wind components, sonic temperature | 2004-present, orientation 209° |
| LI-COR LI-7500 (open path, `IRGA75`) | CO~2~ and H~2~O densities | 2004 until removal on 12 December 2017 |
| LI-COR LI-7200 (enclosed path, `IRGA72`) | CO~2~ and H~2~O mole fractions | from 11 January 2016 |

The two analysers ran in parallel from January 2016. The LI-7500 was removed from
the site on 12 December 2017 but continued to write empty values into the data
stream until it was taken out of it on 31 January 2018, which is why the setup
table lists it for two further periods with no flux run. `IRGA72` itself spans two
physical LI-7200 units, exchanged inside the long 2019 gap; the second has a
different column set in the raw stream. The analyser also moved on the boom in
2023, changing its separation from the sonic. All of this is dated per setup
period in [Yearly Notes](Yearly_Notes.md), which should be read there rather than
summarised.

The fieldbook records the enclosed-path system at this level as an **LI-7200RS
head** with an **LI-7550 analyser unit** and an **LI-7200-101 flow module**.

## Meteorological sensors, 47 m

These produce the tower series documented under
[Meteorological data](Meteo_Data.md).

| variable | instrument | period | source |
|---|---|---|---|
| `TA`, `RH` | Rotronic MP101A, read as a single-ended analog voltage (multiplier 0.1, offset 0) | until 21 January 2016 | CR10X logger program |
| `TA`, `RH` | Campbell Scientific CS215, on SDI-12 (multiplier 1) | from 21 January 2016 | CR1000 logger program |
| `SW_IN`, `SW_OUT`, `LW_IN`, `LW_OUT` | Kipp & Zonen CNR1, SN 020484, sensitivity 10.03 µV W^-1^ m^2^ (multiplier 99.7009, offset 0) applied to **all four** channels | 14 September 2005 until December 2021 | CR10X and CR1000 logger programs |
| `SW_IN`, `SW_OUT`, `LW_IN`, `LW_OUT` | Kipp & Zonen CNR4, SN 212965, sensitivities 13.89 (SW in), 14.38 (SW out), 10.85 (LW in), 11.33 (LW out) µV W^-1^ m^2^, **one per channel** | installed 14 December 2021 | fieldbook |
| `PPFD_IN` | Kipp & Zonen PAR LITE, SN 050590, sensitivity 5.65 µV µmol^-1^ m^2^ s (primary, incoming) | installed 8 January 2016 | fieldbook |
| `PPFD_OUT` | Kipp & Zonen PAR LITE, SN 050603, sensitivity 5.26 µV µmol^-1^ m^2^ s (secondary, outgoing) | installed 8 January 2016 | fieldbook |
| PAR, total and diffuse | Delta-T BF2 sunshine sensor, SN BF2116 | entries 2016-2024, active | fieldbook |
| PAR | Kipp & Zonen PQS-1, SN 110145 | at this level from July 2011, inactive in every later entry | fieldbook |
| wind speed | Vector Instruments A100LK cup anemometer, SN 16697, replacing a broken A100L | installed 8 January 2016 | fieldbook |
| — | Campbell Scientific CR1000 datalogger | from January 2016 (CR10X before) | fieldbook, logger programs |

The **8 January 2016** date covers three of these rows because they were one
visit: the boom was retracted that morning and the LI-7200 with its analyser and
flow-module box, the replacement cup anemometer, both Kipp & Zonen PAR sensors
and a new tower box were installed together. The LI-7200's first raw binary is
three days later, on 11 January 2016. A new reflected-PAR sensor had been fitted
once before, at the end of June or beginning of July 2008; that entry is a remark
added after the fact and dates the work only to within about a fortnight.

Two things about this table are worth stating plainly.

**The temperature and humidity sensor is identified from the logger programs
alone.** The fieldbook records **no** temperature or humidity device at the 47 m
level for the whole period of this dataset; the first such entry is a Campbell
HygroVUE10 in June 2026, after the record ends. The MP101A and CS215
identifications, and the January 2016 date at which they changed, rest on the
CR10X and CR1000 programs and on the step the data themselves show. See
[Air temperature](Meteo_Data_TA.md), where that step is quantified and corrected.

**The radiometer change is dated by the fieldbook, the calibration by the logger
programs.** The CNR1 has no device entry of its own — it predates GIN — but a
2008 entry recording a relay replacement for it on the tower's CR10X meteo logger
confirms it was in service then. The CNR4 was installed on 14 December 2021.
Neither instrument change moved the shortwave series measurably, which is
asserted rather than assumed — see
[Incoming shortwave radiation](Meteo_Data_SW_IN.md).

**One constant for four detectors.** A CNR1 head holds four sensors, and the
factory calibrates each one separately. The logger programs, however, convert all
four with a single factor, the one belonging to the pyranometer. So the longwave
channels, and the outgoing channels, were converted with a factor that is not
their own. The CNR4 that replaced it is converted with four separate
sensitivities, which is why the two instruments cannot be compared channel by
channel without allowing for that difference. Both outgoing products flag the
instrument era for this reason.

**Two dates are easily confused.** The CNR1 instruction first appears in the
logger program of **18 August 2005**, which measures all four channels. The
program of **14 September 2005** changed the relay, moving the outgoing channels
onto different differential inputs, and that is also the day the archive's record
begins. The period column above gives the record, not the program.

**The serial is not fully reconciled.** The logger program comments and this table
give the tower CNR1 as **SN 020484**. The fieldbook row recording the 14 December
2021 exchange names **CNR1_020522**, at a different location. It is most likely a
bookkeeping artefact in GIN rather than a second instrument, but nothing has
settled it.

::: {.callout-warning title="Unverified: 14 December 2021 to 7 January 2022"}

The CNR4 was installed on **14 December 2021**, and the installing entry notes
that the logger script still needed to be adapted to the new calibration
constants. The logger program was updated on **7 January 2022**, adding the four
CNR4 sensitivities and new raw-voltage variables.

The two dates are 24 days apart, and which conversion the logger applied in
between is not recorded anywhere. If the CNR4 was read through the CNR1's
multiplier, the values of that period are wrong by the ratio of the two
sensitivities.

Two products have since tested the window, and between them they bound the
problem without identifying the constant.
[Outgoing shortwave radiation](Meteo_Data_SW_OUT.md) compares the window against
the MeteoSwiss Lägern station and finds the levels **not** consistent with the old
constant still being in force, which argues against the worst case.
[Outgoing longwave radiation](Meteo_Data_LW_OUT.md) bounds any error there at
about 1.6 W m⁻², roughly 0.5 % of the reported value, because a conversion error
scales only the small net signal a pyrgeometer measures and not the large
Stefan-Boltzmann term added to it.

So the window is better understood than it was, and it is still flagged rather
than corrected in all four radiation products. Two things follow for anyone using
it. A correction, if one is ever derived, has to be applied to all four channels
at once, since they share the head and the constant. And the bound above is a
ceiling on the error rather than a demonstration that there is none.

:::

## Soil profile, forest floor (FF1)

The soil sensors were replaced as a set on **19 March 2020**, which is the single
most important date for the soil variables: it is a change of sensor generation
with no overlap, so the step across it cannot be calibrated away.

| variable | instrument | depths | period |
|---|---|---|---|
| soil water content | Decagon ECH2O **EC-20** | 0.05, 0.1, 0.2, 0.3 m | until 19 March 2020 |
| soil water content | METER **TEROS 12** | 0.05, 0.1, 0.2, 0.3, 0.5 m | from 19 March 2020 |
| water potential | Decagon **MPS-2** | 0.05, 0.1, 0.6 m | until 19 March 2020 for the shallow depths |
| water potential | METER **TEROS 21** | 0.2, 0.3, 0.5 m | from 19 March 2020 |
| soil temperature | Campbell **107** thermistor | 0.05 m | until March 2021 |
| soil temperature | Campbell **109** thermistor | 0.05 m | from 24 March 2021 |
| soil heat flux | **three** Hukseflux **HFP01** plates | 0.05 m | three until 24 March 2021, two after |

The soil heat flux row differs from the others in the table, because it describes
three sensors rather than one. The GIN device records list three HFP01 plates at
this location. One of them was discarded at the logger-box rebuild of 24 March
2021 and the two survivors were kept, which is why the product exports three plate
columns of which the third ends in 2021. The plates sit metres apart under a
deciduous canopy, so they are not repeat measurements of one thing: under leaf-off
sunflecks one can read several times another, and that disagreement describes
where the light fell.

The depth is what the archive declares rather than a surveyed figure. The field
names carry 0.05 m until the end of 2011, 0.025 m from 2012 to March 2021, and
0.05 m again afterwards. Whether the plates were ever reburied shallower is
tested in the product notebook from the size and timing of the daily cycle, and
the measurement matches neither a move nor an unchanged depth, so the question is
open. See [Soil heat flux](Meteo_Data_G.md).

The 0.5 m depth exists only in the TEROS 12 generation, which is why the
soil-water-content product carries a homogenised second column at four depths and
deliberately none at 0.5 m. A second profile, **FF2**, carries MPS-2 water
potential sensors at 0.05, 0.1, 0.15, 0.2 and 0.3 m. Coverage, flags and the
sensor-generation step are documented under
[Soil water content](Meteo_Data_SWC.md) and
[Soil temperature](Meteo_Data_TS.md).

The subcanopy station (`M1_2`) carries a **CS215** temperature and humidity
sensor, installed on 26 March 2021 to replace a Rotronic MP100, alongside an
Apogee SQ-521 and a LI-COR LI-190SA quantum sensor, an Apogee SN-500-SS net
radiometer and a W200P wind vane. Forest-floor acquisition is a CR1000 with an
AM16/32B multiplexer until March 2021 and an ARK-1124C from October 2021.

## Profile masts

A temperature, humidity and wind profile is operated on the tower and on
satellite masts at the site (`T1_17.5`, `T1_35`, `M2`, `M3`, `M4`). Its
temperature and humidity sensors are Rotronic units of several generations —
MP101, MP400H and MP402H transmitters with HygroClip S2, S3 and HC2-S3 probes,
with individual heads replaced repeatedly between 2015 and 2021 — and its wind
sensors are Gill WindSonics. **None of these profile sensors contributes to this
dataset**, which takes its meteorology from the 47 m level and the forest floor.
They are listed here only because published descriptions of the site sometimes
name them.

## Published descriptions that disagree

Three sensor identities given in the literature do not match the fieldbook or the
logger programs. They are recorded here so that a reader comparing this dataset
against those papers is not left to wonder which is right.

@shekhar_contrasting_2024 give the site's temperature and humidity sensor as a
**Rotronic HygroClip HC2-S3**. The fieldbook does hold HygroClip HC2-S3 units at
CH-LAE, but on the profile masts (`M3`, `M4`, `T1_35`), never at the 47 m level
that supplies this dataset, and the logger programs give the MP101A and CS215
above.

The same study gives soil moisture as a **Decagon ECH2O EC-5**. The string `EC-5`
does not occur anywhere in the fieldbook export; the CH-LAE profile is EC-20 and
then TEROS 12, as above. The study assigns EC-20 to the subalpine site it
compares against, so the two sites' sensors appear to have been transposed.

The same study assigns the **Delta-T BF2** radiation sensor, serial `BF2116`, to
the subalpine site. That serial is registered in the fieldbook at CH-LAE at the
47 m level.

None of this affects the values in either dataset; it affects only what a reader
concludes about which instrument produced them.

## References

::: {#refs}
:::
