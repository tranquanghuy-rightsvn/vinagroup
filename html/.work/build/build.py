#!/usr/bin/env python3
"""Generate the 5 static pages from shared header/footer partials.

Output is plain static HTML; this script only exists so header/footer stay identical.
Run from the site root: python3 .work/build/build.py
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BUILD = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(ROOT, ".work", "icons")

NAV = [
    ("home", "Home", "index.html"),
    ("gioi-thieu-cong-ty", "Giới thiệu công ty", "gioi-thieu-cong-ty/index.html"),
    ("linh-vuc-dau-tu", "Lĩnh vực đầu tư", "linh-vuc-dau-tu/index.html"),
    ("quan-he-co-dong", "Quan hệ cổ đông", "quan-he-co-dong/index.html"),
    ("lien-he", "Liên Hệ", "lien-he/index.html"),
]

# Production origin used for canonical / og:url / sitemap. Change here if deploying elsewhere.
SITE_URL = "https://vina-group.com.vn"
LASTMOD = "2026-10-08"
SITE_NAME = "Vinagroup - Công ty Cổ phần Tập đoàn Vina Group"
OG_IMAGE = "images/og-image.jpg"

PAGES = {
    "home": dict(
        dir="", css="home", name="Trang chủ",
        title="Vinagroup - Tập đoàn đầu tư tài chính bền vững",
        description="Đầu tư tài chính bền vững với Vinagroup - Tập đoàn hàng đầu Việt Nam, cung cấp giải pháp tối ưu hóa lợi nhuận cho bạn.",
        keywords="vinagroup, tập đoàn tài chính, đầu tư bền vững, dịch vụ tư vấn đầu tư, phân tích thị trường, quản lý tài sản, đầu tư cổ phiếu",
        hero_mod="", h2="CÔNG TY CỔ PHẦN TẬP ĐOÀN VINAGROUP", h3="Đầu tư tài chính bền vững cho tương lai của bạn",
        hero_tag="h1", page_type="WebPage", priority="1.0",
    ),
    "gioi-thieu-cong-ty": dict(
        dir="gioi-thieu-cong-ty", css="gioi-thieu-cong-ty", name="Giới thiệu công ty",
        title="Giới thiệu công ty - Vinagroup: Tập đoàn đầu tư",
        description="Giới thiệu Tập đoàn Vina Group: tầm nhìn xây dựng hệ sinh thái đầu tư minh bạch, bền vững và sứ mệnh kết nối cổ đông với cơ hội Pre-IPO chất lượng.",
        keywords="giới thiệu Vina Group, tầm nhìn, sứ mệnh, Leading Glory, đầu tư Pre-IPO, tập đoàn đầu tư",
        hero_mod=" hero--page", h2="GIỚI THIỆU VỀ CHÚNG TÔI", h3="Đem lại giá trị thực cho cổ đông và khách hàng.",
        hero_tag="h1", page_type="AboutPage", priority="0.8",
    ),
    "linh-vuc-dau-tu": dict(
        dir="linh-vuc-dau-tu", css="linh-vuc-dau-tu", name="Lĩnh vực đầu tư",
        title="Dịch Vụ Tư Vấn Đầu Tư - Vinagroup: Tập đoàn đầu tư",
        description="Khám phá dịch vụ tư vấn đầu tư chuyên nghiệp và hiệu quả, giúp bạn tối ưu hóa tài chính và đầu tư.",
        keywords="dịch vụ, tư vấn đầu tư, quản lý tài sản, cổ phiếu, giao dịch tài chính, phân tích thị trường",
        hero_mod=" hero--page", h2="LĨNH VỰC ĐẦU TƯ", h3="Đem lại giá trị thực cho cổ đông và khách hàng.",
        hero_tag="h1", page_type="WebPage", priority="0.8",
    ),
    "quan-he-co-dong": dict(
        dir="quan-he-co-dong", css="quan-he-co-dong", name="Quan hệ cổ đông",
        title="Quan hệ cổ đông - Vinagroup: Tập đoàn đầu tư",
        description="Thông báo đến cổ đông, mục tiêu và quyền lợi cổ đông của Tập đoàn Vina Group: báo cáo định kỳ, Đại hội đồng cổ đông, chi trả cổ tức và tiến độ dự án Pre-IPO.",
        keywords="quan hệ cổ đông, Vina Group, đại hội đồng cổ đông, cổ tức, báo cáo tài chính, Pre-IPO",
        hero_mod=" hero--page", h2="QUAN HỆ CỔ ĐÔNG", h3="",
        hero_tag="h1", page_type="WebPage", priority="0.8",
    ),
    "lien-he": dict(
        dir="lien-he", css="lien-he", name="Liên hệ",
        title="Liên Hệ Vina Group - Vinagroup: Tập đoàn đầu tư",
        description="Liên hệ với Tập Đoàn Vina Group để nhận hỗ trợ tài chính và giải đáp thắc mắc nhanh chóng!",
        keywords="Liên Hệ, Hỗ trợ, Tài chính, Vina Group, Thông tin liên hệ, Gửi thông tin",
        hero_mod=" hero--page hero--contact", h2="Liên Hệ Chúng Tôi", h3="",
        hero_tag="h1", page_type="ContactPage", priority="0.7",
    ),
}

# Old (misspelled) slugs from the original site -> new slugs. Static redirect pages keep old links alive.
REDIRECTS = {"gii-thiu-cng-ty": "gioi-thieu-cong-ty", "quan-he-co-ong": "quan-he-co-dong"}

ORG_ID = SITE_URL + "/#organization"
WEBSITE_ID = SITE_URL + "/#website"


def page_url(p):
    return SITE_URL + "/" + (p["dir"] + "/" if p["dir"] else "")


def jsonld(key, p):
    import json
    url = page_url(p)
    org = {
        "@type": "FinancialService",
        "@id": ORG_ID,
        "name": "Công ty Cổ phần Tập đoàn Vina Group",
        "alternateName": ["Vinagroup", "Vina Group", "Tập đoàn Vina Group"],
        "url": SITE_URL + "/",
        "logo": {"@type": "ImageObject", "url": SITE_URL + "/images/apple-touch-icon.png", "width": 180, "height": 180},
        "image": SITE_URL + "/" + OG_IMAGE,
        "description": PAGES["home"]["description"],
        "slogan": "Leading Glory",
        "email": "tapdoanvinagroup@gmail.com",
        "telephone": "+84772916169",
        "taxID": "0317904928",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Tầng 27, Tháp A2, Tòa nhà Viettel, 285 Cách mạng tháng 8",
            "addressLocality": "Phường Hòa Hưng",
            "addressRegion": "Thành phố Hồ Chí Minh",
            "addressCountry": "VN",
        },
        "areaServed": {"@type": "Country", "name": "Việt Nam"},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "08:00", "closes": "17:00",
        }],
        "contactPoint": [{
            "@type": "ContactPoint", "contactType": "customer service",
            "telephone": "+84772916169", "email": "tapdoanvinagroup@gmail.com",
            "areaServed": "VN", "availableLanguage": ["vi"],
        }],
    }
    website = {
        "@type": "WebSite", "@id": WEBSITE_ID, "url": SITE_URL + "/", "name": SITE_NAME,
        "inLanguage": "vi-VN", "publisher": {"@id": ORG_ID},
    }
    webpage = {
        "@type": p["page_type"], "@id": url + "#webpage", "url": url, "name": p["title"],
        "description": p["description"], "inLanguage": "vi-VN",
        "isPartOf": {"@id": WEBSITE_ID}, "about": {"@id": ORG_ID},
        "primaryImageOfPage": {"@type": "ImageObject", "url": SITE_URL + "/" + OG_IMAGE, "width": 1200, "height": 630},
        "dateModified": LASTMOD,
    }
    graph = [org, website, webpage]
    if p["dir"]:
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({
            "@type": "BreadcrumbList", "@id": url + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": p["name"], "item": url},
            ],
        })
    if key == "linh-vuc-dau-tu":
        services = ["Đầu tư tự doanh", "Tư vấn quản lý doanh nghiệp", "Tự doanh cổ phiếu",
                    "Tự doanh trái phiếu", "Tự doanh phái sinh", "Nghiên cứu & Phân tích thị trường"]
        packages = [("Gói tư vấn doanh nghiệp Cơ Bản", "10000000"),
                    ("Gói tư vấn doanh nghiệp Nâng Cao", "20000000"),
                    ("Gói tư vấn doanh nghiệp Đặc Biệt", "30000000")]
        org["hasOfferCatalog"] = {
            "@type": "OfferCatalog", "name": "Lĩnh vực đầu tư & gói dịch vụ",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "provider": {"@id": ORG_ID}}}
                for n in services
            ] + [
                {"@type": "Offer", "price": price, "priceCurrency": "VND", "url": url + "#pricing",
                 "itemOffered": {"@type": "Service", "name": n, "serviceType": "Tư vấn doanh nghiệp", "provider": {"@id": ORG_ID}}}
                for n, price in packages
            ],
        }
    data = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")


def seo_head(key, p, pre):
    url = page_url(p)
    img = SITE_URL + "/" + OG_IMAGE
    t, d = p["title"], p["description"]
    return f"""  <title>{t}</title>
  <meta name="description" content="{d}">
  <meta name="keywords" content="{p["keywords"]}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="author" content="Công ty Cổ phần Tập đoàn Vina Group">
  <meta name="theme-color" content="#26912e">
  <meta name="format-detection" content="telephone=no">
  <meta name="geo.region" content="VN-SG">
  <meta name="geo.placename" content="Thành phố Hồ Chí Minh">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="vi-VN" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <link rel="icon" href="{pre}favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="96x96" href="{pre}images/favicon-96.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{pre}images/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:locale" content="vi_VN">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:image" content="{img}">
  <meta property="og:image:secure_url" content="{img}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Công ty Cổ phần Tập đoàn Vina Group - Đầu tư tài chính bền vững">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{img}">
  <meta name="twitter:image:alt" content="Công ty Cổ phần Tập đoàn Vina Group - Đầu tư tài chính bền vững">
  <script type="application/ld+json">
{jsonld(key, p)}
  </script>"""


def icon(name):
    with open(os.path.join(ICONS, name + ".svg"), encoding="utf-8") as f:
        return f.read()


def fill_icons(html):
    return re.sub(r"\{\{([a-z0-9-]+)\}\}", lambda m: icon(m.group(1)), html)


def nav_html(active, pre):
    items = []
    for key, label, href in NAV:
        url = pre + href
        if key == active:
            items.append(f'              <li><a href="{url}" class="active" aria-current="page">{label}</a></li>')
        else:
            items.append(f'              <li><a href="{url}">{label}</a></li>')
    return "\n".join(items)


def render(key, p):
    pre = "../" if p["dir"] else ""
    home = pre + "index.html"
    main = fill_icons(open(os.path.join(BUILD, key + ".main.html"), encoding="utf-8").read())
    tag = p["hero_tag"]
    slogan = f'\n      <p class="hero-slogan">{p["h3"]}</p>' if p["h3"] else ""
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{seo_head(key, p, pre) if key != "404" else not_found_head(pre)}
  <link rel="preload" href="{pre}fonts/merriweather-vietnamese.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{pre}fonts/open-sans-vietnamese.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{pre}css/main.css">
{f'  <link rel="stylesheet" href="{pre}css/{p["css"]}.css">' if p["css"] else ""}
</head>
<body>
  <a href="#main-content" class="skip-link btn">Skip to main content</a>

  <div class="hero{p["hero_mod"]}">
    <header class="site-header">
      <div class="header-bar">
        <div class="container header-inner">
          <a href="{home}" class="logo"><img src="{pre}images/logo.webp" alt="Logo Vinagroup - Tập đoàn Vina Group" width="81" height="81"></a>
          <nav class="main-nav" id="main-nav" aria-label="Menu chính">
            <ul>
{nav_html(key, pre)}
            </ul>
          </nav>
          <div class="mobile-actions">
            <a href="tel:0772916169" class="mobile-phone" aria-label="Gọi điện">{icon("ico-phone")}</a>
            <button type="button" class="menu-toggle" aria-controls="main-nav" aria-expanded="false" aria-label="Mở menu">
              <span class="menu-toggle-lines"></span>
            </button>
          </div>
        </div>
      </div>
    </header>
    <div class="container hero-content">
      <{tag} class="hero-title">{p["h2"]}</{tag}>{slogan}
    </div>
  </div>

  <main id="main-content">
{main.rstrip()}
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col footer-col--left">
        <span class="footer-icon">{icon("fa-light-map-marker-alt")}</span>
        <h3 class="footer-title">ĐỊA CHỈ TRỤ SỞ</h3>
        <p class="footer-text footer-text--address">Tầng 27, Tháp A2, Tòa nhà Viettel, 285 Cách mạng tháng 8, phường Hòa Hưng, TPHCM</p>
      </div>
      <div class="footer-col footer-col--center">
        <span class="footer-icon">{icon("fa-light-phone")}</span>
        <h3 class="footer-title">Phone</h3>
        <p class="footer-text">Phone: <a href="tel:0772916169">077.291.6169</a></p>
      </div>
      <div class="footer-col footer-col--right">
        <span class="footer-icon">{icon("fa-light-envelope")}</span>
        <h3 class="footer-title">Contact</h3>
        <p class="footer-text"><a href="mailto:tapdoanvinagroup@gmail.com">tapdoanvinagroup@gmail.com</a><br><span class="footer-tax">Mã số thuế: 0317904928</span></p>
      </div>
    </div>
  </footer>

  <script src="{pre}js/main.js" defer></script>
</body>
</html>
"""


