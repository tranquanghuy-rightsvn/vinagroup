# GAS.md — Quyết định nghiệp vụ CMS Vina Group (nguồn chân lý)

> Đọc TOÀN BỘ file này trước khi sửa bất kỳ file nào trong `gas/`, `scripts/build.py`,
> `html/cms/`, `html/admin/`. Theo playbook skill `free-cms-static-site-pipeline`
> (dự án mẫu: xevip). Code lệch khỏi file này = sửa code hoặc cập nhật file này trong CÙNG 1 lượt.

0. Phạm vi (ĐÚNG 3 mục, không làm rộng hơn):
   1. Tin tức (bài viết) — viết/sửa/xoá, mỗi bài có trang `/tin-tuc/<slug>/`, danh sách
      `/tin-tuc/` tự cập nhật.
   2. Form Liên hệ (`/lien-he/`) — thay `mailto:` bằng gửi thẳng về CMS: lưu lại + gửi email
      báo về `tapdoanvinagroup@gmail.com`; xem/đổi trạng thái/xoá trong Admin.
   3. Danh mục bài viết — thêm/đổi tên/xoá trong Admin (mục II-B).
   4. Người dùng — đăng nhập OTP, phân quyền root > admin > editor.
   KHÔNG quản lý: Công bố thông tin, Báo cáo tài chính, các trang tĩnh khác (sửa ở repo thien).

