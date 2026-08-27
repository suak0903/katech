#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Suats Punkte 4 bis 11: haben diese Produktseiten im Bestand wirklich kein Bild?

Geprueft wird nicht nur der Inhaltsbereich, sondern die ganze Seite, und es
wird ausserdem gezaehlt, was sonst darauf steht.
"""
import json, os, re, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROH = os.path.join(HERE, "raw")
RAHMEN = re.compile(r"(logo|icon|flags|sign-bg|brcgs|rspo|sedex|ifs|organic|foodchain|"
                    r"halal|kosher|esc|product-tab|banner-green|adobe_pdf)", re.I)

SEITEN = ["yogurt/fruited-yogurt", "yogurt/thermised-yogurt",
          "cream/vegetable-non-dairy", "cheese/cottage-cheese",
          "cheese/cottage-cheese-dressing", "cheese/quarg",
          "desserts/fruchtmousse", "milk-drinks/fruit-dairy-drinks",
          "milk-drinks/with-coffee", "dips/dips-with-sour-cream",
          "soups-and-sauces/chutney", "fruit/fruit-compotes", "fruit/torte-fillings"]

inhalt2 = json.load(open(os.path.join(HERE, "content2.json"), encoding="utf-8"))
daten = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))["seiten"]

print(f"{'Seite':34s} {'Bilder':>7s} {'Reiter':>7s} {'Absaetze':>9s}  Was auf der Seite steht")
print("-" * 108)
for slug in SEITEN:
    pfad = os.path.join(ROH, slug.replace("/", "_") + ".html")
    soup = BeautifulSoup(open(pfad, encoding="utf-8", errors="replace").read(), "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    alle = [i.get("src", "") for i in soup.find_all("img")
            if i.get("src") and not RAHMEN.search(i.get("src", ""))]
    echt = [b for b in alle if "/uploads/" in b or "khpartner" in b]
    reiter = len(inhalt2.get(slug, {}).get("reiter", {}))
    absaetze = len(daten.get(slug, {}).get("absaetze", []))
    bemerkung = "Text und die drei Beratungsreiter" if reiter else (
        "nur Text" if absaetze else "gar nichts")
    print(f"{slug:34s} {len(echt):7d} {reiter:7d} {absaetze:9d}  {bemerkung}")
    for b in echt:
        print(f"{'':34s} Bild: {b}")
