#!/usr/bin/env python3
"""Inject SEO tags (title, meta, canonical, Open Graph, Twitter, JSON-LD) into every
page of html/ and generate html/robots.txt + html/sitemap.xml.

Idempotent: old/broken SEO tags are stripped and a managed <!--seo:begin-->…<!--seo:end-->
block is (re)written, so it is safe to run again after each sync from thien/master:v2.

Usage: python3 scripts/seo/apply-seo.py
Per-page title/description live in scripts/seo/pages.json.
"""
import datetime
import html
import json
import re
import sys
from pathlib import Path

BASE_URL = "https://vina-group.com.vn/"
SITE_NAME = "Vina Group"
ORG_NAME = "CÔNG TY CỔ PHẦN TẬP ĐOÀN VINA GROUP"
LOGO = "assets/iwov-resources/assets/logos/vina-logo.webp"
EMAIL = "tapdoanvinagroup@gmail.com"
PHONE = "+84772916169"
ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "Tầng 27, Tháp A2, Tòa nhà Viettel, 285 Cách Mạng Tháng 8, phường Hòa Hưng",
    "addressLocality": "Thành phố Hồ Chí Minh",
    "addressCountry": "VN",
}
ROBOTS = "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
PAGE_TYPES = {
    "lien-he/": "ContactPage",
    "gioi-thieu/": "AboutPage",
    "gioi-thieu/gioi-thieu-cong-ty/": "AboutPage",
    "tin-tuc/": "CollectionPage",
}

GENERATED_MARKER = "<!--cms:generated-->"

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "html"
PAGES = json.loads((Path(__file__).parent / "pages.json").read_text(encoding="utf-8"))

STRIP_PATTERNS = [
    r"<!--seo:begin-->.*?<!--seo:end-->\n?",
    r"<title>.*?</title>\n?",
    r"<meta\s+name=\"(?:description|keywords|robots|pagetitle)\"[^>]*>\n?",
    r"<meta\s+(?:name|property)=\"(?:og|twitter):[^\"]*\"[^>]*>\n?",
    r"<link\s+rel=\"(?:canonical|alternate)\"[^>]*>\n?",
    r"<script\s+type=\"application/ld\+json\">.*?</script>\n?",
]


def abs_url(path):
    return BASE_URL + path.lstrip("/")


def find_og_image(head):
    """Reuse the page's own banner image from its old og:image (whose URL was broken)."""
    m = re.search(r'property="og:image"\s+content="([^"]+)"', head)
    if m:
        url = m.group(1)
        rel = url[len(BASE_URL):] if url.startswith(BASE_URL) else url.split("/images/", 1)[-1]
        for candidate in (rel, "assets/" + rel, "assets/web-resources/images/" + rel):
            if (SITE / candidate).is_file():
                return candidate
    return LOGO


def breadcrumb(path):
    items = [("Trang Chủ", "")]
    parts = path.strip("/").split("/")
    for i in range(1, len(parts) + 1):
        p = "/".join(parts[:i]) + "/"
        if p in PAGES:
            items.append((PAGES[p]["name"], p))
    return {
        "@type": "BreadcrumbList",
        "@id": abs_url(path) + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": n, "name": name, "item": abs_url(p)}
            for n, (name, p) in enumerate(items, 1)
        ],
    }


