"""
test_score.py — regression test for pilot.py:score() (issue #39)

Runs the 4 acceptance-criteria cases from issue #39. Run from repo root:

    python scripts/test_score.py
"""

from pilot import score


def check(label: str, got: dict, expected: dict) -> bool:
    ok = got == expected
    status = "PASS" if ok else "FAIL"
    print(f"{status}  {label}")
    if not ok:
        print(f"      expected: {expected}")
        print(f"      got:      {got}")
    return ok


def main() -> int:
    results = [
        check(
            'score("", "")  -> pass (Empty pattern correctly applied)',
            score("", ""),
            {"edit": 1.0, "winnowing": 1.0, "empty": False},
        ),
        check(
            'score("", "non-empty")  -> empty flag (model produced nothing, GT expected content)',
            score("", "some content"),
            {"edit": None, "winnowing": None, "empty": True},
        ),
        check(
            'score("non-empty", "")  -> fail (model produced content where GT was empty)',
            score("some content", ""),
            {"edit": 0.0, "winnowing": 0.0, "empty": False},
        ),
        check(
            'score(identical non-empty strings)  -> edit=1.0, winnowing=1.0',
            # Needs >= 8 chars after whitespace removal for winnowing
            # (k=5 5-grams, w=4 window) to produce a non-empty fingerprint.
            score("foo = 1\nbar = 2\nbaz = 3\n", "foo = 1\nbar = 2\nbaz = 3\n"),
            {"edit": 1.0, "winnowing": 1.0, "empty": False},
        ),
        # Whitespace-only resolution must be treated as empty.
        check(
            'score("   \\n", "")  -> pass (whitespace-only counts as empty)',
            score("   \n", ""),
            {"edit": 1.0, "winnowing": 1.0, "empty": False},
        ),
    ]
    failed = sum(1 for r in results if not r)
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
