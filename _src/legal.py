#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rechtstexte vollstaendig und wortgetreu uebernehmen.

Suat am 27.08.: die Privacy policy war im Entwurf leer, obwohl das Original
30.000 Zeichen traegt. Beim Rechtszeug soll gewissenhafter gearbeitet werden -
erst einmal genau so uebernehmen wie es ist, Auffaelligkeiten nur als
farblich hervorgehobener Kommentar daneben, nie als stille Aenderung.

Erzeugt legal.json: pro Seite die Bloecke in Originalreihenfolge.
"""
import json, os, re, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROH = os.path.join(HERE, "raw")

SEITEN = ["privacy-policy", "imprint", "terms-of-use", "cookie-policy-eu",
          "data-protection-information-for-applicants"]

WEG_IDS = ["top-nav-container", "colophon", "pre-footer", "header", "comments",
           "enquiry-form", "fade-dialog", "cmplz-cookiebanner-container",
           "cmplz-manage-consent"]
WEG_KLASSEN = ["sidebar__menu", "sidebar__menu--underlay", "header-fixed",
               "mobile__burger", "language__selector--desktop",
               "language__selector--mobile", "logos-social", "cmplz-cookiebanner",
               "breadcrumb", "breadcrumbs"]
FLOSKEL = ("Comments are closed.", "Read more...", "click!", "\xa0")

aus = {}
for slug in SEITEN:
    pfad = os.path.join(ROH, slug.replace("/", "_") + ".html")
    if not os.path.exists(pfad):
        print(f"  {slug:44s} ROHDATEI FEHLT")
        continue
    soup = BeautifulSoup(open(pfad, encoding="utf-8", errors="replace").read(), "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    for i in WEG_IDS:
        for e in soup.find_all(id=i):
            e.decompose()
    for k in WEG_KLASSEN:
        for e in soup.select("." + k):
            e.decompose()
    c = soup.find(id="content") or soup.body

    # Die Seitenueberschrift steht separat; sie wird nicht in den Fliesstext
    # uebernommen, sondern zur H1 der Seite.
    kopf = c.find(["h1"])
    titel = kopf.get_text(" ", strip=True) if kopf else slug
    if kopf:
        kopf.decompose()

    bloecke, gesehen = [], set()
    for el in c.find_all(["h2", "h3", "h4", "h5", "p", "li", "td", "th"]):
        # Zellen nur, wenn sie nicht schon ueber die Tabelle erfasst wurden
        if el.find(["p", "li"]):
            continue
        t = el.get_text(" ", strip=True)
        if not t or t in FLOSKEL:
            continue
        schluessel = (el.name, t)
        if schluessel in gesehen:
            continue
        gesehen.add(schluessel)
        eintrag = {"tag": el.name, "text": t}
        a = el.find("a", href=True)
        if a and a.get("href", "").startswith(("http", "mailto:", "/")):
            eintrag["href"] = a["href"]
        bloecke.append(eintrag)

    aus[slug] = {"titel": titel, "bloecke": bloecke}
    zeichen = sum(len(b["text"]) for b in bloecke)
    print(f"  {slug:44s} {len(bloecke):4d} Bloecke, {zeichen:6d} Zeichen")

json.dump(aus, open(os.path.join(HERE, "legal.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
