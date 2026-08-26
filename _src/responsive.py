#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt die Groessenstufen des Hero-Bildes und verkleinert die Logodateien.
Ohne srcset laedt ein Telefon dasselbe 2400-Pixel-Bild wie ein grosser Monitor;
das war der groesste Posten im Ladeprofil."""
import os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
MEDIA = os.path.abspath(os.path.join(HERE, "..", "media"))

STUFEN = [800, 1400, 2000, 2400]
QUELLE = os.path.join(ASSETS, "_up_pilot-plant.png")


def hero_stufen():
    for breite in STUFEN:
        hoehe = int(breite * 9 / 21)
        for endung, q in (("webp", "80"), ("jpg", "84")):
            ziel = os.path.join(MEDIA, f"pilot-plant-wide-{breite}.{endung}")
            subprocess.run([
                "magick", QUELLE, "-strip", "-auto-orient",
                "-resize", f"{breite}x{hoehe}^", "-gravity", "center",
                "-extent", f"{breite}x{hoehe}", "-quality", q, ziel], check=True)
        kb = os.path.getsize(os.path.join(MEDIA, f"pilot-plant-wide-{breite}.webp")) // 1024
        print(f"   pilot-plant-wide-{breite}: {kb} KB (webp)")


def logos():
    # Das Logo wird mit 44 Pixel Hoehe dargestellt; 420 Pixel Breite sind Ballast.
    for name in ("logo-light", "logo-dark"):
        src = os.path.join(ASSETS, "_logo_light.png" if name == "logo-light" else "_logo_trans.png")
        ziel = os.path.join(MEDIA, name + ".png")
        subprocess.run(["magick", src, "-strip", "-resize", "260x",
                        "-define", "png:compression-level=9", ziel], check=True)
        print(f"   {name}: {os.path.getsize(ziel) // 1024} KB")


if __name__ == "__main__":
    print("Hero-Groessenstufen ...")
    hero_stufen()
    print("Logos ...")
    logos()
