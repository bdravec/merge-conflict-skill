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

| Metric | Captures | Blind to |
|---|---|---|
| **Edit similarity** | Textual closeness — how few character-level edits separate the two files | Semantically equivalent code expressed differently (different variable names, formatting, structure) |
| **Semantic similarity** | Meaning — whether the two files do the same thing, even if expressed differently | Logical correctness; two wrong resolutions can be semantically similar to each other |
| **Winnowing similarity** | Structural overlap — shared code fingerprints regardless of surface variation | Fine-grained textual differences; may miss small but semantically important changes |

A resolution is considered correct when at least one metric exceeds the 80% threshold, following the ConGra evaluation protocol.

### Edit Similarity

Edit similarity is based on **Levenshtein distance** — the minimum number of single-character operations (insertions, deletions, substitutions) needed to transform one string into another.

**Example:**
```
model output:  "if mask is not None:"
ground truth:  "if mask is None:"
```
Edit distance = 4 (delete " not") → very close.

```
model output:  "return x + 1"
ground truth:  "return x * factor"
```
Edit distance = much larger → far apart.

**Normalization:** Raw edit distance depends on file length — a distance of 50 means something different for a 100-line file vs. a 5000-line file. It is therefore normalized as:

```
edit_similarity = 1 - (edit_distance / max(len(output), len(ground_truth)))
```

The result is always between 0.0 (completely different) and 1.0 (identical).

**What it captures well:** Resolutions that are textually close to the ground truth — same words, same order, minor differences.

**What it misses:** A resolution can be semantically correct but score low if it uses different variable names, different formatting, or expresses the same logic differently. Conversely, it can score high by being textually similar to the ground truth while being logically wrong.

**Implication for this thesis:** Edit similarity is the most straightforward metric but also the most sensitive to surface-level differences. A skill that teaches the model to format output consistently with the ground truth style could inflate this score without genuinely improving resolution quality.

---

## Critical Perspective on the Dataset

### The Ground Truth Problem

ConGra uses the resolution committed by the original developer as the ground truth — the reference against which all model outputs are measured. This is a practical and widely adopted convention, but it carries an important limitation: **merge conflict resolution is not a function with a single correct output**.

When two branches modify the same code in incompatible ways, multiple resolutions may be semantically valid. Different developers, with different intentions or architectural views, may resolve the same conflict differently and both be correct. The committed resolution reflects one developer's judgment at one point in time — it is not a universal truth, but a plausible outcome among potentially several.

This means that a model resolution which differs from the ground truth may still be functionally correct, and will nonetheless be penalized by the similarity metrics. Conversely, a resolution that scores above the 80% threshold may be textually close to the ground truth but logically wrong in ways the metrics cannot detect. The evaluation framework measures proximity to one human decision, not correctness in a deeper sense.

This limitation is not unique to ConGra — it is a fundamental challenge in any benchmark that uses human-produced artifacts as ground truth for open-ended tasks. It should be kept in mind when interpreting results, particularly when differences between conditions (skill vs. no skill, small vs. large model) are small.

### Tiny Dataset vs. Full Dataset

The choice to use `congra_tiny_datasets` rather than `congra_full_datasets` has methodological consequences worth making explicit.

**Advantages of the tiny dataset:**
- Each file contains exactly one conflict region, making the task unambiguous: the model receives one conflicted file and must produce one resolved file.
- Evaluation is clean and directly comparable across samples — there is no need to identify or align multiple conflict regions within a single file.
- The controlled setting is better suited to isolating the effect of skill injection, which is the primary research question of this thesis.

**Limitations compared to the full dataset:**
- Real-world merge conflicts frequently involve multiple conflict regions within a single file. A developer resolving such a file must reason about all regions in context, as they may interact. The tiny dataset removes this complexity entirely.
- By filtering to single-conflict files, the tiny dataset may be systematically biased toward simpler cases. Files with many conflicts are excluded, potentially underrepresenting the most challenging and practically relevant scenarios.
- Results obtained on the tiny dataset may therefore overestimate model performance relative to what would be observed in realistic, multi-conflict settings.

### Dataset Scope and Generalizability

ConGra draws from a specific set of open-source Python and Java projects. The sample counts are large (over 7,500 samples for the two languages used in this thesis), which supports statistical analysis, but the dataset reflects the conflict patterns of those particular projects and their contributor communities. Generalization to other languages, proprietary codebases, or different development workflows cannot be assumed without further study.

Additionally, the conflict type classification (text, syntax, functional) is determined automatically. Classification errors, while expected to be rare at scale, may introduce noise into the per-type analysis used to answer RQ2.

---

## Reference

Zhang, Y. et al. (2024). *ConGra: Benchmarking Automatic Conflict Resolution*. NeurIPS 2024 Datasets and Benchmarks Track. https://github.com/HKU-System-Security-Lab/ConGra
