# UBELIX notes

Living reference for thesis work on the University of Bern HPC cluster (UBELIX). Built up as we learn the environment.

Umbrella issue: [#3](https://github.com/bdravec/merge-conflict-skill/issues/3) (cluster access). Setup tracker: [#72](https://github.com/bdravec/merge-conflict-skill/issues/72).

---

## 1. Access

- **Username:** `bd00p079`
- **SSH:** `ssh <username>@submit[01-04].unibe.ch` — four submit hosts, pick any. SSH config alias `ubelix` set up on Barbara's Macbook (2026-05-26).
- **OnDemand portal:** https://ondemand.hpc.unibe.ch (browser-based)
- **Network requirement:** must be on Unibe network or university VPN to reach SSH or OnDemand.
- **Docs:** https://www.ubelix.hpc.unibe.ch/docs
- **Support boundaries:**
  - UBELIX HPC team → infra issues only (servicedesk@unibe.ch, https://serviceportal.unibe.ch/esc)
  - Data Science Lab (DSL, https://dsl.unibe.ch) → ML/data-science help

## 2. Filesystem

- **Home:** `/storage/homefs/bd00p079` — on GPFS (`rs_gpfs`), parallel filesystem shared across users.
- **Total GPFS capacity:** 350 TB cluster-wide, ~83% used (cluster-wide, not per-user).
- **Quotas** (per [official docs](https://hpc-unibe-ch.github.io/storage/quota/)):

  | Storage | Quota | Backup | Use |
  |---|---|---|---|
  | `$HOME` | **1 TB / 1M files** | Yes | Personal files, lifetime |
  | Workspace (project storage) | min 5 TB / 1M files per TB | Yes | Project-based, expandable on request |
  | Capacity Storage | min 50 TB / 100K files per TB | No | Large-scale |
  | Network Scratch (`/scratch`) | 15 TB / 10M files | No | 30-day retention |
  | Local Scratch | <1 TB per node | No | Job-local, deleted after job |

  Check own usage with `quota` (not `quota -s` — that flag fails). Modifying access times to bypass scratch retention is prohibited.

- **Workspace mechanism:** `module load Workspace` requires `HPC_WORKSPACE=<name>` env var first. As of 2026-05-27, no R/W workspaces allocated to Barbara; read-only DSL shares `dsl_shared` and `dsl_vibe_rs` are visible. Not needed for the 8B/32B/70B-pair work — fits in `$HOME`.

- **Local node storage:** `/tmp` and `/` each 20 GB per node — not for persistent data.

- **Verified quotas for `bd00p079` (2026-05-27):**
  - `HOME` 1 TB / 1M files, 0 GB used, 18 files used
  - `SCR_usr` (personal scratch) **30 TB**, 0 GB used (larger than the 15 TB the docs advertise)

- **Decision (2026-05-27):** put **everything in `$HOME`** for thesis work. 1 TB easily handles 210 GB model weights + ConGra data + venvs + code; backed up; persistent. `SCR_usr` available as fallback for very large temporary artefacts.

## 3. Modules

No modules loaded by default on login. Default `python3` is **3.9.25**.

**CUDA:**
- CUDA/11.8.0, 12.1.1, 12.2.0, 12.3.0, **12.6.0 (default)**, 12.8.0
- NVHPC bundles: NVHPC/23.7-CUDA-12.1.1, NVHPC/24.11-CUDA-12.6.0 (default), NVHPC/25.3-CUDA-12.8.0

**cuDNN:**
- cuDNN/8.7.0.84-CUDA-11.8.0
- cuDNN/8.9.2.26-CUDA-12.1.1
- cuDNN/8.9.2.26-CUDA-12.2.0
- cuDNN/8.9.7.29-CUDA-12.3.0
- **cuDNN/9.5.0.50-CUDA-12.6.0 (default)**
- cuDNN/9.10.1.4-CUDA-12.8.0

**Python:**
- Python/3.10.4-GCCcore-11.3.0
- Python/3.10.8-GCCcore-12.2.0-bare
- Python/3.11.3-GCCcore-12.3.0
- Anaconda3/2022.05, 2023.09-0, **2024.02-1 (default)**

**Compilers:** GCC up to 14.2.0; LLVM up to 20.1.7; Intel compilers up to 2024.2.0.

**Recommended toolchain for vLLM:** `CUDA/12.6.0 + cuDNN/9.5.0.50 + Python/3.11.3`. Modern enough for current vLLM, matches default CUDA on the cluster.

## 4. SLURM partitions + GPUs

| Partition | Nodes | GPU | Per-node count | Per-GPU VRAM | Notes |
|---|---|---|---|---|---|
| `epyc2*` (default) | 61 | none | — | — | CPU-only AMD EPYC |
| `bdw` | 65 | none | — | — | CPU-only Broadwell |
| `gpu` | 3 | RTX 3090 | 8 | 24 GB | consumer, PCIe |
| `gpu` | 10 | RTX 4090 | 8 | 24 GB | consumer, PCIe |
| `gpu` | 1 | A100 | 6 | likely 80 GB | datacenter |
| `gpu` | **5** | **H100** | **8** | **80 GB** | **datacenter, primary target** |
| `gpu` | 1 | H200 | 8 | 141 GB | newest, highest VRAM |
| `gpu-invest` | mirrors `gpu` + gnode38 | RTX Pro 6000 Blackwell (MIG 1g.24gb) | 16 slices | 24 GB | per-share allocation |
| `teaching` | mirrors `gpu` + 156 CPU nodes | various | — | — | teaching-priority queue |

Top H100/H200 nodes: `gnode25-28,34,36`. A100 node: `gnode21`.

**Sizing for 70B-class models (fp16):**

| Model | Weights | Recommended | Partition flag |
|---|---|---|---|
| Qwen3-32B | ~64 GB | 1× H100 (TP=1) or 2× H100 (TP=2 for KV headroom) | `--gres=gpu:h100:1` |
| Apertus-70B | ~140 GB | 2× H100 (TP=2, 160 GB total) | `--gres=gpu:h100:2` |

For first launch, prefer requesting H100s on the `gpu` partition. Consumer cards (3090/4090) at 24 GB each would need 6+ GPUs for 70B via PCIe-only tensor parallelism — slow and not worth attempting until H100 path is validated.

### QoS limits for the gratis (free) tier (2026-05-27)

Per `sacctmgr show qos -P format=Name,MaxTRESPU,GrpTRES`, the `job_gratis` QoS — the default for users without a paid allocation — restricts which GPU types can be requested:

| GPU type | Max per-user | Cluster-wide gratis pool |
|---|---|---|
| H100 | **1** | 7 |
| RTX 4090 | **2** | 16 |
| A100 | 0 (blocked) | 0 |
| H200 | 0 (blocked) | 0 |
| RTX 3090 | 0 (blocked) | 0 |
| Blackwell Pro 6000 | 0 (blocked) | 0 |
| Total `gres/gpu` | 3 | 23 |

Implication: as a gratis user you can use **at most 1 H100 OR up to 2 RTX 4090s** at a time. Requests for A100/H200/3090/Blackwell fail with `QOSMaxGRESPerUser` regardless of partition. `gpu-invest` re-routes you into the `job_gpu_preemptable` QoS (same H100 hardware, but your job can be evicted by a paying user). For 70B-class work, the only path on gratis is **1× H100** — multi-GPU tensor parallelism not available within the gratis budget. If we ever need TP≥2 (e.g., to serve Apertus-70B), we'd need either DSL support to upgrade the QoS or use the `gpu_preemptable` route.

## 5. `congra-env` setup recipe

Mirror of local `/home/baebs/thesis/congra-env/` venv on UBELIX.

```bash
module load Python/3.11.3-GCCcore-12.3.0
cd ~/thesis
python3 -m venv congra-env
source congra-env/bin/activate
pip install --upgrade pip
pip install "openai==1.109.1" "transformers==4.39.0" "numpy==1.26.4" "torch==2.1.2" "huggingface_hub"
```

Pinned versions match local box, so pilot.py / ConGra metrics behave identically. Torch CPU is sufficient — `congra-env` is only used by pilot.py (which calls vLLM over HTTP, no local GPU). GPU work lives in `vllm-env`.

**Gotcha:** `which python` after activation may still show the module's Python path due to bash's command hash cache (`hash -r` clears it). The venv is correctly active if `$VIRTUAL_ENV` is set; verify packages with `congra-env/bin/python -m pip list`.

## 6. Recommended SLURM job template for vLLM

*Pending — to be added once first job runs successfully.*

## 6. Recipes: serving Apertus-70B / Qwen3-32B

*Pending — to be added after smoke test.*

## 7. Gotchas

### `HF_HOME=/huggingface` permission denied (fixed 2026-05-27)

The default UBELIX `~/.bashrc` line 28 sets:
```bash
export HF_HOME="$SCRATCH/huggingface"
```
But `$SCRATCH` is **empty until a workspace module is loaded** (e.g., `module load Workspace_Home`). With `$SCRATCH` unset, `HF_HOME` expands to `/huggingface` — a non-writable root path. Symptom: `huggingface-cli download` fails with `PermissionError: [Errno 13] Permission denied: '/huggingface'`.

**Fix applied:** changed line 28 to:
```bash
export HF_HOME="${SCRATCH:-$HOME/.cache}/huggingface"
```
The `:-` parameter expansion falls back to `$HOME/.cache` when `$SCRATCH` is empty. Future workspace loads still work because the parameter expansion checks at every shell init.

### `python3 -m venv` may produce a venv without `bin/pip` shim

Observed on `vllm-env` (2026-05-27). The pip package was installed under `vllm-env/lib/python3.11/site-packages/`, but `vllm-env/bin/pip` was missing. Symptom: `pip install` falls back to module pip and the warning "Defaulting to user installation because normal site-packages is not writeable" appears.

**Workarounds:**
- `vllm-env/bin/python -m pip install ...` — bypass the missing shim entirely.
- `vllm-env/bin/python -m ensurepip --upgrade` — rebuild the shim.

### `which python` shows module path even when venv is active

After `source venv/bin/activate`, `$VIRTUAL_ENV` is set correctly but `which python` still resolves to the module Python. Cause: bash's command location hash is stale. Fix: `hash -r`. Otherwise harmless — the venv is genuinely active.

### Figshare `ndownloader` URL blocked by AWS WAF

Symptom: curl hangs at 0% indefinitely. With `-v`, response is `HTTP/2 202` with `server: awselb/2.0` and `x-amzn-waf-action: challenge`. AWS WAF demands a JavaScript challenge that curl can't solve.

**Fix:** use the **figshare API endpoint** instead — it skips the WAF:
```bash
curl -L -o ConGra_dataset.tar.gz "https://api.figshare.com/v2/file/download/46967428"
```
ConGra dataset tar.gz is **2.26 GB** (not ~600 MB as I'd guessed earlier).
