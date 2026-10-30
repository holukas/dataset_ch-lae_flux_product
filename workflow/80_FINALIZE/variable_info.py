"""Unit and short description of each column of the finalize collection and the release datasets.

`describe(name)` returns `(unit, description)`, or `None` for a column it does not know, so the
notebooks can assert that every column is described. The Level-1 columns are those of the EddyPro
FLUXNET output; their units were checked against the value ranges of the collection. Columns of the
flux post-processing chain are described from their name, which diive builds from the flux, the
level, the scenario and the test.
"""
import re

DIMLESS = '-'

# --- Level-1 fluxes (EddyPro FLUXNET output) --------------------------------------------------

# Flux, unit, description.
FLUXES = {
    'FC': ('µmol m-2 s-1', 'CO2 flux'),
    'FH2O': ('mmol m-2 s-1', 'H2O flux'),
    'LE': ('W m-2', 'Latent heat flux'),
    'ET': ('mm h-1', 'Evapotranspiration'),
    'H': ('W m-2', 'Sensible heat flux'),
    'TAU': ('kg m-1 s-2', 'Momentum flux'),
}

# Suffix of a flux column: unit (None = unit of the flux), description.
FLUX_SUFFIXES = {
    '': (None, 'fully corrected (EddyPro)'),
    '_UNCORR': (None, 'without corrections'),
    '_STAGE1': (None, 'after the first stage of corrections'),
    '_STAGE2': (None, 'after the second stage of corrections'),
    '_RANDUNC_HF': (None, 'random uncertainty (EddyPro)'),
    '_VADV': (None, 'vertical advection flux'),
    '_SCF': (DIMLESS, 'spectral correction factor'),
    '_SSITC_TEST': (DIMLESS, 'quality flag of the steady-state and integral turbulence tests '
                             '(0 best, 1 good, 2 bad; Mauder and Foken 2004)'),
    '_SS': ('%', 'steady-state test: relative deviation between the 5-min and 30-min covariances '
                 '(Foken and Wichura 1996)'),
    '_SS_TEST': (DIMLESS, 'steady-state test class (1 best to 9 worst)'),
    '_NSR': (DIMLESS, 'non-stationarity ratio (Mahrt 1998)'),
    '_NR': (DIMLESS, 'number of records used for the flux'),
    '_CORRDIFF': (DIMLESS, 'diagnostic of the EddyPro FLUXNET output; definition to be checked'),
}

# Raw variable: unit, description. The CO2 and H2O statistics are of the measured series.
RAW = {
    'U': ('m s-1', 'longitudinal wind component'),
    'V': ('m s-1', 'lateral wind component'),
    'W': ('m s-1', 'vertical wind component'),
    'T_SONIC': ('°C', 'sonic temperature'),
    'CO2_MEAS': ('µmol mol-1', 'CO2 as measured by the analyser'),
    'H2O_MEAS': ('mmol mol-1', 'H2O as measured by the analyser'),
    'CO2': ('µmol mol-1', 'CO2'),
    'H2O': ('mmol mol-1', 'H2O'),
}

# Statistic or test of a raw variable: unit (None = unit of the variable), description.
RAW_SUFFIXES = {
    '_MEDIAN': (None, 'median of the 30-min raw data'),
    '_P25': (None, '25th percentile of the 30-min raw data'),
    '_P75': (None, '75th percentile of the 30-min raw data'),
    '_SIGMA': (None, 'standard deviation of the 30-min raw data'),
    '_SKW': (DIMLESS, 'skewness of the 30-min raw data'),
    '_KUR': (DIMLESS, 'kurtosis of the 30-min raw data'),
    '_NR': (DIMLESS, 'number of valid raw records'),
    '_NUM_SPIKES': (DIMLESS, 'number of spikes detected in the raw data'),
    '_SPIKE_NREX': (DIMLESS, 'number of raw records flagged by the spike test'),
    '_ABSLIM_NREX': (DIMLESS, 'number of raw records outside the absolute limits'),
    '_DIAG_NREX': (DIMLESS, 'number of raw records removed by the analyser diagnostics'),
    '_VM97_TEST': (DIMLESS, 'flags of the raw-data tests of Vickers and Mahrt (1997), one digit per test'),
    '_KID': (DIMLESS, 'kurtosis index of the differenced raw data (Vitale et al. 2020)'),
    '_ZCD': (DIMLESS, 'number of zero crossings of the differenced raw data (Vitale et al. 2020)'),
    '_LGD': ('s', 'longest gap duration in the raw data (Vitale et al. 2020)'),
    '_ITC': ('%', 'integral turbulence characteristics test: relative deviation from the model '
                  '(Foken and Wichura 1996)'),
    '_ITC_TEST': (DIMLESS, 'integral turbulence characteristics test class (1 best to 9 worst)'),
    '_UNROT': ('m s-1', 'before the coordinate rotation'),
    '_TLAG_ACTUAL': ('s', 'time lag found by the covariance maximisation'),
    '_TLAG_USED': ('s', 'time lag used'),
    '_TLAG_NOMINAL': ('s', 'nominal time lag'),
    '_TLAG_MIN': ('s', 'minimum of the time-lag search window'),
    '_TLAG_MAX': ('s', 'maximum of the time-lag search window'),
    '_MIXING_RATIO': (None, 'mixing ratio (mole fraction in dry air)'),
    '_MOLAR_DENSITY': ('mmol m-3', 'molar density'),
    '_MEAS_TYPE': (DIMLESS, 'measurement type of the analyser output (EddyPro code)'),
}

