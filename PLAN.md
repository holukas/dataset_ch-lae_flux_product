# Dataset plan

Working document: what the CH-LAE flux product is to contain, what exists today,
and what is still missing. It is the place to look when picking up the work again.

It lives at the repository root rather than in `docs/` because Quarto renders
every `.md` under `docs/` onto the public website, and this file is internal.
When a section here settles it moves to the site — the variable inventory to
`docs/Variables.md`, the scope and coverage summary to `docs/Overview.md` — and
is deleted from this file so the two cannot drift apart.

Status vocabulary used throughout:

- **done** — exists, checked, and read by something downstream.
- **open** — planned, not started or not finished.
- **verify** — a fact this plan depends on that has not been established yet.
  Nothing marked `verify` may be quoted as settled in the published pages.


## 1. Releases

| release | period | gas analyser | state |
|---|---|---|---|
| `FP2026.1` | 2016-2025 | `IRGA72` (LI-7200, enclosed path) | open |
| `FP2026.2` | 2004-2025 | `IRGA75` (LI-7500, open path) + `IRGA72` | open |

`FP2026.2` supersedes `FP2026.1` and re-includes it in full. The two releases
differ in the flux record only; the meteorological product is built once over
2004-2025 and serves both.


## 2. Record boundaries

These are the periods the dataset can cover, and the reason each one starts and
stops. They bound every table below.

| record | period | note |
|---|---|---|
| `IRGA75` fluxes | 2004 - 12 Dec 2017, plus 17 Jan - 20 Mar 2019 | analyser removed Dec 2017; the 2019 window is the stand-in run `2019_3` |
| `IRGA72` fluxes | 11 Jan 2016 - 2025 | two physical LI-7200 units, exchanged inside the 2019 gap |
| tower meteorology, 47 m | 2004 - 2025 | `PA` and `LW_IN` start Sep 2005 with the CNR1 and the pressure sensor |
| soil profile FF1 | 2004 - 2025 | sensors replaced as a set on 19 Mar 2020, no overlap across the change |
| radiometer | CNR1 Sep 2005 - Dec 2021, CNR4 from 14 Dec 2021 | logger constants updated 7 Jan 2022, 24 days later |

Setup periods, their notes and the unusable windows are in `docs/Yearly_Notes.md`
and are not repeated here.


## 3. Meteorological variables

### 3.1 In the dataset

One product notebook per variable in `workflow/10_METEO/30_PRODUCTS/`, joined by
`99_METEO_MERGED_2004-2025.ipynb` and documented on a page under
`docs/Meteo_Data.md`.

| variable | series | period | notebook | page | state |
|---|---|---|---|---|---|
| `SW_IN` | incoming shortwave, 47 m | 2004-2025 | `01` | yes | done |
| `TA` | air temperature, 47 m | 2004-2025 | `02` | yes | done |
| `PPFD_IN` | photosynthetic photon flux density, 47 m | 2004-2025 | `03` | yes | done |
| `RH` | relative humidity, 47 m | 2004-2025 | `04` | yes | done |
| `PA` | air pressure, 47 m | 2005-2025 | `05` | yes | done |
| `LW_IN` | incoming longwave, 47 m | 2005-2025 | `06` | yes | done |
| `VPD` | vapour pressure deficit, 47 m | 2004-2025 | `07` | yes | done |
| `PREC` | precipitation | 2004-2025 | `08` | yes | done |
| `SWC` | soil water content, 5 depths | 2004-2025 | `09` | yes | done |
| `TS` | soil temperature, 7 depths | 2004-2025 | `10` | yes | done |

Six of these are re-formatted for EddyPro by
`40_EXPORTS/EDDYPRO_BIOMET_CH-LAE_2004-2025.ipynb` (`TA`, `RH`, `PA`, `SW_IN`,
`LW_IN`, `PPFD_IN`) and are the biomet input to the final flux runs.

### 3.2 To be added