def not_found_head(pre):
    return f"""  <title>Không tìm thấy trang (404) - Vinagroup</title>
  <meta name="robots" content="noindex, follow">
  <meta name="theme-color" content="#26912e">
  <link rel="icon" href="{pre}favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="96x96" href="{pre}images/favicon-96.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{pre}images/apple-touch-icon.png">"""


import hashlib
import posixpath
import shutil

PAGES["404"] = dict(dir="", css="", name="404", hero_mod=" hero--page", h2="404", h3="Không tìm thấy trang", hero_tag="p")
OUTPUTS = {key: (p["dir"] + "/index.html" if p["dir"] else ("404.html" if key == "404" else "index.html")) for key, p in PAGES.items()}
DIST = os.path.join(ROOT, "dist")
STATIC_DIRS = ["css", "js", "images", "fonts"]
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|#|data:|//)")


def asset_version(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def to_dist(html, out_rel):
    """Rewrite relative URLs to root-absolute ones: /slug/ for pages, ?v=hash for css/js."""
    base = posixpath.dirname(out_rel)

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if EXTERNAL.match(url):
            return m.group(0)
        path = "/" + posixpath.normpath(posixpath.join(base, url)).lstrip("./")
        if path.endswith("/index.html"):
            path = path[: -len("index.html")]
        elif path == "/index.html":
            path = "/"
        if path.startswith(("/css/", "/js/")) and path.endswith((".css", ".js")):
            path += "?v=" + asset_version(path[1:])
        return f'{attr}="{path}"'

    return re.sub(r'\b(href|src)="([^"]+)"', fix, html)


# --- preview build (site root, relative links, works over file://)
for key, p in PAGES.items():
    out = os.path.join(ROOT, OUTPUTS[key])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(key, p))
    print("wrote", OUTPUTS[key])

