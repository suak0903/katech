#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erste Seite jedes Zertifikats als Bild.

Suat am 27.08.: das RSPO-Zertifikat soll direkt angezeigt werden. Eine
eingebettete PDF-Ansicht taugt dafuer nicht - viele Browser zeigen dort
nur den Ersatztext. Ein Bild zeigt immer etwas, das PDF haengt darunter.
"""
import io, os, sys
import fitz
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "..", "docs")
MEDIA = os.path.join(HERE, "..", "media")

BREITE = 900       # angezeigte Breite; 2x fuer scharfe Darstellung
ZOOM = 2

for datei in sorted(os.listdir(DOCS)):
    if not datei.endswith(".pdf"):
        continue
    name = "cert-" + datei[:-4].replace("katech-", "") + "-p1"
    dok = fitz.open(os.path.join(DOCS, datei))
    seite = dok[0]
    faktor = (BREITE * ZOOM) / seite.rect.width
    pix = seite.get_pixmap(matrix=fitz.Matrix(faktor, faktor), alpha=False)
    bild = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    dok.close()

    for endung, opt in (("webp", {"quality": 82, "method": 6}),
                        ("jpg", {"quality": 85, "optimize": True, "progressive": True})):
        ziel = os.path.join(MEDIA, f"{name}.{endung}")
        bild.save(ziel, **opt)      # Pillow schreibt keine Metadaten mit
    print(f"  {name:34s} {bild.width}x{bild.height}")
