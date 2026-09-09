"""Build the 20-minute final thesis defense deck — 10 slides (#126).

Ten slides, ~2 min each, in the `Thesis_Review_*` house style: red Title A asks the
question, black Title B states the answer, figure below, 10 pt Arial number box on the
right. Storyline: problem/gap -> three RQs -> the three-stage design loop -> RQ1 -> RQ2
-> the cross-benchmark law -> RQ3's four rules -> conclusion + threats.

Two gotchas worth keeping:
  * `prs.slide_layouts` only exposes master 0's layouts, and the Uni Bern template has
    six masters -- iterate `prs.slide_masters` to reach `3: Titel-Folie ohne Bild`.
  * The template ships with its own slides; `delete_all_slides` must drop the *relationship*
    as well, or python-pptx re-writes the orphaned parts on save.

Figures are reused as-is from the repo; nothing here regenerates them.
"""
import os
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt

REPO = Path(__file__).resolve().parent.parent
TPL  = "/home/baebs/thesis/review_mtgs/PPTVorlage-UniBe_ger.pptx"
OUT  = "/home/baebs/thesis/review_mtgs/Thesis_Defense_2026-09-09.pptx"
FIG  = str(REPO / "docs/figures")
OFIG = str(REPO / "results_overleaf_figures")

def delete_all_slides(prs):
    """Drop the relationship too, or python-pptx re-writes orphaned parts on save."""
    from pptx.oxml.ns import qn
    sldIdLst = prs.slides._sldIdLst
    pres_part = prs.part
    for sld_id in list(sldIdLst):
        rId = sld_id.get(qn('r:id'))
        sldIdLst.remove(sld_id)
        pres_part.rels.pop(rId)

prs = Presentation(TPL)
delete_all_slides(prs)

def layout(name):
    for m in prs.slide_masters:
        for l in m.slide_layouts:
            if l.name == name:
                return l
    raise KeyError(name)

L_TITLE = "3: Titel-Folie ohne Bild"
L_TOC   = "4: Inhaltverzeichnis"
L_2COL  = "5a: Text-Folie 2 Spalten"

def ph(slide, idx):
    for p in slide.placeholders:
        if p.placeholder_format.idx == idx:
            return p
    return None

def settext(shape, text, size=None, bold=None, color=None):
    tf = shape.text_frame
    tf.word_wrap = True
    lines = text.split("\n") if isinstance(text, str) else list(text)
    tf.text = lines[0]
    for extra in lines[1:]:
        tf.add_paragraph().text = extra
    for para in tf.paragraphs:
        for r in para.runs:
            if size  is not None: r.font.size = Pt(size)
            if bold  is not None: r.font.bold = bold
            if color is not None: r.font.color.rgb = color

def box(slide, l, t, w, h):
    return slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))

def place_image(slide, path, left, top, max_w, max_h):
    """Insert preserving aspect ratio, fitted inside the box, horizontally centred in it."""
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(max_w / iw, max_h / ih)
    w, h = iw * scale, ih * scale
    return slide.shapes.add_picture(path, Inches(left + (max_w - w) / 2), Inches(top),
                                    Inches(w), Inches(h))

def head(slide, title_a, title_b):
    """Her house pattern: red title placeholder + black subtitle textbox underneath."""
    t = ph(slide, 0)
    t.left, t.top, t.width, t.height = Inches(0.59), Inches(0.62), Inches(8.85), Inches(0.62)
    settext(t, title_a, size=18)
    s = ph(slide, 11)
    if s is not None:
        s.left, s.top, s.width, s.height = Inches(0.59), Inches(1.28), Inches(8.85), Inches(0.55)
        settext(s, title_b, size=17)
    for idx in (10, 12):
        p = ph(slide, idx)
        if p is not None:
            p._element.getparent().remove(p._element)
    return slide

def note(slide, l, t, w, h, lines):
    b = box(slide, l, t, w, h)
    settext(b, lines, size=10)
    for para in b.text_frame.paragraphs:
        for r in para.runs:
            r.font.name = "Arial"
    return b

# ---------------------------------------------------------------- 1. title
s = prs.slides.add_slide(layout(L_TITLE))
settext(ph(s, 0),  "Barbara Dravec — Bachelor Thesis Defense", size=26)
settext(ph(s, 11), "Agent Skills for Merge Conflict Resolution:\n"
                   "Designing and Evaluating SKILL.md-based Knowledge "
                   "for Small and Large Language Models", size=17)
settext(ph(s, 10), "Prof. Dr. T. Kehrer · R. Makacek", size=14, bold=True)
settext(ph(s, 12), "9. September 2026 · Universität Bern", size=12)

