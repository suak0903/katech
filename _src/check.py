#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Qualitaetspruefung des Demonstrators vor dem Deploy:
tote interne Links, fehlende Medien, Chrome-Gleichheit (md5), Gedankenstrich-Gate,
noindex auf jeder Seite, doppelte H1, fehlende alt-Texte."""
import hashlib, os, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IGNORIEREN = {"_src", ".git", "font"}

fehler = defaultdict(list)
seiten = []
for basis, ordner, dateien in os.walk(ROOT):
    ordner[:] = [o for o in ordner if o not in IGNORIEREN]
    for d in dateien:
        if d.endswith(".html"):
            seiten.append(os.path.join(basis, d))

print(f"HTML-Dateien: {len(seiten)}")

kopf_md5, fuss_md5 = defaultdict(list), defaultdict(list)

for pfad in seiten:
    rel = os.path.relpath(pfad, ROOT).replace(os.sep, "/")
    doc = open(pfad, encoding="utf-8").read()
    verzeichnis = os.path.dirname(pfad)

    # noindex
    if 'content="noindex, nofollow"' not in doc:
        fehler["kein noindex"].append(rel)

    # genau eine H1
    h1 = len(re.findall(r"<h1[ >]", doc))
    if h1 != 1:
        fehler[f"H1-Anzahl {h1}"].append(rel)

    # Gedankenstrich-Gate
    treffer = re.findall(r"—|–|&ndash;|&mdash;|&#8211;|&#8212;", doc)
    if treffer:
        fehler[f"Gedankenstrich ({len(treffer)}x)"].append(rel)

    # Chrome-Gleichheit
    m = re.search(r'<header class="nav.*?</nav>\n(?=<main|<section)', doc, re.S)
    if m:
        norm = re.sub(r'(href|src)="[^"]*"', "", m.group(0))
        # aria-current markiert den aktiven Menuepunkt und darf abweichen,
        # ebenso die solid-Klasse auf Seiten ohne dunklen Hero
        norm = norm.replace(' aria-current="page"', "").replace('class="nav solid"', 'class="nav"')
        kopf_md5[hashlib.md5(norm.encode()).hexdigest()].append(rel)
    f = re.search(r'<footer class="foot">.*?</footer>', doc, re.S)
    if f:
        fuss_md5[hashlib.md5(re.sub(r'(href|src)="[^"]*"', "", f.group(0)).encode()).hexdigest()].append(rel)

    # interne Links und Medien
    for attr, wert in re.findall(r'(?:href|src|srcset)="([^"]+)"|(?:href|src)="()"', doc):
        pass
    for wert in re.findall(r'(?:href|src|srcset)="([^"]+)"', doc):
        wert = wert.split()[0] if " " in wert else wert
        if wert.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#")):
            continue
        rein = wert.split("#")[0].split("?")[0]
        if not rein:
            continue
        ziel = os.path.normpath(os.path.join(verzeichnis, rein))
        if os.path.isdir(ziel):
            ziel = os.path.join(ziel, "index.html")
        if not os.path.exists(ziel):
            if rein.endswith("/"):
                ziel2 = os.path.normpath(os.path.join(verzeichnis, rein, "index.html"))
                if os.path.exists(ziel2):
                    continue
            fehler["toter Verweis"].append(f"{rel} -> {wert}")

    # alt-Texte
    for tag in re.findall(r"<img [^>]*>", doc):
        if "alt=" not in tag:
            fehler["img ohne alt"].append(rel)
            break

print(f"Kopf-Varianten: {len(kopf_md5)} | Fuss-Varianten: {len(fuss_md5)}")
if len(kopf_md5) > 1:
    for h, s in kopf_md5.items():
        print(f"   Kopf {h[:8]}: {len(s)} Seiten, z. B. {s[0]}")
if len(fuss_md5) > 1:
    for h, s in fuss_md5.items():
        print(f"   Fuss {h[:8]}: {len(s)} Seiten, z. B. {s[0]}")

print()
if not fehler:
    print("Keine Befunde.")
for art, liste in sorted(fehler.items(), key=lambda x: -len(x[1])):
    print(f"{art}: {len(liste)}")
    for e in liste[:6]:
        print("   ", e)
    if len(liste) > 6:
        print(f"    ... und {len(liste) - 6} weitere")
