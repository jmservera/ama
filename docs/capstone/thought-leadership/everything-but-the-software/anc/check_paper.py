#!/usr/bin/env python3
"""Check paper structure and reproduce approximate body counts without texcount.

Run from the repository root with .venv/bin/python followed by this path.
The baseline is the unmodified draft at the revision's starting commit.
The optional normalisation only sorts existing bibliography entry blocks.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent
BASELINE = "0d5dcb02"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--normalise-bibliography", action="store_true")
    parser.add_argument("--allow-unsorted", action="store_true")
    parser.add_argument("--check-latex-log", action="store_true")
    return parser


def strip_comments(text: str) -> str:
    return re.sub(r"(?m)(?<!\\)%.*$", "", text)


def body_words(text: str) -> int:
    body = text.split(r"\section{Introduction}", 1)[1]
    body = body.split(r"\section*{Acknowledgements}", 1)[0]
    body = strip_comments(body)
    body = re.sub(r"\\begin\{verbatim\}.*?\\end\{verbatim\}", "", body, flags=re.S)
    body = re.sub(r"\\(?:cite\w*|ref|label|includegraphics)(?:\[[^]]*\])?\{[^}]*\}", "", body)
    body = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", " ", body)
    body = re.sub(r"[{}~$&^_=<>|\\]", " ", body)
    return len(body.split())


def normalise_bibliography() -> None:
    source = PACKAGE / "main.tex"
    text = source.read_text(encoding="utf-8")
    start = text.index(r"\bibitem{")
    end = text.index(r"\end{thebibliography}", start)
    entries = re.findall(r"\\bibitem\{([^}]+)\}.*?(?=\\bibitem\{|\Z)", text[start:end], re.S)
    blocks = re.split(r"(?=\\bibitem\{)", text[start:end])
    ordered = sorted(zip(entries, (block for block in blocks if block.strip())))
    source.write_text(text[:start] + "\n\n".join(block.strip() for _, block in ordered) + "\n\n" + text[end:], encoding="utf-8")
    bibfile = PACKAGE / "references.bib"
    bibtext = bibfile.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^@\w+\{([^,]+),", bibtext))
    blocks_by_key = []
    for index, match in enumerate(matches):
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(bibtext)
        blocks_by_key.append((match.group(1), bibtext[match.start():stop].strip()))
    bibfile.write_text(bibtext[:matches[0].start()] + "\n\n".join(block for _, block in sorted(blocks_by_key)) + "\n", encoding="utf-8")


def main() -> int:
    args = create_parser().parse_args()
    if args.normalise_bibliography:
        normalise_bibliography()
    text = (PACKAGE / "main.tex").read_text(encoding="utf-8")
    clean = strip_comments(text)
    root = PACKAGE.parents[3]
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git is unavailable")
    relative = (PACKAGE / "main.tex").relative_to(root).as_posix()
    baseline = subprocess.run([git, "show", f"{BASELINE}:{relative}"], cwd=root, capture_output=True, text=True, check=True).stdout
    print(f"BODY_WORDS_APPROX before={body_words(baseline)} after={body_words(text)}")
    print("COUNT_METHOD introduction through conclusion; tables included; abstract, bibliography and appendices excluded; LaTeX stripped")
    failures = []
    citations = {key.strip() for group in re.findall(r"\\cite\w*(?:\[[^]]*\])*\{([^}]+)\}", clean) for key in group.split(",")}
    bibitems = re.findall(r"\\bibitem\{([^}]+)\}", clean)
    bibkeys = re.findall(r"(?m)^@\w+\{([^,]+),", (PACKAGE / "references.bib").read_text(encoding="utf-8"))
    for name, keys in (("bibitems", bibitems), ("BibTeX", bibkeys)):
        if set(keys) != citations or len(keys) != len(set(keys)):
            failures.append(f"{name}: missing={sorted(citations - set(keys))}, uncited={sorted(set(keys) - citations)}, duplicate={len(keys) != len(set(keys))}")
        if not args.allow_unsorted and keys != sorted(keys):
            failures.append(f"{name} keys are not alphabetically sorted")
    labels = re.findall(r"\\label\{([^}]+)\}", clean)
    references = set(re.findall(r"\\(?:ref|pageref|autoref|eqref)\{([^}]+)\}", clean))
    if references - set(labels) or len(labels) != len(set(labels)):
        failures.append(f"labels: missing={sorted(references - set(labels))}, duplicate={len(labels) != len(set(labels))}")
    environments = []
    for action, name in re.findall(r"\\(begin|end)\{([^}]+)\}", clean):
        if action == "begin":
            environments.append(name)
        elif not environments or environments.pop() != name:
            failures.append(f"environment mismatch at end of {name}")
    if environments:
        failures.append(f"unclosed environments: {environments}")
    nonverbatim = re.sub(r"\\begin\{verbatim\}.*?\\end\{verbatim\}", "", clean, flags=re.S)
    depth = 0
    for brace in re.findall(r"\\.|[{}]", nonverbatim):
        if brace == "{":
            depth += 1
        elif brace == "}":
            depth -= 1
            if depth < 0:
                failures.append("closing brace without opening brace")
                break
    if depth:
        failures.append(f"brace imbalance: {depth}")
    in_verbatim = False
    for number, line in enumerate(text.splitlines(), 1):
        if r"\begin{verbatim}" in line:
            in_verbatim = True
        if r"\end{verbatim}" in line:
            in_verbatim = False
            continue
        if in_verbatim:
            continue
        comment = re.search(r"(?<!\\)%", line)
        if comment and line[:comment.start()].strip():
            failures.append(f"inline percent comment at line {number}: inspect for swallowed paper text")
    abstract = clean.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]
    characters = len(" ".join(abstract.split()))
    print(f"ABSTRACT_SOURCE_CHARACTERS {characters} (limit <1920; conservative source count)")
    if characters >= 1920:
        failures.append("abstract is too long")
    if r"\resultsfalse" not in clean or r"\resultstrue" in clean:
        failures.append("results switch is not false")
    if args.check_latex_log:
        log = (PACKAGE / "main.log").read_text(encoding="utf-8")
        if re.search(r"(?m)^!|undefined|Rerun to get|Label\(s\) may have changed", log, re.I):
            failures.append("LaTeX log has an error, undefined item or unresolved rerun warning")
        overfull = [float(width) for width in re.findall(r"Overfull \\[hv]box \(([\d.]+)pt too (?:wide|high)\)", log)]
        if any(width > 10 for width in overfull):
            failures.append(f"overfull boxes above 10pt: {overfull}")
        if "Output written on main.pdf" not in log:
            failures.append("LaTeX did not report a PDF output")
        print(f"LATEX_CHECK overfull_boxes_above_10pt={sum(width > 10 for width in overfull)}")
    print(f"BIBLIOGRAPHY cited={len(citations)} bibitems={len(bibitems)} bibtex={len(bibkeys)}")
    print("TODO(author) locations:")
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r"\s*% TODO\(author\):", line):
            print(f"{number}: {line.strip()}")
    for failure in failures:
        print(f"FAIL {failure}")
    print("PASS structural checks" if not failures else "FAIL structural checks")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
