#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wie gross sind der deutsche und der polnische Baum der Bestandsseite?

Fuer eine ehrliche Angabe auf der Vorschau-Seite: der Entwurf bildet den
englischen Baum ab, die anderen beiden nicht (Suat 27.08.).
"""
import re, sys, time, urllib.error, urllib.request

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


roh = hole(BASIS + "/sitemap_index.xml") or hole(BASIS + "/wp-sitemap.xml")
if not roh:
    print("Keine Sitemap abrufbar")
    raise SystemExit

karten = re.findall(r"<loc>([^<]+)</loc>", roh)
print(f"Teilkarten: {len(karten)}")

adressen = set()
for k in karten:
    if not k.endswith(".xml"):
        adressen.add(k)
        continue
    teil = hole(k)
    if teil:
        adressen.update(re.findall(r"<loc>([^<]+)</loc>", teil))
    time.sleep(0.5)

zaehler = {"en": 0, "de": 0, "pl": 0}
for a in adressen:
    weg = a.replace(BASIS, "").strip("/")
    erstes = weg.split("/")[0] if weg else ""
    if erstes == "de":
        zaehler["de"] += 1
    elif erstes == "pl":
        zaehler["pl"] += 1
    else:
        zaehler["en"] += 1

print(f"\nAdressen in der Sitemap des Bestands: {len(adressen)}")
for k, v in zaehler.items():
    print(f"  {k}: {v}")
