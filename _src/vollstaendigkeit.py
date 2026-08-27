#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zwei Vollstaendigkeitspruefungen:

1. Steht jede erzeugte Seite in der grafischen Sitemap?
2. Ist jede Seite der Bestandsseite im Entwurf vorhanden?
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

# ---------------------------------------------------------------- 1. Sitemap
sitemap = open(os.path.join(ROOT, "sitemap", "index.html"), encoding="utf-8").read()
haupt = re.search(r'<main id="main">(.*?)</main>', sitemap, re.S).group(1)
verlinkt = set()
for m in re.finditer(r'href="\.\./([^"#]*)"', haupt):
    z = m.group(1).strip("/")
    verlinkt.add(z if z else "")

erzeugt = set()
for basis, ordner, dateien in os.walk(ROOT):
    ordner[:] = [o for o in ordner if o not in ("_src", ".git", "font", "media", "css", "js")]
    for d in dateien:
        if not d.endswith(".html"):
            continue
        rel = os.path.relpath(os.path.join(basis, d), ROOT).replace(os.sep, "/")
        erzeugt.add(rel[:-len("/index.html")] if rel.endswith("index.html") else rel)

fehlt_in_sitemap = sorted(s for s in erzeugt - verlinkt
                          if s not in ("", "index.html", "404.html", "about-this-preview"))
print(f"Erzeugte Seiten:        {len(erzeugt)}")
print(f"In der Sitemap:         {len(verlinkt & erzeugt)}")
print(f"Fehlt in der Sitemap:   {len(fehlt_in_sitemap)}")
for s in fehlt_in_sitemap:
    print(f"    {s}")

# --------------------------------------------------------- 2. Bestandsseiten
daten = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))["seiten"]
bestand = {s for s in daten if s}
fehlt_im_entwurf = sorted(bestand - erzeugt)
print()
print(f"Seiten der Bestandsseite (englischer Baum): {len(bestand)}")
print(f"Davon im Entwurf vorhanden:                 {len(bestand & erzeugt)}")
print(f"Fehlt im Entwurf:                           {len(fehlt_im_entwurf)}")
for s in fehlt_im_entwurf:
    print(f"    {s}")

# News- und Teamseiten des Bestands
for datei, name in (("news-clean.json", "News-Beitraege"), ("team.json", "Teamprofile")):
    pfad = os.path.join(HERE, datei)
    if not os.path.exists(pfad):
        continue
    slugs = {e["slug"] for e in json.load(open(pfad, encoding="utf-8"))}
    fehlt = sorted(slugs - erzeugt)
    print(f"\n{name}: {len(slugs)}, davon im Entwurf {len(slugs & erzeugt)}, fehlt {len(fehlt)}")
    for s in fehlt:
        print(f"    {s}")
