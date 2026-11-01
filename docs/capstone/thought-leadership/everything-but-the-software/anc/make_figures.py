#!/usr/bin/env python3
"""Regenerate the case and published-evidence figures as PNG files.

Usage: python3 anc/make_figures.py [--dpi 400] [--out .] [--only published]
Reads anc/log_daily.json (daily entries, words, hedging phrases), produced from
docs/reference/log.md with `log_metrics.py ... --json log_daily.json`, and writes
case figures and replots anc/published-evidence.json. The --only option can
regenerate either group without changing the other. Output defaults to the
folder containing main.tex, one level above this script.
"""
import argparse, datetime as dt, json, math, os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import rcParams

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
rcParams.update({"font.family": "serif"})


def log_growth(dpi):
    d = json.load(open(os.path.join(HERE, "log_daily.json")))
    start, end = dt.date(2026, 9, 25), dt.date(2026, 10, 22)
    days = [start + dt.timedelta(i) for i in range((end - start).days + 1)]
    words = [d.get(x.isoformat(), [0, 0, 0])[1] / 1000 for x in days]
    hedge_density = [
        1000 * daily[2] / daily[1] if daily[1] else math.nan
        for daily in (d.get(day.isoformat(), [0, 0, 0]) for day in days)
    ]
    x = list(range(len(days)))
    rcParams.update({"font.size": 8})
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.6, 3.5), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1.2], "hspace": 0.12})
    loop = days.index(dt.date(2026, 10, 15))
    ax1.bar(x, words, color=["#9aa5b1" if i < loop else "#1f4e79" for i in x], width=0.8)
    ax1.set_ylabel("Words appended\n(thousands)")
    ax2.bar(x, hedge_density, color=["#c9a227" if i < loop else "#8b1e1e" for i in x], width=0.8)
    ax2.set_ylabel("Hedge matches\nper 1,000 words")
    for ax in (ax1, ax2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.axvline(loop - 0.5, color="black", lw=0.8, ls="--")
    arrow = dict(arrowstyle="-", lw=0.5, color="0.3")
    i = days.index(dt.date(2026, 10, 12)); ax1.annotate("usable MVP on Azure", xy=(i, words[i]), xytext=(i - 7.5, 5.2), fontsize=7, arrowprops=arrow)
    i = loop; ax1.annotate("coordinator loop starts", xy=(i, words[i]), xytext=(i - 8.6, 13.2), fontsize=7, arrowprops=arrow)
    i = days.index(dt.date(2026, 10, 16)); ax1.annotate("cut-over to new\nsource layout", xy=(i, words[i]), xytext=(i + 3.0, 11.6), fontsize=7, arrowprops=arrow)
    i = days.index(dt.date(2026, 10, 22)); ax1.annotate("feedback-first label", xy=(i, words[i]), xytext=(i - 4.6, 4.0), fontsize=7, arrowprops=arrow)
    ax1.set_ylim(0, 15.5)
    ticks = [i for i, dd in enumerate(days) if dd.weekday() == 0 or dd in (start, end)]
    ax2.set_xticks(ticks)
    ax2.set_xticklabels([days[i].strftime("%d %b") for i in ticks])
    ax2.set_xlabel("Date of knowledge-base log entry (2026)")
    fig.savefig(os.path.join(OUT, "fig-log-growth.png"), dpi=dpi, bbox_inches="tight", facecolor="white", pil_kwargs={"optimize": True})
    plt.close(fig)


def causal_loop(dpi):
    rcParams.update({"font.size": 7.2})
    nodes = ["Large up-front\nspecification\n(BRD, PRD, ADRs)",
             "Large backlog and\nmany parallel\nagent loops",
             "Artefacts and gates\nstand in for \u201cdone\u201d\n(proxy capture)",
             "Long read path\nmay impair retrieval\n(unmeasured)",
             "Lessons may drop off\nthe effective read path\n(learning evaporation)",
             "Replacement unusable\nby the owner\n(feedback starvation)",
             "Owner answers gaps\nwith more rules,\ncriteria and gates"]
    angles = [90, 28, -17, -66, -114, -163, 152]
    rx, ry, w, h = 2.35, 1.32, 1.55, 0.52
    pos = [(rx * math.cos(math.radians(a)), ry * math.sin(math.radians(a))) for a in angles]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.set_xlim(-3.25, 3.25); ax.set_ylim(-2.0, 1.65); ax.axis("off")
    for i, (x, y) in enumerate(pos):
        s = (i == 5)
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.07",
                                    fc="#f6dede" if s else "#e8eef5", ec="#8b1e1e" if s else "#1f4e79", lw=0.9))
        ax.text(x, y, nodes[i], ha="center", va="center", linespacing=1.15)

    def edge(x, y, tx, ty, pad=0.05):
        dx, dy = tx - x, ty - y
        s = min((w / 2 + pad) / abs(dx) if dx else 1e9, (h / 2 + pad) / abs(dy) if dy else 1e9)
        return (x + dx * s, y + dy * s)

    mid = None
    for i in range(len(nodes)):
        a, b = pos[i], pos[(i + 1) % len(nodes)]
        s, e = edge(*a, *b), edge(*b, *a)
        ax.add_patch(FancyArrowPatch(s, e, connectionstyle="arc3,rad=-0.15", arrowstyle="-|>", mutation_scale=9, lw=0.9, linestyle="--", color="0.25"))
        if i == 5:
            mid = ((s[0] + e[0]) / 2 - 0.07, (s[1] + e[1]) / 2)
    ax.text(0, 0.06, "R?", ha="center", va="center", fontsize=18, fontweight="bold", color="#1f4e79")
    ax.text(0, -0.24, "hypothesised links", ha="center", va="center", fontsize=7, color="#1f4e79")
    mx, my = mid
    for off in (0.0, -0.075):
        ax.plot([mx - 0.11, mx + 0.11], [my - 0.04 + off, my + 0.04 + off], color="#2e7d32", lw=2.0, solid_capstyle="butt")
    ax.text(mx - 0.17, my - 0.04, "proposed\nintervention", ha="right", va="center", fontsize=6.8, color="#1b5e20")
    ax.add_patch(FancyBboxPatch((-2.9, -1.95), 5.8, 0.26, boxstyle="round,pad=0.02", fc="#e9f4ea", ec="#2e7d32", lw=0.9))
    ax.text(0, -1.82, "Proposed human checkpoints and usable increments: outside the consolidation experiment",
            ha="center", va="center", fontsize=7, color="#1b5e20")
    fig.savefig(os.path.join(OUT, "fig-causal-loop.png"), dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def inherited_history(dpi: int) -> None:
    """Replot published event-resolution differences and confidence intervals."""
    evidence = json.loads((Path(HERE) / "published-evidence.json").read_text(encoding="utf-8"))
    rows = evidence["repository_history"]["rows"]
    positions = list(reversed(range(len(rows))))
    labels = [f"{row['label']}\n(n = {row['paired_events']:,} paired events)" for row in rows]
    rcParams.update({"font.size": 8})
    figure, axis = plt.subplots(figsize=(7.0, 3.5))
    for position, row, marker in zip(positions, rows, ("s", "o", "^", "D")):
        difference = row["difference_pp"]
        lower, upper = row["ci95_pp"]
        if not lower <= difference <= upper:
            raise ValueError(f"Invalid confidence interval: {row['label']}")
        axis.errorbar(
            difference, position,
            xerr=[[difference - lower], [upper - difference]],
            fmt=marker, markersize=5, capsize=3, linewidth=1.2,
            color="#1f4e79" if difference < 0 else "#2e6a51",
        )
        axis.text(9.8, position, f"{difference:+.1f}", ha="right", va="center")
    axis.set_yticks(positions, labels)
    axis.set_xlim(-28, 11)
    axis.set_ylim(-0.65, len(rows) - 0.35)
    axis.set_xticks((-25, -20, -15, -10, -5, 0, 5, 10))
    axis.axvline(0, color="0.35", linewidth=0.8, linestyle="--")
    axis.axhline(2.5, color="0.8", linewidth=0.6)
    axis.grid(axis="x", color="0.9", linewidth=0.5)
    axis.set_axisbelow(True)
    axis.tick_params(axis="y", length=0, pad=8)
    axis.set_xlabel("Agent-history minus developer-history success (percentage points)")
    axis.set_title("Inherited repository history and later maintenance", fontsize=10, pad=12)
    for side in ("top", "right", "left"):
        axis.spines[side].set_visible(False)
    figure.subplots_adjust(left=0.43, right=0.98, bottom=0.20, top=0.86)
    figure.savefig(Path(OUT) / "fig-inherited-history.png", dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def instruction_maintenance(dpi: int) -> None:
    """Replot overlapping instruction-edit labels, not net instruction growth."""
    evidence = json.loads((Path(HERE) / "published-evidence.json").read_text(encoding="utf-8"))
    data = evidence["instruction_maintenance"]
    rows = data["rows"]
    counts = [row["label_assignments"] for row in rows]
    if sum(counts) != data["total_label_assignments"]:
        raise ValueError("Instruction label counts do not match the published total")
    positions = list(reversed(range(len(rows))))
    rcParams.update({"font.size": 8})
    figure, axis = plt.subplots(figsize=(6.6, 2.8))
    axis.barh(positions, counts, height=0.55, color=("#1f4e79", "#727c87", "#2e6a51", "#b3b8bd"))
    for position, count in zip(positions, counts):
        axis.text(count + 1.5, position, str(count), va="center")
    axis.set_yticks(positions, [row["label"] for row in rows])
    axis.set_xlim(0, 100)
    axis.set_xticks((0, 20, 40, 60, 80, 100))
    axis.set_xlabel("Label assignments in 100 post-adoption commits")
    axis.set_title("Agent instructions are maintained, not written once", fontsize=10, pad=12)
    axis.tick_params(axis="y", length=0, pad=8)
    axis.grid(axis="x", color="0.9", linewidth=0.5)
    axis.set_axisbelow(True)
    for side in ("top", "right", "left"):
        axis.spines[side].set_visible(False)
    figure.subplots_adjust(left=0.34, right=0.96, bottom=0.24, top=0.83)
    figure.savefig(Path(OUT) / "fig-instruction-maintenance.png", dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(figure)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=400)
    ap.add_argument("--out", default=None, help="output folder (default: parent of anc/)")
    ap.add_argument("--only", choices=("all", "case", "published"), default="all")
    a = ap.parse_args()
    if a.out:
        OUT = os.path.abspath(a.out)
    figures = {
        "fig-log-growth.png": log_growth,
        "fig-causal-loop.png": causal_loop,
        "fig-inherited-history.png": inherited_history,
        "fig-instruction-maintenance.png": instruction_maintenance,
    }
    selected = list(figures)
    if a.only == "case":
        selected = selected[:2]
    elif a.only == "published":
        selected = selected[2:]
    Path(OUT).mkdir(parents=True, exist_ok=True)
    for name in selected:
        figures[name](a.dpi)
    from PIL import Image
    for name in selected:
        path = os.path.join(OUT, name)
        Image.open(path).convert("RGB").save(path, dpi=(a.dpi, a.dpi), optimize=True)
    print("wrote " + ", ".join(selected))