# Customised variables of the EddyPro runs: 30-min means of the logged analyser diagnostics.
CUSTOM = {
    'AGC_IRGA75': ('%', 'LI-7500 automatic gain control'),
    'AIR_P': ('Pa', 'air pressure logged with the raw data'),
    'CELL_T': ('K', 'LI-7200 cell temperature'),
    'INT_P': ('Pa', 'LI-7200 cell (internal) pressure'),
    'CO2': ('mmol m-3', 'CO2 molar density logged with the raw data'),
    'H2O': ('mmol m-3', 'H2O molar density logged with the raw data'),
    'COOLER_V_IRGA72': ('V', 'LI-7200 cooler voltage'),
    'COOLER_V_IRGA75': ('V', 'LI-7500 cooler voltage'),
    'COOLER_V': ('V', 'analyser cooler voltage'),
    'DATA_SIZE_IRGA72': (DIMLESS, 'LI-7200 data record size'),
    'DATA_SIZE_IRGA75': (DIMLESS, 'LI-7500 data record size'),
    'FLOW_VOLRATE': ('L min-1', 'LI-7200 volumetric flow rate of the sampling line'),
    'GA_DIAG_CODE_IRGA72': (DIMLESS, 'LI-7200 diagnostic code'),
    'GA_DIAG_CODE_IRGA75': (DIMLESS, 'LI-7500 diagnostic code'),
    'SIGNAL_STRENGTH_IRGA72': ('%', 'LI-7200 signal strength'),
    'STATUS_CODE_IRGA72': (DIMLESS, 'LI-7200 status code'),
    'STATUS_CODE_IRGA75': (DIMLESS, 'LI-7500 status code'),
}

