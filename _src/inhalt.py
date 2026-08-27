#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Redaktionelle Daten und Sonderseiten des Demonstrators.
Alle Fakten stammen aus der Bestandsseite (siehe _src/data.json und news.json)."""
import json, os, re

import gen_lib as L

# --------------------------------------------------------------------------
# Stammdaten aus dem Bestand (Impressum und Kontaktseite der Originalseite)
# --------------------------------------------------------------------------
STANDORTE = [
    {"name": "Head office and development", "ort": "Lübeck, Germany",
     "adresse": ["KaTech Ingredient Solutions GmbH", "Aegidienstraße 22", "23552 Lübeck", "Germany"],
     "tel": "+49 451 4070 2-0", "telhref": "+4945140702000",
     "fax": "+49 451 4070 2-377", "mail": "hello@katech-solutions.com",
     "karte": "https://www.google.com/maps?q=Aegidienstra%C3%9Fe+22,+23552+L%C3%BCbeck&output=embed",
     "bild": "hq-luebeck"},
    {"name": "Production and warehouse", "ort": "Wesenberg, Germany",
     "adresse": ["KaTech Ingredient Solutions GmbH", "Buurdieksweg 4", "23858 Wesenberg", "Germany"],
     "tel": "+49 451 4070 2-0", "telhref": "+4945140702000",
     "fax": "+49 451 4070 2-125", "mail": "verkaufsservice@katech-solutions.com",
     "karte": "https://www.google.com/maps?q=Buurdieksweg+4,+23858+Wesenberg&output=embed",
     "bild": "blending-tower"},
    {"name": "Technical development suite", "ort": "Ellesmere Port, United Kingdom",
     "adresse": ["KaTech Ingredient Solutions Ltd", "Unit 19 Venture Point",
                 "Stanney Mill Road", "Ellesmere Port, Cheshire CH2 4NE", "United Kingdom"],
     "tel": "+44 151 357 3700", "telhref": "+441513573700",
     "fax": "+44 151 357 4103", "mail": "custservuk@katech-solutions.com",
     "karte": "https://www.google.com/maps?q=Venture+Point+Stanney+Mill+Road+Ellesmere+Port+CH2+4NE&output=embed",
     "bild": "warehouse"},
    {"name": "Sales office", "ort": "Stęszew, Poland",
     "adresse": ["KaTech Ingredient Solutions Sp. z o. o.", "ul. Powstańców Wlkp. 49",
                 "62-060 Stęszew", "Poland"],
     "tel": "+48 61 67 07 001", "telhref": "+48616707001",
     "fax": "+48 61 67 07 001", "mail": "kontakt@katech-solutions.com",
     "karte": "https://www.google.com/maps?q=ul.+Powsta%C5%84c%C3%B3w+Wlkp.+49,+62-060+St%C4%99szew&output=embed",
     "bild": "reception"},
]

GESCHAEFTSFUEHRUNG = ["Cyril Carrat", "Michael O'Riordan", "Marcel Hergett", "Matthias Reeb"]
HANDELSREGISTER = "Local Court of Lübeck, HRB 12373 HL"

PLATZHALTER = "This page is carried over from the existing site structure."

# Marke im Seitenkopf und Kasten im Inhalt, wenn eine Seite bewusst noch
# nicht ausgebaut ist. Ohne diese Kennzeichnung wirkt eine solche Seite wie
# ein Fehler statt wie eine gezogene Grenze.
# Seiten, die auf der Bestandsseite tatsaechlich keinen Inhalt tragen.
# Ermittelt mit leerpruefung.py: der komplette Inhaltsbereich wurde auf Text,
# Listen, Tabellen, Bilder, Downloads und eingebettete Inhalte untersucht.
def _leere_laden():
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leerpruefung.json")
    if not os.path.exists(pfad):
        return set()
    return set(json.load(open(pfad, encoding="utf-8")).get("leer", []))


def _kategorie_laden(schluessel):
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leerpruefung.json")
    if not os.path.exists(pfad):
        return set()
    return set(json.load(open(pfad, encoding="utf-8")).get(schluessel, []))


LEER_IM_ORIGINAL = _kategorie_laden("leer")
# Seiten, die im Bestand ausschliesslich ein Produktbild tragen. Sie sind hier
# vollstaendig uebernommen und duerfen deshalb keinen Mangel-Hinweis bekommen.
NUR_BILD_IM_ORIGINAL = _kategorie_laden("nur_bild")


def ist_nur_bild(slug):
    return slug in NUR_BILD_IM_ORIGINAL


def _reiter_laden():
    """Die drei Reiter, die jede Produktseite des Bestands unter der
    Beschreibung fuehrt: New product, Troubleshooting, Cost optimisation.
    Der erste Extraktor hatte sie uebersehen (Suat 27.08.)."""
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content2.json")
    if not os.path.exists(pfad):
        return {}
    roh = json.load(open(pfad, encoding="utf-8"))
    return {s: e["reiter"] for s, e in roh.items() if e.get("reiter")}


REITER = _reiter_laden()


def reiter_block(root, slug):
    """Die drei Beratungswege als Reiter, wie im Bestand - nur sauberer.

    Ohne JavaScript stehen alle drei Felder untereinander und sind vollstaendig
    lesbar; erst das Skript macht daraus eine Reiterleiste. So geht nichts
    verloren, wenn es nicht laeuft (Suat 27.08.).
    """
    r = REITER.get(slug)
    if not r:
        return ""
    kennung = slug.replace("/", "-")
    knoepfe, felder = [], []
    for n, (kuerzel, eintrag) in enumerate(r.items()):
        koerper, liste = [], []
        for b in eintrag["bloecke"]:
            if b["tag"] == "li":
                liste.append(b["text"])
                continue
            if liste:
                koerper.append("<ul>" + "".join(f"<li>{L.esc(x)}</li>" for x in liste) + "</ul>")
                liste = []
            koerper.append(f"<p>{L.esc(b['text'])}</p>")
        if liste:
            koerper.append("<ul>" + "".join(f"<li>{L.esc(x)}</li>" for x in liste) + "</ul>")

        id_knopf, id_feld = f"t-{kennung}-{n}", f"p-{kennung}-{n}"
        erster = "true" if n == 0 else "false"
        knoepfe.append(
            f'<button class="tabs__b" role="tab" id="{id_knopf}" type="button" '
            f'aria-controls="{id_feld}" aria-selected="{erster}" '
            f'tabindex="{0 if n == 0 else -1}">'
            f'<span class="tabs__n">{n + 1:02d}</span>'
            f'<span class="tabs__t">{L.esc(eintrag["titel"])}</span></button>')
        felder.append(
            f'<div class="tabs__p" role="tabpanel" id="{id_feld}" '
            f'aria-labelledby="{id_knopf}" tabindex="0">'
            f'<h3 class="tabs__h">{L.esc(eintrag["titel"])}</h3>'
            f'{"".join(koerper)}</div>')

    return f'''<section class="sec sec--sand">
  <div class="wrap wrap--narrow">
    {L.sec_kopf(eyebrow="How we can help", h2="Three ways into this product.",
                lead="Whether you are building it new, fixing something that goes wrong in "
                     "production, or looking for cost in the recipe.")}
    <div class="tabs rv" data-tabs>
      <div class="tabs__bar" role="tablist" aria-label="Three ways into this product">
        {"".join(knoepfe)}
      </div>
      <div class="tabs__box">{"".join(felder)}</div>
    </div>
  </div>
</section>'''


def _bestand_laden():
    """Alle Adressen, die es auf der Bestandsseite tatsaechlich gibt. Nur fuer
    sie darf ein Verweis dorthin gesetzt werden; die Hub-Seiten dieses
    Entwurfs existieren im Original nicht."""
    hier = os.path.dirname(os.path.abspath(__file__))
    vorhanden = set()
    d = os.path.join(hier, "data.json")
    if os.path.exists(d):
        vorhanden |= {s for s in json.load(open(d, encoding="utf-8"))["seiten"] if s}
    for datei in ("news-clean.json", "team.json"):
        pf = os.path.join(hier, datei)
        if os.path.exists(pf):
            vorhanden |= {e["slug"] for e in json.load(open(pf, encoding="utf-8"))}
    vorhanden.discard("bakery-old")   # liefert im Bestand 404
    return vorhanden


IM_BESTAND = _bestand_laden()

# Seiten, die im Bestand Inhalt tragen, hier aber bewusst nicht ausgebaut sind.
# purchasing traegt dort nur eine interne Notiz, die einen Mitarbeiter
# namentlich vorfuehrt.
# Kein Eintrag mehr. "purchasing" stand hier, ist aber im Bestand nicht
# unfertig, sondern leer: die Seite traegt dort nur die interne Notiz
# "Steve Williams needs to put something here". Sie wird deshalb wie jede
# andere leere Bestandsseite behandelt; die Notiz wird nicht uebernommen,
# weil sie einen Mitarbeiter namentlich vorfuehrt (Suat 27.08., Punkt 12).
NICHT_AUSGEBAUT = set()


def ist_nicht_ausgebaut(slug):
    return slug in NICHT_AUSGEBAUT
KACHEL_LEER = "This page carries no content on the existing site."


def ist_leer(slug):
    return slug in LEER_IM_ORIGINAL


STUB_MARKE_LEER = '<span class="stubtag stubtag--leer">No content in the original</span>'
STUB_MARKE_OFFEN = '<span class="stubtag">Not built out in this preview</span>'


def stub_marke(slug):
    return STUB_MARKE_LEER if ist_leer(slug) else STUB_MARKE_OFFEN


BILD_HINWEIS = ("On the existing site this page shows a product photograph and no text. "
                "The photograph is carried over here; nothing else was there to carry.")


def stub_kasten(root, slug):
    """Hinweis auf Seiten ohne Inhalt. Der Wortlaut haengt davon ab, ob im
    Original nichts steht oder ob nur diese Vorschau die Seite nicht ausgebaut
    hat. Beide Faelle verlinken die Originalseite, damit die Aussage
    nachpruefbar ist."""
    original = "https://katech-solutions.com/" + (slug + "/" if slug else "")
    if ist_leer(slug):
        h2 = "This page has no content on the existing site."
        absaetze = (
            "<p>The page exists in your current site structure, and it is carried over here at "
            "its original address so that no link runs into a dead end. On the existing site it "
            "shows a heading and nothing else: no text, no images, no downloads.</p>"
            "<p>It is kept visible rather than quietly dropped, so that the gap is where it "
            "belongs, in plain sight. Use the link below to check the original for yourself.</p>")
    else:
        h2 = "This page is not built out in this preview."
        absaetze = (
            "<p>The existing site carries content here, but it was not part of this preview. "
            "The page is kept at its original address so that no link runs into a dead end.</p>"
            "<p>In the real project it is filled like every other one. It is shown this way on "
            "purpose rather than quietly left out, so you can see exactly where the boundary of "
            "this preview runs.</p>")
    return f'''<div class="stub rv">
      <div class="stub__head">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <circle cx="10" cy="10" r="8.6" stroke="currentColor" stroke-width="1.7"/>
          <path d="M10 5.4V10l3.2 2.2" stroke="currentColor" stroke-width="1.7"/></svg>
        <h2>{h2}</h2>
      </div>
      {absaetze}
      <div class="stub__links">
        <a class="btn btn--outline" href="{original}" target="_blank" rel="noopener">See this page on the original site</a>
        <a class="btn btn--outline" href="{root}sitemap/">Full sitemap</a>
      </div>
    </div>'''


# Logo, Bildbeschreibung und - wo vorhanden - das Dokument dahinter.
ZERTIFIKATE = [
    ("cert-brcgs-cert-food-logo.png", "BRCGS Food Safety certification, AA rating",
     "katech-brcgs-2027.pdf"),
    ("cert-ifs-food-box-rgb.png", "IFS Food certification", "katech-ifs-2027.pdf"),
    ("cert-rspo-1106196-logo-2021.png", "RSPO certified sustainable palm oil",
     "katech-rspo-2026.pdf"),
    ("cert-sedex-logo-small.png", "Sedex membership", "katech-sedex-smeta-2021.pdf"),
    ("cert-horzfoodchain-certificat.png", "FoodChain ID non-GMO certification",
     "katech-non-gmo-2026.pdf"),
    ("cert-gb-organic-logo-181x229-.png", "Organic certification", "katech-organic-2023.pdf"),
    ("cert-kosher-certification-197.png", "Kosher certification"),
    ("cert-halal-logo-blk-web-june-.png", "Halal certification"),
]

# Die Dokumente, die der Bestand verlinkt. Sie liegen jetzt im Entwurf selbst
# statt auf der alten Domain; die RSPO-Urkunde wird zusaetzlich direkt
# angezeigt (Suat 27.08., Punkt 16).
DOKUMENTE = {
    "brcgs": ("katech-brcgs-2027.pdf", "BRCGS Food Safety certificate",
              "Issued by DNV, certification decision 24 March 2026, valid until 25 April 2027."),
    "ifs": ("katech-ifs-2027.pdf", "IFS Food certificate",
            "Certificate C668964, unannounced audit February 2026, valid until 30 April 2027."),
    "rspo": ("katech-rspo-2026.pdf", "RSPO supply chain certificate",
             "Certificate BMC-RSPO-0088 by BM Certification, segregated and mass balance, "
             "valid until 10 February 2029."),
    "non-gmo": ("katech-non-gmo-2026.pdf", "FoodChain ID non-GMO certificate",
                "Certificate 2461031 EU1116, threshold below 0.9 per cent, "
                "valid until 31 December 2026."),
    "sedex": ("katech-sedex-smeta-2021.pdf", "Sedex SMETA audit report",
              "Ethical trade audit of the Reinfeld site, 2021."),
    "organic": ("katech-organic-2023.pdf", "Organic certificate, United Kingdom",
                "Biodynamic Association, GB-ORG-06, for KaTech Ingredient Solutions Ltd "
                "in Ellesmere Port."),
}


def dokument_karte(root, schluessel):
    datei, titel, hinweis = DOKUMENTE[schluessel]
    return f'''<li class="dok">
  <a class="dok__l" href="{root}docs/{datei}" target="_blank" rel="noopener">
    <span class="dok__ico" aria-hidden="true">PDF</span>
    <span class="dok__t"><strong>{L.esc(titel)}</strong><span>{L.esc(hinweis)}</span></span>
  </a>
</li>'''


def dokumente_block(root, schluessel_liste, *, h2, eyebrow="Documents", lead=""):
    karten = "".join(dokument_karte(root, k) for k in schluessel_liste)
    return f'''<section class="sec sec--sand">
  <div class="wrap wrap--narrow">
    {L.sec_kopf(eyebrow=eyebrow, h2=h2, lead=lead)}
    <ul class="doks rv">{karten}</ul>
  </div>
</section>'''


# Bildnamen der ersten Zertifikatsseite (pdf_vorschau.py erzeugt sie)
DOKUMENT_BILD = {k: "cert-" + d[:-4].replace("katech-", "") + "-p1"
                 for k, (d, _, _) in DOKUMENTE.items()}


def dokument_ansicht(root, schluessel, *, h2="The certificate.", lead=""):
    """Das Dokument direkt auf der Seite, nicht nur als Verweis.

    Als Bild der ersten Seite, nicht als eingebettetes PDF: eine
    <object>-Einbettung zeigt in vielen Browsern nur den Ersatztext.
    Das vollstaendige PDF haengt darunter (Suat 27.08., Punkt 16).
    """
    datei, titel, hinweis = DOKUMENTE[schluessel]
    bild = DOKUMENT_BILD[schluessel]
    return f'''<section class="sec">
  <div class="wrap wrap--narrow">
    {L.sec_kopf(eyebrow="The certificate", h2=h2, lead=lead)}
    <figure class="pdfview rv">
      <a href="{root}docs/{datei}" target="_blank" rel="noopener"
         aria-label="Open {L.esc(titel)} as PDF">
        <picture>
          <source type="image/webp" srcset="{root}media/{bild}.webp">
          <img src="{root}media/{bild}.jpg" width="1800" height="2546"
               alt="First page of the {L.esc(titel)}" loading="lazy" decoding="async">
        </picture>
      </a>
      <figcaption>{L.esc(titel)}. {L.esc(hinweis)}
        <a href="{root}docs/{datei}" target="_blank" rel="noopener">Open the full document</a></figcaption>
    </figure>
  </div>
</section>'''


SCHRITTE = [
    ("01", "Understand the brief",
     "Your end product goals, your process capabilities and the raw materials you already buy. "
     "Nothing is designed against a line that cannot run it."),
    ("02", "Formulate and trial",
     "Development in our pilot plants in Lübeck and Cheshire, on equipment that behaves like "
     "production equipment. Iterations happen in days, not quarters."),
    ("03", "Prove it on your line",
     "Our technologists come to your factory for the scale-up trial. The people who designed "
     "the system are the people standing next to it."),
    ("04", "Supply and support",
     "Blending and supply from our allergen-controlled production site, with the technical "
     "contact you already know."),
]

# Cluster der Produktwelten: id, Eyebrow, (H2, Lead), Bereiche
CLUSTER = [
    ("dairy", "Dairy and dairy alternatives",
     ("Where texture is the product.",
      "Yogurt, cream, cheese, desserts and milk drinks. The classic core of KaTech, and still "
      "the area with the deepest formulation library."),
     ["yogurt", "cream", "cheese", "desserts", "milk-drinks"]),
    ("plant", "Plant-based",
     ("Meat and fish alternatives.",
      "The fastest moving category we work in, with a dedicated centre of excellence and its "
      "own pilot machinery in Lübeck."),
     ["vegan"]),
    ("savoury", "Savoury",
     ("Emulsions that hold.",
      "Mayonnaise, dressings, dips, soups and sauces. Cold and hot processes, clean label and "
      "egg-free routes included."),
     ["mayonnaise", "dressings", "dips", "soups-and-sauces", "soups"]),
    ("bakery", "Bakery and fruit",
     ("Fillings, toppings, glazes.",
      "From muffin batter to fruit preparation, including the KaTech Scratch Plus system for "
      "clean label and allergen-free baking."),
     ["bakery", "fruit"]),
]

START_BEREICHE = ["vegan", "yogurt", "cheese", "mayonnaise", "cream", "bakery"]

PRODUKTBEREICHE = ["vegan", "yogurt", "cheese", "cream", "desserts", "milk-drinks",
                   "mayonnaise", "dressings", "dips", "soups-and-sauces", "soups",
                   "bakery", "fruit", "bakery-old"]
# bakery-old ist der aeltere Backwarenbaum des Bestands. Seine drei Seiten
# werden erzeugt und erscheinen unter Bakery; eine eigene Bereichsseite
# bekommt er nicht.
KEINE_BEREICHE = ["find-us", "our-people", "our-ingredients", "certifications"]

TITEL = {
    "vegan": "Vegan solutions",
    "cheese": "Cheese is a tasty, flexible and delicious foodstuff with endless applications",
    "how-we-work": "Working with you, to deliver on your objectives",
}

KURZTITEL = {
    "vegan": "Vegan solutions",
    "soups-and-sauces": "Soups and sauces",
    "milk-drinks": "Milk drinks",
    "our-approach": "Our approach",
    "how-we-work": "How we work",
    "our-vision": "Our vision",
    "our-people": "Our people",
    "our-facilities": "Our facilities",
    "our-ingredients": "Ingredients used",
    "new-products": "New product development",
    "cost-optimisation": "Cost optimisation",
    "fat-reduction": "Fat reduction",
    "sugar-reduction": "Sugar reduction",
    "gm-status": "GM status",
    "raw-materials": "Raw materials",
    "sourcing-and-sustainability": "Sourcing and sustainability",
    "production-facilities-germany": "Production, Germany",
    "technical-development-suite-germany": "Development suite, Germany",
    "technical-development-suite-uk": "Development suite, UK",
    "sales-office-poland": "Sales office, Poland",
    "customer-area": "Customer area",
    "case-studies": "Case studies",
    "katech-scratch-plus": "KaTech Scratch Plus",
    "bakery/katech-scratch-plus": "KaTech Scratch Plus",
    "contact-us": "Contact",
    "certifications": "Certifications",
    "certifications/rspo": "RSPO",
    "imprint": "Imprint",
    "privacy-policy": "Privacy policy",
    "terms-of-use": "Terms of use",
    "cookie-policy-eu": "Cookie policy",
    "data-protection-information-for-applicants": "Applicant privacy notice",
    "find-us": "Find us",
    "find-us/katech-head-office-germany": "Head office, Germany",
    "find-us/katech-production-germany": "Production, Germany",
    "find-us/katech-uk": "United Kingdom",
    "find-us/katech-poland": "Poland",
    "our-people/sales-team": "Sales team",
    "our-people/development-team": "Development team",
    "our-ingredients/ingredients-list": "Ingredients list",
    # Deutsche Reste im englischen Baum. Die Adresse bleibt unveraendert,
    # nur die Beschriftung wird die des Bestandstitels.
    "vegan/pflanzliche-burger-patties": "Plant-based burger patties",
    "vegan/wurstchen-alternativen": "Plant-based sausages",
    "desserts/fruchtmousse": "Fruchtmousse (German duplicate)",
    # Adressbestandteile, die fuer sich genommen nichts sagen
    "yogurt/layered": "Layered yogurt",
    "yogurt/whipped": "Whipped yogurt",
    "desserts/triflejelly": "Trifle jelly",
    "dips/yogurtquarg-dips": "Dips with yogurt and quarg",
    "cream/vegetable-non-dairy": "Vegetable and non-dairy",
    "milk-drinks/with-coffee": "With coffee",
    "soups/freshpasteurised": "Soups, fresh and pasteurised",
    "bakery-old/cleaner-label-cakes": "Cleaner label cakes",
    "bakery-old/cleaner-label-muffins": "Cleaner label muffins",
    "bakery-old/cleaner-label-sponge": "Cleaner label sponge",
    "cheese/cottage-cheese-dressing": "Cottage cheese dressing",
    "our-people/sales-team": "Sales team",
    "our-people/development-team": "Development team",
    "venture-point": "Venture Point, UK",
    "stephankoruma-cabinet": "Stephan and Koruma cabinet",
    "nasz-cel": "Nasz cel (Polish page)",
    "bakery-old": "Bakery, earlier version",
}

# Motive fuer News-Beitraege. Die Bestandsseite haengt an ihre Beitraege keine
# Bilder; ohne Motiv wirkt eine Nachrichtenliste in diesem Layout aber wie ein
# Fehler. Zugeordnet wird nur, wo der Bezug aus dem Text eindeutig ist.
NEWS_BILD = {
    "katech-receives-highest-brc-food-aa-rating-for-food-safety": "lab-measurement",
    "katech-invests-in-pilot-plant-and-strengthens-its-focus-on-plant-based-product-development":
        "pilot-plant",
    "ingredion-to-showcase-plant-based-expertise-at-pbwe2022": "p-vegan-plant-based-mince",
    "ingredion-expands-specialty-ingredient-portfolio-with-acquisition-of-katech": "hq-luebeck",
    "katech-successful-in-vegan-bakery-product-development": "p-bakery",
    "katech-strong-vegan-product-development": "p-vegan-vegan-yogurt",
    "katech-vlog-certified-food-without-genetic-engineering": "raw-materials",
    "katech-prize-outstanding-food-research-awarded-first-time": "sensory-panel",
    "katech-presents-first-company-video": "reception",
    "katech-food-industrys-secret-weapon": "development-meeting",
    "milky-grins": "p-milk-drinks",
    "keeping-the-market-sweet": "p-cheese-cream-cheese",
    "future-consumer-demands-traceability-sustainability": "warehouse",
    "food-navigator-article-on-healthy-origin-of-stabilisers": "raw-materials",
    "study-backs-whey-protein-fat-starch-replacement": "p-yogurt",
    "could-fracking-increase-guar-gum-demand": "raw-materials",
    "current-eu-approved-additives": "blending-tower",
}

def anker(text):
    """Abschnitts-Kennung aus einem Gruppennamen."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# Kurztexte und Motive der vier Plant-based-Gruppen. Sie erscheinen auf der
