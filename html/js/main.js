(function () {
  var body = document.body;
  var bar = document.querySelector(".header-bar");
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("main-nav");

  // Sticky header: bar becomes fixed (green) once the page scrolls past it.
  function onScroll() {
    bar.classList.toggle("is-sticky", window.scrollY > bar.parentElement.offsetHeight);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile menu toggle
  function setMenu(open) {
    body.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Đóng menu" : "Mở menu");
  }
  toggle.addEventListener("click", function () {
    setMenu(!body.classList.contains("menu-open"));
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setMenu(false);
  });

  // Contact form: no backend on a static site, so hand the message to the visitor's mail app
  var form = document.getElementById("contact-form");
  if (form) {
    var q = form.querySelector(".captcha-question");
    var answerInput = form.querySelector('[name="captcha"]');
    var answer = 0;
    var newQuestion = function () {
      var a = 1 + Math.floor(Math.random() * 9);
      var b = 1 + Math.floor(Math.random() * 9);
      answer = a + b;
      q.textContent = a + " + " + b + " = ?";
      answerInput.value = "";
    };
    newQuestion();
    form.querySelector(".captcha-refresh").addEventListener("click", newQuestion);
    answerInput.addEventListener("input", function () { answerInput.classList.remove("is-invalid"); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (+answerInput.value !== answer) {
        answerInput.classList.add("is-invalid");
        answerInput.focus();
        newQuestion();
        return;
      }
      var d = new FormData(form);
      var body = "Họ tên: " + d.get("name") + "\nEmail: " + d.get("email") + "\n\n" + d.get("message");
      window.location.href = form.getAttribute("action") +
        "?subject=" + encodeURIComponent("Liên hệ từ website - " + d.get("name")) +
        "&body=" + encodeURIComponent(body);
      form.querySelector(".form-status").textContent = "Đang mở ứng dụng email để gửi thông tin của bạn…";
    });
  }

  // Count-up animation when counters enter the viewport
  var nums = document.querySelectorAll(".counter-num");
  if (!nums.length || !("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  function run(el) {
    var target = +el.dataset.count;
    var start = performance.now();
    var dur = 2000;
    (function step(now) {
      var t = Math.min((now - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3)));
      if (t < 1) requestAnimationFrame(step);
    })(start);
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        io.unobserve(en.target);
        run(en.target);
      }
    });
  }, { threshold: 0.5 });
  // The real numbers stay in the HTML (crawlers never scroll, so they always see them).
  // Only once a visitor starts scrolling are below-the-fold counters reset and animated.
  var belowFold = [].filter.call(nums, function (el) {
    return el.getBoundingClientRect().top >= window.innerHeight;
  });
  window.addEventListener("scroll", function () {
    belowFold.forEach(function (el) {
      el.textContent = "0";
      io.observe(el);
    });
  }, { once: true, passive: true });
})();
