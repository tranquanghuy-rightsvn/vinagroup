#!/usr/bin/env python3
"""Build phần động của site từ data/ (CMS ghi qua GitHub Contents API) - xem GAS.md mục VIII.

  1. scripts/seo/apply-seo.py  : SEO trang tĩnh, robots.txt, sitemap.xml (gồm bài viết), 404.
  2. html/tin-tuc/<slug>/      : trang chi tiết mỗi bài, dựng từ CHÍNH html/tin-tuc/index.html
                                 (header/footer luôn khớp giao diện mới nhất của repo thien).
  3. html/tin-tuc/index.html   : vá vùng thẻ tin (bài CMS mới nhất trước, rồi thẻ legacy).
  4. html/lien-he/index.html   : vá form Liên hệ gửi về CMS thay cho mailto: (GAS.md mục V).
  5. Xoá html/tin-tuc/<slug>/ mồ côi (bài đã xoá khỏi CMS).

Idempotent - chạy lại nhiều lần không sinh thêm diff. Chỉ dùng Python stdlib.
Usage: python3 scripts/build.py
"""
import html
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # import apply-seo.py không để lại __pycache__

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "html"
DATA = ROOT / "data"

# PHẢI KHỚP y hệt POST_CATEGORIES trong gas/Code.js (GAS.md mục II.1).
POST_CATEGORIES = ["Kiến thức đầu tư", "Thị trường", "Tin Vina Group"]

UPLOAD_PREFIX = "/uploads/tin-tuc/"
POSTS_BEGIN, POSTS_END = "<!--cms:posts-begin-->", "<!--cms:posts-end-->"
CONTACT_MARKER = 'data-cms="contact"'


def load_seo():
    spec = importlib.util.spec_from_file_location("apply_seo", ROOT / "scripts" / "seo" / "apply-seo.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SEO = load_seo()
MARKER = SEO.GENERATED_MARKER


def esc(s):
    return html.escape(str(s or ""), quote=True)


def date_vn(iso):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(iso or ""))
    return f"{m[3]}/{m[2]}/{m[1]}" if m else ""


def load_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


# ---------------------------------------------------------------- thẻ tin (dùng chung)

def card_html(title, description, image, href=None, category=None, date=None):
    """Đúng markup thẻ tin của trang /tin-tuc/ (repo thien) - chỉ bọc thêm <a> cho bài CMS."""
    meta = " · ".join(x for x in (category, date_vn(date)) if x)
    inner = (
        '<div class="card rounded-10 h-100" tabindex="-1">\n'
        f'               <div class="card-header text-center p-0 "><img loading="lazy" class="rounded-top-10 img-fluid card-img card-img-top large-image" src="{esc(image)}" alt="{esc(title)}"></div>\n'
        '               <div class="card-body p-6">\n'
        + (f'                  <p class="vg-card-meta">{esc(meta)}</p>\n' if meta else "")
        + f'                  <h4 class="card-title uob-h4 mb-3 text-bright-blue">{esc(title)}</h4>\n'
        f'                  <p class="card-text paragraph">{esc(description)}</p>\n'
        "               </div>\n"
        "            </div>"
    )
    if href:
        inner = f'<a class="vg-card-link" href="{esc(href)}">{inner}</a>'
    return (
        f'         <div class="dtm-tile card-col col-12 col-md-4 mb-sm-5 mb-6" tile_name="{esc(title.lower())}">\n'
        f"            {inner}\n"
        "         </div>\n"
    )


def post_card(p):
    return card_html(p["title"], p.get("description"), UPLOAD_PREFIX + p["cover"],
                     href=f"/tin-tuc/{p['slug']}/", category=p.get("category"), date=p.get("date"))


CARD_CSS = (
    "<style>.vg-card-link{display:block;height:100%;color:inherit;text-decoration:none}"
    ".vg-card-link:hover .card{box-shadow:0 8px 24px rgba(15,107,63,.15)}"
    ".vg-card-link:hover .card-title{text-decoration:underline}"
    ".vg-card-meta{font-size:13px;color:#0f6b3f;font-weight:600;margin:0 0 8px}</style>\n"
)


# ---------------------------------------------------------------- /tin-tuc/ (danh sách)

