#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator des KaTech-Demonstrators.

Erzeugt die komplette Seitenstruktur der Bestandsseite als statische Dateien.
Die Original-URL-Pfade bleiben erhalten (z. B. /cheese/cream-cheese/), damit
sichtbar wird, dass beim Umstieg nichts verloren geht. Chrome kommt aus einer
einzigen Quelle (gen_chrome.py) und ist auf allen Seiten byte-identisch.
"""
import json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import gen_lib as L
import gen_chrome as C
import inhalt as I
import struktur as S

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
DATEN = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
MEDIA = json.load(open(os.path.join(HERE, "media-map.json"), encoding="utf-8"))
NEWS_DATEI = os.path.join(HERE, "news-clean.json")
if not os.path.exists(NEWS_DATEI):
    NEWS_DATEI = os.path.join(HERE, "news.json")
NEWS = json.load(open(NEWS_DATEI, encoding="utf-8"))
SEITEN = DATEN["seiten"]
BAUM = DATEN["baum"]

geschrieben = []

TEAM_DATEI = os.path.join(HERE, "team.json")
TEAM = json.load(open(TEAM_DATEI, encoding="utf-8")) if os.path.exists(TEAM_DATEI) else []

# Eine einzige Quelle fuer die Bereichszugehoerigkeit. Menuemarkierung,
# Breadcrumb, Hub-Einordnung und Sitemap leiten sich daraus ab.
BEREICH = S.zuordnung(
    I.PRODUKTBEREICHE, BAUM,
    [n["slug"] for n in NEWS if n["slug"] != "news"],
    [p["slug"] for p in TEAM])

BEREICHS_TITEL = {b: t for b, t, _ in S.BEREICHE}
BEREICHS_ZIEL = {b: z for b, _, z in S.BEREICHE}


def bereich_von(slug):
    """Bereich einer Seite, leer wenn sie zu keinem gehoert."""
    return BEREICH.get(slug, "")


def aktiv_von(slug):
    """Wert fuer die Menuemarkierung: das Ziel des Bereichs."""
    b = bereich_von(slug)
    return BEREICHS_ZIEL.get(b, "")


def crumbs_von(root, slug, *, zwischen=None):
    """Breadcrumb-Pfad. Wurzel ist immer der Bereich aus der Zuordnung,
    damit Menuemarkierung und Pfad nicht auseinanderlaufen koennen."""
    weg = [("Start", root + "index.html")]
    b = bereich_von(slug)
    # Die Startseite eines Bereichs fuehrt sich nicht selbst als Zwischenglied
    ist_bereichsstart = b and S.BEREICHS_START.get(b) == slug
    if b and not ist_bereichsstart:
        weg.append((BEREICHS_TITEL[b], root + BEREICHS_ZIEL[b]))
    for titel, ziel in (zwischen or []):
        weg.append((titel, ziel))
    weg.append((BEREICHS_TITEL[b] if ist_bereichsstart else kurztitel(slug), None))
    return weg


def schreibe(zielpfad, html):
    voll = os.path.join(OUT, zielpfad.replace("/", os.sep))
    os.makedirs(os.path.dirname(voll), exist_ok=True)
    with open(voll, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    geschrieben.append(zielpfad)


def ziel(slug):
    """Original-Slug zu Ausgabepfad."""
    return (slug + "/index.html") if slug else "index.html"


def link(root, slug):
    return root + (slug + "/" if slug else "index.html")


def bild_von(slug):
    if slug in I.BEREICHS_BILD:
        return I.BEREICHS_BILD[slug]
    return MEDIA.get(slug)


def kurz(text, n=155):
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= n:
        return text
    schnitt = text[:n].rsplit(" ", 1)[0]
    return schnitt.rstrip(",.;:") + "."


def titel_von(slug):
    if slug in I.TITEL:
        return I.TITEL[slug]
    s = SEITEN.get(slug, {})
    t = (s.get("h1") or s.get("titel") or slug.split("/")[-1].replace("-", " ").title()).strip()
    t = re.sub(r"\s*\|.*$", "", t)
    return t


def kurztitel(slug):
    """Beschriftung fuer Navigation, Kacheln und Sitemap.

    Grundlage ist der Adressbestandteil, weil er kurz und eindeutig ist. Die
    Titel des Bestands taugen dafuer nicht: dort stehen Werbesaetze wie
    "Greek yogurt - the food of the gods". Wo der Adressbestandteil deutsch
    oder unverstaendlich ist, greift die Tabelle in inhalt.KURZTITEL."""
    if slug in I.KURZTITEL:
        return I.KURZTITEL[slug]
    letzte = slug.split("/")[-1]
    t = re.sub(r"^katech ", "", letzte.replace("-", " "))
    return t[:1].upper() + t[1:]


def intro_von(slug, n=150):
    if slug in I.BEREICHS_KURZTEXT:
        return I.BEREICHS_KURZTEXT[slug]
    s = SEITEN.get(slug, {})
    if s.get("absaetze"):
        return kurz(s["absaetze"][0], n)
    if s.get("description"):
        return kurz(s["description"], n)
    return ""


# ==========================================================================
# 1. Startseite
# ==========================================================================
def start():
    root = ""
    teile = []
    teile.append(L.hero(
        root,
        eyebrow="Texture and stabilising solutions",
        h1='We make food <em>work</em>.<br>Recipe by recipe.',
        sub="KaTech develops bespoke stabilising and emulsifying systems for food manufacturers "
            "across dairy, plant-based, savoury and bakery. Developed in our own pilot plants, "
            "produced in Germany, the UK and Poland.",
        bild="pilot-plant-wide",
        alt="A KaTech technologist working on a Romaco pilot plant vessel",
        cta=[("Explore our solutions", "solutions/", "btn--primary"),
             ("Make an enquiry", "contact-us/", "btn--ghost")],
        ribbon=[("2010", "founded in Lübeck"), ("95", "people across three countries"),
                ("BRC AA", "highest food safety rating"), ("4", "sites in DE, UK and PL")],
    ))

    # Produktwelten
    karten = []
    for slug in I.START_BEREICHE:
        karten.append(L.karte(
            root, titel=kurztitel(slug), text=intro_von(slug, 108),
            ziel=link(root, slug), bild=bild_von(slug) or "sensory-panel",
            zusatz=f"{len(BAUM.get(slug, []))} applications" if BAUM.get(slug) else "",
            mehr="View area"))
    teile.append(f'''<section class="sec" id="solutions">
  <div class="wrap">
    {L.sec_kopf(eyebrow="What we solve", h2="Your product category, our formulation work.",
                lead="Eleven application areas, more than one hundred product types. Every solution "
                     "is developed for your recipe, your process and your raw materials.")}
    {L.raster(karten, 3)}
    <div class="btn-row btn-row--single rv" style="margin-top:34px">
      <a class="btn btn--outline" href="solutions/">All product areas</a>
    </div>
  </div>
</section>''')

    # Split-Bloecke: das Ingredion-Signaturmuster
    teile.append(L.split(
        root, ton="brand", eyebrow="Plant-based",
        h2="The category that decides who eats what in ten years.",
        text=["Plant-based products only succeed if they taste and feel like what they replace. "
              "Texture is where most of them fail.",
              "Our centre of excellence for meat and fish alternatives in Lübeck lets us build and "
              "test that texture on real machinery, not on paper."],
        liste=["Meat and fish alternatives on dedicated pilot equipment",
               "Plant-based dairy: yogurt, cream, drinks, desserts, cheese",
               "Clean label and allergen-free routes"],
        cta=("Plant-based solutions", "vegan/"),
        bild=bild_von("vegan/plant-based-mince") or "sensory-panel",
        alt="Plant-based mince developed at KaTech"))

    teile.append(L.split(
        root, ton="teal", eyebrow="How we work", flip=True,
        h2="We start with your process, not with our catalogue.",
        text=["A stabiliser that works in the lab and fails on your line is worth nothing. "
              "That is why our technologists work hands-on, from the first trial to the factory run.",
              "Everything is confidential, and everything stays yours."],
        liste=["Replicating an existing product to reduce cost",
               "Developing a new product from a concept",
               "Fixing a texture or stability problem in production"],
        cta=("How we work", "how-we-work/"),
        bild="lab-measurement",
        alt="KaTech technologist taking a measurement in the development laboratory"))

    # Kennzahlen und Zertifikate
    teile.append(f'''<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Quality and safety", h2="Certified where it counts.",
                lead="Food safety has been the focus since the company started in 2011. "
                     "KaTech holds the rare BRC Food AA rating and is audited against every "
                     "standard our customers need.", zentriert=True)}
    {L.zertifikate(root, I.ZERTIFIKATE)}
    <div class="btn-row btn-row--single rv" style="margin:38px auto 0">
      <a class="btn btn--outline" href="certifications/">All certifications</a>
    </div>
  </div>
</section>''')

    # Prozess
    teile.append(f'''<section class="sec">
  <div class="wrap">
    {L.sec_kopf(eyebrow="From idea to line", h2="Four steps, one team.",
                lead="The same technologists who design your formulation stand next to your "
                     "production line when it runs for the first time.")}
    {L.schritte(I.SCHRITTE)}
  </div>
</section>''')

    # Anlagen
    teile.append(L.split(
        root, ton="ink", eyebrow="Our facilities",
        h2="Pilot plants in Lübeck and Cheshire. Production in Reinfeld.",
        text=["Development happens on equipment that behaves like yours. Production runs in a "
              "purpose-built, allergen-controlled blending site in northern Germany.",
              "Our subsidiary near Poznań serves the Polish market from its own temperature "
              "and humidity controlled warehouse."],
        cta=("See our facilities", "our-facilities/"),
        bild="blending-tower",
        alt="Blending tower at the KaTech production site"))

    # Highlights: die sieben Aussagen des Bestands-Karussells als laufendes Band
    teile.append(I.highlights_band(root))

    # News
    aktuell = [n for n in NEWS if n["slug"] != "news"][:3]
    eintraege = "".join(f'''<article class="newsitem">
      <time datetime="{n['datum']}">{I.datum_lang(n['datum'])}</time>
      <div>
        <a href="{link(root, n['slug'])}"><h3>{L.esc(n['titel'])}</h3></a>
        <p>{L.esc(kurz(n['absaetze'][0] if n['absaetze'] else '', 190))}</p>
      </div>
    </article>''' for n in aktuell)
    teile.append(f'''<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow="News", h2="What is happening at KaTech.")}
    <div class="rv">{eintraege}</div>
    <div class="btn-row btn-row--single rv" style="margin-top:34px">
      <a class="btn btn--outline" href="news/">All news</a>
    </div>
  </div>
</section>''')

    # Abschluss-CTA
    teile.append(f'''<section class="sec sec--teal">
  <div class="wrap wrap--narrow center">
    {L.sec_kopf(eyebrow="Talk to a technologist",
                h2="Tell us what the product has to do.",
                lead="Describe the product, the process and the problem. You will hear back from "
                     "someone who has built it before, not from a call centre.", zentriert=True)}
    <div class="btn-row rv" style="margin-inline:auto">
      <a class="btn btn--ghost" href="contact-us/">Make an enquiry</a>
      <a class="btn btn--ghost" href="mailto:hello@katech-solutions.com">hello@katech-solutions.com</a>
    </div>
  </div>
</section>''')

    schreibe("index.html", L.seite(
        "index.html",
        "Stabiliser and emulsifier solutions for the food industry",
        "KaTech develops bespoke stabilising and texturising systems for dairy, plant-based, "
        "savoury and bakery products. Pilot plants in Germany and the UK, production in Reinfeld. "
        "Part of Ingredion.",
        "\n".join(teile), og="og-home.jpg", jsonld=I.LD_ORG,
        extra_head=L.hero_preload(root, "pilot-plant-wide")))


# ==========================================================================
# 2. Hub-Seiten
# ==========================================================================
def hub_solutions():
    slug, root = "solutions", "../"
    bloecke = []
    for cluster_id, cluster_titel, cluster_text, bereiche in I.CLUSTER:
        karten = [L.karte(root, titel=kurztitel(b), text=intro_von(b, 108),
                          ziel=link(root, b), bild=bild_von(b) or "sensory-panel",
                          zusatz=f"{len(BAUM.get(b, []))} applications" if BAUM.get(b) else "",
                          mehr="View area") for b in bereiche]
        bloecke.append(f'''<section class="sec{' sec--sand' if cluster_id in ('savoury',) else ''}" id="{cluster_id}">
  <div class="wrap">
    {L.sec_kopf(eyebrow=cluster_titel, h2=cluster_text[0], lead=cluster_text[1])}
    {L.raster(karten, 3)}
  </div>
</section>''')

    inhalt = L.subhero(root, crumbs=[("Start", root + "index.html"), ("Solutions", None)],
                       eyebrow="Product areas", h1="Everything we formulate for.",
                       sub="Eleven application areas with more than one hundred product types. "
                           "Each one is a starting point, never a finished recipe.",
                       bild="sensory-panel",
                       alt="Sensory panel with product samples at KaTech") + "\n" + "\n".join(bloecke)
    inhalt += f'''
<section class="sec sec--teal">
  <div class="wrap wrap--narrow center">
    {L.sec_kopf(h2="Your category is not listed?",
                lead="Most of our work starts with a product that does not fit a category. "
                     "Describe it and we will tell you honestly whether we can help.", zentriert=True)}
    <div class="btn-row btn-row--single rv" style="margin-inline:auto">
      <a class="btn btn--ghost" href="{root}contact-us/">Make an enquiry</a>
    </div>
  </div>
</section>'''
    schreibe(ziel(slug), L.seite(ziel(slug), "Solutions",
             "All KaTech application areas: dairy and dairy alternatives, plant-based meat and "
             "fish, savoury, bakery and fruit.", inhalt, aktiv="solutions/", og="og-solutions.jpg",
             jsonld=I.ld_liste("Product areas", [(kurztitel(b), L.PAGES_URL + b + "/")
                                                 for _, _, _, bs in I.CLUSTER for b in bs])))


def hub_generisch(slug, titel, eyebrow, h1, sub, gruppen, og, bild="hq-luebeck",
                  zusatz=""):
    root = "../"
    bloecke = []
    for n, (gruppen_titel, gruppen_lead, eintraege) in enumerate(gruppen):
        kacheln = []
        for i, (s, t, t2) in enumerate(eintraege, 1):
            kacheln.append(L.kachel(
                nummer=f"{i:02d}",
                titel=kurztitel(s) if s in SEITEN else t,
                text=intro_von(s, 96) or t2 or I.KACHEL_LEER,
                ziel=link(root, s),
                leer=I.ist_leer(s)))
        bloecke.append(f'''<section class="sec{" sec--sand" if n % 2 else ""}">
  <div class="wrap">
    {L.sec_kopf(eyebrow=gruppen_titel, h2=gruppen_lead[0], lead=gruppen_lead[1])}
    <div class="grid grid--3 rv">{"".join(kacheln)}</div>
  </div>
</section>''')
    if zusatz:
        if slug == "our-facilities":
            bloecke.append(zusatz.format(
                kopf=L.sec_kopf(eyebrow="Impressions", h2="Inside the sites."),
                galerie=L.galerie(root, [
                    ("hq-luebeck", "KaTech head office in Lübeck"),
                    ("blending-tower", "Blending tower at the production site"),
                    ("lab-measurement", "Measurement in the development laboratory"),
                    ("sensory-panel", "Sensory panel with product samples"),
                    ("warehouse", "Temperature controlled warehouse"),
                    ("plant-reinfeld", "Production site in northern Germany")])))
        else:
            bloecke.append(zusatz.format(
                root=root,
                kopf=L.sec_kopf(eyebrow="Sites and production",
                                h2="Where the work happens.",
                                lead="Development suites in Lübeck and Cheshire, production and "
                                     "warehousing in northern Germany, a sales office in Poland.",
                                zentriert=True)))
    inhalt = L.subhero(root, crumbs=crumbs_von(root, BEREICHS_SEITE.get(slug, slug)),
                       eyebrow=eyebrow, h1=h1, sub=sub, bild=bild,
                       alt=titel) + "\n" + "\n".join(bloecke)
    schreibe(ziel(slug), L.seite(ziel(slug), titel, sub, inhalt,
                                 aktiv=aktiv_von(BEREICHS_SEITE.get(slug, slug)), og=og))


# Hub-Slug zu der Seite, deren Bereichszuordnung gilt
BEREICHS_SEITE = {"expertise": "expertise", "company": "company",
                  "our-facilities": "our-facilities"}


# ==========================================================================
# 3. Bereichsseiten und Produktseiten
# ==========================================================================
def bereichsseite(slug):
    root = "../"
    s = SEITEN.get(slug, {})
    unter = BAUM.get(slug, [])
    absaetze = s.get("absaetze", [])
    kopf_text = absaetze[0] if absaetze else ""
    rest = absaetze[1:6]

    # Seiten, die im Bestand woanders liegen, hier aber hingehoeren
    unter = unter + S.FREMDE_KINDER.get(slug, [])

    def karte_fuer(u):
        return L.karte(root, titel=kurztitel(u), text=intro_von(u, 96),
                       ziel=root + u + "/", bild=bild_von(u), mehr="Open",
                       leer=I.ist_leer(u))

    gruppen = S.VEGAN_GRUPPEN if slug == "vegan" else None
    karten = [karte_fuer(u) for u in unter]

    prosa_bloecke = [L.absatz(t) for t in rest]
    prosa_html = ""
    if prosa_bloecke:
        prosa_html = f'''<section class="sec">
  <div class="wrap wrap--narrow">
    {L.prosa(prosa_bloecke)}
  </div>
</section>'''

    kacheln_html = ""
    if gruppen:
        # Vier Gruppen statt achtzehn Seiten nebeneinander. Wo der Bestand eine
        # Kopfseite hat, fuehrt sie die Gruppe an; sonst bleibt es bei einer
        # Ueberschrift, damit keine Seite erfunden wird.
        bloecke = []
        for n, (gruppe, kopfseite, kinder) in enumerate(gruppen):
            liste = ([kopfseite] if kopfseite else []) + kinder
            lead = intro_von(kopfseite, 150) if kopfseite else ""
            bloecke.append(f'''<section class="sec{" sec--sand" if n % 2 == 0 else ""}">
  <div class="wrap">
    {L.sec_kopf(eyebrow=gruppe, h2=f"{len(liste)} product types.", lead=lead)}
    {L.raster([karte_fuer(u) for u in liste], 3)}
  </div>
</section>''')
        kacheln_html = "\n".join(bloecke)
    elif karten:
        kacheln_html = f'''<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Applications", h2=f"{len(unter)} product types in this area.",
                lead="Every one of these is a formulation route we have already walked. "
                     "The detail page tells you what the product has to do and where the "
                     "technical work usually sits.")}
    {L.raster(karten, 3)}
  </div>
</section>'''

    inhalt = L.subhero(
        root, crumbs=crumbs_von(root, slug),
        eyebrow="Product area", h1=L.esc(titel_von(slug)),
        sub=kurz(kopf_text, 230), bild=bild_von(slug) or "sensory-panel",
        alt=kurztitel(slug))
    inhalt += "\n" + prosa_html + "\n" + kacheln_html + "\n" + cta_block(root)
    schreibe(ziel(slug), L.seite(
        ziel(slug), kurztitel(slug),
        kurz(s.get("description") or kopf_text, 158) or f"KaTech solutions for {kurztitel(slug)}.",
        inhalt, aktiv=aktiv_von(slug),
        og="og-solutions.jpg",
        jsonld=I.ld_liste(kurztitel(slug), [(kurztitel(u), L.PAGES_URL + u + "/") for u in unter])))


def produktseite(slug):
    root = "../" * (slug.count("/") + 1)
    s = SEITEN.get(slug, {})
    bereich = slug.split("/")[0]
    absaetze = s.get("absaetze", [])
    geschwister = [g for g in BAUM.get(bereich, []) if g != slug]

    bloecke = [L.absatz(t) for t in absaetze[:8]]
    # Drei Faelle: (a) im Original nur ein Bild, hier vollstaendig uebernommen,
    # (b) im Original ohne jeden Inhalt, (c) hier nicht ausgebaut.
    nur_bild = I.ist_nur_bild(slug) and bool(bild_von(slug))
    ist_stub = not bloecke and not nur_bild
    if nur_bild and not bloecke:
        bloecke = [L.absatz(I.BILD_HINWEIS)]
    elif ist_stub:
        bloecke = [I.stub_kasten(root, slug)]
    if s.get("listen"):
        bloecke.append(L.faktenkasten("Covered in this application",
                                      s["listen"][:8]))

    bild_html = ""
    b = bild_von(slug)
    if b:
        bild_html = f'''<figure style="margin:0 0 30px">
      <picture><source srcset="{root}media/{b}.webp" type="image/webp">
      <img src="{root}media/{b}.jpg" alt="{L.esc(kurztitel(slug))}" loading="lazy" decoding="async" width="800" height="533"></picture>
    </figure>'''

    nachbarn = ""
    if geschwister:
        kacheln = [L.kachel(nummer=f"{i:02d}", titel=kurztitel(g), text=intro_von(g, 82),
                            ziel=root + g + "/") for i, g in enumerate(geschwister[:6], 1)]
        nachbarn = f'''<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow=kurztitel(bereich), h2="More in this area.")}
    <div class="grid grid--3 rv">{"".join(kacheln)}</div>
    <div class="btn-row btn-row--single rv" style="margin-top:30px">
      <a class="btn btn--outline" href="{root}{bereich}/">All of {kurztitel(bereich)}</a>
    </div>
  </div>
</section>'''

    inhalt = L.subhero(
        root, crumbs=crumbs_von(root, slug,
                                zwischen=[(kurztitel(bereich), root + bereich + "/")]),
        eyebrow=kurztitel(bereich),
        h1=L.esc(titel_von(slug)) + (" " + I.stub_marke(slug) if ist_stub else ""),
        sub=kurz(absaetze[0], 190) if absaetze else "")
    inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow">
    {bild_html}
    {L.prosa(bloecke)}
  </div>
</section>
{nachbarn}
{cta_block(root)}'''
    schreibe(ziel(slug), L.seite(
        ziel(slug), kurztitel(slug),
        kurz(s.get("description") or (absaetze[0] if absaetze else ""), 158)
        or f"KaTech stabilising solutions for {kurztitel(slug).lower()}.",
        inhalt, aktiv=aktiv_von(slug), og="og-solutions.jpg"))


def cta_block(root):
    return f'''<section class="sec sec--teal">
  <div class="wrap wrap--narrow center">
    {L.sec_kopf(h2="Bring us the product.",
                lead="Tell us what it has to do, how it is produced and where it currently fails. "
                     "We will tell you what is possible.", zentriert=True)}
    <div class="btn-row rv" style="margin-inline:auto">
      <a class="btn btn--ghost" href="{root}contact-us/">Make an enquiry</a>
      <a class="btn btn--ghost" href="{root}how-we-work/">How we work</a>
    </div>
  </div>
</section>'''


# ==========================================================================
# 4. Textseiten des Unternehmens
# ==========================================================================
def textseite(slug, *, eyebrow, crumbs_extra=None, bild=None, extra_html="", aktiv=None):
    root = "../" * (slug.count("/") + 1)
    s = SEITEN.get(slug, {})
    absaetze = s.get("absaetze", [])
    bloecke = [L.absatz(t) for t in absaetze]
    if s.get("listen"):
        bloecke.append(L.faktenkasten("At a glance", s["listen"][:10]))
    # Seiten ohne Bestandsinhalt werden sichtbar als solche gekennzeichnet,
    # sonst wirken sie wie ein Fehler statt wie eine gezogene Grenze.
    ist_stub = not bloecke
    if ist_stub:
        bloecke = [I.stub_kasten(root, slug)]

    crumbs = crumbs_von(root, slug, zwischen=crumbs_extra)

    inhalt = L.subhero(root, crumbs=crumbs, eyebrow=eyebrow,
                       h1=L.esc(titel_von(slug)) + (" " + I.stub_marke(slug) if ist_stub else ""),
                       sub=kurz(absaetze[0], 200) if absaetze else "",
                       bild=bild, alt=kurztitel(slug))
    inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow">
    {L.prosa(bloecke)}
  </div>
</section>
{extra_html}
{cta_block(root)}'''
    schreibe(ziel(slug), L.seite(
        ziel(slug), kurztitel(slug),
        kurz(s.get("description") or (absaetze[0] if absaetze else ""), 158) or I.PLATZHALTER[:150],
        inhalt, aktiv=aktiv if aktiv is not None else aktiv_von(slug),
        og="og-" + (bereich_von(slug) or "company") + ".jpg"))


def main():
    print("Startseite ...")
    start()
    print("Hubs ...")
    hub_solutions()
    I.baue_hubs(hub_generisch)

    print("Bereichs- und Produktseiten ...")
    bereiche = [b for b in BAUM if BAUM[b] and b not in I.KEINE_BEREICHE]
    for b in bereiche:
        if b in I.PRODUKTBEREICHE:
            bereichsseite(b)
            for u in BAUM[b]:
                produktseite(u)
    print(f"  {len(bereiche)} Bereiche")

    print("Unternehmens- und Expertise-Seiten ...")
    I.baue_textseiten(textseite)

    print("Sonderseiten ...")
    I.baue_sonderseiten(schreibe, SEITEN, BAUM, NEWS, MEDIA, kurztitel, titel_von, intro_von, kurz, geschrieben)

    print(f"\nGeschrieben: {len(geschrieben)} Seiten")
    return geschrieben


if __name__ == "__main__":
    main()