The three variables below are the agreed next additions. Each needs the same
chain as an existing variable: screening notebooks per sensor and era in
`20_SCREENING/<VAR>/`, one product notebook in `30_PRODUCTS/`, an entry in the
`PRODUCTS` registry of `30_PRODUCTS/99`, and a page under `docs/Meteo_Data.md`.

| variable | measures | raw database field | state |
|---|---|---|---|
| `SW_OUT` | outgoing (reflected) shortwave, 47 m | `SW_OUT_T1_47_1` | open, field exists |
| `LW_OUT` | outgoing (emitted) longwave, 47 m | `LW_OUT_T1_47_1` | open, field exists |
| `G` | soil heat flux, forest floor | unknown | open, **verify** |

**Both outgoing radiation fields exist in `ch-lae_raw`.** Measurement `SW` holds
five fields (`SW_IN_BC_M1_2_1`, `SW_IN_NABEL_T1_49_1`, `SW_IN_T1_47_1`,
`SW_OUT_BC_M1_2_1`, `SW_OUT_T1_47_1`) and measurement `LW` holds four
(`LW_IN_BC_M1_2_1`, `LW_IN_T1_47_1`, `LW_OUT_BC_M1_2_1`, `LW_OUT_T1_47_1`), per
the field listings cached in the outputs of the `SW_IN` and `LW_IN` screening
notebooks. So the tower has a full four-component radiation record and a second
four-component set below canopy at the subcanopy station.

What the listing does **not** say is how far back each field reaches. The CR1000
update of 7 January 2022 introduced the CNR4 with four *new* raw-voltage
variables (`SW_VIN_T1_47_1`, `SW_VOUT_T1_47_1`, `LW_VIN_T1_47_1`,
`LW_VOUT_T1_47_1`), and `docs/Instrumentation.md` gives the CNR1 a single
sensitivity covering `SW_IN` and `LW_IN` only. **verify** the first date of
`SW_OUT_T1_47_1` and `LW_OUT_T1_47_1`: if the CNR1 outgoing channels were never
logged, both products are 2022-2025, and so are `ALB` and a four-component
`NETRAD`.

Note also that `ch-lae_processed` already carries `LW_IN_COR_T1_47_1` and
`LW_OUT_COR_T1_47_1` — a corrected longwave version from earlier work. Establish
what that correction was before screening the raw fields, since the existing
`LW_IN` product does not use it.

**Soil heat flux: nothing is known from here.** No notebook has ever queried the
measurement, so its name, its fields and their coverage are all unestablished.
Two things are worth carrying into that query. The 2004 CR10X program declares
**four** plates, `SHF_A` to `SHF_D`, storing 30-minute mean and standard
deviation for `A`, `B` and `C` and not storing `D`; `docs/Instrumentation.md`
lists a single HFP01 at 0.05 m, which the program contradicts. **verify** the
measurement name (`G` or `SHF`), how many plates are in the database, and over
which eras — then decide whether the product exports the plates individually,
their mean, or both. The FLUXNET convention is `G_1_1_1`, `G_2_1_1`, … per plate.

The listing query is the same one the screening notebooks already run:

```python
dbc.show_fields_in_measurement(bucket='ch-lae_raw', measurement='G')
```

Two further points to settle while writing these products:

- **`G` is measured below the surface.** A plate at 0.05 m misses the heat stored
  in the soil above it. Whether the product exports the plate flux as measured or
  adds a storage term computed from `TS` and `SWC` is a scope decision, and it
  determines whether `G` can be used in an energy-balance closure figure.
- **The 24-day CNR4 window (14 Dec 2021 - 7 Jan 2022)** is unresolved for the
  incoming components already and applies to the outgoing ones identically: if
  the CNR4 was read through the CNR1 multiplier, those values are wrong by the
  ratio of the sensitivities. See `docs/Instrumentation.md`.

### 3.3 Candidates, not yet decided

