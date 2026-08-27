#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Die Beitrags-Karte des Bestands listet 107 Adressen, der Entwurf zeigt 17
News. Diese Pruefung klaert, was die uebrigen sind (Suat 27.08.)."""
import json, os, re, sys, time, urllib.error, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASIS = "https://katech-solutions.com"


def hole(url):
    for versuch in range(3):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                timeout=30).read().decode("utf-8", "replace")
        except urllib.error.HTTPError as f:
            if f.code != 503:
                return None
            time.sleep(3 + versuch * 4)
        except Exception:
            return None
    return None


roh = hole(BASIS + "/post-sitemap.xml")
adressen = re.findall(r"<loc>([^<]+)</loc>", roh)
wege = [a.replace(BASIS, "").strip("/") for a in adressen]

de = [w for w in wege if w.startswith("de/")]
pl = [w for w in wege if w.startswith("pl/")]
en = [w for w in wege if not w.startswith(("de/", "pl/"))]

eigene = {e["slug"] for e in json.load(
    open(os.path.join(HERE, "news-clean.json"), encoding="utf-8"))}

print(f"Beitraege im Bestand:  {len(wege)}")
print(f"  englisch:            {len(en)}")
print(f"  deutsch:             {len(de)}")
print(f"  polnisch:            {len(pl)}")
print()
print(f"Englische im Entwurf:  {len(set(en) & eigene)}")
fehlt = sorted(set(en) - eigene)
print(f"Englische, die fehlen: {len(fehlt)}")
for f in fehlt:
    print(f"    {f}")