LIST_ROW_RE = re.compile(
    r'(<div class="container-fluid pl-0 pr-0 need-more-help bb-two-col-tile-stack">.*?<div class="row pl-0 pr-0">\n?)'
    r"(.*?)"
    r"(\s*</div>\s*</div>\s*</div><!--ls:end\[component)",
    re.S,
)


def patch_news_list(posts, legacy):
    path = SITE / "tin-tuc" / "index.html"
    src = path.read_text(encoding="utf-8")
    block = POSTS_BEGIN + "\n" + CARD_CSS + "".join(post_card(p) for p in posts) + "".join(
        card_html(x["title"], x.get("description"), x["image"]) for x in legacy
    ) + "         " + POSTS_END
    if POSTS_BEGIN in src:
        src = re.sub(re.escape(POSTS_BEGIN) + ".*?" + re.escape(POSTS_END), lambda _: block, src, count=1, flags=re.S)
    else:
        src, n = LIST_ROW_RE.subn(lambda m: m[1] + block + m[3], src, count=1)
        if not n:
            sys.exit("ERROR: không tìm thấy vùng thẻ tin trong html/tin-tuc/index.html (repo thien đổi markup?)")
    path.write_text(src, encoding="utf-8")


# ---------------------------------------------------------------- /tin-tuc/<slug>/ (chi tiết)

ARTICLE_CSS = """<style>
.vg-article{max-width:820px;margin:0 auto;padding:40px 16px 24px;color:#1c1c1c}
.vg-article-meta{font-size:14px;color:#0f6b3f;font-weight:600;margin:0 0 10px}
.vg-article-meta a{color:#0f6b3f}
.vg-article h1{margin:0 0 14px;line-height:1.3}
.vg-article-lead{font-size:18px;line-height:1.6;color:#4b5563;margin:0 0 24px}
.vg-article-cover{width:100%;height:auto;border-radius:10px;margin:0 0 28px;display:block}
.vg-article-body{font-size:17px;line-height:1.75}
.vg-article-body h2{font-size:26px;margin:36px 0 14px;color:#0f6b3f;font-family:"Noto Sans Bold",sans-serif}
.vg-article-body h3{font-size:21px;margin:28px 0 12px;font-family:"Noto Sans Bold",sans-serif}
.vg-article-body h4{font-size:18px;margin:24px 0 10px;font-family:"Noto Sans Bold",sans-serif}
.vg-article-body p{margin:0 0 16px}
.vg-article-body ul,.vg-article-body ol{margin:0 0 16px;padding-left:24px}
.vg-article-body li{margin:0 0 6px}
.vg-article-body a{color:#0f6b3f;text-decoration:underline}
.vg-article-body figure{margin:28px 0;text-align:center}
.vg-article-body img{max-width:100%;height:auto;border-radius:8px}
.vg-article-body figcaption{font-size:14px;color:#6b7280;font-style:italic;margin-top:8px}
.vg-article-body table{width:100%;border-collapse:collapse;margin:0 0 20px;font-size:15px}
.vg-article-body th,.vg-article-body td{border:1px solid #dfe5e1;padding:8px 10px;text-align:left}
.vg-article-body th{background:#f4f8f5}
.vg-article-body blockquote{margin:0 0 16px;padding:12px 18px;border-left:4px solid #0f6b3f;background:#f4f8f5}
.vg-article-back{margin-top:32px}
.vg-related{max-width:1180px;margin:0 auto;padding:16px 16px 40px}
.vg-related h2{text-align:center;margin:0 0 28px}
</style>
"""

COMPONENT_RE = re.compile(
    r'<div class="container-fluid pl-0 pr-0 need-more-help bb-two-col-tile-stack">.*?(?=<!--ls:end\[component)',
    re.S,
)
BREADCRUMB_RE = re.compile(r'(<div class="row ml-0 mr-0 breadscrum">).*?(</div>)', re.S)


