#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt die Social-Vorschaubilder (1200x630 JPG) mit Marken-Lockup.
Kit-Regel: ein OG-Bild ist nie ein rohes Foto, sondern traegt Tint,
Logo und eine kurze Zeile."""
import os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.abspath(os.path.join(HERE, "..", "media"))
LOGO = os.path.join(MEDIA, "logo-light.png")

VARIANTEN = [
    ("og-home", "pilot-plant-wide", "Texture and stabilising solutions"),
    ("og-solutions", "sensory-panel", "Eleven product areas, one formulation team"),
    ("og-company", "hq-luebeck", "Lübeck, Cheshire, Reinfeld, Poznań"),
    ("og-expertise", "raw-materials", "Formulation knowledge and pilot plants"),
    ("og-preview", "lab-measurement", "Redesign preview by Dr.-Ing. Suat Akyol"),
    ("og-default", "blending-tower", "Bespoke solutions for the food industry"),
]


def bauen(name, quelle, zeile):
    src = os.path.join(MEDIA, quelle + ".jpg")
    ziel = os.path.join(MEDIA, name + ".jpg")
    if not os.path.exists(src):
        print("  Quelle fehlt:", quelle)
        return
    # 1. Foto auf 1200x630 beschneiden, abdunkeln, leichter Gruenstich unten
    subprocess.run([
        "magick", src, "-strip", "-resize", "1200x630^", "-gravity", "center",
        "-extent", "1200x630",
        "(", "-size", "1200x630", "gradient:none-#1d2a10", ")", "-compose", "over", "-composite",
        "-fill", "#373738", "-colorize", "38",
        ziel], check=True)
    # 2. Logo unten links einsetzen
    subprocess.run([
        "magick", ziel, "(", LOGO, "-resize", "300x", ")",
        "-gravity", "southwest", "-geometry", "+56+130", "-composite", ziel], check=True)
    # 3. Textzeile setzen
    subprocess.run([
        "magick", ziel, "-gravity", "southwest",
        "-font", os.path.join(HERE, "..", "font", "Barlow-600.woff2")
        if False else "Segoe-UI-Semibold",
        "-pointsize", "34", "-fill", "#ffffff",
        "-annotate", "+58+70", zeile,
        "-quality", "86", ziel], check=True)
    print("  ", name, os.path.getsize(ziel) // 1024, "KB")


for n, q, z in VARIANTEN:
    try:
        bauen(n, q, z)
    except subprocess.CalledProcessError as e:
        print("  FEHLER", n, e)
print("OG-Bilder in", MEDIA)
