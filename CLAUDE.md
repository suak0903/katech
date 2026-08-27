# CLAUDE - KaTech-Demonstrator

Redesign-Vorschau für **KaTech Ingredient Solutions GmbH** (Lübeck, Ingredion-Tochter).
Akquise-Demonstrator, kein Kundenauftrag. Auftrag und Hintergrund liegen im Vault unter
`projects/KaTech/` ([[Demonstrator-Auftrag]], [[CD-Analyse]], [[Demo-Drehbuch]]).

**Live:** https://suak0903.github.io/katech/ · **Original:** https://katech-solutions.com/
**Demo-Termin:** Fr 04.09.2026, 13:00, Teams, mit Group Managing Director Cyril Carrat.

---

## 1. Abweichung vom Kit, die man kennen muss

Das Web-Starter-Kit sieht handgeschriebene HTML-Dateien vor, in die `build-site.mjs` das Chrome
über Marker einsetzt. **Hier werden alle Seiten erzeugt.** Bei 200 Seiten, davon über hundert
Produktseiten mit je eigenem Text und Bild aus dem Bestand, ist Handarbeit nicht sinnvoll.

Der Zweck der Kit-Regel bleibt erfüllt, sogar strenger: Kopfleiste, mobiles Menü, Fußzeile,
Demo-Leiste und Consent-Banner stehen **ausschließlich** in `_src/gen_chrome.py`. Es gibt keinen
Chrome-Textblock, den man versehentlich kopieren könnte. `_src/check.py` misst das nach und meldet
die Zahl der Kopf- und Fußvarianten über alle Seiten; **Sollwert ist jeweils 1**.

Das Ergebnis ist statisches HTML wie überall sonst: kein Framework, kein Laufzeit-Include, keine
Datenbank. Der Generator läuft vor dem Ausliefern, nicht im Browser des Besuchers.

## 2. Aufbau

```
index.html, <bereich>/, <bereich>/<produkt>/   200 erzeugte Seiten, Pfade wie im Original
css/site.css      Design-System (Schriften, Token, Komponenten)
js/site.js        Nav, Menü, Parallaxe, Reveal, Lightbox, Consent, Formular
font/             Barlow + Open Sans, self-hosted (OFL)
media/            aufbereitete Bestandsbilder, WebP + JPG
_src/             Generator, Datenbasis, Prüfwerkzeuge (nicht Teil der Auslieferung)
```

### Generator

| Datei | Aufgabe |
|---|---|
| `gen.py` | Hauptlauf: Startseite, Hubs, Bereiche, Produktseiten, Textseiten |
| `gen_chrome.py` | **Einzige Quelle** für Kopf, Menü, Fuß, Demo-Leiste, Consent |
| `gen_lib.py` | Seitenrahmen, Kopfdaten, JSON-LD, Sektionsbausteine, `VERSION` |
| `inhalt.py` | Redaktionelle Daten, Sonderseiten (News, Team, Kontakt, Hinweisseite) |
| `check.py` | Tote Verweise, Chrome-Gleichheit, Typografie, noindex, H1, alt-Texte |
| `qa.mjs` | Klickt alle Bedienelemente durch (Playwright, braucht lokalen Server) |
| `mobil.html` | iframe-Messharness für Mobilbreiten (320 bis 1440) |
| `sitemap.py` | Schreibt `sitemap.xml` |

### Ablauf bei jeder Änderung

```bash
cd _src
# VERSION in gen_lib.py erhöhen, wenn css oder js geändert wurden
python gen.py && python sitemap.py && python check.py
# im Projektwurzelverzeichnis: python -m http.server 8777
node qa.mjs
git add -A && git commit && git push
```

## 3. Datenherkunft

Alle Inhalte stammen aus der Bestandsseite, erhoben am 26.08.2026:

| Datei in `_src/` | Inhalt |
|---|---|
| `data.json` | 160 englische Seiten mit Titel, Absätzen, Listen, Hauptbild |
| `content.json` | Rohextrakt je Seite (Blöcke mit Tag) |
| `news-clean.json` | 17 echte Pressemeldungen |
| `team.json` | 23 Personenprofile mit Rolle, Team, Standort |
| `media-map.json` | Zuordnung Seite zu aufbereitetem Bild |

Die Roh-HTML-Dateien (`raw/`, `raw-news/`) und die Originalbilder (`assets/`) liegen lokal,
sind aber nicht versioniert. Zum Wiederherstellen: `crawl.py`, `extract.py`, `news.py`,
`team.py`, `download_media.py`, `prepare_media.py`, `upscale_food.py`, `fonts.py` in dieser
Reihenfolge.

