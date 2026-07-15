"""Publish the real workflow notebooks as standalone HTML into the built site.

This layers every "real" research notebook under ``workflow/`` into the Quarto
build output as self-contained HTML, so the ``.../notebooks/<stage>/<name>.html``
links that the curated docs point at actually resolve.

BUILD ORDER (important)
-----------------------
Run this **AFTER** ``quarto render docs`` (the book/site build). That render
writes and cleans ``docs/_build/html/``; this script then layers the notebooks
into its ``notebooks/`` subdirectory. Running it before the render would just
have the notebooks wiped out again.

What it does
------------
- Walks ``workflow/`` for ``*.ipynb`` and keeps only "real" notebooks: any
  notebook whose relative path (under ``workflow/``) has a path component
  starting with ``_`` is excluded (drops ``_archive/``, ``_templates/``,
  ``_create_readme.ipynb`` and the in-stage ``_TEMPLATE_FULL_RPC_.ipynb``).
  ``.ipynb_checkpoints`` is skipped too.
- Converts each to standalone HTML with embedded images/outputs via nbconvert's
  ``HTMLExporter`` (``embed_images=True``, ``lab`` template). Notebooks are
  **never executed** -- they read an offline data folder and already carry
  committed cell outputs.
- Mirrors the ``workflow/`` folder structure under the output ``notebooks/`` dir.
- Generates an ``index.html`` landing page listing every converted notebook,
  grouped by top-level stage folder.

Usage
-----
    uv run python build_notebooks.py                # writes to the real build dir
    uv run python build_notebooks.py <output_dir>   # writes to a scratch dir

We use nbconvert (not Quarto) on purpose: Quarto tries to parse a notebook's
leading markdown cell as YAML front-matter and chokes on arbitrary research
notebooks.
"""

from __future__ import annotations

import sys
from pathlib import Path

from nbconvert import HTMLExporter
from traitlets.config import Config

# --- Configuration ----------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent
WORKFLOW_DIR = REPO_ROOT / "workflow"

# Self-contained (no external assets) lightbox injected into every notebook HTML.
# Clicking any rendered output/markdown image opens it enlarged in an overlay;
# click anywhere or press Esc to close.
LIGHTBOX_SNIPPET = """
<style>
  .jp-OutputArea-output img, .jp-RenderedImage img, .jp-RenderedMarkdown img { cursor: zoom-in; }
  .nb-lightbox { position: fixed; inset: 0; z-index: 9999; display: none;
                 align-items: center; justify-content: center; padding: 2rem;
                 background: rgba(0, 0, 0, 0.85); cursor: zoom-out; }
  .nb-lightbox.open { display: flex; }
  .nb-lightbox img { max-width: 100%; max-height: 100%;
                     box-shadow: 0 0 40px rgba(0, 0, 0, 0.5); }
</style>
<div class="nb-lightbox" id="nb-lightbox"><img alt=""></div>
<script>
  (function () {
    var overlay = document.getElementById("nb-lightbox");
    var big = overlay.querySelector("img");
    function close() { overlay.classList.remove("open"); big.removeAttribute("src"); }
    document.addEventListener("click", function (e) {
      var img = e.target;
      if (img.tagName === "IMG" && !img.closest(".nb-lightbox") &&
          img.closest(".jp-OutputArea-output, .jp-RenderedImage, .jp-RenderedMarkdown")) {
        big.src = img.currentSrc || img.src;
        overlay.classList.add("open");
      }
    });
    overlay.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  })();
</script>
"""


def inject_lightbox(body: str) -> str:
    """Insert the self-contained lightbox just before the closing </body>."""
    marker = "</body>"
    idx = body.rfind(marker)
    if idx == -1:  # unexpected, but don't lose the document
        return body + LIGHTBOX_SNIPPET
    return body[:idx] + LIGHTBOX_SNIPPET + body[idx:]

# Default output: the notebooks/ subdir of the Quarto build output. Override
# with a single positional CLI arg to verify against a scratch dir without
# clobbering the shared build directory.
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs" / "_build" / "html" / "notebooks"


def is_included(rel_path: Path) -> bool:
    """True if the notebook is a "real" one that should be published.

    Excludes any notebook that lives under a path component starting with ``_``
    (``_archive/``, ``_templates/``, ``_create_readme.ipynb``,
    ``_TEMPLATE_FULL_RPC_.ipynb``) and anything under ``.ipynb_checkpoints``.
    """
    for part in rel_path.parts:
        if part.startswith("_"):
            return False
        if part == ".ipynb_checkpoints":
            return False
    return True


