#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trennt die Beitraege der Bestandsseite in echte News und Team-Profile.
Die Bestandsseite fuehrt beides als WordPress-Posts; die Kategorie
our-people/... kennzeichnet die Personenprofile."""
import json, os, re, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROH = os.path.join(HERE, "raw-news")

NOISE_IDS = ["top-nav-container", "enquiry-form", "fade-dialog", "colophon", "pre-footer",
             "cmplz-cookiebanner-container", "cmplz-manage-consent", "comments", "header"]
NOISE_CLASSES = ["sidebar__menu", "sidebar__menu--underlay", "header-fixed", "mobile__burger",
                 "language__selector--desktop", "language__selector--mobile", "wpcf7",
                 "screen-reader-response", "logos-social", "cmplz-cookiebanner"]

TEAM_GRUPPEN = {
    "our-people/management": ("Management", "Lübeck"),
    "our-people/technical-germany": ("Technical, Germany", "Lübeck"),
    "our-people/technical-uk": ("Technical, United Kingdom", "Ellesmere Port"),
    "our-people/sales-germany": ("Sales, Germany", "Lübeck"),
    "our-people/sales-uk": ("Sales, United Kingdom", "Ellesmere Port"),
    "our-people/sales-poland": ("Sales, Poland", "Stęszew"),
    "our-people/purchasing": ("Purchasing", "Lübeck"),
}

news = json.load(open(os.path.join(HERE, "news.json"), encoding="utf-8"))
echte_news, team = [], []

for eintrag in news:
    slug = eintrag["slug"]
    pfad = os.path.join(ROH, slug + ".html")
    if not os.path.exists(pfad):
        continue
    doc = open(pfad, encoding="utf-8", errors="replace").read()
    kategorien = set(re.findall(r'/category/([a-z0-9/-]+)/"', doc))
    personen_kats = [k for k in kategorien if k.startswith("our-people/")]

    if not personen_kats:
        if slug != "news":
            echte_news.append(eintrag)
        continue

    soup = BeautifulSoup(doc, "lxml")
    for i in NOISE_IDS:
        for el in soup.find_all(id=i):
            el.decompose()
    for c in NOISE_CLASSES:
        for el in soup.select("." + c):
            el.decompose()
    for el in soup.find_all(["script", "style", "noscript"]):
        el.decompose()
    inhalt = soup.find(id="content") or soup.body
    h1 = inhalt.find("h1")
    rolle = inhalt.find(["h2", "h3", "h4"])
    absaetze = [p.get_text(" ", strip=True) for p in inhalt.find_all("p")]
    absaetze = [a for a in absaetze if len(a) > 45 and "Comments are closed" not in a]
    gruppe, ort = TEAM_GRUPPEN.get(sorted(personen_kats)[0], ("Team", ""))
    team.append({
        "slug": slug,
        "name": h1.get_text(" ", strip=True) if h1 else eintrag["titel"],
        "rolle": rolle.get_text(" ", strip=True) if rolle else "",
        "gruppe": gruppe, "ort": ort,
        "vita": absaetze,
        "kategorie": sorted(personen_kats)[0],
    })

json.dump(echte_news, open(os.path.join(HERE, "news-clean.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(team, open(os.path.join(HERE, "team.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"Echte News: {len(echte_news)} | Team-Profile: {len(team)}")
for t in team:
    print(f"  {t['gruppe']:28s} {t['name']:24s} {t['rolle'][:40]}")