L1 = {
    # Time
    'TIMESTAMP_START': (DIMLESS, 'Start of the averaging period, YYYYMMDDhhmm (EddyPro)'),
    'DOY_START': (DIMLESS, 'Start of the averaging period, fractional day of year (EddyPro)'),
    'DOY_END': (DIMLESS, 'End of the averaging period, fractional day of year (EddyPro)'),
    'NIGHT': (DIMLESS, 'Night flag of EddyPro (1 = night)'),
    'SW_IN_POT_EDDYPRO': ('W m-2', 'Potential incoming shortwave radiation from EddyPro, computed for '
                                   'the end of the half-hour (renamed from SW_IN_POT)'),
    # Raw files and records
    'FILE_NR': (DIMLESS, 'Number of records in the raw file'),
    'EXPECT_NR': (DIMLESS, 'Number of records expected in the averaging period'),
    'FILE_TIME_DURATION': (DIMLESS, 'Duration of the raw file as reported by EddyPro; unit to be checked'),
    'SONIC_NR': (DIMLESS, 'Number of valid sonic anemometer records'),
    'SONIC_DIAG_NREX': (DIMLESS, 'Number of records removed by the sonic anemometer diagnostics'),
    'CUSTOM_FILTER_NR': (DIMLESS, 'Number of records checked by the custom filter'),
    'CUSTOM_FILTER_NREX': (DIMLESS, 'Number of records removed by the custom filter'),
    'WD_FILTER_NR': (DIMLESS, 'Number of records checked by the wind-direction filter'),
    'WD_FILTER_NREX': (DIMLESS, 'Number of records removed by the wind-direction filter'),
    'NUM_BIOMET_VARS': (DIMLESS, 'Number of biomet variables read by EddyPro'),
    'NUM_CUSTOM_VARS': (DIMLESS, 'Number of custom variables read by EddyPro'),
    # Storage terms from one point
    'SC_SINGLE': ('µmol m-2 s-1', 'CO2 storage term from the concentration at the measurement height'),
    'SH2O_SINGLE': ('mmol m-2 s-1', 'H2O storage term from the concentration at the measurement height'),
    'SLE_SINGLE': ('W m-2', 'Latent heat storage term from the measurement height'),
    'SET_SINGLE': ('mm h-1', 'Evapotranspiration storage term from the measurement height'),
    'SH_SINGLE': ('W m-2', 'Sensible heat storage term from the measurement height'),
    # Turbulence and wind
    'USTAR': ('m s-1', 'Friction velocity'),
    'USTAR_UNCORR': ('m s-1', 'Friction velocity without corrections'),
    'TKE': ('m2 s-2', 'Turbulent kinetic energy'),
    'TSTAR': ('K', 'Scaling temperature'),
    'MO_LENGTH': ('m', 'Monin-Obukhov length'),
    'MO_LENGTH_UNCORR': ('m', 'Monin-Obukhov length without corrections'),
    'ZL': (DIMLESS, 'Stability parameter z/L'),
    'ZL_UNCORR': (DIMLESS, 'Stability parameter z/L without corrections'),
    'BOWEN': (DIMLESS, 'Bowen ratio H/LE'),
    'WS': ('m s-1', 'Mean wind speed (sonic anemometer)'),
    'WS_MAX': ('m s-1', 'Maximum wind speed (sonic anemometer)'),
    'WD': ('°', 'Mean wind direction (sonic anemometer)'),
    'WD_SIGMA': ('°', 'Standard deviation of the wind direction'),
    'ROT_YAW': ('°', 'Yaw angle of the coordinate rotation'),
    'ROT_PITCH': ('°', 'Pitch angle of the coordinate rotation'),
    'W_U_COV': ('m2 s-2', 'Covariance of W and U'),
    'W_T_SONIC_COV': ('K m s-1', 'Covariance of W and T_SONIC'),
    'W_T_SONIC_COV_IBROM': ('K m s-1', 'Covariance of W and T_SONIC used for the in-situ spectral '
                                       'assessment (Ibrom et al. 2007)'),
    'W_CO2_MEAS_COV': ('µmol mol-1 m s-1', 'Covariance of W and the measured CO2'),
    'W_H2O_MEAS_COV': ('mmol mol-1 m s-1', 'Covariance of W and the measured H2O'),
    'CO2_MEAS_H2O_MEAS_COV': ('µmol mol-1 mmol mol-1', 'Covariance of the measured CO2 and H2O'),
    'VM97_AOA_HF': (DIMLESS, 'Angle-of-attack test of Vickers and Mahrt (1997), hard flag'),
    'VM97_NSHW_HF': (DIMLESS, 'Non-steady horizontal wind test of Vickers and Mahrt (1997), hard flag'),
    'VM97_TLAG_HF': (DIMLESS, 'Time-lag test of Vickers and Mahrt (1997), hard flags per scalar'),
    'VM97_TLAG_SF': (DIMLESS, 'Time-lag test of Vickers and Mahrt (1997), soft flags per scalar'),
    # Air and thermodynamics
    'TA_EP': ('°C', 'Air temperature used by EddyPro'),
    'PA_EP': ('kPa', 'Air pressure used by EddyPro'),
    'RH_EP': ('%', 'Relative humidity used by EddyPro'),
    'VPD_EP': ('hPa', 'Vapour pressure deficit used by EddyPro'),
    'TDEW': ('°C', 'Dew point temperature'),
    'T_CELL': ('°C', 'Temperature in the LI-7200 cell'),
    'PA_CELL': ('kPa', 'Pressure in the LI-7200 cell'),
    'AIR_CP': ('J kg-1 K-1', 'Specific heat of moist air at constant pressure'),
    'AIR_DENSITY': ('kg m-3', 'Density of moist air'),
    'AIR_MV': ('m3 mol-1', 'Molar volume of moist air'),
    'AIR_RHO_CP': ('J m-3 K-1', 'Volumetric heat capacity of moist air'),
    'DRYAIR_DENSITY': ('kg m-3', 'Density of dry air'),
    'DRYAIR_MV': ('m3 mol-1', 'Molar volume of dry air'),
    'DRYAIR_PARTIAL_PRESSURE': ('kPa', 'Partial pressure of dry air'),
    'MV_AIR_CELL_CO2': ('m3 mol-1', 'Molar volume of air in the LI-7200 cell, for CO2'),
    'MV_AIR_CELL_H2O': ('m3 mol-1', 'Molar volume of air in the LI-7200 cell, for H2O'),
    'VAPOR_DENSITY': ('kg m-3', 'Water vapour density'),
    'VAPOR_DRYAIR_RATIO': ('kg kg-1', 'Mass ratio of water vapour to dry air'),
    'VAPOR_PARTIAL_PRESSURE': ('hPa', 'Water vapour partial pressure'),
    'VAPOR_PARTIAL_PRESSURE_SAT': ('hPa', 'Saturation water vapour pressure'),
    'SPECIFIC_HUMIDITY': ('kg kg-1', 'Specific humidity'),
    'SPECIFIC_HEAT_EVAP': ('J kg-1', 'Latent heat of vaporisation'),
    # Footprint
    'FOOTPRINT_MODEL': (DIMLESS, 'Footprint model (EddyPro code)'),
    'FETCH_MAX': ('m', 'Distance of the peak contribution to the flux footprint'),
    'FETCH_OFFSET': ('m', 'Footprint offset'),
    # Processing options (EddyPro codes)
    'AOA_METHOD': (DIMLESS, 'Angle-of-attack correction (EddyPro code)'),
    'AXES_ROTATION_METHOD': (DIMLESS, 'Coordinate rotation method (EddyPro code)'),
    'BURBA_METHOD': (DIMLESS, 'Self-heating correction of Burba et al. 2008 (EddyPro code)'),
    'DETRENDING_METHOD': (DIMLESS, 'Detrending method (EddyPro code)'),
    'DENTRENDING_TIME_CONSTANT': ('s', 'Time constant of the detrending'),
    'SPECTRAL_CORRECTION_METHOD': (DIMLESS, 'Spectral correction method (EddyPro code)'),
    'TIMELAG_DETECTION_METHOD': (DIMLESS, 'Time-lag detection method (EddyPro code)'),
    'WBOOST_APPLIED': (DIMLESS, 'W-boost correction of the Gill sonic anemometers applied (1 = yes)'),
    'WPL_APPLIED': (DIMLESS, 'WPL density correction applied (1 = yes)'),
    # Instruments and site (BADM)
    'HPATH_GA_CO2': ('cm', 'Horizontal path of the analyser, CO2'),
    'HPATH_GA_H2O': ('cm', 'Horizontal path of the analyser, H2O'),
    'HPATH_SA': ('cm', 'Horizontal path of the sonic anemometer'),
    'VPATH_GA_CO2': ('cm', 'Vertical path of the analyser, CO2'),
    'VPATH_GA_H2O': ('cm', 'Vertical path of the analyser, H2O'),
    'VPATH_SA': ('cm', 'Vertical path of the sonic anemometer'),
    'RESPONSE_TIME_GA_CO2': ('s', 'Response time of the analyser, CO2'),
    'RESPONSE_TIME_GA_H2O': ('s', 'Response time of the analyser, H2O'),
    'RESPONSE_TIME_SA': ('s', 'Response time of the sonic anemometer'),
    'INST_LI7200_AGC_OR_RSSI': (DIMLESS, 'LI-7200 AGC or RSSI from the EddyPro metadata (9999 = not set)'),
    'INST_LI7500_AGC_OR_RSSI': (DIMLESS, 'LI-7500 AGC or RSSI from the EddyPro metadata (9999 = not set)'),
    'DISPLACEMENT_HEIGHT': ('m', 'Zero-plane displacement height'),
    'ROUGHNESS_LENGTH': ('m', 'Roughness length'),
    'BADM_HEIGHTC': ('m', 'Canopy height'),
    'BADM_INST_HEIGHT_SA': ('m', 'Measurement height of the sonic anemometer'),
    'BADM_INST_AVERAGING_INT': ('min', 'Averaging interval of the fluxes'),
    'BADM_INST_SAMPLING_INT': ('Hz', 'Sampling frequency of the raw data'),
    'BADM_LOCATION_LAT': ('°N', 'Latitude of the site'),
    'BADM_LOCATION_LONG': ('°E', 'Longitude of the site'),
    'BADM_LOCATION_ELEV': ('m a.s.l.', 'Elevation of the site'),
    'BADM_SA_OFFSET_NORTH': ('°', 'Offset of the sonic anemometer from north'),
}
for _gas in ('CO2', 'H2O'):
    L1.update({
        f'BADM_INSTPAIR_EASTWARD_SEP_GA_{_gas}': ('cm', f'Eastward separation of the analyser from the sonic, {_gas}'),
        f'BADM_INSTPAIR_NORTHWARD_SEP_GA_{_gas}': ('cm', f'Northward separation of the analyser from the sonic, {_gas}'),
        f'BADM_INSTPAIR_HEIGHT_SEP_GA_{_gas}': ('cm', f'Vertical separation of the analyser from the sonic, {_gas}'),
        f'BADM_INST_GA_CP_TUBE_FLOW_RATE_GA_{_gas}': ('L min-1', f'Flow rate of the LI-7200 intake tube, {_gas}'),
        f'BADM_INST_GA_CP_TUBE_IN_DIAM_GA_{_gas}': ('mm', f'Inner diameter of the LI-7200 intake tube, {_gas}'),
        f'BADM_INST_GA_CP_TUBE_LENGTH_GA_{_gas}': ('cm', f'Length of the LI-7200 intake tube, {_gas}'),
    })