# ---------------------------------------------------------------- 2. agenda
s = prs.slides.add_slide(layout(L_TOC))
settext(ph(s, 20), "Bachelor Thesis Defense — Agent Skills for Merge Conflict Resolution", size=12)
settext(ph(s, 0),  "Agenda", size=20)
settext(ph(s, 11), "20 minutes", size=17)
settext(ph(s, 12), ["1.  Problem and motivation",
                    "2.  Research questions",
                    "3.  Method — the skill design loop"], size=18)
settext(ph(s, 14), ["4.  Results — RQ1 and RQ2",
                    "5.  What makes a skill work — RQ3",
                    "6.  Conclusion and Q&A"], size=18)

# ---------------------------------------------------------------- 3. problem
s = prs.slides.add_slide(layout(L_2COL))
settext(ph(s, 20), "1. Problem and motivation", size=12)
settext(ph(s, 0),  "Merge conflicts are expensive, and SKILL.md is adopted on faith", size=18)
settext(ph(s, 11), "The practice is spreading faster than the evidence", size=17)
settext(ph(s, 16), "The task", size=14, bold=True)
settext(ph(s, 17), ["• Merge conflicts interrupt development and are still resolved by hand",
                    "• ConGra (Zhang et al. 2024): 44,948 real conflicts, graded by complexity",
                    "• Ground truth = the resolution the developer actually committed"], size=12)
settext(ph(s, 18), "The gap", size=14, bold=True)
settext(ph(s, 19), ["• SKILL.md packages domain knowledge as plain text, read at inference time",
                    "• Published skill evaluations use agentic harnesses and proprietary models",
                    "• No evidence for single-shot use on open-weight models — which is what a "
                    "lab or a small team can actually run"], size=12)

# ---------------------------------------------------------------- 4. RQs
s = prs.slides.add_slide(layout(L_2COL))
settext(ph(s, 20), "2. Research questions", size=12)
settext(ph(s, 0),  "Probing the effect, limits, and design of SKILL.md", size=18)
settext(ph(s, 11), "Three research questions", size=17)
settext(ph(s, 16), "Questions", size=14, bold=True)
settext(ph(s, 17), ["RQ1  Does a domain-specific skill improve resolution quality over no skill?",
                    "",
                    "RQ2  Does a small model with a skill perform as well as a large model "
                    "without one?",
                    "",
                    "RQ3  What makes a skill effective — and how do you know what to keep?"],
        size=12)
settext(ph(s, 18), "Setup", size=14, bold=True)
settext(ph(s, 19), ["• 4 open-weight models, 2 scales: Apertus-8B / 70B · Qwen3-8B / 32B",
                    "• 3 benchmarks: ConGra, SALLM (security), SWE-bench Lite (repair)",
                    "• Conditions: no-skill baseline vs. skill as system prompt",
                    "• Solved = max(edit, winnowing) > 0.8, single greedy draw"], size=12)

# ---------------------------------------------------------------- 5. method
s = prs.slides.add_slide(layout(L_TITLE))
head(s, "A three-stage skill design loop",
        "Only stage 2 iterates — stage 3 runs on the full benchmark")
place_image(s, os.path.join(FIG, "skill_design_loop.png"), 0.59, 1.95, 5.30, 3.45)
note(s, 6.15, 2.05, 3.30, 3.20,
     ["Stage 1 — no-skill baseline: what the model",
      "already does unaided.",
      "",
      "Stage 2 — write → pilot → analyze. The only",
      "stage that iterates. 20 conflicts (python/func),",
      "both 8B models, 3 conditions.",
      "",
      "Stage 3 — every surviving version runs on the",
      "full benchmark: python-tiny, 3,597 conflicts",
      "per model.",
      "",
      "Three versions reached stage 3:",
      "v1 (control), v2, v2.1."])

# ---------------------------------------------------------------- 6. RQ1
s = prs.slides.add_slide(layout(L_TITLE))
head(s, "RQ1  Does a domain-specific skill improve resolution quality?",
        "Only for the small, weak model — Apertus-8B +7.1 pp")
place_image(s, os.path.join(FIG, "rq1_baseline_vs_v2.1_sys_max.png"), 0.59, 1.95, 4.55, 3.45)
note(s, 5.45, 2.00, 4.00, 3.30,
     ["Solved-rate Δ vs. each model's own baseline (v2.1, sys):",
      "",
      "   Apertus-8B    21.5%    +7.10 pp      the only clear win",
      "   Qwen3-8B      29.2%     −0.86 pp",
      "   Apertus-70B   31.5%     −2.70 pp",
      "   Qwen3-32B     38.4%     −0.42 pp",
      "",
      "n = 3,597 per model, python-tiny.",
      "",
      "Apertus-70B is the same family scaled up and is still",
      "harmed — so this is not a model-family effect.",
      "",
      "The benefit holds only while the model is genuinely",
      "weak; once it is competent, the skill is neutral to",
      "harmful."])

