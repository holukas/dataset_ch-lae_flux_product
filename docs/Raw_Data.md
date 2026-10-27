# Raw Data: Eddy Covariance

The raw eddy covariance data are not part of FP2026.1. This page describes the data the fluxes
were calculated from.

## Measurement

- **Height and rate.** The sonic anemometer and the gas analysers are mounted at 47 m on the tower
  and sampled at 20 Hz. The sonic orientation is 209° (see [Level 0](L0.md)).
- **Gas analysers.**
  - `IRGA72`, the enclosed-path LI-7200, from 11 January 2016. The fluxes in FP2026.1 are
    calculated from this analyser.
  - `IRGA75`, the open-path LI-7500, from 2004 to 12 December 2017, and from 17 January to
    20 March 2019 as a stand-in for the defective LI-7200. Its fluxes are in progress for FP2026.2
    and are not part of FP2026.1.

  Both analysers measured in parallel from 11 January 2016 to 12 December 2017. Models, serial
  numbers and exchanges of all instruments are listed on [Instrumentation](Instrumentation.md).

## Files

The raw data are stored as binary files, each typically covering 6 hours. The file name gives the
start of the file: `2013070615.b02` starts on 6 July 2013 at 15:00.

The setup changes over time. Each change of hardware or configuration starts a new **setup
period**, labelled by year and number (`2016_2`). The setup table on
[Yearly Notes](Yearly_Notes.md) lists every setup period with its first and last raw file, its
instruments and their separations. Its numbered notes are explained on the
[SwissFluxNet page on the raw binary format](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-lae/ec-raw-binary-format-ch-lae/).

## Conversion to ASCII

The binary files are converted to ASCII with [bico](https://github.com/holukas/bico) before the
flux calculation. Two corrections are made in this step:

- **Wrong calibration gas.** All `IRGA72` CO2 concentrations from 14 December 2017 to
  15 March 2019 were calibrated against the wrong reference gas. They are multiplied by 0.974
  during the conversion, so every flux calculated from them is corrected.
- **File names in July 2013.** The names of the files from `2013070615.b02` to `2013071214.b00`
  give a start time that is wrong by about 6 hours. The converted files are renamed after the
  conversion. This affects only the `IRGA75` record.

## Known limitations

- **No fluxes from 13 December 2021 to 7 February 2022.** The raw data of setup periods `2021_2`
  and `2022_1` were logged in an unknown format, and the conversion fails on an unrecognised
  analyser record. The data may be corrupted.
