#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Die Informationsarchitektur des Demonstrators - eine einzige Quelle.

Vorher wurde an vier Stellen unabhaengig voneinander festgelegt, zu welchem
Bereich eine Seite gehoert: in der Hub-Kachel, im Wert fuer die
Menuemarkierung, im Breadcrumb-Pfad und in der Seitenliste des Generators.
Sie sind auseinandergedriftet. Hier steht die Zuordnung genau einmal;
Menue, Breadcrumb, Hubs, Sitemap und Pruefung leiten sich daraus ab.
"""

# --------------------------------------------------------------------------
# Die Hauptbereiche. Reihenfolge = Reihenfolge im Menue.
# id, Beschriftung, Startseite des Bereichs
# --------------------------------------------------------------------------
BEREICHE = [
    ("solutions", "Solutions", "solutions/"),
    ("expertise", "Expertise", "expertise/"),
    ("company", "Company", "company/"),
    ("facilities", "Facilities", "our-facilities/"),
    ("news", "News", "news/"),
]

# --------------------------------------------------------------------------
# Gliederung innerhalb der Bereiche.
# Jeder Eintrag: (Abschnittstitel, Ueberschrift, Beschreibung, [Seiten-Slugs])
# Die Reihenfolge bestimmt Hub-Seite und Sitemap.
# --------------------------------------------------------------------------

# --- Solutions: die Produktwelten, gruppiert wie im Bestandsmenue ---------
SOLUTIONS = [
    ("dairy", "Dairy and dairy alternatives",
     ("Where texture is the product.",
      "Yogurt, cream, cheese, desserts and milk drinks. The classic core of KaTech, and still "
      "the area with the deepest formulation library."),
     ["yogurt", "cream", "cheese", "desserts", "milk-drinks"]),
    ("plant", "Plant-based",
     ("Alternatives for meat, fish, dairy and savoury.",
      "The fastest moving category we work in, with a dedicated centre of excellence and its "
      "own pilot machinery in Lübeck. Eighteen product types in four groups."),
     ["vegan"]),
    ("savoury", "Savoury",
     ("Emulsions that hold.",
      "Mayonnaise, dressings, dips, soups and sauces. Cold and hot processes, clean label and "
      "egg-free routes included."),
     ["mayonnaise", "dressings", "dips", "soups-and-sauces"]),
    ("bakery", "Bakery and fruit",
     ("Fillings, toppings, glazes.",
      "From muffin batter to fruit preparation, including the KaTech Scratch Plus system for "
      "clean label and allergen-free baking."),
     ["bakery", "fruit"]),
]

# --- Plant-based: vier Gruppen statt achtzehn Seiten nebeneinander --------
# Vier der achtzehn Seiten sind selbst Ueberkategorien; die uebrigen gehoeren
# darunter. Fuer "Dairy alternatives" und "Savoury" gibt es im Bestand keine
# Kopfseite, dort bleibt es bei einer Gruppenueberschrift. Es wird keine Seite
# erfunden, die es im Original nicht gibt.
VEGAN_GRUPPEN = [
    ("Meat alternatives", "vegan/vegan-meat-alternatives",
     ["vegan/pflanzliche-burger-patties", "vegan/plant-based-cold-cuts",
      "vegan/plant-based-mince", "vegan/plant-based-nuggets",
      "vegan/plant-based-pates", "vegan/wurstchen-alternativen"]),
    ("Fish alternatives", "vegan/plant-based-fish-alternatives",
     ["vegan/plant-based-fish-cakes", "vegan/plant-based-fish-fingers"]),
    ("Dairy alternatives", None,
     ["vegan/vegan-cheese-alternatives", "vegan/vegan-cream-products",
      "vegan/vegan-yogurt", "vegan/vegan-drinks", "vegan/vegan-desserts"]),
    ("Savoury", None,
     ["vegan/vegan-mayonnaises-and-dressings", "vegan/vegan-sauces",
      "vegan/vegan-spreads"]),
]

# Die Suppenseite liegt im Bestand in einem eigenen Bereich mit genau einer
# Seite, obwohl es "Soups and sauces" gibt. Sie wird dort eingeordnet; ihre
# Adresse bleibt unveraendert.
FREMDE_KINDER = {
    "soups-and-sauces": ["soups/freshpasteurised"],
    # Der Bestand fuehrt neben /bakery/ noch einen aelteren Baum /bakery-old/
    # mit drei Seiten. Sie bleiben erreichbar und erscheinen unter Bakery.
    "bakery": ["bakery-old/cleaner-label-cakes", "bakery-old/cleaner-label-muffins",
               "bakery-old/cleaner-label-sponge"],
}

# Seiten des Bestands, die zu keinem Abschnitt gehoeren, aber vorhanden sind
# und deshalb in der Sitemap stehen muessen.
UEBRIGE = ["soups", "venture-point", "stephankoruma-cabinet", "nasz-cel"]

# --- Expertise: was das Unternehmen kann ----------------------------------
EXPERTISE = [
    ("Development services",
     ("Where our work starts.",
      "Four routes into a project. Most customers arrive through one of them and end up "
      "using several."),
     ["new-products", "replication", "troubleshooting", "cost-optimisation"]),
    ("Reformulation",
     ("Taking things out without taking taste out.",
      "Fat and sugar reduction are texture problems long before they are nutrition claims."),
     ["fat-reduction", "sugar-reduction", "specials", "products"]),
    ("What goes in",
     ("The raw material base.",
      "What we formulate from, and where it comes from."),
     ["our-ingredients", "our-ingredients/ingredients-list"]),
]

# --- Company: wer das Unternehmen ist -------------------------------------
COMPANY = [
    ("The business",
     ("What drives the company.",
      "Vision, approach, the people and the work we can show."),
     ["our-vision", "our-approach", "how-we-work", "our-people", "case-studies", "careers"]),
    ("Standards and sourcing",
     ("What we can prove.",
      "Certifications, raw material policy and the sustainability position."),
     ["certifications", "certifications/rspo", "gm-status", "raw-materials",
      "sourcing-and-sustainability", "purchasing"]),
    ("Service",
     ("For existing customers.",
      "Access and documents for customers we already work with."),
     ["customer-area"]),
]

# --- Facilities: wo gearbeitet wird ---------------------------------------
# Frueher ein Menuepunkt ohne eigenen Inhalt. Der Company-Abschnitt
# "Sites and production" ist vollstaendig hierher gewandert (Suat 27.08.).
FACILITIES = [
    ("Sites and production",
     ("Where the work happens.",
      "Development suites, production and warehousing across three countries."),
     ["production-facilities-germany", "technical-development-suite-germany",
      "technical-development-suite-uk", "sales-office-poland"]),
    ("Find us",
     ("Addresses and routes.",
      "Four locations in Germany, the United Kingdom and Poland."),
     ["find-us", "find-us/katech-head-office-germany", "find-us/katech-production-germany",
      "find-us/katech-uk", "find-us/katech-poland"]),
]

# --- Seiten ohne Bereichsabschnitt ----------------------------------------
LEGAL = ["imprint", "privacy-policy", "terms-of-use", "cookie-policy-eu",
         "data-protection-information-for-applicants"]

# Seiten, die im Bestandsbaum liegen, aber in keinen Abschnitt gehoeren.
# Sie bleiben erreichbar und stehen in der Sitemap.
SONSTIGE = {
    "venture-point": "facilities",       # UK-Standortbeschreibung
    "stephankoruma-cabinet": "facilities",  # Geraetebeschreibung der Pilotanlage
    "nasz-cel": "company",               # polnische Restseite im englischen Baum
    "sitemap": "",                       # eigene Seite ohne Bereich
    "products": "expertise",
}

# Bereichsseiten und ihre Startseiten
BEREICHS_START = {
    "solutions": "solutions",
    "expertise": "expertise",
    "company": "company",
    "facilities": "our-facilities",
    "news": "news",
}


def zuordnung(produktbereiche, baum, news_slugs, team_slugs):
    """Baut die vollstaendige Tabelle Seite -> Bereich.

    Rueckgabe: {slug: bereich_id}. Genau diese Tabelle bestimmt Menuemarkierung,
    Breadcrumb-Wurzel, Hub-Zugehoerigkeit und Sitemap-Einordnung.
    """
    zu = {}

    # Solutions: alle Produktbereiche samt Unterseiten
    for _, _, _, bereiche in SOLUTIONS:
        for b in bereiche:
            zu[b] = "solutions"
            for u in baum.get(b, []):
                zu[u] = "solutions"
    for eltern, kinder in FREMDE_KINDER.items():
        for k in kinder:
            zu[k] = "solutions"
    # der aufgeloeste Bereich selbst bleibt erreichbar
    zu["soups"] = "solutions"
    for b in produktbereiche:
        zu.setdefault(b, "solutions")
        for u in baum.get(b, []):
            zu.setdefault(u, "solutions")
    for u in baum.get("bakery-old", []):
        zu[u] = "solutions"
    zu["bakery-old"] = "solutions"

    for abschnitte, bereich in ((EXPERTISE, "expertise"), (COMPANY, "company"),
                                (FACILITIES, "facilities")):
        for _, _, seiten in abschnitte:
            for s in seiten:
                zu[s] = bereich

    # Team: Uebersicht und Einzelprofile gehoeren zu Company
    zu["our-people"] = "company"
    for s in team_slugs:
        zu[s] = "company"
    for s in ("our-people/sales-team", "our-people/development-team"):
        zu[s] = "company"

    for s in news_slugs:
        zu[s] = "news"
    zu["news"] = "news"

    for s, b in SONSTIGE.items():
        zu[s] = b
    for s in LEGAL:
        zu[s] = ""          # Rechtstexte tragen keinen Bereich
    zu["contact-us"] = ""   # Kontakt ist der Handlungsaufruf, kein Bereich

    for b, start in BEREICHS_START.items():
        zu[start] = b
    return zu


# --------------------------------------------------------------------------
# Umgehaengte Seiten: welcher Produktbereich fuehrt sie im Breadcrumb.
# Ohne diese Umkehr zeigt der Pfad auf den Ordner der Adresse statt auf die
# Kategorie, unter der die Seite tatsaechlich haengt - bei
# soups/freshpasteurised stand deshalb "Start / Solutions / Soups /" statt
# "Soups and sauces" (Suat 27.08.).
# --------------------------------------------------------------------------
ELTERN = {kind: eltern for eltern, kinder in FREMDE_KINDER.items() for kind in kinder}
# Der aufgeloeste Ein-Seiten-Bereich selbst haengt ebenfalls dort.
ELTERN["soups"] = "soups-and-sauces"


def eltern_von(slug, vorgabe):
    """Der Produktbereich, unter dem eine Seite im Breadcrumb steht."""
    return ELTERN.get(slug, vorgabe)
