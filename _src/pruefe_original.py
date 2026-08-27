#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gibt es die Seiten ohne Pfeil im Bestand wirklich nicht?

In der Sitemap traegt jeder Eintrag einen Pfeil zur gleichen Seite im
Bestand - ausser dort, wo die Liste IM_BESTAND die Adresse nicht kennt.
Suat fragt am 27.08. zu Recht nach, ob das stimmt. Diese Pruefung fragt
jede betroffene Adresse einzeln beim Server nach.
"""
import re, os, sys, time, urllib.error, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BASIS = "https://katech-solutions.com/"

sitemap = open(os.path.join(ROOT, "sitemap", "index.html"), encoding="utf-8").read()
haupt = re.search(r'<main id="main">(.*?)</main>', sitemap, re.S).group(1)

ohne_pfeil = []
for li in re.findall(r"<li class=\"sm__i[^\"]*\">(.*?)</li>", haupt, re.S):
    m = re.search(r'href="\.\./([^"#]*)"', li)
    if not m:
        continue
    slug = m.group(1).strip("/")
    if "sm__orig" not in li:
        ohne_pfeil.append(slug)

print(f"Sitemap-Eintraege ohne Pfeil: {len(ohne_pfeil)}\n")

existiert, fehlt = [], []
for slug in ohne_pfeil:
    url = BASIS + (slug + "/" if slug else "")
    code = None
    for versuch in range(3):
        try:
            anfrage = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            code = urllib.request.urlopen(anfrage, timeout=25).getcode()
            break
        except urllib.error.HTTPError as f:
            code = f.code
            if code != 503:
                break
            time.sleep(2 + versuch * 3)
        except Exception as f:
            code = str(f)[:40]
            break
    marke = "GIBT ES" if code == 200 else "nicht vorhanden"
    (existiert if code == 200 else fehlt).append((slug, code))
    print(f"  {slug or '(Startseite)':46s} {str(code):5s} {marke}")
    time.sleep(0.4)

print(f"\n{'=' * 78}")
print(f"Ohne Pfeil, existiert im Bestand trotzdem: {len(existiert)}")
for s, c in existiert:
    print(f"    {s}")
print(f"Ohne Pfeil, gibt es dort wirklich nicht:   {len(fehlt)}")
