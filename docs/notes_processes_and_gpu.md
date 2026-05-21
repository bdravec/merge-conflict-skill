# Notes: Processes, Memory, and the GPU

Learning notes bridging the OS lecture (processes, virtual memory, syscalls) to
the actual setup we run thesis experiments on. Written while watching the
Apertus v1 rerun for #57.

## The setup, in process terms

When pilot.py runs against vLLM, there are *two* Linux processes involved, not
one:

```
┌─────────────────────────────┐         ┌──────────────────────────────┐
│ pilot.py                    │  HTTP   │ vllm serve                   │
│ PID 964452                  │ ──────► │ PID 962792 (EngineCore child)│
│ python3 (CPU only)          │ :8000   │ python3 + CUDA kernels       │
│ reads dataset, scores edits │         │ owns the GPU                 │
└─────────────────────────────┘         └──────────────────────────────┘
                                                  │
                                                  ▼
                                        ┌──────────────────────────────┐
                                        │ GPU 0 — RTX 3090 24 GB       │
                                        │ ~22.5 GB VRAM in use:        │
                                        │   model weights + KV-cache   │
                                        └──────────────────────────────┘
```

Three commands to find each of these:

| Question | Command |
|---|---|
| Is the pilot process alive? | `ps -p 964452` or `pgrep -af "pilot.py"` |
| Is vLLM serving the right model? | `curl -s http://localhost:8000/v1/models` |
| What's on the GPU? | `nvidia-smi` |

## PID is the universal handle

The kernel assigns every process an integer PID when it's created. The PID
isn't a memory address — it's a *key* into the kernel's process table. That
table holds the rest: CPU register snapshots, memory mappings, file
descriptors, parent PID, scheduling state.

The same PID shows up everywhere:
- `ps -p 964452` — kernel's process table
- `kill 964452` — send SIGTERM to that process
- `/proc/964452/...` — Linux's view of the kernel's data for that PID
- `nvidia-smi` Processes section — same PID, if the process uses the GPU

For our setup: pilot.py PID 964452 only ever appears in the first three.
vLLM PID 962792 appears in all four because vLLM is what allocates CUDA
contexts.

## What `/proc/PID/maps` shows

Every line is one *virtual memory region* (VMA) the process has mapped:

```
<start>-<end>  <perms>  <offset>  <dev:inode>  <inode>  <pathname>
                rwxp
                │││└── private (vs shared)
                ││└─── execute
                │└──── write
                └───── read
```

For pilot.py (999 regions total), what we see:

- **The program** — `/usr/bin/python3.10` mapped four times with different
  permissions: code (`r-xp`), constants (`r--p`), initialized globals (`r--p`),
  uninitialized globals (`rw-p`). This is the dynamic linker laying out the
  ELF sections. Same pattern repeats for every shared library.
- **`[heap]`** — where `malloc()` lives. Already at ~242 MB for our Python.
- **Anonymous `rw-p` regions** (no pathname, `00:00 0`) — `mmap` calls without
  a backing file. Python's arenas, openai SDK buffers, NumPy arrays.
- **`---p` regions** (no permissions at all) — reserved but *uncommitted*
  address space. Lazy allocation: the kernel won't touch physical RAM until
  the process actually reads or writes there.
- **Shared libraries** — `libstdc++`, `libz`, the whole CUDA stack
  (`libcufft`, `libcublasLt`, `libcusparseLt`, …) sitting in the venv. Most
  of those CUDA libraries are *mapped but not resident* — the Python pilot
  never touches them, so the kernel never pages them in.
- **`[stack]`** — main thread's call stack.
- **`[vdso]`, `[vvar]`, `[vsyscall]`** — kernel-injected fast-path mappings
  for syscalls like `gettimeofday()` (avoids the context-switch into
  kernel mode for hot syscalls).

Big takeaway: **virtual size ≠ physical size.** `ps -o vsz,rss -p <pid>`
shows both: `vsz` is the sum of all mapped regions (huge), `rss` is the
physical RAM actually in use (much smaller).

