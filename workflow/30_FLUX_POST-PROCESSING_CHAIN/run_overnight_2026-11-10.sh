#!/usr/bin/env bash
# Overnight run of 10 Nov 2026 (plan item 25, PLAN.md section 5 steps 1-3):
#   1. copy the product files of 4 Nov 2026 (opco heat scale 1) into _product_2026-11-04/ beside each
#   2. rerun the IRGA75 chain with IRGA75/01 version 3 (daytime heat scale 0.6 before 2008):
#      IRGA75/01 -> IRGA75/05 -> IRGA75/99 -> 99_FPPC_MERGED -> 80_FINALIZE/10
#   3. the IRGA75 overview notebooks in 90_OVERVIEW
#   4. test T16 (scale 0.4) and the comparison notebook TESTS_T16_COMPARISON_2026-11-10
#   5. beside 2-4: the raw-data statistics of the periods A-D (2008-2012) and the raw-data analysis,
#      which reads the copy of the 4 Nov 01 file, so its opco columns stay those of scale 1
# A failed notebook stops only the steps that depend on it. Logs go to the external data folder.
#
# Usage, from Git Bash:  bash workflow/30_FLUX_POST-PROCESSING_CHAIN/run_overnight_2026-11-10.sh
#                        DRYRUN=1 bash ...   only checks that every notebook and input exists
REPO=/f/dev/datasets/dataset_ch-lae_flux_product
WF=$REPO/workflow
PY=$REPO/.venv/Scripts/python.exe
DATA=/f/Sync/luhk_work/dev-data/datasets-data/dataset_ch-lae_flux_product-data
DWF=$DATA/workflow
RAW=$DATA/research/reports/raw_hf_2026-11-09
LOG=$DWF/30_FLUX_POST-PROCESSING_CHAIN/_logs_overnight_2026-11-10
BK=_product_2026-11-04
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

backup() {  # backup <data folder under workflow> <file>; never overwrites an existing copy
  local dir=$DWF/$1 f=$2
  if [ ! -f "$dir/$f" ]; then say "MISSING data file $1/$f"; FAILED=1; return 1; fi
  if [ -n "$DRYRUN" ]; then say "dry run: copy $1/$f"; return 0; fi
  mkdir -p "$dir/$BK"
  if [ -f "$dir/$BK/$f" ]; then say "copy exists: $1/$BK/$f"; return 0; fi
  cp -p "$dir/$f" "$dir/$BK/$f" && say "copied $1/$f to $BK/"
}

raw() {  # the raw-data part, run in the background beside the chain
  local F75=$DWF/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/$BK/01_FPPC_IRGA75_OPEN-PATH_CORRECTION_2004-2017_2019.parquet
  if [ -n "$DRYRUN" ]; then say "dry run: raw statistics 2008_1+4 2009 2010 2011 2012, then hf_analyse --tag _ext"; return 0; fi
  say "start raw statistics of the periods A-D"
  ( cd "$RAW" && PYTHONUTF8=1 "$PY" hf_run.py --datasets 2008_1+4 2009 2010 2011 2012 --workers 6 --out out \
      > "$LOG/raw_hf_run.log" 2>&1 )
  say "end   raw statistics exit $?"
  ( cd "$RAW" && HF_F75="$F75" PYTHONUTF8=1 "$PY" -W ignore hf_analyse.py --out out --tag _ext \
      > "$LOG/raw_hf_analyse.log" 2>&1 )
  say "end   raw analysis exit $? (results_out_ext)"
}

say "=== run started${DRYRUN:+ (dry run)} ==="
C=30_FLUX_POST-PROCESSING_CHAIN
backup $C/IRGA75 01_FPPC_IRGA75_OPEN-PATH_CORRECTION_2004-2017_2019.parquet
backup $C/IRGA75 05_FPPC_IRGA75_NEE_OPCO_2004-2017.parquet
backup $C/IRGA75 99_FPPC_IRGA75_MERGED_2004-2017.parquet
backup $C 99_FPPC_MERGED_2004-2026.09.parquet
backup 80_FINALIZE 10_FLUXES_and_METEO_2004-2026.09.parquet
if [ $FAILED -ne 0 ] && [ -z "$DRYRUN" ]; then say "a copy failed: nothing is rerun"; exit 1; fi

raw &
RAWPID=$!

if run $C/IRGA75 01_FPPC_IRGA75_OPEN-PATH_CORRECTION_2004-2017_2019 \
   && run $C/IRGA75 05_FPPC_IRGA75_NEE_OPCO_2004-2017 \
   && run $C/IRGA75 99_FPPC_IRGA75_MERGED_2004-2017 \
   && run $C 99_FPPC_MERGED_2004-2026.09; then
  run 80_FINALIZE 10_FLUXES_and_METEO_2004-2026.09
  for nb in FLUX_NEE FLUX_GPP FLUX_RECO FLUX_NEE_IRGA75_COMPARISONS FLUX_NEE_IRGA75_EVALUATION \
            FLUX_NEE_IRGA75_INDEPENDENT_ESTIMATES FLUX_NEE_IRGA75_PARTITIONING_COMPARISON; do
    run 90_OVERVIEW $nb
  done
else
  say "chain rerun stopped: 80_FINALIZE and the overviews are not run"
fi

if run $C/IRGA75 T16_01_FPPC_IRGA75_OPEN-PATH_CORRECTION_HEATDAYEARLY04_2004-2017_2019; then
  run $C/IRGA75 T16_05_FPPC_IRGA75_NEE_OPCO_HEATDAYEARLY04_2004-2017
fi
run $C TESTS_T16_COMPARISON_2026-11-10

wait $RAWPID
say "=== run finished, $( [ $FAILED -eq 0 ] && echo 'no failure' || echo 'with failures, see the logs' ) ==="
