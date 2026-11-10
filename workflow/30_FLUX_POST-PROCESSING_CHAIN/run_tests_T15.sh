#!/usr/bin/env bash
# Runs test T15 of 10 Nov 2026 in place, one notebook after the other (plan item 25):
#   T15  IRGA75/01 and 05 with the daytime heating part of opco scaled by 0.6 before 2008, unchanged from 2008
# then the comparison notebook TESTS_T15_COMPARISON_2026-11-10.ipynb.
# The test writes its own output files, named after its notebooks, so no product file is overwritten.
# Logs go to the external data folder.
#
# Usage, from Git Bash:  bash workflow/30_FLUX_POST-PROCESSING_CHAIN/run_tests_T15.sh
STAGE=/f/dev/datasets/dataset_ch-lae_flux_product/workflow/30_FLUX_POST-PROCESSING_CHAIN
PY=/f/dev/datasets/dataset_ch-lae_flux_product/.venv/Scripts/python.exe
LOG=/f/Sync/luhk_work/dev-data/datasets-data/dataset_ch-lae_flux_product-data/workflow/30_FLUX_POST-PROCESSING_CHAIN/_logs_T15
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
if run IRGA75 T15_01_FPPC_IRGA75_OPEN-PATH_CORRECTION_HEATDAYEARLY06_2004-2017_2019; then
  run IRGA75 T15_05_FPPC_IRGA75_NEE_OPCO_HEATDAYEARLY06_2004-2017
else
  echo "skipped T15_05 (its 01 failed)" | tee -a "$SUMMARY"
fi
run . TESTS_T15_COMPARISON_2026-11-10
echo "=== run finished $(date '+%Y-%m-%d %H:%M') ===" | tee -a "$SUMMARY"
