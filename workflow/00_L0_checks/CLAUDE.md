# Stage 00 (`00_L0_checks`) and the EC setup

> Stage-specific guidance. Repo-wide conventions and the hard rules live in the
> root `CLAUDE.md`.


Level 0 is the preliminary flux calculation. EddyPro is run **per setup period**,
so this stage merges the per-run *FLUXNET* output files into one 30MIN record per
gas analyser (`01`/`11`) and then checks that record — fluxes, wind direction,
time lags — before anything downstream reads it. The merge notebook computes and
corrects nothing beyond dropping columns that do not belong; the check notebooks
export nothing.

`docs/Yearly_Notes.md` is the authority for the setup. Its `## Setup EC` table
lists every setup period with its raw-binary range, sonic, gas analysers, sensor
separations and the BICO/flux-run configuration. Read it there rather than
quoting from memory; the points below are the ones that keep costing time.

**The table's numbered notes are the important part and their legend is not in
this repo.** `(1)`-`(24)` are defined on the SwissFluxNet page linked at the top
of `Yearly_Notes.md`
(`swissfluxnet.ethz.ch/index.php/sites/site-info-ch-lae/ec-raw-binary-format-ch-lae/`).
They carry the corrections, the unusable periods and the time-lag settings — a
setup period read without its note looks clean when it is not. The BICO and `FR`
letters have no published legend on either page.

- **`IRGA72` and `IRGA75` name the analyser, not a period.** `IRGA75` is the
  open-path LI-7500, `IRGA72` the closed-path LI-7200. The LI-7500 runs from
  2004; the LI-7200 was added on **11 January 2016** (`2016_2`, first binary
  `2016011115.b05`, and the merged L0 record does start 2016-01-11 15:15). Both
  were calculated in parallel through `2017_1`. The LI-7500 was **removed from
  the site on 12 December 2017** (note 9) but kept logging empty values in the
  data stream until it was taken out of it on **31 January 2018** (notes 10, 11),
  which is why `2017_2` and `2018_1` list it in parentheses with no flux run.
  Each analyser has its own `0_data/` source folder, its own subfolder under
  every stage, and its own merged L0 file.
- **A gap in one analyser's run sequence is often a run in the other's — but not
  always, and the largest gaps have more than one cause.** The two longest holes
  in the merged IRGA72 record are both fully explained by the notes:
  - **69 days, 2019-01-10 15:15 → 2019-03-20 18:45.** Two causes end to end. The
    LI-7200 was replaced on 11 January 2019 and *both* units were defective, so
    `2019_2` yields mostly incomplete files and unusable fluxes (note 17); then
    the LI-7500 was brought back to stand in for it for `2019_3`, 17 January -
    20 March (note 16). `2019_3` is therefore in the IRGA75 source folder, which
    is what the `+2019` in `OPENLAG-IRGA75-Level-0_fluxnet_2005-2016+2019` means.
    A `2019_2` file exists here and yields **no** `FC` and **no** `LE` at all;
    its presence is not evidence that the period has data. It does yield 289
    half-hours of `H`, because `H` comes from the sonic and only the gas analyser
    was defective — so a coverage check run on `H` alone would miss this entirely.
    Judge a gas-analyser fault on a gas flux.
  - **56 days, 2021-12-13 19:15 → 2022-02-07 10:45.** `2021_2` and `2022_1` have
    no source file at all: the raw data was logged in an unknown format and the
    conversion fails on an unrecognised 44-byte IRGA record, so it may be
    corrupted (note 22). This gap cannot be filled from the other analyser.
- **`IRGA72` spans two physical analysers.** IRGA72-B (as `IRGA72-B-GN1` from
  `2017_2`) through `2019_2`, then IRGA72-A from `2019_4`, whose stream has 13
  columns — `diag_val` and `signal_strength` added, `status_byte` gone (note 14).
  The swap sits inside the 69-day gap above. Same trap as the meteo field names:
  one name, two instruments.
