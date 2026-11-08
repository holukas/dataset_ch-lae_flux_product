#!/usr/bin/env bash
# Runs the overnight tests T13-T14 of 8 Nov 2026 in place, one after the other (plan item 25):
#   T13  IRGA75/01 and 05 with the daytime heating part of opco scaled by 0.76 before 2008, 0.84 from 2008
#   T14  IRGA75/01 and 05 with the daytime CO2 covariance of 2004-2007 scaled up to the 2016-2017 level
# then the comparison notebook TESTS_T13-T14_COMPARISON_2026-11-08.ipynb.
# A failed test does not stop the run; the 05 notebook of a test is skipped when its 01 failed.
# Each test writes its own output file, named after its notebook, so no product file is overwritten.
# Logs go to the external data folder.
#
# Usage, from Git Bash:  bash workflow/30_FLUX_POST-PROCESSING_CHAIN/run_tests_T13-T14.sh
STAGE=/f/dev/datasets/dataset_ch-lae_flux_product/workflow/30_FLUX_POST-PROCESSING_CHAIN
PY=/f/dev/datasets/dataset_ch-lae_flux_product/.venv/Scripts/python.exe
LOG=/f/Sync/luhk_work/dev-data/datasets-data/dataset_ch-lae_flux_product-data/workflow/30_FLUX_POST-PROCESSING_CHAIN/_logs_T13-T14
mkdir -p "$LOG"
SUMMARY="$LOG/summary.log"

run() {  # run <folder> <notebook stem>; returns the exit code of nbconvert
  local dir=$1 stem=$2
  echo "$(date '+%Y-%m-%d %H:%M') start $stem" | tee -a "$SUMMARY"
  ( cd "$STAGE/$dir" && PYTHONUTF8=1 "$PY" -m jupyter nbconvert --to notebook --execute --inplace \
      --ExecutePreprocessor.timeout=-1 --ExecutePreprocessor.kernel_name=python3 "$stem.ipynb" \
      > "$LOG/$stem.log" 2>&1 )
  local rc=$?
  echo "$(date '+%Y-%m-%d %H:%M') end   $stem exit $rc" | tee -a "$SUMMARY"
  return $rc
}

echo "=== run started $(date '+%Y-%m-%d %H:%M') ===" | tee -a "$SUMMARY"
for spec in "13 HEATDAYPERIOD" "14 COVGAIN"; do
  set -- $spec
  if run IRGA75 "T$1_01_FPPC_IRGA75_OPEN-PATH_CORRECTION_$2_2004-2017_2019"; then
    run IRGA75 "T$1_05_FPPC_IRGA75_NEE_OPCO_$2_2004-2017"
  else
    echo "skipped T$1_05 (its 01 failed)" | tee -a "$SUMMARY"
  fi
done
run . TESTS_T13-T14_COMPARISON_2026-11-08
echo "=== run finished $(date '+%Y-%m-%d %H:%M') ===" | tee -a "$SUMMARY"
