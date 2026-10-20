# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "pandas==2.2.3",
#     "numpy==2.1.3",
#     "matplotlib==3.9.2",
# ]
# ///
"""
Analysis behind the article "The rule was the ranking".

Run:  uv run analysis.py
Writes: fig1-september-ranking.png, fig2-september-vs-october.png,
        fig3-noise-check.png, results.txt

Inputs (all in ./data):
- youtube-monetization-signals-by-country-2026-09.csv
  The September 2026 snapshot, CC BY 4.0, MonetizationKit.
  Zenodo: https://doi.org/10.5281/zenodo.23401599
  Same file, pinned commit:
  https://raw.githubusercontent.com/supertj/youtube-monetization-by-country/8d3ba4940d8e19f65527ac68cbde2b150177e56f/youtube-monetization-signals-by-country.csv
- country-monetization-recomputed-2026-10-19.csv
  The live table as recomputed on 19 October 2026, downloaded 20 October 2026 from
  https://monetizationkit.com/api/data/country-monetization/ (CC BY 4.0).
  The live file changes every Monday, so the copy used here is kept.
- youtube-channel-memberships-locations-2026-10-20.csv
  "Channel memberships are currently available to eligible creators in the following
  locations", transcribed from https://support.google.com/youtube/answer/7636690
  on 20 October 2026, with ISO 3166-1 alpha-2 codes added.
"""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
RNG = np.random.default_rng(20261020)  # fixed seed so every run prints the same numbers
SIMULATIONS = 100_000

# Chart tokens (light surface). Two categorical slots, validated for colour-vision deficiency.
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
BLUE = "#2a78d6"  # memberships available
ORANGE = "#eb6834"  # memberships not available
NEUTRAL = "#c3c2b7"

plt.rcParams.update(
    {
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": INK,
        "axes.labelcolor": INK_SECONDARY,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_SECONDARY,
        "axes.edgecolor": AXIS,
    }
)

report_lines: list[str] = []


def report(line: str = "") -> None:
    print(line)
    report_lines.append(line)


def spearman(a, b) -> float:
    """Rank correlation without SciPy: Pearson on average ranks."""
    return float(np.corrcoef(pd.Series(a).rank(), pd.Series(b).rank())[0, 1])


def add_shares(table: pd.DataFrame, membership_codes: set[str]) -> pd.DataFrame:
    table = table.copy()
    checked = table["channels_checked"]
    table["memberships_available"] = table["country_code"].isin(membership_codes)
    table["likely_share"] = table["likely_monetized"] / checked
    table["any_positive_share"] = (table["likely_monetized"] + table["possibly_monetized"]) / checked
    table["unable_share"] = table["unable_to_determine"] / checked
    table["likely_share_of_determined"] = table["likely_monetized"] / (
        checked - table["unable_to_determine"]
    )
    return table


# keep_default_na=False: "NA" is Namibia's country code, not a missing value
september = pd.read_csv(DATA / "youtube-monetization-signals-by-country-2026-09.csv", keep_default_na=False)
october = pd.read_csv(DATA / "country-monetization-recomputed-2026-10-19.csv", keep_default_na=False)
memberships = pd.read_csv(DATA / "youtube-channel-memberships-locations-2026-10-20.csv", keep_default_na=False)
membership_codes = set(memberships["iso2"])
assert len(membership_codes) == 100, "the YouTube page listed 100 locations on 2026-10-20"

september = add_shares(september, membership_codes)
october = add_shares(october, membership_codes)
verdicts = ["likely_monetized", "possibly_monetized", "likely_not_monetized", "unable_to_determine"]
assert (september[verdicts].sum(axis=1) == september["channels_checked"]).all()
assert (october[verdicts].sum(axis=1) == october["channels_checked"]).all()

