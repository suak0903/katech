#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chrome des Demonstrators aus EINER Quelle: Kopfleiste, mobiles Menue,
Fusszeile, Demo-Leiste, Consent-Banner. Wird vom Generator in jede Seite
eingesetzt, damit alle Seiten byte-identisches Chrome tragen."""

ORT = "KaTech Ingredient Solutions"
ORIGINAL = "https://katech-solutions.com/"

# Hauptnavigation: Reihenfolge gilt in Kopfleiste UND mobilem Menue
NAV = [
    ("Solutions", "solutions/"),
    ("Expertise", "expertise/"),
    ("Company", "company/"),
    ("Facilities", "our-facilities/"),
    ("News", "news/"),
]

FOOT_SPALTEN = [
    ("Solutions", [
        ("Dairy and dairy alternatives", "solutions/#dairy"),
        ("Plant-based meat and fish", "vegan/"),
        ("Savoury", "solutions/#savoury"),
        ("Bakery and fruit", "solutions/#bakery"),
        ("All product areas", "solutions/"),
    ]),
    ("Expertise", [
        ("How we work", "how-we-work/"),
        ("Our people", "our-people/"),
        ("Ingredients used", "our-ingredients/"),
        ("New product development", "new-products/"),
        ("Troubleshooting", "troubleshooting/"),
        ("Cost optimisation", "cost-optimisation/"),
    ]),
    ("Company", [
        ("Our vision", "our-vision/"),
        ("Our facilities", "our-facilities/"),
        ("Certifications", "certifications/"),
        ("Sourcing and sustainability", "sourcing-and-sustainability/"),
        ("Careers", "careers/"),
        ("Find us", "find-us/"),
        ("Customer area", "customer-area/"),
    ]),
]


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
      <button type="button" data-lang="en" aria-current="true">EN</button>
      <button type="button" data-lang="de">DE</button>
      <button type="button" data-lang="pl">PL</button>
    </div>
    <button class="burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mmenu"><span></span></button>
  </div>
</header>
<nav class="mmenu" id="mmenu" aria-label="Mobile navigation" hidden>
  <div class="mmenu__body">
    <ul class="mmenu__list">
{mobil_links(root)}
    </ul>
    <div class="mmenu__foot">
      <a class="mmenu__pill" href="{pfad(root, "contact-us/")}" style="grid-column:1/-1;background:rgba(108,179,62,.22);border-color:rgba(108,179,62,.6)">Make an enquiry</a>
      <div class="mmenu__pills">
        <a class="mmenu__pill" href="tel:+4945140702000">Call Lübeck</a>
        <a class="mmenu__pill" href="mailto:hello@katech-solutions.com">E-mail</a>
      </div>
      <div class="mmenu__lang" role="group" aria-label="Language">
        <button type="button" data-lang="en" aria-current="true">EN</button>
        <button type="button" data-lang="de">DE</button>
        <button type="button" data-lang="pl">PL</button>
      </div>
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
    <div class="foot__demo">
      <b>Design preview.</b> This is an independent redesign concept for {ORT}, built by
      Dr.-Ing. Suat Akyol. It is not the official KaTech website and has no connection to it.
      All content and images are taken from the publicly available existing site.
      <a href="{pfad(root, "about-this-preview/")}">About this preview</a>
      <span class="demobar__sep">·</span>
      <a href="{ORIGINAL}" target="_blank" rel="noopener">Original site</a>
    </div>
    <div class="foot__grid">
      <div class="foot__brand">
        <img src="{root}media/logo-light.png" alt="{ORT}" width="420" height="120">
        <p>Bespoke stabilising and texturising solutions for the food industry.
        Developed in Lübeck, produced in Germany, the UK and Poland. Part of Ingredion.</p>
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
