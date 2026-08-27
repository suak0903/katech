/**
 * Prueft, dass jedes Bild etwas tut: Produktbilder und Portraets oeffnen die
 * Grossansicht, die Referenzbilder fuehren zur jeweiligen Seite, und die
 * Galerie funktioniert weiterhin.
 */
import { chromium } from 'playwright';

const BASIS = 'http://localhost:8777';
let fehler = 0;
const pruefe = (b, was) => {
  console.log((b ? '  ok    ' : '  FEHLER') + '  ' + was);
  if (!b) fehler++;
};

const browser = await chromium.launch();
const seite = await browser.newPage({ viewport: { width: 1440, height: 900 } });

// --- Produktbild ---------------------------------------------------------
await seite.goto(BASIS + '/yogurt/drinking-yogurt/');
const zoom = seite.locator('.prodbild .zoom');
pruefe(await zoom.count() === 1, 'Produktbild ist vergroesserbar');
await zoom.click();
await seite.waitForTimeout(400);
const lb = seite.locator('#lb');
pruefe(await lb.isVisible(), 'Grossansicht oeffnet');
const quelle = await lb.locator('img').getAttribute('src');
pruefe(!!quelle && quelle.includes('drinking-yogurt'), `zeigt das richtige Bild (${quelle})`);
pruefe(!(await lb.locator('.lb__prev').isVisible()), 'kein Blaettern bei einem Einzelbild');
await seite.keyboard.press('Escape');
await seite.waitForTimeout(300);
pruefe(!(await lb.isVisible()), 'Escape schliesst wieder');

// --- Portraet ------------------------------------------------------------
await seite.goto(BASIS + '/cyril-carrat/');
const portraet = seite.locator('.profil .zoom');
pruefe(await portraet.count() === 1, 'Portraet ist vergroesserbar');
await portraet.click();
await seite.waitForTimeout(400);
pruefe(await seite.locator('#lb').isVisible(), 'Grossansicht des Portraets oeffnet');
await seite.keyboard.press('Escape');

// --- Galerie unveraendert ------------------------------------------------
await seite.goto(BASIS + '/our-facilities/');
const galerieKnoepfe = seite.locator('.gallery button');
const anzahl = await galerieKnoepfe.count();
pruefe(anzahl >= 2, `Galerie hat ${anzahl} Bilder`);
await galerieKnoepfe.first().click();
await seite.waitForTimeout(400);
pruefe(await seite.locator('#lb').isVisible(), 'Galerie oeffnet die Grossansicht');
pruefe(await seite.locator('#lb .lb__next').isVisible(), 'Blaettern ist moeglich');
const zaehler = await seite.locator('#lb .lb__count').innerText();
pruefe(/\d+ \/ \d+/.test(zaehler), `Zaehler steht (${zaehler})`);
await seite.locator('#lb .lb__next').click();
await seite.waitForTimeout(300);
const zaehler2 = await seite.locator('#lb .lb__count').innerText();
pruefe(zaehler2 !== zaehler, `Weiterblaettern zaehlt hoch (${zaehler2})`);
await seite.keyboard.press('Escape');

// --- Referenzbilder ------------------------------------------------------
await seite.goto(BASIS + '/about-this-preview/');
const refs = seite.locator('.ref');
const refAnzahl = await refs.count();
pruefe(refAnzahl === 6, `sechs Referenzkarten (${refAnzahl})`);
let alleVerlinkt = true;
for (let i = 0; i < refAnzahl; i++) {
  const bildverweis = refs.nth(i).locator('a.ref__link');
  if (await bildverweis.count() !== 1) { alleVerlinkt = false; continue; }
  const ziel = await bildverweis.getAttribute('href');
  if (!ziel || !ziel.startsWith('http')) alleVerlinkt = false;
}
pruefe(alleVerlinkt, 'jedes Referenzbild fuehrt zur Seite');

// Reaktion auf das Ueberfahren
const vorher = await refs.first().locator('.ref__shot').evaluate(
  el => getComputedStyle(el).transform);
await refs.first().hover();
await seite.waitForTimeout(600);
const nachher = await refs.first().locator('.ref__shot').evaluate(
  el => getComputedStyle(el).transform);
pruefe(vorher !== nachher, 'Referenzbild reagiert auf das Ueberfahren');

// --- Kein Bild ohne Aufgabe ---------------------------------------------
await seite.goto(BASIS + '/yogurt/drinking-yogurt/');
const stumm = await seite.evaluate(() => {
  const raus = [];
  for (const img of document.images) {
    if (img.closest('a, button, .subhero__bg, .hero__bg, .foot__brand, .nav, .mmenu, #lb')) continue;
    raus.push(img.getAttribute('src'));
  }
  return raus;
});
pruefe(stumm.length === 0, `kein stummes Bild auf der Produktseite (${stumm.join(', ') || 'keins'})`);

await browser.close();
console.log(fehler === 0 ? '\nBilder: alle Pruefungen bestanden.' : `\nBilder: ${fehler} Befunde.`);
process.exit(fehler === 0 ? 0 : 1);
