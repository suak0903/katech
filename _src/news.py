#!/usr/bin/env python3
"""Holt die englischen News-Beitraege der Bestandsseite (Titel, Datum, Text, Bilder)."""
import json, os, re, sys, time, urllib.request
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://katech-solutions.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "raw-news")
os.makedirs(CACHE, exist_ok=True)

NOISE_IDS = ["top-nav-container", "enquiry-form", "fade-dialog", "colophon", "pre-footer",
             "cmplz-cookiebanner-container", "cmplz-manage-consent", "comments", "header"]
NOISE_CLASSES = ["sidebar__menu", "sidebar__menu--underlay", "header-fixed", "mobile__burger",
                 "language__selector--desktop", "language__selector--mobile", "wpcf7",
                 "screen-reader-response", "logos-social", "cmplz-cookiebanner"]


def fetch(url):
    slug = url.replace(BASE, "").strip("/").replace("/", "_") or "news"
    path = os.path.join(CACHE, slug + ".html")
    if os.path.exists(path):
        return open(path, encoding="utf-8", errors="replace").read()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    last = None
    for versuch in range(5):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                doc = r.read().decode("utf-8", errors="replace")
            open(path, "w", encoding="utf-8").write(doc)
            time.sleep(1.2)
            return doc
        except Exception as e:
            last = e
            time.sleep(8 * (versuch + 1))
    raise last


sm = open(os.path.join(HERE, "post-sitemap.xml"), encoding="utf-8").read()
items = re.findall(r"<url>\s*<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sm)
en = [(u, d) for u, d in items if "/de/" not in u and "/pl/" not in u]
en.sort(key=lambda x: x[1], reverse=True)

res = []
for url, datum in en:
    try:
        soup = BeautifulSoup(fetch(url), "lxml")
    except Exception as e:
        print("FAIL", url, e)
        continue
    for i in NOISE_IDS:
        for el in soup.find_all(id=i):
            el.decompose()
    for c in NOISE_CLASSES:
        for el in soup.select("." + c):
            el.decompose()
    for el in soup.find_all(["script", "style", "noscript"]):
        el.decompose()
    content = soup.find(id="content") or soup.body
    h1 = content.find(["h1", "h2"])
    absaetze = [p.get_text(" ", strip=True) for p in content.find_all("p")]
    absaetze = [a for a in absaetze if len(a) > 40]
    bilder = []
    for im in content.find_all("img"):
        s = im.get("src") or ""
        if "/wp-content/uploads/" in s or "khpartner" in s:
            bilder.append(s if not s.startswith("/") else BASE + s)
    res.append({
        "url": url, "slug": url.rstrip("/").split("/")[-1], "datum": datum[:10],
        "titel": h1.get_text(" ", strip=True) if h1 else "",
        "absaetze": absaetze, "bilder": bilder,
    })
    print("  ok", datum[:10], res[-1]["titel"][:60])

json.dump(res, open(os.path.join(HERE, "news.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("News gespeichert:", len(res))
