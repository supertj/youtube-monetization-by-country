# YouTube monetization signals by country

How often YouTube channels in each country show the public signals of a channel in the
YouTube Partner Program. October 2026 snapshot: 51 countries, 4,514 channels checked,
recomputed on 19 October 2026.

Live version, updated weekly: https://monetizationkit.com/data/youtube-monetized-channels-by-country/

The scoring rule and the sample have both changed since the September 2026 snapshot. Read the
[changelog](#changelog) before comparing the two.

## Why this exists

YouTube removed the public `is_monetization_enabled` flag in November 2023. Since then nobody
outside YouTube can read a channel's monetization status directly — every "monetization checker"
on the internet, ours included, is inferring it from public signals. Most of them still advertise
95% accuracy for a number that stopped being publicly available three years ago.

We publish what we can actually observe, including the share we cannot call either way.

## Files

| File | What it is |
|---|---|
| `youtube-monetization-signals-by-country.csv` | The October 2026 snapshot. One row per country. Counts, not percentages. |
| `datapackage.json` | Frictionless Data descriptor with column types. |
| `analysis/2026-10-membership-rule/data/youtube-monetization-signals-by-country-2026-09.csv` | The September 2026 snapshot, unchanged. |

## The book

A Jupyter Book walks through the September 2026 snapshot: how the sample was drawn, how a
verdict is made, the country shares with their uncertainty, and how the September scoring rule
shaped the bottom of the ranking. Its notebooks recompute every figure from the September file
listed above, not from the October CSV. The analysis in `analysis/2026-10-membership-rule` also
starts from the September snapshot.

Read it at https://monetizationkit.com/data/book/. The source is in `book/`, with build
instructions in `book/README.md`.

## Columns

| Column | Meaning |
|---|---|
| `country_code` | ISO 3166-1 alpha-2 code of the country the channel lists on its own page |
| `country` | English country name |
| `channels_checked` | Sample size for the row. Countries under 30 are not published. |
| `likely_monetized` | Channels showing the signals of a channel in the Partner Program |
| `possibly_monetized` | Some signals present, others absent or unreadable |
| `likely_not_monetized` | Signals consistently absent |
| `unable_to_determine` | We could not read enough to say. 24.0% of the channels in this file. |
| `median_subscribers` | Median subscriber count of the channels checked in that country. Empty since October 2026, see the changelog. |

The four verdict columns sum to `channels_checked`.

## How the sample was drawn

Every channel we have checked that lists a country counts once, under its latest check. The
channels come from three places:

- **The September 2026 sample.** For all 111 regions the YouTube Data API exposes, we pulled
  `videos.list?chart=mostPopular` across 10 content categories, then took the owning channels.
  That produced 13,388 channels, 10,348 of which declare a country. Countries were then filled
  toward a target sample size rather than sampled round-robin, so a published row has enough
  channels to mean something. We no longer use the Data API, and this sample is not being redrawn.
- **Lookups.** Channels people checked with the MonetizationKit checker.
- **Scheduled checks.** About a dozen well-known channels we recheck to keep the cache warm.

The October snapshot counts 4,514 channels: 3,182 from the September sample and the scheduled
checks, and 1,332 from lookups. Countries with fewer than 30 checked channels are not published,
so the 51 rows here add up to 4,382.

## What this is not

None of this is a random sample of a country's channels. The September sample is **trending**
channels, and most of them have hundreds of thousands of subscribers. Lookups are whichever
channels people were curious about. A low share for a country does not mean creators there rarely
get monetized. It means the channels we checked there showed fewer public signals.

The mix also varies by country. Since the September sample hasn't been redrawn, new rows come
from lookups, and they are concentrated in a few countries: the United States went from 66
channels in September to 457, India from 60 to 367. In 28 of the 50 September countries the
count moved by six channels or fewer.

Read a row as: *of the channels we checked in this country, this many showed the signals.*
Not as the country's monetization rate.

One known bias we found and fixed in September: our own crawler was being rate-limited, which
inflated `unable_to_determine` for whichever countries happened to be crawled in a throttled
hour. In an early crawl of about 900 channels (5 September 2026), the US read 37.1% unable;
after slowing the crawl and rechecking, it came down to 14.3% in that early sample. The sample
then grew to the 3,192 channels of the September snapshot, where the US row read 16 unable out
of 66 (24.2%). Failure rates are now monitored over time, not just in aggregate.

## Changelog

### October 2026 (recomputed 19 October 2026)

**The scoring rule changed.** In September a channel needed the memberships Join button to count
as likely monetized. Since 29 September 2026, a channel with enough subscribers and ads on its
recent long-form videos also counts when it has a store on the channel or 100,000 or more
subscribers. Since 1 October 2026 we also recognise the channel's Store tab, the ad signal counts
videos with ads instead of taking a share (positive with ads on two or more sampled long videos,
or on all of them; negative only when none of at least three had ads), and channels set as made
for kids are no longer marked down for having no memberships or store, since YouTube turns both
off for them. All September checks were re-scored under these rules, so every row in this file
uses the same definition.

**The sample grew.** 4,514 channels checked, up from 3,192. The published rows hold 4,382, up
from 3,080. 1,332 of the 4,514 came from lookups. Australia reached 30 checked channels and
appears for the first time, with 38. No country dropped out.

**The results moved a lot.** Across the published rows:

| Verdict | September (3,080 channels) | October (4,382 channels) |
|---|---|---|
| Likely monetized | 784 (25.5%) | 2,247 (51.3%) |
| Possibly monetized | 1,521 (49.4%) | 778 (17.8%) |
| Likely not monetized | 158 (5.1%) | 306 (7.0%) |
| Unable to determine | 617 (20.0%) | 1,051 (24.0%) |

The likely-monetized share went up in all 50 countries that were in the September file. Thailand
is now at the top with 50 of 63 (79.4%); in September it was Taiwan with 29 of 60 (48.3%). The
United States is now at the bottom with 158 of 457 (34.6%), where in September Kazakhstan,
Tanzania and Bangladesh had none at all. The bottom eight in September were the eight countries
in the file where YouTube doesn't offer channel memberships. In October they range from 6th to
48th of 51; Iraq went from 2 of 60 to 40 of 60.

**`median_subscribers` is empty.** We stopped computing it on 1 October 2026, when we changed how
long we keep channel details from YouTube (30 days at most). The column is still in the file so
code written for the September version keeps working, but every value in it is empty.

**The country field is read from the channel page.** Since 1 October 2026 we read channels from
their public YouTube pages instead of the Data API. The country is still the one the creator
sets on the channel.

### September 2026

First release. 50 countries, 3,192 channels checked, 3,080 of them in the published rows.
Archived on Zenodo as https://doi.org/10.5281/zenodo.23401599.

## Licence

CC BY 4.0. Reuse commercially, republish the table, build on it — just credit it.

## Citation

> MonetizationKit. YouTube monetization signals by country. October 2026.
> https://monetizationkit.com/data/youtube-monetized-channels-by-country/

Archived on Zenodo with a DOI:

- All versions (resolves to the latest): https://doi.org/10.5281/zenodo.23401598
- September 2026 snapshot: https://doi.org/10.5281/zenodo.23401599

`CITATION.cff` in this repository has the same details in a machine-readable form.

## Contact

hi@monetizationkit.com
