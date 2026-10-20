# How the memberships signal shaped the September country ranking

The September 2026 table ranked eight countries at the bottom. They turned out to be the eight countries in the table where YouTube doesn't offer channel memberships, and the September scoring rule needed the memberships Join button for a "likely monetized" verdict. This folder compares that snapshot with the table recomputed on 19 October 2026 under the revised rule, and checks how much of the spread between countries is sampling noise.

Run it with [uv](https://docs.astral.sh/uv/) (Python 3.12):

```
uv run analysis.py
```

It reads the three CSVs in `data/` and writes the three figures and `results.txt`. The random seed is fixed, so the numbers repeat.

## Inputs

- `data/youtube-monetization-signals-by-country-2026-09.csv`: the September snapshot, the same file as `youtube-monetization-signals-by-country.csv` in the repository root (Zenodo: https://doi.org/10.5281/zenodo.23401599).
- `data/country-monetization-recomputed-2026-10-19.csv`: the table recomputed on 19 October 2026, downloaded on 20 October from https://monetizationkit.com/api/data/country-monetization/ . The live file changes every Monday, so this copy is kept here.
- `data/youtube-channel-memberships-locations-2026-10-20.csv`: the locations where YouTube Help says channel memberships are available, transcribed on 20 October 2026 with ISO 3166-1 alpha-2 codes added.

The data files are CC BY 4.0, like the rest of this repository.