## nvidia-smi and GPU memory

GPU memory lives in a *completely separate* address space the kernel doesn't
track in `/proc/PID/maps`. To see it you need `nvidia-smi`, which queries the
NVIDIA driver directly.

```
| GPU 0  RTX 3090       100% util   22574MiB / 24576MiB   349W / 350W   74°C |
| GPU 1  RTX 3090         0% util       1MiB / 24576MiB    30W / 350W   42°C |

Processes:
|  GPU       PID   Process name             GPU Memory  |
|    0    962792   VLLM::EngineCore           22574MiB  |
```

What the columns mean:
- **`GPU-Util`** — fraction of recent samples where at least one SM
  (streaming multiprocessor) was active. 100% means the GPU is the
  bottleneck.
- **`Memory-Usage`** — bytes of VRAM allocated by *any* process on this GPU.
  Not the same as `r--p .data` in `/proc/PID/maps` — it's tracked by the
  NVIDIA driver, not the Linux kernel.
- **`Pwr:Usage/Cap`** — power draw vs power cap. RTX 3090 caps at 350 W;
  hitting it means the GPU is at thermal/power throttle.

Only processes that have a CUDA context appear in the Processes section.
pilot.py doesn't — it's pure CPU. vLLM does — it loaded model weights and
allocated KV-cache buffers in VRAM.

For an 8B model on a 24 GB card:
- Model weights at bf16: ~16 GB.
- KV-cache reservation for `--max-model-len 32768` at `--concurrency 2`:
  ~6 GB.
- Total ~22.5 GB matches what `nvidia-smi` reports.

## KV-cache, in one paragraph

In transformer attention, each token gets projected into Query, Key, and
Value vectors. When generating text token-by-token, naïvely you'd recompute
K and V for every previous token at each step (quadratic work). Instead,
transformers **cache** the K and V of every token once computed — the
**KV-cache** — and at each new step only compute K and V for the new token.
The cache lives in GPU memory. Budget per token per layer is roughly
`2 (K+V) × hidden_dim × bytes_per_element`. For Apertus-8B at bf16 that's
~16 KB per token per layer, ~512 KB per token across all layers, ~16 GB
for one full 32 k-token context. vLLM uses **PagedAttention** to share that
budget across concurrent requests (same idea as OS-level virtual memory
pages, applied to GPU memory).

## OOM: two flavors

Out Of Memory. Different mechanics on CPU vs GPU.

- **CPU OOM** — process tries to allocate more RAM than the OS can give.
  Linux's OOM killer wakes up, picks a process (usually the biggest memory
  hog by an internal score), and sends it SIGKILL. You'd see it in `dmesg`
  as `Out of memory: Killed process <pid>`. The process can't catch this.
- **GPU OOM** — CUDA can't allocate the requested VRAM. The runtime returns
  `cudaErrorMemoryAllocation`; PyTorch surfaces it as
  `RuntimeError: CUDA out of memory. Tried to allocate X MiB; Y MiB free`.
  The Python process doesn't die from the kernel — it's an application-level
  exception that the application either handles or crashes on.

For #57: GPU KV-cache OOM was the leading hypothesis (two long requests
at `c=2` exceeding the cache budget). #59 ruled it out — crashed prompts
were 370–2,901 tokens while non-crashed prompts went to 27 k tokens. So
the cause is still open; the rerun runs with `--max-prompt-tokens 30720`
as a belt for the 2 known real outliers.

## Live monitoring

For the running pilot:

```
watch -n 5 nvidia-smi              # GPU side, refreshes every 5 s
watch -n 30 'wc -l scripts/results/pilot_results_apertus_v1_python_tiny_c2_text+func.jsonl'
tail -f scripts/results/pilot_run_apertus_v1_python_tiny_c2_text+func.log
```

If GPU 0 memory usage spikes from ~22.5 GB toward 24 GB during long
requests, you're seeing KV-cache fill up — and you're close to the
GPU-OOM scenario.
