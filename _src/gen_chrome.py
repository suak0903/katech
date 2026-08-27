#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chrome des Demonstrators aus EINER Quelle: Kopfleiste, mobiles Menue,
Fusszeile, Demo-Leiste, Consent-Banner. Wird vom Generator in jede Seite
eingesetzt, damit alle Seiten byte-identisches Chrome tragen."""

ORT = "KaTech Ingredient Solutions"
ORIGINAL = "https://katech-solutions.com/"
# Aus der Bestandsseite uebernommen. Der dortige Xing-Eintrag liefert 404
# und wird deshalb nicht mitgefuehrt.
LINKEDIN = "https://www.linkedin.com/company/katech-katharina-hahn-&amp;-partner/"

# Hauptnavigation: Reihenfolge gilt in Kopfleiste UND mobilem Menue
NAV = [
    ("Solutions", "solutions/"),
    ("Expertise", "expertise/"),
    ("Company", "company/"),
    ("Facilities", "our-facilities/"),
    ("News", "news/"),
]

FOOT_SPALTEN = [
    # Die ersten vier fuehren auf ihren Abschnitt der Solutions-Seite. Vegan
    # solutions ist die eigene Bereichsseite und steht deshalb abgesetzt.
    ("Solutions", [
        ("Dairy and dairy alternatives", "solutions/#dairy"),
        ("Plant-based alternatives", "solutions/#plant"),
        ("Savoury", "solutions/#savoury"),
        ("Bakery and fruit", "solutions/#bakery"),
        ("All product areas", "solutions/"),
        ("Vegan solutions", "vegan/"),
    ]),
    ("Expertise", [
        ("New product development", "new-products/"),
        ("Troubleshooting", "troubleshooting/"),
        ("Cost optimisation", "cost-optimisation/"),
        ("Ingredients used", "our-ingredients/"),
        ("Fat and sugar reduction", "fat-reduction/"),
    ]),
    ("Company", [
        ("Our vision", "our-vision/"),
        ("How we work", "how-we-work/"),
        ("Our people", "our-people/"),
        ("Case studies", "case-studies/"),
        ("Certifications", "certifications/"),
        ("Sourcing and sustainability", "sourcing-and-sustainability/"),
        ("Careers", "careers/"),
        ("Customer area", "customer-area/"),
    ]),
]



# Landesflaggen und das LinkedIn-Zeichen als Inline-SVG (Kit: keine Icon-Fonts).
# Die Flaggen stehen fuer die drei Maerkte, die die Bestandsseite bedient.
FLAGGE_GB = ('<svg viewBox="0 0 60 30" width="22" height="11" aria-hidden="true">'
             '<path d="M0 0h60v30H0z" fill="#012169"/>'
             '<path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/>'
             '<path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/>'
             '<path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/>'
             '</svg>')
FLAGGE_DE = ('<svg viewBox="0 0 5 3" width="22" height="13" aria-hidden="true">'
             '<path d="M0 0h5v3H0z"/><path d="M0 1h5v2H0z" fill="#D00"/>'
             '<path d="M0 2h5v1H0z" fill="#FFCE00"/></svg>')
FLAGGE_PL = ('<svg viewBox="0 0 8 5" width="22" height="13" aria-hidden="true">'
             '<path d="M0 0h8v5H0z" fill="#fff"/><path d="M0 2.5h8V5H0z" fill="#DC143C"/></svg>')
ZEICHEN_LI = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
              '<path d="M20.4 20.4h-3.6v-5.6c0-1.3 0-3-1.9-3-1.9 0-2.1 1.4-2.1 2.9v5.7H9.3V9h3.4v1.6h.1c.5-.9 '
              '1.6-1.9 3.4-1.9 3.6 0 4.3 2.4 4.3 5.5v6.2zM5.3 7.4a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2zm1.8 '
              '13H3.5V9h3.6v11.4zM22.2 0H1.8C.8 0 0 .8 0 1.7v20.6c0 .9.8 1.7 1.8 1.7h20.4c1 0 1.8-.8 '
              '1.8-1.7V1.7c0-.9-.8-1.7-1.8-1.7z"/></svg>')


def pfad(root, ziel):
    """Relativer Pfad vom aktuellen Seitenverzeichnis aus."""
    if ziel.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return ziel
    return root + ziel


def kopf(root, aktiv="", solid=False):
    links = []
    for text, ziel in NAV:
        cur = ' aria-current="page"' if aktiv and ziel.startswith(aktiv) else ""
        links.append(f'<a href="{pfad(root, ziel)}"{cur}>{text}</a>')
    links.append(f'<a class="nav__cta" href="{pfad(root, "contact-us/")}">Make an enquiry</a>')
    klasse = "nav solid" if solid else "nav"
    return f'''<header class="{klasse}">
  <div class="nav__inner">
    <a class="brand" href="{pfad(root, "index.html")}" aria-label="{ORT} - to the start page">
      <img class="logo-light" src="{root}media/logo-light.png" alt="{ORT}" width="420" height="120" fetchpriority="high">
      <img class="logo-dark" src="{root}media/logo-dark.png" alt="{ORT}" width="420" height="120">
    </a>
    <nav class="nav__links" aria-label="Main navigation">
      {chr(10).join("      " + l for l in links).strip()}
    </nav>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" data-lang="en" aria-current="true">{FLAGGE_GB}<span>EN</span></button>
      <button type="button" data-lang="de">{FLAGGE_DE}<span>DE</span></button>
      <button type="button" data-lang="pl">{FLAGGE_PL}<span>PL</span></button>
    </div>
    <button class="burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mmenu"><span></span></button>
  </div>
</header>
<nav class="mmenu" id="mmenu" aria-label="Mobile navigation" hidden>
  <div class="mmenu__body">
    <div class="mmenu__lang" role="group" aria-label="Language">
      <button type="button" data-lang="en" aria-current="true">{FLAGGE_GB}<span>EN</span></button>
      <button type="button" data-lang="de">{FLAGGE_DE}<span>DE</span></button>
      <button type="button" data-lang="pl">{FLAGGE_PL}<span>PL</span></button>
    </div>
    <ul class="mmenu__list">
{mobil_links(root)}
    </ul>
    <div class="mmenu__foot">
      <a class="mmenu__pill mmenu__pill--cta" href="{pfad(root, "contact-us/")}">Make an enquiry</a>
      <div class="mmenu__pills">
        <a class="mmenu__pill" href="tel:+4945140702000">Call Lübeck</a>
        <a class="mmenu__pill" href="mailto:hello@katech-solutions.com">E-mail</a>
      </div>
      <a class="mmenu__pill mmenu__pill--li" href="{LINKEDIN}" target="_blank" rel="noopener">{ZEICHEN_LI}<span>KaTech on LinkedIn</span></a>
    </div>
  </div>
</nav>'''


def mobil_links(root):
    zeilen = []
    alle = NAV + [("Contact", "contact-us/")]
    for i, (text, ziel) in enumerate(alle, 1):
        zeilen.append(f'      <li><a href="{pfad(root, ziel)}"><span class="mmenu__num">{i:02d}</span>{text}</a></li>')
    return "\n".join(zeilen)


def fuss(root):
    spalten = []
    for titel, eintraege in FOOT_SPALTEN:
        li = "\n".join(f'        <li><a href="{pfad(root, z)}">{t}</a></li>' for t, z in eintraege)
        kuerzel = titel.split()[0].lower()
        spalten.append(f'''      <nav aria-labelledby="foot-{kuerzel}">
        <h2 class="foot__h" id="foot-{kuerzel}">{titel}</h2>
        <ul>
{li}
        </ul>
      </nav>''')
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div class="foot__brand">
        <img src="{root}media/logo-light.png" alt="{ORT}" width="420" height="120">
        <p>Bespoke stabilising and texturising solutions for the food industry.
        Developed in Lübeck, produced in Germany, the UK and Poland. Part of Ingredion.</p>
        <a class="foot__social" href="{LINKEDIN}" target="_blank" rel="noopener">
          <svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M20.4 20.4h-3.6v-5.6c0-1.3 0-3-1.9-3-1.9 0-2.1 1.4-2.1 2.9v5.7H9.3V9h3.4v1.6h.1c.5-.9 1.6-1.9 3.4-1.9 3.6 0 4.3 2.4 4.3 5.5v6.2zM5.3 7.4a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2zm1.8 13H3.5V9h3.6v11.4zM22.2 0H1.8C.8 0 0 .8 0 1.7v20.6c0 .9.8 1.7 1.8 1.7h20.4c1 0 1.8-.8 1.8-1.7V1.7c0-.9-.8-1.7-1.8-1.7z"/>
          </svg>
          <span>KaTech on LinkedIn</span>
        </a>
        <a class="foot__social" href="{pfad(root, "find-us/")}">
          <svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>
          </svg>
          <span>Find us</span>
        </a>
      </div>
{chr(10).join(spalten)}
    </div>
    <div class="foot__bar">
      <span>© 2026 {ORT} GmbH. Design preview by Dr.-Ing. Suat Akyol.</span>
      <nav aria-label="Legal">
        <a href="{pfad(root, "sitemap/")}">Sitemap</a>
        <a href="{pfad(root, "imprint/")}">Imprint</a>
        <a href="{pfad(root, "privacy-policy/")}">Privacy policy</a>
        <a href="{pfad(root, "terms-of-use/")}">Terms of use</a>
        <a href="{pfad(root, "cookie-policy-eu/")}">Cookie policy</a>
        <a href="#" data-consent-revoke>Cookie settings</a>
      </nav>
    </div>
  </div>
</footer>'''


def demoleiste(root):
    return f'''<div class="demobar" id="demobar">
  <span>Redesign preview, not an official {ORT} website.
    <a href="{pfad(root, "about-this-preview/")}">What is different?</a>
    <span class="demobar__sep">·</span>
    <a href="{pfad(root, "sitemap/")}">Sitemap</a>
    <span class="demobar__sep">·</span>
    <a href="{ORIGINAL}" target="_blank" rel="noopener">Original site</a></span>
  <button id="demoClose" type="button" aria-label="Dismiss notice">&times;</button>
</div>'''


def consent(root):
    return '''<div class="consent" id="consent" role="dialog" aria-label="Cookie notice" hidden>
  <div class="consent__inner">
    <p>This preview loads no tracking and sets no advertising cookies. Only if you open a map
      is content requested from Google Maps. Your choice is stored locally in your browser.</p>
    <div class="consent__actions">
      <button class="btn btn--primary" type="button" data-consent="ja">Allow external maps</button>
      <button class="btn btn--outline" type="button" data-consent="nein">Decline</button>
    </div>
  </div>
</div>'''