def discover_notebooks(workflow_dir: Path) -> tuple[list[Path], list[Path]]:
    """Return (included, excluded) notebook paths relative to ``workflow_dir``."""
    included: list[Path] = []
    excluded: list[Path] = []
    for nb in sorted(workflow_dir.rglob("*.ipynb")):
        rel = nb.relative_to(workflow_dir)
        (included if is_included(rel) else excluded).append(rel)
    return included, excluded


def build_exporter() -> HTMLExporter:
    """HTMLExporter that embeds images and never executes the notebook."""
    config = Config()
    # Embed base64 images/outputs so each HTML file is fully self-contained.
    config.HTMLExporter.embed_images = True
    # Explicitly ensure no execution preprocessor is attached.
    config.HTMLExporter.preprocessors = []
    exporter = HTMLExporter(config=config, template_name="lab")
    return exporter


def convert_notebook(exporter: HTMLExporter, src: Path, dst: Path) -> list[str]:
    """Convert one notebook to standalone HTML. Returns captured warnings."""
    import warnings

    dst.parent.mkdir(parents=True, exist_ok=True)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        body, _resources = exporter.from_filename(str(src))
        messages = [str(w.message) for w in caught]
    dst.write_text(inject_lightbox(body), encoding="utf-8")
    return messages


def render_index(included: list[Path], output_dir: Path) -> Path:
    """Write a self-contained index.html grouping links by top-level stage."""
    # Group by top-level stage folder (first path component).
    groups: dict[str, list[Path]] = {}
    for rel in included:
        stage = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        groups.setdefault(stage, []).append(rel)

    def esc(text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    parts: list[str] = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>CH-LAE workflow notebooks</title>",
        "<style>",
        "  :root { color-scheme: light dark; }",
        "  body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;",
        "         max-width: 60rem; margin: 2rem auto; padding: 0 1.25rem;",
        "         line-height: 1.5; }",
        "  h1 { font-size: 1.6rem; margin-bottom: 0.25rem; }",
        "  p.lead { color: #666; margin-top: 0; }",
        "  h2 { font-size: 1.15rem; margin-top: 2rem; padding-bottom: 0.25rem;",
        "       border-bottom: 1px solid #ccc; }",
        "  ul { list-style: none; padding-left: 0; }",
        "  li { margin: 0.25rem 0; }",
        "  a { text-decoration: none; }",
        "  a:hover { text-decoration: underline; }",
        "  code { font-size: 0.9em; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>CH-LAE flux product &mdash; workflow notebooks</h1>",
        f'<p class="lead">{len(included)} notebooks, grouped by processing stage.</p>',
    ]

    for stage in sorted(groups):
        parts.append(f"<h2>{esc(stage)}</h2>")
        parts.append("<ul>")
        for rel in sorted(groups[stage]):
            href = rel.with_suffix(".html").as_posix()
            parts.append(f'  <li><a href="{esc(href)}"><code>{esc(rel.as_posix())}</code></a></li>')
        parts.append("</ul>")

    parts += ["</body>", "</html>"]

    index_path = output_dir / "index.html"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(parts), encoding="utf-8")
    return index_path


def main(argv: list[str]) -> int:
    output_dir = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_OUTPUT_DIR

    if not WORKFLOW_DIR.is_dir():
        print(f"ERROR: workflow dir not found: {WORKFLOW_DIR}", file=sys.stderr)
        return 1

    included, excluded = discover_notebooks(WORKFLOW_DIR)
    exporter = build_exporter()

    print(f"Output directory : {output_dir}")
    print(f"Included         : {len(included)} notebooks")
    print(f"Excluded (_*)    : {len(excluded)} notebooks")
    print("-" * 60)

    converted = 0
    warnings_by_nb: dict[str, list[str]] = {}
    for rel in included:
        src = WORKFLOW_DIR / rel
        dst = output_dir / rel.with_suffix(".html")
        try:
            msgs = convert_notebook(exporter, src, dst)
        except Exception as exc:  # keep going, but surface the failure loudly
            print(f"  FAILED  {rel.as_posix()}: {exc}", file=sys.stderr)
            continue
        converted += 1
        if msgs:
            warnings_by_nb[rel.as_posix()] = msgs
        print(f"  ok      {rel.as_posix()}")

    index_path = render_index(included, output_dir)

    # --- Summary ------------------------------------------------------------
    print("-" * 60)
    print(f"Converted        : {converted}/{len(included)} notebooks")
    print(f"Index page       : {index_path}")
    print(f"Output location  : {output_dir}")

    if warnings_by_nb:
        print(f"\nnbconvert warnings ({len(warnings_by_nb)} notebook(s)):")
        for name, msgs in warnings_by_nb.items():
            for msg in msgs:
                print(f"  - {name}: {msg}")
    else:
        print("\nnbconvert warnings: none")

    print(f"\nExcluded (_*) notebooks ({len(excluded)}):")
    for rel in excluded:
        print(f"  - {rel.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
