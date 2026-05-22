#!/usr/bin/env bash
# Launcher for the Qwen3 v1 c=2 per-bucket rerun (refs #63).
# Usage: bash scripts/launch_qwen3_v1_rerun.sh <bucket>
# where <bucket> is one of: text+sytx | text | text+func | text+sytx+func
set -euo pipefail

BUCKET="${1:?Usage: $0 <text+sytx|text|text+func|text+sytx+func>}"

case "$BUCKET" in
    text+sytx|text|text+func|text+sytx+func) ;;
    *) echo "unknown bucket: $BUCKET" >&2; exit 1 ;;
esac

REPO="$(cd "$(dirname "$0")/.." && pwd)"
TAG="v1_python_tiny_c2_${BUCKET}"
LOG="$REPO/scripts/results/pilot_run_qwen3_v1_python_tiny_c2_${BUCKET}.log"

cd "$REPO"
source /home/baebs/thesis/vllm-env/bin/activate

nohup python -u scripts/pilot.py \
    --model qwen3 \
    --skill-version v1 \
    --bucket "$BUCKET" \
    --n-cases all \
    --tag "$TAG" \
    --concurrency 2 \
    --max-prompt-tokens 30720 \
    > "$LOG" 2>&1 &

PID=$!
echo "launched pilot.py for bucket=$BUCKET, pid=$PID"
echo "log: $LOG"
echo "jsonl: $REPO/scripts/results/pilot_results_qwen3_${TAG}.jsonl"
