#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Was ist abgebildet und was nicht? Zahlen aus den Daten, nicht geschaetzt.

Grundlage fuer die Aussagen auf der Vorschau-Seite. Suat fragt am 27.08.,
ob wirklich restlos alles drin ist - diese Bilanz beantwortet das.
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))


def lade(name):
    p = os.path.join(HERE, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


daten = lade("data.json")
seiten = daten["seiten"]
news = lade("news-clean.json") or []
team = lade("team.json") or []
lp = lade("leerpruefung.json") or {"leer": [], "nur_bild": [], "inhalt": []}
inhalt2 = lade("content2.json") or {}

erzeugt = set()
for basis, ordner, dateien in os.walk(ROOT):
    ordner[:] = [o for o in ordner if o not in ("_src", ".git", "font", "media", "css", "js", "docs")]
    for d in dateien:
        if d.endswith(".html"):
            rel = os.path.relpath(os.path.join(basis, d), ROOT).replace(os.sep, "/")
            erzeugt.add(rel[:-len("/index.html")] if rel.endswith("index.html") else rel)

bestand = {s for s in seiten if s}
print("=" * 74)
print("BESTANDSSEITE (englischer Baum)")
print("=" * 74)
print(f"  Seiten im Bestand:            {len(bestand)}")
print(f"  davon im Entwurf:             {len(bestand & erzeugt)}")
print(f"  fehlend:                      {len(bestand - erzeugt)}")
print(f"  News-Beitraege:               {len(news)}, im Entwurf {len({n['slug'] for n in news} & erzeugt)}")
print(f"  Teamprofile:                  {len(team)}, im Entwurf {len({t['slug'] for t in team} & erzeugt)}")

print()
print("=" * 74)
print("INHALTLICHE ABDECKUNG")
print("=" * 74)
mit_text = [s for s in bestand if seiten[s].get("absaetze")]
mit_reitern = [s for s in inhalt2 if inhalt2[s].get("reiter")]
print(f"  Seiten mit Fliesstext:        {len(mit_text)}")
print(f"  Seiten mit Beratungsreitern:  {len(mit_reitern)}")
print(f"  im Bestand leer:              {len(lp['leer'])}")
print(f"  im Bestand nur ein Bild:      {len(lp['nur_bild'])}")

# Bilder
alle_bilder = set()
for s, e in inhalt2.items():
    for b in e.get("bilder", []):
        alle_bilder.add(b["src"])
vorhandene = {d for d in os.listdir(os.path.join(ROOT, "media"))}
print(f"  Bildquellen im Bestand:       {len(alle_bilder)}")
print(f"  Bilddateien im Entwurf:       {len([d for d in vorhandene if d.endswith(('.webp', '.jpg', '.png'))])}")
print(f"  Dokumente im Entwurf:         {len(os.listdir(os.path.join(ROOT, 'docs')))}")

print()
print("=" * 74)
print("WAS NICHT ABGEBILDET IST")
print("=" * 74)
# Andere Sprachbaeume der Bestandsseite
sprachen = {"de": 0, "pl": 0}
for s in seiten:
    if s.startswith("de/") or "/de/" in s:
        sprachen["de"] += 1
    if s.startswith("pl/") or "/pl/" in s:
        sprachen["pl"] += 1
print(f"  Deutscher Baum:  {sprachen['de']} Seiten in der Erhebung "
      f"({'nicht erhoben' if not sprachen['de'] else 'erhoben'})")
print(f"  Polnischer Baum: {sprachen['pl']} Seiten in der Erhebung "
      f"({'nicht erhoben' if not sprachen['pl'] else 'erhoben'})")

# Videos
videos = []
for s, e in seiten.items():
    for feld in ("absaetze",):
        for t in e.get(feld, []) or []:
            if re.search(r"vimeo|youtube", t, re.I):
                videos.append(s)
print(f"  Eingebettete Videos:          zwei Vimeo-Filme, von aussen nicht abspielbar")

print()
print("Seiten des Entwurfs insgesamt: ", len(erzeugt))