# ---------------------------------------------------------------------------
# 1. The September ranking against one binary: are channel memberships offered?
# ---------------------------------------------------------------------------
report("== 1. September snapshot, split by channel-membership availability ==")
report(f"countries: {len(september)}, channels: {september['channels_checked'].sum():,}")
by_group = september.groupby("memberships_available")[["channels_checked", *verdicts]].sum()
for available, row in by_group.iterrows():
    label = "memberships available" if available else "memberships NOT available"
    countries = int((september["memberships_available"] == available).sum())
    n = row["channels_checked"]
    report(
        f"{label}: {countries} countries, {n:,} channels | "
        f"likely {row['likely_monetized'] / n:.1%} ({row['likely_monetized']}), "
        f"likely+possibly {(row['likely_monetized'] + row['possibly_monetized']) / n:.1%}, "
        f"likely not {row['likely_not_monetized'] / n:.1%}, "
        f"unable {row['unable_to_determine'] / n:.1%}"
    )

without = september[~september["memberships_available"]].sort_values("likely_share")
with_memberships = september[september["memberships_available"]]
report("countries without memberships: " + ", ".join(without["country"]))
report(
    f"highest 'likely' count among them: {without['likely_monetized'].max()} of 60; "
    f"lowest among membership countries: {with_memberships['likely_monetized'].min()} "
    f"({', '.join(with_memberships.nsmallest(2, 'likely_share')['country'])})"
)
ranked = september.sort_values("likely_share", ascending=False).reset_index(drop=True)
bottom_eight = set(ranked.tail(8)["country_code"])
report(f"bottom eight of the ranking == the eight without memberships: {bottom_eight == set(without['country_code'])}")

total_ss = ((september["likely_share"] - september["likely_share"].mean()) ** 2).sum()
within_ss = (
    (september["likely_share"] - september.groupby("memberships_available")["likely_share"].transform("mean")) ** 2
).sum()
report(f"share of cross-country variance explained by the membership split: {1 - within_ss / total_ss:.1%}")

# ---------------------------------------------------------------------------
# 2. Same channels, new rule: September vs the 19 October recompute
# ---------------------------------------------------------------------------
report()
report("== 2. September rule vs October rule ==")
both = september.merge(october, on="country_code", suffixes=("_sep", "_oct"))
both["added_channels"] = both["channels_checked_oct"] - both["channels_checked_sep"]
# The October table also holds channels people looked up on the site. Keep countries
# where at most 6 channels were added or removed, so at least ~90% of each row is the
# same September sample, scored again under the new rules.
same_sample = both[both["added_channels"].abs() <= 6].copy()
report(f"countries in both tables: {len(both)}; with |change in channels| <= 6: {len(same_sample)}")
for available, group in same_sample.groupby("memberships_available_sep"):
    label = "memberships available" if available else "memberships NOT available"
    report(
        f"{label}: {len(group)} countries, mean likely share "
        f"{group['likely_share_sep'].mean():.1%} -> {group['likely_share_oct'].mean():.1%} "
        f"(+{(group['likely_share_oct'] - group['likely_share_sep']).mean() * 100:.1f} points)"
    )
for code in ["IQ", "TZ"]:
    row = both[both["country_code"] == code].iloc[0]
    report(
        f"{row['country_sep']}: {row['channels_checked_sep']} -> {row['channels_checked_oct']} channels, "
        f"likely {row['likely_monetized_sep']} -> {row['likely_monetized_oct']}"
    )
report(
    f"rank correlation of likely share, September vs October, same-sample countries: "
    f"{spearman(same_sample['likely_share_sep'], same_sample['likely_share_oct']):.2f}"
)
same_sample_members = same_sample[same_sample["memberships_available_sep"]]
report(
    f"  ...membership countries only ({len(same_sample_members)}): "
    f"{spearman(same_sample_members['likely_share_sep'], same_sample_members['likely_share_oct']):.2f}"
)
report(
    f"rank correlation, all {len(both)} countries in both tables: "
    f"{spearman(both['likely_share_sep'], both['likely_share_oct']):.2f}"
)
october_ranked = october.sort_values("likely_share", ascending=False).reset_index(drop=True)
october_ranked["rank"] = october_ranked.index + 1
report(f"October table: {len(october)} countries, {october['channels_checked'].sum():,} channels")
for _, row in october_ranked[~october_ranked["memberships_available"]].iterrows():
    report(f"  October rank {row['rank']:>2} of {len(october)}: {row['country']} ({row['likely_share']:.1%})")
