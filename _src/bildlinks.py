#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Welche Bilder fuehren nirgendwohin?

Suat am 27.08.: alle Bilder sollen reaktiv und verlinkt sein. Diese
Pruefung listet auf, welche Bilder weder in einem Verweis noch in der
Bildergalerie liegen - Hintergrundbilder der Kopfbereiche und reine
Zierbilder ausgenommen, die haben kein sinnvolles Ziel.
"""
import os, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

# Bilder, die kein Ziel haben koennen oder eines auf anderem Weg bekommen
OHNE_ZIEL = {
    "subhero__bg": "Kopfbereich, liegt als Hintergrund hinter der Ueberschrift",
    "hero__bg": "Startbild, Hintergrund",
    "gal__img": "Bildergalerie, oeffnet die Grossansicht per Skript",
    "hlbox__img": "Grossansicht des Karussells",
    "foot__brand": "Logo im Fuss",
    "nav__logo": "Logo im Kopf",
    "mmenu": "Logo im mobilen Menue",
}

gruppen = Counter()
beispiele = {}

for basis, ordner, dateien in os.walk(ROOT):
    ordner[:] = [o for o in ordner if o not in ("_src", ".git", "font", "media", "css", "js", "docs")]
    for d in dateien:
        if not d.endswith(".html"):
            continue
        pfad = os.path.join(basis, d)
        rel = os.path.relpath(pfad, ROOT).replace(os.sep, "/")
        html = open(pfad, encoding="utf-8").read()

        # Alle <img>, und ob ein <a> davor offen ist
        for treffer in re.finditer(r"<img\b[^>]*>", html):
            vorher = html[:treffer.start()]
            # Der letzte geoeffnete Verweis vor dem Bild, sofern nicht geschlossen
            letztes_a = vorher.rfind("<a ")
            letztes_ende = vorher.rfind("</a>")
            im_verweis = letztes_a > letztes_ende

            tag = treffer.group(0)
            klasse = re.search(r'class="([^"]*)"', tag)
            klasse = klasse.group(1) if klasse else ""
            # Klasse des umgebenden Bereichs mitnehmen
            umfeld = vorher[-400:]
            schluessel = klasse.split()[0] if klasse else "(ohne Klasse)"
            for k in OHNE_ZIEL:
                if k in klasse or k in umfeld:
                    schluessel = k
                    break

            if im_verweis:
                gruppen["VERLINKT " + schluessel] += 1
            else:
                gruppen["OHNE ZIEL " + schluessel] += 1
                beispiele.setdefault(schluessel, (rel, tag[:110]))

print("Bilder nach Zustand\n" + "=" * 66)
for name, anzahl in sorted(gruppen.items(), key=lambda x: (-x[1], x[0])):
    art = name.split(" ", 2)
    zustand, schluessel = (" ".join(art[:2]), art[2]) if art[0] == "OHNE" else (art[0], art[1])
    hinweis = ""
    if zustand.startswith("OHNE"):
        hinweis = OHNE_ZIEL.get(schluessel, "")
    print(f"  {zustand:10s} {schluessel:22s} {anzahl:5d}  {hinweis}")

print("\nOhne Ziel und ohne Erklaerung:")
offen = [(k, v) for k, v in beispiele.items() if k not in OHNE_ZIEL]
if not offen:
    print("  keine")
for k, (datei, tag) in offen:
    print(f"  {k}\n     {datei}\n     {tag}")
