# Báo cáo clone — vina-group.com.vn (5 trang)

Cập nhật: 2026-10-08 · Ngưỡng nghiệm thu: **≥90% mỗi section** (theo yêu cầu cuối của đại ca).

## 1. Danh sách trang

| Trang gốc | Bản clone | Ghi chú |
|---|---|---|
| `/` | `index.html` | |
| `/gii-thiu-cng-ty` (slug sai chính tả) | `gioi-thieu-cong-ty/index.html` | Đã sửa slug; `gii-thiu-cng-ty/index.html` chuyển hướng sang trang mới |
| `/linh-vuc-dau-tu` | `linh-vuc-dau-tu/index.html` | |
| `/quan-he-co-ong` (slug sai chính tả) | `quan-he-co-dong/index.html` | Đã sửa slug; `quan-he-co-ong/index.html` chuyển hướng sang trang mới |
| `/lien-he` | `lien-he/index.html` | |

**Kiểm tra URL bị thiếu:** site gốc chỉ có 5 URL, nên không có URL nào bị bỏ qua hay bị thiếu. Đã đối chiếu bằng 3 cách:
- `sitemap.xml` của site gốc liệt kê đúng 5 URL.
- Crawl đệ quy trên DOM đã render chỉ tìm thấy 5 trang.
- Thử 17 đường dẫn phổ biến (privacy, tin-tuc, blog, tuyen-dung, robots.txt…) đều trả 404.

## 2. File đã tạo

| Loại | File |
|---|---|
| HTML | 5 trang + 2 trang chuyển hướng (`gii-thiu-cng-ty/`, `quan-he-co-ong/`) |
| CSS dùng chung | `css/main.css`: reset, biến màu, nút, header/menu, hero, card dịch vụ, footer |
| CSS riêng | `css/home.css`, `css/gioi-thieu-cong-ty.css`, `css/linh-vuc-dau-tu.css`, `css/quan-he-co-dong.css`, `css/lien-he.css` |
| JS | `js/main.js`: header sticky, menu mobile, đếm số, form liên hệ + câu hỏi chống spam |
| SEO | `sitemap.xml`, `robots.txt`, `images/og-image.jpg` (1200×630), `images/favicon-32.png`, `images/apple-touch-icon.png` |
| Ảnh | hero-bg, page-hero-bg, contact-hero-bg, about-chart, vision, mission, shareholder-notice, shareholder-goals, logo |
| Font | Merriweather + Open Sans (bản variable, các subset vietnamese / latin-ext / latin) |

Không dùng framework. Không còn URL nào trỏ về domain gốc, không có ảnh lỗi, không có asset thừa.

## 3. Đồng bộ menu & footer
- Bản gốc mỗi trang có header một kiểu: trang Lĩnh vực đầu tư và Quan hệ cổ đông xếp logo/tiêu đề ở giữa, logo trang Quan hệ cổ đông bị kẹt ở góc, menu trang Giới thiệu và Liên hệ bị đẩy xuống thấp. Trang Lĩnh vực đầu tư và Liên hệ **không có footer**.
- Bản clone dùng **chung header + footer của trang chủ cho cả 5 trang**. HTML lặp lại trong từng trang, nhưng CSS/JS chỉ có một nguồn (`main.css`, `main.js`). Mục menu active được đánh dấu theo từng trang.
- Vì đồng bộ header, hero của trang con sẽ khác bản gốc. Đây là thay đổi chủ động, xem mục 4.

## 4. Pixel-diff theo section × breakpoint

| Trang | Section | 1920 | 1440 | 1366 | 768 | 375 |
|---|---|---|---|---|---|---|
| Trang chủ | header | 100.00% | 100.00% | 100.00% | 99.98% | 99.64% |
| Trang chủ | about | 99.99% | 99.98% | 99.98% | 99.53% | 99.95% |
| Trang chủ | growth | 99.96% | 99.95% | 99.94% | 99.49% | 99.89% |
| Trang chủ | services | 99.95% | 99.94% | 99.93% | 99.07% | 99.74% |
| Trang chủ | cta | 100.00% | 100.00% | 100.00% | 99.42% | 100.00% |
| Trang chủ | footer | 99.92% | 99.89% | 99.88% | 98.25% | 98.73% |
| Giới thiệu công ty | hero | 98.65% | 98.22% | 98.12% | 94.62% | **88.67%** |
| Giới thiệu công ty | vision | 100.00% | 100.00% | 100.00% | 99.27% | 100.00% |
| Giới thiệu công ty | mission | 100.00% | 100.00% | 100.00% | 99.05% | 99.97% |
| Giới thiệu công ty | footer | 99.91% | 99.88% | 99.87% | 98.88% | 98.58% |
| Lĩnh vực đầu tư | hero | 92.18% | 91.41% | 91.25% | **87.51%** | 90.10% |
| Lĩnh vực đầu tư | services | 98.47% | 97.96% | 97.85% | 99.26% | 95.39% |
| Lĩnh vực đầu tư | pricing | 99.56% | 99.45% | 99.42% | 99.98% | 100.00% |
| Quan hệ cổ đông | hero | 98.30% | 97.74% | 97.62% | **88.00%** | 90.55% |
| Quan hệ cổ đông | notice | 99.76% | 99.68% | 99.66% | 99.42% | 99.85% |
| Quan hệ cổ đông | goals | 99.73% | 99.63% | 99.61% | 96.93% | 100.00% |
| Quan hệ cổ đông | rights | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% |
| Quan hệ cổ đông | footer | 99.91% | 99.88% | 99.87% | 99.06% | 98.58% |
| Liên hệ | hero | 98.19% | 97.42% | 97.28% | **86.28%** | **84.94%** |
| Liên hệ | hours | 99.78% | 99.71% | 99.69% | 99.81% | 99.67% |
| Liên hệ | contact | 99.69% | 99.56% | 99.52% | 97.10% | 94.93% |