```
I. Đối với tính năng đăng nhập:
  1. Luồng: gửi OTP -> xác nhận -> vào trang Admin (không mật khẩu, không dựa session Google).
  2. Chỉ email đã ĐĂNG KÝ (Sheet Users) mới được gửi OTP.
  3. Account chủ của GAS (người deploy) LUÔN hợp lệ, luôn là root - KHÔNG lưu trong Users,
     KHÔNG hiện/không sửa được trong UI quản lý người dùng. requestOtp tự cho qua account này.
  4. Phân quyền: 3 cấp root > admin > editor (ROLE_RANK = {editor:1, admin:2, root:3}).
     - editor : Tin tức (thêm/sửa/xoá bài). KHÔNG thấy Liên hệ (thông tin khách hàng).
     - admin  : mọi thứ của editor + Danh mục + Liên hệ + Người dùng (thêm/sửa/xoá admin & editor).
     - root   : chủ script (ngầm định) hoặc dòng "root" sửa tay trong Sheet - toàn quyền.
     - Qua CMS chỉ gán được admin/editor; không tự sửa/xoá chính mình.
  5. OTP sống 10 phút, cooldown 60 giây/email, tối đa 5 lần nhập sai rồi phải xin mã mới.
     Token sống 30 ngày, lưu localStorage. verifyOtp gọi purgeExpiredTokens_(); Đăng xuất gọi
     logout(token) phía server rồi mới reload.
  6. Server tự requireRole_ ở MỌI hàm - ẩn nút trên UI không phải bảo mật.

II. Đối với viết bài (Tin tức):
  1. Field có ô nhập (không tự ý thêm/bớt):
     - Tiêu đề
     - Slug (tự sinh từ tiêu đề, bỏ dấu + gạch ngang; bất biến sau lần Lưu đầu - mục III)
     - Danh mục: chọn từ danh sách quản lý ở mục II-B; bài lưu SLUG danh mục (field
       "category"). Để trống được. Server chặn Lưu nếu slug không còn tồn tại.
     - Mô tả ngắn (dùng cho thẻ bài ở /tin-tuc/ + meta description)
     - Ảnh bìa (bắt buộc)
     - Ngày đăng (input date; mặc định hôm nay khi tạo, sửa được)
     - Nội dung: TinyMCE (iframe mode, tự host tại html/vendor/tinymce/), có: đoạn/tiêu đề
       H2-H4, đậm/nghiêng/gạch chân, danh sách, link, bảng, code, xoá định dạng.
       CÓ chèn ảnh giữa bài: nút "quickimage" mở thẳng file picker (không dialog Image),
       chọn nhiều ảnh, bọc <figure> + <figcaption>; alt/title = caption, rỗng thì = tiêu đề
       (đồng bộ sống); caption placeholder bị xoá lúc Lưu.
  2. Field server tự suy (không có ô nhập):
     - seo_title = "<Tiêu đề> | Vina Group"; breadcrumb = tiêu đề; cover_alt = tiêu đề.
     - cover = "<slug>-cover.jpg" (tất định theo slug, server kiểm tra file đã có trên GitHub).
     - updated_at = thời điểm Lưu (UTC).
  3. Danh sách trong Admin: đọc data/posts.json qua GitHub Contents API trong boot() (luôn mới
     nhất), cache stale-while-revalidate ở client.
  4. Ảnh: nén client (canvas) cạnh dài tối đa 1600px, JPEG 0.85, upload THẲNG lên GitHub ngay
     lúc chọn (không qua Drive), hiện ảnh tạm ngay. Ảnh RIÊNG 1-1 cho từng bài, tên tất định:
     html/uploads/tin-tuc/<slug>-cover.jpg, html/uploads/tin-tuc/<slug>-content-<N>.jpg
     (N tăng dần, không đánh số lại). Trong content_html lưu đường dẫn TUYỆT ĐỐI theo domain
     "/uploads/tin-tuc/<file>" (không phụ thuộc độ sâu trang). Trong editor hiển thị qua
     raw.githubusercontent.com.

II-B. Đối với Danh mục bài viết (quyền admin trở lên; editor chỉ chọn khi viết bài):
   - Field: Tên (bắt buộc, tối đa 60 ký tự, không trùng tên danh mục khác).
   - Mã (slug): tự sinh từ tên lúc tạo, BẤT BIẾN - bài viết tham chiếu bằng slug, nên đổi tên
     chỉ ghi lại data/categories.json (không phải ghi lại từng bài) và tự áp lên mọi bài.
   - Xoá: CHẶN nếu còn bài thuộc danh mục (server đếm trong data/posts.json; nút Xoá trên UI
     cũng disable) - không tự động gỡ danh mục khỏi bài.
   - Thứ tự hiển thị trong dropdown = thứ tự tạo. Danh sách nằm trong boot(), không tải riêng.
   - Danh mục chỉ hiển thị trên site (thẻ tin, trang bài, JSON-LD articleSection); KHÔNG có
     trang lọc theo danh mục.

III. Đối với sửa bài:
   - Slug bất biến sau lần lưu đầu: server throw nếu bài không tồn tại với slug đó; client
     disable ô slug khi sửa (và khi đã tải ảnh bìa/ảnh nội dung); mở form tạo mới thì bật lại.
   - Ảnh khi sửa hiển thị bằng URL tuyệt đối raw.githubusercontent.com/<owner>/<repo>/<branch>/.

IV. Đối với xoá bài:
   - Xoá trong 1 thao tác: data/tin-tuc/<slug>.json + ảnh bìa + mọi ảnh nội dung của bài
     (an toàn vì ảnh riêng 1-1) + gỡ khỏi data/posts.json (ghi SAU CÙNG).
   - build.py xoá thư mục html/tin-tuc/<slug>/ mồ côi (chỉ thư mục có marker
     <!--cms:generated--> trong index.html).
   - Bắt buộc confirm (Huỷ/Xoá) trước khi xoá.

V. Đối với form Liên hệ (/lien-he/):
   - Field: Họ và tên (bắt buộc), Email (bắt buộc), Chủ đề, Nội dung (bắt buộc).
   - Honeypot input ẩn tên "_hp" (ẩn bằng style inline trên chính phần tử, không phụ thuộc
     file CSS khác - gotcha #27). Có giá trị -> âm thầm trả ok, không lưu.
   - Rate-limit theo email: 20 giây/lần.
   - Lưu Sheet Contacts + gửi email báo tới Script Property NOTIFY_EMAIL
     (= tapdoanvinagroup@gmail.com). Thiếu cấu hình/gửi lỗi -> chỉ mất mail, liên hệ vẫn lưu.
     Quota Gmail 100 mail/ngày DÙNG CHUNG với OTP đăng nhập.
   - Email (cả OTP lẫn thông báo liên hệ) là email HTML có thương hiệu, khuôn RIÊNG ở
     gas/email.html (render bằng renderEmail_ trong Code.js, kind "otp" | "contact"), tên người
     gửi "Vina Group", luôn kèm bản text thuần. Mail báo liên hệ có replyTo = email khách +
     nút "Trả lời khách hàng". Không gửi mail tự động cho khách (giữ quota cho OTP).
   - Site gọi fetch() tới URL /exec với Content-Type: text/plain;charset=utf-8 (né preflight).
     Script: html/cms/contact.js (hằng GAS_EXEC_URL). build.py tự vá form trong
     html/lien-he/index.html (bỏ onsubmit mailto, thêm honeypot, gắn script) - vì trang này
     thuộc repo thien và bị ghi đè mỗi lần đồng bộ.

VI. Form công khai loại 2: Không áp dụng cho dự án này.

VII. Lưu ý UX chung:
   - 2 modal riêng: XÁC NHẬN (Huỷ/Xoá) trước khi xoá; THÔNG BÁO (1 nút Đóng) sau khi xong,
     không alert()/confirm() native, không toast. Sau mọi Lưu/Xoá bài: ghi chú
     "Website sẽ được cập nhật sau 1-2 phút!".
   - Mọi nút async: disable + spinner (withLoading), tự phục hồi kể cả khi lỗi.
   - Sau Lưu/Xoá: danh sách tự cập nhật + syncBootCache_() ngay; Lưu xong quay về danh sách.
   - Chuyển tab chỉ ẩn/hiện, không tải lại; Liên hệ/Người dùng cache localStorage (sống qua F5).
   - boot(token): 1 round-trip duy nhất {me, appHtml, posts, categories, github}.
   - CLIENT_BUILD do server băm từ app.html + js.html (clientBuild_()), ghép vào mọi key
     localStorage (trừ token), purgeStaleCaches_ dọn key bản cũ; revalidate ngầm tự vẽ lại
     appHtml khi đổi (trừ lúc đang mở form soạn).
   - Không lộ tên hạ tầng (Sheet/Drive/Apps Script/GitHub) trong app.html/js.html/index.html/
     css.html, kể cả comment và chuỗi lỗi throw ra UI.

VIII. Kiến trúc lưu trữ:
   - Google Sheet "Vina Group CMS Data" (tự tạo lần đầu):
     - Users    : email, role                     (role ∈ root | admin | editor)
     - Contacts : id, created_at, name, email, subject, message, status
                  (status ∈ "Mới" | "Đã xử lý"; KHÔNG bao giờ đẩy lên GitHub)
   - GitHub (Contents API, repo site):
     - data/posts.json              index nhẹ mọi bài (commit CHỐT, trigger CI)
     - data/tin-tuc/<slug>.json     nội dung đầy đủ 1 bài
     - data/categories.json         danh mục [{slug, name}] (commit CHỐT riêng, trigger CI)
     - data/legacy-posts.json       thẻ tin viết tay không có trang chi tiết (hiện rỗng: 3 thẻ
                                    cũ đã được viết thành bài CMS thật); CMS không đụng,
                                    build.py liệt kê sau bài CMS.
     - html/uploads/tin-tuc/*       ảnh bài viết (ghi thẳng vào vị trí site)
   - Build (scripts/build.py, GitHub Actions khi data/posts.json HOẶC data/categories.json đổi):
     - html/tin-tuc/<slug>/index.html  dựng từ CHÍNH html/tin-tuc/index.html lúc build (giữ
       đồng bộ header/footer khi repo thien đổi giao diện) - lệch khỏi mặc định "templates/"
       của playbook có chủ đích: design gốc thuộc repo khác, scaffold 1 lần sẽ lỗi thời.
     - vá vùng thẻ tin trong html/tin-tuc/index.html (giữa <!--cms:posts-begin/end-->).
     - vá khối "Tin Tức" trang chủ html/index.html: mục nào có anchor_name trùng tiêu đề bài
       CMS thì tiêu đề (cột trái, chuyển tin bằng hover) + link "Tìm hiểu thêm" trỏ thẳng tới
       bài, ảnh = ảnh bìa bài (đổi tiêu đề bài là
       mất khớp, mục đó giữ nguyên markup gốc).
     - vá form html/lien-he/index.html (mục V).
     - gọi scripts/seo/apply-seo.py (SEO trang tĩnh, robots.txt, sitemap.xml gồm cả bài, 404).
   - scripts/sync-from-thien.sh giữ lại html/uploads, html/admin, html/vendor, html/cms,
     wrangler.jsonc, .assetsignore, _headers rồi chạy build.py.
   - Độ trễ từ Lưu tới site: ~1-2 phút (CI build + deploy khi push).

IX. Bug đã gặp ở dự án này:
   - Hàm public include(filename) (có từ bản mẫu) cho phép người CHƯA đăng nhập gọi
     google.script.run.include("app") lấy trọn markup trang quản trị — do mọi hàm không có
     hậu tố _ đều gọi được từ client. Cách né: đổi thành include_ (private); scriptlet phía
     server vẫn gọi được. Mọi hàm helper mới phải có hậu tố _ nếu không cần gọi từ client.

X. Script Properties (TÊN cố định; giá trị người deploy tự điền):
   - GITHUB_TOKEN  : fine-grained PAT, Contents = Read and write cho repo vinagroup.
   - GITHUB_OWNER  = tranquanghuy-rightsvn
   - GITHUB_REPO   = vinagroup
   - GITHUB_BRANCH = master
   - NOTIFY_EMAIL  = tapdoanvinagroup@gmail.com
   - SPREADSHEET_ID: KHÔNG điền, code tự tạo Sheet lần đầu và tự lưu.
```
