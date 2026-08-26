#!/usr/bin/env python3
"""Bereitet die Bestandsbilder fuer den Demonstrator auf:
Schluesselmotive per Real-ESRGAN hochskalieren, alle Bilder in WebP + JPG
in den benoetigten Groessen ausgeben, Metadaten strippen."""
import json, os, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
MEDIA = os.path.abspath(os.path.join(HERE, "..", "media"))
ESRGAN = r"C:\Users\suak\tools\realesrgan\realesrgan-ncnn-vulkan.exe"
os.makedirs(MEDIA, exist_ok=True)

# Motive, die gross ausgespielt werden und deshalb vorher hochskaliert werden
UPSCALE = {
    "up_KATECH_0870.jpg": "pilot-plant",          # Technologin an der Pilotanlage (Hero)
    "up_KATECH_0151.jpg": "sensory-panel",        # Verkostungsreihe im Labor
    "up_production-facilities-germany3.jpg": "lab-measurement",
    "up_production-facilities-germany2.jpg": "blending-tower",
    "up_KATECH_2048.jpg": "hq-luebeck",
    "up_production-facilities-germany6.jpg": "warehouse",
    "up_production-facilities-germany4.jpg": "development-meeting",
    "up_KATECH_0982.jpg": "reception",
    "kh_Ingredients.jpg": "raw-materials",
    "kh_130815_Raetzke_KATECH_0021-300x199.jpg": "plant-reinfeld",
}

# Zielbreiten je Rolle
GROESSEN = {"hero": 2400, "wide": 1600, "block": 1200, "card": 800, "thumb": 480}


def magick(*args):
    subprocess.run(["magick", *args], check=True)


def upscale():
    for quelle, ziel in UPSCALE.items():
        src = os.path.join(ASSETS, quelle)
        out = os.path.join(ASSETS, f"_up_{ziel}.png")
        if not os.path.exists(src):
            print("  fehlt:", quelle)
            continue
        if os.path.exists(out):
            continue
        subprocess.run([ESRGAN, "-i", src, "-o", out, "-n", "realesrgan-x4plus", "-s", "4"],
                       check=True, capture_output=True)
        print("  hochskaliert:", ziel)


def ausgeben(src, name, rolle, seitenverhaeltnis=None):
    """Schreibt name.webp und name.jpg in der Zielbreite der Rolle."""
    breite = GROESSEN[rolle]
    argumente = [src, "-strip", "-auto-orient"]
    if seitenverhaeltnis:
        w, h = seitenverhaeltnis
        argumente += ["-resize", f"{breite}x{int(breite * h / w)}^",
                      "-gravity", "center", "-extent", f"{breite}x{int(breite * h / w)}"]
    else:
        argumente += ["-resize", f"{breite}x>"]
    magick(*argumente, "-quality", "82", os.path.join(MEDIA, name + ".webp"))
    magick(*argumente, "-quality", "85", os.path.join(MEDIA, name + ".jpg"))


def main():
    print("Hochskalieren ...")
    upscale()

    print("Grosse Motive ausgeben ...")
    rollen = {
        "pilot-plant": ("hero", (16, 9)),
        "sensory-panel": ("block", (4, 3)),
        "lab-measurement": ("block", (4, 3)),
        "blending-tower": ("block", (4, 3)),
        "hq-luebeck": ("block", (4, 3)),
        "warehouse": ("card", (3, 2)),
        "development-meeting": ("block", (4, 3)),
        "reception": ("card", (3, 2)),
        "raw-materials": ("block", (4, 3)),
        "plant-reinfeld": ("card", (3, 2)),
    }
    for name, (rolle, ar) in rollen.items():
        src = os.path.join(ASSETS, f"_up_{name}.png")
        if not os.path.exists(src):
            continue
        ausgeben(src, name, rolle, ar)
        print("   ", name, rolle)
    # Hero zusaetzlich als breites 21:9 fuer Desktop
    src = os.path.join(ASSETS, "_up_pilot-plant.png")
    if os.path.exists(src):
        ausgeben(src, "pilot-plant-wide", "hero", (21, 9))

    print("Seitenbilder ausgeben ...")
    data = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
    manifest = {}
    for slug, s in data["seiten"].items():
        if not s["bild"]:
            continue
        datei = s["bild"].split("/")[-1].split("?")[0]
        host = "kh" if "khpartner" in s["bild"] else "up"
        kandidaten = [os.path.join(ASSETS, f"{host}_{datei}"),
                      os.path.join(ASSETS, f"up_{datei}"),
                      os.path.join(ASSETS, f"kh_{datei}"),
                      os.path.join(ASSETS, f"th_{datei}")]
        src = next((k for k in kandidaten if os.path.exists(k)), None)
        if not src:
            continue
        name = "p-" + (slug.replace("/", "-") or "home")
        try:
            ausgeben(src, name, "card", (3, 2))
            manifest[slug] = name
        except Exception as e:
            print("   FEHLER", slug, e)
    json.dump(manifest, open(os.path.join(HERE, "media-map.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"Seitenbilder: {len(manifest)}")
    print("Ziel:", MEDIA)


if __name__ == "__main__":
    main()
