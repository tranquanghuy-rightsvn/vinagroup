#!/usr/bin/env bash
# Sync html/ from the "thien" remote (thien/master:v2), then commit + push to origin.
# Usage: bash scripts/sync-from-thien.sh
# SEO data per page: scripts/seo/pages.json (new pages from thien need an entry there).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

git remote get-url thien >/dev/null 2>&1 || git remote add thien git@github-personal:thanhthien0706/vinagroup.git
git fetch thien master

# Keep our deploy config, replace everything else with thien/master:v2
keep=$(mktemp -d)
cp html/wrangler.jsonc html/.assetsignore "$keep"/ 2>/dev/null || true
git rm -r -q --cached html 2>/dev/null || true
rm -rf html && mkdir html
git archive thien/master v2 | tar -x --strip-components=1 -C html
cp "$keep"/wrangler.jsonc "$keep"/.assetsignore html/ 2>/dev/null || true
rm -rf "$keep"

# Re-apply SEO tags + regenerate robots.txt, sitemap.xml, 404.html
python3 scripts/seo/apply-seo.py

git add -A html
if git diff --cached --quiet; then
  echo "html/ already up to date with thien/master:v2"
  exit 0
fi
git commit -m "Sync html from thien/master:v2 ($(git rev-parse --short thien/master))"
git push origin master
