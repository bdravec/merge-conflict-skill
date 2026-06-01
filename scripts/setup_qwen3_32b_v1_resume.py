"""Set up a filtered resume for the qwen3-32b v1 python-tiny run (refs #75, #80).

The 2026-06-01 run hung at ~3123/3604 cases on a single wedged vLLM request
(no client timeout — fixed in #80). Every remaining case is in the
text+sytx+func bucket. This builds a disposable temp data-root containing only
the not-yet-done cases (symlinked hash files + a filtered meta_list.txt), then
prints the exact pilot.py command to finish them on the hardened runner.

Nothing in ConGra is mutated; the temp data-root is safe to delete afterwards.

Usage (on the box holding the data + the partial jsonl):
    python scripts/setup_qwen3_32b_v1_resume.py            # build + print command
    python scripts/setup_qwen3_32b_v1_resume.py --dry-run  # report only, no FS changes
"""
import argparse
import json
from pathlib import Path

HERE        = Path(__file__).resolve().parent
CONGRA_ROOT = (HERE / "../../ConGra").resolve()
RESULTS     = HERE / "results"

BUCKET = "text+sytx+func"
LANG   = "python"

MAIN_JSONL = RESULTS / "pilot_results_qwen3-32b_v1_python_tiny.jsonl"
BUCKET_DIR = CONGRA_ROOT / "data" / "congra_tiny_datasets" / LANG / BUCKET
RESUME_DIR = CONGRA_ROOT / "data" / "congra_tiny_datasets" / LANG / f"{BUCKET}__resume"
RESUME_TAG = "v1_python_tiny_tsf_resume"


def done_case_ids() -> set[str]:
    """case_ids already present for this bucket in the partial run."""
    done = set()
    with MAIN_JSONL.open() as f:
        for line in f:
            r = json.loads(line)
            # the original run was --bucket all (multi_bucket), so rows carry "bucket"
            if r.get("bucket") == BUCKET:
                done.add(r["case_id"])
    return done


def parse_meta() -> list[tuple[str, str]]:
    """Return [(raw_line, hash_idx), ...] for every case in the bucket meta_list."""
    out = []
    for line in (BUCKET_DIR / "meta_list.txt").read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(": ")
        if len(parts) != 3:
            continue
        out.append((line, parts[1]))  # parts[1] == hash_idx == case_id
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Report counts and the resume command without writing anything.")
    args = ap.parse_args()

    done = done_case_ids()
    meta = parse_meta()
    kept = [(line, h) for line, h in meta if h not in done]

    print(f"bucket {BUCKET}: total {len(meta)}, done {len(done)}, remaining {len(kept)}")

    # sanity: every done id should be a real case in this bucket
    stray = done - {h for _, h in meta}
    if stray:
        print(f"WARNING: {len(stray)} done case_ids not found in {BUCKET} meta_list "
              f"(first few: {sorted(stray)[:3]})")

    if not kept:
        print("Nothing to resume — bucket already complete.")
        return

    if args.dry_run:
        print("\n--dry-run: not writing the resume data-root.")
    else:
        RESUME_DIR.mkdir(parents=True, exist_ok=True)
        # clear any stale symlinks / meta from a previous attempt
        for e in RESUME_DIR.iterdir():
            if e.is_symlink() or e.name == "meta_list.txt":
                e.unlink()
        for _line, h in kept:
            (RESUME_DIR / h).symlink_to(BUCKET_DIR / h)
        (RESUME_DIR / "meta_list.txt").write_text(
            "\n".join(line for line, _ in kept) + "\n")
        print(f"wrote resume data-root: {RESUME_DIR}  ({len(kept)} cases)")

    print("\nResume command (run on the RTX 6000 after `git pull`):\n")
    print(f"python scripts/pilot.py \\\n"
          f"  --model qwen3-32b --skill-version v1 \\\n"
          f"  --bucket {BUCKET} \\\n"
          f"  --data-root {RESUME_DIR} \\\n"
          f"  --n-cases all --tag {RESUME_TAG} \\\n"
          f"  --concurrency 2 --max-prompt-tokens 30720")


if __name__ == "__main__":
    main()
