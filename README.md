# YouTube monetization signals by country

How often YouTube channels in each country show the public signals of a channel in the
YouTube Partner Program. 50 countries, 3,192 channels checked, September 2026.

Live version, updated weekly: https://monetizationkit.com/data/youtube-monetized-channels-by-country/

## Why this exists

YouTube removed the public `is_monetization_enabled` flag in November 2023. Since then nobody
outside YouTube can read a channel's monetization status directly — every "monetization checker"
on the internet, ours included, is inferring it from public signals. Most of them still advertise
95% accuracy for a number that stopped being publicly available three years ago.

We publish what we can actually observe, including the share we cannot call either way.

## Files

| File | What it is |
|---|---|
| `youtube-monetization-signals-by-country.csv` | One row per country. Counts, not percentages. |
| `datapackage.json` | Frictionless Data descriptor with column types. |

## Columns

| Column | Meaning |
|---|---|
| `country_code` | ISO 3166-1 alpha-2, from the channel's own `country` field |
| `country` | English country name |
| `channels_checked` | Sample size for the row. Countries under 30 are not published. |
| `likely_monetized` | Channels showing the signals of a channel in the Partner Program |
| `possibly_monetized` | Some signals present, others absent or unreadable |
| `likely_not_monetized` | Signals consistently absent |
| `unable_to_determine` | We could not read enough to say. 20.1% of the whole sample. |
| `median_subscribers` | Median subscriber count of the channels checked in that country |

The four verdict columns sum to `channels_checked`.

## How the sample was drawn

The frame is the set of channels behind each region's most popular videos: for all 111 regions
the YouTube Data API exposes, we pulled `videos.list?chart=mostPopular` across 10 content
categories, then took the owning channels. That produced 13,388 channels, 10,348 of which
declare a country. Countries were then filled toward a target sample size rather than sampled
round-robin, so a published row has enough channels to mean something.

Each channel was checked once. A channel checked a hundred times still counts once.

## What this is not

These are **trending** channels, not typical ones — most have hundreds of thousands of
subscribers. A low share for a country does not mean creators there rarely get monetized. It
means the large channels we checked showed fewer public signals.

Read a row as: *of the channels we checked in this country, this many showed the signals.*
Not as the country's monetization rate.

One known bias we found and fixed: our own crawler was being rate-limited, which inflated
`unable_to_determine` for whichever countries happened to be crawled in a throttled hour.
In an early crawl of about 900 channels (5 September 2026), the US read 37.1% unable; after
slowing the crawl and rechecking, it came down to 14.3% in that early sample. The sample then
grew to the 3,192 channels in this snapshot, where the US row reads 16 unable out of 66 (24.2%).
Failure rates are now monitored over time, not just in aggregate.

## Licence

CC BY 4.0. Reuse commercially, republish the table, build on it — just credit it.

## Citation

> MonetizationKit. YouTube monetization signals by country. September 2026.
> https://monetizationkit.com/data/youtube-monetized-channels-by-country/

Archived on Zenodo with a DOI:

- All versions (resolves to the latest): https://doi.org/10.5281/zenodo.23401598
- This snapshot (September 2026): https://doi.org/10.5281/zenodo.23401599

`CITATION.cff` in this repository has the same details in a machine-readable form.

## Contact

hi@monetizationkit.com
