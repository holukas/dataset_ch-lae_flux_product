"""Render the GIN fieldbook export as one readable, redacted markdown file.

The export beside this repository is a csv whose body is HTML, whose entries are signed with the
names of the people who did the work, and whose older entries carry network configuration and
account names. None of that can be read comfortably and none of it can be shared as it stands.
This script produces the readable form: one markdown file, entries in chronological order, with

  * every person replaced by the stable pseudonym the redaction map gives them (the same map the
    product notebooks use, so `person 01` means the same person here as there),
  * e-mail addresses, IP addresses, account names and remote-access ports removed,
  * the HTML flattened, the Word paste-in boilerplate dropped and the mojibake repaired,
  * the legacy block - 94 sub-entries from 2006-2011 pasted into a single row dated 2011-06-03
    when GIN was introduced - split back out and filed under its own dates.

Two nets guard the redaction. The narrow one is the notebooks' own `audit_unmapped_names()`: a
name-shaped token in the author parenthesis or in a `with X` byline that survived redaction
**raises**. The wide one lists every capitalised token left standing anywhere in the text, minus
the device vocabulary of the export itself and minus anything that also occurs lowercase; it
cannot raise - it holds ~600 technical terms - so it writes its candidates to a file beside the
map and prints only the count. The wide list is what found the 53 unmapped surface forms the map
gained when this script was written, so it is worth reading after an export with new entries.

Neither net prints a candidate: an unmapped token is most likely a real name, and this script's
output is read in a terminal and pasted into tickets.

    uv run python build_fieldbook_md.py                  # newest export, entries up to 2025-12-31
    uv run python build_fieldbook_md.py --until 2026-12-31
    uv run python build_fieldbook_md.py --out somewhere.md
"""
from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import pandas as pd

FIELDBOOK_DIR = Path(r"F:\Sync\luhk_work\dev-data\datasets-data"
                     r"\dataset_ch-lae_flux_product-data\fieldbook_gin")
EXPORT_GLOB = "CH-LAE-laegeren-export_*.csv"
DEFAULT_UNTIL = "2025-12-31"

# The legacy fieldbook, pasted into GIN as one row when the system was introduced. Its 94
# sub-entries carry their dates in the text, so a date filter over the export cannot see them.
LEGACY_MARKER = "Additional old fieldbook entries"

# Parts of the export are UTF-8 that has been through a single-byte round trip, so an umlaut
# arrives as the two or three characters its UTF-8 bytes were read as. Repairing it by table was
# the first attempt and it missed half of them: the same byte turns up both as its cp1252
# character and as the raw C1 control, and only one of those is spellable in a source file.
MOJIBAKE_RX = re.compile(r"[ÃâÂ][\x80-ſ]{1,2}")

# The record writes a name in lower case now and then ('advised eugenie to free some memory'), so
# redaction gets a second, case-insensitive pass. It runs on the longer surface forms only: the
# map holds four-letter ones that are ordinary words once lowercased, and a case-insensitive pass
# over those would eat the prose. A few longer forms are ordinary German words as well - they are
# listed in a file beside the map, since naming them here would put a real surname in this
# repository, which is the thing the map exists to prevent.
CI_MIN_LEN = 5
CI_EXCLUDE_FILE = "redact_ci_exclude.csv"


# ---------------------------------------------------------------------------------------------
# redaction
# ---------------------------------------------------------------------------------------------
def load_ci_exclusions(path: Path) -> set:
    """Load the surface forms that must be matched case-sensitively only.

    Raises if the file is missing rather than defaulting to 'exclude nothing'. The failure that
    would follow is quiet: every lowercase occurrence of an ordinary word that happens to also be
    somebody's surname would be replaced by a pseudonym, and the result still reads like prose.
    """
    if not path.is_file():
        raise FileNotFoundError(
            f"the case-insensitive exclusion list is missing: {path}. Without it the second "
            f"redaction pass replaces ordinary words that happen to be surnames. Restore it - a "
            f"file holding only its header row is a valid empty list.")
    with path.open(encoding="utf-8") as fh:
        return {r["term"].strip() for r in csv.DictReader(fh) if r.get("term", "").strip()}