## 4. Gestaltung

Farbwerte und Layoutmuster kommen aus dem Ingredion-Konzerndesign. **Der tragende Befund:** das
KaTech-Logo führt bereits exakt die Ingredion-Token (`#6cb33e`, `#ffe115`, `#373738`), während
das Bestands-Stylesheet von 2013 noch die alten Werte trägt. Die Website hinkt ihrem eigenen
Logo hinterher. Vollständige Analyse: [[CD-Analyse]] im Vault.

Eigenständigkeit entsteht nicht über abweichende Farben, sondern über deren **Gewichtung**:
Ingredion führt mit Blau, hier führen Grün und Teal, und das Gelb, das der Konzern kaum nutzt,
ist das KaTech-Erkennungszeichen.

**Schriften:** Barlow für Überschriften (freier Ersatz für das lizenzpflichtige Milo Pro des
Konzerns), Open Sans für Fließtext (dieselbe Familie wie beim Konzern). Beide self-hosted.

**Signaturmuster:** der Split-Block aus Farbfläche und Foto, direkt aus dem Ingredion-Layout
übernommen. Rechte Winkel überall, keine Schatten, Trennung über Flächenwechsel und Haarlinien.

## 5. Entschieden und nicht mehr diskutieren

- **Original-URL-Pfade bleiben.** `/cheese/cream-cheese/` heißt hier genauso. Das ist das
  stärkste Migrationsargument und darf nicht der Bequemlichkeit geopfert werden.
- **Englisch einsprachig.** Der Sprachumschalter ist ein Stub mit Hinweis. DE und PL sind im
  echten Projekt der größte Posten und werden hier bewusst nicht angetäuscht.
- **Kein Backend.** Das Anfrageformular zeigt nach dem Absenden einen Hinweis. Kein Shop, kein
  Chat, kein Login, weil das Original all das auch nicht hat.
- **Team-Rollen kommen aus dem Bestand**, auch wenn sie veraltet sind. Carrats Profil zeigt
  „Technical Director" (Stand 2017). Das ist **Absicht**: es ist die vorbereitete Live-Änderung
  der Demo (siehe [[Demo-Drehbuch]]). Vor dem Termin muss `ROLLEN_OVERRIDE` in `inhalt.py` leer
  sein, sonst ist die Pointe verbraucht.
- **Bestandstexte werden übernommen, aber typografisch normalisiert** (`gen_lib.normalisieren`):
  keine Gedankenstriche, keine typografischen Anführungszeichen. Gilt auch für JSON-LD.
