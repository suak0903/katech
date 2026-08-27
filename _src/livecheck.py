#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft nach dem Deploy, ob die Aenderungen dieser Runde live sind."""
import sys, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASIS = "https://suak0903.github.io/katech/"

PRUEFUNGEN = [
    ("yogurt/drinking-yogurt/", "tabs__bar", "Reiter als Tabs"),
    ("vegan/", "Vegan solutions", "Bereichsseite heisst Vegan solutions"),
    ("solutions/", "subhero__cta", "Weg zur Vegan-Seite im Hero"),
    ("solutions/", 'id="plant"', "Anker fuer Plant-based"),
    ("privacy-policy/", "prose--legal", "Privacy policy vollstaendig"),
    ("certifications/rspo/", "cert-rspo-2026-p1", "RSPO-Zertifikat sichtbar"),
    ("certifications/", "katech-ifs-2027.pdf", "Zertifikatsdokumente verlinkt"),
    ("docs/katech-rspo-2026.pdf", None, "PDF erreichbar"),
    ("soups/freshpasteurised/", "Soups and sauces", "Breadcrumb umgehaengt"),
    ("sitemap/", "sm__mk", "Sitemap-Marken"),
    ("case-studies/", "Expertise", "Case studies unter Expertise"),
    ("about-this-preview/", "all 201 are in this preview", "Abdeckung benannt"),
    ("yogurt/drinking-yogurt/", "BreadcrumbList", "Breadcrumb-Markup"),
    ("yogurt/drinking-yogurt/", "data-lb", "Produktbild vergroesserbar"),
    ("cyril-carrat/", "zoom--portraet", "Portraet vergroesserbar"),
    ("about-this-preview/", "ref__link", "Referenzbilder verlinkt"),
    ("media/refs/cancontrols.jpg", None, "Referenzbild als JPG"),
    ("technical-development-suite-germany/", 'id="address"', "Adresse auf der Standortseite"),
    ("find-us/", "loc__mehr", "Find us fuehrt zu den Standorten"),
    ("find-us/katech-uk/", "technical-development-suite-uk", "alte Adresse leitet weiter"),
    ("our-facilities/", "weiter__t", "Facilities mit Verweisstreifen"),
    ("sitemap/", "sm__mk--um", "Sitemap kennzeichnet Weiterleitungen"),
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
                # Datei statt Seite: nur pruefen, dass echte Daten kommen
                anfang = (b"%PDF", b"\xff\xd8\xff", b"RIFF", b"\x89PNG")
                zustand = ("ok" if roh.startswith(anfang) and len(roh) > 2000
                           else f"unerwarteter Inhalt ({len(roh)} Bytes)")
            else:
                zustand = "ok" if erwartet in roh.decode("utf-8", "replace") else "NICHT GEFUNDEN"
            break
        except Exception as fehler:
            zustand = str(fehler)[:40]
            time.sleep(4)
    print(f"  {was:34s} {zustand}")
