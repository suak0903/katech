#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Die Zertifikat- und Policy-Dokumente des Bestands ins Repo holen.

Der Bestand verlinkt auf der RSPO-Seite und unter Certifications sechs
Dokumente. Im Entwurf fehlten sie (Suat 27.08., Punkt 16). Sie werden
lokal abgelegt und direkt angezeigt, statt auf die alte Domain zu zeigen.
"""
import os, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ZIEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
BASIS = "https://katech-solutions.com/wp-content/uploads/"

DOKUMENTE = {
    "katech-rspo-2026.pdf": BASIS + "2026/04/katech-ingredient-solutions-gmbh-rspo-2026.pdf",
    "katech-brcgs-2027.pdf": BASIS + "2026/04/katech-brc-certificate-exp-25-04-2027.pdf",
    "katech-ifs-2027.pdf": BASIS + "2026/04/katech-ifs-certificate-exp-30-04-2027.pdf",
    "katech-non-gmo-2026.pdf": BASIS + "2026/01/3-katech-ingredient-solutions-gmbh-ngmo-certificate-2025-2026.pdf",
    "katech-sedex-smeta-2021.pdf": "https://www.khpartner.com/wp-content/uploads/2022/01/sedex-audit-smeta-2021.pdf",
    "katech-organic-2023.pdf": BASIS + "2023/04/ka-tech-ingrediant-solutions-2023-en.pdf",
}

os.makedirs(ZIEL, exist_ok=True)
for name, url in DOKUMENTE.items():
    pfad = os.path.join(ZIEL, name)
    if os.path.exists(pfad) and os.path.getsize(pfad) > 1000:
        print(f"{name:34s} liegt schon vor")
        continue
    try:
        anfrage = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        rohdaten = urllib.request.urlopen(anfrage, timeout=40).read()
        if not rohdaten.startswith(b"%PDF"):
            print(f"{name:34s} kein PDF ({len(rohdaten)} Bytes)")
            continue
        open(pfad, "wb").write(rohdaten)
        print(f"{name:34s} geladen, {len(rohdaten):8d} Bytes")
    except Exception as fehler:
        print(f"{name:34s} FEHLER: {fehler}")
