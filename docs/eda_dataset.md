# ConGra Dataset

## Overview

This thesis uses the **ConGra** benchmark (Zhang et al., NeurIPS 2024) for evaluating merge conflict resolution quality. ConGra is a large-scale, multilingual dataset of real-world merge conflicts extracted from open-source repositories, paired with ground truth resolutions. It provides a ready-made evaluation pipeline based on three similarity metrics.

The dataset is available at: https://github.com/HKU-System-Security-Lab/ConGra

---

## Conflict Type Taxonomy

ConGra classifies merge conflicts into three base categories:

| Type | Description |
|---|---|
| **text** | Conflicts at the textual level — overlapping edits with no deeper semantic meaning (e.g., whitespace, comments, formatting) |
| **sytx** (syntax) | Conflicts that affect the syntactic structure of the code (e.g., changed function signatures, restructured blocks) |
| **func** (functional) | Conflicts that affect program behavior — both sides change the same logic in incompatible ways |

Samples may belong to a single category or a combination (e.g., `text+sytx`, `sytx+func`, `text+sytx+func`), reflecting that real-world conflicts often span multiple dimensions simultaneously.

---

## Dataset Variants

ConGra is distributed in three variants:

| Variant | Description |
|---|---|
| `raw_datasets` | Full conflict data per project, including all files needed for tool-level evaluation (base, branches a and b, merged output, resolved output, region annotations) |
| `congra_tiny_datasets` | One conflict region per file; suitable for LLM evaluation |
| `congra_full_datasets` | Multiple conflict regions may appear per file |

This thesis uses `congra_tiny_datasets` exclusively. The single-conflict-per-file constraint simplifies evaluation: the LLM receives one conflicted file and must produce one resolved file, with no ambiguity about which region to target.

---

## File Structure

### `congra_tiny_datasets`

The tiny dataset is organized by programming language and conflict type:

```
congra_tiny_datasets/
└── <language>/
    └── <conflict_type>/
        ├── <hash_id>         ← conflicted file (with Git conflict markers)
        ├── <hash_id>
        └── meta_list.txt     ← index mapping hash IDs to raw_datasets paths
```

Each sample file (named by a hex hash) is a complete source file containing exactly one conflict region, marked with standard Git conflict markers:

```
<<<<<<< a
<lines from branch A>
=======
<lines from branch B>
>>>>>>> b
```

### `raw_datasets`

The raw dataset provides the full context for each conflict pair, organized by language and project:

```
raw_datasets/
└── <Language>/
    └── <project>/
        └── conflict_files_<N>/
            ├── merged_without_base/   ← conflicted file (identical to tiny dataset sample)
            ├── resolved/              ← ground truth resolution
            ├── regions/               ← conflict region line numbers (origin and resolved)
            ├── a/                     ← branch A version of the file
            ├── b/                     ← branch B version of the file
            ├── base/                  ← common ancestor version
            └── merged/                ← Git auto-merge output (with markers)
```

### `meta_list.txt`

Each conflict type subdirectory contains a `meta_list.txt` file that serves as an index. Each line maps a sample to its ground truth in `raw_datasets`:

```
<raw_datasets_path>: <hash_id>: <num_conflict_regions>
```

Example:
```
Python/keras/conflict_files_56/merged_without_base/theano_backend.py: 0xddd5322de12565fe: 1
```

In the tiny dataset, the third field (number of conflict regions) is always `1`.

### Region Files

The `.region` file for each sample records the line span of the conflict region in both the conflicted file and the resolved file:

```
# (origin_conflict_start, origin_conflict_end, resolved_start, resolved_end)
(448, 456, 437, 443)
```

This allows precise, region-level metric computation rather than whole-file comparison.

---

## Sample Counts (Tiny Dataset — Python and Java)

This thesis focuses on Python and Java samples. The distribution across conflict types in the tiny dataset is as follows:

| Conflict type | Python | Java |
|---|---|---|
| text | 822 | 1151 |
| sytx | 447 | 843 |
| func | 555 | 849 |
| text+sytx | 81 | 77 |
| text+func | 663 | 62 |
| sytx+func | 128 | 622 |
| text+sytx+func | 908 | 312 |
| **Total** | **3,604** | **3,916** |

The full tiny dataset (all languages) contains samples in C and C++ as well, which are not used in this thesis.

---

## Ground Truth and Evaluation

For each sample, the ground truth resolution is the `resolved/` file from `raw_datasets` — the actual resolution committed by the developer in the original repository. This represents what a human developer judged to be the correct merge outcome.

The ConGra evaluation pipeline compares a model-produced resolution against the ground truth using three metrics:

| Metric | Description |
|---|---|
| **Edit similarity** | Normalized character-level edit distance between resolution and ground truth |
| **Semantic similarity** | Cosine similarity between code embeddings of resolution and ground truth |
| **Winnowing similarity** | Fingerprinting-based structural similarity between resolution and ground truth |

A resolution is considered correct when at least one metric exceeds the 80% threshold, following the ConGra evaluation protocol.

---

## Reference

Zhang, Y. et al. (2024). *ConGra: Benchmarking Automatic Conflict Resolution*. NeurIPS 2024 Datasets and Benchmarks Track. https://github.com/HKU-System-Security-Lab/ConGra