# Solutions-Seite und muessen dasselbe sagen wie die Gruppen der Bereichsseite.
VEGAN_GRUPPENTEXT = {
    "Meat alternatives": "Burger patties, mince, nuggets, cold cuts, patés and sausages. "
                         "Bite and texture built on dedicated pilot machinery.",
    "Fish alternatives": "Fish cakes and fish fingers with the flake and mouthfeel that "
                         "consumers compare against the original.",
    "Dairy alternatives": "Cheese, cream, yogurt, drinks and desserts without milk, and "
                          "without the chalky finish that gives them away.",
    "Savoury": "Mayonnaises, dressings, sauces and spreads. Emulsions that hold without egg.",
}
VEGAN_GRUPPENBILD = {
    "Meat alternatives": "p-vegan-plant-based-mince",
    "Fish alternatives": "p-vegan-plant-based-fish-alternatives",
    "Dairy alternatives": "p-vegan-vegan-cheese-alternatives",
    "Savoury": "p-vegan-vegan-sauces",
}

PFEIL_EXTERN = ('<svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">'
                '<path d="M4.2 2h5.8v5.8M10 2 2.4 9.6" stroke="currentColor" stroke-width="1.6" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg>')

MONATE = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def datum_lang(iso):
    j, m, t = iso.split("-")
    return f"{int(t)} {MONATE[int(m) - 1]} {j}"


