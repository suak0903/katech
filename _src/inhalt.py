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

PLATZHALTER = ("This page exists in the current website structure and is carried over so that "
               "nothing is lost in the redesign. In this preview it is shown as a designed "
               "placeholder: the live version carries the full text, images and downloads of "
               "the existing page.")

# Marke im Seitenkopf und Kasten im Inhalt, wenn eine Seite bewusst noch
# nicht ausgebaut ist. Ohne diese Kennzeichnung wirkt eine solche Seite wie
# ein Fehler statt wie eine gezogene Grenze.
STUB_MARKE = ('<span class="stubtag">Not built out in this preview</span>')


def stub_kasten(root, slug):
    original = "https://katech-solutions.com/" + (slug + "/" if slug else "")
    return f'''<div class="stub rv">
      <div class="stub__head">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <circle cx="10" cy="10" r="8.6" stroke="currentColor" stroke-width="1.7"/>
          <path d="M10 5.4V10l3.2 2.2" stroke="currentColor" stroke-width="1.7"/></svg>
        <h2>This page is not built out yet.</h2>
      </div>
      <p>It exists in your current site structure and is carried over here at its original
        address, so that nothing is lost and no link runs into a dead end. What is missing is
        the content itself: the existing page carries text, images and downloads that were not
        part of this preview.</p>
      <p>In the real project this page is filled like every other one. It is shown this way on
        purpose rather than quietly left out, so you can see exactly where the boundary of this
        preview runs.</p>
      <div class="stub__links">
        <a class="btn btn--outline" href="{original}" target="_blank" rel="noopener">See the current page</a>
        <a class="btn btn--outline" href="{root}about-this-preview/#scope">What is and is not included</a>
      </div>
    </div>'''

ZERTIFIKATE = [
    ("cert-brcgs-cert-food-logo.png", "BRCGS Food Safety certification, AA rating"),
    ("cert-ifs-food-box-rgb.png", "IFS Food certification"),
    ("cert-rspo-1106196-logo-2021.png", "RSPO certified sustainable palm oil"),
    ("cert-sedex-logo-small.png", "Sedex membership"),
    ("cert-horzfoodchain-certificat.png", "FoodChain ID non-GMO certification"),
    ("cert-gb-organic-logo-181x229-.png", "Organic certification"),
    ("cert-kosher-certification-197.png", "Kosher certification"),
    ("cert-halal-logo-blk-web-june-.png", "Halal certification"),
]

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
                   "bakery", "fruit"]
KEINE_BEREICHE = ["bakery-old", "find-us", "our-people", "our-ingredients", "certifications"]

TITEL = {
    "vegan": "Plant-based meat and fish alternatives",
    "cheese": "Cheese is a tasty, flexible and delicious foodstuff with endless applications",
    "how-we-work": "Working with you, to deliver on your objectives",
}

