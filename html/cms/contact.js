/**
 * Form Liên hệ (/lien-he/) -> gửi thẳng về CMS (lưu lại + email báo), thay cho mailto:.
 * Quyết định nghiệp vụ: GAS.md mục V. Form được build.py vá tự động (thêm honeypot, bỏ
 * onsubmit mailto, gắn script này) vì trang lien-he thuộc repo thien, bị ghi đè mỗi lần sync.
 */
(function () {
  // URL web app /exec của CMS - điền sau khi deploy (gas/README.md bước 6).
  var GAS_EXEC_URL = 'https://script.google.com/macros/s/AKfycbx4jwZfFsbAKZlzz3M-hK_bXLG8Rg9wj_PiS3lYPZQqYFuA1i7J35kqwXjgqez8Tj2m/exec';

  var form = document.getElementById('vgContactForm');
  if (!form) return;
  var status = document.getElementById('vgFormStatus');
  var button = form.querySelector('button[type="submit"]');
  var buttonHtml = button ? button.innerHTML : '';

  function setStatus(text, type) {
    if (!status) return;
    status.textContent = text;
    status.style.color = type === 'error' ? '#c0392b' : type === 'success' ? '#0f6b3f' : '';
    status.style.fontWeight = type ? '600' : '';
  }

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!GAS_EXEC_URL) {
      // Chưa cấu hình CMS: giữ đúng hành vi cũ của trang (mở ứng dụng email soạn sẵn) để site
      // thật không mất kênh liên hệ trong lúc chờ deploy.
      var subject = val('vgSubject') || 'Yêu cầu hỗ trợ từ website';
      window.location.href = 'mailto:tapdoanvinagroup@gmail.com?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent('Họ tên: ' + val('vgName') + '\nEmail: ' + val('vgEmail') + '\n\n' + val('vgMessage'));
      return;
    }
    var payload = {
      formType: 'contact',
      name: val('vgName'),
      email: val('vgEmail'),
      subject: val('vgSubject'),
      message: val('vgMessage'),
      _hp: val('vgHp')
    };
    if (button) {
      button.disabled = true;
      button.textContent = 'Đang gửi...';
    }
    setStatus('', '');
    // text/plain giữ request ở dạng "simple request" - trình duyệt không gửi preflight OPTIONS
    // (phía CMS không xử lý được OPTIONS).
    fetch(GAS_EXEC_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    })
      .then(function (res) { return res.json(); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.error || 'Gửi không thành công');
        form.reset();
        setStatus('Cảm ơn bạn! Yêu cầu đã được gửi tới Vina Group, chúng tôi sẽ phản hồi qua email trong thời gian sớm nhất.', 'success');
      })
      .catch(function (err) {
        console.error('[lien-he] gửi thất bại:', err);
        setStatus((err && err.message && err.message !== 'Failed to fetch' ? err.message + '. ' : 'Không gửi được do lỗi kết nối. ') +
          'Bạn có thể gọi hotline 077.291.6169 hoặc email tapdoanvinagroup@gmail.com.', 'error');
      })
      .then(function () {
        if (button) {
          button.disabled = false;
          button.innerHTML = buttonHtml;
        }
      });
  });
})();
