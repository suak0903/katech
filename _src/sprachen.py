#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Welche Seiten gibt es auf Deutsch und Polnisch, und in welchem Zustand?

Fuer die Ampel in der Sitemap. Fuer jede englische Seite wird geprueft:

  gruen  Uebersetzung vorhanden und inhaltlich vergleichbar lang
  gelb   vorhanden, aber deutlich duenner als das Englische oder fast leer
  rot    nicht vorhanden

Die Uebersetzungen tragen eigene Adressen - aus /yogurt/ wird /de/joghurt/
und /pl/jogurty/. Ein Vergleich ueber den Slug ginge deshalb ins Leere; die
Zuordnung steht als hreflang im Kopf jeder englischen Seite.

Gemessen wird die Textmenge im Inhaltsbereich, nicht das blosse Vorhandensein
einer Adresse: eine Seite, die nur eine Ueberschrift traegt, ist keine
Uebersetzung.
"""
import json, os, re, sys, time, urllib.error, urllib.request
from collections import Counter
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASIS = "https://katech-solutions.com"
KOPF = {"User-Agent": "Mozilla/5.0"}

WEG_IDS = ["top-nav-container", "colophon", "pre-footer", "header", "comments",
           "enquiry-form", "fade-dialog", "cmplz-cookiebanner-container"]
WEG_KLASSEN = ["sidebar__menu", "header-fixed", "mobile__burger", "logos-social",
               "cmplz-cookiebanner", "language__selector--desktop",
               "language__selector--mobile"]


def hole(url, versuche=3):
    for n in range(versuche):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers=KOPF), timeout=30) as a:
                return a.getcode(), a.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as f:
            if f.code == 404:
                return 404, ""
            time.sleep(2 + n * 3)
        except Exception:
            time.sleep(2 + n * 3)
    return 0, ""


def textmenge(html):
    """Zeichen im Inhaltsbereich, ohne Rahmen und Menue."""
    if not html:
        return 0
    suppe = BeautifulSoup(html, "lxml")
    for t in suppe(["script", "style", "noscript"]):
        t.decompose()
    for i in WEG_IDS:
        for e in suppe.find_all(id=i):
            e.decompose()
    for k in WEG_KLASSEN:
        for e in suppe.select("." + k):
            e.decompose()
    inhalt = suppe.find(id="content") or suppe.body
    return len(re.sub(r"\s+", " ", inhalt.get_text(" ", strip=True))) if inhalt else 0


def uebersetzungen(html):
    """Die hreflang-Verweise aus dem Kopf einer englischen Seite."""
    gefunden = {}
    for sprache, adresse in re.findall(
            r'<link[^>]*hreflang="([^"]+)"[^>]*href="([^"]+)"', html):
        kurz = sprache.split("-")[0]
        if kurz in ("de", "pl"):
            gefunden[kurz] = adresse
    return gefunden


daten = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))["seiten"]
englisch = sorted(s for s in daten if s)
print(f"Englische Seiten zu pruefen: {len(englisch)}\n")

ergebnis = {}
for n, slug in enumerate(englisch, 1):
    en_menge = len(re.sub(r"\s+", " ", " ".join(daten[slug].get("absaetze", []) or [])))
    eintrag = {"en_zeichen": en_menge, "adressen": {}}

    code, html = hole(f"{BASIS}/{slug}/")
    ziele = uebersetzungen(html) if code == 200 else {}

    for sprache in ("de", "pl"):
        if sprache not in ziele:
            eintrag[sprache] = {"stand": "fehlt", "zeichen": 0}
            continue
        eintrag["adressen"][sprache] = ziele[sprache].replace(BASIS, "")
        code2, html2 = hole(ziele[sprache])
        menge = textmenge(html2)
        # Der Rahmen bringt selbst etwas Text mit; darunter ist nichts da
        if code2 != 200 or menge < 220:
            stand = "leer"
        elif en_menge > 0 and menge < en_menge * 0.55:
            stand = "duenn"
        else:
            stand = "gut"
        eintrag[sprache] = {"stand": stand, "zeichen": menge}
        time.sleep(0.3)

    ergebnis[slug] = eintrag
    time.sleep(0.25)
    if n % 25 == 0:
        print(f"  {n} von {len(englisch)} geprueft")

json.dump(ergebnis, open(os.path.join(HERE, "sprachen.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print()
for sprache in ("de", "pl"):
    z = Counter(e[sprache]["stand"] for e in ergebnis.values())
    print(f"{sprache.upper()}: gut {z['gut']}, duenn {z['duenn']}, "
          f"leer {z['leer']}, fehlt {z['fehlt']}")
