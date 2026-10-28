#!/usr/bin/env python3
"""Batch-rename pic/mv skill families across BOTH skill libraries.

Usage:
    python3 rename_skill_family.py picbpreal3:picbpwjw picbpreal2:picbpbookroom picbpreal:picbpgd
    python3 rename_skill_family.py --dry-run picrun:picbprun

Why this exists (three bugs it prevents):
  1. Order: replacing a bare name first eats numbered siblings —
     `picbpreal` -> `picbpgd` turns `picbpreal2` into `picbpgd2`.
     Pairs are therefore applied longest-old-name-first.
  2. Boundary: naive substring replace hits foreign skills that merely
     contain the old name (`picsun` inside `picsunny`/`mvpicsun`;
     `picbpreal` inside `picgirlreal` is safe only because of the letter
     before it, not because of word structure). A word-boundary regex is used.
  3. Two libraries: default (`~/.hermes/skills/`) is the source of truth and
     learn (`~/.hermes/profiles/<profile>/skills/`) holds independent copies
     with their own family lists. Both are rewritten and both are re-checked.

What it does NOT fix: historical strings that legitimately contain the old
name — `/tmp/<old>_v2_backup.md` paths, body notes like "原 <old> 版", and
selection tables keyed by the old style. After running, grep the new name,
read those lines, and restore the old spelling there by hand.

Exit code 1 if any old name still appears in skill .md files afterwards.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

DEFAULT_LIB = pathlib.Path.home() / ".hermes" / "skills"
LEARN_ROOT = pathlib.Path.home() / ".hermes" / "profiles"
# Hermes bookkeeping files keep historical records on purpose; never rewrite them.
SKIP_NAMES = {".usage.json", ".curator_ledger.jsonl"}


def skill_libs() -> list[pathlib.Path]:
    libs = [DEFAULT_LIB]
    if LEARN_ROOT.exists():
        libs.extend(p / "skills" for p in sorted(LEARN_ROOT.iterdir()) if (p / "skills").exists())
    return [p for p in libs if p.exists()]


def parse_pairs(raw: list[str]) -> list[tuple[str, str]]:
    pairs = []
    for item in raw:
        if ":" not in item:
            sys.exit(f"bad pair {item!r}; expected old:new")
        old, new = (s.strip() for s in item.split(":", 1))
        if not old or not new:
            sys.exit(f"bad pair {item!r}; both sides required")
        if old == new:
            sys.exit(f"no-op pair {item!r}")
        pairs.append((old, new))
    # Longest old name first so a bare name never eats its numbered siblings.
    return sorted(pairs, key=lambda p: len(p[0]), reverse=True)


def rename_dirs(libs: list[pathlib.Path], pairs: list[tuple[str, str]], dry: bool) -> None:
    for lib in libs:
        for old, new in pairs:
            hits = [d for d in lib.rglob(old) if d.is_dir()]
            for src in hits:
                dst = src.with_name(new)
                if dst.exists():
                    print(f"!! {dst} already exists, skipping dir rename")
                    continue
                print(f"{'[dry] ' if dry else ''}dir {src} -> {dst}")
                if not dry:
                    src.rename(dst)


def rewrite(libs: list[pathlib.Path], pairs: list[tuple[str, str]], dry: bool) -> int:
    """Rewrite references; returns count of files touched."""
    touched = 0
    for lib in libs:
        for f in lib.rglob("*.md"):
            if f.name in SKIP_NAMES:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            orig = text
            for old, new in pairs:
                # Not preceded/followed by an identifier char or hyphen.
                text = re.sub(rf"(?<![A-Za-z0-9_-]){re.escape(old)}(?![A-Za-z0-9_-])", new, text)
            if text != orig:
                print(f"{'[dry] ' if dry else ''}edit {f}")
                touched += 1
                if not dry:
                    f.write_text(text, encoding="utf-8")
    return touched


def residual(libs: list[pathlib.Path], pairs: list[tuple[str, str]]) -> int:
    """Report files still containing an old name (excludes bookkeeping files)."""
    total = 0
    for lib in libs:
        for f in lib.rglob("*.md"):
            if f.name in SKIP_NAMES:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for old, _ in pairs:
                if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(old)}(?![A-Za-z0-9_-])", text):
                    print(f"residual {old} in {f}")
                    total += 1
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pairs", nargs="+", help="old:new ...")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pairs = parse_pairs(args.pairs)
    libs = skill_libs()
    print("libraries:")
    for lib in libs:
        print(f"  {lib}")
    print("order:", " -> ".join(f"{o}:{n}" for o, n in pairs))

    rename_dirs(libs, pairs, args.dry_run)
    touched = rewrite(libs, pairs, args.dry_run)
    print(f"files touched: {touched}")

    if args.dry_run:
        print("dry run: nothing written")
        return 0

    left = residual(libs, pairs)
    if left:
        print("\nFix these by hand — historical backup paths and "
              "\"originally named X\" notes must keep the old spelling,")
        print("while stale selection-table keys should be rewritten to the current style.")
        return 1
    print("no residual references; remember to grep every surviving skill's family list "
          "and to `diff` default vs learn copies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
