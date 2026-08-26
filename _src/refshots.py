#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nimmt Startseiten-Screenshots der Referenzprojekte fuer die Referenz-Riege
der Hinweisseite auf (Edge headless) und schneidet sie auf 640x400 WebP zu."""
import os, subprocess, sys, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.abspath(os.path.join(HERE, "..", "media", "refs"))
TMP = os.path.join(HERE, "_shots")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
os.makedirs(ZIEL, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

REFS = [
    ("akyol", "https://www.akyol.de"),
    ("coreform", "https://www.core-form.de"),
    ("barista", "https://barista-biker.de/"),
    ("cancontrols", "https://suak0903.github.io/cancontrols/"),
    ("seitec", "https://suak0903.github.io/seitec/"),
    ("msrodenkirchen", "https://suak0903.github.io/ms-rodenkirchen/"),
]

for key, url in REFS:
    # Erreichbarkeit pruefen, tote Links auf einer Pitch-Seite sind peinlich
    status = "?"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Chrome/126"},
                                     method="GET")
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
    except Exception as e:
        status = f"FEHLER {e}"
    png = os.path.join(TMP, key + ".png")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--window-size=1366,854", "--virtual-time-budget=11000",
                    f"--user-data-dir={TMP}\\ud-{key}", f"--screenshot={png}", url],
                   capture_output=True)
    for _ in range(10):
        if os.path.exists(png) and os.path.getsize(png) > 4000:
            break
        time.sleep(1)
    if not os.path.exists(png):
        print(f"  {key}: kein Screenshot (HTTP {status})")
        continue
    subprocess.run(["magick", png, "-strip", "-resize", "640x", "-gravity", "north",
                    "-crop", "640x400+0+0", "+repage", "-quality", "80",
                    os.path.join(ZIEL, key + ".webp")], check=True)
    print(f"  {key}: HTTP {status}, Screenshot ok")

print("Referenzbilder in", ZIEL)