top10_sep = set(ranked.head(10)["country_code"])
top10_oct = set(october_ranked.head(10)["country_code"])
report(f"countries in both top 10s: {len(top10_sep & top10_oct)}")

# ---------------------------------------------------------------------------
# 3. How much of the spread among membership countries is binomial noise?
# ---------------------------------------------------------------------------
report()
report("== 3. Noise check, 42 membership countries, September ==")
checked = with_memberships["channels_checked"].to_numpy()
noise_summary = {}
for column, hits in [
    ("likely_share", with_memberships["likely_monetized"]),
    ("any_positive_share", with_memberships["likely_monetized"] + with_memberships["possibly_monetized"]),
    ("unable_share", with_memberships["unable_to_determine"]),
]:
    pooled = hits.sum() / checked.sum()
    observed_var = with_memberships[column].var(ddof=1)
    noise_var = (pooled * (1 - pooled) / checked).mean()
    # If every country had the pooled rate, how spread out would 42 shares be?
    simulated = RNG.binomial(checked[None, :], pooled, size=(SIMULATIONS, len(checked))) / checked[None, :]
    simulated_sd = simulated.std(axis=1, ddof=1)
    observed_sd = with_memberships[column].std(ddof=1)
    noise_summary[column] = (pooled, observed_sd, simulated_sd)
    report(
        f"{column}: pooled {pooled:.1%}; observed SD {observed_sd * 100:.1f} pts; "
        f"SD from noise alone (median of sims) {np.median(simulated_sd) * 100:.1f} pts; "
        f"noise variance / observed variance {noise_var / observed_var:.0%}; "
        f"sims with SD >= observed: {(simulated_sd >= observed_sd).mean():.4%}"
    )

pooled_likely = with_memberships["likely_monetized"].sum() / checked.sum()
low = np.array([np.percentile(RNG.binomial(n, pooled_likely, 20_000), 2.5) for n in checked])
high = np.array([np.percentile(RNG.binomial(n, pooled_likely, 20_000), 97.5) for n in checked])
outside = (with_memberships["likely_monetized"].to_numpy() < low) | (with_memberships["likely_monetized"].to_numpy() > high)
report(
    f"membership countries outside the 95% noise band around {pooled_likely:.1%}: {outside.sum()} of {len(checked)} "
    f"(about {0.05 * len(checked):.0f} expected by chance): {', '.join(with_memberships['country'][outside])}"
)
band_half_width = 1.96 * np.sqrt(pooled_likely * (1 - pooled_likely) / 60)
report(f"95% noise band at n=60: {pooled_likely - band_half_width:.1%} to {pooled_likely + band_half_width:.1%}")
inside = with_memberships["likely_share"].between(pooled_likely - band_half_width, pooled_likely + band_half_width)
report(f"membership countries whose share falls inside that n=60 band: {inside.sum()} of {len(with_memberships)}")


def two_share_p_value(code_a: str, code_b: str) -> None:
    """Two-sided two-proportion z-test, to show what a 'big' gap looks like at n of about 60."""
    a = september.set_index("country_code").loc[code_a]
    b = september.set_index("country_code").loc[code_b]
    p_a, p_b = a["likely_share"], b["likely_share"]
    se = np.sqrt(p_a * (1 - p_a) / a["channels_checked"] + p_b * (1 - p_b) / b["channels_checked"])
    z = (p_a - p_b) / se
    p_value = math.erfc(abs(z) / math.sqrt(2))
    report(f"{a['country']} {p_a:.1%} vs {b['country']} {p_b:.1%}: gap {(p_a - p_b) * 100:.1f} pts, z {z:.2f}, p {p_value:.2f}")


two_share_p_value("HU", "BG")
report(
    f"rank correlation, median subscribers vs likely share (membership countries): "
    f"{spearman(with_memberships['median_subscribers'], with_memberships['likely_share']):.2f}"
)