- **The analyser also moved on the boom.** Its separation from the sonic changes
  at `2023_2` from `N+6 E-1 V-15` to `N+11 E+1 V-1`, tube length and delay
  unchanged; the inlet was repositioned and `2023031319.L00` is the first
  complete file in the new position (note 23). A separation change moves time
  lags, which is exactly what `05_…check_timelags` looks at.
- **Time lags are not comparable across setup periods, and the notes say why.**
  An artificial lag of 12 s was introduced by buffer processing in `2019_2` and
  has to be allowed for in lag detection (note 13); `2022_2` carries no
  artificial lag and its detected lag falls in the expected range, ~1.25 s for
  CO2 (note 12); the lag then shifts again in `2022_3` (back to 8.5 s) and
  `2022_4` (lower still), and those two periods need to be calculated separately
  (note 7). A lag-detection notebook that pools setup periods is comparing
  different acquisition settings.
- **The sonic is HS50-B at 47 m, orientation `209°`, unchanged through the
  record — with one open question.** Note 5 records that the orientation may have
  changed to `206°` from `2005_2` onward and says recalculations should verify
  it; it is unresolved, and it is in the LI-7500 era. The `209°` itself was
  confirmed independently from wind-direction histograms across years; an old
  `locations.table` gives `183°` to `209°` and is not trusted.
- **The per-year sections below that table are partly unedited stubs.** The
  2021-2025 blocks say `Instruments: R350, IRGA75` and link to the **Chamau**
  setup page, contradicting the table's HS50-B and IRGA72-A. The table wins; do
  not take instrument names from those blocks.
- **The run label is the setup period, not a part of the year.** `2016_2+3` is
  one EddyPro run covering setup periods 2 and 3 of 2016, so a run boundary is a
  hardware or configuration change and runs do not map onto calendar years. Merge
  on the timestamps inside the files, never on the file names.
- **The EC output carries no meteo.** The 2025 IRGA72 run exported its biomet
  inputs (`TA_1_1_1`, `RH_1_1_1`, `PA_1_1_1`, `SW_IN_1_1_1`, `LW_IN_1_1_1`,
  `PPFD_IN_1_1_1`) into the FLUXNET file by mistake; no other run has them. The
  merge notebook drops them so the merged record keeps one column set over its
  whole length; meteo comes from the `10_METEO` products. The drop is guarded by
  reading the source **headers** and asserting that exactly one run carries the
  columns. A first version guarded on the year instead and failed: a run begins
  at the last binary of the previous December (`2025_1` starts
  `2024123119.L00`), so its records reach back into 31 December of the year
  before, and any per-year threshold is off by a day at every run boundary.
- **Periods that are present in the record and should not be used as measured:**
  - **The wrong calibration gas (note 15)** affects **all IRGA72 CO2
    concentrations between 14 December 2017 and 15 March 2019** — not just the
    end of 2017, which is what `Yearly_Notes.md` alone suggests. The correction
    is a factor **0.974 applied to the CO2 concentration before the fluxes are
    calculated**, so it cannot be applied to a finished flux product. The
    LI-7500 fluxes of `2019_3` are unaffected (note 16), and the correct gas is
    in use from `2019_4` (note 18).
  - **May/June 2018 (note 19):** the LI-7200 flow module failed, which also
    prevented lag detection until the module was replaced on 7 June 2018. Do not
    use CO2 fluxes 19 May - 6 Jun 2018 or water fluxes 13 May - 6 Jun 2018.
  - **The 2016 commissioning (notes 20, 21):** `2016_2` splits into an
    installation phase and a low-flowrate phase, both to be avoided (water in the
    filter suppressed the CO2 and H2O fluxes), with an acceptable initialisation
    phase between them. Quality is good from `2016_3` on.
- **July 2013 (LI-7500 era):** the timestamp in the raw binary *file names* is
  wrong between `2013070615.b02` and `2013071214.b00` by about 6 hours (note 8;
  the MOXA clock was corrected on 12 July 2013). The raw files still carry the
  wrong names; the fix is to rename after the bico conversion. Uncorrected, it
  reached the FP2021 fluxes as a ~14.5 h shift between 2013-07-06 15:45 and
  2013-07-12 23:45.

