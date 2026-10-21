#!/usr/bin/env bash
# Build the book for https://monetizationkit.com/data/book/ and copy it into a checkout of the
# MonetizationKit website repository. Usage: ./build-for-site.sh /path/to/monetizationkit
set -euo pipefail

site_repo="${1:?usage: $0 /path/to/monetizationkit}"
# Guard against wiping the wrong directory: the target must look like the website repository
if [[ ! -f "$site_repo/next.config.ts" || ! -d "$site_repo/public" ]]; then
  echo "$site_repo does not look like the MonetizationKit website repository" >&2
  exit 1
fi
target="$site_repo/public/data/book"

cd "$(dirname "$0")"
# _build/site keeps every figure and download from earlier builds; clear it with the output so
# stale files are not published. The execution cache in _build/execute is kept.
rm -rf _build/html _build/site
BASE_URL=/data/book jupyter book build --html --execute

# MyST writes these for a site at the domain root and points them at localhost. The website's own
# robots.txt and sitemap.xml cover the book pages instead.
rm -f _build/html/robots.txt _build/html/sitemap.xml _build/html/sitemap_style.xsl

rm -rf "$target"
mkdir -p "$target"
cp -R _build/html/. "$target/"
echo "Copied $(find "$target" -type f | wc -l | tr -d ' ') files to $target"
