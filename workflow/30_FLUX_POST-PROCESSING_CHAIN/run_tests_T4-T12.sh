#!/usr/bin/env bash
# Runs the overnight tests T4-T12 of 6 Nov 2026 in place, one after the other, in order of priority:
#   T4-T6   IRGA75/01 and 05 with the daytime heating part of opco scaled by 0.84, 0.5 and 0
#   T7-T8   IRGA75/05 with random seeds 1 and 2 of the gap-filling models
#   T9-T10  IRGA72/05 with random seeds 1 and 2
#   T11-T12 IRGA75/05 with 50 and 200 trees in every gap-filling model
# A failed test does not stop the run; the 05 notebook of a heat test is skipped when its 01 failed.
# Each test writes its own output file, named after its notebook, so no product file is overwritten.
# Logs go to the external data folder. Compare the results with TESTS_T4-T12_COMPARISON_2026-11-06.ipynb.
#
# Usage, from Git Bash:  bash workflow/30_FLUX_POST-PROCESSING_CHAIN/run_tests_T4-T12.sh
STAGE=/f/dev/datasets/dataset_ch-lae_flux_product/workflow/30_FLUX_POST-PROCESSING_CHAIN
PY=/f/dev/datasets/dataset_ch-lae_flux_product/.venv/Scripts/python.exe
LOG=/f/Sync/luhk_work/dev-data/datasets-data/dataset_ch-lae_flux_product-data/workflow/30_FLUX_POST-PROCESSING_CHAIN/_logs_T4-T12
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
for spec in "4 HEATDAY084" "5 HEATDAY050" "6 HEATDAY000"; do
  set -- $spec
  if run IRGA75 "T$1_01_FPPC_IRGA75_OPEN-PATH_CORRECTION_$2_2004-2017_2019"; then
    run IRGA75 "T$1_05_FPPC_IRGA75_NEE_OPCO_$2_2004-2017"
  else
    echo "skipped T$1_05 (its 01 failed)" | tee -a "$SUMMARY"
  fi
done
run IRGA75 T7_05_FPPC_IRGA75_NEE_OPCO_SEED1_2004-2017
run IRGA75 T8_05_FPPC_IRGA75_NEE_OPCO_SEED2_2004-2017
run IRGA72 T9_05_FPPC_IRGA72_NEE_SEED1_2016-2026.09
run IRGA72 T10_05_FPPC_IRGA72_NEE_SEED2_2016-2026.09
run IRGA75 T11_05_FPPC_IRGA75_NEE_OPCO_TREES50_2004-2017
run IRGA75 T12_05_FPPC_IRGA75_NEE_OPCO_TREES200_2004-2017
echo "=== run finished $(date '+%Y-%m-%d %H:%M') ===" | tee -a "$SUMMARY"