KURZTITEL = {
    "vegan": "Plant-based",
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

MONATE = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def datum_lang(iso):
    j, m, t = iso.split("-")
    return f"{int(t)} {MONATE[int(m) - 1]} {j}"


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
    hub("expertise", "Expertise", "What we bring to the table",
        "Formulation knowledge, and the equipment to prove it.",
        "Our technologists work hands-on: from the first concept through pilot trials to the "
        "run on your production line.",
        [("Development services",
          ("Where our work starts.",
           "Four routes into a project. Most customers arrive through one of them and end up "
           "using several."),
          [("new-products", "New product development", ""),
           ("replication", "Replication", ""),
           ("troubleshooting", "Troubleshooting", ""),
           ("cost-optimisation", "Cost optimisation", "")]),
         ("Reformulation",
          ("Taking things out without taking taste out.",
           "Fat and sugar reduction are texture problems long before they are nutrition claims."),
          [("fat-reduction", "Fat reduction", ""),
           ("sugar-reduction", "Sugar reduction", ""),
           ("specials", "Specials", ""),
           ("products", "Our products", "")]),
         ("Ingredients and people",
          ("What goes in, and who works on it.",
           "The raw material base we formulate from, and the team behind it."),
          [("our-ingredients", "Ingredients used", ""),
           ("our-ingredients/ingredients-list", "Ingredients list", ""),
           ("our-people", "Our people", ""),
           ("case-studies", "Case studies", "")])],
        og="og-expertise.jpg", bild="lab-measurement")

    hub("company", "Company", "Who we are",
        "A food technology company that stayed hands-on.",
        "Founded in Lübeck in 2010, around 95 people across Germany, the UK and Poland, "
        "part of Ingredion since 2021.",
        [("The business",
          ("What drives the company.",
           "Vision, approach and the way we work with customers."),
          [("our-vision", "Our vision", ""),
           ("our-approach", "Our approach", ""),
           ("how-we-work", "How we work", ""),
           ("careers", "Careers", "")]),
         ("Sites and production",
          ("Where the work happens.",
           "Development suites, production and warehousing across three countries."),
          [("our-facilities", "Our facilities", ""),
           ("production-facilities-germany", "Production, Germany", ""),
           ("technical-development-suite-germany", "Development suite, Germany", ""),
           ("technical-development-suite-uk", "Development suite, UK", ""),
           ("sales-office-poland", "Sales office, Poland", ""),
           ("find-us", "Find us", "")]),
         ("Standards and sourcing",
          ("What we can prove.",
           "Certifications, raw material policy and the sustainability position."),
          [("certifications", "Certifications", ""),
           ("gm-status", "GM status", ""),
           ("raw-materials", "Raw materials", ""),
           ("sourcing-and-sustainability", "Sourcing and sustainability", ""),
           ("purchasing", "Purchasing", ""),
           ("customer-area", "Customer area", "")])],
        og="og-company.jpg", bild="hq-luebeck")


# --------------------------------------------------------------------------
# Textseiten
# --------------------------------------------------------------------------
COMPANY_SEITEN = [
    ("our-vision", "hq-luebeck"), ("our-approach", "reception"),
    ("our-facilities", "blending-tower"), ("careers", "sensory-panel"),
    ("production-facilities-germany", "plant-reinfeld"),
    ("technical-development-suite-germany", "lab-measurement"),
    ("technical-development-suite-uk", "warehouse"),
    ("sales-office-poland", "reception"),
    ("certifications", None), ("certifications/rspo", None),
    ("gm-status", None), ("raw-materials", "raw-materials"),
    ("sourcing-and-sustainability", None), ("purchasing", None),
    ("customer-area", None), ("case-studies", None),
    ("our-people/sales-team", None), ("our-people/development-team", None),
]

EXPERTISE_SEITEN = [
    ("new-products", "development-meeting"), ("replication", None),
    ("troubleshooting", None), ("cost-optimisation", None),
    ("fat-reduction", None), ("sugar-reduction", None),
    ("specials", None), ("products", "sensory-panel"),
    ("our-ingredients", "raw-materials"), ("our-ingredients/ingredients-list", None),
]

LEGAL_SEITEN = ["imprint", "privacy-policy", "terms-of-use", "cookie-policy-eu",
                "data-protection-information-for-applicants"]


def baue_textseiten(textseite):
    for slug, bild in COMPANY_SEITEN:
        extra = ""
        if slug == "certifications":
            extra = f'''<section class="sec sec--sand">
  <div class="wrap">
    {L.sec_kopf(eyebrow="Audited and certified", h2="The standards we hold.", zentriert=True)}
    {L.zertifikate("../", ZERTIFIKATE)}
  </div>
</section>'''
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
        # "Our facilities" steht als eigener Punkt in der Hauptnavigation und
        # muss dort markiert werden, nicht unter "Company".
        aktiv = "our-facilities/" if slug == "our-facilities" else "company/"
        textseite(slug, eyebrow="Company",
                  crumbs_extra=[("Company", "../" * (slug.count("/") + 1) + "company/")],
                  bild=bild, extra_html=extra, aktiv=aktiv)

    for slug, bild in EXPERTISE_SEITEN:
        textseite(slug, eyebrow="Expertise",
                  crumbs_extra=[("Expertise", "../" * (slug.count("/") + 1) + "expertise/")],
                  bild=bild, aktiv="expertise/")

    for slug in LEGAL_SEITEN:
        textseite(slug, eyebrow="Legal", crumbs_extra=None, bild=None, aktiv="")


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
              <option>Plant-based meat and fish</option><option>Yogurt</option>
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
                                     ("Company", root + "company/"), ("Find us", None)],
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
        inhalt, aktiv="company/", og="og-company.jpg", jsonld=LD_ORG))

    for s, slug in zip(STANDORTE, ["find-us/katech-head-office-germany",
                                   "find-us/katech-production-germany",
                                   "find-us/katech-uk", "find-us/katech-poland"]):
        r = "../../"
        inhalt = L.subhero(r, crumbs=[("Start", r + "index.html"), ("Company", r + "company/"),
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
            aktiv="company/", og="og-company.jpg"))