# --------------------------------------------------------------------------
# Highlights: die sieben Aussagen des Bestands-Karussells
# Wortlaut aus der Bestandsseite uebernommen, Motive ebenfalls.
# --------------------------------------------------------------------------
HIGHLIGHTS = [
    ("hl-pilot-plant", "Investment in pilot plant",
     "KaTech strengthens its focus on meat and fish alternative products with the extension "
     "of their pilot machinery.",
     "The centre of excellence for meat and fish alternatives in Lübeck opened in February 2022. "
     "The new high-tech machinery lets our technical team build and test the texture of "
     "plant-based products on equipment that behaves like production equipment.",
     "katech-invests-in-pilot-plant-and-strengthens-its-focus-on-plant-based-product-development"),
    ("hl-ingredion", "KaTech is now part of Ingredion",
     "Ingredion Incorporated, a leading global provider of ingredient solutions to the food and "
     "beverage industry, has acquired KaTech.",
     "Since 2021 KaTech has been part of Ingredion Incorporated. The combination brings together "
     "KaTech's formulation expertise with Ingredion's texture business in Europe, giving customers "
     "access to a wider range of nature-based ingredients alongside the bespoke work they know.",
     "ingredion-expands-specialty-ingredient-portfolio-with-acquisition-of-katech"),
    ("hl-development", "Focus on key areas in product development",
     "KaTech's highly experienced development team create bespoke stabilising and emulsifying "
     "solutions for plant-based, dairy and dairy alternative, meat and fish, savoury and bakery "
     "products.",
     "Every solution is built for one recipe, one process and one set of raw materials. Our "
     "technical sales and technical staff are hands-on, with years of experience in real "
     "production environments, and they support development from the first idea to the factory "
     "trial.", "solutions"),
    ("hl-plant-based", "KaTech strong in developing plant-based products",
     "KaTech use their expertise around functional plant-based food ingredients and technology "
     "to develop high quality food products.",
     "Plant-based products only succeed if they taste and feel like what they replace, and "
     "texture is where most of them fail. Our range covers meat and fish alternatives as well as "
     "plant-based dairy: yogurt, cream, drinks, desserts and cheese alternatives.", "vegan"),
    ("hl-video", "New product development support",
     "At our pilot plant facilities, our technologists support food manufacturers and brands "
     "with trials, to facilitate development of their latest products.",
     "Development happens in our pilot plants in Lübeck and Cheshire. Iterations take days rather "
     "than quarters, and the technologists who designed the formulation stand next to your line "
     "when it runs for the first time.", "how-we-work"),
    ("hl-allergen", "Allergen-free production",
     "KaTech's state of the art facilities provide for tailored functional ingredient blending.",
     "Production runs in a purpose-built, allergen-controlled blending site in northern Germany. "
     "The facilities are fully certified to meet the needs of food manufacturers, and the "
     "warehouse is humidity and temperature controlled.", "our-facilities"),
    ("hl-quality", "Highest quality standards",
     "We put strong emphasis on delivering the best possible ingredient quality by being "
     "certified at the highest level.",
     "Food safety has been the focus since the company started. KaTech holds the rare BRC Food "
     "AA rating and is audited against IFS, RSPO, Sedex, non-GMO, organic, kosher and halal "
     "standards.", "certifications"),
]


def highlights_band(root):
    """Endlos laufendes Band der sieben Aussagen, per Maus oder Finger
    verschiebbar. Der Klick oeffnet den vollstaendigen Text."""
    def karte(i, h, klon=False):
        bild, titel, kurztext, _voll, _ziel = h
        return f'''<button class="hl__card" type="button" data-hl="{i}"{' tabindex="-1" aria-hidden="true"' if klon else ''}>
        <span class="hl__media"><picture>
          <source srcset="{root}media/{bild}.webp" type="image/webp">
          <img src="{root}media/{bild}.jpg" alt="" loading="lazy" decoding="async" width="560" height="360" draggable="false"></picture></span>
        <span class="hl__body">
          <span class="hl__title">{L.esc(titel)}</span>
          <span class="hl__text">{L.esc(kurztext)}</span>
          <span class="hl__more">Read more</span>
        </span>
      </button>'''

    karten = "".join(karte(i, h) for i, h in enumerate(HIGHLIGHTS))
    klone = "".join(karte(i, h, klon=True) for i, h in enumerate(HIGHLIGHTS))
    # Logos und Illustrationen duerfen nicht beschnitten werden, Fotos schon.
    marken = {"hl-ingredion", "hl-plant-based", "hl-quality"}
    inhalte = "".join(
        f'''<template data-hl-inhalt="{i}"><div class="hlbox__inner{" hlbox__inner--marke" if h[0] in marken else ""}">
      <picture><source srcset="{root}media/{h[0]}.webp" type="image/webp">
      <img src="{root}media/{h[0]}-gross.jpg" alt="{L.esc(h[1])}" loading="lazy"></picture>
      <div class="hlbox__text">
        <h3>{L.esc(h[1])}</h3>
        <p>{L.esc(h[2])}</p>
        <p>{L.esc(h[3])}</p>
        <a class="btn btn--outline" href="{root}{h[4]}/">Open the page</a>
      </div></div></template>''' for i, h in enumerate(HIGHLIGHTS))

    return f'''<section class="sec sec--ink hl" aria-label="Highlights">
  <div class="wrap">
    {sec_kopf_hl()}
  </div>
  <div class="hl__rail" id="hlRail">
    <div class="hl__track" id="hlTrack">{karten}{klone}</div>
  </div>
  {inhalte}
  <div class="hlbox" id="hlBox" hidden role="dialog" aria-modal="true" aria-label="Highlight">
    <button class="hlbox__close" type="button" aria-label="Close">&times;</button>
    <button class="hlbox__prev" type="button" aria-label="Previous">&#8249;</button>
    <div class="hlbox__stage" id="hlStage"></div>
    <button class="hlbox__next" type="button" aria-label="Next">&#8250;</button>
    <span class="hlbox__count" id="hlCount"></span>
  </div>
</section>'''


def sec_kopf_hl():
    return L.sec_kopf(eyebrow="Highlights", h2="What has been happening.",
                      lead="Seven things worth knowing about the company. Drag the row or "
                           "click an item to read it in full.")


# --------------------------------------------------------------------------
# JSON-LD
# --------------------------------------------------------------------------
LD_ORG = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": L.PAGES_URL + "#org",
         "name": "KaTech Ingredient Solutions GmbH",
         "alternateName": "KaTech",
         "url": L.ORIGINAL,
         "logo": L.PAGES_URL + "media/logo-dark.png",
         "description": "Development and production of bespoke stabilising, emulsifying and "
                        "texturising systems for the food industry.",
         "foundingDate": "2010",
         "parentOrganization": {"@type": "Organization", "name": "Ingredion Incorporated",
                                "url": "https://www.ingredion.com/"},
         "address": {"@type": "PostalAddress", "streetAddress": "Aegidienstraße 22",
                     "postalCode": "23552", "addressLocality": "Lübeck",
                     "addressRegion": "Schleswig-Holstein", "addressCountry": "DE"},
         "telephone": "+49 451 4070 2-0",
         "email": "hello@katech-solutions.com",
         "numberOfEmployees": {"@type": "QuantitativeValue", "value": 95},
         "areaServed": ["DE", "GB", "PL", "EU"],
         "knowsAbout": ["food stabilisers", "emulsifiers", "texture solutions",
                        "plant-based meat alternatives", "dairy alternatives",
                        "clean label formulation", "fat reduction", "sugar reduction",
                        "recipe cost optimisation", "pilot plant trials"],
         "contactPoint": [{"@type": "ContactPoint", "contactType": "sales",
                           "email": "hello@katech-solutions.com",
                           "telephone": "+49 451 4070 2-0",
                           "availableLanguage": ["en", "de", "pl"]}],
         "potentialAction": {"@type": "CommunicateAction",
                             "target": "mailto:hello@katech-solutions.com",
                             "name": "Make an enquiry"}},
        {"@type": "WebSite", "@id": L.PAGES_URL + "#site",
         "url": L.PAGES_URL, "name": "KaTech Ingredient Solutions - design preview",
         "inLanguage": "en", "publisher": {"@id": L.PAGES_URL + "#org"}},
    ],
}


def ld_liste(name, eintraege):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name,
            "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "url": u}
                                for i, (n, u) in enumerate(eintraege, 1)]}


def ld_artikel(titel, datum, beschreibung, url):
    return {"@context": "https://schema.org", "@type": "Article", "headline": titel,
            "datePublished": datum, "description": beschreibung, "url": url,
            "publisher": {"@type": "Organization", "name": "KaTech Ingredient Solutions GmbH"},
            "inLanguage": "en"}


# --------------------------------------------------------------------------
# Hub-Seiten (Expertise, Company)
# --------------------------------------------------------------------------
def baue_hubs(hub):
    """Erzeugt Expertise, Company und Facilities aus der Struktur.
    Solutions hat eine eigene Funktion, weil dort Kacheln mit Bild stehen."""
    import struktur as S

    hub("expertise", "Expertise", "What we bring to the table",
        "Formulation knowledge, and the equipment to prove it.",
        "Our technologists work hands-on: from the first concept through pilot trials to the "
        "run on your production line.",
        [(titel, kopf, [(s, "", "") for s in seiten])
         for titel, kopf, seiten in S.EXPERTISE],
        og="og-expertise.jpg", bild="lab-measurement")

    hub("our-facilities", "Our facilities", "Facilities",
        "State of the art facilities built with the customer in mind.",
        "Pilot plants in Lübeck and Cheshire, production and warehousing in northern Germany, "
        "a sales office near Poznań.",
        [(titel, kopf, [(s, "", "") for s in seiten])
         for titel, kopf, seiten in S.FACILITIES],
        og="og-facilities.jpg", bild="blending-tower",
        zusatz=GALERIE_FACILITIES)

    hub("company", "Company", "Who we are",
        "A food technology company that stayed hands-on.",
        "Founded in Lübeck in 2010, around 95 people across Germany, the UK and Poland, "
        "part of Ingredion since 2021.",
        [(titel, kopf, [(s, "", "") for s in seiten])
         for titel, kopf, seiten in S.COMPANY],
        og="og-company.jpg", bild="hq-luebeck",
        zusatz=VERWEIS_FACILITIES)


GALERIE_FACILITIES = """<section class="sec sec--sand">
  <div class="wrap">
    {kopf}
    {galerie}
  </div>
</section>"""