for _p in (10, 30, 50, 70, 80, 90):
    L1[f'FETCH_{_p}'] = ('m', f'Distance from the tower within which {_p} % of the flux footprint lies')


def _describe_l1(name):
    if name in L1:
        return L1[name]
    for flux, (funit, fdesc) in FLUXES.items():
        for suffix, (unit, desc) in FLUX_SUFFIXES.items():
            if name == flux + suffix:
                return unit or funit, f'{fdesc}, {desc}'
    m = re.fullmatch(r'W_T_SONIC_COV_IBROM_N(\d{4})', name)
    if m:
        return 'K m s-1', (f'Covariance of W and T_SONIC after low-pass filtering, step {m.group(1)} of the '
                           f'in-situ spectral assessment (Ibrom et al. 2007)')
    m = re.fullmatch(r'CUSTOM_(.+?)_MEAN(?:_(\d))?', name)
    if m and m.group(1) in CUSTOM:
        unit, desc = CUSTOM[m.group(1)]
        desc = f'30-min mean of the {desc}'
        if m.group(2):
            desc += f' (column {m.group(2)} of the same name in the EddyPro output)'
        return unit, desc[0].upper() + desc[1:]
    for raw in sorted(RAW, key=len, reverse=True):
        if name.startswith(raw + '_') and name[len(raw):] in RAW_SUFFIXES:
            runit, rdesc = RAW[raw]
            unit, desc = RAW_SUFFIXES[name[len(raw):]]
            return unit or runit, f'{rdesc[0].upper() + rdesc[1:]}, {desc}'
    if name in ('U', 'V', 'W', 'T_SONIC'):
        return RAW[name][0], f'Mean {RAW[name][1]}'
    if name in RAW:
        unit, desc = RAW[name]
        return unit, f'{desc} (mixing ratio, mean of the 30-min raw data)'
    return None


