# merge-conflict-skill

Bachelor thesis project — University of Bern, Software Engineering Group.

**Working title:** Agent Skills for Merge Conflict Resolution: Designing and Evaluating SKILL.md-based Knowledge for Small and Large Language Models

**Candidate:** Barbara Dravec
**Supervisor:** Prof. Dr. Timo Kehrer
**Advisor:** Roman Makacek

---

## Repository Structure

```
merge-conflict-skill/
├── docs/
│   └── eda_dataset.md       ← Dataset analysis and critical perspective
├── scripts/
│   └── smoke_test.py        ← Pipeline smoke test (metrics only, no LLM)
├── skills/                  ← SKILL.md versions (coming in Month 2)
└── README.md
```

---

## Prerequisites

| Requirement | Version used |
|---|---|
| Python | 3.10.12 |
| CUDA | 13.0 |
| GPU | NVIDIA GeForce RTX 3090 (24 GB VRAM) |
| PyTorch | 2.1.2 |
| vLLM | 0.3.3 |
| transformers | 4.39.0 |
| langchain | 0.1.15 |

---

## Setup

### 1. Clone this repo and the ConGra benchmark

```bash
git clone https://github.com/bdravec/merge-conflict-skill.git
git clone https://github.com/HKU-System-Security-Lab/ConGra.git
```

### 2. Create and activate the virtual environment

```bash
cd ConGra
python3 -m venv congra-env
source congra-env/bin/activate
```

### 3. Install dependencies

ConGra has no `requirements.txt`. Install manually:

```bash
pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cu121
pip install transformers==4.39.0
pip install langchain==0.1.15 langchain-openai==0.1.6 langchain-core==0.1.52 langchain-community==0.0.38
pip install langchain-anthropic==0.1.11 langchain-aws==0.1.3 langchain-google-genai==1.0.3
pip install langchain-groq==0.1.3 langchain-text-splitters==0.0.2 langsmith==0.1.59
pip install vllm==0.3.3
```

### 4. Download the ConGra dataset

The dataset is hosted on Figshare. Download it via your browser:

```
https://figshare.com/ndownloader/files/46967428
```

Move the downloaded file into the `ConGra/data/` directory and extract:

```bash
mv ~/Downloads/Congra_datasets.tar.gz ConGra/data/
cd ConGra/data
tar -xzvf Congra_datasets.tar.gz
```

Expected structure after extraction:

```
data/
├── congra_full_datasets/
├── congra_tiny_datasets/
├── raw_datasets/
└── README.md
```

---

## Running the Evaluation Pipeline

### Smoke test (no LLM required)

Verifies that the metrics work correctly using known inputs, without running a model:

```bash
cd ConGra/src
source ../congra-env/bin/activate
python ../../merge-conflict-skill/scripts/smoke_test.py
```

Expected output:

```
Case                             Edit sim  Winnowing  Verdict
------------------------------------------------------------
Perfect (ground truth)             1.0000     1.0000  PASS ✓
Empty string                       0.0000     1.0000  PASS ✓  ← known bug
Dummy ("pass")                     0.0296     0.0000  fail ✗
```

Note: the empty string case passes via winnowing — this is a known bug in the ConGra pipeline (see `docs/eda_dataset.md` for details).

### Full pipeline (with LLM via vLLM)

First, serve a model using vLLM (only one model fits in VRAM at a time):

```bash
export HF_HUB_OFFLINE=1
source /home/baebs/thesis/vllm-env/bin/activate

# Qwen3-8B
vllm serve Qwen/Qwen3-8B --port 8000 --max-model-len 32768

# Apertus-8B
vllm serve swiss-ai/Apertus-8B-Instruct-2509 --port 8000 --max-model-len 32768
```

Wait for `Application startup complete` in the terminal, then verify it's responding:

```bash
curl -s http://localhost:8000/v1/models | python3 -m json.tool
```

To switch models, stop the running server first: `pkill -f "vllm serve"`

> **Note:** ConGra's `main.py` does not support Qwen3 or Apertus (hardcoded model routing in `utils.py`). Use the standalone pilot script instead:

```bash
source /home/baebs/thesis/vllm-env/bin/activate
python scripts/pilot.py
```

Results are saved to `scripts/results/pilot_results.jsonl`. See `docs/vllm_setup.md` for full setup details.

---

## Interpreting Output Metrics

Each line of `resolutions.jsonl` is a JSON object with the following fields:

| Field | Description |
|---|---|
| `source_hash` | Hash ID of the sample |
| `conflict_type` | Conflict category (e.g. `func`, `text`) |
| `conflict` | The conflicted region shown to the model |
| `resolution` | The model's output |
| `resolved_text` | The ground truth resolution |
| `edit_distance` | Edit similarity score (0.0–1.0) |
| `winnowing` | Winnowing similarity score (0.0–1.0) |
| `fix_time` | Time taken to generate the resolution (seconds) |
| `context_line` | Number of context lines provided to the model |
| `completion_tokens` | Output tokens used |
| `prompt_tokens` | Input tokens used |

A resolution is considered **correct** if at least one metric (edit similarity or winnowing) exceeds **0.80**, following the ConGra evaluation protocol.

**Note:** Semantic similarity (cosine similarity via code embeddings) is defined in `metrics.py` but is not computed by `main.py`. It would need to be added separately.

---

## Known Issues with the ConGra Pipeline

See `docs/eda_dataset.md` — "Pipeline Limitations Discovered During Smoke Testing" for a detailed discussion of:

- The winnowing bug (empty resolutions score as perfect)
- Missing semantic similarity in `main.py`
- When empty resolutions can realistically occur