def load_redactions(path: Path) -> dict:
    """Load the name -> pseudonym map. A missing map raises: redaction that quietly does nothing
    prints real names and looks exactly like success."""
    if not path.is_file():
        raise FileNotFoundError(
            f"the fieldbook redaction map is missing: {path}. Without it every name in the "
            f"fieldbook would be written out. Restore the file rather than skipping this.")
    with path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    pairs = {r["name"].strip(): r["pseudonym"].strip() for r in rows if r.get("name", "").strip()}
    if not pairs:
        raise ValueError(f"{path}: holds no usable name -> pseudonym pairs.")
    return pairs


class Redactor:
    """Replace every known name with its pseudonym, longest surface form first.

    Longest-first is not cosmetic: the map holds both bare given names and surnames and the longer
    forms built out of them ('Ada', 'Lovelace' and 'Ada Lovelace'), and where two people share one
    of those words, replacing the short form first hands the entry to the wrong person.
    """

    def __init__(self, pairs: dict, ci_exclude: set):
        self.pairs = pairs
        forms = sorted(pairs, key=len, reverse=True)
        # A multi-word name can arrive split across two lines or with a doubled space once the
        # HTML is flattened, so the space in a surface form matches any run of whitespace. Without
        # this, 'Ada Lovelace' falls back to two separate one-word matches, and where the map
        # holds two people who share a first name that hands the entry to the wrong Ada.
        self.rx = re.compile(r"(?<!\w)(" + "|".join(self._pattern(f) for f in forms) + r")(?!\w)")
        ci = [f for f in forms if len(f) >= CI_MIN_LEN and f not in ci_exclude]
        self.rx_ci = re.compile(r"(?<!\w)(" + "|".join(self._pattern(f) for f in ci) + r")(?!\w)",
                                re.IGNORECASE)
        self.lookup = {re.sub(r"\s+", " ", f).lower(): p for f, p in pairs.items()}
        if len({f.lower() for f in pairs}) != len(pairs):
            raise ValueError("the redaction map holds two surface forms that differ only in case; "
                             "one would silently take the other's pseudonym.")

    @staticmethod
    def _pattern(form: str) -> str:
        return r"\s+".join(re.escape(part) for part in form.split())

    def _replace(self, m) -> str:
        return self.lookup[re.sub(r"\s+", " ", m.group(1)).lower()]

    def __call__(self, s) -> str:
        out = self.rx_ci.sub(self._replace, self.rx.sub(self._replace, str(s)))
        # 'Lovelace Ada', and a name the record spells two ways in one breath, are two surface
        # forms of one person and become the same pseudonym twice over, which reads as two people.
        return re.sub(r"(person \d+)(?:\s+\1)+", r"\1", out)


NAME_TOKEN = r"[A-ZÄÖÜ][\wÄÖÜäöüß'-]{1,20}"
NAME_UNIT = NAME_TOKEN + r"(?:\s+" + NAME_TOKEN + r"){0,2}"
NAME_SHAPES = (
    re.compile(r"\((" + NAME_UNIT + r"(?:\s*[,+&]\s*" + NAME_UNIT + r")*)\s*"
               r"(?:\d{1,2}\.\d{1,2}\.\d{4})?\)"),
    re.compile(r"(?:with|by|durch|von|gemaess)\s+(" + NAME_TOKEN
               + r"(?:\s+" + NAME_TOKEN + r")?)"),
)


def audit_unmapped_names(texts, allow_path: Path, report: Path, write_report: bool = True) -> None:
    """Raise if a name-shaped token survived redaction in the two shapes that carry names."""
    allow = set(pd.read_csv(allow_path, encoding="utf-8")["term"].astype(str).str.strip())
    found = Counter()
    for text in texts:
        for rx in NAME_SHAPES:
            for m in rx.finditer(text):
                for tok in re.findall(NAME_TOKEN, m.group(1)):
                    if tok.isupper() or any(c.isdigit() for c in tok) or tok in allow:
                        continue
                    found[tok] += 1
    if found:
        if write_report:
            report.write_text("\n".join(f"{n}\t{t}" for t, n in found.most_common()),
                              encoding="utf-8")
        raise ValueError(
            f"{len(found)} name-shaped token(s) survived redaction. They are deliberately NOT "
            f"shown here - see {report}. Add the people to redact_names.csv and the technical "
            f"terms to redact_allow.csv, then re-run.")
    print(f"  narrow name net: clean ({len(allow)} allowlisted terms)")


