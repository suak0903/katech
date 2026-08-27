#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft nach dem Deploy, ob die Aenderungen dieser Runde live sind."""
import sys, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASIS = "https://suak0903.github.io/katech/"

PRUEFUNGEN = [
    ("yogurt/drinking-yogurt/", "wege__w", "Reiter auf der Produktseite"),
    ("privacy-policy/", "prose--legal", "Privacy policy vollstaendig"),
    ("certifications/rspo/", "cert-rspo-2026-p1", "RSPO-Zertifikat sichtbar"),
    ("certifications/", "katech-ifs-2027.pdf", "Zertifikatsdokumente verlinkt"),
    ("docs/katech-rspo-2026.pdf", None, "PDF erreichbar"),
    ("soups/freshpasteurised/", "Soups and sauces", "Breadcrumb umgehaengt"),
    ("case-studies/", "Company", "Case studies unter Company"),
    ("sitemap/", "sm__mk", "Sitemap-Marken"),
]

for pfad, erwartet, was in PRUEFUNGEN:
    url = BASIS + pfad
    zustand = "FEHLER"
    for versuch in range(3):
        try:
            antwort = urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
            roh = antwort.read()
            if erwartet is None:
                zustand = "ok" if roh.startswith(b"%PDF") else "kein PDF"
            else:
                zustand = "ok" if erwartet in roh.decode("utf-8", "replace") else "NICHT GEFUNDEN"
            break
        except Exception as fehler:
            zustand = str(fehler)[:40]
            time.sleep(4)
    print(f"  {was:34s} {zustand}")
