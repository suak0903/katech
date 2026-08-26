#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bausteine des Seiten-Generators: Seitenrahmen mit Kopfdaten und JSON-LD
sowie die wiederkehrenden Sektionsmuster (Hero, Split-Block, Kartenraster,
Kennzahlen, Prozessschritte, Galerie)."""
import html, json, os, re

import gen_chrome as chrome

VERSION = 14  # Cache-Busting: bei jeder Aenderung an css/js erhoehen
PAGES_URL = "https://suak0903.github.io/katech/"
ORIGINAL = "https://katech-solutions.com/"
ORT = "KaTech Ingredient Solutions"


def normalisieren(t):
    """Typografie angleichen: keine Gedankenstriche in Fliesstext (Hausregel),
    keine typografischen Sonderformen aus dem Bestandstext."""
    t = str(t)
    t = t.replace("—", " - ").replace("–", " - ")
    t = t.replace("‘", "'").replace("’", "'")
    t = t.replace("“", '"').replace("”", '"')
    t = t.replace("…", "...")
    t = re.sub(r"\s+-\s+", " - ", t)
    return re.sub(r"[ 	]{2,}", " ", t)


def esc(t):
    return html.escape(normalisieren(t), quote=False)


def wurzel(zielpfad):
    """Relativer Pfad zum Site-Root fuer eine Seite wie 'vegan/index.html'."""
    tiefe = zielpfad.count("/")
    return "../" * tiefe if tiefe else ""


def kanonisch(zielpfad):
    """Canonical zeigt auf die Original-Domain (Demonstrator-Regel)."""
    p = zielpfad.replace("index.html", "").replace(".html", "/")
    return ORIGINAL + p.lstrip("/")


def og_bild(root, name):
    return PAGES_URL + "media/" + name


def seite(zielpfad, titel, beschreibung, inhalt, *, aktiv="", solid=False,
          og="og-default.jpg", jsonld=None, extra_head="", body_klasse=""):
    root = wurzel(zielpfad)
    v = f"?v={VERSION}"
    ld = ""
    if jsonld:
        ld = ('\n<script type="application/ld+json">'
              + normalisieren(json.dumps(jsonld, ensure_ascii=False, indent=1)) + "</script>")
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titel)} | {ORT}</title>
<meta name="description" content="{esc(beschreibung)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{kanonisch(zielpfad)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="{ORT}">
<meta property="og:title" content="{esc(titel)}">
<meta property="og:description" content="{esc(beschreibung)}">
<meta property="og:image" content="{og_bild(root, og)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{PAGES_URL}{zielpfad.replace("index.html", "")}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(titel)}">
<meta name="twitter:description" content="{esc(beschreibung)}">
<meta name="twitter:image" content="{og_bild(root, og)}">
<meta name="theme-color" content="#373738">
<link rel="icon" href="{root}media/favicon.ico" sizes="any">
<link rel="icon" href="{root}media/favicon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{root}media/apple-touch-icon.png">
<link rel="preload" href="{root}font/Barlow-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}font/OpenSans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}css/site.css{v}">{extra_head}{ld}
</head>
<body{f' class="{body_klasse}"' if body_klasse else ''}>
<a class="skip" href="#main">Skip to content</a>
{chrome.kopf(root, aktiv=aktiv, solid=solid)}
<main id="main">
{inhalt}
</main>
{chrome.fuss(root)}
{chrome.demoleiste(root)}
{chrome.consent(root)}
<script src="{root}js/site.js{v}" defer></script>
</body>
</html>
'''


# --------------------------------------------------------------------------
# Sektionsbausteine
# --------------------------------------------------------------------------

PFEIL = ('<svg width="15" height="11" viewBox="0 0 15 11" fill="none" aria-hidden="true">'
         '<path d="M9.2 0.6 14 5.4l-4.8 4.8M14 5.4H0.5" stroke="currentColor" stroke-width="1.8"/></svg>')


def hero_preload(root, bild):
    """Preload des LCP-Bildes. URL, Typ und srcset muessen exakt dem
    picture-Element entsprechen, sonst laedt der Browser zweimal."""
    return ('\n<link rel="preload" as="image" type="image/webp" fetchpriority="high"'
            ' imagesizes="100vw"'
            ' imagesrcset="' + srcset(root, bild, "webp") + '"'
            ' href="' + root + 'media/' + bild + '-1400.webp">')


HERO_STUFEN = (800, 1400, 2000, 2400)


def srcset(root, bild, endung):
    return ", ".join(f"{root}media/{bild}-{b}.{endung} {b}w" for b in HERO_STUFEN)


def hero(root, *, eyebrow, h1, sub, bild, cta=None, ribbon=None, alt=""):
    knoepfe = ""
    if cta:
        teile = "".join(f'<a class="btn {k}" href="{z}">{t}</a>' for t, z, k in cta)
        knoepfe = f'<div class="btn-row{" btn-row--single" if len(cta) == 1 else ""}">{teile}</div>'
    band = ""
    if ribbon:
        zellen = "".join(f"<div><b>{esc(w)}</b><span>{esc(l)}</span></div>" for w, l in ribbon)
        band = f'<div class="hero__ribbon"><div class="wrap">{zellen}</div></div>'
    return f'''<section class="hero">
  <div class="hero__bg" id="heroBg">
    <picture>
      <source type="image/webp" sizes="100vw" srcset="{srcset(root, bild, "webp")}">
      <source type="image/jpeg" sizes="100vw" srcset="{srcset(root, bild, "jpg")}">
      <img src="{root}media/{bild}-1400.jpg" alt="{esc(alt)}" width="2400" height="1029"
           loading="eager" fetchpriority="high" decoding="sync">
    </picture>
  </div>
  <div class="hero__scrim"></div>
  <div class="hero__inner">
    <div class="hero__copy">
      <p class="eyebrow">{esc(eyebrow)}</p>
      <h1>{h1}</h1>
      <p class="hero__sub">{esc(sub)}</p>
      {knoepfe}
    </div>
  </div>
</section>
{band}'''



def subhero(root, *, crumbs, h1, sub="", eyebrow="", bild=None, alt=""):
    weg = []
    for i, (t, z) in enumerate(crumbs):
        if z:
            weg.append(f'<a href="{z}">{esc(t)}</a>')
        else:
            weg.append(f"<span>{esc(t)}</span>" if i < len(crumbs) - 1 else esc(t))
    pfad_html = '<span aria-hidden="true">/</span>'.join(weg)
    hg = ""
    if bild:
        hg = (f'<div class="subhero__bg" id="subheroBg"><picture>'
              f'<source srcset="{root}media/{bild}.webp" type="image/webp">'
              f'<img src="{root}media/{bild}.jpg" alt="{esc(alt)}" loading="lazy" decoding="async">'
              f'</picture></div>')
    eb = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    su = f'<p class="subhero__sub">{esc(sub)}</p>' if sub else ""
    return f'''<section class="subhero">
  {hg}
  <div class="subhero__inner">
    <nav class="crumbs" aria-label="Breadcrumb">{pfad_html}</nav>
    {eb}
    <h1>{h1}</h1>
    {su}
  </div>
</section>'''


def split(root, *, ton, eyebrow, h2, text, bild, alt="", liste=None, cta=None, flip=False):
    punkte = ""
    if liste:
        punkte = '<ul class="split__list">' + "".join(f"<li>{esc(x)}</li>" for x in liste) + "</ul>"
    knopf = ""
    if cta:
        t, z = cta
        knopf = f'<div class="btn-row btn-row--single"><a class="btn btn--ghost" href="{z}">{esc(t)}</a></div>'
    absaetze = "".join(f"<p>{esc(t)}</p>" for t in (text if isinstance(text, list) else [text]))
    return f'''<section class="split{" split--flip" if flip else ""} rv">
  <div class="split__pane split__pane--{ton}">
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h2>{h2}</h2>
    {absaetze}
    {punkte}
    {knopf}
  </div>
  <div class="split__media">
    <picture>
      <source srcset="{root}media/{bild}.webp" type="image/webp">
      <img src="{root}media/{bild}.jpg" alt="{esc(alt)}" loading="lazy" decoding="async">
    </picture>
  </div>
</section>'''


def sec_kopf(*, eyebrow="", h2="", lead="", zentriert=False):
    eb = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    hd = f"<h2>{h2}</h2>" if h2 else ""
    ld = f'<p class="lead">{esc(lead)}</p>' if lead else ""
    k = "sec__head sec__head--center" if zentriert else "sec__head"
    return f'<div class="{k}">{eb}{hd}{ld}</div>'


def karte(root, *, titel, text, ziel, bild=None, zusatz="", mehr="Read more"):
    medien = ""
    if bild:
        medien = f'''<div class="card__media">
      <picture>
        <source srcset="{root}media/{bild}.webp" type="image/webp">
        <img src="{root}media/{bild}.jpg" alt="{esc(titel)}" loading="lazy" decoding="async" width="800" height="533">
      </picture>
    </div>'''
    zu = f'<span class="card__count">{esc(zusatz)}</span>' if zusatz else ""
    return f'''<a class="card" href="{ziel}">
    {medien}
    <div class="card__body">
      {zu}
      <h3>{esc(titel)}</h3>
      <p>{esc(text)}</p>
      <span class="card__more">{esc(mehr)} {PFEIL}</span>
    </div>
  </a>'''


def kachel(*, nummer, titel, text, ziel):
    return f'''<a class="tile" href="{ziel}">
    <span class="tile__num">{esc(nummer)}</span>
    <h3>{esc(titel)}</h3>
    <p>{esc(text)}</p>
  </a>'''


def raster(karten, spalten=3):
    return f'<div class="grid grid--{spalten} rv">' + "\n  ".join(karten) + "</div>"


def stats(werte):
    zellen = "".join(f"<div><b>{esc(w)}</b><span>{esc(l)}</span></div>" for w, l in werte)
    return f'<div class="stats rv">{zellen}</div>'


def schritte(eintraege):
    li = "".join(
        f'<li><span class="steps__num">{esc(n)}</span><h3>{esc(t)}</h3><p>{esc(x)}</p></li>'
        for n, t, x in eintraege)
    return f'<ol class="steps rv">{li}</ol>'


def galerie(root, bilder):
    knoepfe = "".join(
        f'''<button type="button" aria-label="Enlarge: {esc(a)}">
      <picture><source srcset="{root}media/{b}.webp" type="image/webp">
      <img src="{root}media/{b}.jpg" alt="{esc(a)}" loading="lazy" decoding="async" width="800" height="533"></picture>
    </button>''' for b, a in bilder)
    return f'''<div class="gallery rv">{knoepfe}</div>
<div class="lb" id="lb" hidden>
  <button class="lb__close" type="button" aria-label="Close">&times;</button>
  <button class="lb__prev" type="button" aria-label="Previous">&#8249;</button>
  <img src="" alt="">
  <button class="lb__next" type="button" aria-label="Next">&#8250;</button>
  <span class="lb__count"></span>
</div>'''


def zertifikate(root, eintraege):
    imgs = "".join(
        f'<img src="{root}media/{b}" alt="{esc(a)}" loading="lazy" decoding="async">'
        for b, a in eintraege)
    return f'<div class="certs rv">{imgs}</div>'


def prosa(bloecke):
    return '<div class="prose rv">' + "".join(bloecke) + "</div>"


def absatz(t):
    return f"<p>{esc(t)}</p>"


def faktenkasten(titel, punkte):
    li = "".join(f"<li>{esc(p)}</li>" for p in punkte)
    return f'<div class="factbox"><h3>{esc(titel)}</h3><ul>{li}</ul></div>'
