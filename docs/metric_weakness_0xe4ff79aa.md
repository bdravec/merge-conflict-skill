# Metric weakness — compact wrongness beats verbose correctness on `0xe4ff79aa`

A concrete piece of evidence that ConGra's edit-similarity metric can rank a wrong-pick resolution higher than a right-pick resolution when the wrong-pick output happens to be more compact and the right-pick output extends past the conflict region.

Surfaced 2026-05-06 via `scripts/inspect_case.py 0xe4ff79aa` during the cross-model verification recorded in `analysis_apertus_v1_v2.md`'s correction note.

---

## Observation

Case `0xe4ff79aa2f3f8922` (Keras `convolutional.py`, conflict #1) has the simplest possible identifier-divergence shape: side a uses `pool_size`, side b uses `poolsize`. Ground truth picks side a (correct: surrounding code uses `pool_size` consistently — `pool_output_length(input_length, pool_size, ...)`, `MaxPooling1D.pool_size`, etc.).

Edit-similarity scores across the two 8B pilot models:

| Model   | Condition  | Pick (a / b) | edit  | winnowing | Output shape                                                                |
|---------|------------|--------------|------:|----------:|-----------------------------------------------------------------------------|
| Qwen3   | no-skill   | b (wrong)    | **0.785** | 0.6685    | 6 lines: just the conflict region content with `poolsize`                   |
| Qwen3   | skill-v2-sys | b (wrong)  | **0.785** | 0.6685    | identical to no-skill                                                       |
| Qwen3   | skill-v2-user | b (wrong) | **0.785** | 0.6685    | identical to no-skill                                                       |
| Apertus | skill-v2-sys | a (correct) | 0.620 | 0.7688    | 9 lines: conflict region + `self.stride`, `self.ignore_border`, `@property def output_shape:` stub |
| Apertus | skill-v2-user | a (correct) | 0.620 | 0.7688    | identical to v2-sys                                                         |
| Apertus | no-skill   | a (correct)  | 0.451 | 0.6759    | 14 lines: also includes a fabricated `output_shape` body with malformed return divisions |

**The headline:** Qwen3's *wrong* pick scores 0.785; Apertus's *correct* pick scores at most 0.620. The metric ranks them in the order opposite to the resolution-quality order.

Source files: `scripts/results/pilot_results_qwen3_skill-v2.jsonl`, `scripts/results/pilot_results_apertus_skill-v2.jsonl`. Verification command: `python3 scripts/inspect_case.py 0xe4ff79aa`.

---

## Mechanism

Two independent factors combine to produce this inversion.

**(1) Side a and side b have heavy token overlap.** They differ only by an underscore: `pool_size` vs `poolsize`. After ConGra's `_remove_invisible` normalisation strips whitespace, `pool_size` and `poolsize` differ by 1 character per occurrence. With 4 occurrences in the conflict region, the two sides are ~4 characters apart out of ~150. A wrong-pick output is therefore *almost* a right-pick output as far as Levenshtein-based edit similarity is concerned.

**(2) The model that picks correctly extends past the conflict region.** Apertus, which picks the right side (a), continues generating beyond the conflict region's 4 lines: it adds `self.stride = tuple(stride)`, `self.ignore_border = ignore_border`, then opens an `@property def output_shape(self):` block. Each extra line adds to the resolution length without adding ground-truth tokens, depressing the edit-similarity ratio. Apertus's no-skill output (0.45) goes further still — it fabricates the body of `output_shape` with broken-syntax divisions.

The combination is what makes the inversion possible:
- Qwen3's wrong pick is "free" (≈4 chars off correct, no over-generation penalty).
- Apertus's right pick costs ≈0 chars at the conflict line itself but pays heavily for the over-generation that surrounds it.

The metric's notion of "similar" is dominated by length-ratio effects in the denominator (`max(len(gen), len(ref))`); when the conflict region is short and the over-generation is long, the over-generation factor swamps the pick correctness.

---

## Reproduction

```bash
python3 /home/baebs/thesis/merge-conflict-skill/scripts/inspect_case.py 0xe4ff79aa
```

Look at the model resolutions in the output. `pool_size` in the first `def __init__` line = correct pick (a). `poolsize` = wrong pick (b). Compare against the edit scores reported per record.

To verify the metric mechanics directly:

```python
from scripts.pilot import metric_edit_distance
gt = "..."  # paste ground truth from inspect_case output
qwen3_wrong = "..."  # paste Qwen3 v2-sys resolution
apertus_right = "..."  # paste Apertus v2-sys resolution
print("Qwen3 (wrong, compact):", metric_edit_distance(qwen3_wrong, gt))
print("Apertus (right, longer):", metric_edit_distance(apertus_right, gt))
```

(`metric_edit_distance` is inlined from `ConGra/src/metrics.py`; the function is defined at `scripts/pilot.py` near line 46.)

---

## Implications

**This is a metric problem, not a skill problem.** No version of the SKILL.md can fix the metric inversion observed here. v2 already applies the rules it should: it trims over-generation. On Apertus, that trimming improves the score from 0.45 (no-skill) to 0.62 (v2-sys). It still can't beat Qwen3's 0.785 because Qwen3's compact wrongness has structural metric privilege.

**Two sibling findings document the same underlying weakness from different angles:**

- **`0xd9272c5e0e8f15ee`** (`analysis_apertus_v1_v2.md` sub-q 3, "A note on metric mechanics", line 290): when the ground-truth resolution lives *outside* the conflict region (architectural pattern that neither side encodes), *retaining surrounding context becomes a proxy* for the pattern-recognition the model cannot actually do. The metric rewards *leak that happens to align*. There, length helps; here, length hurts.
- **`pool_size`/`poolsize`, `get_shape`/`_keras_shape`** (`analysis_qwen3_v1_v2.md` sub-q 3, line 278): identifier-divergence cases where the two sides have heavy token overlap inflate scores irrespective of correctness. This finding is the same shape as the present one, restricted to Qwen3.

**For the thesis:**

- Chapter 6 (skill evaluation) should discuss this as a case where v2's mechanism works as intended but the metric does not reward the result.
- Chapter 7 (limitations) should cite this finding, alongside `0xd9272c5e`, as concrete evidence that edit-similarity is an imperfect proxy for resolution quality. A semantic-equivalence metric (AST-aware, identifier-aware) would not produce this inversion.
- RQ3 framing — "does small model + skill close the gap to large model without skill?" — needs to acknowledge that `gap` here is partly an artefact of the metric, not just an artefact of model capability.

**The finding does not invalidate the v2 evaluation.** Across the 20-case pilot, identifier-divergence cases like this one are a minority. The Apertus +0.034 mean uplift and the Qwen3 −0.012 mean uplift remain the right summary statistics for v2's effect on this metric. What this finding adds is a constraint on how strongly to interpret those summary statistics as quality measurements rather than as joint length-and-content measurements.

---

## Related

- `analysis_apertus_v1_v2.md` — `0xe4ff79aa` correction note (line 57 area)
- `analysis_qwen3_v1_v2.md` — sub-q 3 `0xe4ff79aa` update (line 278 area)
- `skill_v2_1_recommendations.md` — rec 7 (now retargeted to Qwen3, [#44](https://github.com/bdravec/merge-conflict-skill/issues/44))
- `scripts/inspect_case.py` — the verification tool that surfaced the finding