# --- Meteo -------------------------------------------------------------------------------------

METEO = {
    'SW_IN': ('W m-2', 'Incoming shortwave radiation'),
    'SW_OUT': ('W m-2', 'Outgoing (reflected) shortwave radiation'),
    'LW_IN': ('W m-2', 'Incoming longwave radiation'),
    'LW_OUT': ('W m-2', 'Outgoing (emitted) longwave radiation'),
    'PPFD_IN': ('µmol m-2 s-1', 'Incoming photosynthetic photon flux density'),
    'TA': ('°C', 'Air temperature'),
    'RH': ('%', 'Relative humidity'),
    'VPD': ('kPa', 'Vapour pressure deficit'),
    'PA': ('kPa', 'Air pressure'),
    'PREC_TOT': ('mm (30 min)-1', 'Precipitation'),
    'SWC': ('%', 'Volumetric soil water content'),
    'TS': ('°C', 'Soil temperature'),
    'G': ('W m-2', 'Soil heat flux (positive into the soil)'),
}
METEO_SUFFIXES = {
    '': '',
    '_gfXG': ', gap-filled with XGBoost',
    '_HOMOGENIZED': ', homogenised across sensor changes',
    '_HOMOGENIZED_gfXG': ', homogenised across sensor changes and gap-filled with XGBoost',
    '_HOMOGENIZED_GAPFILLED': ', homogenised across sensor changes and gap-filled',
    '_HOMOGENIZED_MEASURED': ', homogenised across sensor changes, measured values only',
    '_MEASURED': ', measured values only',
}
METEO_FLAGS = {
    'ISFILLED': 'Gap-filling flag of {v} (0 = measured, otherwise filled)',
    'SOURCE': 'Source flag of {v}: which sensor, record or calibration each value comes from',
    'MISSING': 'Flag of {v}: measured or reconstructed values',
    'METHOD': 'Method flag of {v}: measured (and by which sensor generation) or modelled',
    'SUSPECT': 'Flag of {v} for the period in which the early soil profile disagreed with itself',
    'NPLATES': 'Number of heat flux plates behind each value of {v}',
    'INSTRUMENT': 'Instrument flag of {v}: which radiometer and calibration constant',
}
# Tower at 47 m, or the forest-floor profile FF1 at a depth in metres.
LOCATION = r'(?P<loc>T1_47_1|FF1_(?P<depth>[\d.]+)(?:_1)?)'


def _where(m):
    return 'at the tower, 47 m' if m.group('depth') is None else f"at the forest floor, {m.group('depth')} m depth"