Các ô **in đậm** (<90%) đều là **hero của trang con ở tablet/mobile**. Nguyên nhân là header đã được đồng bộ theo yêu cầu. Ví dụ ở 375px, bản gốc trang Giới thiệu dùng logo 50px trong khi header chung dùng logo 144px; ở 768px, bản gốc trang Lĩnh vực đầu tư cao 450px còn header chung cao 491px. Phần nội dung không có section nào dưới 90%.

## 5. Kiểm tra "không vỡ giao diện" (1920 / 1366 / 768 / 375)
- [x] Không có scroll ngang (`scrollWidth` bằng viewport ở mọi trang).
- [x] Không có ảnh lỗi, không có chữ tràn. Lỗi email tràn ở footer 768px của bản gốc đã được sửa.
- [x] Menu mobile mở/đóng được trên cả 5 trang, mục active đúng trang.
- [x] Các nút có hover. Thẻ bảng giá phóng to 2.5% khi hover (giống bản gốc).
- [x] Form liên hệ hoạt động: kiểm tra trường bắt buộc, câu hỏi chống spam, mở ứng dụng mail với nội dung đã điền.

## 6. SEO đã bổ sung (bản gốc hầu như không có)
- **Meta:** title, description (viết mới cho trang Giới thiệu và Quan hệ cổ đông vì bản gốc thiếu), keywords, robots, author, theme-color, geo (VN-SG).
- **Canonical + hreflang `vi-VN` / `x-default`.** Canonical dùng domain `https://vina-group.com.vn` với **slug đã sửa**. Đổi domain ở biến `SITE_URL` trong `.work/build/build.py`.
- **Open Graph + Twitter Card** dùng ảnh OG 1200×630 mới (bản gốc không có ảnh chia sẻ).
- **JSON-LD (`@graph`):**
  - `FinancialService`: tên, logo, địa chỉ, điện thoại, email, mã số thuế, giờ làm việc T2–T6 08:00–17:00.
  - `WebSite`.
  - `WebPage` / `AboutPage` / `ContactPage` tuỳ trang.
  - `BreadcrumbList` cho trang con.
  - `OfferCatalog` ở trang Lĩnh vực đầu tư: 6 dịch vụ và 3 gói giá (10 / 20 / 30 triệu VNĐ).
- **`sitemap.xml`:** 5 URL, có lastmod và image sitemap. **`robots.txt`:** cho phép toàn site, chặn `/reports/`, khai báo sitemap.
- **Trang chuyển hướng ở slug cũ:** meta refresh + JS + canonical + `noindex`, để giữ link cũ không bị chết.
- Mỗi trang có đúng 1 thẻ `h1`. Trang chủ cũ không có h1 nội dung (chỉ có h1 bọc logo).
- Đã sửa dữ liệu sai của bản gốc: toạ độ geo trỏ tới New York kèm "Hà Nội", trong khi trụ sở ở TPHCM. Bản clone **không ghi toạ độ** để tránh dữ liệu sai, chỉ ghi khu vực VN-SG.

## 7. Ghi chú UX / giả định
- **Form liên hệ:** site tĩnh không có backend, nên khi gửi sẽ mở ứng dụng mail với tiêu đề và nội dung đã điền. Captcha ảnh của bản gốc (do server sinh ra) được thay bằng câu hỏi phép cộng, kiểm tra bằng JS và có nút đổi câu hỏi. Nếu sau này cần gửi form thật, cần thêm một dịch vụ form (ví dụ Formspree hoặc Cloudflare Worker).
- **Link nội dung:** nút "Tìm hiểu thêm" trỏ tới trang Giới thiệu, "Khám phá dịch vụ" trỏ tới trang Lĩnh vực đầu tư, các nút "Đặt ngay" trỏ tới trang Liên hệ. Ở bản gốc các nút này để `#`.
- Sticky header, đếm số, fade-in hero và bg-fixed (parallax) giữ như ở bản clone trang chủ.

