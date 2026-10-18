#!/usr/bin/env bash
# Sync html/ from the "thien" remote (thien/master:v2), then commit + push to origin.
# Usage: bash scripts/sync-from-thien.sh
# SEO data per page: scripts/seo/pages.json (new pages from thien need an entry there).
# CMS parts of html/ (see GAS.md mục VIII) are kept, then scripts/build.py re-applies SEO,
# rebuilds Tin tức pages and re-patches the Liên hệ form.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree not clean - commit or stash first." >&2
  exit 1
fi

# The CMS commits straight to origin (data/, html/uploads/) - pull first or the push is rejected.
git pull --rebase origin master

git remote get-url thien >/dev/null 2>&1 || git remote add thien git@github-personal:thanhthien0706/vinagroup.git
git fetch thien master

# Paths in html/ that belong to this repo (not to thien) - kept across the sync.
KEEP=(wrangler.jsonc .assetsignore _headers admin cms vendor uploads)

keep=$(mktemp -d)
for p in "${KEEP[@]}"; do
  [ -e "html/$p" ] && cp -R "html/$p" "$keep/"
done
git rm -r -q --cached html 2>/dev/null || true
rm -rf html && mkdir html
git archive thien/master v2 | tar -x --strip-components=1 -C html
for p in "${KEEP[@]}"; do
  [ -e "$keep/$p" ] && cp -R "$keep/$p" html/
done
rm -rf "$keep"

python3 scripts/build.py

git add -A html
if git diff --cached --quiet; then
  echo "html/ already up to date with thien/master:v2"
  exit 0
fi
git commit -m "Sync html from thien/master:v2 ($(git rev-parse --short thien/master))"
git push origin master
