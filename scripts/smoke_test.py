"""
Smoke test for the ConGra evaluation pipeline.

Tests the metrics (edit similarity, winnowing similarity) in isolation —
without running an LLM. Uses one sample from the tiny dataset.

Three cases:
  1. Perfect resolution (ground truth as input) → expect ~1.0
  2. Empty resolution → expect 0.0
  3. Dummy wrong resolution → expect low score

Run from the src/ directory:
    python smoke_test.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from metrics import metric_edit_distance, metric_winnowing
from utils import load_conflict_and_answer

# --- Pick one sample from tiny dataset (python/func) ---
DATA_ROOT = "../data/congra_tiny_datasets/python/func"
META_LIST = os.path.join(DATA_ROOT, "meta_list.txt")

# Read the first entry from meta_list
with open(META_LIST, "r") as f:
    first_line = f.readline().strip()

source_rel_path, hash_idx, conflict_idx = first_line.split(": ")
conflict_idx = int(conflict_idx)

# Build full paths
source_path = os.path.join("../data/raw_datasets", source_rel_path)
source_path = source_path.replace("merged_without_base", "regions")
file_path = os.path.join(DATA_ROOT, hash_idx)

print("=" * 60)
print("ConGra Evaluation Pipeline — Smoke Test")
print("=" * 60)
print(f"Sample:        {hash_idx}")
print(f"Conflict type: func")
print(f"Language:      python")
print(f"Conflict idx:  {conflict_idx}")
print()

# Load conflict and ground truth
conflict_context, conflict_text, resolved_text = load_conflict_and_answer(
    source_path, file_path, conflict_idx, n=5
)

print(f"Conflict region ({len(conflict_text.splitlines())} lines):")
print("-" * 40)
print(conflict_text[:500] + ("..." if len(conflict_text) > 500 else ""))
print()
print(f"Ground truth resolution ({len(resolved_text.splitlines())} lines):")
print("-" * 40)
print(resolved_text[:500] + ("..." if len(resolved_text) > 500 else ""))
print()

# --- Case 1: Perfect resolution (ground truth == resolution) ---
edit_perfect   = metric_edit_distance(resolved_text, resolved_text)
winnow_perfect = metric_winnowing(resolved_text, resolved_text)

# --- Case 2: Empty resolution ---
edit_empty   = metric_edit_distance("", resolved_text)
winnow_empty = metric_winnowing("", resolved_text)

# --- Case 3: Dummy wrong resolution ---
dummy = "pass"
edit_dummy   = metric_edit_distance(dummy, resolved_text)
winnow_dummy = metric_winnowing(dummy, resolved_text)

THRESHOLD = 0.8

def result(score):
    return "PASS ✓" if score >= THRESHOLD else "fail ✗"

print("=" * 60)
print("Results")
print("=" * 60)
print(f"{'Case':<30} {'Edit sim':>10} {'Winnowing':>10}  {'Verdict'}")
print("-" * 60)
print(f"{'Perfect (ground truth)':30} {edit_perfect:>10.4f} {winnow_perfect:>10.4f}  {result(max(edit_perfect, winnow_perfect))}")
print(f"{'Empty string':30} {edit_empty:>10.4f} {winnow_empty:>10.4f}  {result(max(edit_empty, winnow_empty))}")
dummy_label = 'Dummy ("pass")'
print(f"{dummy_label:<30} {edit_dummy:>10.4f} {winnow_dummy:>10.4f}  {result(max(edit_dummy, winnow_dummy))}")
print()
print("Note: a resolution is considered correct if at least one metric >= 0.8")
print()
print("Note: semantic similarity (cosine via code embeddings) is defined in")
print("metrics.py but is NOT called by main.py. It requires a GPU-loaded")
print("embedding model and would need to be wired in separately.")
