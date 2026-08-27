#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Was steckt in den 1996 Adressen der Bestands-Sitemap?

Die Zahl klang zu hoch fuer 159 Inhaltsseiten. Diese Auswertung trennt
Inhaltsseiten von Anhangseiten, Kategorien und Ahnlichem, damit die
Angabe auf der Vorschau-Seite stimmt (Suat 27.08.).
"""
import json, os, re, sys, time, urllib.error, urllib.request
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
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


roh = hole(BASIS + "/sitemap_index.xml")
karten = re.findall(r"<loc>([^<]+)</loc>", roh)
nach_karte = {}
for k in karten:
    teil = hole(k) if k.endswith(".xml") else None
    adressen = set(re.findall(r"<loc>([^<]+)</loc>", teil)) if teil else set()
    nach_karte[k.split("/")[-1]] = adressen
    print(f"  {k.split('/')[-1]:34s} {len(adressen):5d}")
    time.sleep(0.5)

alle = set().union(*nach_karte.values()) if nach_karte else set()
sprache = Counter()
for a in alle:
    weg = a.replace(BASIS, "").strip("/")
    erstes = weg.split("/")[0] if weg else ""
    sprache[erstes if erstes in ("de", "pl") else "en"] += 1

print(f"\nInsgesamt {len(alle)} Adressen: " +
      ", ".join(f"{k} {v}" for k, v in sorted(sprache.items())))

# Wie viele davon sind Inhaltsseiten? Der Entwurf bildet den page-Baum ab.
seiten_karte = [n for n in nach_karte if n.startswith("page-")]
if seiten_karte:
    p = nach_karte[seiten_karte[0]]
    en = {a.replace(BASIS, "").strip("/") for a in p
          if not a.replace(BASIS, "").strip("/").startswith(("de/", "pl/"))}
    eigene = {s for s in json.load(open(os.path.join(HERE, "data.json"),
                                        encoding="utf-8"))["seiten"] if s}
    print(f"\nEnglische Seiten in der Seiten-Karte: {len(en)}")
    print(f"Davon im Entwurf:                     {len(en & eigene)}")
    fehlt = sorted(en - eigene)
    print(f"Nicht im Entwurf:                     {len(fehlt)}")
    for f in fehlt[:40]:
        print(f"    {f}")
