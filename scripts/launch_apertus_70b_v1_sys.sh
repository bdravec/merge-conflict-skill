#!/usr/bin/env bash
# Launcher for the Apertus-70B fp8 v1 run on python-tiny (refs #83, #75).
#
# Large-pair sibling to the Qwen3-32B v1 run: produces no-skill + skill-v1-sys
# rows so Apertus has its OWN no-skill baseline on ConGra (mirrors the 32B
# v1_sys_plus_baseline file). The 'user' condition is dropped per the large-pair
# convention. Later versions (v2/v2.1), if run, reuse this no-skill baseline.
#
# Prereqs (RTX 6000 96GB box, #75): vLLM serving Apertus-70B fp8 on :8000, e.g.
#   export HF_HUB_OFFLINE=1
#   vllm serve swiss-ai/Apertus-70B-Instruct-2509 \
#     --port 8000 --quantization fp8 --max-model-len 32768 --gpu-memory-utilization 0.92
#
# Run from a separate shell (tmux), with the vLLM venv on PATH:
#   tmux new -s apertus70
#   bash scripts/launch_apertus_70b_v1_sys.sh
# Detach with Ctrl-b d; reattach with tmux attach -t apertus70.
#
# Tunables (env overrides): CONC (client concurrency), VENV (virtualenv path).
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${VENV:-$HOME/vllm-env}"
CONC="${CONC:-16}"
MAX_PROMPT_TOKENS=30720       # leaves room under --max-model-len 32768 for 2048 output
TAG="v1_python_tiny"          # output holds both no-skill baseline + skill-v1-sys
LOG="$REPO/scripts/results/pilot_run_apertus-70b_${TAG}.log"

cd "$REPO"
# shellcheck disable=SC1091
[ -f "$VENV/bin/activate" ] && source "$VENV/bin/activate"
export HF_HUB_OFFLINE=1       # tokenizer is cached; no HF network calls

# Wait for vLLM to answer (max 5 min)
ready=0
for _ in $(seq 1 60); do
  if curl -s -m 2 http://localhost:8000/v1/models > /dev/null 2>&1; then
    echo "vllm ready at $(date)"; ready=1; break
  fi
  sleep 5
done
if [ "$ready" = "0" ]; then
  echo "ERROR: vllm not ready after 5 min, aborting" >&2; exit 1
fi

echo "=== apertus-70b v1 (no-skill+sys) start $(date) -> $LOG ==="
python -u scripts/pilot.py \
  --model apertus-70b \
  --skill-version v1 \
  --conditions no-skill,sys \
  --bucket all \
  --n-cases all \
  --tag "$TAG" \
  --concurrency "$CONC" \
  --max-prompt-tokens "$MAX_PROMPT_TOKENS" \
  > "$LOG" 2>&1
rc=$?
echo "=== apertus-70b v1 (no-skill+sys) end rc=$rc $(date) -> $LOG ==="
echo "jsonl: $REPO/scripts/results/pilot_results_apertus-70b_${TAG}.jsonl"
exit $rc