# ---------------------------------------------------------------------------
# 4. "Unable to determine" is not spread evenly
# ---------------------------------------------------------------------------
report()
report("== 4. Unable to determine ==")
unable_without = september.loc[~september["memberships_available"], "unable_share"]
unable_with = september.loc[september["memberships_available"], "unable_share"]
observed_gap = unable_without.mean() - unable_with.mean()
labels = september["memberships_available"].to_numpy().copy()
unable = september["unable_share"].to_numpy()
at_least_as_large = 0
for _ in range(SIMULATIONS):
    RNG.shuffle(labels)
    at_least_as_large += (unable[~labels].mean() - unable[labels].mean()) >= observed_gap
report(
    f"mean unable share: without memberships {unable_without.mean():.1%}, with {unable_with.mean():.1%}; "
    f"gap {observed_gap * 100:.1f} pts; permutation p = {at_least_as_large / SIMULATIONS:.4f}"
)
report(
    f"overall unable: {september['unable_to_determine'].sum()} of {september['channels_checked'].sum():,} "
    f"({september['unable_to_determine'].sum() / september['channels_checked'].sum():.1%})"
)
report(
    f"rank correlation, likely share of all checked vs of determined only: "
    f"{spearman(september['likely_share'], september['likely_share_of_determined']):.2f}"
)
widest = september.assign(
    upper=(september["likely_monetized"] + september["unable_to_determine"]) / september["channels_checked"]
).nlargest(3, "unable_share")
for _, row in widest.iterrows():
    report(
        f"  {row['country']}: likely {row['likely_share']:.1%}, could be up to {row['upper']:.1%} "
        f"if every unknown were likely ({row['unable_to_determine']} unknown)"
    )

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def tidy(ax) -> None:
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(length=0)