def wide_name_candidates(texts, export: pd.DataFrame, allow_path: Path, report: Path) -> int:
    """Write every capitalised token left standing, minus what is certainly not a person.

    Reports rather than raises. The filters are the export's own device/location/tag vocabulary
    and 'this token also occurs lowercase somewhere', which between them take ~2000 tokens down to
    ~600 - small enough to read once, far too many to raise on.
    """
    allow = set(pd.read_csv(allow_path, encoding="utf-8")["term"].astype(str).str.strip())
    vocab = set()
    for col in ("Event Tag", "Device Name", "Device Model", "Operation Tag", "Location", "Status"):
        for value in export[col].dropna().astype(str):
            vocab.update(re.findall(r"[\w.-]+", value))
    corpus = "\n".join(texts)
    lower_seen = set(re.findall(r"(?<![\w'-])[a-zäöü][\wäöüß'-]{2,24}", corpus))
    found = Counter()
    for m in re.finditer(r"[A-ZÄÖÜ][\wÄÖÜäöüßé'-]{2,24}", corpus):
        tok = m.group(0)
        if (tok.isupper() or any(c.isdigit() for c in tok) or tok in allow or tok in vocab
                or tok.lower() in lower_seen):
            continue
        found[tok] += 1
    report.write_text("\n".join(f"{n}\t{t}" for t, n in found.most_common()), encoding="utf-8")
    print(f"  wide name net: {len(found)} capitalised token(s) left standing, listed in "
          f"{report.name} (technical terms expected; read it after a new export)")
    return len(found)


# ---------------------------------------------------------------------------------------------
# credentials and network configuration
# ---------------------------------------------------------------------------------------------
ACCOUNTS = ("root", "admin", "laedaq")
CRED_CONTEXT = re.compile(r"(?i)\b(ssh|login|user\s?name|user|account|nas)\b")

IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?!\d)")

