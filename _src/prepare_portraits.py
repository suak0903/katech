#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bereitet die 23 Teamportraets auf.

Die Bestandsseite haelt sie nur als 140x140 grosse Vorschaubilder vor; die
Originale sind nicht mehr abrufbar. Sie werden deshalb hochskaliert und
quadratisch ausgegeben. Die Schwarzweiss-Anmutung bleibt, sie ist bei allen
23 Aufnahmen gleich und passt zur zurueckhaltenden Bildsprache der Seite."""
import json, os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
QUELLE = os.path.join(HERE, "_port")
MEDIA = os.path.abspath(os.path.join(HERE, "..", "media"))
ESRGAN = r"C:\Users\suak\tools\realesrgan\realesrgan-ncnn-vulkan.exe"

manifest = {}
for datei in sorted(os.listdir(QUELLE)):
    slug = os.path.splitext(datei)[0]
    src = os.path.join(QUELLE, datei)
    # Drei Aufnahmen liegen als PNG mit Transparenz vor. Die weisse Unterlage
    # muss VOR dem Hochskalieren gelegt werden, sonst brennt das Verfahren den
    # transparenten Bereich als Schwarz ein.
    flach = os.path.join(QUELLE, "_flat_" + slug + ".png")
    if not os.path.exists(flach):
        subprocess.run(["magick", src, "-background", "white", "-alpha", "remove",
                        "-alpha", "off", "-strip", flach], check=True)
    gross = os.path.join(QUELLE, "_upw_" + slug + ".png")
    if not os.path.exists(gross):
        subprocess.run([ESRGAN, "-i", flach, "-o", gross, "-n", "realesrgan-x4plus", "-s", "4"],
                       check=True, capture_output=True)
    ziel = "team-" + slug
    for endung, qualitaet in (("webp", "84"), ("jpg", "86")):
        subprocess.run([
            "magick", gross, "-strip",
            # Drei der Aufnahmen liegen als PNG mit Transparenz vor. Ohne
            # weisse Unterlage werden sie beim Umwandeln schwarz und fallen
            # in der Kachelreihe sofort auf.
            "-background", "white", "-alpha", "remove", "-alpha", "off",
            "-resize", "440x440^", "-gravity", "north", "-extent", "440x440",
            "-quality", qualitaet, os.path.join(MEDIA, f"{ziel}.{endung}")], check=True)
    manifest[slug] = ziel
    print(f"   {ziel}")

json.dump(manifest, open(os.path.join(HERE, "team-media.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"\n{len(manifest)} Portraets in {MEDIA}")