- **Kachel- und Einstiegstexte der Produktbereiche sind neu geschrieben** (`BEREICHS_KURZTEXT`).
  Der Bestandstext ist dort Lexikonprosa („cheese is a nutritious food made mostly from the milk
  of cows") und taugt nicht als Einstieg.

## 5a. Das Karussell der Bestandsseite und das Video

Die Startseite des Originals fuehrt einen **RoyalSlider mit sieben Folien**
(Ueberschrift, ein bis zwei Saetze, Bild 385x248). Ein Karussell zeigt eine
Aussage und versteckt sechs. Hier laufen dieselben sieben Aussagen als
**Highlights-Band** ueber der Nachrichtenliste: alle gleichzeitig sichtbar,
per Maus oder Finger schiebbar, Klick oeffnet den vollen Text in einer
Lightbox. Wortlaut und Motive stammen aus dem Bestand (`HIGHLIGHTS` in
`inhalt.py`, Bildaufbereitung `highlights.py`).

**Das Video der Bestandsseite fehlt bewusst.** Die Folie "New product
development support" traegt ein Standbild mit Abspielsymbol; ein Skript
(`eclipse-custom.js`) oeffnet dahinter eine von zwei Vimeo-Nummern,
**509794560** und **512503894**. Beide sind von aussen nicht abspielbar:
`player.vimeo.com/video/<nr>` antwortet mit 404, auch mit dem Referer der
Originaldomain; die Vimeo-Seiten selbst antworten mit 200, geben aber keinen
Titel preis. Das Muster passt zu privat gestellten oder domainbeschraenkten
Videos. **Ohne Freigabe durch KaTech laesst sich das Video nicht einbinden.**
Fuer die Demo ist das ein Gespraechsanlass: das einzige Bewegtbild der Firma
ist auf ihrer eigenen Startseite moeglicherweise tot.

**Kein content-visibility auf den Sektionen.** Es bringt messbar Ladezeit
(Blockierzeit von rund 300 auf 120 Millisekunden), aber die geschaetzten
Hoehen werden beim Rendern korrigiert und die Scrollposition wandert dabei um
bis zu 200 Pixel. Beim Vorfuehren waere das sichtbar. Dreimal geprueft und
verworfen am 26.08.

## 5b. Bedienung des Highlights-Bandes

Vier Fallen, die alle erst am echten Geraet auffielen:

- **Ueber Bildern startet der Browser sein eigenes Ziehen.** Ohne
  `draggable="false"`, `user-drag:none` und `preventDefault()` im
  `pointerdown` liess sich das Band nur ueber dem Textbereich schieben.
- **Auf Beruehrung braucht es `touch-action:pan-y`.** Sonst deutet der
  Browser die Geste als Scrollen und bricht den Zeiger nach wenigen
  Millimetern ab.
- **Der Stopp unter dem Zeiger wird auf Beruehrung nie aufgehoben**, weil es
  dort kein Verlassen gibt. Beim Loslassen muss `frei` wieder gesetzt werden,
  sonst steht das Band nach einem Tipp fuer immer.
- **Der Zugwert muss nach dem Loslassen zurueckgesetzt werden**, sonst
  blockiert ein frueherer Zug den naechsten Klick. Zuruecksetzen im
  `setTimeout(..., 0)`, damit das unmittelbar folgende Klickereignis den
  Wert noch sieht.

## 5c. Die Teamportraets

Die Bestandsseite zeigt **kein einziges Portraet im sichtbaren Inhalt**. Alle
23 Aufnahmen liegen aber auf dem Server: sie sind je Profilseite als
Vorschaubild fuer soziale Netzwerke im Kopf hinterlegt (`og:image`). Wer die
Seite besucht, sieht sie nie, wer den Link teilt, schon. Gesammelt in
`portraits.json`, aufbereitet mit `prepare_portraits.py`.

**Sie liegen nur als 140x140 vor**, die Originale sind nicht mehr abrufbar
(die Variante ohne Groessensuffix liefert 404). Hochskaliert auf 440x440.
Das Set ist einheitlich: Schwarzweiss, heller Hintergrund, gleiche Bildsprache
ueber alle Personen.

**Falle:** Drei Aufnahmen sind PNG mit Transparenz. Die weisse Unterlage muss
**vor** dem Hochskalieren gelegt werden, sonst brennt das Verfahren den
transparenten Bereich als Schwarz ein und die drei fallen in der Kachelreihe
sofort auf.

## 5d. Die Informationsarchitektur liegt in struktur.py

**Eine Quelle, aus der sich alles ableitet.** Vorher legten vier Stellen
unabhaengig voneinander fest, zu welchem Bereich eine Seite gehoert:
Hub-Kachel, Menuemarkierung, Breadcrumb und Generator-Liste. Sie sind
auseinandergedriftet (Suat 27.08.: Team unter Expertise verlinkt, aber Company
markiert; Facilities markiert, aber Company im Pfad).

Jetzt steht die Zuordnung in `struktur.py`. `gen.bereich_von()`,
`gen.aktiv_von()` und `gen.crumbs_von()` lesen daraus; Hubs und Sitemap
ebenfalls. **`check.py` prueft fuer jede Seite, ob markierter Menuepunkt und
Breadcrumb uebereinstimmen** - Sollwert null Abweichungen.

**Bereichsschnitt:**
- **Solutions** - die dreizehn Produktwelten und alles darunter.
- **Expertise** - was das Unternehmen kann, einschliesslich Case studies.
- **Company** - wer es ist, einschliesslich Our people und der 23 Profile.
- **Facilities** - eigener Bereich seit 27.08.; der Company-Abschnitt
  "Sites and production" ist vollstaendig dorthin gewandert, ebenso Find us
  mit den vier Standortseiten.
- **News** - Archiv und Einzelmeldungen.

**Plant-based** hat vier Gruppen: Meat alternatives und Fish alternatives mit
den vorhandenen Kopfseiten, Dairy alternatives und Savoury als reine
Gruppenueberschriften, weil es dafuer im Bestand keine Kopfseite gibt. Es wird
keine Seite erfunden.

**Die verwaiste Suppenkategorie** (`soups` mit genau einer Seite neben
`soups-and-sauces`) erscheint unter Soups and sauces. Die Adresse
`/soups/freshpasteurised/` bleibt unveraendert.

**Offen:** Ob Case studies bei Expertise bleibt oder unter Company wandert,
entscheidet Suat. Der Umzug ist eine Zeile in `struktur.py`.

## 5e. Seiten ohne Inhalt: drei Faelle, ehrlich benannt

Ermittelt mit `leerpruefung.py`, das den kompletten Inhaltsbereich auf Text,
Listen, Tabellen, Bilder, Downloads und eingebettete Inhalte prueft. Der erste
Extraktor hatte nur Fliesstext gezaehlt und deshalb Bilder uebersehen.

| Fall | Anzahl | Was auf der Seite steht |
|---|---|---|
| Im Original ohne jeden Inhalt | 21 | "This page has no content on the existing site." |
| Im Original nur ein Produktbild | 10 | Das Bild, plus ein Satz dazu. Kein Mangel-Hinweis. |
| Im Original vorhanden, hier nicht ausgebaut | wenige | "This page is not built out in this preview." |

**Jeder dieser Hinweise verlinkt die Originalseite**, damit die Aussage
nachpruefbar ist (Suat 27.08.). Der frueher einheitliche Text behauptete, die
Vorschau sei unfertig - bei 21 Seiten war das schlicht falsch.

**Nebenbefund:** `katech-solutions.com/purchasing/` traegt oeffentlich die
interne Notiz "Steve Williams needs to put something here". **Bewusst nicht
uebernommen**, weil sie einen Mitarbeiter namentlich vorfuehrt.

## 5f. Grafische Sitemap

`/sitemap/` zeigt die vollstaendige Hierarchie, jede Seite einzeln anklickbar,
Seiten ohne Inhalt gekennzeichnet. Sie speist sich aus `struktur.py` und kann
deshalb nicht von Menue und Breadcrumb abweichen. Verlinkt in der Demo-Leiste
neben "What is different?" und "Original site".

**Beschriftungen** stammen aus dem Adressbestandteil, nicht aus den
Bestandstiteln - dort stehen Werbesaetze wie "Greek yogurt - the food of the
gods", die als Navigationsbeschriftung nicht taugen. Deutsche Adressreste
(`pflanzliche-burger-patties`, `wurstchen-alternativen`) und
unverstaendliche Kuerzel bekommen in `inhalt.KURZTITEL` eine Beschriftung;
die Adressen bleiben unveraendert.

## 6. Stolperfallen aus diesem Projekt

- **Der Server drosselt.** Ab etwa 70 schnellen Abrufen liefert `katech-solutions.com` HTTP 503.
  Crawler brauchen mindestens eine Sekunde Pause und einen Wiederholversuch mit Backoff.
- **Bilder liegen teils auf `khpartner.com`**, der Domain der Vorgängergesellschaft. Beim
  Abholen beide Hosts berücksichtigen.
- **Die WordPress-REST-API liefert nur 199 der 743 Medien.** Verlässlicher ist es, alle Bild-URLs
  aus den gecachten HTML-Seiten zu ziehen (auch aus `style`-Attributen).
- **Team-Profile sind WordPress-Posts** wie die News und tauchen sonst fälschlich im
  Newsarchiv auf. Unterscheidungsmerkmal ist die Kategorie `our-people/...`.
- **Bestandsbilder sind klein** (432 bis 700 Pixel). Alles, was groß ausgespielt wird, läuft
  vorher durch Real-ESRGAN (`upscale_food.py`, `prepare_media.py`).
- **Die Demo-Leiste ist fixiert** und verdeckte anfangs den Fußbereich, wodurch Klicks ins Leere
  gingen. Deshalb `body{padding-bottom:56px}`, das beim Schließen der Leiste entfällt.
- **Consent-Banner und Demo-Leiste sitzen beide unten.** Solange das Banner offen ist, tritt die
  Demo-Leiste zurück (`visibility`), sonst überlagern sie sich.
- **`.foot a` überschreibt spätere Unterstreichungen.** Links im Hinweistext des Fußes brauchen
  `.foot .foot__demo a`, sonst heben sie sich nur über die Farbe ab (Barrierefreiheitsfehler).

## 7. Messwerte (lokal, 26.08.2026)

| Prüfung | Ergebnis |
|---|---|
| Seiten | 200, keine toten Verweise |
| Chrome | 1 Kopfvariante, 1 Fußvariante über alle Seiten |
| Mobilbreiten 320 bis 1440 | kein horizontaler Überlauf auf 20 geprüften Seiten |
| Bedienelemente | alle Prüfungen bestanden, keine Konsolenfehler |
| Lighthouse | Performance 94, Barrierefreiheit 96, Best Practices 100 |
| SEO-Wert | 69, ausschließlich wegen `noindex` - so gewollt |

Die Performance ist lokal gemessen, ohne Kompression. GitHub Pages liefert komprimiert, der
Live-Wert liegt darüber. **Nach dem Deploy live nachmessen** (Kit-Regel: erst messen, dann
bewerten).
