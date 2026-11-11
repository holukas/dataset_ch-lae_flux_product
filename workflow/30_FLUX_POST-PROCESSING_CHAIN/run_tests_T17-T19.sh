#!/usr/bin/env bash
# Night tests of the too-low LI-7500 nights, 11 Nov 2026 (PLAN.md section 5, step 4):
#   T17  wet-night fill raised by its offset to the LI-7200 in the parallel period
#   T18  every night fill raised by the offset of its fill flag
#   T19  measured cold nights with a wet window or an overcast sky removed before gap-filling
# then the comparison notebook TESTS_T17-T19_COMPARISON_2026-11-11. All read the product IRGA75/01.
# The tests run one after another; a failed test does not stop the others. Logs go to the external
# data folder.
#
# Usage, from Git Bash:  bash workflow/30_FLUX_POST-PROCESSING_CHAIN/run_tests_T17-T19.sh
#                        DRYRUN=1 bash ...   only checks that every notebook and input exists
REPO=/f/dev/datasets/dataset_ch-lae_flux_product
WF=$REPO/workflow
PY=$REPO/.venv/Scripts/python.exe
DWF=/f/Sync/luhk_work/dev-data/datasets-data/dataset_ch-lae_flux_product-data/workflow
LOG=$DWF/30_FLUX_POST-PROCESSING_CHAIN/_logs_tests_T17-T19
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
need $C/IRGA75/05_FPPC_IRGA75_NEE_OPCO_2004-2017.parquet
need $C/IRGA72/05_FPPC_IRGA72_NEE_2016-2026.09.parquet
if [ $FAILED -ne 0 ] && [ -z "$DRYRUN" ]; then say "an input is missing: nothing is run"; exit 1; fi

run $C/IRGA75 T17_05_FPPC_IRGA75_NEE_OPCO_NIGHTOFFSETWN_2004-2017
run $C/IRGA75 T18_05_FPPC_IRGA75_NEE_OPCO_NIGHTOFFSETALL_2004-2017
run $C/IRGA75 T19_05_FPPC_IRGA75_NEE_OPCO_COLDWETSCREEN_2004-2017
run $C TESTS_T17-T19_COMPARISON_2026-11-11

say "=== run finished, $( [ $FAILED -eq 0 ] && echo 'no failure' || echo 'with failures, see the logs' ) ==="
