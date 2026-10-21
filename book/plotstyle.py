"""Chart colours and axis styling shared by the notebooks in this book.

Kept in one file so both chapters draw with the same palette. The verdict colours were
checked for colour-vision deficiency (adjacent pairs) on the light surface below; grey is
deliberately neutral because "unable to determine" is the absence of an answer.
"""

import matplotlib
import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

VERDICT_COLOURS = {
    "likely_monetized": "#1c5cab",
    "possibly_monetized": "#6da7ec",
    "likely_not_monetized": "#eb6834",
    "unable_to_determine": "#c3c2b7",
}
VERDICT_LABELS = {
    "likely_monetized": "Likely monetized",
    "possibly_monetized": "Possibly monetized",
    "likely_not_monetized": "Likely not monetized",
    "unable_to_determine": "Unable to determine",
}

# Two groups in the scoring-rule chapter
MEMBERSHIPS = "#2a78d6"
NO_MEMBERSHIPS = "#eb6834"

PERCENT = matplotlib.ticker.PercentFormatter(1.0, decimals=0)

plt.rcParams.update(
    {
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "figure.dpi": 150,
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": INK,
        "axes.labelcolor": INK_SECONDARY,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_SECONDARY,
        "axes.edgecolor": AXIS,
    }
)


def tidy(ax) -> None:
    """Hairline grid on the value axis, no box, no tick marks."""
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(length=0)
    ax.set_axisbelow(True)
