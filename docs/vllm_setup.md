# vLLM Local Setup

## Overview

Models are served locally via [vLLM](https://docs.vllm.ai), which exposes an OpenAI-compatible HTTP API at `http://localhost:8000`. This lets the ConGra pipeline and the Hermes agent talk to local models using the same interface as the OpenAI API.

## Environment

- **GPU:** NVIDIA GeForce RTX 3090, 24 GB VRAM
- **Python:** 3.10.12
- **vLLM:** 0.19.0
- **venv:** `/home/baebs/thesis/vllm-env/`
- **Model cache:** `~/.cache/huggingface/hub/`

## Setup Steps (one-time)

### 1. Create the venv

```bash
python3 -m venv /home/baebs/thesis/vllm-env
```

### 2. Install vLLM

```bash
source /home/baebs/thesis/vllm-env/bin/activate
pip install --upgrade pip
pip install vllm
```

### 3. Hugging Face authentication

Install `huggingface-hub` (already included with vLLM), then save your token:

```bash
echo 'export HF_TOKEN="hf_..."' >> ~/.bashrc
source ~/.bashrc
```

Verify login:

```python
from huggingface_hub import whoami
print(whoami()['name'])
```

### 4. Download model weights

```bash
source /home/baebs/thesis/vllm-env/bin/activate
huggingface-cli download Qwen/Qwen3-8B
```

## Starting the Server

```bash
export HF_HUB_OFFLINE=1
source /home/baebs/thesis/vllm-env/bin/activate
vllm serve Qwen/Qwen3-8B --port 8000 --max-model-len 32768
```

**Flags explained:**
- `HF_HUB_OFFLINE=1` — prevents vLLM from calling the HF API on startup (model is already cached)
- `--max-model-len 32768` — caps context to 32K tokens; the model's default 40K requires more KV cache memory than fits on the RTX 3090 alongside the model weights

## Testing the Server

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen/Qwen3-8B", "messages": [{"role": "user", "content": "Reply with just: OK"}], "max_tokens": 10}'
```

## Notes

- **Thinking mode:** Qwen3-8B enables chain-of-thought by default (responses start with `<think>` blocks). Disable for benchmarking by adding `"chat_template_kwargs": {"enable_thinking": false}` to requests.
- **Apertus-8B:** Same setup — download with `huggingface-cli download <model-id>`, serve on a different port or stop Qwen3 first.
