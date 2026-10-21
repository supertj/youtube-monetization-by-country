# The book

Source of the Jupyter Book "YouTube monetization signals by country", published at
https://monetizationkit.com/data/book/

It is a Jupyter Book 2 (MyST) project. The two notebooks read the CSV files from the rest of
this repository by relative path, and the build executes them, so every figure and every number
in the notebook chapters comes from the data at build time. Notebooks are committed without
outputs for that reason.

## Build it

Python 3.12 and Node.js 18 or newer:

```bash
cd book
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter book start --execute          # live preview
jupyter book build --html --execute   # static site in _build/html
```

## Publish it on monetizationkit.com

The site is served as static files from the MonetizationKit website repository, under
`public/data/book/`. With that repository checked out on a feature branch:

```bash
./build-for-site.sh /path/to/monetizationkit
```

The script builds with `BASE_URL=/data/book`, drops the `robots.txt` and `sitemap.xml` that MyST
writes for a site at the domain root, and replaces `public/data/book/` in the website checkout.
If you add or rename a page, also update the page list in that repository's `src/app/sitemap.ts`.

## Files

| File | What it is |
|---|---|
| `myst.yml` | Book configuration and table of contents |
| `index.md`, `sampling.md`, `method.md`, `reproduce.md` | Text chapters |
| `country-shares.ipynb`, `scoring-rule.ipynb` | Notebook chapters |
| `plotstyle.py` | Chart colours shared by both notebooks |
| `style.css`, `images/` | Site colours, logo and favicon |
| `thumbnail.png` | Screenshot of the published book, for listings |