Measured at the site, plausible for the dataset, no decision taken. Listed so the
scope question is asked once rather than rediscovered.

| candidate | raw database field | note |
|---|---|---|
| `PPFD_OUT` | `PPFD_OUT_T1_47_1`, `PPFD_OUT_T1_47_2` | two sensors; a reflected-PAR channel (`PPFD_refl`) already exists in the 2004 program, so the record may predate the 2016 PAR LITE |
| `PPFD_DIF` | `PPFD_DIF_T1_47_1` | Delta-T BF2 sunshine sensor, total and diffuse PAR, from Aug 2004 |
| second `PPFD_IN` | `PPFD_IN_T1_47_2` | a second incoming sensor at the same level; decide whether it is a replicate or a replacement era |
| `NETRAD` | `NETRAD_FF1_2_1`, `NETRAD_NABEL_T1_49_1` | no tower-level net radiometer field; a 47 m `NETRAD` would be derived from the four components. Only the NABEL sensor is screened (2004-2018), and no product exists |
| `ALB` | derived, `SW_OUT`/`SW_IN` | follows from 3.2, costs nothing extra |
| `WS`, `WD` | — | A100LK cup anemometer from Jan 2016; the sonic series is already in the flux output |
| `SWP` | — | MPS-2 and TEROS 21 water potential, FF1 and FF2; same 19 Mar 2020 generation change as `SWC` |
| subcanopy (`M1_2`) | `SW_IN_BC_M1_2_1`, `SW_OUT_BC_M1_2_1`, `LW_IN_BC_M1_2_1`, `LW_OUT_BC_M1_2_1`, `PPFD_IN_BC_M1_2_1` | a full four-component radiation set below canopy, plus PAR — a second measurement level, not a single variable |
| forest floor | `PPFD_IN_AVG_FF1_2_1`, `NETRAD_FF1_2_1` | the FF1 profile's own radiation |

The database field names above are read from listings cached in the outputs of
the `SW_IN`, `LW_IN`, `PPFD_IN` and `NETRAD` screening notebooks. Field existence
is not coverage: the first and last date of each has still to be checked.

Excluded by an existing decision: the **profile masts** (`T1_17.5`, `T1_35`,
`M2`, `M3`, `M4`). The dataset takes its meteorology from the 47 m level and the
forest floor. See `docs/Instrumentation.md`.


## 4. Fluxes

### 4.1 What the dataset publishes

| flux | from | state |
|---|---|---|
| `NEE` | CO~2~ flux plus storage, u*-filtered, gap-filled | open, chain exists |
| `LE` | latent heat flux plus storage, gap-filled | open, chain exists |
| `H` | sensible heat flux | **no chain notebook exists** |
| `GPP`, `RECO` | Level-4.2 partitioning of gap-filled `NEE` | **no notebook exists** |
| `ET` | derived from `LE` | not started; decide whether to publish |

`H` and the partitioned fluxes are the two real gaps in the flux side. `H` is
described in `docs/index.md` as part of the dataset and Level-4.2 is in the
processing-chain flowchart, but neither has a notebook.

### 4.2 Chain status

Levels as defined in `docs/FPC.qmd`.

| level | what it does | `IRGA75` | `IRGA72` | site page |
|---|---|---|---|---|
| Raw | binary → ASCII (bico) | done | done | stub |
| L0 | preliminary run, per setup period | done, 2004-2019 | done, **through 2025** | written |
| L1 | final run, per setup period | done, 2004-2019 | done **only through 2024** | stub |
| L1.1 | self-heating correction (open path only) | notebooks exist | n/a | written |
| L2 | quality flags from L1 output | in `30_` chain | in `30_` chain | stub |
| L3.1 | storage term added | in `30_` chain | in `30_` chain | stub |
| L3.2 | outlier detection, u* threshold detection | done, 2005-2019 | done, 2016-2024 | stub |
| L3.3 | flags from three constant u* thresholds | `NEE` | `NEE`, `LE` | written |
| L4.1 | gap-filling (long-term random forest) | open | `NEE`, `LE` | stub |
| L4.2 | partitioning into `GPP` / `RECO` | open | open | stub |
| QCF | overall quality flag | — | — | stub |

