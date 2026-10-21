#!/usr/bin/env bash
# Build the book for https://monetizationkit.com/data/book/ and copy it into a checkout of the
# MonetizationKit website repository. Usage: ./build-for-site.sh /path/to/monetizationkit
set -euo pipefail

# Resolve to an absolute path before the cd below, so a relative argument can't point somewhere else
site_repo="$(cd -- "${1:?usage: $0 /path/to/monetizationkit}" >/dev/null && pwd)"
# Guard against wiping the wrong directory: the target must look like the website repository
if [[ ! -f "$site_repo/next.config.ts" || ! -d "$site_repo/public" ]]; then
  echo "$site_repo does not look like the MonetizationKit website repository" >&2
  exit 1
fi
target="$site_repo/public/data/book"

cd "$(dirname "$0")"
# Start from a clean _build: _build/site keeps every figure and download from earlier builds, and
# the execution cache in _build/execute is keyed on the notebook source, not on the CSV files the
# notebooks read, so a corrected CSV would otherwise republish old numbers. Execution takes seconds.
rm -rf _build/html _build/site _build/execute
BASE_URL=/data/book jupyter book build --html --execute

# MyST writes these for a site at the domain root and points them at localhost. The website's own
# robots.txt and sitemap.xml cover the book pages instead.
rm -f _build/html/robots.txt _build/html/sitemap.xml _build/html/sitemap_style.xsl

rm -rf "$target"
mkdir -p "$target"
cp -R _build/html/. "$target/"
echo "Copied $(find "$target" -type f | wc -l | tr -d ' ') files to $target"