# ---------------------------------------------------------------- 7. RQ2
s = prs.slides.add_slide(layout(L_TITLE))
head(s, "RQ2  Does a small model with a skill match a large one without?",
        "Almost, for Apertus — 71% of the gap closed; for Qwen3 the gap widens")
place_image(s, os.path.join(OFIG, "skill_vs_scale_violin_apertus_v2.1_vs_70b.png"),
            0.59, 2.00, 5.55, 2.75)
note(s, 6.30, 2.00, 3.15, 3.30,
     ["Apertus",
      "   8B 21.47 → +skill 28.57",
      "   vs 70B 31.52",
      "   gap 10.05 pp, recovered +7.10,",
      "   residual +2.95 → closure +71%",
      "   positive in all 7 buckets,",
      "   overtakes the 70B in 2",
      "",
      "Qwen3",
      "   8B 29.16 → +skill 28.30",
      "   vs 32B 38.57",
      "   closure −9%: the gap widens",
      "",
      "SWE-bench Lite: within 1.3 pp on",
      "apply failures (56% vs 57%); 95% CI",
      "rules out a residual gap over ~7 pp."])

# ---------------------------------------------------------------- 8. cross-benchmark
s = prs.slides.add_slide(layout(L_2COL))
settext(ph(s, 20), "4. Results — generalization", size=12)
settext(ph(s, 0),  "The same pattern holds on security and bug repair", size=18)
settext(ph(s, 11), "The score moves only when the skill's target is the binding constraint",
        size=17)
settext(ph(s, 16), "SALLM — security, 8B pair, 55 reliable tasks", size=13, bold=True)
settext(ph(s, 17), ["• Secure tasks rise sharply: Qwen3-8B +13, Apertus-8B +10",
                    "• Functional correctness falls: 37→29 and 29→22",
                    "• Net correct and secure barely moves: 13→17, 10→11",
                    "• The correctness oracle is the binding constraint, so the security "
                    "win never reaches the headline number"], size=12)
settext(ph(s, 18), "SWE-bench Lite — repair, all 4 models, n = 300", size=13, bold=True)
settext(ph(s, 19), ["• Patch-apply failures fall for 3 of 4 models",
                    "• Resolved counts barely move — and not on the same instances",
                    "• The skill fixes patch formatting, not the ability to find the bug",
                    "",
                    "⇒  skill benefit = (the mechanical fix works)",
                    "        × (that deficiency is what actually limits the model)"], size=12)

# ---------------------------------------------------------------- 9. RQ3
s = prs.slides.add_slide(layout(L_TITLE))
head(s, "RQ3  What actually makes a skill work",
        "Four rules, derived from the stage-2 case analysis")
place_image(s, os.path.join(FIG, "Key_differences_between_skills_v1_v2_v2_1.png"),
            0.59, 3.55, 8.85, 1.75)
note(s, 0.59, 1.95, 8.85, 1.60,
     ["1.  More skill text is not automatically better — every sentence must change behaviour in an identifiable "
      "class of cases. v1 (the control) hurt Qwen3-8B.",
      "2.  The gains came from constraint, not instruction — output discipline did the work, not the "
      "pick/combine/empty taxonomy. v2.1 was reframed accordingly.",
      "3.  A constraint the model cannot check is not enforced — the |a|+|b| character cap was exceeded by 11 of 20 "
      "outputs, worst case by 21×. Replaced by a post-hoc self-check.",
      "4.  Placement matters as much as content — rules are read top-down. \"One side empty → pick\" sat at the "
      "bottom and never fired; hoisting it into step 1 fixed 2 of 5 Qwen3 losses."])

# ---------------------------------------------------------------- 10. conclusion
s = prs.slides.add_slide(layout(L_2COL))
settext(ph(s, 20), "6. Conclusion", size=12)
settext(ph(s, 0),  "Contribution, threats, and what I would do next", size=18)
settext(ph(s, 11), "A skill helps a weak model; the loop tells you what to keep", size=17)
settext(ph(s, 16), "Threats to validity", size=14, bold=True)
settext(ph(s, 17), ["• Edit similarity is a proxy — optimising against it invites Goodhart's law",
                    "• The full benchmark did double duty: it settled the keep decisions and "
                    "reported the results",
                    "• Single greedy draw at temperature 0.0, no error bars",
                    "• The four rules come from 20 conflicts, one language, two 8B models"],
        size=12)
settext(ph(s, 18), "Contribution", size=14, bold=True)
settext(ph(s, 19), ["• A designed, versioned skill and a reusable three-stage loop for "
                    "deciding what to keep",
                    "• Evidence across three benchmarks that skill benefit is a pairing "
                    "property, not a property of the skill",
                    "• Next: multi-sample error bars, the SALLM large pair, and automated "
                    "authoring — a generator needs a keep criterion just as an author does"],
        size=12)

prs.save(OUT)
print("saved:", OUT, "|", len(prs.slides._sldIdLst), "slides")
