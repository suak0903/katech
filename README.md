# KaTech Ingredient Solutions - Design-Vorschau

Unverbindlicher Redesign-Entwurf für die Website von **KaTech Ingredient Solutions GmbH**
(Lübeck, Tochtergesellschaft von Ingredion Incorporated).

**Live:** https://suak0903.github.io/katech/
**Über den Entwurf:** https://suak0903.github.io/katech/about-this-preview/
**Originalseite:** https://katech-solutions.com/

---

## Was das ist

Dies ist **nicht** der offizielle Auftritt von KaTech und steht in keiner Verbindung dazu.
Es ist ein eigenständig erstellter Gestaltungsvorschlag von **Dr.-Ing. Suat Akyol**.
Sämtliche Texte und Bilder stammen aus der öffentlich zugänglichen Bestandsseite und
bleiben Eigentum ihrer Rechteinhaber. Die Seite ist für Suchmaschinen gesperrt
(`noindex, nofollow` plus `robots.txt`) und lässt sich auf Wunsch jederzeit abschalten.

Anmerkungen und Einwände: **contact@akyol.de**

## Aufbau

Statisches HTML ohne Framework, ohne Build-Schritt im Browser, ohne Datenbank.

| Verzeichnis | Inhalt |
|---|---|
| `index.html`, `<bereich>/` | 200 fertige Seiten; die Pfade entsprechen denen der Bestandsseite |
| `css/site.css` | Design-System, beginnt mit Schriften und Farbtoken |
| `js/site.js` | Navigation, Parallaxe, Lightbox, Consent, Formular |
| `font/` | Barlow und Open Sans, selbst gehostet (OFL) |
| `media/` | Bilder aus dem Bestand, aufbereitet als WebP mit JPG-Rückfall |
| `_src/` | Generator und Datenbasis (nicht Teil der ausgelieferten Seite) |

## Neu bauen

Die Seiten werden erzeugt, nicht von Hand gepflegt. Kopfleiste, mobiles Menü und Fußzeile
stammen aus einer einzigen Quelle (`_src/gen_chrome.py`) und sind dadurch auf allen Seiten
identisch.

```bash
cd _src
python gen.py        # erzeugt alle Seiten
python sitemap.py    # schreibt sitemap.xml
python check.py      # prüft tote Verweise, Chrome-Gleichheit, Typografie, noindex
node qa.mjs          # klickt alle Bedienelemente durch (benötigt lokalen Server)
```

Vor dem Ausliefern die Zahl in `_src/gen_lib.py` (`VERSION`) erhöhen, damit Browser die
geänderten Dateien laden.

## Herkunft der Gestaltung

Farb- und Layoutsystem folgen dem Ingredion-Konzerndesign; das KaTech-Logo trägt dessen
Farbwerte bereits. Die Analyse dazu liegt beim Ersteller.
