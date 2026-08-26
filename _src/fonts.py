#!/usr/bin/env python3
"""Laedt die benoetigten OFL-Schnitte (Barlow, Open Sans) als woff2 zum Self-Hosting."""
import os, re, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0.0.0 Safari/537.36")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "font")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

WANTED = [
    ("Barlow", "600", "Barlow-600"),
    ("Barlow", "700", "Barlow-700"),
    ("Open+Sans", "400", "OpenSans-400"),
    ("Open+Sans", "600", "OpenSans-600"),
    ("Open+Sans", "700", "OpenSans-700"),
]


def hole(url, binaer=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read()
    return data if binaer else data.decode("utf-8")


for familie, gewicht, ziel in WANTED:
    css = hole(f"https://fonts.googleapis.com/css2?family={familie}:wght@{gewicht}&display=swap")
    # den latin-Block (letzter unicode-range-Block) nehmen
    bloecke = css.split("/*")
    latin = [b for b in bloecke if b.strip().startswith("latin */")]
    quelle = latin[-1] if latin else css
    m = re.search(r"url\((https://[^)]+\.woff2)\)", quelle)
    if not m:
        print("  KEINE woff2-URL fuer", ziel)
        continue
    daten = hole(m.group(1), binaer=True)
    pfad = os.path.join(OUT, ziel + ".woff2")
    open(pfad, "wb").write(daten)
    print(f"  {ziel}.woff2  {len(daten)//1024} KB")

print("Schriften in", OUT)
