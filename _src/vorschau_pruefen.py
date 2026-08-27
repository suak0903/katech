#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stimmt jede Zahl auf der Vorschau-Seite noch?

Nach jeder Aenderungsrunde altert diese Seite still vor sich hin: sie nennt
Zahlen, die anderswo laengst anders sind. Diese Pruefung liest die Zahlen
aus dem erzeugten HTML und stellt sie neben den gemessenen Stand.
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

seite = open(os.path.join(ROOT, "about-this-preview", "index.html"), encoding="utf-8").read()

# --------------------------------------------------------------- gemessen
erzeugt, weitergeleitet, mit_breadcrumb, unterseiten = set(), [], 0, 0
for basis, ordner, dateien in os.walk(ROOT):
    ordner[:] = [o for o in ordner if o not in ("_src", ".git", "font", "media", "css", "js", "docs")]
    for d in dateien:
        if not d.endswith(".html"):
            continue
        pfad = os.path.join(basis, d)
        rel = os.path.relpath(pfad, ROOT).replace(os.sep, "/")
        erzeugt.add(rel)
        html = open(pfad, encoding="utf-8").read()
        if 'http-equiv="refresh"' in html:
            weitergeleitet.append(rel)
            continue
        if "BreadcrumbList" in html:
            mit_breadcrumb += 1
        if '<nav class="crumbs"' in html:
            unterseiten += 1

media = os.path.join(ROOT, "media")
webp = {f[:-5] for f in os.listdir(media) if f.endswith(".webp")}
motive = set()
for w in webp:
    motive.add(re.sub(r"-(800|1400|2000|2400)$", "", w.replace("team-_up_", "team-")))
bilder_bestand = len({m for m in motive if not m.startswith("cert-")})

daten = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
import struktur as S
bereiche = [b for _, _, _, bs in S.SOLUTIONS for b in bs]
produkttypen = sum(len(daten["baum"].get(b, [])) + len(S.FREMDE_KINDER.get(b, []))
                   for b in bereiche)

import inhalt as I
gemessen = {
    "Seiten insgesamt": len(erzeugt),
    "davon Weiterleitungen": len(weitergeleitet),
    "echte Seiten": len(erzeugt) - len(weitergeleitet),
    "Seiten mit Breadcrumb-Markup": mit_breadcrumb,
    "Produktbereiche": len(bereiche),
    "Produkttypen": produkttypen,
    "Bilder aus dem Bestand": bilder_bestand,
    "Seiten mit Beratungsreitern": len(I.REITER),
    "im Bestand leere Seiten": len(I.LEER_IM_ORIGINAL),
    "Dokumente": len([f for f in os.listdir(os.path.join(ROOT, "docs")) if f.endswith(".pdf")]),
    "Teamprofile": len(json.load(open(os.path.join(HERE, "team.json"), encoding="utf-8"))),
    "JavaScript in KB": round(os.path.getsize(os.path.join(ROOT, "js", "site.js")) / 1024),
    "Menuepunkte": len(S.BEREICHE),
}

print("Gemessener Stand")
print("=" * 62)
for k, v in gemessen.items():
    print(f"  {k:34s} {v}")

# ------------------------------------------------- Zahlen auf der Seite
print("\nZahlen, die auf der Vorschau-Seite stehen")
print("=" * 62)
# Kennzahlen-Kacheln und Umfangstabelle
for m in re.finditer(r"<div><b>([^<]{1,8})</b><span>([^<]+)</span></div>", seite):
    print(f"  {m.group(1):>8s}  {m.group(2)}")

print("\nAussagen mit Zahlen im Fliesstext")
print("=" * 62)
text = re.sub(r"<[^>]+>", " ", seite)
text = re.sub(r"\s+", " ", text)
for satz in re.split(r"(?<=[.!?]) ", text):
    if re.search(r"\b(all |every |\d{2,3})\b", satz) and len(satz) < 320:
        if re.search(r"\d", satz):
            print("  " + satz.strip()[:300])
