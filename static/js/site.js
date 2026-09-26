(function () {
  // Google Analytics event helper (no-op without GA)
  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-track]");
    if (el) track("cta_click", { cta: el.dataset.track });
    var tel = e.target.closest('a[href^="tel:"]');
    if (tel) track("phone_click");
  });
  document.querySelectorAll("form[data-track-submit]").forEach(function (f) {
    f.addEventListener("submit", function () { track("form_submit", { form: f.dataset.trackSubmit }); });
  });

  // Gallery lightbox: open the carousel at the clicked photo
  var lb = document.getElementById("lightbox");
  if (lb) {
    lb.addEventListener("show.bs.modal", function (e) {
      var idx = parseInt(e.relatedTarget.dataset.index || "0", 10);
      bootstrap.Carousel.getOrCreateInstance("#lightboxCarousel").to(idx);
    });
  }

  // Count-up numbers on the homepage stats
  var nums = document.querySelectorAll("[data-count]");
  if (nums.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = +el.dataset.count, start = performance.now();
        (function step(t) {
          var p = Math.min((t - start) / 1200, 1);
          el.textContent = Math.round(end * p) + (p === 1 && end >= 50 ? "+" : "");
          if (p < 1) requestAnimationFrame(step);
        })(start);
        io.unobserve(el);
      });
    });
    nums.forEach(function (n) { io.observe(n); });
  }
})();