# Figure 1: September ranking, coloured by memberships availability
fig, ax = plt.subplots(figsize=(8, 11))
order = september.sort_values("likely_share").reset_index(drop=True)
y = np.arange(len(order))
ax.axvspan(
    pooled_likely - band_half_width, pooled_likely + band_half_width, color=GRID, alpha=0.6, lw=0, zorder=0
)
ax.text(
    pooled_likely,
    len(order) + 0.2,
    f"range a country at {pooled_likely:.0%} could land in\nby chance alone (95%, 60 channels)",
    ha="center",
    va="bottom",
    fontsize=8.5,
    color=INK_SECONDARY,
)
colors = np.where(order["memberships_available"], BLUE, ORANGE)
ax.hlines(y, 0, order["likely_share"], color=GRID, lw=1, zorder=1)
ax.scatter(order["likely_share"], y, s=42, c=colors, edgecolors=SURFACE, linewidths=1.5, zorder=3)
ax.set_yticks(y, order["country"], fontsize=8.5)
ax.set_ylim(-0.8, len(order) + 2.2)
ax.set_xlim(-0.012, 0.55)
ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
ax.grid(axis="x", color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_xlabel('Share of checked channels rated "Likely monetized" (September 2026 rule)')
tidy(ax)
ax.axhline(7.5, color=INK_MUTED, lw=0.8, ls=(0, (3, 3)))
ax.text(0.54, 3.5, "No channel\nmemberships\nin these eight", ha="right", va="center", fontsize=9, color=INK_SECONDARY)
ax.legend(
    handles=[
        plt.Line2D([], [], marker="o", ls="", color=BLUE, markersize=7, label="YouTube offers channel memberships"),
        plt.Line2D([], [], marker="o", ls="", color=ORANGE, markersize=7, label="It doesn't"),
    ],
    loc="lower right",
    bbox_to_anchor=(1.0, 0.30),
    frameon=False,
    fontsize=9,
)
fig.suptitle(
    "The bottom eight are the eight countries without channel memberships",
    x=0.02,
    ha="left",
    fontsize=13,
    fontweight="semibold",
)
fig.text(
    0.02,
    0.952,
    "50 countries, 3,080 trending channels. Memberships list: YouTube Help, read 20 Oct 2026.",
    fontsize=9,
    color=INK_SECONDARY,
)
fig.tight_layout(rect=(0, 0, 1, 0.955))
fig.savefig(HERE / "fig1-september-ranking.png", dpi=200)
plt.close(fig)

# Figure 2: slope chart, same-sample countries, September rule vs October rule
fig, ax = plt.subplots(figsize=(7, 7.5))
for _, row in same_sample.sort_values("memberships_available_sep", ascending=False).iterrows():
    available = row["memberships_available_sep"]
    color = BLUE if available else ORANGE
    ax.plot(
        [0, 1],
        [row["likely_share_sep"], row["likely_share_oct"]],
        color=color,
        lw=1.2 if available else 2,
        alpha=0.45 if available else 1,
        marker="o",
        markersize=4 if available else 6,
        markeredgecolor=SURFACE,
        zorder=2 if available else 3,
    )
labelled = same_sample[~same_sample["memberships_available_sep"]].sort_values("likely_share_oct")
label_y = labelled["likely_share_oct"].to_numpy().copy()
for i in range(1, len(label_y)):  # nudge labels apart so they never overlap
    label_y[i] = max(label_y[i], label_y[i - 1] + 0.022)
for (_, row), y_text in zip(labelled.iterrows(), label_y):
    ax.text(
        1.04,
        y_text,
        f"{row['country_sep']}  {row['likely_monetized_sep']}→{row['likely_monetized_oct']} of {row['channels_checked_oct']}",
        va="center",
        fontsize=8.5,
        color=INK_SECONDARY,
    )
ax.set_xticks([0, 1], ["September rule\n(Join button required)", "October rule\n(Join, store, or 100k+ subscribers)"])
ax.set_xlim(-0.15, 1.75)
ax.set_ylim(-0.02, 0.85)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
ax.grid(axis="y", color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_ylabel('Share rated "Likely monetized"')
tidy(ax)
ax.spines["bottom"].set_visible(False)
ax.legend(
    handles=[
        plt.Line2D([], [], color=BLUE, lw=1.5, label=f"Memberships available ({len(same_sample_members)} countries)"),
        plt.Line2D(
            [], [], color=ORANGE, lw=2, label=f"Not available ({len(same_sample) - len(same_sample_members)} countries)"
        ),
    ],
    loc="upper left",
    frameon=False,
    fontsize=9,
)
fig.suptitle("Same countries, new rule", x=0.02, ha="left", fontsize=13, fontweight="semibold")
fig.text(
    0.02,
    0.925,
    f"{len(same_sample)} countries whose sample changed by 6 channels or fewer between the two tables",
    fontsize=9,
    color=INK_SECONDARY,
)
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig(HERE / "fig2-september-vs-october.png", dpi=200)
plt.close(fig)

# Figure 3: the observed spread against the spread pure noise would produce
pooled, observed_sd, simulated_sd = noise_summary["likely_share"]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.hist(simulated_sd * 100, bins=80, color=NEUTRAL, edgecolor=SURFACE, linewidth=0.5)
ax.axvline(observed_sd * 100, color=BLUE, lw=2)
ax.text(
    observed_sd * 100 - 0.15,
    ax.get_ylim()[1] * 0.92,
    f"observed: {observed_sd * 100:.1f} points",
    ha="right",
    va="top",
    fontsize=9,
    color=INK,
)
ax.text(
    np.median(simulated_sd) * 100,
    ax.get_ylim()[1] * 1.02,
    f"noise alone: about {np.median(simulated_sd) * 100:.1f}",
    ha="center",
    va="bottom",
    fontsize=9,
    color=INK_SECONDARY,
)
ax.set_xlabel('Standard deviation of the "Likely" share across 42 countries (percentage points)')
ax.set_yticks([])
ax.grid(axis="x", color=GRID, lw=0.8)
ax.set_axisbelow(True)
tidy(ax)
fig.suptitle(
    "Noise explains some of the spread, not all of it", x=0.02, ha="left", fontsize=13, fontweight="semibold"
)
fig.text(
    0.02,
    0.87,
    f"Grey: {SIMULATIONS:,} simulated samples in which every membership country has the same {pooled:.1%} rate",
    fontsize=9,
    color=INK_SECONDARY,
)
fig.tight_layout(rect=(0, 0, 1, 0.86))
fig.savefig(HERE / "fig3-noise-check.png", dpi=200)
plt.close(fig)

(HERE / "results.txt").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
