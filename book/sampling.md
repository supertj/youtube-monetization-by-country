---
title: Where the data comes from
description: How the channels in the September 2026 snapshot were chosen, whose country the country column records, what gets published, and what each file and column holds.
---

## The sampling frame

The channels were not drawn at random from all of YouTube. According to the dataset README, the frame was built like this: for all 111 regions the YouTube Data API exposes, we pulled the most popular videos (`videos.list?chart=mostPopular`) in 10 content categories and took the channels that own them. That gave 13,388 channels, 10,348 of which declare a country. Countries were then filled toward a target sample size instead of being sampled round-robin, so that a published row has enough channels to say something.

This frame decides what the dataset can describe. These are channels whose videos were trending in September 2026, so they lean large and currently active. [How a verdict is made](method.md) comes back to what that means when you read a country's share.

MonetizationKit has since stopped using the YouTube Data API, so this sampling list is not kept and will not be repeated in the same form.

Each channel counts once in the table, however many times it was checked.

## Whose country

The country is the one the channel declares on YouTube. It is where the creator says they are, not where the audience watches from. Channels that leave the field blank are not in the dataset.

## What gets published

A country is published once at least 30 of its channels have been checked. Below that, one or two channels would move the share too much. The September 2026 snapshot covers 3,192 checked channels in total. The 50 countries that pass the threshold account for 3,080 of them, and those 3,080 are what the CSV holds. The other 112 belong to countries with fewer than 30 checked channels.

## Files

All paths are relative to the root of the repository.

| File | What it holds |
|---|---|
| `youtube-monetization-signals-by-country.csv` | The September 2026 snapshot. One row per country, counts rather than percentages. |
| `datapackage.json` | A Frictionless Data descriptor with the column types. |
| `analysis/2026-10-membership-rule/data/country-monetization-recomputed-2026-10-19.csv` | The country table as recomputed on 19 October 2026 under the revised rule, downloaded on 20 October. Used in the last chapter. |
| `analysis/2026-10-membership-rule/data/youtube-channel-memberships-locations-2026-10-20.csv` | The locations where YouTube Help listed channel memberships as available on 20 October 2026, with ISO codes added. |

## Columns of the snapshot

| Column | Meaning |
|---|---|
| `country_code` | ISO 3166-1 alpha-2 code, from the channel's own country field |
| `country` | English country name |
| `channels_checked` | Sample size for the row |
| `likely_monetized` | Channels showing the signals of a channel in the Partner Program |
| `possibly_monetized` | Some signals present, others absent or unreadable |
| `likely_not_monetized` | Signals consistently absent |
| `unable_to_determine` | Not enough could be read to say either way |
| `median_subscribers` | Median subscriber count of the channels checked in that country |

The four verdict columns add up to `channels_checked` in every row, and [Shares by country](country-shares.ipynb) checks that before using the file. If you load it yourself, read `country_code` as text. Namibia's code is `NA`, which pandas and R both turn into a missing value by default.

## Archived and live versions

The snapshot is archived on Zenodo. DOI 10.5281/zenodo.23401599 points to this September 2026 version, and DOI 10.5281/zenodo.23401598 to whichever version is the latest.

The [live table](https://monetizationkit.com/data/youtube-monetized-channels-by-country/) on MonetizationKit is recomputed every Monday and will not match the snapshot. Channels have been added since September, and the scoring rule changed between 29 September and 1 October 2026. [How the scoring rule shaped the ranking](scoring-rule.ipynb) compares the two.