VERWEIS_FACILITIES = """<section class="sec sec--teal">
  <div class="wrap">
    {kopf}
    <div class="btn-row btn-row--single rv">
      <a class="btn btn--ghost" href="{root}our-facilities/">Our facilities</a>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# Textseiten
# --------------------------------------------------------------------------
# Bilder fuer die Kopfbereiche einzelner Seiten. Wo nichts steht, bleibt der
# Kopf ohne Bild.
SEITEN_BILD = {
    "our-vision": "hq-luebeck", "our-approach": "reception",
    "our-facilities": "blending-tower", "careers": "sensory-panel",
    "production-facilities-germany": "plant-reinfeld",
    "technical-development-suite-germany": "lab-measurement",
    "technical-development-suite-uk": "warehouse",
    "sales-office-poland": "reception", "raw-materials": "raw-materials",
    "new-products": "development-meeting", "products": "sensory-panel",
    "our-ingredients": "raw-materials", "venture-point": "warehouse",
}

LEGAL_SEITEN = LEGAL = ["imprint", "privacy-policy", "terms-of-use", "cookie-policy-eu",
                        "data-protection-information-for-applicants"]


def _laden(name):
    """Eine der erhobenen JSON-Dateien neben diesem Modul, oder {}."""
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    return json.load(open(pfad, encoding="utf-8")) if os.path.exists(pfad) else {}


LEGAL_TEXTE = _laden("legal.json")

# Auffaelligkeiten in den Rechtstexten des Bestands. Sie werden NICHT still
# korrigiert - der Text bleibt wortgetreu, der Befund steht als sichtbarer
# Kommentar daneben (Suat 27.08.: beim Rechtszeug gewissenhafter, erst so
# uebernehmen wie es ist, hoechstens Hinweise als Empfehlung).
LEGAL_ANMERKUNGEN = {
    "privacy-policy": [
        ("Page title", "The heading is the full opening sentence, 148 characters long. It reads "
         "that way on the existing site too. Suggested: shorten the title to “Privacy "
         "policy” and let the sentence become the first paragraph."),
        ("Legal term", "The text refers to the regulation as DSGVO in some places and GDPR in "
         "others. Suggested: use GDPR throughout in the English version."),
        ("Address", "The street is spelled “Aegiedienstraße” here and "
         "“Aegidienstraße” in the imprint. One of the two is wrong."),
    ],
    "imprint": [
        ("Fax number", "The fax number appears twice in two different forms: 0451 40 70-377 "
         "and 0451 40 70 2-377."),
    ],
    "terms-of-use": [
        ("Company name", "The text refers throughout to “K. Hahn + Partners Food "
         "Technology Ltd”, the name used before the change to KaTech Ingredient "
         "Solutions. Suggested: update."),
        ("Page title", "The page carries no heading of its own."),
    ],
    "cookie-policy-eu": [
        ("Date", "The text is dated 23 July 2025 and is therefore more than a year old."),
    ],
}


def _legal_anmerkung(titel, text):
    return f'''<aside class="anm">
  <span class="anm__marke">Note on the original</span>
  <p><strong>{L.esc(titel)}:</strong> {L.esc(text)}</p>
</aside>'''


def legal_html(slug):
    """Die Rechtstexte wortgetreu, in Originalreihenfolge, mit Listen."""
    e = LEGAL_TEXTE.get(slug)
    if not e:
        return "", ""
    teile, liste = [], []

    def liste_leeren():
        if liste:
            teile.append("<ul>" + "".join(f"<li>{L.esc(x)}</li>" for x in liste) + "</ul>")
            liste.clear()

    for b in e["bloecke"]:
        if b["tag"] == "li":
            liste.append(b["text"])
            continue
        liste_leeren()
        text = L.esc(b["text"])
        if b.get("href"):
            ziel_ = L.esc(b["href"])
            if ziel_.startswith("/"):
                ziel_ = "https://katech-solutions.com" + ziel_
            text = f'{text} <a href="{ziel_}" rel="noopener noreferrer" target="_blank">Open</a>'
        if b["tag"] in ("h2", "h3", "h4", "h5"):
            stufe = {"h2": "h2", "h3": "h3", "h4": "h3", "h5": "h4"}[b["tag"]]
            teile.append(f"<{stufe}>{L.esc(b['text'])}</{stufe}>")
        elif b["tag"] in ("td", "th"):
            teile.append(f"<p>{text}</p>")
        else:
            teile.append(f"<p>{text}</p>")
    liste_leeren()

    anm = "".join(_legal_anmerkung(t, x) for t, x in LEGAL_ANMERKUNGEN.get(slug, []))
    return "".join(teile), anm


def _legal_titel(slug):
    """Kurzer Seitentitel. Der Bestand fuehrt bei der Privacy policy den
    ganzen Einleitungssatz als Ueberschrift; der bleibt als erster Absatz
    erhalten, die Ueberschrift wird lesbar. Vermerkt als Anmerkung."""
    return {"privacy-policy": "Privacy policy",
            "imprint": "Imprint",
            "terms-of-use": "Terms of use",
            "cookie-policy-eu": "Cookie policy (EU)",
            "data-protection-information-for-applicants":
                "Data protection information for applicants"}.get(slug, slug)


def baue_textseiten(textseite, legalseite):
    """Alle Seiten der Bereiche Company, Expertise und Facilities.
    Die Zuordnung kommt aus struktur.py; Menuemarkierung und Breadcrumb
    leitet der Generator daraus ab."""
    import struktur as S

    for abschnitte, bereich, eyebrow in (
            (S.COMPANY, "company", "Company"),
            (S.EXPERTISE, "expertise", "Expertise"),
            (S.FACILITIES, "facilities", "Facilities")):
        for _, _, seiten in abschnitte:
            for slug in seiten:
                # Diese Seiten haben eigene Funktionen mit mehr Inhalt
                # (Prozessschritte, Teamkacheln, Standortkarten) und wuerden
                # hier nur ueberschrieben.
                if slug in ("find-us", "how-we-work", "our-people",
                            "our-facilities") or slug.startswith("find-us/"):
                    continue
                extra = ""
                if slug == "certifications/rspo":
                    extra = dokument_ansicht("../../", "rspo")
                if slug == "certifications":
                    extra = f'''<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Audited and certified", h2="The standards we hold.", zentriert=True)}
    {L.zertifikate("../", ZERTIFIKATE)}
  </div>
</section>
''' + dokumente_block("../", ["brcgs", "ifs", "rspo", "non-gmo", "sedex", "organic"],
                      h2="The certificates themselves.",
                      lead="Every certificate as issued, ready to open or pass on.")
                if slug == "our-facilities":
                    extra = f'''<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Impressions", h2="Inside the sites.")}
    {L.galerie("../", [("hq-luebeck", "KaTech head office in Lübeck"),
                       ("blending-tower", "Blending tower at the production site"),
                       ("lab-measurement", "Measurement in the development laboratory"),
                       ("sensory-panel", "Sensory panel with product samples"),
                       ("warehouse", "Temperature controlled warehouse"),
                       ("plant-reinfeld", "Production site in northern Germany")])}
  </div>
</section>'''
                textseite(slug, eyebrow=eyebrow,
                          crumbs_extra=None,
                          bild=SEITEN_BILD.get(slug), extra_html=extra)

    # Seiten ausserhalb der Abschnitte, die trotzdem erreichbar bleiben
    for slug in ("venture-point", "stephankoruma-cabinet", "nasz-cel"):
        textseite(slug, eyebrow="Company", crumbs_extra=None,
                  bild=SEITEN_BILD.get(slug))

    # Die beiden Teamlisten des Bestands. Sie tragen dort keinen Inhalt, bleiben
    # aber erreichbar und haengen unter der Teamuebersicht.
    for slug in ("our-people/sales-team", "our-people/development-team"):
        textseite(slug, eyebrow="Our people",
                  crumbs_extra=[("Our people", "../../our-people/")],
                  bild=None)

    for slug in LEGAL_SEITEN:
        legalseite(slug)


# --------------------------------------------------------------------------
# Sonderseiten
# --------------------------------------------------------------------------
def baue_sonderseiten(schreibe, SEITEN, BAUM, NEWS, MEDIA, kurztitel, titel_von, intro_von,
                      kurz, geschrieben):
    _how_we_work(schreibe, SEITEN)
    _team(schreibe, SEITEN, kurz)
    _news(schreibe, NEWS, kurz)
    _kontakt(schreibe)
    _find_us(schreibe)
    _hinweise(schreibe, SEITEN, BAUM, NEWS)
    _sitemap(schreibe, SEITEN, BAUM, NEWS, kurztitel)
    _fehlerseite(schreibe)


def _how_we_work(schreibe, SEITEN):
    slug, root = "how-we-work", "../"
    s = SEITEN.get(slug, {})
    absaetze = s.get("absaetze", [])
    inhalt = L.subhero(root, crumbs=[("Start", root + "index.html"),
                                     ("Company", root + "company/"), ("How we work", None)],
                       eyebrow="How we work",
                       h1="Working with you, to deliver on your <em>objectives</em>.",
                       sub=kurz_lokal(absaetze[0] if absaetze else "", 220),
                       bild="development-meeting",
                       alt="Development meeting with product samples at KaTech")
    inhalt += f'''
<section class="sec">
  <div class="wrap">
    {L.sec_kopf(eyebrow="In practice", h2="Sounds good. What does that mean on a Tuesday?",
                lead="Four steps, and the same people through all of them.")}
    {L.schritte(SCHRITTE)}
  </div>
</section>
<section class="sec sec--sand">
  <div class="wrap wrap--narrow">
    {L.prosa([L.absatz(t) for t in absaetze[1:]] or [L.absatz(PLATZHALTER)])}
  </div>
</section>'''
    inhalt += L.split(root, ton="brand", eyebrow="What you keep",
                      h2="Confidential, independent, and yours.",
                      text=["We work confidentially and independently. The formulation we build "
                            "with you is built for your line and your raw material contracts.",
                            "That is the reason customers come back with the next product rather "
                            "than with a complaint."],
                      liste=["Your recipe stays your recipe",
                             "Independent of any single raw material supplier",
                             "Technologists on site for the scale-up run"],
                      cta=("Make an enquiry", root + "contact-us/"),
                      bild="lab-measurement",
                      alt="Laboratory measurement during formulation work")
    inhalt += f'''
<section class="sec sec--teal">
  <div class="wrap wrap--narrow center">
    {L.sec_kopf(h2="Start with one product.",
                lead="Most partnerships here started with a single difficult item that nobody "
                     "else wanted to touch.", zentriert=True)}
    <div class="btn-row btn-row--single rv" style="margin-inline:auto">
      <a class="btn btn--ghost" href="{root}contact-us/">Make an enquiry</a>
    </div>
  </div>
</section>'''
    schreibe(slug + "/index.html", L.seite(
        slug + "/index.html", "How we work",
        "How KaTech develops bespoke stabiliser and emulsifier systems: from the brief through "
        "pilot trials to the run on your production line.",
        inhalt, aktiv="company/", og="og-company.jpg"))


def kurz_lokal(text, n=155):
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "."


def _news(schreibe, NEWS, kurz):
    root = "../"
    posts = [n for n in NEWS if n["slug"] != "news" and n["absaetze"]]
    # Uebersicht
    def news_medien(n):
        b = NEWS_BILD.get(n["slug"])
        if not b:
            return ""
        return (f'''<a class="newsitem__media" href="{root}{n['slug']}/" tabindex="-1" aria-hidden="true">
        <picture><source srcset="{root}media/{b}.webp" type="image/webp">
        <img src="{root}media/{b}.jpg" alt="" loading="lazy" decoding="async" width="800" height="533"></picture>
      </a>''')

    eintraege = "".join(f'''<article class="newsitem newsitem--bild">
      <time datetime="{n['datum']}">{datum_lang(n['datum'])}</time>
      {news_medien(n)}
      <div>
        <a href="{root}{n['slug']}/"><h3>{L.esc(n['titel'])}</h3></a>
        <p>{L.esc(kurz(n['absaetze'][0], 210))}</p>
      </div>
    </article>''' for n in posts)
    inhalt = L.subhero(root, crumbs=[("Start", root + "index.html"), ("News", None)],
                       eyebrow="News", h1="News and press.",
                       sub=f"{len(posts)} releases from the company archive, carried over in full.",
                       bild="hq-luebeck", alt="KaTech head office")
    inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow">
    <div class="rv">{eintraege}</div>
  </div>
</section>'''
    schreibe("news/index.html", L.seite(
        "news/index.html", "News",
        "Press releases and company news from KaTech Ingredient Solutions.",
        inhalt, aktiv="news/", og="og-company.jpg",
        jsonld=ld_liste("News", [(n["titel"], L.PAGES_URL + n["slug"] + "/") for n in posts])))

    # Detailseiten
    for i, n in enumerate(posts):
        r = "../"
        weiter = [x for x in posts if x["slug"] != n["slug"]][:3]
        naechste = "".join(f'''<a class="tile" href="{r}{w['slug']}/">
      <span class="tile__num">{datum_lang(w['datum'])}</span>
      <h3>{L.esc(w['titel'])}</h3>
    </a>''' for w in weiter)
        koerper = "".join(f"<p>{L.esc(a)}</p>" for a in n["absaetze"])
        motiv = NEWS_BILD.get(n["slug"])
        inhalt = L.subhero(r, crumbs=[("Start", r + "index.html"), ("News", r + "news/"),
                                      (kurz(n["titel"], 46), None)],
                           eyebrow=datum_lang(n["datum"]), h1=L.esc(n["titel"]),
                           bild=motiv, alt="")
        inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow">
    <div class="prose rv">{koerper}</div>
  </div>
</section>
<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow="More news", h2="Also from the archive.")}
    <div class="grid grid--3 rv">{naechste}</div>
    <div class="btn-row btn-row--single rv" style="margin-top:30px">
      <a class="btn btn--outline" href="{r}news/">All news</a>
    </div>
  </div>
</section>'''
        schreibe(n["slug"] + "/index.html", L.seite(
            n["slug"] + "/index.html", kurz(n["titel"], 60),
            kurz(n["absaetze"][0], 158), inhalt, aktiv="news/", og="og-company.jpg",
            jsonld=ld_artikel(n["titel"], n["datum"], kurz(n["absaetze"][0], 158),
                              L.PAGES_URL + n["slug"] + "/")))


def _kontakt(schreibe):
    root = "../"
    karten = "".join(f'''<div class="loc">
      <span class="loc__role">{L.esc(s['name'])}</span>
      <h3>{L.esc(s['ort'])}</h3>
      <address>{"<br>".join(L.esc(z) for z in s['adresse'])}</address>
      <dl>
        <dt>Phone</dt><dd><a href="tel:{s['telhref']}">{L.esc(s['tel'])}</a></dd>
        <dt>Fax</dt><dd>{L.esc(s['fax'])}</dd>
        <dt>E-mail</dt><dd><a href="mailto:{s['mail']}">{L.esc(s['mail'])}</a></dd>
      </dl>
    </div>''' for s in STANDORTE)

    inhalt = L.subhero(root, crumbs=[("Start", root + "index.html"), ("Contact", None)],
                       eyebrow="Contact", h1="Tell us what the product has to <em>do</em>.",
                       sub="Describe the product, the process and where it currently fails. "
                           "Your enquiry goes to a technologist, not to a queue.",
                       bild="sensory-panel", alt="Product samples on the sensory panel table")
    inhalt += f'''
<section class="sec">
  <div class="wrap">
    <div class="grid grid--2" style="gap:clamp(32px,5vw,64px);align-items:start">
      <div class="rv">
        {L.sec_kopf(eyebrow="Enquiry", h2="Make an enquiry.",
                    lead="All fields marked with an asterisk are required.")}
        <form class="form" id="enquiry" novalidate>
          <div class="field"><label for="f-name">Name *</label>
            <input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-company">Company *</label>
            <input id="f-company" name="company" type="text" autocomplete="organization" required></div>
          <div class="field"><label for="f-mail">E-mail *</label>
            <input id="f-mail" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-phone">Telephone</label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field full"><label for="f-country">Country</label>
            <select id="f-country" name="country">
              <option>Germany</option><option>United Kingdom</option><option>Poland</option>
              <option>Netherlands</option><option>France</option><option>Other</option>
            </select></div>
          <div class="field full"><label for="f-area">Product area</label>
            <select id="f-area" name="area">
              <option>Vegan solutions</option><option>Yogurt</option>
              <option>Cheese</option><option>Cream</option><option>Milk drinks</option>
              <option>Desserts</option><option>Mayonnaise</option><option>Dressings and dips</option>
              <option>Soups and sauces</option><option>Bakery</option><option>Fruit</option>
              <option>Not sure yet</option>
            </select></div>
          <div class="field full"><label for="f-msg">Your enquiry *</label>
            <textarea id="f-msg" name="message" required></textarea></div>
          <label class="check full"><input type="checkbox" name="privacy" required>
            <span>I have read and understood the <a href="{root}privacy-policy/">privacy policy</a>. *</span></label>
          <div class="full"><button class="btn btn--primary" type="submit">Send enquiry</button></div>
          <p class="form__note" id="formNote" hidden>
            <strong>This is a design preview.</strong> The form is not connected to a mailbox.
            In the live version it delivers straight to the responsible technologist, with spam
            protection and a confirmation mail. For a real enquiry today please write to
            <a href="mailto:hello@katech-solutions.com">hello@katech-solutions.com</a>.</p>
        </form>
      </div>
      <div class="rv">
        {L.sec_kopf(eyebrow="Direct", h2="Or simply call.",
                    lead="Lübeck answers the phone during German business hours, Ellesmere Port "
                         "during UK hours.")}
        <div class="grid" style="gap:18px">{karten}</div>
      </div>
    </div>
  </div>
</section>
<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Head office", h2="Aegidienstraße 22, Lübeck.",
                lead="The map loads from Google only after you allow it.")}
    <div class="mapwrap rv" style="position:relative;aspect-ratio:16/7;border:1px solid var(--line)">
      <div class="mapph">
        <p>This map is loaded from Google Maps. Loading it transfers data to Google.</p>
        <button class="btn btn--ghost" type="button" data-map-load>Load map</button>
      </div>
      <iframe title="Map of the KaTech head office in Lübeck" data-src="{STANDORTE[0]['karte']}"
        style="width:100%;height:100%;border:0" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>'''
    schreibe("contact-us/index.html", L.seite(
        "contact-us/index.html", "Contact",
        "Contact KaTech Ingredient Solutions: head office Lübeck, production Wesenberg, "
        "development suite Ellesmere Port, sales office Stęszew.",
        inhalt, aktiv="contact", og="og-company.jpg", jsonld=LD_ORG))


def _find_us(schreibe):
    root = "../"
    karten = "".join(f'''<div class="loc">
      <span class="loc__role">{L.esc(s['name'])}</span>
      <h3>{L.esc(s['ort'])}</h3>
      <address>{"<br>".join(L.esc(z) for z in s['adresse'])}</address>
      <dl><dt>Phone</dt><dd><a href="tel:{s['telhref']}">{L.esc(s['tel'])}</a></dd>
      <dt>E-mail</dt><dd><a href="mailto:{s['mail']}">{L.esc(s['mail'])}</a></dd></dl>
    </div>''' for s in STANDORTE)
    inhalt = L.subhero(root, crumbs=[("Start", root + "index.html"),
                                     ("Facilities", root + "our-facilities/"), ("Find us", None)],
                       eyebrow="Locations", h1="Four sites, three countries.",
                       sub="Development in Lübeck and Cheshire, production and warehousing in "
                           "northern Germany, sales in Poland.",
                       bild="plant-reinfeld", alt="KaTech production site")
    inhalt += f'''
<section class="sec">
  <div class="wrap">
    <div class="grid grid--2 rv">{karten}</div>
  </div>
</section>'''
    schreibe("find-us/index.html", L.seite(
        "find-us/index.html", "Find us",
        "KaTech locations in Lübeck, Wesenberg, Ellesmere Port and Stęszew.",
        inhalt, aktiv="our-facilities/", og="og-facilities.jpg", jsonld=LD_ORG))

    for s, slug in zip(STANDORTE, ["find-us/katech-head-office-germany",
                                   "find-us/katech-production-germany",
                                   "find-us/katech-uk", "find-us/katech-poland"]):
        r = "../../"
        inhalt = L.subhero(r, crumbs=[("Start", r + "index.html"),
                                      ("Facilities", r + "our-facilities/"),
                                      ("Find us", r + "find-us/"), (s["ort"], None)],
                           eyebrow=s["name"], h1=L.esc(s["ort"]), bild=s["bild"], alt=s["ort"])
        inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow">
    <div class="loc rv">
      <span class="loc__role">{L.esc(s['name'])}</span>
      <h3>{L.esc(s['ort'])}</h3>
      <address>{"<br>".join(L.esc(z) for z in s['adresse'])}</address>
      <dl>
        <dt>Phone</dt><dd><a href="tel:{s['telhref']}">{L.esc(s['tel'])}</a></dd>
        <dt>Fax</dt><dd>{L.esc(s['fax'])}</dd>
        <dt>E-mail</dt><dd><a href="mailto:{s['mail']}">{L.esc(s['mail'])}</a></dd>
      </dl>
    </div>
    <div class="mapwrap rv" style="position:relative;aspect-ratio:16/8;border:1px solid var(--line);margin-top:26px">
      <div class="mapph">
        <p>This map is loaded from Google Maps.</p>
        <button class="btn btn--ghost" type="button" data-map-load>Load map</button>
      </div>
      <iframe title="Map of {L.esc(s['ort'])}" data-src="{s['karte']}"
        style="width:100%;height:100%;border:0" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>'''
        schreibe(slug + "/index.html", L.seite(
            slug + "/index.html", s["ort"],
            f"KaTech {s['name'].lower()} in {s['ort']}.", inhalt,
            aktiv="our-facilities/", og="og-facilities.jpg"))


def _sitemap(schreibe, SEITEN, BAUM, NEWS, kurztitel):
    """Grafische Sitemap: alle Seiten hierarchisch und einzeln anklickbar."""
    import struktur as S
    root = "../"

    def original_pfeil(slug, name):
        """Verweis auf dieselbe Seite im Bestand, aber nur wo es sie dort gibt.
        Die Hub-Seiten dieses Entwurfs existieren im Original nicht.
        Die News-Zeilen hatten den Pfeil nicht, obwohl es alle 17 Beitraege
        im Bestand gibt - Suat hat das am 27.08. gefunden (Punkt 2)."""
        if slug not in IM_BESTAND:
            return ""
        return (f'<a class="sm__orig" href="https://katech-solutions.com/{slug}/" '
                f'target="_blank" rel="noopener" '
                f'aria-label="Open {L.esc(name)} on the original site">'
                f'{PFEIL_EXTERN}</a>')

    def eintrag(slug, titel=None, tiefe=0):
        name = titel or kurztitel(slug)
        if ist_leer(slug):
            marke = ('<span class="sm__mk" title="no content on the existing site">'
                     'empty</span>')
        elif ist_nicht_ausgebaut(slug):
            marke = ('<span class="sm__mk sm__mk--offen" '
                     'title="not built out in this preview">not built</span>')
        else:
            marke = ""
        original = original_pfeil(slug, name)
        return (f'<li class="sm__i sm__i--{tiefe}">'
                f'<a href="{root}{slug}/">{L.esc(name)}</a>{marke}{original}</li>')

    bloecke = []

    # ---- Solutions -------------------------------------------------------
    spalten = []
    for _, gruppentitel, _, bereiche in S.SOLUTIONS:
        eintraege = []
        for b in bereiche:
            eintraege.append(f'<li class="sm__k"><a href="{root}{b}/">{L.esc(kurztitel(b))}</a></li>')
            if b == "vegan":
                for gruppe, kopf, kinder in S.VEGAN_GRUPPEN:
                    # Die Gruppe fuehrt auf ihre Kopfseite, sonst auf den
                    # Abschnitt der Bereichsseite. Beides ist anklickbar.
                    ziel = f"{root}{kopf}/" if kopf else f"{root}vegan/#{anker(gruppe)}"
                    eintraege.append(
                        f'<li class="sm__g"><a href="{ziel}">{L.esc(gruppe)}</a></li>')
                    for u in ([kopf] if kopf else []) + kinder:
                        eintraege.append(eintrag(u, tiefe=2))
            else:
                for u in BAUM.get(b, []) + S.FREMDE_KINDER.get(b, []):
                    eintraege.append(eintrag(u, tiefe=1))
        spalten.append(f'<div class="sm__sp"><h3>{L.esc(gruppentitel)}</h3>'
                       f'<ul class="sm__l">{"".join(eintraege)}</ul></div>')
    bloecke.append(("Solutions", "solutions", spalten))

    # ---- Expertise, Company, Facilities ----------------------------------
    for abschnitte, titel, start_slug in ((S.EXPERTISE, "Expertise", "expertise"),
                                          (S.COMPANY, "Company", "company"),
                                          (S.FACILITIES, "Facilities", "our-facilities")):
        spalten = []
        for gruppentitel, _, seiten in abschnitte:
            eintraege = []
            for s in seiten:
                # Seiten, die unter einer anderen Seite derselben Spalte liegen,
                # werden dort eingerueckt gezeigt. Die vier Standorte standen
                # sonst zweimal da: einmal als Kind von Find us, einmal als
                # eigener Eintrag (Suat 27.08.).
                eltern = s.rsplit("/", 1)[0] if "/" in s else None
                if eltern and eltern in seiten:
                    eintraege.append(eintrag(s, tiefe=1))
                    continue
                eintraege.append(eintrag(s))
                if s == "our-people":
                    for u in ("our-people/sales-team", "our-people/development-team"):
                        eintraege.append(eintrag(u, tiefe=1))
                    pfad_team = os.path.join(os.path.dirname(os.path.abspath(__file__)), "team.json")
                    if os.path.exists(pfad_team):
                        for p in json.load(open(pfad_team, encoding="utf-8")):
                            eintraege.append(eintrag(p["slug"], p["name"], tiefe=1))
            spalten.append(f'<div class="sm__sp"><h3>{L.esc(gruppentitel)}</h3>'
                           f'<ul class="sm__l">{"".join(eintraege)}</ul></div>')
        bloecke.append((titel, start_slug, spalten))

    # ---- News ------------------------------------------------------------
    nw = "".join(f'<li class="sm__i sm__i--0"><a href="{root}{n["slug"]}/">'
                 f'{L.esc(kurz_lokal(n["titel"], 62))}</a>'
                 f'<span class="sm__d">{datum_lang(n["datum"])}</span>'
                 f'{original_pfeil(n["slug"], n["titel"])}</li>'
                 for n in NEWS if n["slug"] != "news" and n["absaetze"])
    bloecke.append(("News", "news",
                    [f'<div class="sm__sp sm__sp--breit"><h3>Press releases</h3>'
                     f'<ul class="sm__l">{nw}</ul></div>']))

    # ---- Team-Unterseiten an ihrer Stelle ergaenzen -----------------------
    # (siehe oben bei our-people)

    # ---- Kontakt, Rechtliches, uebrige Seiten ----------------------------
    meta = "".join(eintrag(s) for s in ["contact-us", "sitemap"])
    recht = "".join(eintrag(s) for s in LEGAL_SEITEN)
    # Seiten des Bestands, die zu keinem Abschnitt gehoeren. Sie sind
    # vorhanden und muessen deshalb auffindbar sein.
    uebrig = "".join(eintrag(s) for s in S.UEBRIGE + ["bakery-old"])
    bloecke.append(("Contact, legal and other pages", "contact-us", [
        f'<div class="sm__sp"><h3>Direct</h3><ul class="sm__l">{meta}</ul></div>',
        f'<div class="sm__sp"><h3>Legal</h3><ul class="sm__l">{recht}</ul></div>',
        f'<div class="sm__sp"><h3>Other pages of the existing site</h3>'
        f'<ul class="sm__l">{uebrig}</ul></div>',
    ]))

    abschnitte_html = "".join(
        f'''<section class="sec{" sec--sand" if n % 2 else ""}">
  <div class="wrap">
    <div class="sm__kopf">
      <h2><a href="{root}{ziel}/">{L.esc(titel)}</a></h2>
    </div>
    <div class="sm__raster rv">{"".join(spalten)}</div>
  </div>
</section>''' for n, (titel, ziel, spalten) in enumerate(bloecke))

    anzahl = len([s for s in SEITEN if s])
    inhalt = L.subhero(root, crumbs=[("Start", root + "index.html"), ("Sitemap", None)],
                       eyebrow="Overview", h1="Every page, in order.",
                       sub="The complete structure of the existing site, every page "
                           "reachable at its original address. Entries marked empty carry no "
                           "content on the existing site either. The small arrow behind an "
                           "entry opens the same page on the original site, so anything stated "
                           "here can be checked. Only one entry has no arrow: bakery-old has "
                           "sub-pages on the existing site but no page of its own.")
    inhalt += "\n" + abschnitte_html
    schreibe("sitemap/index.html", L.seite(
        "sitemap/index.html", "Sitemap",
        "Full page overview of the KaTech design preview, hierarchically ordered.",
        inhalt, og="og-company.jpg"))


def _fehlerseite(schreibe):
    root = ""
    inhalt = L.subhero(root, crumbs=[("Start", "index.html"), ("Page not found", None)],
                       eyebrow="Error 404", h1="This page does not exist.",
                       sub="It may have moved, or the link is wrong. The overview below "
                           "gets you back on track.")
    inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow center">
    <div class="btn-row rv" style="margin-inline:auto">
      <a class="btn btn--primary" href="index.html">To the start page</a>
      <a class="btn btn--outline" href="sitemap/">To the sitemap</a>
    </div>
  </div>
</section>'''
    schreibe("404.html", L.seite("404.html", "Page not found",
                                 "The requested page does not exist.", inhalt, solid=True))


def _hinweise(schreibe, SEITEN, BAUM, NEWS):
    """Die Pflicht-Hinweisseite des Demonstrator-Standards."""
    root = "../"
    anzahl_seiten = len(SEITEN)
    anzahl_news = len([n for n in NEWS if n["slug"] != "news" and n["absaetze"]])

    swatches = [("--brand", "#6cb33e", "Logo green"), ("--brand-deep", "#4f6e18", "Text green"),
                ("--teal", "#006a71", "Signature surface"), ("--ink", "#373738", "Text and footer"),
                ("--accent", "#ffe115", "Logo yellow"), ("--blue", "#0073d8", "Technical accent"),
                ("--sand", "#f4f4f1", "Light surface"), ("--line", "#d8d9d9", "Hairline")]
    ds = "".join(f'''<div class="ds__sw"><i style="background:{h}"></i>
      <div><b>{L.esc(n)}</b><span>{h}</span></div></div>''' for _, h, n in swatches)

    vergleich = [
        ("Design", "Template from 2013, unchanged since launch",
         "Built on the Ingredion colour and layout system, with the KaTech logo unchanged"),
        ("Structure", "Mega menu with over 100 entries at once",
         "Four clear routes, every page still reachable and kept at its original address"),
        ("Images", "Small images at 432 by 288 pixels, some loaded from a third-party domain",
         "The same photographs, sharpened and delivered as WebP from one domain"),
        ("Speed", "WordPress with several stylesheets, jQuery and an old slider",
         "Static HTML, no framework, no database, no plugin updates"),
        ("Findability for AI", "One generic schema block, no machine-readable structure",
         "Organization, ItemList, Article and Breadcrumb schema on every page type"),
        ("Mobile", "Layout from before responsive design was standard",
         "Built mobile first, tested down to 320 pixels"),
        ("Maintenance", "Every change goes through an agency",
         "Content changes by prompt, live in minutes, demonstrated in this meeting"),
    ]
    zeilen = "".join(f'''<tr><td>{L.esc(m)}</td><td data-l="Current site">{L.esc(a)}</td>
      <td data-l="This preview">{L.esc(b)}</td></tr>''' for m, a, b in vergleich)

    metriken = [("Stylesheets", "3 files", "1 file"),
                ("JavaScript", "jQuery, qTip, Colorbox, RoyalSlider", "One file, 9 KB"),
                ("Fonts", "System fonts, no self-hosting", "2 families, self-hosted"),
                ("Schema types", "none worth indexing", "4 types across all pages")]
    mk = "".join(f'''<div><span class="lbl">{L.esc(l)}</span>
      <span class="old">{L.esc(a)}</span><span class="new">{L.esc(b)}</span></div>'''
                 for l, a, b in metriken)

    # "Who I am": Herkunft statt Angebot. Inhalte von akyol.de, Sektionen
    # Philosophie, Geschaeftsverantwortung und Wertversprechen.
    werdegang = [
        ("Eighteen years in industry, at the seam between engineering and market",
         "Business responsibility in operating roles, not in advisory ones. As Business Manager "
         "in healthcare IT I ran a unit of 80 people, from sales through to development, with "
         "hospital groups among the customers. In renewable energy it was wind power with "
         "international partners and solar thermal across EMEA, including work with Siemens "
         "and the German Aerospace Center.",
         "https://www.akyol.de/index.html#industrie", "The projects behind this"),
        ("Transformation as line work",
         "Lean Six Sigma, an ERP rollout, post-merger integration of people and systems with "
         "buy-in rather than turnover, commercial analytics for a sales force of a thousand "
         "across EMEA. The kind of work where the organisational chart is the easy part.",
         "", ""),
        ("Research first: RWTH Aachen",
         "A doctorate in artificial intelligence and image processing, awarded with distinction, "
         "at a time when AI was a niche subject. Gesture recognition for automotive on-board "
         "systems, a sign language exhibit at the Heinz Nixdorf MuseumsForum, publications and "
         "teaching. The question was the same then as now: what can the machine actually do, "
         "and how does it land with the person using it.",
         "https://www.akyol.de/index.html#wurzeln", "Where this comes from"),
        ("Why this preview exists at all",
         "I work as an interim manager for technical mid-sized companies and for group "
         "subsidiaries that are still run in a mid-sized way. A website built like this is not "
         "my trade, it is the shortest way to show what an organisation can do for itself once "
         "the work is set up properly. One contact who has run technical organisations himself, "
         "rather than a chain of internal handovers.",
         "https://www.akyol.de/", "akyol.de"),
    ]
    wk = "".join(
        f"<div><h4>{L.esc(t)}</h4><p>{L.esc(x)}</p>"
        + (f'<p style="margin-top:14px"><a href="{u}" target="_blank" rel="noopener">'
           f'{L.esc(lt)}</a></p>' if u else "")
        + "</div>" for t, x, u, lt in werdegang)

    refs = [
        ("cancontrols", "CanControls", "Measurement technology for engine development. B2B, "
         "technical audience, explanation-heavy subject matter.",
         "https://suak0903.github.io/cancontrols/", False),
        ("seitec", "SEITec", "Safety and electrical engineering for industrial clients. "
         "Certifications, services, plant environment.",
         "https://suak0903.github.io/seitec/", False),
        ("akyol", "akyol.de", "My own site: interim management, writing and talks. "
         "The reference implementation for everything shown here.",
         "https://www.akyol.de", True),
        ("coreform", "core:form", "Pilates studio in Cologne, in operation on its own domain.",
         "https://www.core-form.de", False),
        ("barista", "Barista-Biker", "Mobile coffee service and events, in operation on its "
         "own domain.", "https://barista-biker.de/", False),
        ("msrodenkirchen", "MS Rodenkirchen", "Restaurant ship in Cologne. The most recent "
         "concept, built one week before this one.",
         "https://suak0903.github.io/ms-rodenkirchen/", False),
    ]
    rk = []
    for key, name, text, url, extra in refs:
        zusatz = ""
        if extra:
            zusatz = '''<div class="ref__extra"><div class="lbl">Interactive talks</div>
          <a href="https://akyol.de/presentations/ki-gestern-heute-morgen/" target="_blank" rel="noopener">KI: gestern, heute, morgen</a>
          <a href="https://akyol.de/presentations/ki-arbeitsarchitektur/" target="_blank" rel="noopener">KI als Arbeitsarchitektur</a>
        </div>'''
        rk.append(f'''<div class="ref">
      <img class="ref__shot" src="{root}media/refs/{key}.webp" alt="Start page of {L.esc(name)}"
           width="640" height="400" loading="lazy" decoding="async">
      <div class="ref__body">
        <h4>{L.esc(name)}</h4><p>{L.esc(text)}</p>
        <a href="{url}" target="_blank" rel="noopener">View live</a>
        {zusatz}
      </div>
    </div>''')

    toc = [("01", "What was built", "#built"), ("02", "Design system", "#design"),
           ("03", "The full picture", "#scope"), ("04", "Scope scale", "#scale"),
           ("05", "What is different", "#different"),
           ("06", "Technology and peace of mind", "#tech"),
           ("07", "References", "#refs"), ("08", "Who I am", "#who")]
    toc_html = "".join(f'<a href="{z}"><i>{n}</i> {L.esc(t)}</a>' for n, t, z in toc)

    # Groessenordnungen des Bestands, alle Werte gemessen (siehe _src/data.json,
    # news.json, team.json und die Sitemaps der Bestandsseite)
    umfang = [
        ("387", "page addresses in the existing sitemap, across all three languages"),
        ("160", "English pages, each carried over here at its original address"),
        ("13", "product areas with over one hundred product types below them"),
        ("107", "news and press posts in the archive, 41 of them in English"),
        ("23", "individual team profiles, each with its own page"),
        ("743", "media files registered in the existing site"),
        ("8", "certification marks to keep current"),
        ("3", "languages: English, German and Polish"),
    ]
    umfang_html = "".join(
        f"<div><b>{L.esc(w)}</b><span>{L.esc(t)}</span></div>" for w, t in umfang)

    umgesetzt = [
        "Complete design system in the Ingredion colour and layout world, with the KaTech logo "
        "and its yellow kept as the mark of identity",
        "All 13 product areas and every product type below them, navigable and with their own "
        "text and image from the existing site",
        "Every page of the existing site is here. 22 of them carry no content on the existing "
        "site either; they are marked as empty and link to the original, so you can check that "
        "for yourself rather than take our word for it",
        "The three advice tabs that sit under each product description on the existing site "
        "(new product, troubleshooting, cost optimisation) carried over for all 67 products "
        "that have them, open on the page instead of hidden behind a click",
        "All legal texts taken over word for word, with anything inconsistent flagged as a "
        "visible note rather than silently corrected",
        "The certificates themselves held on the site: BRCGS, IFS, RSPO, non-GMO, Sedex and the "
        "environmental policy, instead of links pointing at the previous domain",
        "Every existing page kept at its original address, so bookmarks and external links "
        "continue to work",
        "Company, expertise, facilities, certifications and locations, restructured into four "
        "clear routes instead of a menu with over one hundred entries",
        "News archive and all team profiles as individual pages",
        "Enquiry form, mobile navigation, image gallery and consent-gated maps, tested by machine "
        "on desktop and on a phone",
        "Machine-readable structure for search engines and AI assistants: organisation, product "
        "lists, articles and breadcrumbs",
        "Social preview images, sitemap, error page and a text file that tells AI assistants what "
        "this company does",
        "Built for phones first and verified down to 320 pixels without a single horizontal "
        "overflow",
        "Static delivery without WordPress, plugins or a database",
    ]
    offen = [
        "Writing content for the 22 pages that are empty on the existing site as well, plus the "
        "full news archive beyond the English part shown here",
        "The German and Polish versions, and the habit of making every future change three times",
        "Connecting the enquiry route to your mailboxes, including who receives which product area",
        "A publishing workflow and the training that goes with it, so your team changes content "
        "without calling an agency",
        "Redirects and search engine migration from the existing domain, so nothing that ranks "
        "today is lost",
        "Hosting, operation, backups and the question of who is responsible for what",
        "Legal texts reviewed against the current company structure rather than carried over",
        "The approval loop with Ingredion for the final corporate design and the corporate "
        "typeface licence",
        "Photography: the current images are from 2012 and 2013, and the plant-based centre of "
        "excellence does not appear in a single one of them",
    ]
    haken = ('<svg width="15" height="12" viewBox="0 0 15 12" fill="none" aria-hidden="true">'
             '<path d="M1 6.2 5.4 10.6 14 2" stroke="currentColor" stroke-width="2"/></svg>')
    offen_zeichen = ('<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">'
                     '<circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.6"/>'
                     '<path d="M7 3.6V7l2.4 1.6" stroke="currentColor" stroke-width="1.6"/></svg>')
    umgesetzt_html = "".join(
        f'<li><i class="mark mark--done">{haken}</i><span>{L.esc(t)}</span></li>' for t in umgesetzt)
    offen_html = "".join(
        f'<li><i class="mark mark--open">{offen_zeichen}</i><span>{L.esc(t)}</span></li>' for t in offen)

    inhalt = f'''<section class="subhero" id="toc">
  <div class="subhero__inner">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{root}index.html">Start</a>
      <span aria-hidden="true">/</span>About this preview</nav>
    <p class="eyebrow">Redesign preview</p>
    <h1>About this <em>preview</em>.</h1>
    <p class="subhero__sub">What this is, what was built, how far it goes and what it would take
      to put it live. Written for the people who have to decide, not for developers.</p>
    <div class="toc">{toc_html}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap--narrow">
    <div class="notice rv">
      <h3>Please note</h3>
      <ul>
        <li>This is a <strong>non-binding design concept</strong>, produced independently by
          Dr.-Ing. Suat Akyol. It is not commissioned work and not an offer.</li>
        <li>It is <strong>blocked for search engines</strong> and does not compete with the
          existing site.</li>
        <li>All texts and photographs come <strong>exclusively from the publicly available
          existing website</strong> of KaTech Ingredient Solutions and remain the property of
          their owners.</li>
        <li>There is <strong>no connection</strong> to the official KaTech or Ingredion web
          presence. It can be taken offline at any time on request.</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--sand" id="built">
  <div class="wrap">
    {L.sec_kopf(eyebrow="What was built", h2="The same site, rebuilt.",
                lead="Nothing was left out. Every area of the existing site exists here, and "
                     "every page kept its original address.")}
    {L.stats([(str(anzahl_seiten), "existing pages carried over"),
              ("13", "product areas, all built out"),
              (str(anzahl_news), "news releases, complete"),
              ("167", "original images reused")])}
    <div class="grid grid--2 rv" style="margin-top:36px">
      <div class="loc">
        <span class="loc__role">Finished and working</span>
        <h3>What you can click today</h3>
        <ul style="margin:0;padding-left:1.2em;font-size:15.5px;color:var(--ink-soft)">
          <li>Start page, all eleven product areas and every product type below them</li>
          <li>Company, expertise, facilities, certifications and locations</li>
          <li>Complete news archive with detail pages</li>
          <li>Enquiry form, mobile navigation, image gallery, consent-gated maps</li>
          <li>Schema markup, social preview images, sitemap and error page</li>
        </ul>
      </div>
      <div class="loc">
        <span class="loc__role">Open for live operation</span>
        <h3>What would still be done</h3>
        <ul style="margin:0;padding-left:1.2em;font-size:15.5px;color:var(--ink-soft)">
          <li>Connect the enquiry form to your mailbox</li>
          <li>German and Polish versions from your existing translations</li>
          <li>Final Ingredion corporate design values once the group specification lands</li>
          <li>Move to your domain and release it for search engines</li>
          <li>Content editing by your team, by prompt or through a small editor</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="design">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Design system", h2="Your colours. Already the group's colours.",
                lead="The KaTech logo already uses the exact Ingredion values: the green, the "
                     "yellow and the dark grey are identical. The website simply never followed. "
                     "This preview closes that gap.")}
    <div class="ds rv">{ds}</div>
    <div class="prose rv">
      <p>Two typefaces are used. Headlines are set in <strong>Barlow</strong>, a compact,
        straightforward typeface without the small serifs, close in character to the one the
        group uses. Body text is set in <strong>Open Sans</strong>, which is literally the
        same family Ingredion uses on its own site.</p>
      <p>Both are free to license and are delivered from the site itself, so no data goes to
        a font service and nothing depends on an external provider. When the group licence for
        the corporate typeface arrives, swapping it is a one-line change.</p>
    </div>
  </div>
</section>

<section class="sec sec--ink" id="scope">
  <div class="wrap">
    {L.sec_kopf(eyebrow="The full picture", h2="What is actually in there.",
                lead="A website of this kind is not one page, it is an archive. These are the "
                     "measured numbers of the existing site, and they are the reason this preview "
                     "rebuilt the structure rather than a few sample screens.")}
    <div class="scopegrid rv">{umfang_html}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="grid grid--2" style="gap:clamp(32px,4vw,56px);align-items:start">
      <div class="rv">
        {L.sec_kopf(eyebrow="Already done", h2="What this preview already delivers.")}
        <ul class="cklist cklist--done">{umgesetzt_html}</ul>
      </div>
      <div class="rv">
        {L.sec_kopf(eyebrow="Still open", h2="What the real project would still involve.")}
        <ul class="cklist cklist--open">{offen_html}</ul>
      </div>
    </div>
    <div class="prose rv" style="margin-top:44px;max-width:74ch">
      <p>The two lists are deliberately shown side by side. The left one is design and structure,
        and that work is largely behind us. The right one is content, languages and operations,
        and that is where a project of this kind actually lives.</p>
      <p>It is worth saying plainly: the site is trilingual, which means every text decision is
        made once and carried three times. That single fact shapes the size of the undertaking
        more than any design question.</p>
    </div>
  </div>
</section>

<section class="sec sec--sand" id="scale">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Scope", h2="How far this goes.",
                lead="A website can be a single page or a platform. Saying out loud where "
                     "a project sits keeps everyone talking about the same thing.")}
    <div class="rv">
      <div class="scale">
        <div class="scale__bar">
          <span class="scale__mk scale__mk--rec" style="left:72%"><i>My recommendation</i></span>
          <span class="scale__mk scale__mk--now" style="left:62%"><i>This preview</i></span>
          <span class="scale__mk scale__mk--full" style="left:55%"><i>Your current site, rebuilt</i></span>
        </div>
        <div class="scale__nums"><span>0</span><span>2</span><span>4</span><span>6</span><span>8</span><span>10</span></div>
        <div class="scale__steps">
          <div><b>0 to 1</b>Single page, no subpages, no forms</div>
          <div><b>around 5</b>Multi-page site: form, SEO and AI findability, media gallery, news</div>
          <div><b>10</b>All in: online ordering, CMS, customer login, AI assistant, analytics</div>
        </div>
      </div>
    </div>
    <div class="prose rv" style="margin-top:40px">
      <ul>
        <li><strong>Your current site rebuilt sits around 5.5.</strong> Many pages, a form, news,
          three languages, no login and no shop.</li>
        <li><strong>This preview sits slightly above it</strong>, because findability, speed and
          the schema work are already included.</li>
        <li><strong>My recommendation sits a little higher again:</strong> add the customer area
          with real content and let your own team edit pages. Both are steps, not a rebuild.</li>
        <li><strong>Eight to ten is a different horizon</strong>, not a gap you are behind on:
          customer login with documents, and an assistant that answers formulation questions
          from your own product data.</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec" id="different">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Comparison", h2="What is different.",
                lead="Measured, not asserted. The existing site does several things right, "
                     "including a clean sitemap structure and consistent page titles.")}
    <div class="rv" style="overflow-x:auto">
      <table class="cmp">
        <thead><tr><th>Aspect</th><th>Current site</th><th>This preview</th></tr></thead>
        <tbody>{zeilen}</tbody>
      </table>
    </div>
    <div class="metrics rv" style="margin-top:40px">{mk}</div>
  </div>
</section>

<section class="sec sec--sand" id="tech">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Technology and peace of mind", h2="Nothing is lost, nothing is risked.",
                lead="The existing site runs on WordPress with a custom theme built in 2013, "
                     "hosted on a virtual server in London.")}
    <div class="why rv">
      <div><h4>Your current site stays untouched</h4>
        <p>The new site runs in parallel on a separate address until you decide to switch.
          The switch itself is one setting, and it is reversible.</p></div>
      <div><h4>A full backup before anything happens</h4>
        <p>The existing site is backed up completely and stays restorable after the switch.
          There is no point at which the old site is gone.</p></div>
      <div><h4>No plugin treadmill</h4>
        <p>Static HTML has no database and no plugins, so there is nothing to patch on a
          Friday evening and nothing that breaks when a plugin updates itself.</p></div>
      <div><h4>Your addresses stay valid</h4>
        <p>Every page here sits at the address it has today. Bookmarks, links in supplier
          documents and search results keep working.</p></div>
      <div><h4>The site belongs to you</h4>
        <p>Full rights to everything that is built, no lock-in, no dependency you cannot leave.
          If you want to move it elsewhere or hand it to your own IT, you do exactly that.</p></div>
    </div>
  </div>
</section>

<section class="sec" id="refs">
  <div class="wrap">
    {L.sec_kopf(eyebrow="References", h2="Other sites I have built.",
                lead="B2B and industry first, then the range. Some are in operation on their "
                     "own domain, others are concepts like this one.")}
    <div class="refs rv">{"".join(rk)}</div>
  </div>
</section>

<section class="sec sec--sand" id="who">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Who I am", h2="Twenty-five years of people and machines.",
                lead="Dr.-Ing. Suat Akyol, interim manager for technical mid-sized companies and "
                     "for group subsidiaries that are still run in a mid-sized way. Research, "
                     "line management, and artificial intelligence in day-to-day operations.")}
    <div class="why rv">{wk}</div>
    <figure class="quote rv">
      <blockquote>Few people connect strategic and tactical thinking as effectively as he does.</blockquote>
      <figcaption>A former superior, quoted on akyol.de</figcaption>
    </figure>
    <div class="btn-row rv" style="margin-top:36px">
      <a class="btn btn--outline" href="https://www.akyol.de" target="_blank" rel="noopener">akyol.de</a>
      <a class="btn btn--outline" href="https://www.linkedin.com/in/dr-ing-suat-akyol" target="_blank" rel="noopener">LinkedIn</a>
    </div>
  </div>
</section>

<section class="sec sec--teal">
  <div class="wrap wrap--narrow center">
    {L.sec_kopf(h2="Questions about this concept?",
                lead="Comments, corrections and objections are welcome. Write to "
                     "contact@akyol.de.", zentriert=True)}
    <div class="btn-row rv" style="margin-inline:auto">
      <a class="btn btn--ghost" href="mailto:contact@akyol.de">contact@akyol.de</a>
      <a class="btn btn--ghost" href="https://www.akyol.de" target="_blank" rel="noopener">akyol.de</a>
    </div>
  </div>
</section>
<button class="toc-top" id="tocTop" type="button" aria-label="Back to the contents">&uarr;</button>'''

    # Die Hinweisseite traegt keine Demo-Leiste (Kit-Standard). Ohne diese
    # Klasse bliebe der Freiraum fuer sie stehen und erschiene als weisser
    # Streifen unter der Fusszeile.
    html = L.seite("about-this-preview/index.html", "About this preview",
                   "What this redesign concept for KaTech contains, how it was built and what "
                   "it would take to put it live.",
                   inhalt, og="og-preview.jpg", body_klasse="ohne-demobar")
    # Demo-Leiste auf der Hinweisseite selbst entfernen (Standard des Kits)
    html = re.sub(r'<div class="demobar" id="demobar">.*?</div>\s*(?=<div class="consent")',
                  "", html, flags=re.S)
    schreibe("about-this-preview/index.html", html)


# --------------------------------------------------------------------------
# Team-Seite und Personenprofile
# --------------------------------------------------------------------------
GRUPPEN_REIHENFOLGE = ["Management", "Technical, Germany", "Technical, United Kingdom",
                       "Sales, Germany", "Sales, United Kingdom", "Sales, Poland", "Purchasing"]

# Rollen, die von der Bestandsseite abweichen sollen. Die Profile der
# Bestandsseite stammen aus 2014 bis 2018 und sind teilweise ueberholt;
# hier wird korrigiert, ohne die Datenbasis anzufassen.
# Schluessel ist der Seiten-Slug, Wert die anzuzeigende Rolle.
ROLLEN_OVERRIDE = {}


def rolle_von(person):
    return ROLLEN_OVERRIDE.get(person["slug"], person["rolle"])


def _team(schreibe, SEITEN, kurz):
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "team.json")
    if not os.path.exists(pfad):
        return
    leute = json.load(open(pfad, encoding="utf-8"))
    root = "../"
    s = SEITEN.get("our-people", {})
    einleitung = s.get("absaetze", [])

    bloecke = []
    for gruppe in GRUPPEN_REIHENFOLGE:
        mitglieder = [p for p in leute if p["gruppe"] == gruppe]
        if not mitglieder:
            continue
        karten = "".join(f'''<a class="person" href="{root}{p['slug']}/">
      <span class="person__foto"><picture>
        <source srcset="{root}media/team-{p['slug']}.webp" type="image/webp">
        <img src="{root}media/team-{p['slug']}.jpg" alt="{L.esc(p['name'])}"
             width="440" height="440" loading="lazy" decoding="async"></picture></span>
      <span class="person__text">
        <span class="person__ort">{L.esc(p['ort'])}</span>
        <span class="person__name">{L.esc(p['name'])}</span>
        <span class="person__rolle">{L.esc(rolle_von(p))}</span>
      </span>
    </a>''' for p in mitglieder)
        bloecke.append(f'''<section class="sec{' sec--sand' if len(bloecke) % 2 else ''}">
  <div class="wrap">
    {L.sec_kopf(eyebrow=gruppe, h2=f"{len(mitglieder)} {'person' if len(mitglieder) == 1 else 'people'} in this team.")}
    <div class="grid grid--3 rv">{karten}</div>
  </div>
</section>''')

    inhalt = L.subhero(root, crumbs=[("Start", root + "index.html"),
                                     ("Company", root + "company/"), ("Our people", None)],
                       eyebrow="Our people", h1="The people who build the formulation.",
                       sub=kurz(einleitung[0], 210) if einleitung else
                           "Technologists and technical sales staff with hands-on experience in "
                           "real production environments.",
                       bild="development-meeting", alt="KaTech development meeting")
    if einleitung:
        inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow">
    {L.prosa([L.absatz(t) for t in einleitung])}
  </div>
</section>'''
    inhalt += "\n" + "\n".join(bloecke)
    inhalt += f'''
<section class="sec sec--teal">
  <div class="wrap wrap--narrow center">
    {L.sec_kopf(h2="Talk to the person who will do the work.",
                lead="Enquiries go to the technologist responsible for your product area, "
                     "not into a general inbox.", zentriert=True)}
    <div class="btn-row btn-row--single rv" style="margin-inline:auto">
      <a class="btn btn--ghost" href="{root}contact-us/">Make an enquiry</a>
    </div>
  </div>
</section>'''
    schreibe("our-people/index.html", L.seite(
        "our-people/index.html", "Our people",
        "The KaTech team: technologists and technical sales staff in Germany, the United "
        "Kingdom and Poland.", inhalt, aktiv="company/", og="og-company.jpg",
        jsonld=ld_liste("Our people", [(p["name"], L.PAGES_URL + p["slug"] + "/") for p in leute])))

    # Einzelprofile
    for p in leute:
        r = "../"
        kollegen = [k for k in leute if k["gruppe"] == p["gruppe"] and k["slug"] != p["slug"]][:3]
        weitere = "".join(f'''<a class="person" href="{r}{k['slug']}/">
      <span class="person__foto"><picture>
        <source srcset="{r}media/team-{k['slug']}.webp" type="image/webp">
        <img src="{r}media/team-{k['slug']}.jpg" alt="{L.esc(k['name'])}"
             width="440" height="440" loading="lazy" decoding="async"></picture></span>
      <span class="person__text">
        <span class="person__ort">{L.esc(k['ort'])}</span>
        <span class="person__name">{L.esc(k['name'])}</span>
        <span class="person__rolle">{L.esc(rolle_von(k))}</span>
      </span>
    </a>''' for k in kollegen)
        vita = "".join(f"<p>{L.esc(a)}</p>" for a in p["vita"]) or f"<p>{L.esc(PLATZHALTER)}</p>"
        inhalt = L.subhero(r, crumbs=[("Start", r + "index.html"), ("Company", r + "company/"),
                                      ("Our people", r + "our-people/"), (p["name"], None)],
                           eyebrow=p["gruppe"], h1=L.esc(p["name"]),
                           sub=rolle_von(p))
        inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow">
    <div class="profil rv">
      <picture>
        <source srcset="{r}media/team-{p['slug']}.webp" type="image/webp">
        <img src="{r}media/team-{p['slug']}.jpg" alt="{L.esc(p['name'])}"
             width="440" height="440" loading="eager" decoding="async">
      </picture>
      <div class="profil__daten">
        <h2>{L.esc(rolle_von(p))}</h2>
        <dl>
          <dt>Team</dt><dd>{L.esc(p['gruppe'])}</dd>
          <dt>Based in</dt><dd>{L.esc(p['ort'])}</dd>
        </dl>
      </div>
    </div>
    <div class="prose rv">{vita}</div>
  </div>
</section>'''
        if weitere:
            inhalt += f'''
<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow=p['gruppe'], h2="Colleagues in this team.")}
    <div class="grid grid--3 rv">{weitere}</div>
    <div class="btn-row btn-row--single rv" style="margin-top:30px">
      <a class="btn btn--outline" href="{r}our-people/">The whole team</a>
    </div>
  </div>
</section>'''
        schreibe(p["slug"] + "/index.html", L.seite(
            p["slug"] + "/index.html", p["name"],
            f"{p['name']}, {rolle_von(p)} at KaTech Ingredient Solutions, {p['ort']}.",
            inhalt, aktiv="company/", og="og-company.jpg",
            jsonld={"@context": "https://schema.org", "@type": "ProfilePage",
                    "mainEntity": {"@type": "Person", "name": p["name"], "jobTitle": rolle_von(p),
                                   "worksFor": {"@type": "Organization",
                                                "name": "KaTech Ingredient Solutions GmbH"}}}))


# --------------------------------------------------------------------------
# Kurztexte der Produktbereiche
# Der Bestandstext ist an diesen Stellen Lexikonprosa ("cheese is a nutritious
# food made mostly from the milk of cows"). Fuer Kacheln und Einstiege braucht
# es je einen Satz, der das technische Problem benennt, das KaTech loest.
# --------------------------------------------------------------------------
BEREICHS_KURZTEXT = {
    "vegan": "Meat and fish alternatives that keep their bite. Texture built on dedicated pilot "
             "machinery, not on paper.",
    "yogurt": "Set, stirred, drinking or Greek style: the mouthfeel consumers expect, at the fat "
              "level your costing allows.",
    "cheese": "Cream cheese, processed, quarg, analogue. Spreadability and melt behaviour that "
              "survive your process.",
    "cream": "Whipping, cooking, sour and non-dairy. Stability through heat, shear and shelf life.",
    "desserts": "Mousse, custard, jelly, cheesecake. Aeration and set that stay put until the spoon.",
    "milk-drinks": "Flavoured, acidified, shakes and dairy alternatives. No sedimentation, no "
                   "separation, no chalky finish.",
    "mayonnaise": "Full fat, reduced fat, egg free, clean label. Emulsions that do not break on "
                  "the line.",
    "dressings": "Clear, emulsified or dairy based. Suspension that survives a shelf and a shake.",
    "dips": "Sour cream, yogurt, quarg or mayonnaise based. Body without gumminess.",
    "soups-and-sauces": "Fresh, pasteurised, sterilised, high fat. Viscosity that behaves the same "
                        "after every batch.",
    "soups": "Fresh and pasteurised soups with the body they need and the label you want.",
    "bakery": "Cakes, muffins, choux, fillings and toppings, including the Scratch Plus system for "
              "clean label and allergen free baking.",
    "fruit": "Preparations, fillings, glazes and jellies. Fruit that stays where you put it.",
}

# Bereichsbilder, wo das Bestandsbild fehlt oder nicht traegt
BEREICHS_BILD = {
    "vegan": "p-vegan-plant-based-mince",
    "soups": "p-soups-freshpasteurised",
}