def _describe_meteo(name):
    m = re.fullmatch(rf'FLAG_(?P<var>[A-Z_]+?)_{LOCATION}(?P<suffix>_HOMOGENIZED(?:_GAPFILLED)?)?_(?P<flag>[A-Z]+)', name)
    if m and m.group('var') in METEO and m.group('flag') in METEO_FLAGS:
        v = f"{m.group('var')}_{m.group('loc')}{m.group('suffix') or ''}"
        return DIMLESS, METEO_FLAGS[m.group('flag')].format(v=v)
    m = re.fullmatch(rf'(?P<var>[A-Z_]+?)_{LOCATION}(?P<suffix>.*)', name)
    if m and m.group('var') in METEO and m.group('suffix') in METEO_SUFFIXES:
        unit, desc = METEO[m.group('var')]
        return unit, f'{desc} {_where(m)}{METEO_SUFFIXES[m.group("suffix")]}'
    return None


# --- Flux post-processing chain (diive) --------------------------------------------------------

CHAIN_FLUXES = {
    'NEE': ('µmol m-2 s-1', 'Net ecosystem exchange of CO2'),
    'FC': ('µmol m-2 s-1', 'CO2 flux'),
    'LE': ('W m-2', 'Latent heat flux'),
    'H': ('W m-2', 'Sensible heat flux'),
    'ET': ('mm (30 min)-1', 'Evapotranspiration'),
}
CHAIN = {
    'FLAG_FLUX_SOURCE': (DIMLESS, 'Gas analyser of the fluxes of the half-hour: 75 = open-path LI-7500 '
                                  '(IRGA75), 72 = enclosed-path LI-7200 (IRGA72)'),
    'SW_IN_POT': ('W m-2', 'Potential incoming shortwave radiation, for the middle of the half-hour'),
    'DAYTIME': (DIMLESS, 'Daytime flag from SW_IN_POT (1 = day)'),
    'NIGHTTIME': (DIMLESS, 'Nighttime flag from SW_IN_POT (1 = night)'),
    'SC_SINGLE_gfRMED_L3.1': ('µmol m-2 s-1', 'CO2 storage term, screened and gap-filled with a rolling median'),
    'FLAG_SC_SINGLE_gfRMED_L3.1_ISFILLED': (DIMLESS, 'Gap-filling flag of SC_SINGLE_gfRMED_L3.1 '
                                                     '(0 = measured, 1 = filled because missing, '
                                                     '2 = spike block replaced by its mean, '
                                                     '3 = discarded next to a gap and filled)'),
}
TESTS = {
    'MISSING': 'missing-value test',
    'SSITC': 'steady-state and integral turbulence test',
    'SCF': 'spectral correction factor test',
    'SIGNAL_STRENGTH': 'analyser signal strength test',
    'CO2_VM97_SPIKE_HF': 'CO2 raw-data spike test (Vickers and Mahrt 1997)',
    'CO2_VM97_DROPOUT_HF': 'CO2 raw-data dropout test (Vickers and Mahrt 1997)',
    'H2O_VM97_SPIKE_HF': 'H2O raw-data spike test (Vickers and Mahrt 1997)',
    'H2O_VM97_DROPOUT_HF': 'H2O raw-data dropout test (Vickers and Mahrt 1997)',
    'T_SONIC_VM97_SPIKE_HF': 'T_SONIC raw-data spike test (Vickers and Mahrt 1997)',
    'T_SONIC_VM97_DROPOUT_HF': 'T_SONIC raw-data dropout test (Vickers and Mahrt 1997)',
    'T_SONIC_VM97_ABSOLUTE_LIMITS_HF': 'T_SONIC raw-data absolute-limits test (Vickers and Mahrt 1997)',
    'OUTLIER_MANUAL': 'manual removal of periods',
    'OUTLIER_ABSLIM': 'absolute-limits test',
    'OUTLIER_HAMPEL': 'Hampel outlier test',
    'OUTLIER_HAMPEL_2': 'second Hampel outlier test',
    'OUTLIER_NEGNIGHT': 'test for negative values at night',
    'OUTLIER_NEGNIGHTS': 'test for whole nights whose median lies clearly below zero',
    'USTAR': 'USTAR filter',
}
LEVELS = {
    'L2': 'Level 2 (quality tests)',
    'L3.1': 'Level 3.1 (storage correction)',
    'L3.2': 'Level 3.2 (outlier removal)',
    'L3.3': 'Level 3.3 (USTAR filter)',
}
GAPFILL = {'gfXG': 'gap-filled with XGBoost', 'gfMDS': 'gap-filled with MDS'}
UNC = {
    'RANDUNC': 'random uncertainty, 1 sigma (Pastorello et al. 2020)',
    'USTARUNC': 'USTAR uncertainty: half the difference between the CUT_84 and CUT_16 series',
    'JOINTUNC': 'joint uncertainty: random and USTAR uncertainty combined',
}


