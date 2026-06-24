/* FLORSIMINTEX · app.js — interacțiuni minime, fără dependențe. */
(function () {
  'use strict';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* anul curent în footer */
  var y = document.getElementById('y');
  if (y) y.textContent = new Date().getFullYear();

  /* meniu mobil */
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* reveal la scroll, cu mic decalaj pe grupuri */
  var revs = [].slice.call(document.querySelectorAll('.reveal'));
  if (reduce || !('IntersectionObserver' in window)) {
    revs.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var sibs = [].slice.call((el.parentElement || document).children).filter(function (c) { return c.classList && c.classList.contains('reveal'); });
        var idx = Math.max(0, sibs.indexOf(el));
        el.style.transitionDelay = Math.min(idx * 80, 320) + 'ms';
        el.classList.add('in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revs.forEach(function (el) { io.observe(el); });
  }

  /* count-up pentru statistici numerice */
  var counted = false;
  function runCount() {
    if (counted) return; counted = true;
    document.querySelectorAll('.stat b[data-count]').forEach(function (el) {
      var raw = el.getAttribute('data-count');
      var m = /^(\d+)(.*)$/.exec(raw);
      if (!m || raw.indexOf('/') > -1 || reduce) { el.textContent = raw; return; }
      var target = parseInt(m[1], 10), suffix = m[2] || '', t0 = null, dur = 1200;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var e = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * e) + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }
  var statsEl = document.querySelector('.stats');
  if (statsEl && 'IntersectionObserver' in window && !reduce) {
    var io2 = new IntersectionObserver(function (e) {
      if (e[0].isIntersecting) { runCount(); io2.disconnect(); }
    }, { threshold: 0.4 });
    io2.observe(statsEl);
  } else { runCount(); }

  /* header: umbră la scroll */
  var head = document.querySelector('.site-head');
  if (head) {
    var onScroll = function () { head.classList.toggle('scrolled', window.scrollY > 8); };
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }
})();
