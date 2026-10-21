---
title: YouTube monetization signals by country
short_title: Introduction
description: An open dataset on 3,080 trending YouTube channels in 50 countries, read closely. Where the channels came from, how each verdict is made, what the country shares look like with their uncertainty, and notebooks that recompute every number.
---

Nobody outside YouTube can look up whether a channel is monetized. YouTube stopped exposing the `is_monetization_enabled` flag in November 2023, so every tool that answers the question infers it from what a channel shows in public: a Join button, a store, ads on its videos, a subscriber count above the Partner Program thresholds.

In September 2026 we ran that inference on 3,192 trending channels and published the counts for the 50 countries where at least 30 had been checked, 3,080 channels in all. ("We" in this book is MonetizationKit, which runs the checker and publishes the data.) This book goes through that dataset slowly. It explains where the channels came from and how each verdict was reached, shows the country shares together with how uncertain they are, and works through the biggest problem we found in our own numbers: the bottom of the September ranking was produced by the scoring rule, not by the countries.

:::{figure} #fig-verdicts
:label: fig-verdicts-intro
Verdicts for the channels checked in each country under the September 2026 rule, sorted by the share rated likely monetized. Grey is the share we could not call either way. The figure is built in [Shares by country](country-shares.ipynb).
:::

## How to read the numbers

Three things to keep in mind before looking at any one country:

- A row describes the channels we checked in that country, not every channel there. They are trending channels: in all but one country, the median channel we checked has more than 100,000 subscribers.
- "Likely monetized" is an inference from public signals. YouTube has not confirmed any of these verdicts.
- One channel in five could not be called. Those channels stay in the table as "unable to determine".

## What is in the book

- [Where the data comes from](sampling.md): the sampling frame, the country field, the files and their columns.
- [How a verdict is made](method.md): the five signals, the rule behind the September snapshot, the rule used since October, and the limits.
- [Shares by country](country-shares.ipynb): the verdict mix in each country, and how much of the spread is sampling noise.
- [How the scoring rule shaped the ranking](scoring-rule.ipynb): why the eight countries at the bottom are the eight without channel memberships.
- [Rebuild it yourself](reproduce.md): commands and package versions.

The two notebook chapters show their code. Every figure and table is computed from the CSV files when the book is built, and so are the numbers in the notebook chapters' text. Facts about how the sample was drawn come from the dataset's README.

## Data, citation and licence

The data is free to reuse under CC BY 4.0, commercially too, as long as you credit it. To cite the September 2026 snapshot:

> MonetizationKit. YouTube monetization signals by country. September 2026. DOI 10.5281/zenodo.23401599

DOI 10.5281/zenodo.23401598 always resolves to the latest archived version. The live table is on the [MonetizationKit data page](https://monetizationkit.com/data/youtube-monetized-channels-by-country/).

The book, its notebooks and the data files are in the GitHub repository `supertj/youtube-monetization-by-country`, in the `book` folder. Questions and corrections go to hi@monetizationkit.com.
