#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genaue Zahlen zu den drei Sprachbaeumen des Bestands.

Grundlage fuer die Angaben auf der Vorschau-Seite. Anhangseiten zaehlen
nicht mit: das sind WordPress-Medienseiten ohne eigenen Inhalt.
"""
import re, sys, time, urllib.error, urllib.request
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
BASIS = "https://katech-solutions.com"


def hole(url):
    for versuch in range(3):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                timeout=30).read().decode("utf-8", "replace")
        except urllib.error.HTTPError as f:
            if f.code != 503:
                return None
            time.sleep(3 + versuch * 4)
        except Exception:
            return None
    return None


def sprache(weg):
    erstes = weg.split("/")[0] if weg else ""
    return erstes if erstes in ("de", "pl") else "en"


gesamt = Counter()
for karte, art in (("page-sitemap.xml", "Seiten"), ("post-sitemap.xml", "Beitraege")):
    roh = hole(BASIS + "/" + karte)
    wege = [a.replace(BASIS, "").strip("/") for a in re.findall(r"<loc>([^<]+)</loc>", roh)]
    z = Counter(sprache(w) for w in wege)
    print(f"{art:10s} en {z['en']:4d}   de {z['de']:4d}   pl {z['pl']:4d}   "
          f"gesamt {sum(z.values()):4d}")
    gesamt.update(z)
    time.sleep(0.6)

print("-" * 58)
print(f"{'Summe':10s} en {gesamt['en']:4d}   de {gesamt['de']:4d}   pl {gesamt['pl']:4d}   "
      f"gesamt {sum(gesamt.values()):4d}")
print()
print("Anhangseiten (WordPress-Medienseiten, kein eigener Inhalt): 1471")
print("Kategorie- und Autorenseiten:                                 31")