def json_ld(path, page, image):
    url = abs_url(path)
    org = {
        "@type": ["Organization", "FinancialService"],
        "@id": BASE_URL + "#organization",
        "name": ORG_NAME,
        "alternateName": SITE_NAME,
        "url": BASE_URL,
        "logo": {"@type": "ImageObject", "url": abs_url(LOGO)},
        "image": abs_url(LOGO),
        "email": EMAIL,
        "telephone": PHONE,
        "address": ADDRESS,
        "areaServed": "VN",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "email": EMAIL,
            "contactType": "customer service",
            "areaServed": "VN",
            "availableLanguage": ["vi"],
        },
    }
    website = {
        "@type": "WebSite",
        "@id": BASE_URL + "#website",
        "url": BASE_URL,
        "name": SITE_NAME,
        "alternateName": ORG_NAME,
        "inLanguage": "vi-VN",
        "publisher": {"@id": BASE_URL + "#organization"},
    }
    webpage = {
        "@type": PAGE_TYPES.get(path, "WebPage"),
        "@id": url + "#webpage",
        "url": url,
        "name": page["title"],
        "description": page["description"],
        "inLanguage": "vi-VN",
        "isPartOf": {"@id": BASE_URL + "#website"},
        "about": {"@id": BASE_URL + "#organization"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": abs_url(image)},
    }
    graph = [org, website, webpage]
    if path:
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append(breadcrumb(path))
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return data.replace("</", "<\\/")


def seo_block(path, page, image):
    a = lambda s: html.escape(s, quote=True)
    url, img = abs_url(path), abs_url(image)
    tags = [
        f"<title>{html.escape(page['title'], quote=False)}</title>",
        f'<meta name="description" content="{a(page["description"])}">',
        f'<meta name="robots" content="{ROBOTS}">',
        f'<link rel="canonical" href="{url}">',
        f'<link rel="alternate" hreflang="vi" href="{url}">',
        f'<link rel="alternate" hreflang="x-default" href="{url}">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:locale" content="vi_VN">',
        f'<meta property="og:title" content="{a(page["title"])}">',
        f'<meta property="og:description" content="{a(page["description"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{img}">',
        f'<meta property="og:image:alt" content="{a(page["name"])} – {SITE_NAME}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{a(page["title"])}">',
        f'<meta name="twitter:description" content="{a(page["description"])}">',
        f'<meta name="twitter:image" content="{img}">',
        f'<script type="application/ld+json">\n{json_ld(path, page, image)}\n</script>',
    ]
    return "<!--seo:begin-->\n" + "\n".join(tags) + "\n<!--seo:end-->\n"


def process(path, page):
    file = SITE / path / "index.html"
    src = file.read_text(encoding="utf-8")
    head_end = src.lower().index("</head>")
    head, rest = src[:head_end], src[head_end:]
    image = page.get("image") or find_og_image(head)
    for pat in STRIP_PATTERNS:
        head = re.sub(pat, "", head, flags=re.S | re.I)
    m = re.search(r"<meta[^>]+charset[^>]*>\n?", head, re.I)
    at = m.end() if m else head.lower().index("<head>") + len("<head>")
    head = head[:at] + seo_block(path, page, image) + head[at:]
    head = re.sub(r"<html(?![^>]*\blang=)", '<html lang="vi"', head, count=1, flags=re.I)
    file.write_text(head + rest, encoding="utf-8")


NOT_FOUND_TEMPLATE = "bao-mat/"  # one level deep: its "../x" links become root-absolute "/x"
NOT_FOUND_CONTENT = """<div class="container-fulid pl-0 pr-0">
   <div class="uob-accordion text-center">
      <h1 class="col-12 uob-h2 text-center content-title">404 – Không Tìm Thấy Trang</h1>
      <p>Trang bạn đang tìm có thể đã bị xóa, đổi địa chỉ hoặc tạm thời không truy cập được.</p>
      <p>Vui lòng quay lại trang chủ, xem sơ đồ trang hoặc liên hệ với chúng tôi để được hỗ trợ.</p>
      <p>
         <a class="btn-default-primary mt-3" href="/">Về Trang Chủ</a>
         <a class="btn-default-secondary mt-3" href="/so-do-trang/">Sơ Đồ Trang</a>
         <a class="btn-default-secondary mt-3" href="/lien-he/">Liên Hệ</a>
      </p>
   </div>
</div>"""


def build_404():
    """Cloudflare serves html/404.html (not_found_handling: 404-page) at any unknown URL,
    so every asset/link in it must be root-absolute."""
    src = (SITE / NOT_FOUND_TEMPLATE / "index.html").read_text(encoding="utf-8")
    title = "Không Tìm Thấy Trang (404) | " + SITE_NAME
    block = (
        "<!--seo:begin-->\n"
        f"<title>{title}</title>\n"
        '<meta name="description" content="Trang bạn đang tìm không tồn tại trên website Vina Group.">\n'
        '<meta name="robots" content="noindex, follow">\n'
        "<!--seo:end-->\n"
    )
    src = re.sub(r"<!--seo:begin-->.*?<!--seo:end-->\n", lambda _: block, src, flags=re.S)
    src = re.sub(
        r'(<div class="row ml-0 mr-0 breadscrum">).*?(</div>)',
        r'\1<a href="/">Trang Chủ</a><a class="last">Không Tìm Thấy Trang</a>\2',
        src, count=1, flags=re.S,
    )
    # Replace the page body (accordion component after the banner) with the 404 message
    src, n = re.subn(
        r'(<!--ls:begin\[component-\d+\]--><style>[^<]*</style>)<div class="container-fulid pl-0 pr-0">\s*<div class="uob-accordion">.*?(?=<!--ls:end\[component)',
        lambda m: m.group(1) + NOT_FOUND_CONTENT,
        src, count=1, flags=re.S,
    )
    if not n:
        print(f"WARN: 404 template {NOT_FOUND_TEMPLATE} changed; 404.html body not replaced", file=sys.stderr)
    src = re.sub(r"""(["'(])\.\./""", r"\1/", src)
    src = src.replace('href="./"', 'href="/"')
    (SITE / "404.html").write_text(src, encoding="utf-8")


def main():
    found = set()
    for f in SITE.rglob("index.html"):
        rel = f.parent.relative_to(SITE)
        if rel.parts[:1] in (("assets",), ("docs",), ("admin",), ("vendor",)):
            continue
        # Trang bài viết do scripts/build.py sinh ra tự mang SEO riêng (Article) - không đụng.
        if GENERATED_MARKER in f.read_text(encoding="utf-8"):
            continue
        found.add("" if rel == Path(".") else rel.as_posix() + "/")
    missing = sorted(found - PAGES.keys())
    gone = sorted(PAGES.keys() - found)
    if missing:
        print("WARN: pages without SEO data in pages.json (skipped):", *missing, sep="\n  ", file=sys.stderr)
    if gone:
        print("WARN: pages.json entries without a page (skipped):", *gone, sep="\n  ", file=sys.stderr)

    pages = [p for p in PAGES if p in found]
    for path in pages:
        process(path, PAGES[path])
    build_404()

    today = datetime.date.today().isoformat()
    entries = [
        (abs_url(p), today, PAGES[p].get("changefreq", "monthly"),
         PAGES[p].get("priority", "0.8" if p.count("/") == 1 else "0.6"))
        for p in pages
    ]
    # Bài viết CMS (data/posts.json) - trang chi tiết do scripts/build.py sinh ra.
    posts_file = ROOT / "data" / "posts.json"
    if posts_file.is_file():
        for post in json.loads(posts_file.read_text(encoding="utf-8")):
            lastmod = str(post.get("updated_at") or post.get("date") or today)[:10]
            entries.append((abs_url(f"tin-tuc/{post['slug']}/"), lastmod, "monthly", "0.6"))
    urls = "".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n"
        for loc, lastmod, freq, prio in entries
    )
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
        encoding="utf-8",
    )
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /docs/\n\n" f"Sitemap: {abs_url('sitemap.xml')}\n",
        encoding="utf-8",
    )
    print(f"SEO applied to {len(pages)} pages; wrote html/sitemap.xml, html/robots.txt, html/404.html")


if __name__ == "__main__":
    main()
