---
title: How a verdict is made
description: The five public signals behind each verdict, the rule used for the September 2026 snapshot, what changed in October, and the limits of reading a country's share.
---

Every channel gets one of four verdicts: likely monetized, possibly monetized, likely not monetized, or unable to determine. The verdict is built from five signals. Anyone can see all five on a channel's public YouTube pages without logging in. Nothing comes from YouTube Studio or from the channel owner.

## The five signals

| Signal | What it is | How much it tells you |
|---|---|---|
| S1: 1,000+ subscribers | The subscriber requirement for the ad-revenue tier of the Partner Program | Necessary, not sufficient. Many channels above 1,000 are not in the program. |
| S2: Join button | Channel memberships, which only Partner Program channels can offer | Strong when present. Its absence says little: many partner channels never turn memberships on, and YouTube does not offer them in every country. |
| S3: Ads on recent long-form videos | Ad slots on a sample of the channel's recent long videos | Good evidence, not proof. YouTube can run ads on channels outside the program, in the US since November 2020 and elsewhere since June 2021. |
| S4: Store tab or merch shelf | A store connected to the channel, which requires the Partner Program | Strong when present. Most channels have no store, so its absence is normal. |
| S5: 500+ subscribers | The lowest subscriber threshold of any Partner Program tier | Works as a negative signal: below 500, no tier is open. |

## The September 2026 rule

The September 2026 snapshot was scored with the rule MonetizationKit used in early September 2026. At that time the ad signal (S3) counted as present when at least two thirds of the sampled long videos had ads.

Likely monetized
: 1,000+ subscribers, a Join button, and ads on recent long videos. All three.

Possibly monetized
: A Join button, ads, or a merch shelf, without all three conditions above.

Likely not monetized
: No positive signal and fewer than 500 subscribers. Or 1,000+ subscribers with the Join button, ads and merch shelf all read and all absent.

Unable to determine
: Neither the channel page nor the ad sample could be read, or what could be read pointed neither way.

The first line is the one that matters later. A channel could only be rated likely monetized with a Join button, and YouTube does not offer channel memberships everywhere. [How the scoring rule shaped the ranking](scoring-rule.ipynb) shows what that did to the country ranking.

## What changed at the turn of October

Between 29 September and 1 October 2026 the rule changed in four ways:

- A channel with 1,000+ subscribers and ads on its recent long videos also counts as likely monetized when it has a store, or 100,000 or more subscribers. The Join button is no longer the only way in.
- The ad signal counts videos instead of a share. It is positive with ads on two or more sampled long videos, or on every one that could be sampled. It is negative only when none of at least three had ads. Anything in between leaves it unknown.
- Channels set as made for kids are no longer marked down for having no memberships or store, because YouTube switches both off for them.
- The Store tab counts as well as the older merch shelf.

Every stored check behind the live table was re-scored under the new rule, so the live table uses one definition throughout. The September snapshot on Zenodo stays as it was published. That is why the last chapter reads it next to a copy of the table recomputed on 19 October.

## Limits

### Trending channels, not typical ones

The channels come from trending charts, and most of them have hundreds of thousands of subscribers. The `median_subscribers` column gives the figure for each country. A low share for a country does not mean creators there rarely get monetized. It means the large channels we checked showed fewer public signals.

### A row is not a monetization rate

Read a row as: of the channels we checked in this country, this many showed the signals. With about 60 channels per country, each share also carries a wide margin of error. [Shares by country](country-shares.ipynb) puts numbers on it.

### One in five could not be called

A channel ends up as unable to determine when its pages could not be read, when YouTube blocked the ad sample, or when the signals pointed neither way. These channels are kept as their own group, not guessed into another one. They are not spread evenly across countries, which matters when two countries are compared.

### A bias in our own crawler

The dataset README describes one bias found and fixed before publication. The crawler was being rate-limited, which inflated "unable to determine" for whichever countries happened to be crawled in a throttled hour. In an early crawl of about 900 channels on 5 September 2026, the United States read 37.1% unable. After the crawl was slowed and those channels rechecked, the figure in that early sample came down to 14.3%. In the full snapshot, the US row reads 16 unable out of 66. Failure rates are now watched over time, not only in aggregate.

### A signal can only appear where YouTube offers it

Channel memberships, stores and the Partner Program itself are not available in every country. Russia, one of the 50 countries in the snapshot, was not on YouTube's list of countries where the Partner Program is open when MonetizationKit last checked that list on 1 October 2026. Where a feature does not exist, a missing signal is not evidence of anything. The last chapter shows how much this mattered for memberships.

### Public pages only

We see what a logged-out visitor sees: no earnings, no Studio data, nothing from the owner. A verdict is an inference from public signals, not a statement from YouTube.
