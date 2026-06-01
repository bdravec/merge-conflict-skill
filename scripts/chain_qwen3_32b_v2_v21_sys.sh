#!/usr/bin/env bash
# Chain: run qwen3-32B v2 then v2.1, sys-condition only, sequentially (refs #75, #81).
#
# Sys-only + reuse-v1-no-skill: each version produces only skill-{v}-sys rows;
# the no-skill baseline is reused from the v1 run at analysis time (recomputing
# would inject temperature=0 batch-nondeterminism drift between versions).
#
# Run inside tmux, with the vLLM venv on PATH:
#   tmux new -s v2chain
#   source ~/vllm-env/bin/activate        # or: VENV=/path/to/venv
#   bash scripts/chain_qwen3_32b_v2_v21_sys.sh
# Detach with Ctrl-b d; reattach with tmux attach -t v2chain.
#
# Tunables (env overrides): CONC (client concurrency), VENV (virtualenv path).
set -uo pipefail  # NOT -e — a failed version must not abort the chain

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${VENV:-$HOME/vllm-env}"
CONC="${CONC:-16}"
MAX_PROMPT_TOKENS=30720       # leaves room under --max-model-len 32768 for 2048 output
RESULTS="$REPO/scripts/results"
CHAIN_LOG="$RESULTS/chain_qwen3_32b_v2_v21_sys.log"

cd "$REPO"
# shellcheck disable=SC1091
[ -f "$VENV/bin/activate" ] && source "$VENV/bin/activate"
export HF_HUB_OFFLINE=1       # tokenizer is cached; no HF network calls

echo "=== chain start $(date) ===" | tee "$CHAIN_LOG"
echo "PID=$$ REPO=$REPO VENV=$VENV CONC=$CONC" | tee -a "$CHAIN_LOG"

# Wait for vLLM to answer (max 5 min)
ready=0
for _ in $(seq 1 60); do
  if curl -s -m 2 http://localhost:8000/v1/models > /dev/null 2>&1; then
    echo "vllm ready at $(date)" | tee -a "$CHAIN_LOG"; ready=1; break
  fi
  sleep 5
done
if [ "$ready" = "0" ]; then
  echo "ERROR: vllm not ready after 5 min, aborting" | tee -a "$CHAIN_LOG"; exit 1
fi

run_version() {
  local ver="$1"
  local tag="${ver}_python_tiny_sys"
  local log="$RESULTS/pilot_run_qwen3-32b_${tag}.log"
  echo "=== ${ver} (sys) start $(date) ===" | tee -a "$CHAIN_LOG"
  python -u scripts/pilot.py \
    --model qwen3-32b \
    --skill-version "$ver" \
    --conditions sys \
    --bucket all \
    --n-cases all \
    --tag "$tag" \
    --concurrency "$CONC" \
    --max-prompt-tokens "$MAX_PROMPT_TOKENS" \
    > "$log" 2>&1
  local rc=$?
  echo "=== ${ver} (sys) end rc=$rc $(date) -> $log ===" | tee -a "$CHAIN_LOG"
}

for ver in v2 v2.1; do
  run_version "$ver"
done

echo "=== chain done $(date) ===" | tee -a "$CHAIN_LOG"