urls = "\n".join(f"""  <url>
    <loc>{page_url(p)}</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{p["priority"]}</priority>
    <image:image>
      <image:loc>{SITE_URL}/{OG_IMAGE}</image:loc>
    </image:image>
  </url>""" for k, p in PAGES.items() if k != "404")
SITEMAP = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{urls}
</urlset>
"""
ROBOTS = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
# Static rules first, splat rules last (Cloudflare evaluates static rules faster)
REDIRECTS_FILE = (
    "# Old misspelled slugs from the previous site -> new slugs (permanent)\n"
    + "".join(f"/{old} /{new}/ 301\n/{old}/ /{new}/ 301\n" for old, new in REDIRECTS.items())
    + "\n# Canonical form is /slug/ — make the alternatives permanent (Cloudflare's own trailing-slash redirect is 307)\n/index.html / 301\n"
    + "".join(f"/{p['dir']} /{p['dir']}/ 301\n/{p['dir']}/index.html /{p['dir']}/ 301\n" for p in PAGES.values() if p["dir"])
    + "\n# Anything below an old slug\n"
    + "".join(f"/{old}/* /{new}/ 301\n" for old, new in REDIRECTS.items())
)
HEADERS_FILE = """# Preview/default hostnames must never be indexed (duplicate of the real domain)
https://:version.:subdomain.workers.dev/*
  X-Robots-Tag: noindex

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  X-Frame-Options: SAMEORIGIN

