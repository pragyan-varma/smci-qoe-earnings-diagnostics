"""
qoe.charts — the QoE exhibits (matplotlib, no seaborn, single-figure functions).

  waterfall(): GAAP EBITDA -> management add-back -> diligence adjustments -> Adjusted EBITDA,
               with the three-tier structure visible. Increases green, decreases red, levels navy.
  ccc_trend(): DIO/DSO/DPO bars + CCC line across periods — often the better story than the walk.

All inputs are DERIVED from the FactSet; nothing is hard-coded here.
"""
from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from finlib.facts import FactSet
from . import bridge as B, metrics as M

GREEN, RED, NAVY, GREY = "#2E7D32", "#C62828", "#1F3A5F", "#9E9E9E"
MM = 1e6  # whole dollars -> $ millions for labels


def _mm(x):
    return x / MM


def waterfall(fs: FactSet, period: str, out_path: str) -> str:
    br = B.build_bridge(fs, period)
    # Build the walk: start, booked steps, end. SBC shown as the contested management add-back.
    steps = [("GAAP\nEBITDA", br.gaap_ebitda, "level")]
    for l in br.lines:
        if l.booked and l.value:
            kind = "up" if l.value > 0 else "down"
            steps.append((f"{l.id}\n{l.name.split('(')[0].strip()[:18]}", l.value, kind))
    steps.append(("Diligence Adj.\nEBITDA (pre-SBC)", br.diligence_ebitda_pre_sbc, "level"))

    fig, ax = plt.subplots(figsize=(11, 6.2))
    running = 0.0
    xs = range(len(steps))
    for i, (label, val, kind) in enumerate(steps):
        if kind == "level":
            ax.bar(i, _mm(val), color=NAVY, edgecolor="black", linewidth=0.5, zorder=3)
            ax.text(i, _mm(val) + 12, f"${_mm(val):,.0f}M", ha="center", va="bottom",
                    fontweight="bold", fontsize=9)
            running = val
        else:
            color = GREEN if kind == "up" else RED
            bottom = _mm(running if val > 0 else running + val)
            ax.bar(i, _mm(abs(val)), bottom=bottom, color=color, edgecolor="black",
                   linewidth=0.5, zorder=3)
            # connector
            ax.plot([i - 1 + 0.4, i + 0.4], [_mm(running), _mm(running)], color=GREY,
                    linewidth=0.8, linestyle="--", zorder=2)
            sign = "+" if val > 0 else "−"
            ax.text(i, bottom + _mm(abs(val)) + 12, f"{sign}${_mm(abs(val)):,.0f}M",
                    ha="center", va="bottom", fontsize=8, color=color)
            running += val

    ax.set_xticks(list(xs))
    ax.set_xticklabels([s[0] for s in steps], fontsize=8)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:,.0f}M"))
    ax.set_ylabel("EBITDA ($ millions)")
    ax.set_title(f"SMCI EBITDA Bridge — {period}\nGAAP EBITDA to Diligence Adjusted EBITDA "
                 "(SBC shown as contested add-back)", fontsize=11, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, zorder=0)
    ax.margins(y=0.15)
    fig.text(0.5, 0.005,
                "Green = increase, red = decrease, navy = level. Only sourced, booked items shown; "
                "SENSITIVITY/REJECT exposures are on the Adjustment Schedule.",
                ha="center", fontsize=7.5, color=GREY)
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def ccc_trend(fs: FactSet, periods, out_path: str) -> str:
    mets = M.compute(fs, periods)
    labels = [m.period for m in mets]
    fig, ax = plt.subplots(figsize=(9, 5.6))
    x = range(len(mets))
    ax.bar([i - 0.25 for i in x], [m.dio for m in mets], width=0.25, label="DIO", color=NAVY, zorder=3)
    ax.bar([i for i in x], [m.dso for m in mets], width=0.25, label="DSO", color="#4C7AAF", zorder=3)
    ax.bar([i + 0.25 for i in x], [m.dpo for m in mets], width=0.25, label="DPO", color=GREY, zorder=3)
    ax.plot(list(x), [m.ccc for m in mets], color=RED, marker="o", linewidth=2, label="CCC", zorder=4)
    for i, m in enumerate(mets):
        ax.text(i, m.ccc + 2, f"{m.ccc:.0f}", ha="center", color=RED, fontweight="bold", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Days")
    ax.set_title("SMCI Cash Conversion Cycle\nDPO falling (suppliers demanding cash) while inventory "
                 "days stay elevated", fontsize=11, fontweight="bold")
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.08))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, zorder=0)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path
