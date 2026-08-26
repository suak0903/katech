/* =====================================================================
   KaTech Design-Vorschau - Seitenlogik
   Funktionsliste (bei Aenderungen mitpflegen und nach dem Deploy pruefen):
     1. has-js / no-js
     2. Kopfleiste: scrolled-Zustand
     3. Mobiles Menue: oeffnen, schliessen, ESC, Aussen-Tap, Swipe, Linkklick
        (kein eigenes Logo, die Kopfleiste bleibt sichtbar)
     4. Hero-Parallaxe 50 Prozent auf Start- und Unterseiten (rAF, GPU)
     5. Reveal beim Scrollen (IntersectionObserver)
     6. Galerie-Lightbox (ESC, Pfeile, Swipe, Zaehler)
     7. Demo-Leiste schliessen (nur fuer die aktuelle Ansicht)
     8. Nach-oben-Knopf der Hinweisseite
     9. Consent-Banner und consent-gated Karte
    10. Sprachumschalter (Stub mit Hinweis)
    11. Anfrageformular (Attrappe, kein Backend)
   ===================================================================== */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. has-js -------------------------------------------------------- */
  document.documentElement.classList.remove('no-js');
  document.documentElement.classList.add('has-js');

  /* 2. Kopfleiste ---------------------------------------------------- */
  var nav = document.querySelector('.nav');
  if (nav && !nav.classList.contains('solid')) {
    var setScrolled = function () {
      nav.classList.toggle('scrolled', window.scrollY > 28);
    };
    setScrolled();
    window.addEventListener('scroll', setScrolled, { passive: true });
  }

  /* 3. Mobiles Menue ------------------------------------------------- */
  var burger = document.getElementById('burger');
  var mmenu = document.getElementById('mmenu');
  if (burger && mmenu) {
    var oeffnen = function () {
      mmenu.hidden = false;
      // erzwingt einen Reflow, damit die Transition greift
      void mmenu.offsetWidth;
      mmenu.classList.add('open');
      mmenu.removeAttribute('inert');
      nav.classList.add('menu-open');
      burger.setAttribute('aria-expanded', 'true');
    };
    var schliessen = function () {
      mmenu.classList.remove('open');
      mmenu.setAttribute('inert', '');
      nav.classList.remove('menu-open');
      burger.setAttribute('aria-expanded', 'false');
      window.setTimeout(function () {
        if (!mmenu.classList.contains('open')) mmenu.hidden = true;
      }, 420);
    };
    mmenu.setAttribute('inert', '');
    mmenu.hidden = true;
    burger.addEventListener('click', function () {
      if (mmenu.classList.contains('open')) schliessen(); else oeffnen();
    });
    mmenu.addEventListener('click', function (e) {
      if (e.target.closest('a')) schliessen();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mmenu.classList.contains('open')) schliessen();
    });
    document.addEventListener('click', function (e) {
      if (!mmenu.classList.contains('open')) return;
      if (e.target.closest('#mmenu') || e.target.closest('#burger')) return;
      schliessen();
    });
    // Swipe nach rechts schliesst (Herkunftsrichtung)
    var sx = 0, sy = 0;
    mmenu.addEventListener('touchstart', function (e) {
      sx = e.touches[0].clientX; sy = e.touches[0].clientY;
    }, { passive: true });
    mmenu.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - sx;
      var dy = e.changedTouches[0].clientY - sy;
      if (dx > 55 && Math.abs(dx) > Math.abs(dy)) schliessen();
    }, { passive: true });
  }

  /* 4. Hero-Parallaxe ------------------------------------------------ */
  // Gilt fuer den Hero der Startseite und die Hero-Bilder der Unterseiten.
  var parallaxe = document.getElementById('heroBg') || document.getElementById('subheroBg');
  if (parallaxe && !reduce) {
    var laeuft = false;
    var zeichnen = function () {
      parallaxe.style.transform = 'translate3d(0,' + (window.scrollY * 0.5) + 'px,0)';
      laeuft = false;
    };
    window.addEventListener('scroll', function () {
      if (!laeuft) { laeuft = true; window.requestAnimationFrame(zeichnen); }
    }, { passive: true });
    zeichnen();
  }

  /* 5. Reveal -------------------------------------------------------- */
  var rvs = document.querySelectorAll('.rv');
  if (rvs.length) {
    if (!('IntersectionObserver' in window) || reduce) {
      Array.prototype.forEach.call(rvs, function (el) { el.classList.add('in'); });
    } else {
      var io = new IntersectionObserver(function (eintraege) {
        eintraege.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
      Array.prototype.forEach.call(rvs, function (el) { io.observe(el); });
    }
  }

  /* 6. Lightbox ------------------------------------------------------ */
  var galerie = document.querySelector('.gallery');
  var lb = document.getElementById('lb');
  if (galerie && lb) {
    var knoepfe = Array.prototype.slice.call(galerie.querySelectorAll('button'));
    var lbImg = lb.querySelector('img');
    var lbCount = lb.querySelector('.lb__count');
    var index = 0;

    var zeigen = function (i) {
      index = (i + knoepfe.length) % knoepfe.length;
      var q = knoepfe[index].querySelector('img');
      lbImg.src = knoepfe[index].dataset.full || q.currentSrc || q.src;
      lbImg.alt = q.alt || '';
      if (lbCount) lbCount.textContent = (index + 1) + ' / ' + knoepfe.length;
    };
    var oeffnenLb = function (i) {
      zeigen(i); lb.hidden = false; document.body.style.overflow = 'hidden';
      var c = lb.querySelector('.lb__close'); if (c) c.focus();
    };
    var schliessenLb = function () {
      lb.hidden = true; document.body.style.overflow = '';
    };
    knoepfe.forEach(function (b, i) {
      b.addEventListener('click', function () { oeffnenLb(i); });
    });
    lb.querySelector('.lb__close').addEventListener('click', schliessenLb);
    lb.querySelector('.lb__prev').addEventListener('click', function () { zeigen(index - 1); });
    lb.querySelector('.lb__next').addEventListener('click', function () { zeigen(index + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) schliessenLb(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') schliessenLb();
      if (e.key === 'ArrowLeft') zeigen(index - 1);
      if (e.key === 'ArrowRight') zeigen(index + 1);
    });
    var lx = 0;
    lb.addEventListener('touchstart', function (e) { lx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      var d = e.changedTouches[0].clientX - lx;
      if (Math.abs(d) > 50) zeigen(index + (d < 0 ? 1 : -1));
    }, { passive: true });
  }

  /* 7. Demo-Leiste --------------------------------------------------- */
  var demoClose = document.getElementById('demoClose');
  if (demoClose) {
    demoClose.addEventListener('click', function () {
      var b = document.getElementById('demobar');
      if (b) b.classList.add('hide');
      document.body.classList.add('demobar-zu');
    });
  }

  /* 8. Nach-oben-Knopf ----------------------------------------------- */
  var tocTop = document.getElementById('tocTop');
  if (tocTop) {
    window.addEventListener('scroll', function () {
      tocTop.classList.toggle('show', window.scrollY > 640);
    }, { passive: true });
    tocTop.addEventListener('click', function () {
      var ziel = document.getElementById('toc') || document.body;
      ziel.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
  }

  /* 9. Consent und Karte --------------------------------------------- */
  var consent = document.getElementById('consent');
  var SCHLUESSEL = 'katech-demo-consent';
  var karteLaden = function () {
    Array.prototype.forEach.call(document.querySelectorAll('[data-src]'), function (el) {
      if (!el.src) el.src = el.dataset.src;
      var platz = el.closest('.mapwrap');
      if (platz) {
        var ph = platz.querySelector('.mapph');
        if (ph) ph.hidden = true;
      }
    });
  };
  var karteEntfernen = function () {
    Array.prototype.forEach.call(document.querySelectorAll('[data-src]'), function (el) {
      el.removeAttribute('src');
      var platz = el.closest('.mapwrap');
      if (platz) {
        var ph = platz.querySelector('.mapph');
        if (ph) ph.hidden = false;
      }
    });
  };
  var demobar = document.getElementById('demobar');
  var demobarSchieben = function (an) {
    if (!demobar || !consent) return;
    // Beide Leisten sitzen unten; solange die Einwilligung offen ist, tritt
    // der Demo-Hinweis zurueck, sonst ueberlagern sie sich.
    demobar.style.visibility = an ? 'hidden' : '';
  };
  var stand = null;
  try { stand = window.localStorage.getItem(SCHLUESSEL); } catch (e) { stand = null; }
  if (stand === 'ja') karteLaden();
  if (consent && stand === null) { consent.hidden = false; demobarSchieben(true); }
  if (consent) {
    consent.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-consent]');
      if (!b) return;
      var wert = b.dataset.consent;
      try { window.localStorage.setItem(SCHLUESSEL, wert); } catch (err) { /* Privatmodus */ }
      consent.hidden = true;
      demobarSchieben(false);
      if (wert === 'ja') karteLaden(); else karteEntfernen();
    });
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-consent-revoke]');
    if (!t) return;
    e.preventDefault();
    try { window.localStorage.removeItem(SCHLUESSEL); } catch (err) { /* Privatmodus */ }
    karteEntfernen();
    if (consent) { consent.hidden = false; demobarSchieben(true); }
  });
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-map-load]');
    if (!t) return;
    e.preventDefault();
    try { window.localStorage.setItem(SCHLUESSEL, 'ja'); } catch (err) { /* Privatmodus */ }
    if (consent) consent.hidden = true;
    demobarSchieben(false);
    karteLaden();
  });

  /* 10. Sprachumschalter (Stub) -------------------------------------- */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-lang]');
    if (!b) return;
    if (b.getAttribute('aria-current') === 'true') return;
    window.alert('This design preview is built in English only. The live site keeps all three '
      + 'languages (EN / DE / PL) via the existing translation structure.');
  });

  /* 11. Anfrageformular (Attrappe) ----------------------------------- */
  var form = document.getElementById('enquiry');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var hinweis = document.getElementById('formNote');
      if (hinweis) {
        hinweis.hidden = false;
        hinweis.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      }
    });
  }
})();
