#!/usr/bin/env python3
"""Crawlt alle EN-Seiten der KaTech-Bestandsseite und legt Titel, H1, Fliesstext
und Bildliste als JSON ab. Grundlage fuer Inhalte und Stub-Intros des Demonstrators."""
import json, re, html, os, sys, time, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://katech-solutions.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
    return raw.decode("utf-8", errors="replace")


def strip_tags(fragment):
    fragment = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", fragment)
    fragment = re.sub(r"(?is)<br[^>]*>", "\n", fragment)
    fragment = re.sub(r"(?is)</(p|div|li|h[1-6]|td|tr)>", "\n", fragment)
    fragment = re.sub(r"(?s)<[^>]+>", " ", fragment)
    fragment = html.unescape(fragment)
    fragment = re.sub(r"[ \t]+", " ", fragment)
    lines = [l.strip() for l in fragment.split("\n")]
    return [l for l in lines if l]


def parse(url, doc):
    out = {"url": url}
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", doc)
    out["title"] = html.unescape(m.group(1)).strip() if m else ""
    m = re.search(r'(?is)<meta[^>]+name="description"[^>]+content="([^"]*)"', doc)
    out["description"] = html.unescape(m.group(1)).strip() if m else ""
    m = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", doc)
    out["h1"] = " ".join(strip_tags(m.group(1))) if m else ""

    # Inhaltsbereich des Nucima-Themes eingrenzen, sonst dominiert die Mega-Navigation
    body = doc
    for pat in (r'(?is)<div[^>]+id="content".*?(?=<div[^>]+id="footer")',
                r'(?is)<div[^>]+class="[^"]*content[^"]*".*?(?=<div[^>]+id="footer")',
                r"(?is)<body[^>]*>(.*)</body>"):
        m = re.search(pat, doc)
        if m:
            body = m.group(0)
            break
    lines = strip_tags(body)

    # Navigationsrauschen entfernen: sehr kurze Zeilen ohne Satzzeichen und Dubletten
    seen, text = set(), []
    for l in lines:
        if l in seen:
            continue
        seen.add(l)
        text.append(l)
    out["lines"] = text

    imgs = re.findall(r'<img[^>]+src="([^"]+)"', body)
    keep = []
    for i in dict.fromkeys(imgs):
        if "/wp-content/uploads/" in i or "/themes/nucima/images/" in i:
            if i.startswith("/"):
                i = BASE + i
            keep.append(i)
    out["images"] = keep
    return out


def main():
    urls = [l.strip() for l in open(os.path.join(HERE, "en-pages.txt"), encoding="utf-8") if l.strip()]
    urls.insert(0, BASE + "/")
    result, failed = {}, []
    for n, u in enumerate(urls, 1):
        try:
            doc = fetch(u)
            result[u] = parse(u, doc)
            print(f"{n}/{len(urls)} ok   {u}")
        except Exception as e:
            failed.append((u, str(e)))
            print(f"{n}/{len(urls)} FAIL {u}  {e}")
        time.sleep(0.25)
    with open(os.path.join(HERE, "pages.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"\nGespeichert: {len(result)} Seiten, {len(failed)} Fehler")
    for u, e in failed:
        print("  FAIL", u, e)


if __name__ == "__main__":
    main()
