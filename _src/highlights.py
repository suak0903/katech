#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bereitet die sieben Motive des Bestands-Karussells auf.

Die Startseite der Bestandsseite fuehrt einen RoyalSlider mit sieben Folien.
Ein Karussell versteckt sechs von sieben Aussagen hinter Wartezeit; hier
laufen sie stattdessen als Band durch und sind alle gleichzeitig erreichbar.

Die Quellbilder tragen einen eingebrannten grauen Rahmen mit abgerundeten
Ecken, der weggeschnitten wird (Kit-Regel: sonst hat ein Bild einen Rahmen
und die anderen nicht).
"""
import os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
MEDIA = os.path.abspath(os.path.join(HERE, "..", "media"))
ESRGAN = r"C:\Users\suak\tools\realesrgan\realesrgan-ncnn-vulkan.exe"

# Quelle, Zielname, Rahmenbreite in Pixeln (0 = kein Rahmen)
MOTIVE = [
    ("up_plant-based-pilot-plant-385x248-1.png", "hl-pilot-plant", 7),
    ("up_ingredion-logo-385x248-1.png", "hl-ingredion", 0),
    ("kh_marcus-banner-385x248-1.png", "hl-development", 7),
    ("up_plant-based-block-385x248-1.png", "hl-plant-based", 7),
    ("up_video-banner-edited-pilot-plant-385x248-1.png", "hl-video", 7),
    ("kh_katech-food-technology-banner-2.png", "hl-allergen", 7),
    ("kh_brcgs-banner-green.png", "hl-quality", 7),
]


def main():
    for quelle, ziel, rahmen in MOTIVE:
        src = os.path.join(ASSETS, quelle)
        if not os.path.exists(src):
            print("  fehlt:", quelle)
            continue
        # 1. Rahmen abschneiden
        beschnitten = os.path.join(ASSETS, f"_hl_{ziel}.png")
        if rahmen:
            subprocess.run(["magick", src, "-shave", f"{rahmen}x{rahmen}",
                            "+repage", beschnitten], check=True)
        else:
            subprocess.run(["magick", src, "-background", "white", "-flatten",
                            beschnitten], check=True)
        # 2. Hochskalieren, die Quellen sind nur 385 Pixel breit
        gross = os.path.join(ASSETS, f"_hl4_{ziel}.png")
        if not os.path.exists(gross):
            subprocess.run([ESRGAN, "-i", beschnitten, "-o", gross,
                            "-n", "realesrgan-x4plus", "-s", "4"],
                           check=True, capture_output=True)
        # 3. Ausgabe in zwei Groessen: Band (560) und Lightbox (1200)
        for breite, endung, qualitaet in ((560, "webp", "82"), (560, "jpg", "85")):
            subprocess.run([
                "magick", gross, "-strip", "-resize", f"{breite}x{int(breite * 248 / 385)}^",
                "-gravity", "center", "-extent", f"{breite}x{int(breite * 248 / 385)}",
                "-quality", qualitaet, os.path.join(MEDIA, f"{ziel}.{endung}")], check=True)
        subprocess.run([
            "magick", gross, "-strip", "-resize", "1200x", "-quality", "84",
            os.path.join(MEDIA, f"{ziel}-gross.jpg")], check=True)
        kb = os.path.getsize(os.path.join(MEDIA, ziel + ".webp")) // 1024
        print(f"   {ziel:16s} {kb} KB")
    print("Motive in", MEDIA)


if __name__ == "__main__":
    main()