# Partitioning of NEE into GPP and RECO (ONEFlux methods in diive), one column per USTAR scenario.
PARTITIONING = {
    'NEE_NIGHT_OF': ('µmol m-2 s-1', 'Nighttime NEE used by the nighttime partitioning'),
    'RECO_NT_OF': ('µmol m-2 s-1', 'Ecosystem respiration, nighttime partitioning (Reichstein et al. 2005)'),
    'RECO_NT_OF_ROB': ('µmol m-2 s-1', 'Ecosystem respiration, nighttime partitioning, outlier-robust fit'),
    'GPP_NT_OF': ('µmol m-2 s-1', 'Gross primary production, nighttime partitioning (RECO_NT_OF minus NEE)'),
    'GPP_NT_OF_ROB': ('µmol m-2 s-1', 'Gross primary production, nighttime partitioning, outlier-robust fit'),
    'RREF_NT_OF': ('µmol m-2 s-1', 'Reference respiration of the Lloyd-Taylor fit, nighttime partitioning'),
    'E0_NT_OF': ('K', 'Temperature sensitivity of respiration (Lloyd-Taylor E0), nighttime partitioning'),
    'RECO_DT_OF': ('µmol m-2 s-1', 'Ecosystem respiration, daytime partitioning (Lasslop et al. 2010)'),
    'GPP_DT_OF': ('µmol m-2 s-1', 'Gross primary production, daytime partitioning (Lasslop et al. 2010)'),
    'SE_GPP_DT_OF': ('µmol m-2 s-1', 'Standard error of GPP_DT_OF'),
    'ALPHA_DT_OF': ('µmol J-1', 'Initial slope of the light response (light use efficiency), daytime partitioning'),
    'BETA_DT_OF': ('µmol m-2 s-1', 'CO2 uptake at light saturation, daytime partitioning'),
    'K_DT_OF': ('hPa-1', 'VPD sensitivity of the light response, daytime partitioning'),
    'RREF_DT_OF': ('µmol m-2 s-1', 'Reference respiration, daytime partitioning'),
    'E0_DT_OF': ('K', 'Temperature sensitivity of respiration (E0), daytime partitioning'),
}


def _scenario(cut):
    if cut is None:
        return ''
    if cut == 'NONE':
        return ', no USTAR threshold applied (CUT_NONE)'
    return f', USTAR scenario CUT_{cut} ({cut}th percentile threshold)'


def _describe_chain(name):
    if name in CHAIN:
        return CHAIN[name]
    m = re.fullmatch(r'(?P<var>[A-Z0-9_]+?)_CUT_(?P<cut>\d+)', name)
    if m and m.group('var') in PARTITIONING:
        unit, desc = PARTITIONING[m.group('var')]
        return unit, desc + _scenario(m.group('cut'))
    lvl = r'(?P<lvl>L2|L3\.1|L3\.2|L3\.3)'
    cut = r'(?:_CUT_(?P<cut>\d+|NONE))?'
    flux = r'(?P<flux>NEE|FC|LE|H)'
    # Test flag of one level.
    m = re.fullmatch(rf'FLAG_{lvl}{cut}_{flux}(?:_L3\.1(?:_QCF)?)?_(?P<test>.+)_TEST', name)
    if m and m.group('test') in TESTS:
        return DIMLESS, (f"{m.group('flux')}: flag of the {TESTS[m.group('test')]}, "
                         f"{LEVELS[m.group('lvl')]}{_scenario(m.group('cut'))} "
                         f"({'0 best, 1 medium, 2 rejected' if m.group('test') in ('SSITC', 'SCF') else '0 passed, 2 rejected'})")
    # Number of flags raised.
    m = re.fullmatch(rf'SUM_{lvl}{cut}_{flux}(?:_L3\.1)?_(?P<kind>HARDFLAGS|SOFTFLAGS|FLAGS)', name)
    if m:
        kind = {'HARDFLAGS': 'hard flags', 'SOFTFLAGS': 'soft flags', 'FLAGS': 'all flags'}[m.group('kind')]
        return DIMLESS, (f"{m.group('flux')}: sum of the {kind} of "
                         f"{LEVELS[m.group('lvl')]}{_scenario(m.group('cut'))}")
    # Overall quality flag of one level.
    m = re.fullmatch(rf'FLAG_{lvl}{cut}_{flux}(?:_L3\.1)?_QCF', name)
    if m:
        return DIMLESS, (f"{m.group('flux')}: overall quality flag of "
                         f"{LEVELS[m.group('lvl')]}{_scenario(m.group('cut'))} (0 best, 1 good, 2 rejected)")
    # Flux series of a level, quality-controlled, gap-filled, or its uncertainty.
    m = re.fullmatch(rf'(?P<flag>FLAG_)?(?P<flux>NEE|FC|LE|H|ET)_(?P<lvls>L[\d.]+(?:_L[\d.]+)?)'
                     rf'{cut}(?:_(?P<qcf>QCF0?))?(?:_(?P<gf>gfXG|gfMDS))?(?:_(?P<unc>RANDUNC|USTARUNC|JOINTUNC))?'
                     rf'(?P<filled>_ISFILLED)?', name)
    if m:
        unit, desc = CHAIN_FLUXES[m.group('flux')]
        last = m.group('lvls').split('_')[-1]
        parts = [f'{desc} after {LEVELS[last]}{_scenario(m.group("cut"))}']
        if m.group('qcf') == 'QCF':
            parts.append('from the records with quality flag 0 or 1')
        elif m.group('qcf') == 'QCF0':
            parts.append('from the records with quality flag 0 only')
        if m.group('gf') and m.group('flux') == 'ET':
            parts.append(f"computed from LE {GAPFILL[m.group('gf')]}")
        elif m.group('gf'):
            parts.append(GAPFILL[m.group('gf')])
        if m.group('flux') == 'NEE' and m.group('lvls') == 'L3.1' and not m.group('qcf'):
            parts = ['Net ecosystem exchange of CO2: FC plus the gap-filled storage term, Level 3.1']
        if m.group('flux') in ('LE', 'H') and m.group('lvls') == 'L3.1' and not m.group('qcf'):
            parts = [f'{desc}, Level 3.1 (storage term set to zero)']
        if m.group('filled'):
            if not (m.group('flag') and m.group('gf')):
                return None
            return DIMLESS, f"Gap-filling flag of {name[5:-9]} (0 = measured, otherwise filled)"
        if m.group('flag'):
            return None
        if m.group('unc'):
            text = UNC[m.group('unc')]
            return unit, f"{text[0].upper() + text[1:]}, of {name[:-len(m.group('unc')) - 1]}"
        return unit, ', '.join(parts)
    return None


