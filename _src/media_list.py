#!/usr/bin/env python3
"""Listet alle Medien der Bestandsseite ueber die WordPress-REST-API auf
(Datei-URL, Alt-Text, Groesse, Aufnahmedatum) und legt sie als JSON ab."""
import json, os, sys, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://katech-solutions.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for versuch in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            time.sleep(6 * (versuch + 1))
    raise RuntimeError("Abruf fehlgeschlagen: " + url)


items, page = [], 1
while True:
    batch = get(f"{BASE}/wp-json/wp/v2/media?per_page=100&page={page}&_fields=id,source_url,alt_text,media_details,date,title")
    if not batch:
        break
    for m in batch:
        det = m.get("media_details") or {}
        items.append({
            "id": m["id"],
            "url": m.get("source_url", ""),
            "alt": (m.get("alt_text") or "").strip(),
            "titel": ((m.get("title") or {}).get("rendered") or "").strip(),
            "w": det.get("width"), "h": det.get("height"),
            "datum": m.get("date", "")[:10],
        })
    print(f"  Seite {page}: {len(batch)} Eintraege (gesamt {len(items)})")
    if len(batch) < 100:
        break
    page += 1
    time.sleep(0.8)

json.dump(items, open(os.path.join(HERE, "media.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Gesamt:", len(items), "-> media.json")
