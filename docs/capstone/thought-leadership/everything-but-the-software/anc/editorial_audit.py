"""Extract article numbers and reproducible editorial metrics without changing sources."""

import argparse
import difflib
import hashlib
import json
import math
import re
import statistics
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path

from check_paper import expand_inputs

PACKAGE = Path(__file__).resolve().parent.parent
NUMBER = re.compile(r"[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?")
WORD = re.compile(r"[A-Za-z]+(?:['-][A-Za-z]+)*|\d+(?:\.\d+)?")
TICS = {
    "remain/remains": r"\bremains?\b",
    "separate/separately": r"\bseparate(?:ly)?\b",
    "retained": r"\bretained\b",
    "establish": r"\bestablish\b",
}


def expand(path: Path, root: Path) -> str:
    return expand_inputs(path.read_text(), root)


def uncomment(text: str) -> str:
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def detex(text: str) -> str:
    text = re.sub(
        r"\\(?:label|cite[pt]?|sourceref|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}", "", text
    )
    text = re.sub(r"\\(?:ref|eqref)\{[^}]*\}", "REF", text)
    text = re.sub(r"\\(?:no)?linkurl\{[^}]*\}", "URL", text)
    text = re.sub(r"\\href\{[^}]*\}", "", text)
    text = re.sub(
        r"\\begin\{(?:equation|align)\*?\}.*?\\end\{(?:equation|align)\*?\}",
        "",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(r"\$\$?.*?\$\$?", " MATH ", text, flags=re.DOTALL)
    text = re.sub(r"\\(?:section|subsection|subsubsection|paragraph)\*?\{[^}]*\}", "", text)
    return subprocess.run(
        ["detex", "-l"], input=text, capture_output=True, text=True, check=True
    ).stdout


def table_numbers(source: str) -> dict[str, list[str]]:
    result = {}
    for table in re.findall(r"\\begin\{table\}.*?\\end\{table\}", source, re.DOTALL):
        labels = re.findall(r"\\label\{([^}]+)\}", table)
        if len(labels) != 1:
            raise ValueError(f"Expected one label in a numeric table: {labels}")
        if labels[0] in result:
            raise ValueError(f"Duplicate table label: {labels[0]}")
        cells = table.split(r"\midrule", 1)[1].split(r"\bottomrule", 1)[0]
        result[labels[0]] = NUMBER.findall(cells)
    return result


def sentence_words(prose: str) -> list[list[str]]:
    prose = re.sub(r"\b(RQ\d+)\.", r"\1", prose)
    return [
        WORD.findall(part) for part in re.split(r"[.!?]+(?:\s+|$)", prose) if WORD.findall(part)
    ]


def capture(root: Path) -> dict:
    source = uncomment(expand(root / "main.tex", root))
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", source, re.DOTALL)[1]
    main = source[
        source.index(r"\section{Introduction}") : source.index(r"\section*{Author contributions}")
    ]
    sections, numbers, prose_all = [], [], []
    for index, section in enumerate(filter(str.strip, re.split(r"(?=\\section\{)", main)), 1):
        name = re.match(r"\\section\{([^}]+)\}", section)[1]
        prose = re.sub(
            r"\\begin\{(?:table|figure)\}.*?\\end\{(?:table|figure)\}", "", section, flags=re.DOTALL
        )
        prose_all.append(detex(prose))
        sections.append(
            {"section": index, "title": name, "words": len(WORD.findall(detex(section)))}
        )
        for match in NUMBER.finditer(section):
            numbers.append(
                {
                    "section": index,
                    "value": match[0],
                    "context": re.sub(
                        r"\s+", " ", section[max(0, match.start() - 85) : match.end() + 85]
                    ),
                }
            )
    prose = "\n\n".join(prose_all)
    prose = re.sub(r"\bet al\.", "et al", prose)
    prose = re.sub(r"\b(?:e\.g|i\.e)\.", "eg", prose)
    sentences = sentence_words(prose)
    count = len(WORD.findall(prose))
    return {
        "sections": sections,
        "total_section_words": sum(section["words"] for section in sections),
        "prose_words_excluding_tables_figures_equations": count,
        "sentences": len(sentences),
        "mean_sentence_words": statistics.mean(map(len, sentences)),
        "sentence_length_sd": statistics.pstdev(map(len, sentences)),
        "sentence_length_range": [min(map(len, sentences)), max(map(len, sentences))],
        "tic_words": {
            key: {
                "count": len(re.findall(pattern, prose, re.IGNORECASE)),
                "per_1000_words": len(re.findall(pattern, prose, re.IGNORECASE)) * 1000 / count,
            }
            for key, pattern in TICS.items()
        },
        "abstract_plain_characters": len(re.sub(r"\s+", " ", detex(abstract)).strip()),
        "abstract_source_characters": len(re.sub(r"\s+", " ", abstract).strip()),
        "numbers": numbers,
        "table_numbers": table_numbers(source),
        "source_sha256": hashlib.sha256(main.encode()).hexdigest(),
    }


def compare_numbers(before: dict, after: dict) -> dict:
    old, new = before["numbers"], after["numbers"]
    matcher = difflib.SequenceMatcher(
        a=[row["value"] for row in old], b=[row["value"] for row in new], autojunk=False
    )
    differences = [
        {
            "operation": tag,
            "before_indices": [a, b],
            "after_indices": [c, d],
            "before": old[a:b],
            "after": new[c:d],
        }
        for tag, a, b, c, d in matcher.get_opcodes()
        if tag != "equal"
    ]
    old_counts = Counter(row["value"] for row in old)
    new_counts = Counter(row["value"] for row in new)
    return {
        "before_count": len(old),
        "after_count": len(new),
        "removed_multiset": dict(old_counts - new_counts),
        "added_multiset": dict(new_counts - old_counts),
        "all_sequence_differences": differences,
    }


def gemini_cr1_comparison() -> dict:
    n, successes_b, successes_c = 21, 8, 16
    z = statistics.NormalDist().inv_cdf(0.975)

    def wilson(successes: int) -> tuple[float, float]:
        p = successes / n
        denominator = 1 + z * z / n
        centre = (p + z * z / (2 * n)) / denominator
        radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
        return centre - radius, centre + radius

    p_b, p_c = successes_b / n, successes_c / n
    lower_b, upper_b = wilson(successes_b)
    lower_c, upper_c = wilson(successes_c)
    difference = p_b - p_c
    lower = difference - math.hypot(p_b - lower_b, upper_c - p_c)
    upper = difference + math.hypot(upper_b - p_b, p_c - lower_c)
    successes, failures = successes_b + successes_c, 2 * n - successes_b - successes_c

    def probability(x: int) -> Fraction:
        return Fraction(math.comb(successes, x) * math.comb(failures, n - x), math.comb(2 * n, n))

    observed = probability(successes_b)
    fisher = sum(
        (
            probability(x)
            for x in range(max(0, n - failures), min(n, successes) + 1)
            if probability(x) <= observed
        ),
        Fraction(),
    )
    return {
        "successes_B": successes_b,
        "successes_C": successes_c,
        "n_per_arm": n,
        "difference_percentage_points": difference * 100,
        "newcombe_hybrid_score_95_ci_percentage_points": [lower * 100, upper * 100],
        "two_sided_fisher_exact_p": float(fisher),
        "fisher_exact_fraction": str(fisher),
        "multiplicity": "Unadjusted and exploratory among many comparisons",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=PACKAGE)
    parser.add_argument("--baseline-json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = capture(args.source)
    if args.baseline_json:
        baseline = json.loads(args.baseline_json.read_text())
        before = baseline.get("before", baseline)
        result = {
            "before": before,
            "after": result,
            "number_diff": compare_numbers(before, result),
            "authorised_recalculation": gemini_cr1_comparison(),
        }
    with args.output.open("x") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
