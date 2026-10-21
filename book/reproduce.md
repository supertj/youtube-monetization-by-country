---
title: Rebuild it yourself
description: How to rerun the notebooks and rebuild this book from the repository, with the exact package versions used.
---

The book, its notebooks and the data are all in one GitHub repository, `supertj/youtube-monetization-by-country`. The book lives in the `book` folder and reads the CSV files from the rest of the repository by relative path, so nothing is downloaded while it builds.

## Run the notebooks

You need Python 3.12. From a clone of the repository:

```bash
cd book
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install jupyterlab
jupyter lab
```

Open `country-shares.ipynb` or `scoring-rule.ipynb` and run all cells. Each one finishes in a few seconds. The shared chart colours are in `plotstyle.py`, next to the notebooks.

## Build the book

This is a Jupyter Book 2 project, built on MyST. The same environment builds it. Jupyter Book 2 also needs Node.js 18 or newer; if `node` is not on your path, the `jupyter book` command offers to install a private copy.

```bash
jupyter book start --execute          # live preview on a local port
jupyter book build --html --execute   # static site in _build/html
```

`--execute` runs both notebooks during the build, so the figures and the numbers in the notebook chapters' text come from the CSV files as they are at that moment. Change a CSV and rebuild, and the text follows.

## Versions used for this edition

| Package | Version |
|---|---|
| Python | 3.12 |
| jupyter-book | 2.1.7 |
| pandas | 2.2.3 |
| numpy | 2.1.3 |
| matplotlib | 3.9.2 |
| ipykernel | 7.4.0 |

The same pins are in `book/requirements.txt`.

## A longer analysis

The folder `analysis/2026-10-membership-rule` holds a standalone script that goes further than the last chapter of this book. Among other things it simulates how much spread between countries sampling noise alone would produce, and tests whether the share of unknowns differs between countries with and without channel memberships. Its README explains how to run it.
