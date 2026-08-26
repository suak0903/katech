#!/usr/bin/env python3
"""Verdichtet content.json zu einer Datenbasis fuer den Seiten-Generator:
je Bestandsseite Titel, Intro-Absaetze, Hauptbild und Unterseiten-Baum."""
import json, os, re, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://katech-solutions.com"
HERE = os.path.dirname(os.path.abspath(__file__))
content = json.load(open(os.path.join(HERE, "content.json"), encoding="utf-8"))


def hauptbild(slug):
    """Erstes inhaltliches Bild aus dem Rohdokument der Seite."""
    pfad = os.path.join(HERE, "raw", (slug.replace("/", "_") or "home") + ".html")
    if not os.path.exists(pfad):
        return ""
    doc = open(pfad, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'<img[^>]+src="([^"]+)"', doc):
        u = m.group(1)
        if ("/wp-content/uploads/" in u or "khpartner.com" in u) and not re.search(
                r"(logo|icon|cert|sedex|brcgs|ifs|rspo|organic|foodchain|halal|kosher|flags|banner-green)", u, re.I):
            return u if not u.startswith("/") else BASE + u
    return ""


daten = {}
for url, p in content.items():
    slug = url.replace(BASE, "").strip("/")
    absaetze = [b["text"] for b in p["blocks"] if b["tag"] == "p" and len(b["text"]) > 45]
    ueberschriften = [b["text"] for b in p["blocks"] if b["tag"] in ("h1", "h2", "h3")]
    listen = [b["text"] for b in p["blocks"] if b["tag"] == "li" and 3 < len(b["text"]) < 200]
    titel = re.sub(r"\s*\|?\s*KaTech\s*$", "", p["title"]).strip()
    titel = re.sub(r"^KaTech\s*[-–]\s*", "", titel).strip()
    daten[slug] = {
        "slug": slug,
        "url": url,
        "titel": titel,
        "h1": p["h1"],
        "ueberschriften": ueberschriften[:8],
        "description": p["description"],
        "absaetze": absaetze,
        "listen": listen[:40],
        "bild": hauptbild(slug),
    }

# Bereichsbaum: Top-Level-Slugs mit ihren Unterseiten
baum = {}
for slug in daten:
    if not slug:
        continue
    teile = slug.split("/")
    if len(teile) == 1:
        baum.setdefault(slug, [])
    else:
        baum.setdefault(teile[0], []).append(slug)
for k in baum:
    baum[k].sort()

json.dump({"seiten": daten, "baum": baum},
          open(os.path.join(HERE, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

mit_text = sum(1 for d in daten.values() if d["absaetze"])
mit_bild = sum(1 for d in daten.values() if d["bild"])
print(f"Seiten: {len(daten)} | mit Fliesstext: {mit_text} | mit Hauptbild: {mit_bild}")
print("Bereiche mit Unterseiten:")
for k, v in sorted(baum.items(), key=lambda x: -len(x[1])):
    if v:
        print(f"  {k:28s} {len(v)}")
