#!/usr/bin/env bash
# Tests of a radiation-dependent daytime heat scale, 15 Nov 2026 (PLAN.md section 5):
#   T24  daytime heating part of opco scaled by s(SW_IN) = clip(0.90 - 0.86 SW_IN/500, 0, 1) before 2008
#   T25  the same before 2016
# Each test runs its 01 notebook, then its 05 notebook on that output.
# then the comparison notebook TESTS_T24-T25_COMPARISON_2026-11-15. The 05 notebooks read their own 01 output.
# The tests run one after another; a failed test does not stop the others. Logs go to the external
# data folder.
#
# Usage, from Git Bash:  bash workflow/30_FLUX_POST-PROCESSING_CHAIN/run_tests_T24-T25.sh
#                        DRYRUN=1 bash ...   only checks that every notebook and input exists
REPO=/f/dev/datasets/dataset_ch-lae_flux_product
WF=$REPO/workflow
PY=$REPO/.venv/Scripts/python.exe
DWF=/f/Sync/luhk_work/dev-data/datasets-data/dataset_ch-lae_flux_product-data/workflow
LOG=$DWF/30_FLUX_POST-PROCESSING_CHAIN/_logs_tests_T24-T25
mkdir -p "$LOG"
SUMMARY="$LOG/summary.log"
FAILED=0

say() { echo "$(date '+%Y-%m-%d %H:%M') $*" | tee -a "$SUMMARY"; }

run() {  # run <folder under workflow> <notebook stem>
  local dir=$1 stem=$2
  if [ ! -f "$WF/$dir/$stem.ipynb" ]; then say "MISSING notebook $dir/$stem"; FAILED=1; return 1; fi
  if [ -n "$DRYRUN" ]; then say "dry run: $dir/$stem"; return 0; fi
  say "start $dir/$stem"
  ( cd "$WF/$dir" && PYTHONUTF8=1 "$PY" -m jupyter nbconvert --to notebook --execute --inplace \
      --ExecutePreprocessor.timeout=-1 --ExecutePreprocessor.kernel_name=python3 "$stem.ipynb" \
      > "$LOG/$(basename "$stem").log" 2>&1 )
  local rc=$?
  say "end   $dir/$stem exit $rc"
  [ $rc -ne 0 ] && FAILED=1
  return $rc
}

need() {  # need <file under the data workflow folder>
  if [ ! -f "$DWF/$1" ]; then say "MISSING data file $1"; FAILED=1; fi
}

say "=== run started${DRYRUN:+ (dry run)} ==="
C=30_FLUX_POST-PROCESSING_CHAIN
need $C/IRGA75/01_FPPC_IRGA75_OPEN-PATH_CORRECTION_2004-2017_2019.parquet
need $C/IRGA75/00_FPPC_IRGA75_INPUT_noSHC_2004-2017_2019.parquet
need $C/IRGA75/05_FPPC_IRGA75_NEE_OPCO_2004-2017.parquet
need $C/IRGA75/T16_05_FPPC_IRGA75_NEE_OPCO_HEATDAYEARLY04_2004-2017.parquet
need $C/IRGA72/05_FPPC_IRGA72_NEE_2016-2026.09.parquet
if [ $FAILED -ne 0 ] && [ -z "$DRYRUN" ]; then say "an input is missing: nothing is run"; exit 1; fi

run $C/IRGA75 T24_01_FPPC_IRGA75_OPEN-PATH_CORRECTION_HEATDAYRAD2008_2004-2017_2019
run $C/IRGA75 T24_05_FPPC_IRGA75_NEE_OPCO_HEATDAYRAD2008_2004-2017
run $C/IRGA75 T25_01_FPPC_IRGA75_OPEN-PATH_CORRECTION_HEATDAYRAD2016_2004-2017_2019
run $C/IRGA75 T25_05_FPPC_IRGA75_NEE_OPCO_HEATDAYRAD2016_2004-2017
run $C TESTS_T24-T25_COMPARISON_2026-11-15

say "=== run finished, $( [ $FAILED -eq 0 ] && echo 'no failure' || echo 'with failures, see the logs' ) ==="