Every chain stage stops at **2024** for `IRGA72`. Extending it to 2025 is the
work described in section 5.

### 4.3 Auxiliary flux-derived series to decide on

Storage terms (`SC`, `SLE`, `SH`), friction velocity `USTAR`, the u* threshold
actually applied, the per-level quality flags and `QCF`, and the sonic wind
series. These exist in the processing output; the decision is which of them the
published file carries and under which names. `docs/Variables.md` is the page
that will state it.


## 5. Where to continue

In order. Each item is blocked by the one above it.

1. **Final 2025 fluxes for `IRGA72`.** EddyPro run for setup period `2025_1`,
   using `2025_1`'s own time lags from
   `00_L0_checks/IRGA72/05_IRGA72-L0_check_timelags_2016-2025.ipynb` and the
   biomet file `EDDYPRO_BIOMET_CH-LAE_2004-2025.csv`. Output into
   `0_data/IRGA72-Level-1_fluxnet_2016-2025/`. The biomet file is ready and has
   been checked against the 2016-2024 runs: same timestamp convention, no
   discontinuity.
2. **Carry `20_MERGE_DATA/IRGA72` to 2025** — notebooks `22.1` and `22.3`, both
   currently named `2016-2024`.
3. **Carry the `30_FLUX_PROCESSING_CHAIN` stages to 2025** — `32_` u* detection,
   `34_` L3.3 and L4.1 for `NEE` and `LE`. Note that stage `34_IRGA72_2016-2024`
   holds notebooks whose filenames say `IRGA75`; check which instrument they
   actually process before extending them.
4. **Add `SW_OUT`, `LW_OUT` and `G`** — resolve the two `verify` items in 3.2
   first, since they set each product's period.
5. **Decide the candidate list in 3.3**, then freeze the variable inventory and
   write `docs/Variables.md`.
6. **Close the flux gaps** — `H` through the chain, and Level-4.2 partitioning.
7. **Fill the stub pages** — `L1`, `L2`, `L3.1`, `L3.2`, `L4.1`, `L4.2`, `QCF`,
   `Raw_Data`, and `Overview`, `Variables`, `Versions`, `Software`,
   `Management_Data`, `Supplementary`, `Links`.


## 6. Open questions

Carried here because each blocks a scope decision or a published statement.

- **How far back do `SW_OUT_T1_47_1` and `LW_OUT_T1_47_1` reach?** The fields
  exist; their first date sets whether `SW_OUT`, `LW_OUT`, `ALB` and a
  four-component `NETRAD` are 2005-2025 or 2022-2025 products. Section 3.2.
- **What is the soil heat flux measurement called, and how many plates does it
  hold?** Nothing is known; the 2004 logger program says four plates, the
  instrumentation page says one. Section 3.2.
- **What is `LW_*_COR_T1_47_1` in `ch-lae_processed`?** A longwave correction
  from earlier work that the current `LW_IN` product does not use. Section 3.2.
- **Does `G` carry a storage term above the plate?** Section 3.2.
- **The 24-day CNR4 window, 14 Dec 2021 - 7 Jan 2022.** Radiation values there
  are unverified. `docs/Instrumentation.md`.
- **Sonic orientation from `2005_2`**: note 5 records a possible change from
  209° to 206° and asks for verification. Unresolved, and it falls in the
  `IRGA75` era. `workflow/00_L0_checks/CLAUDE.md`.
- **Shifted raw-file timestamps, July 2013.** The raw files still carry wrong
  names; the fix is applied by renaming after the bico conversion, and has to be
  applied again on any re-run. `docs/Yearly_Notes.md`.
- **Is `H` in the dataset?** `docs/index.md` says it is; nothing computes it.
  Section 4.1.
