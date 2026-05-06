# Ablation — pick-criterion failure on `0xe4ff79aa` (Qwen3)

Diagnostic ablation for [#44](https://github.com/bdravec/merge-conflict-skill/issues/44) (rec 7). Tests whether v2's pick-criterion failure on `0xe4ff79aa` is **prompt-level fixable** (H1 — the criterion is underspecified for the model) or a **model-level capability ceiling** (H2 — the model cannot reliably notice surrounding-code identifier style under any prompting).

Date: 2026-05-06. Source: `scripts/ablation_0xe4ff79aa.py`. Raw data: `scripts/results/ablation_0xe4ff79aa2f3f8922.jsonl`.

---

## Verdict

**H1 (prompt-level) is supported at the most extreme end. H2 is ruled out.** Qwen3 *can* pick correctly on this case when given an explicit per-case answer; it does not when given a worked example or a generic criterion exhortation. The proposed rec-3 worked example (Keras-vs-TF identifier divergence) does **not transfer** to this case.

| # | Condition | Pick | Edit | Flipped from baseline? |
|---|---|---|--:|---|
| 1 | baseline-v2 | b (`poolsize`, wrong) | 0.785 | (baseline) |
| 2 | v2 + explicit answer | **a (`pool_size`, correct)** | 0.7991 | **YES (b → a)** |
| 3 | v2 + criterion-only hint | b (wrong) | 0.785 | no |
| 4 | v2 + worked example | b (wrong) | 0.785 | no |

---

## Setup

**Case:** `0xe4ff79aa2f3f8922`, conflict #1 (Keras `convolutional.py`, MaxPooling2D `__init__`).
**Model:** Qwen/Qwen3-8B (served via vLLM on `localhost:8000`).
**Skill base:** `skills/merge-conflict-resolve-v2/SKILL.md` injected as system prompt (matches `pilot.py`'s `skill-v2-sys` condition that produced the original 0.785 result).
**Sampling:** `TEMPERATURE = 0.0`, single run per condition (matches `pilot.py`).

The four condition-specific additions (appended after v2's existing content):

- **Condition 2 — explicit answer:**
  > The surrounding code in this file uses underscores in identifiers (e.g. `pool_size`-style, not `poolsize`-style). The correct pick is `pool_size`.

- **Condition 3 — criterion-only hint:**
  > Examine the surrounding code's identifier style before picking. Match the convention used in the rest of the file.

- **Condition 4 — worked example** (the proposed rec-3 example for v2.1 § 6):
  > Pick — identifier divergence with surrounding-code style as tiebreaker.
  > ```
  > <<<<<<< a
  > j_tf = K.placeholder(shape=(None, 32), dtype=K.floatx())
  > =======
  > j_tf = tf.placeholder(dtype=K.floatx())
  > >>>>>>> b
  > ```
  > The surrounding code uses `K.` prefixes (`K.int_shape`, `K.floatx`). Pick a — its API style matches the rest of the file. Do not pick b just because it is shorter.

---

## Results

### Resolutions per condition

**Condition 1 — baseline-v2** (replicates pilot failure):

```python
def __init__(self, poolsize=(2, 2), stride=(1, 1), ignore_border=True):
        super(MaxPooling2D, self).__init__()
        self.input = T.tensor4()
        self.poolsize = tuple(poolsize)
        ...
```

Picks `poolsize` (side b, wrong). Identical to the v2-sys pilot output.

**Condition 2 — v2 + explicit answer** (only condition that flipped):

```python
def __init__(self, pool_size=(2, 2), stride=(1, 1), ignore_border=True):
        super(MaxPooling2D, self).__init__()
        self.input = T.tensor4()
        self.pool_size = tuple(pool_size)
        self.stride = tuple(stride)
        self.ignore_border = ignore_border
```

Picks `pool_size` (side a, correct, matches GT verbatim for the first 4 lines). Bonus: the explicit hint also suppressed the over-generation that baseline produces — output stops cleanly after the surrounding-context lines without fabricating an `@property def output_shape` body.

**Conditions 3 and 4** — identical resolutions to condition 1 (same wrong pick, same edit score, same length). The criterion-only hint and the worked example produced no observable change in Qwen3's output on this case.

### Edit-score note

Condition 2's edit score (0.7991) is only +0.014 above baseline (0.785), even though the pick decision flipped from wrong to correct. This is a direct manifestation of the **metric-weakness finding** documented in [`metric_weakness_0xe4ff79aa.md`](metric_weakness_0xe4ff79aa.md): on identifier-divergence cases where sides differ by ~1 character per occurrence, the wrong pick is "almost free" in edit-similarity terms. **The pick flip is real and cleanly visible in the resolution; the edit score barely moves because the metric does not weight pick correctness on this category of case.** Use the `pick` column, not the `edit` column, to read the result.

---

## Interpretation

### Why H2 is ruled out

Condition 2 demonstrates that Qwen3 has the capacity to apply the pick criterion on this case — when given an explicit per-case answer, it picks `pool_size` cleanly, and *also* trims the over-generation that baseline produces. The model is not blind to surrounding-code identifier style at this scale; it just doesn't apply the criterion under v2's framing.

### Why the rec-3 worked example does not transfer

The proposed example uses `K.placeholder` vs `tf.placeholder` (Keras-vs-TensorFlow API divergence). The target failure case uses `pool_size` vs `poolsize` (underscore-vs-no-underscore identifier divergence). The two are both "identifier-divergence with surrounding-code style as tiebreaker", but the *surface shape* differs:

- **Keras-vs-TF case:** the divergent token is a *namespace prefix* (`K.` vs `tf.`); the remainder of the identifier is the same.
- **`pool_size` case:** the divergent token is an *internal punctuation* (underscore present vs absent); the namespace and root identifier are the same.

Qwen3 appears to treat these as different categories. Generalising from one to the other does not happen automatically.

### Why the criterion-only hint does not work

"Examine the surrounding code's identifier style" tells the model *what to do* but not *what to look for* — an underscore-vs-no-underscore distinction is invisible unless the model is primed to attend to it specifically. v2's existing § Pick criterion 3 ("Local style: prefer the side that matches naming and indentation in the surrounding 5–10 lines") is structurally the same level of abstraction and produces the same outcome (no flip).

### What flipped the model

The minimum information sufficient to flip Qwen3 on this case is **the actual answer**: name the convention (`underscores`), name the correct pick (`pool_size`). Anything less abstract (criterion / example) was insufficient.

---

## Implications for v2.1 § 6 (rec 3 design)

Three options for the worked example in v2.1, in order from most-conservative to most-radical:

**(a) Keep the Keras-vs-TF example as-is.** Acknowledge in the v2.1 design doc that it has demonstrated non-transfer to underscore-style identifier divergence on Qwen3. May still help on Apertus (which already picks correctly on the `pool_size` case anyway, so no harm) or on other models / cases not yet tested.

**(b) Replace with a pool-size-style underscore-divergence example.** Use `pool_size` vs `poolsize` (or a structurally identical fictional example) explicitly. Pro: directly targets the observed failure mode. Con: harder to claim generality from an example that mirrors the failure-case identifier shape one-to-one — risks looking like teaching to the test.

**(c) Use both examples.** Keras-vs-TF for namespace divergence + a pool-size-style example for internal-punctuation divergence. Pro: covers two distinct surface shapes. Con: longer SKILL.md; further from the minimal-change principle; same teaching-to-the-test concern as (b).

**Recommended: (a) with a chapter-7 caveat.** The thesis methodology section can document the rec-3 transfer failure on Qwen3 / `0xe4ff79aa` as a finding about how worked-example transfer works at 8B scale: namespace-divergence examples don't generalise to internal-punctuation divergence without additional priming. This is itself a contribution.

The minimal-change principle disfavours (b) and (c) — both add example content without empirical evidence the new content helps (we only have evidence the *existing* example doesn't help on this specific case-shape). Option (a) is the cleanest.

---

## Reproduction

```bash
# Serve Qwen3-8B
source /home/baebs/thesis/vllm-env/bin/activate
export HF_HUB_OFFLINE=1
vllm serve Qwen/Qwen3-8B --port 8000 --max-model-len 32768 &

# Wait until ready
until curl -s http://localhost:8000/v1/models | grep -q "Qwen3-8B"; do sleep 5; done

# Run the ablation
python3 /home/baebs/thesis/merge-conflict-skill/scripts/ablation_0xe4ff79aa.py
```

Each condition takes ~2 seconds. Total runtime ~10 seconds.

---

## Related

- **Issue [#44](https://github.com/bdravec/merge-conflict-skill/issues/44)** — tracking issue for this ablation.
- **`docs/skill_v2_1_recommendations.md`** — rec 7 (the diagnostic that motivated this ablation), rec 3 (the proposed worked example whose transfer this ablation tests).
- **`docs/analysis_apertus_v1_v2.md`** — the `0xe4ff79aa` correction note that surfaced this case as the real ablation target.
- **`docs/analysis_qwen3_v1_v2.md`** — sub-q 3 commentary on the case (identifier-divergence cases that v2 doesn't fix).
- **`docs/metric_weakness_0xe4ff79aa.md`** — the metric finding that explains why condition 2's correct pick scored only 0.014 higher than baseline's wrong pick.
- **`scripts/inspect_case.py`** — diagnostic tool used to surface the original attribution error.
- **`scripts/ablation_0xe4ff79aa.py`** — the script that generated this data.
