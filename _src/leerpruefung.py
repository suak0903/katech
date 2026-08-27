#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gruendliche Pruefung der als leer eingestuften Seiten.

Der erste Extraktor hat nur Fliesstext gelesen. Hier wird der komplette
Inhaltsbereich untersucht: Text, Listen, Tabellen, Bilder, Downloads,
eingebettete Inhalte und Verweise. Nur was danach wirklich nichts traegt,
ist wirklich leer.
"""
import json, os, re, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROH = os.path.join(HERE, "raw")

NOISE_IDS = ["top-nav-container", "enquiry-form", "fade-dialog", "colophon", "pre-footer",
             "cmplz-cookiebanner-container", "cmplz-manage-consent", "comments", "header"]
NOISE_CLASSES = ["sidebar__menu", "sidebar__menu--underlay", "header-fixed", "mobile__burger",
                 "language__selector--desktop", "language__selector--mobile", "wpcf7",
                 "screen-reader-response", "logos-social", "cmplz-cookiebanner"]
# Bilder, die auf jeder Seite im Rahmen stehen und nichts ueber den Inhalt sagen
RAHMEN = re.compile(r"(logo|icon|flags|sign-bg|brcgs|rspo|sedex|ifs|organic|foodchain|"
                    r"halal|kosher|esc|product-tab|banner-green)", re.I)

daten = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))["seiten"]
kandidaten = [s for s, p in daten.items()
              if s and not p.get("absaetze") and not p.get("listen")]

print(f"Als leer eingestuft: {len(kandidaten)} Seiten. Jede wird jetzt vollstaendig untersucht.\n")

wirklich_leer, doch_inhalt = [], []

for slug in sorted(kandidaten):
    pfad = os.path.join(ROH, (slug.replace("/", "_") or "home") + ".html")
    if not os.path.exists(pfad):
        print(f"  {slug:44s} ROHDATEI FEHLT")
        continue
    soup = BeautifulSoup(open(pfad, encoding="utf-8", errors="replace").read(), "lxml")
    for i in NOISE_IDS:
        for e in soup.find_all(id=i):
            e.decompose()
    for c in NOISE_CLASSES:
        for e in soup.select("." + c):
            e.decompose()
    for e in soup.find_all(["script", "style", "noscript"]):
        e.decompose()
    inhalt = soup.find(id="content") or soup.body

    text = re.sub(r"\s+", " ", inhalt.get_text(" ", strip=True))
    # Titel und Standardfloskeln abziehen
    for weg in ("Comments are closed.", "Read more...", "click!"):
        text = text.replace(weg, " ")
    h = inhalt.find(["h1", "h2"])
    if h:
        text = text.replace(h.get_text(" ", strip=True), " ", 1)
    text = re.sub(r"\s+", " ", text).strip()

    bilder = [i.get("src", "") for i in inhalt.find_all("img")
              if i.get("src") and not RAHMEN.search(i.get("src", ""))]
    tabellen = inhalt.find_all("table")
    rahmenfenster = inhalt.find_all("iframe")
    dateien = [a.get("href", "") for a in inhalt.find_all("a", href=True)
               if re.search(r"\.(pdf|docx?|xlsx?|zip|pptx?)$", a.get("href", ""), re.I)]
    verweise = [a.get("href", "") for a in inhalt.find_all("a", href=True)
                if a.get("href", "").startswith(("http", "/")) and "katech" in a.get("href", "")]

    gefunden = []
    if len(text) > 25:
        gefunden.append(f"Text ({len(text)} Z.): {text[:110]}")
    if bilder:
        gefunden.append(f"Bilder: {[b.split('/')[-1] for b in bilder][:4]}")
    if tabellen:
        gefunden.append(f"Tabellen: {len(tabellen)}")
    if rahmenfenster:
        gefunden.append(f"Eingebettet: {len(rahmenfenster)}")
    if dateien:
        gefunden.append(f"Downloads: {[d.split('/')[-1] for d in dateien][:3]}")

    nur_bild = bool(bilder) and len(text) <= 25 and not tabellen and not rahmenfenster and not dateien
    if gefunden:
        doch_inhalt.append((slug, gefunden, nur_bild))
        print(f"  {slug:44s} {'NUR BILD' if nur_bild else 'INHALT GEFUNDEN'}")
        for g in gefunden:
            print(f"      {g}")
    else:
        wirklich_leer.append(slug)

print(f"\n{'=' * 90}")
print(f"Wirklich leer: {len(wirklich_leer)}")
for s in wirklich_leer:
    print(f"  {s}")
print(f"\nDoch mit Inhalt: {len(doch_inhalt)}")
json.dump({"leer": wirklich_leer,
           "nur_bild": [s for s, _, nb in doch_inhalt if nb],
           "inhalt": [s for s, _, nb in doch_inhalt if not nb]},
          open(os.path.join(HERE, "leerpruefung.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
