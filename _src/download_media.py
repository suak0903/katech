#!/usr/bin/env python3
"""Laedt die in image-urls.json gesammelten Bilder der Bestandsseite herunter."""
import json, os, sys, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

d = json.load(open(os.path.join(HERE, "image-urls.json"), encoding="utf-8"))
urls = d["uploads"] + d["theme"] + d["khpartner"]
# Thumbnails ueberspringen, wenn das Original ebenfalls in der Liste steht
import re
by_stem = {}
for u in urls:
    stem = re.sub(r"-\d+x\d+(?=\.[a-z]+$)", "", u)
    by_stem.setdefault(stem, []).append(u)
pick = []
for stem, group in by_stem.items():
    original = [g for g in group if not re.search(r"-\d+x\d+\.[a-z]+$", g)]
    pick.append(original[0] if original else sorted(group)[-1])

ok = fail = skip = 0
manifest = []
for u in sorted(set(pick)):
    name = u.split("/")[-1].split("?")[0]
    host = "kh" if "khpartner" in u else ("th" if "/themes/" in u else "up")
    ziel = os.path.join(OUT, f"{host}_{name}")
    if os.path.exists(ziel) and os.path.getsize(ziel) > 0:
        skip += 1
        manifest.append({"url": u, "datei": os.path.basename(ziel)})
        continue
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        if len(data) < 400:
            raise ValueError("zu klein")
        open(ziel, "wb").write(data)
        manifest.append({"url": u, "datei": os.path.basename(ziel), "bytes": len(data)})
        ok += 1
    except Exception as e:
        print("  FAIL", u, e)
        fail += 1
    time.sleep(0.15)

json.dump(manifest, open(os.path.join(HERE, "assets-manifest.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"geladen {ok} | uebersprungen {skip} | fehlgeschlagen {fail} | Ziel {OUT}")