def article_html(detail, related):
    category = detail.get("category")
    meta = [f'<a href="/tin-tuc/">Tin Tức</a>']
    if category:
        meta.append(esc(category))
    meta.append(f'<time datetime="{esc(detail["date"])}">{date_vn(detail["date"])}</time>')
    body = re.sub(r"<img(?![^>]*\bloading=)", '<img loading="lazy"', detail.get("content_html") or "")
    out = (
        '<div class="container-fluid pl-0 pr-0">\n' + ARTICLE_CSS + CARD_CSS +
        '<article class="vg-article">\n'
        f'   <p class="vg-article-meta">{" · ".join(meta)}</p>\n'
        f'   <h1 class="uob-h2">{esc(detail["title"])}</h1>\n'
        + (f'   <p class="vg-article-lead">{esc(detail["description"])}</p>\n' if detail.get("description") else "")
        + f'   <img class="vg-article-cover" src="{UPLOAD_PREFIX}{esc(detail["cover"])}" alt="{esc(detail.get("cover_alt") or detail["title"])}">\n'
        f'   <div class="vg-article-body">\n{body}\n   </div>\n'
        '   <p class="vg-article-back"><a class="btn-default-secondary" href="/tin-tuc/">&larr; Xem tất cả tin tức</a></p>\n'
        "</article>\n"
    )
    if related:
        out += (
            '<section class="vg-related">\n   <h2 class="uob-h2">Bài Viết Khác</h2>\n'
            '   <div class="row pl-0 pr-0">\n' + "".join(post_card(p) for p in related) + "   </div>\n</section>\n"
        )
    return out + "</div>"


def article_seo_block(d):
    url = SEO.abs_url(f"tin-tuc/{d['slug']}/")
    img = SEO.abs_url(UPLOAD_PREFIX + d["cover"])
    title = d.get("seo_title") or d["title"] + " | Vina Group"
    desc = d.get("description") or d["title"]
    a = lambda s: html.escape(str(s), quote=True)
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": url + "#article",
                "headline": d["title"],
                "description": desc,
                "image": [img],
                "datePublished": d["date"],
                "dateModified": str(d.get("updated_at") or d["date"]),
                "inLanguage": "vi-VN",
                "articleSection": d.get("category") or "Tin tức",
                "mainEntityOfPage": url,
                "author": {"@id": SEO.BASE_URL + "#organization"},
                "publisher": {
                    "@type": "Organization",
                    "@id": SEO.BASE_URL + "#organization",
                    "name": SEO.ORG_NAME,
                    "url": SEO.BASE_URL,
                    "logo": {"@type": "ImageObject", "url": SEO.abs_url(SEO.LOGO)},
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Trang Chủ", "item": SEO.BASE_URL},
                    {"@type": "ListItem", "position": 2, "name": "Tin Tức", "item": SEO.abs_url("tin-tuc/")},
                    {"@type": "ListItem", "position": 3, "name": d["title"], "item": url},
                ],
            },
        ],
    }
    ld = json.dumps(graph, ensure_ascii=False, indent=2).replace("</", "<\\/")
    tags = [
        f"<title>{html.escape(title, quote=False)}</title>",
        f'<meta name="description" content="{a(desc)}">',
        f'<meta name="robots" content="{SEO.ROBOTS}">',
        f'<link rel="canonical" href="{url}">',
        f'<link rel="alternate" hreflang="vi" href="{url}">',
        f'<link rel="alternate" hreflang="x-default" href="{url}">',
        '<meta property="og:type" content="article">',
        f'<meta property="og:site_name" content="{SEO.SITE_NAME}">',
        '<meta property="og:locale" content="vi_VN">',
        f'<meta property="og:title" content="{a(title)}">',
        f'<meta property="og:description" content="{a(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{img}">',
        f'<meta property="og:image:alt" content="{a(d.get("cover_alt") or d["title"])}">',
        f'<meta property="article:published_time" content="{a(d["date"])}">',
        f'<meta property="article:modified_time" content="{a(d.get("updated_at") or d["date"])}">',
        f'<meta property="article:section" content="{a(d.get("category") or "Tin tức")}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{a(title)}">',
        f'<meta name="twitter:description" content="{a(desc)}">',
        f'<meta name="twitter:image" content="{img}">',
        f'<script type="application/ld+json">\n{ld}\n</script>',
    ]
    return "<!--seo:begin-->\n" + MARKER + "\n" + "\n".join(tags) + "\n<!--seo:end-->\n"


def article_template():
    """Trang /tin-tuc/ (đã qua apply-seo) -> khung trang chi tiết: mọi đường dẫn tương đối quy
    về tuyệt đối theo domain (trang chi tiết sâu hơn 1 cấp)."""
    src = (SITE / "tin-tuc" / "index.html").read_text(encoding="utf-8")
    if POSTS_BEGIN in src:  # bỏ khối thẻ đã vá để regex COMPONENT_RE không phụ thuộc nội dung đó
        src = re.sub(re.escape(POSTS_BEGIN) + ".*?" + re.escape(POSTS_END), "", src, flags=re.S)
    src = re.sub(r"""(["'(])\.\./""", r"\1/", src)
    src = src.replace('href="./"', 'href="/tin-tuc/"')
    if "<!--seo:begin-->" not in src or not COMPONENT_RE.search(src) or not BREADCRUMB_RE.search(src):
        sys.exit("ERROR: html/tin-tuc/index.html không còn đúng cấu trúc mong đợi (repo thien đổi markup?)")
    return src


