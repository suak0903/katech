#!/usr/bin/env python3
"""Zweiter Durchgang: holt die EN-Seiten erneut und extrahiert mit BeautifulSoup
sauber den Inhaltsbereich (ohne Mega-Navigation, Anfrageformular, Cookie-Banner)."""
import json, os, sys, time, urllib.request
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://katech-solutions.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "raw")

# Container, die nur Navigation, Formular oder Rechtstexte des Themes tragen
NOISE_IDS = ["top-nav-container", "enquiry-form", "fade-dialog", "colophon", "pre-footer",
             "cmplz-cookiebanner-container", "cmplz-manage-consent", "comments", "header"]
NOISE_CLASSES = ["sidebar__menu", "sidebar__menu--underlay", "header-fixed", "mobile__burger",
                 "language__selector--desktop", "language__selector--mobile", "wpcf7",
                 "screen-reader-response", "logos-social", "cmplz-cookiebanner"]


def fetch(url):
    slug = url.replace(BASE, "").strip("/").replace("/", "_") or "home"
    path = os.path.join(CACHE, slug + ".html")
    if os.path.exists(path):
        return open(path, encoding="utf-8", errors="replace").read()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    last = None
    for versuch in range(5):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                doc = r.read().decode("utf-8", errors="replace")
            os.makedirs(CACHE, exist_ok=True)
            open(path, "w", encoding="utf-8").write(doc)
            time.sleep(1.2)
            return doc
        except Exception as e:
            last = e
            time.sleep(8 * (versuch + 1))
    raise last


def parse(url, doc):
    soup = BeautifulSoup(doc, "lxml")
    out = {"url": url}
    out["title"] = soup.title.get_text(strip=True) if soup.title else ""
    md = soup.find("meta", attrs={"name": "description"})
    out["description"] = md.get("content", "").strip() if md else ""

    for i in NOISE_IDS:
        for el in soup.find_all(id=i):
            el.decompose()
    for c in NOISE_CLASSES:
        for el in soup.select("." + c):
            el.decompose()
    for el in soup.find_all(["script", "style", "noscript"]):
        el.decompose()

    content = soup.find(id="content") or soup.body or soup
    h1 = content.find("h1")
    out["h1"] = h1.get_text(" ", strip=True) if h1 else ""

    blocks = []
    for el in content.find_all(["h1", "h2", "h3", "h4", "p", "li", "td", "th"]):
        t = el.get_text(" ", strip=True)
        if not t or len(t) < 2:
            continue
        blocks.append({"tag": el.name, "text": t})
    # Dubletten in Folge entfernen
    clean, prev = [], None
    for b in blocks:
        if prev and b["text"] == prev:
            continue
        clean.append(b)
        prev = b["text"]
    out["blocks"] = clean

    imgs = []
    for im in content.find_all("img"):
        src = im.get("src") or ""
        if "/wp-content/uploads/" in src or "khpartner.com" in src:
            if src.startswith("/"):
                src = BASE + src
            imgs.append({"src": src, "alt": im.get("alt", "")})
    out["images"] = imgs

    links = []
    for a in content.find_all("a", href=True):
        h = a["href"]
        if h.startswith("/") or h.startswith(BASE):
            links.append({"href": h, "text": a.get_text(" ", strip=True)})
    out["links"] = links
    return out


def main():
    urls = [l.strip() for l in open(os.path.join(HERE, "en-pages.txt"), encoding="utf-8") if l.strip()]
    urls.insert(0, BASE + "/")
    res = {}
    for n, u in enumerate(urls, 1):
        try:
            res[u] = parse(u, fetch(u))
            if n % 20 == 0:
                print(f"  {n}/{len(urls)}")
        except Exception as e:
            print("FAIL", u, e)
    json.dump(res, open(os.path.join(HERE, "content.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("Fertig:", len(res), "Seiten -> content.json")


if __name__ == "__main__":
    main()
