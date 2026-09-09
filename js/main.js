/* geertvos.be — menu + lamp-aan intro */
(function () {
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

  // Hero: de lamp flikkert één keer aan per bezoek, daarna staat hij gewoon aan
  var hero = document.querySelector('.hero');
  if (hero) {
    var gezien = false;
    try { gezien = sessionStorage.getItem('gv-lamp') === '1'; } catch (e) {}
    var rustig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
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
  }

  var form = document.querySelector('form[data-gv]');
  if (form) {
    form.addEventListener('submit', function () {
      var btn = form.querySelector('button[type=submit]');
      if (btn) { btn.disabled = true; btn.textContent = 'Versturen…'; }
    });
  }
})();
