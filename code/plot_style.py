"""Shared matplotlib style, carried over from the Post 4 repository. Import once at the top of every figure notebook:

    from plot_style import apply_style, COLORS, SITE, MAP_BINS, MAP_LABELS, MAP_COLORS, source_note

Figures carry a title, axis labels with units, a legend and a source line only.
No explanatory prose inside figures.
"""
import numpy as np
import matplotlib as mpl

# Site tokens, copied from Personal Website/theme.scss so figures sit on the page background
SITE = {
    "paper": "#fffdf9",      # $paper: page background
    "ink": "#16130f",        # $ink: titles
    "muted": "#6e6559",      # $muted: axis labels, ticks
    "faint": "#857b6c",      # $faint: source line, reference lines
    "rule": "#e6dfd2",       # $rule: gridlines, "no data" fill on maps
    "axis": "#b5ab9b",       # $fainter: axis spines, background dots
}

COLORS = {
    "total": SITE["ink"],
    "part1": "#2f5d7c",      # slate blue
    "part2": "#d19a3a",      # ochre
    "accent": "#a8442a",     # site $accent (rust): highlighted series
    "grey": SITE["faint"],
}

# Fig 1 map bins: percent change in the price-to-income ratio, 2015-19 to 2020-24.
# Diverging around zero: slate where incomes kept pace, warm ramp where prices pulled ahead.
MAP_BINS = [-np.inf, -10, 0, 10, 20, 30, np.inf]
MAP_LABELS = ["Fell more than 10%", "Fell up to 10%", "Rose up to 10%",
              "Rose 10% to 20%", "Rose 20% to 30%", "Rose more than 30%"]
MAP_COLORS = ["#2f5d7c", "#b3c6d4", "#f2dfbd", "#dcae5b", "#c3673a", "#7a2e1e"]


def apply_style():
    mpl.rcParams.update({
        "figure.facecolor": SITE["paper"],
        "axes.facecolor": SITE["paper"],
        "savefig.facecolor": SITE["paper"],
        "text.color": SITE["ink"],
        "axes.titlecolor": SITE["ink"],
        "axes.labelcolor": SITE["muted"],
        "axes.edgecolor": SITE["axis"],
        "xtick.color": SITE["muted"],
        "ytick.color": SITE["muted"],
        "legend.labelcolor": SITE["muted"],
        "figure.figsize": (9, 5),
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelsize": 12,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": SITE["rule"],
        "grid.linewidth": 0.8,
        "legend.frameon": False,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "lines.linewidth": 1.8,
    })


def source_note(fig, text, y=-0.02):
    """Source line in the bottom-left corner, outside the axes.
    Lower y (more negative) when a legend sits below the axes."""
    fig.text(0.01, y, f"Source: {text}", ha="left", va="top",
             fontsize=9, color=COLORS["grey"])