SANITIZERS = (
    # Local paths first: the one in this export runs through somebody's home directory, and it
    # would otherwise be chopped up by the rules below rather than removed.
    # The drive-letter half needs the lookbehind, or the 's:/' inside 'https://' matches and the
    # rule quietly eats every link in the record. It also has to survive a space inside a path
    # ('P:\\Research Sites_...'), which it does by accepting whitespace only where the next word
    # continues the path.
    ("local file path",
     re.compile(r"(?i)(?:file:///[^\s)\]]*"
                r"|(?<![\w:/])[A-Z]:[\\/](?:[^\s)\]]|\s(?=[\w.-]*[\\/]))*)"),
     "[local file path removed]"),
    ("e-mail address", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[e-mail removed]"),
    ("IP address", IPV4, "[IP removed]"),
    ("MAC address", re.compile(r"(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}"), "[MAC removed]"),
    # Only the assignment shapes. 'password is not documented anywhere' is a complaint, not a
    # disclosure, and an earlier version of this rule deleted the 'not' out of it.
    ("password", re.compile(r"(?i)\b(passwor[dt]|kennwort|pwd)\b\s*(?:=|:)\s*\S+"),
     "password = [removed]"),
    ("account name", re.compile(r"(?i)\b((?:ssh\s+)?login|user\s?name|benutzername)\s*"
                                r"(?:=|:)\s*[\w.@-]+"), r"\1 = [account removed]"),
)


def sanitize(text: str, counts: Counter) -> str:
    """Remove credentials and network configuration, counting what each rule took out."""
    for label, rx, repl in SANITIZERS:
        text, n = rx.subn(repl, text)
        counts[label] += n

    out_lines = []
    for line in text.split("\n"):
        if CRED_CONTEXT.search(line):
            for account in ACCOUNTS:
                line, n = re.subn(rf"(?<!\w){account}(?!\w)", "[account removed]", line)
                counts["account name"] += n
        if re.search(r"(?i)\bport\b", line):
            # A bare number on a line that talks about a port is a port. This is deliberately
            # blunt: matching only 'port = N' misses 'from only 22 to 22 and 22118'. Numbers that
            # touch a colon are clock times and are left alone, and IP addresses have already been
            # removed above, so what is left to match is a port.
            line, n = re.subn(r"(?<![\w.:])\d{2,5}(?![\d:])", "[port removed]", line)
            counts["port"] += n
        out_lines.append(line)
    return "\n".join(out_lines)


LEAK_CHECKS = (
    ("e-mail address", re.compile(r"[\w.+-]+@[\w-]+\.[\w]{2,}")),
    ("IP address", IPV4),
    ("local file path", re.compile(r"(?i)file:///|(?<![\w.])[A-Z]:[\\/]")),
)


def assert_no_leaks(text: str) -> None:
    """Fail loudly rather than write a file that still carries what it claims to have removed."""
    for label, rx in LEAK_CHECKS:
        hits = rx.findall(text)
        if hits:
            raise ValueError(f"{len(hits)} {label}(es) survived sanitising - refusing to write.")
    for line in text.split("\n"):
        if CRED_CONTEXT.search(line):
            for account in ACCOUNTS:
                if re.search(rf"(?<!\w){account}(?!\w)", line):
                    raise ValueError("an account name survived sanitising - refusing to write.")
    print("  leak check: no e-mail address, IP address or account name in the output")


# ---------------------------------------------------------------------------------------------
# HTML -> text
# ---------------------------------------------------------------------------------------------
def fix_mojibake(s: str) -> str:
    """Undo the single-byte round trip, longest sequence first and unrepairable ones left alone."""
    def repair(m):
        seq = m.group(0)
        for n in (3, 2):
            for encoding in ("latin-1", "cp1252"):
                try:
                    return seq[:n].encode(encoding).decode("utf-8") + seq[n:]
                except (UnicodeEncodeError, UnicodeDecodeError, IndexError):
                    continue
        return seq
    return MOJIBAKE_RX.sub(repair, s)


def to_text(raw) -> str:
    """Flatten one GIN entry to plain text, keeping its line and list structure.

    Word paste-ins arrive as conditional comments wrapping several kilobytes of `<w:...>` markup
    plus a CSS block; both are dropped whole rather than stripped tag by tag, which would leave
    the style rules behind as text.
    """
    s = fix_mojibake(str(raw))
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?is)<(style|xml|script)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<a [^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"\2 (\1)", s, flags=re.S)
    # The wiki's decorative icons were pasted in as links to files on somebody's own machine.
    # They carry nothing, so they go rather than becoming '[image: [local file path removed]]'.
    s = re.sub(r"(?i)<img[^>]*src=\"(?:file:///|[A-Z]:[\\/])[^\"]*\"[^>]*>", " ", s)
    s = re.sub(r"(?i)<img[^>]*src=\"([^\"]+)\"[^>]*>", r"[image: \1]", s)
    s = re.sub(r"(?i)<li[^>]*>", "\n- ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>|</ul>|</ol>|<p[^>]*>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    # what a Word paste-in leaves behind once its markup is gone
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
    s = re.sub(r"[\w.@:-]+\s*\{[^{}]*\}", " ", s)
    s = re.sub(r"(?i)\bNormal\s+0\s+\d+\s+false\s+false\s+false(\s+[\w-]+){0,4}", " ", s)
    s = s.replace("\xa0", " ")
    # What is left of a quotation mark whose lead byte the source lost. Nothing repairable, and it
    # renders as a box.
    s = re.sub(r"[\x80-\x9f]", "", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = "\n".join(line.strip() for line in s.split("\n"))
    s = re.sub(r"(?m)^[-)]\s*$", "", s)          # list items the export left empty
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ---------------------------------------------------------------------------------------------
# entries
# ---------------------------------------------------------------------------------------------
SUB_ENTRY = re.compile(r"^=*\s*(\d{1,2}\.\d{1,2}\.\d{4})\s*(?:-|–)?\s*", re.M)


def split_legacy(text: str, row_date):
    """Split the legacy block into its dated sub-entries.

    Returns (preamble, [(date, body), ...]). The sub-entry dates live in the text, so the export's
    own `Date` column - 2011-06-03 for all 94 of them - is not usable here.
    """
    marks = list(SUB_ENTRY.finditer(text))
    if not marks:
        return text, []
    preamble = text[:marks[0].start()].strip()
    out = []
    for i, m in enumerate(marks):
        body = text[m.end():marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        body = re.sub(r"^=+|=+$", "", body.strip()).strip()
        # The legacy block runs newest first and carries the paper fieldbook's own year headings.
        # Everything here is filed by its own date, so a stray 'YEAR 2008' would sit under 2009.
        body = re.sub(r"(?im)^\s*YEAR\s+\d{4}\s*$", "", body).strip()
        try:
            when = datetime.strptime(m.group(1), "%d.%m.%Y")
        except ValueError:
            continue
        if when > row_date:                       # a typo'd year would file the entry in the future
            continue
        out.append((when, body))
    return preamble, out


def meta_line(row) -> str:
    """The one-line header above an entry: who, where, on what, in what state."""
    bits = []
    for label, key in (("", "Operation Tag"), ("at ", "Location"), ("device ", "Device Name"),
                       ("model ", "Device Model"), ("", "Status")):
        value = str(row.get(key, "na")).strip()
        if key == "Operation Tag" and value.isdigit():
            value = f"operation {value}"      # some rows carry GIN's numeric operation id instead
        if value and value.lower() not in ("na", "nan", "none"):
            bits.append(f"{label}{value}")
    people = str(row.get("Namelist", "")).strip()
    if people and people.lower() not in ("na", "nan", "none"):
        bits.append(people)
    return " · ".join(bits)


REPO = Path(__file__).resolve().parent


def refuse_repo_path(out_path: Path) -> None:
    """Refuse to write the rendered fieldbook anywhere inside this repository.

    The record belongs beside the export, in the untracked data folder. It is derived data, it is
    a personnel record even after redaction, and anything under docs/ would additionally be
    rendered onto the public website by Quarto whether or not it is listed in the navigation.
    Redaction makes the file shareable; it does not make it publishable.
    """
    resolved = out_path.resolve() if out_path.is_absolute() else (Path.cwd() / out_path).resolve()
    if resolved == REPO or REPO in resolved.parents:
        raise ValueError(
            f"refusing to write the rendered fieldbook inside the repository ({resolved}). It "
            f"belongs beside the export in the external data folder. Pass an --out path outside "
            f"{REPO}.")


def self_test(redact: Redactor, allow_path: Path) -> None:
    """Feed each net something it must object to.

    Every one of these can fail silently in the direction that matters - a regex that matches
    nothing removes nothing and looks exactly like a clean record - so each is exercised on input
    that is not from the export. 'Ada Lovelace' is nobody at this site, so the name control can be
    spelled out without disclosing anyone.
    """
    probe = ("Ada Lovelace set login = fieldworker on 10.0.0.1, wrote to ada@example.org "
             "and left it in file:///C:/Users/somebody/notes.txt")
    clean = sanitize(probe, Counter())
    for leftover in ("10.0.0.1", "ada@example.org", "file:///", "fieldworker"):
        if leftover in clean:
            raise AssertionError(f"(!) the sanitiser left {leftover!r} standing - it is broken.")
    try:
        audit_unmapped_names(["12.05.2019 (Ada Lovelace) replaced the logger battery"],
                             allow_path, Path("unused"), write_report=False)
    except ValueError:
        pass
    else:
        raise AssertionError("(!) the name net did not fire on an unmapped name - it is broken.")
    # Taken from the map at run time rather than written out here: this file is in the repository,
    # and a worked example is exactly as published as a printed one.
    mapped = next(iter(redact.pairs))
    if redact(f"visited by {mapped} today") == f"visited by {mapped} today":
        raise AssertionError("(!) the redactor returned a mapped name unchanged - it is broken.")
    try:
        refuse_repo_path(REPO / "docs" / "fieldbook.md")
    except ValueError:
        pass
    else:
        raise AssertionError("(!) an output path inside the repository was accepted.")
    print("  self-test: sanitiser, name net, redactor and output-path guard all fired")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--export", type=Path, default=None, help="the GIN csv (default: the newest)")
    ap.add_argument("--until", default=DEFAULT_UNTIL, help=f"last date to include ({DEFAULT_UNTIL})")
    ap.add_argument("--out", type=Path, default=None, help="output markdown file")
    args = ap.parse_args()

    export = args.export or max(FIELDBOOK_DIR.glob(EXPORT_GLOB), key=lambda p: p.name)
    until = pd.Timestamp(args.until)
    out_path = args.out or FIELDBOOK_DIR / f"CH-LAE_fieldbook_redacted_until_{until:%Y}.md"
    refuse_repo_path(out_path)
    print(f"export : {export.name}")
    print(f"until  : {until:%Y-%m-%d}")

    raw = pd.read_csv(export, encoding="utf-8")
    raw["date"] = pd.to_datetime(raw["Date"], format="%d.%m.%Y")
    redact = Redactor(load_redactions(FIELDBOOK_DIR / "redact_names.csv"),
                      load_ci_exclusions(FIELDBOOK_DIR / CI_EXCLUDE_FILE))
    print("controls:")
    self_test(redact, FIELDBOOK_DIR / "redact_allow.csv")

    # Build the entry list. The legacy row is replaced by the sub-entries it contains, which is
    # what puts the 2006-2011 record under its own dates instead of under 2011-06-03.
    entries, counts = [], Counter()
    n_legacy = 0
    for _, row in raw.iterrows():
        text = to_text(row["Text"])
        is_legacy = LEGACY_MARKER.lower() in text.lower()
        pieces = [(row["date"], text, False)]
        if is_legacy:
            preamble, subs = split_legacy(text, row["date"])
            n_legacy = len(subs)
            pieces = [(row["date"], preamble, False)] + [(d, b, True) for d, b in subs]
        for when, body, legacy in pieces:
            if when > until or not body.strip():
                continue
            # Sanitise first, redact second. An e-mail address carries a name, and redacting it
            # first turns 'ada.lovelace@x.ch' into 'person 07.person 07@x.ch', which the e-mail
            # rule then only half removes.
            entries.append({
                "date": when,
                "meta": redact(meta_line(row)) if not legacy else "from the legacy fieldbook, "
                                                                  "imported 2011-06-03",
                "body": redact(sanitize(body, counts)),
                "legacy": legacy,
            })

    if not entries:
        raise ValueError(f"{export.name}: no entries up to {until:%Y-%m-%d}. Has the export "
                         f"format changed? An empty render reads exactly like a quiet site.")
    entries.sort(key=lambda e: (e["date"], e["legacy"]))

    bodies = [e["body"] for e in entries] + [e["meta"] for e in entries]
    print(f"\nentries: {len(entries)} ({n_legacy} of them from the legacy block), "
          f"{entries[0]['date']:%Y-%m-%d} -> {entries[-1]['date']:%Y-%m-%d}")
    print("redaction:")
    audit_unmapped_names(bodies, FIELDBOOK_DIR / "redact_allow.csv",
                         FIELDBOOK_DIR / "redact_unmapped.txt")
    wide_name_candidates(bodies, raw, FIELDBOOK_DIR / "redact_allow.csv",
                         FIELDBOOK_DIR / "redact_name_candidates.txt")
    for label, n in sorted(counts.items()):
        print(f"  removed {n:>3} {label}(s)")

    per_year = Counter(e["date"].year for e in entries)
    lines = [
        f"# CH-LAE fieldbook, {entries[0]['date']:%Y}-{until:%Y}",
        "",
        "Redacted rendering of the site maintenance record kept in GIN, for the mixed forest "
        "eddy-covariance site CH-LAE (Lägeren).",
        "",
        "## About this file",
        "",
        f"- Source: `{export.name}`, entries dated up to {until:%Y-%m-%d}.",
        f"- Generated by `build_fieldbook_md.py` on {datetime.now():%Y-%m-%d}. "
        f"It is generated output; edit the script, not this file.",
        "- **People are pseudonymised.** Each person carries a stable `person NN` label from the "
        "redaction map that lives beside the export, so the same label means the same person "
        "here and in the processing notebooks. Labels are append-only, so a re-run reproduces "
        "them.",
        "- **Credentials and network configuration are removed**: e-mail and IP addresses, "
        "account names and remote-access ports appear as `[... removed]`. Device serial numbers "
        "and model names are kept, since they identify equipment rather than access.",
        "- The entry bodies were HTML. They are flattened here, with Word paste-in boilerplate "
        "dropped and the encoding damage in the older entries repaired. Attachments are shown as "
        "`[image: url]` and remain in GIN.",
        f"- The {n_legacy} entries marked *from the legacy fieldbook* come from a single row "
        "dated 2011-06-03, into which the pre-GIN fieldbook was pasted when GIN was introduced. "
        "They are filed here under the dates written in their own text. The record before "
        "2006-08-31 does not exist in any form.",
        "- Dates carry no time of day, and entries are frequently written up days after the "
        "visit they describe. A date here is worth about a day of slack.",
        "",
        "## Entries per year",
        "",
        "| Year | Entries |",
        "|---|---|",
    ]
    lines += [f"| {y} | {per_year[y]} |" for y in sorted(per_year)]
    lines += [f"| **Total** | **{len(entries)}** |", ""]

    year = day = None
    for e in entries:
        if e["date"].year != year:
            year = e["date"].year
            lines += ["", f"## {year}", ""]
        if e["date"].date() != day:
            day = e["date"].date()
            lines += [f"### {day:%Y-%m-%d}", ""]
        if e["meta"]:
            lines += [f"*{e['meta']}*", ""]
        lines += [e["body"], ""]

    text = "\n".join(lines)
    assert_no_leaks(text)
    out_path.write_text(text, encoding="utf-8")
    print(f"\nwrote {out_path}  ({len(text):,} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