# --- Open-path correction of the LI-7500 CO2 flux (opco, Level 1.1) ----------------------------

OPCO = {
    'FC_L1.1_OPCO': ('µmol m-2 s-1', 'CO2 flux of the LI-7500 corrected with opco: FC minus BIAS_OPCO'),
    'BIAS_OPCO': ('µmol m-2 s-1', 'opco: bias of the LI-7500 CO2 flux (measured minus true flux), '
                                  'BIAS_HEAT_OPCO plus BIAS_WPL_H_OPCO'),
    'BIAS_HEAT_OPCO': ('µmol m-2 s-1', 'opco: heating part of the bias, XI_OPCO times HEAT_OPCO'),
    'BIAS_WPL_H_OPCO': ('µmol m-2 s-1', 'opco: H part of the bias, K_OPCO times WPL_H_OPCO'),
    'HEAT_OPCO': ('µmol m-2 s-1', 'opco: heating term of the LI-7500 head, unscaled'),
    'WPL_H_OPCO': ('µmol m-2 s-1', 'opco: WPL thermal term, from H'),
    'XI_OPCO': (DIMLESS, 'opco: coefficient of the heating term'),
    'K_OPCO': (DIMLESS, 'opco: coefficient of the WPL thermal term'),
    'K_OP_OPCO': (DIMLESS, 'opco: weekly detector of the switching error, the slope of the nighttime '
                           'LI-7500 flux on the WPL thermal term'),
    'OUT_OF_ENVELOPE_OPCO': (DIMLESS, 'opco: TA, USTAR or the WPL thermal term outside the range of the '
                                      'training data (True = extrapolated)'),
}


def _describe_opco(name):
    return OPCO.get(name)


def describe(name):
    """Return (unit, description) of a column, or None if it is not known."""
    for f in (_describe_opco, _describe_chain, _describe_meteo, _describe_l1):
        r = f(name)
        if r is not None:
            return r
    return None


def describe_all(columns):
    """Return {column: (unit, description)} for all columns; fail on any that is not described."""
    out = {c: describe(c) for c in columns}
    missing = [c for c, r in out.items() if r is None]
    assert not missing, f"no description for {len(missing)} columns: {missing}"
    return out


def info_section(title, columns, described):
    """Markdown lines of one source in an _INFO.md file: a table of variable, unit and description."""
    lines = ["", f"## {title} ({len(columns)} variables)", "", "| variable | unit | description |", "|---|---|---|"]
    lines += [f"| `{c}` | {described[c][0]} | {described[c][1]} |" for c in columns]
    return lines
