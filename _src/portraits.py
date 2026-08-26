#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Laedt die Teamportraets der Bestandsseite und meldet ihre Abmessungen.

Die Portraets sind auf der Bestandsseite nicht im sichtbaren Inhalt zu sehen,
sondern nur als Vorschaubild fuer soziale Netzwerke im Kopf der jeweiligen
Profilseite hinterlegt (og:image)."""
import json, os, subprocess, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HERE, "_port")
os.makedirs(ZIEL, exist_ok=True)

quellen = json.load(open(os.path.join(HERE, "portraits.json"), encoding="utf-8"))
for slug, url in quellen.items():
    endung = os.path.splitext(url.split("?")[0])[1] or ".jpg"
    pfad = os.path.join(ZIEL, slug + endung)
    if os.path.exists(pfad):
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Chrome/126"})
        with urllib.request.urlopen(req, timeout=30) as r:
            open(pfad, "wb").write(r.read())
    except Exception as e:
        print("  FEHLER", slug, e)

dateien = sorted(os.listdir(ZIEL))
print(f"Geladen: {len(dateien)} von {len(quellen)}\n")
klein = 0
for d in dateien:
    aus = subprocess.run(["magick", "identify", "-format", "%wx%h %b",
                          os.path.join(ZIEL, d)], capture_output=True, text=True)
    masse = aus.stdout.strip()
    breite = int(masse.split("x")[0]) if "x" in masse else 0
    if breite < 300:
        klein += 1
    print(f"  {d:34s} {masse}")
print(f"\nUnter 300 Pixel breit: {klein} von {len(dateien)}")