## 8. Dọn `.work/` cũ
Không có thư mục `.work/` nào cũ hơn 3 ngày.

## 9. Deploy lên Cloudflare (Workers Static Assets) — cập nhật 2026-10-08
Chỉ deploy thư mục **`dist/`**, được sinh bằng lệnh `python3 .work/build/build.py`. Cấu hình nằm ở `wrangler.jsonc`. Đã chạy thử bằng `wrangler dev` 4.148.0.

| Hạng mục | Cách xử lý | Kết quả test |
|---|---|---|
| URL chuẩn `/slug/` | Link nội bộ, canonical và sitemap đều dùng `/slug/`; `html_handling: auto-trailing-slash` | Crawl chỉ gặp 5 URL chuẩn |
| Biến thể URL | `_redirects`: `/slug`, `/slug/index.html`, `/index.html` → 301 (redirect mặc định của Cloudflare là 307) | Mọi biến thể chỉ 1 bước 301 |
| Slug cũ sai chính tả | `_redirects` 301: `/gii-thiu-cng-ty*` → `/gioi-thieu-cong-ty/`, `/quan-he-co-ong*` → `/quan-he-co-dong/` | 301, 1 bước |
| 404 thật | `not_found_handling: 404-page` + `404.html` (`noindex`) | URL lạ trả 404 |
| Chống index domain phụ | `_headers`: `X-Robots-Tag: noindex` cho `*.workers.dev` | — (chỉ kiểm tra được sau khi deploy) |
| Cache | css/js có `?v=<hash>` → cache 1 năm (immutable); fonts 1 năm; ảnh 30 ngày; HTML luôn kiểm tra lại | Header đúng |
| Bảo mật | nosniff, Referrer-Policy, Permissions-Policy, X-Frame-Options | Header đúng |
| File nội bộ | `.work/`, `reports/`, `wrangler.jsonc` không nằm trong `dist/` | Đều trả 404 |
| Số liệu trang chủ | Số thật luôn có trong DOM; chỉ chạy hiệu ứng đếm sau khi người dùng cuộn | Googlebot thấy 11 / 45 / 2530 / 100 |
| Logo JSON-LD / favicon | Logo 180×180 (Google yêu cầu tối thiểu 112), `favicon.ico` 48px + PNG 96px | Trả 200 |

**Không xử lý được bằng file trong `dist/`, cần làm trên dashboard:**
- Chuyển hướng `www` → không `www`: dùng Redirect Rule.
- Chuyển `http` → `https`: bật "Always Use HTTPS".

## 10. Tối ưu ảnh (WebP) & title — cập nhật 2026-10-08
- Ảnh nội dung và ảnh nền đã đổi sang **WebP** (cwebp q80, `-sharp_yuv`). Ảnh lớn hơn nhiều so với kích thước hiển thị được thu nhỏ về rộng 960px (~2× khung lớn nhất). Ảnh gốc lưu ở `.work/original-images/`.

  | Ảnh | Trước | Sau |
  |---|---|---|
  | about-chart | PNG 1344×768, 1013 KB | WebP 960px, 44 KB |
  | shareholder-notice | JPG 1024², 321 KB | WebP 960px, 74 KB |
  | vision / mission / shareholder-goals | 133 / 43 / 34 KB | 104 / 31 / 18 KB |
  | hero-bg / page-hero-bg / contact-hero-bg | 49 / 47 / 51 KB | 34 / 29 / 47 KB |
  | logo | PNG 8 KB | WebP lossless 5 KB |

- **Giữ nguyên định dạng** cho `og-image.jpg` (tương thích tốt nhất với Facebook/Zalo), `apple-touch-icon.png` (cũng là logo trong JSON-LD), `favicon-96.png`, `favicon.ico`.
- Dung lượng tải trang chủ: **1387 KB → 399 KB**. `dist/` giảm từ 2.3 MB xuống 1.0 MB.
- Title trang chủ rút gọn từ 77 xuống 46 ký tự: **"Vinagroup - Tập đoàn đầu tư tài chính bền vững"** (áp dụng cho `<title>`, `og:title`, `twitter:title`, JSON-LD).
- Pixel-diff sau khi đổi ảnh (1440 / 375) vẫn giữ mức cũ: các section có ảnh đạt 99.6–100%, hero không đổi.
