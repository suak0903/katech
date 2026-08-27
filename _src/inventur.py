#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vollstaendige Inventur: welche Bestandsseite traegt Inhalt, welche ist leer.

Grundlage fuer die Strukturentscheidung. Eine Struktur, die Abschnitte bildet,
in denen nur leere Seiten stehen, hilft niemandem."""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
seiten, baum = d["seiten"], d["baum"]

PRODUKT = ["yogurt", "cream", "cheese", "desserts", "milk-drinks", "vegan",
           "mayonnaise", "dressings", "dips", "soups-and-sauces", "soups",
           "bakery", "fruit"]

def status(slug):
    p = seiten.get(slug, {})
    n = len(p.get("absaetze", []))
    listen = len(p.get("listen", []))
    if n == 0 and listen == 0:
        return "LEER"
    return f"{n} Abs."

def zeile(slug, tiefe=0):
    p = seiten.get(slug, {})
    titel = (p.get("h1") or p.get("titel") or slug.split("/")[-1]).strip()
    print(f"{'  ' * tiefe}{slug:44s} {status(slug):9s} {titel[:46]}")

print("=" * 104)
print("PRODUKTBEREICHE")
print("=" * 104)
leer_produkt = 0
for b in PRODUKT:
    zeile(b)
    for u in baum.get(b, []):
        zeile(u, 1)
        if status(u) == "LEER":
            leer_produkt += 1

print()
print("=" * 104)
print("UEBRIGE SEITEN (ohne News, Team, Legal)")
print("=" * 104)
rest = [s for s in sorted(seiten)
        if s and s.split("/")[0] not in PRODUKT + ["bakery-old"]]
leer_rest = 0
for s in rest:
    zeile(s)
    if status(s) == "LEER":
        leer_rest += 1

gesamt_leer = sum(1 for s in seiten if s and status(s) == "LEER")
print()
print(f"Leere Seiten gesamt: {gesamt_leer} von {len(seiten)}")
print(f"  davon in Produktbereichen: {leer_produkt}")
print(f"  davon in uebrigen Seiten:  {leer_rest}")