# css/js are referenced with ?v=<content hash>, so they can be cached for a year
/css/*
  Cache-Control: public, max-age=31536000, immutable
/js/*
  Cache-Control: public, max-age=31536000, immutable
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/images/*
  Cache-Control: public, max-age=2592000
/favicon.ico
  Cache-Control: public, max-age=2592000
"""
for name, body in [("sitemap.xml", SITEMAP), ("robots.txt", ROBOTS)]:
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(body)

# --- Cloudflare build (dist/)
if os.path.isdir(DIST):
    shutil.rmtree(DIST)
os.makedirs(DIST)
for d in STATIC_DIRS:
    shutil.copytree(os.path.join(ROOT, d), os.path.join(DIST, d))
shutil.copy(os.path.join(ROOT, "favicon.ico"), DIST)
for key, p in PAGES.items():
    out = os.path.join(DIST, OUTPUTS[key])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(os.path.join(ROOT, OUTPUTS[key]), encoding="utf-8") as f:
        html = f.read()
    with open(out, "w", encoding="utf-8") as f:
        f.write(to_dist(html, OUTPUTS[key]))
for name, body in [("sitemap.xml", SITEMAP), ("robots.txt", ROBOTS), ("_redirects", REDIRECTS_FILE), ("_headers", HEADERS_FILE)]:
    with open(os.path.join(DIST, name), "w", encoding="utf-8") as f:
        f.write(body)
print("wrote dist/ (Cloudflare Workers static assets)")