def _sitemap(schreibe, SEITEN, BAUM, NEWS, kurztitel):
    root = "../"
    abschnitte = []
    for _, titel, _, bereiche in CLUSTER:
        zeilen = []
        for b in bereiche:
            unter = "".join(f'<li><a href="{root}{u}/">{L.esc(kurztitel(u))}</a></li>'
                            for u in BAUM.get(b, []))
            zeilen.append(f'<li><a href="{root}{b}/"><strong>{L.esc(kurztitel(b))}</strong></a>'
                          f'<ul>{unter}</ul></li>')
        abschnitte.append(f"<h2>{L.esc(titel)}</h2><ul>{''.join(zeilen)}</ul>")

    firma = "".join(f'<li><a href="{root}{s}/">{L.esc(kurztitel(s))}</a></li>'
                    for s, _ in COMPANY_SEITEN)
    exp = "".join(f'<li><a href="{root}{s}/">{L.esc(kurztitel(s))}</a></li>'
                  for s, _ in EXPERTISE_SEITEN)
    nw = "".join(f'<li><a href="{root}{n["slug"]}/">{L.esc(n["titel"])}</a></li>'
                 for n in NEWS if n["slug"] != "news" and n["absaetze"])
    legal = "".join(f'<li><a href="{root}{s}/">{L.esc(kurztitel(s))}</a></li>' for s in LEGAL_SEITEN)
    abschnitte.append(f"<h2>Company</h2><ul>{firma}</ul>")
    abschnitte.append(f"<h2>Expertise</h2><ul>{exp}</ul>")
    abschnitte.append(f"<h2>News</h2><ul>{nw}</ul>")
    abschnitte.append(f"<h2>Legal</h2><ul>{legal}</ul>")

    inhalt = L.subhero(root, crumbs=[("Start", root + "index.html"), ("Sitemap", None)],
                       eyebrow="Overview", h1="Every page in this preview.",
                       sub="The full structure of the existing site, carried over one to one.")
    inhalt += f'''
<section class="sec">
  <div class="wrap">
    <div class="prose rv" style="max-width:none;column-count:2;column-gap:48px">
      {"".join(abschnitte)}
    </div>
  </div>
</section>'''
    schreibe("sitemap/index.html", L.seite(
        "sitemap/index.html", "Sitemap", "Full page overview of the KaTech design preview.",
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
        "173 of the 200 pages carry real content; the remaining 27 are marked as not built out "
        "rather than quietly left blank, so the boundary of this preview is visible",
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
        "Filling the 27 pages that are marked as not built out, plus the detail content and the "
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

    html = L.seite("about-this-preview/index.html", "About this preview",
                   "What this redesign concept for KaTech contains, how it was built and what "
                   "it would take to put it live.",
                   inhalt, og="og-preview.jpg")
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
        karten = "".join(f'''<a class="tile" href="{root}{p['slug']}/">
      <span class="tile__num">{L.esc(p['ort'])}</span>
      <h3>{L.esc(p['name'])}</h3>
      <p>{L.esc(rolle_von(p))}</p>
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
        weitere = "".join(f'''<a class="tile" href="{r}{k['slug']}/">
      <span class="tile__num">{L.esc(k['ort'])}</span>
      <h3>{L.esc(k['name'])}</h3><p>{L.esc(rolle_von(k))}</p>
    </a>''' for k in kollegen)
        vita = "".join(f"<p>{L.esc(a)}</p>" for a in p["vita"]) or f"<p>{L.esc(PLATZHALTER)}</p>"
        inhalt = L.subhero(r, crumbs=[("Start", r + "index.html"), ("Company", r + "company/"),
                                      ("Our people", r + "our-people/"), (p["name"], None)],
                           eyebrow=p["gruppe"], h1=L.esc(p["name"]),
                           sub=rolle_von(p))
        inhalt += f'''
<section class="sec">
  <div class="wrap wrap--narrow">
    <div class="factbox rv">
      <h3>{L.esc(rolle_von(p))}</h3>
      <ul><li>Team: {L.esc(p['gruppe'])}</li><li>Based in {L.esc(p['ort'])}</li></ul>
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
