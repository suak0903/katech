/**
 * Prueft die Reiter auf den Produktseiten: Umschalten mit der Maus, mit der
 * Tastatur, und dass ohne JavaScript alle drei Texte lesbar bleiben.
 */
import { chromium } from 'playwright';

const BASIS = 'http://localhost:8777';
const SEITE = '/yogurt/drinking-yogurt/';
let fehler = 0;

function pruefe(bedingung, was) {
  console.log((bedingung ? '  ok    ' : '  FEHLER') + '  ' + was);
  if (!bedingung) fehler++;
}

const browser = await chromium.launch();

// --- mit JavaScript ------------------------------------------------------
const seite = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await seite.goto(BASIS + SEITE);
await seite.waitForSelector('[data-tabs].bereit');

const knoepfe = seite.locator('.tabs__b');
const felder = seite.locator('.tabs__p');
pruefe(await knoepfe.count() === 3, 'drei Reiterknoepfe');
pruefe(await felder.count() === 3, 'drei Reiterfelder');
pruefe(await felder.nth(0).isVisible(), 'erstes Feld ist offen');
pruefe(!(await felder.nth(1).isVisible()), 'zweites Feld ist zu');
pruefe(await knoepfe.nth(0).getAttribute('aria-selected') === 'true', 'erster Knopf ist markiert');

// Ueberschriften im Reiterbetrieb nur fuer Vorleseprogramme
const hoehe = await seite.locator('.tabs__h').first().evaluate(el => el.getBoundingClientRect().height);
pruefe(hoehe <= 1, 'Feldueberschrift im Reiterbetrieb ausgeblendet');

await knoepfe.nth(1).click();
await seite.waitForTimeout(420);
pruefe(await felder.nth(1).isVisible(), 'Klick oeffnet das zweite Feld');
pruefe(!(await felder.nth(0).isVisible()), 'erstes Feld schliesst dabei');
pruefe(await knoepfe.nth(1).getAttribute('aria-selected') === 'true', 'zweiter Knopf markiert');
const text2 = await felder.nth(1).innerText();
pruefe(text2.length > 80, 'zweites Feld traegt Text (' + text2.length + ' Zeichen)');

await knoepfe.nth(1).focus();
await seite.keyboard.press('ArrowRight');
await seite.waitForTimeout(420);
pruefe(await felder.nth(2).isVisible(), 'Pfeil rechts schaltet weiter');
pruefe(await seite.evaluate(() => document.activeElement.id.startsWith('t-')),
       'Fokus liegt auf dem neuen Knopf');
await seite.keyboard.press('Home');
await seite.waitForTimeout(420);
pruefe(await felder.nth(0).isVisible(), 'Pos1 springt auf den ersten Reiter');

// kein waagerechter Ueberlauf durch die Reiterleiste
for (const breite of [320, 390, 768]) {
  await seite.setViewportSize({ width: breite, height: 800 });
  await seite.waitForTimeout(200);
  const ueber = await seite.evaluate(() =>
    document.documentElement.scrollWidth - document.documentElement.clientWidth);
  pruefe(ueber <= 1, `kein Ueberlauf bei ${breite} Pixel`);
}

// --- ohne JavaScript -----------------------------------------------------
const ohne = await browser.newContext({ javaScriptEnabled: false });
const seite2 = await ohne.newPage();
await seite2.goto(BASIS + SEITE);
const felder2 = seite2.locator('.tabs__p');
let alleSichtbar = true;
for (let i = 0; i < 3; i++) if (!(await felder2.nth(i).isVisible())) alleSichtbar = false;
pruefe(alleSichtbar, 'ohne Skript sind alle drei Felder lesbar');
pruefe(await seite2.locator('.tabs__h').first().isVisible(),
       'ohne Skript tragen die Felder ihre Ueberschrift');

await browser.close();
console.log(fehler === 0 ? '\nReiter: alle Pruefungen bestanden.' : `\nReiter: ${fehler} Befunde.`);
process.exit(fehler === 0 ? 0 : 1);