def render_article(tpl, detail, related):
    out = re.sub(r"<!--seo:begin-->.*?<!--seo:end-->\n", lambda _: article_seo_block(detail), tpl, count=1, flags=re.S)
    out = BREADCRUMB_RE.sub(
        lambda m: m[1] + f'<a href="/">Trang Chủ</a><a href="/tin-tuc/">Tin Tức</a><a class="last">{esc(detail["title"])}</a>' + m[2],
        out, count=1)
    out = COMPONENT_RE.sub(lambda _: article_html(detail, related), out, count=1)
    return out


# ---------------------------------------------------------------- /lien-he/ (form)

def patch_contact_form():
    path = SITE / "lien-he" / "index.html"
    src = path.read_text(encoding="utf-8")
    if CONTACT_MARKER in src:
        return
    src, n1 = re.subn(r'<form id="vgContactForm"[^>]*>', f'<form id="vgContactForm" action="#" {CONTACT_MARKER}>', src, count=1)
    honeypot = ('<div aria-hidden="true" style="position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden">'
                '<label for="vgHp">Không điền ô này</label><input type="text" id="vgHp" name="_hp" tabindex="-1" autocomplete="off"></div>\n            ')
    src, n2 = re.subn(r'(<button type="submit" class="vg-btn-submit">)', lambda m: honeypot + m[1], src, count=1)
    src, n3 = re.subn(
        r'<p class="vg-form-note">.*?</p>',
        '<p class="vg-form-note" id="vgFormStatus" role="status" aria-live="polite">Chúng tôi sẽ phản hồi qua email trong thời gian sớm nhất.</p>',
        src, count=1, flags=re.S)
    src, n4 = re.subn(r"</body>", '<script src="/cms/contact.js" defer></script>\n</body>', src, count=1)
    if not (n1 and n2 and n3 and n4):
        sys.exit(f"ERROR: không vá được form Liên hệ (form={n1}, honeypot={n2}, note={n3}, script={n4})")
    path.write_text(src, encoding="utf-8")


# ---------------------------------------------------------------- main

def main():
    posts = load_json(DATA / "posts.json", [])
    legacy = load_json(DATA / "legacy-posts.json", [])
    posts.sort(key=lambda p: (str(p.get("date", "")), str(p.get("updated_at", ""))), reverse=True)
    for p in posts:
        if p.get("category") and p["category"] not in POST_CATEGORIES:
            print(f"WARN: bài {p['slug']} có danh mục lạ: {p['category']}", file=sys.stderr)

    SEO.main()  # trang tĩnh trước: khung bài viết lấy từ /tin-tuc/ đã chuẩn hoá SEO
    tpl = article_template()

    news_dir = SITE / "tin-tuc"
    valid = set()
    for p in posts:
        detail = load_json(DATA / "tin-tuc" / f"{p['slug']}.json", None)
        if not detail:
            print(f"WARN: thiếu data/tin-tuc/{p['slug']}.json - bỏ qua", file=sys.stderr)
            continue
        related = [x for x in posts if x["slug"] != p["slug"]][:3]
        out = news_dir / p["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_article(tpl, detail, related), encoding="utf-8")
        valid.add(p["slug"])

    # Bài đã xoá khỏi CMS: xoá thư mục đã build (chỉ thư mục do build tạo - có MARKER).
    for d in news_dir.iterdir():
        page = d / "index.html"
        if d.is_dir() and d.name not in valid and page.is_file() and MARKER in page.read_text(encoding="utf-8"):
            shutil.rmtree(d)
            print(f"removed orphan html/tin-tuc/{d.name}/")

    patch_news_list([p for p in posts if p["slug"] in valid], legacy)
    patch_contact_form()
    print(f"build: {len(valid)} bài viết, {len(legacy)} thẻ legacy, form liên hệ OK")


if __name__ == "__main__":
    main()
