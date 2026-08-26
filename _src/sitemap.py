#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Schreibt sitemap.xml des Demonstrators. Die Seite ist per robots.txt und
noindex von der Indexierung ausgenommen; die Sitemap dient als Strukturbeleg
und als Vorlage fuer den spaeteren Livebetrieb."""
import os, sys
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BASIS = "https://suak0903.github.io/katech/"
HEUTE = date.today().isoformat()
IGNORIEREN = {"_src", ".git", "font", "media", "css", "js"}

urls = []
for basis, ordner, dateien in os.walk(ROOT):
    ordner[:] = [o for o in ordner if o not in IGNORIEREN]
    for d in sorted(dateien):
        if not d.endswith(".html") or d == "404.html":
            continue
        rel = os.path.relpath(os.path.join(basis, d), ROOT).replace(os.sep, "/")
        pfad = rel[:-len("index.html")] if rel.endswith("index.html") else rel
        urls.append(BASIS + pfad)

urls.sort(key=lambda u: (u.count("/"), u))
zeilen = "\n".join(
    f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{HEUTE}</lastmod>\n"
    f"    <priority>{'1.0' if u == BASIS else ('0.8' if u.count('/') == 4 else '0.6')}</priority>\n  </url>"
    for u in urls)

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       f"{zeilen}\n</urlset>\n")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write(xml)
print(f"sitemap.xml: {len(urls)} URLs")
