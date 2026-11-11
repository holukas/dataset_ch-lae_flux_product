# Roadmap

Features and corrections planned for flux product releases after `FP2026.2`. The work for the
current release is in section 5 of `PLAN.md`; "item" numbers refer to `PLAN.md`. Each entry has
an identifier `R<n>`, which stays with it and is never reused. An entry moves out of this file
once it is scheduled for a release, and its outcome is recorded in `PLAN.md` or the docs.

## Next release

- **R1. `SW_IN` step of the CNR1** (decided 10 Nov 2026). Candidate factor 1.04 (range about
  1.025-1.06) on measured `SW_IN` from 14 Sep 2005 to about 1 Apr 2013, none on the 2004-2005
  fills. Evidence (item 25 (d), `research/reports/uptake_2026-11-08/D_swin/`): `SW/PPFD` and
  `SW/POT` step up in 2013 while `PPFD/POT` is flat; the CNR4 from Dec 2021 continues the later
  level. Weak points: before 2011 `SW/MeteoSwiss` shows no deficit (MeteoSwiss Laegern has its own
  step of about +4 % in 2011); the break lies between Nov 2012 and Sep 2013; no fieldbook entry;
  NABEL `SW_IN` was not compared (held in InfluxDB). Before applying: compare with NABEL 2008-2015
  and look for a CNR1 exchange or recalibration in 2012-2013.
- **R2. Meteo logger clock offset** (decided 10 Nov 2026). The tower radiation series run 10-15 min
  early against MeteoSwiss and potential radiation from about Jan 2009 (onset between Oct 2008 and
  Jan 2009, with resets of the meteo station power on 11 Nov 2008, 18 Jan 2009 and 25 Feb 2009) to
  the power failure of 7-9 Aug 2012 (last offset day 27 Jul, first normal day 11 Aug 2012); against
  potential radiation it grows to about -15 to -18 min in 2011-2012. Both `SW_IN` and `PPFD` move
  together, so it is the logger clock. To decide: whether the EC clock shares the offset (diel
  timing of `H` against `SW_IN` and potential radiation per quarter; the embedded computer was set
  7 min forward on 29 Sep 2011). If the EC clock is right, shift the meteo series of that period;
  otherwise document it.

## Later or unscheduled

- **R3. Recompute the `IRGA75` fluxes from the 20 Hz raw data** (noted 3 Nov 2026). With the zero and
  span coefficients of each calibration period applied to the raw CO2 and H2O (fieldbook checks of
  7 Feb 2006, 26 Sep 2007, 19 Dec 2007, 16 May 2008 and later; H2O gain +30 % in May 2008 - Dec
  2010), so that the covariance effect of the CO2 offset (Fratini et al. 2014) is included, which
  Level-1 data cannot give. Then look for the heating signature in the cospectra: a part common to
  the CO2 and H2O signals in proportion to their densities, which would estimate the self-heating
  from the open-path data alone. Raw data: 2004-2008 converted (`F:\CURRENT\LAE_FP2026\`), 2008-2015
  as bico binaries; the half-hourly statistics code of `research/reports/raw_hf_2026-11-09/`
  reproduces EddyPro and can serve as a start.
- **R4. Sensitivity of the gap-filled sums to the number of trees** (item 8). The `IRGA72` sum of 2016
  moves from +58 to +188 gC m-2 between 90 and 1000 trees.

## Waiting for outside data

- **R5. An independent constraint of the early `IRGA75` years** (items 17 and 25): biometric data of
  Etzold et al. (2011), TreeNet, MODIS/Landsat greenness, FLUXNET2015 CH-Lae, or QCL or chamber
  data. Decides whether the lower uptake of 2004-2007 is real.
- **R6. The probable LI-7200 of Dec 2010 to Jun 2011** (item 26). Not in the site's raw files of
  2010-2011; the search continues on other disks and in the institute archive.
