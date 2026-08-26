#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skaliert die gross ausgespielten Food-Motive hoch (Split-Bloecke und
Bereichsbilder), damit sie bei halber Bildschirmbreite nicht weich wirken.
Die Bestandsbilder liegen nur mit 432 bis 460 Pixel Breite vor."""
import os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
MEDIA = os.path.abspath(os.path.join(HERE, "..", "media"))
ESRGAN = r"C:\Users\suak\tools\realesrgan\realesrgan-ncnn-vulkan.exe"

# Quelle in assets/ -> Zielname in media/ (ohne Endung), Seitenverhaeltnis
GROSS = [
    ("up_plant-based-meat-balls-2.jpg", "p-vegan-plant-based-mince", (4, 3)),
    ("up_vegan-burger.jpg", "p-vegan-plant-based-burger-patties", (4, 3)),
    ("up_vegan-yogurt.jpg", "p-vegan-vegan-yogurt", (4, 3)),
    ("up_vegan-cheese-substitute.jpg", "p-vegan-vegan-cheese-alternatives", (4, 3)),
    ("up_vegan-desserts.jpg", "p-vegan-vegan-desserts", (4, 3)),
    ("kh_cheese-heading.jpg", "p-cheese", (4, 3)),
    ("up_1st-food-1576.jpg", "p-cheese-cream-cheese", (4, 3)),
    ("kh_yogurt.jpg", "p-yogurt", (4, 3)),
    ("kh_mayonnaise.jpg", "p-mayonnaise", (4, 3)),
    ("kh_cream.jpg", "p-cream", (4, 3)),
    ("kh_milk-drinks.jpg", "p-milk-drinks", (4, 3)),
    ("kh_bakery-1820-745.jpg", "p-bakery", (4, 3)),
    ("up_IMG_0069.jpg", "p-soups-freshpasteurised", (4, 3)),
]


def main():
    for quelle, ziel, (w, h) in GROSS:
        src = os.path.join(ASSETS, quelle)
        if not os.path.exists(src):
            print("  fehlt:", quelle)
            continue
        gross = os.path.join(ASSETS, "_up4_" + ziel + ".png")
        if not os.path.exists(gross):
            subprocess.run([ESRGAN, "-i", src, "-o", gross, "-n", "realesrgan-x4plus", "-s", "4"],
                           check=True, capture_output=True)
        breite = 1400
        hoehe = int(breite * h / w)
        for endung, qualitaet in (("webp", "82"), ("jpg", "85")):
            subprocess.run([
                "magick", gross, "-strip", "-auto-orient",
                "-resize", f"{breite}x{hoehe}^", "-gravity", "center",
                "-extent", f"{breite}x{hoehe}", "-quality", qualitaet,
                os.path.join(MEDIA, f"{ziel}.{endung}")], check=True)
        print("  ", ziel)
    print("Fertig.")


if __name__ == "__main__":
    main()
