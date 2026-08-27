#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zweiter, gruendlicher Durchgang durch die Bestandsseiten.

Der erste Extraktor hat nur den Hauptbereich gelesen und dabei zwei Dinge
uebersehen, die Suat am 27.08. gefunden hat:

1. Jede Produktseite traegt unter der Beschreibung drei Reiter mit eigenem,
   produktspezifischem Text: New Product, Troubleshooting, Cost Optimisation.
   Sie liegen in den Containern #new_product, #troubleshooting und
   #cost_optimisation.
2. Bilder ausserhalb des Hauptbereichs, etwa im Kopfbereich der Seite.

Ergebnis: content2.json mit Beschreibung, Reitern und allen Bildern.
"""
import json, os, re, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROH = os.path.join(HERE, "raw")
BASE = "https://katech-solutions.com"

REITER = [("new_product", "New product"),
          ("troubleshooting", "Troubleshooting"),
          ("cost_optimisation", "Cost optimisation")]

RAHMEN = re.compile(r"(logo|icon|flags|sign-bg|brcgs|rspo|sedex|ifs|organic|foodchain|"
                    r"halal|kosher|esc|product-tab|banner-green|adobe_pdf)", re.I)


def bloecke(el):
    """Absaetze und Listenpunkte eines Containers, in Reihenfolge."""
    aus = []
    for kind in el.find_all(["p", "li", "h3", "h4"]):
        t = kind.get_text(" ", strip=True)
        if not t or t in ("Comments are closed.", "\xa0"):
            continue
        aus.append({"tag": kind.name, "text": t})
    return aus


ergebnis = {}
mit_reitern = 0

for datei in sorted(os.listdir(ROH)):
    if not datei.endswith(".html"):
        continue
    slug = datei[:-5].replace("_", "/")
    if slug == "home":
        slug = ""
    doc = open(os.path.join(ROH, datei), encoding="utf-8", errors="replace").read()
    soup = BeautifulSoup(doc, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()

    eintrag = {"slug": slug, "reiter": {}, "bilder": []}

    # --- Reiter --------------------------------------------------------
    for kennung, titel in REITER:
        c = soup.find(id=kennung)
        if not c:
            continue
        b = bloecke(c)
        if b:
            eintrag["reiter"][kennung] = {"titel": titel, "bloecke": b}
    if eintrag["reiter"]:
        mit_reitern += 1

    # --- Bilder, ueberall auf der Seite --------------------------------
    gesehen = set()
    for im in soup.find_all("img"):
        src = im.get("src") or ""
        if not src or RAHMEN.search(src):
            continue
        if "/wp-content/uploads/" not in src and "khpartner" not in src:
            continue
        if src.startswith("/"):
            src = BASE + src
        if src in gesehen:
            continue
        gesehen.add(src)
        eintrag["bilder"].append({"src": src, "alt": im.get("alt", ""),
                                  "eltern": (im.parent.get("id") or
                                             " ".join(im.parent.get("class") or []))[:40]})

    # --- Verweise auf Dateien -----------------------------------------
    eintrag["dateien"] = [a.get("href") for a in soup.find_all("a", href=True)
                          if re.search(r"\.(pdf|docx?|xlsx?)$", a.get("href", ""), re.I)]

    ergebnis[slug] = eintrag

json.dump(ergebnis, open(os.path.join(HERE, "content2.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

mit_bildern = sum(1 for e in ergebnis.values() if e["bilder"])
mit_dateien = sum(1 for e in ergebnis.values() if e["dateien"])
print(f"Seiten untersucht:      {len(ergebnis)}")
print(f"davon mit Reitern:      {mit_reitern}")
print(f"davon mit Bildern:      {mit_bildern}")
print(f"davon mit Dateiverweis: {mit_dateien}")
