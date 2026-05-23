#!/usr/bin/env bash
# Chain wrapper: run text, text+func, text+sytx+func sequentially (refs #63).
# Launch under nohup so it survives shell exit:
#   nohup bash scripts/chain_qwen3_v1_remaining.sh > /dev/null 2>&1 &
#   disown
set -uo pipefail  # NOT -e — a failed bucket should not abort the chain

cd /home/baebs/thesis/merge-conflict-skill
source /home/baebs/thesis/vllm-env/bin/activate
export HF_HUB_OFFLINE=1

RESULTS=/home/baebs/thesis/merge-conflict-skill/scripts/results
CHAIN_LOG=$RESULTS/chain_qwen3_v1_remaining.log

echo "=== chain start $(date) ===" > "$CHAIN_LOG"
echo "PID=$$" >> "$CHAIN_LOG"

# Wait for vLLM to be ready (max 5 min)
ready=0
for i in $(seq 1 60); do
  if curl -s -m 2 http://localhost:8000/v1/models > /dev/null 2>&1; then
    echo "vllm ready at $(date)" >> "$CHAIN_LOG"
    ready=1
    break
  fi
  sleep 5
done
if [ "$ready" = "0" ]; then
  echo "ERROR: vllm not ready after 5 min, aborting" >> "$CHAIN_LOG"
  exit 1
fi

run_bucket() {
  local bucket="$1"
  local tag="v1_python_tiny_c2_${bucket}"
  local log="$RESULTS/pilot_run_qwen3_v1_python_tiny_c2_${bucket}.log"
  echo "=== bucket=$bucket start $(date) ===" >> "$CHAIN_LOG"
  python -u scripts/pilot.py \
    --model qwen3 \
    --skill-version v1 \
    --bucket "$bucket" \
    --n-cases all \
    --tag "$tag" \
    --concurrency 2 \
    --max-prompt-tokens 30720 \
    > "$log" 2>&1
  local rc=$?
  echo "=== bucket=$bucket end rc=$rc $(date) ===" >> "$CHAIN_LOG"
}

for bucket in text text+func text+sytx+func; do
  run_bucket "$bucket"
done

echo "=== chain done $(date) ===" >> "$CHAIN_LOG"
