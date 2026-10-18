# Vina Group — Static Site (v2)

Trang web tĩnh của CÔNG TY CỔ PHẦN TẬP ĐOÀN VINA GROUP (36 trang), dựng trên nền tảng
HTML/CSS/JS gốc được rebrand lại từ bản clone UOBAM ban đầu.

## Cấu trúc URL

Mỗi trang nằm trong một thư mục riêng dưới dạng `<slug>/index.html` (ví dụ:
`about-us/corporate-profile/index.html`). Toàn bộ link nội bộ dùng dạng thư mục có
dấu `/` ở cuối (ví dụ `href="about-us/corporate-profile/"`) — khi deploy qua Vercel,
URL hiển thị ra chỉ còn slug, không lộ `index.html`.

File `vercel.json` ở thư mục gốc bật `cleanUrls` để URL không cần đuôi `.html`.

## Đã kiểm tra

- 0 broken link trong hơn 5500 tham chiếu `src=`/`href=` nội bộ trên toàn bộ 36 trang.
- Không còn chuỗi `index.page.html` nào sót lại trong mã nguồn.

## Giới hạn đã biết

- 2 trang Công Bố Thông Tin và Báo Cáo Tài Chính Công Ty dùng dữ liệu tĩnh (đã bỏ
  component JS đọc CSV động của bản UOBAM gốc).
- Khi mở trực tiếp bằng `file://` (không qua HTTP server), các link dạng thư mục
  (`about-us/`) vẫn mở được bình thường trên hầu hết trình duyệt vì chúng tự tìm
  `index.html` bên trong thư mục.
