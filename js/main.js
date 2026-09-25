/* geertvos.be — menu, lamp, teller, stroomlijn, voor/na-slider */
(function () {
  var rustig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mobiel menu
  var head = document.querySelector('.site-head');
  var toggle = document.querySelector('.nav-toggle');
  if (head && toggle) {
    toggle.addEventListener('click', function () {
      var open = head.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && head.classList.contains('nav-open')) {
        head.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Diensten-submenu (klik/touch; hover werkt via CSS)
  document.querySelectorAll('.sub-knop').forEach(function (knop) {
    knop.addEventListener('click', function () {
      var sub = knop.parentNode;
      var open = sub.classList.toggle('open');
      knop.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // Hero: de lamp flikkert één keer aan per bezoek, daarna staat hij gewoon aan
  var hero = document.querySelector('.hero');
  if (hero) {
    var gezien = false;
    try { gezien = sessionStorage.getItem('gv-lamp') === '1'; } catch (e) {}
    if (gezien || rustig) {
      hero.classList.add('lit');
    } else {
      hero.classList.add('flik');
      window.setTimeout(function () {
        hero.classList.add('lit');
        hero.classList.remove('flik');
      }, 1500);
      try { sessionStorage.setItem('gv-lamp', '1'); } catch (e) {}
    }

    // Het licht volgt de cursor (alleen met een muis, niet op touch)
    if (!rustig && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      var raf = null;
      hero.addEventListener('mousemove', function (e) {
        if (raf) return;
        raf = window.requestAnimationFrame(function () {
          var r = hero.getBoundingClientRect();
          hero.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
          hero.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
          hero.classList.add('volgt');
          raf = null;
        });
      });
      hero.addEventListener('mouseleave', function () {
        hero.classList.remove('volgt');
        hero.style.removeProperty('--mx');
        hero.style.removeProperty('--my');
      });
    } else if (!rustig && hero.classList.contains('flik')) {
      // Geen muis: het licht veegt één keer mee binnen als de lamp aanflikkert
      var t0v = null, duurVeeg = 1400;
      var veeg = function (t) {
        if (!t0v) t0v = t;
        var p = Math.min(1, (t - t0v) / duurVeeg);
        var e = 1 - Math.pow(1 - p, 3);
        hero.style.setProperty('--mx', (12 + 60 * e).toFixed(1) + '%');
        hero.style.setProperty('--my', (28 + 17 * e).toFixed(1) + '%');
        if (p < 1) window.requestAnimationFrame(veeg);
      };
      window.setTimeout(function () { window.requestAnimationFrame(veeg); }, 1500);
    }

    // De lamp knipoogt als je eroverheen gaat (of erop tikt)
    var lamp = hero.querySelector('.lamp');
    if (lamp && !rustig) {
      var knipoog = function () {
        if (!hero.classList.contains('lit') || lamp.classList.contains('knipoog')) return;
        lamp.classList.add('knipoog');
        window.setTimeout(function () { lamp.classList.remove('knipoog'); }, 950);
      };
      lamp.addEventListener('mouseenter', knipoog);
      lamp.addEventListener('click', knipoog);
    }
  }

  // Teller: dagen sinds de start bij Nike (afgerond op tientallen, telt op als de hero zichtbaar is)
  document.querySelectorAll('.teller[data-sinds]').forEach(function (el) {
    var start = new Date(el.getAttribute('data-sinds') + 'T00:00:00');
    var dagen = Math.floor((Date.now() - start.getTime()) / 864e5 / 10) * 10;
    var fmt = function (n) { return n.toLocaleString('nl-BE'); };
    if (rustig) { el.textContent = fmt(dagen); return; }
    var t0 = null, duur = 1600;
    var tik = function (t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / duur);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(dagen * e / 10) * 10);
      if (p < 1) window.requestAnimationFrame(tik);
    };
    window.setTimeout(function () { window.requestAnimationFrame(tik); }, hero && hero.classList.contains('flik') ? 1500 : 200);
  });

  // Stroomlijn: één stroompje als hij in beeld komt, daarna om de zoveel tijd nog eens
  if (!rustig && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var el = en.target;
        if (en.isIntersecting) {
          el.classList.add('stroomt');
          el._timer = window.setInterval(function () {
            el.classList.remove('stroomt');
            void el.offsetWidth; // herstart de animatie
            el.classList.add('stroomt');
          }, 7000);
        } else if (el._timer) {
          window.clearInterval(el._timer); el._timer = null;
          el.classList.remove('stroomt');
        }
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('.stroom').forEach(function (el) { io.observe(el); });
  }

  // Voor/na-slider
  document.querySelectorAll('[data-vergelijk]').forEach(function (blok) {
    var beeld = blok.querySelector('.vergelijk-beeld');
    var range = blok.querySelector('input[type=range]');
    var zet = function (p) {
      p = Math.min(99.5, Math.max(0.5, Number(p)));
      beeld.style.setProperty('--p', p + '%');
      beeld.style.setProperty('--pf', (p / 100).toFixed(4));
    };
    zet(50);
    range.addEventListener('input', function () { zet(range.value); });
  });

  // Vacatures: functie voorselecteren via ?functie=
  var functie = document.getElementById('s-functie');
  if (functie && window.URLSearchParams) {
    var gekozen = new URLSearchParams(location.search).get('functie');
    if (gekozen) {
      for (var i = 0; i < functie.options.length; i++) {
        if (functie.options[i].value === gekozen) { functie.selectedIndex = i; }
      }
    }
  }

  // Formulieren
  var form = document.querySelector('form[data-gv]');
  if (form) {
    form.addEventListener('submit', function () {
      var btn = form.querySelector('button[type=submit]');
      if (btn) { btn.disabled = true; btn.textContent = 'Versturen…'; }
    });
  }
})();
