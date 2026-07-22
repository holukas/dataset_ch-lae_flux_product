"""Fail if any name from the fieldbook redaction map appears anywhere in this repository.

The GIN fieldbook signs its entries with the names of the people who did the work. Those names
are personal data and this repository is published as a website, so they must not survive into a
notebook (in a cell's source, in its stored output, or in a traceback), into a narrative page, or
into a code comment.

The map itself lives outside the repository, beside the export it belongs to, so this checker
needs no name of its own.

    uv run python check_no_names.py            # scan, print where, exit 1 if anything found
    uv run python check_no_names.py --quiet    # print locations only, never the name itself

`docs/index.md` is skipped: its acknowledgements are deliberate published credit, not a leak.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
DEFAULT_MAP = Path(r"F:\Sync\luhk_work\dev-data\datasets-data"
                   r"\dataset_ch-lae_flux_product-data\fieldbook_gin\redact_names.csv")

# Deliberate exceptions, and build/vendor trees that are not ours to police.
SKIP_FILES = {"docs/index.md",           # acknowledgements: published credit, not a leak
              "docs/References.md"}      # a bibliography is nothing but names, by definition
SKIP_PARTS = {".venv", ".git", "_build", "node_modules", ".ipynb_checkpoints",
              "docs/notebooks"}          # staged build copies of the real notebooks
SUFFIXES = {".ipynb", ".md", ".qmd", ".py", ".yml", ".yaml", ".ps1"}

# Some people in the fieldbook are also published authors and photographers, and crediting them
# is the opposite of leaking them. Rather than skipping whole pages - which would also hide a
# genuine fieldbook quote added to them later - a single LINE is exempt when it is visibly a
# citation or a credit. Anything else on the page is still checked.
CREDIT_LINE = re.compile(r"et al\.|Photo:|doi\.org|https?://")


def load_names(map_path: Path) -> dict[str, str]:
    """Load the surface forms to search for.

    Raises rather than returning nothing: a checker that silently finds no names to look for
    would pass every file in the repository and report success.
    """
    if not map_path.is_file():
        raise FileNotFoundError(
            f"the redaction map is missing: {map_path}. Without it this checker cannot know what "
            f"to look for, and passing would mean nothing. Restore it or pass --map.")
    with map_path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    names = {r["name"].strip(): r["pseudonym"].strip() for r in rows if r.get("name", "").strip()}
    if not names:
        raise ValueError(f"{map_path}: holds no names.")
    return names


def texts_of(path: Path):
    """Yield (location, text) for everything in a file that could carry a name."""
    if path.suffix != ".ipynb":
        yield "", path.read_text(encoding="utf-8", errors="replace")
        return
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"  (!) {path}: unreadable notebook ({exc})")
        return
    for i, cell in enumerate(nb.get("cells", [])):
        yield f"cell {i} source", "".join(cell.get("source", []))
        for out in cell.get("outputs", []) or []:
            if "text" in out:
                yield f"cell {i} output", "".join(out["text"])
            for key in ("text/plain", "text/html", "text/markdown"):
                if key in out.get("data", {}):
                    yield f"cell {i} output", "".join(out["data"][key])
            if "traceback" in out:
                yield f"cell {i} traceback", "\n".join(out["traceback"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", type=Path, default=DEFAULT_MAP,
                    help="the name -> pseudonym csv (default: beside the GIN export)")
    ap.add_argument("--quiet", action="store_true",
                    help="report locations but never echo the name (for shared logs)")
    args = ap.parse_args()

    names = load_names(args.map)
    # Longest first so a report names the fullest form it can rather than a fragment of it.
    rx = re.compile(r"(?<!\w)(" + "|".join(re.escape(n) for n in
                                           sorted(names, key=len, reverse=True)) + r")(?!\w)")

    hits, scanned = [], 0
    for path in sorted(REPO.rglob("*")):
        if path.suffix not in SUFFIXES or not path.is_file():
            continue
        rel = path.relative_to(REPO).as_posix()
        if rel in SKIP_FILES or any(part in rel.split("/") or part in rel for part in SKIP_PARTS):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        scanned += 1
        for where, text in texts_of(path):
            # Line by line, so that one citation does not exempt the rest of the page.
            for line in text.split("\n"):
                if CREDIT_LINE.search(line):
                    continue
                for m in rx.finditer(line):
                    hits.append((rel, where, m.group(1)))

    print(f"checked {scanned} file(s) against {len(names)} surface forms "
          f"({len(set(names.values()))} people)")
    if not hits:
        print("OK - no fieldbook names found in the repository.")
        return 0

    print(f"\n(!) {len(hits)} occurrence(s) of a fieldbook name:\n")
    for rel, where, name in hits:
        shown = "<redacted>" if args.quiet else repr(name)
        print(f"    {rel}{'  ' + where if where else ''}: {shown}")
    print("\nReplace each with its pseudonym from the map, or - if it is deliberate published "
          "credit - add the file to SKIP_FILES above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
