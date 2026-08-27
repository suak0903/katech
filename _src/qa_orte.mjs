/**
 * Prueft den Weg zu den Standorten:
 *   Facilities zeigt vier Orte und einen Weg zur Adressuebersicht,
 *   Find us fuehrt zu jedem Ort weiter,
 *   jede Standortseite traegt Beschreibung, Adresse und Karte,
 *   die alten Adressen des Bestands leiten dorthin weiter.
 */
import { chromium } from 'playwright';

const BASIS = 'http://localhost:8777';
let fehler = 0;
const pruefe = (b, was) => {
  console.log((b ? '  ok    ' : '  FEHLER') + '  ' + was);
  if (!b) fehler++;
};

const ORTE = [
  ['technical-development-suite-germany', 'Lübeck', 'find-us/katech-head-office-germany'],
  ['production-facilities-germany', 'Wesenberg', 'find-us/katech-production-germany'],
  ['technical-development-suite-uk', 'Ellesmere Port', 'find-us/katech-uk'],
  ['sales-office-poland', 'Stęszew', 'find-us/katech-poland'],
];

const browser = await chromium.launch();
const seite = await browser.newPage({ viewport: { width: 1440, height: 900 } });

// --- Facilities ----------------------------------------------------------
await seite.goto(BASIS + '/our-facilities/');
const ziele = await seite.$$eval('main a[href]', a =>
  a.map(x => x.getAttribute('href')).filter(h => h && !h.startsWith('#')));
const adressseiten = ziele.filter(z => /find-us\/katech-/.test(z));
pruefe(adressseiten.length === 0,
       `keine reinen Adressseiten mehr verlinkt (${adressseiten.length})`);
for (const [slug] of ORTE) {
  pruefe(ziele.some(z => z.includes(slug + '/')), `fuehrt zu ${slug}`);
}
pruefe(ziele.some(z => /find-us\/$/.test(z)), 'fuehrt zur Adressuebersicht');

// --- Find us -------------------------------------------------------------
await seite.goto(BASIS + '/find-us/');
const karten = seite.locator('.loc--karte');
pruefe(await karten.count() === 4, `vier Adresskarten (${await karten.count()})`);
for (let i = 0; i < 4; i++) {
  const verweise = await karten.nth(i).evaluate(el =>
    [...el.querySelectorAll('a[href]')].map(x => x.getAttribute('href'))
      .filter(h => !h.startsWith('tel:') && !h.startsWith('mailto:')));
  const trifft = verweise.some(v => ORTE.some(([slug]) => v.includes(slug + '/')));
  pruefe(trifft, `Adresskarte ${i + 1} fuehrt zur Standortseite`);
}

// --- Standortseiten ------------------------------------------------------
for (const [slug, ort] of ORTE) {
  // Die Einwilligung wird im Browser gemerkt. Ohne Leeren waere die Karte
  // auf der zweiten Seite schon geladen und der Knopf gar nicht mehr da.
  await seite.goto(BASIS + '/' + slug + '/');
  await seite.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
  await seite.reload();
  const text = await seite.locator('main').innerText();
  pruefe(text.length > 400, `${slug}: Beschreibung steht (${text.length} Zeichen)`);
  const adresse = seite.locator('#address address');
  pruefe(await adresse.count() === 1, `${slug}: Adressblock vorhanden`);
  pruefe((await adresse.innerText()).includes(ort), `${slug}: nennt ${ort}`);
  pruefe(await seite.locator('#address .mapwrap iframe').count() === 1,
         `${slug}: Karte vorhanden`);
  // Karte laedt erst nach Zustimmung. Der Bereich blendet sich beim
  // Scrollen ein, deshalb erst hinfahren und den Einblendvorgang abwarten.
  await seite.locator('#address').scrollIntoViewIfNeeded();
  await seite.waitForTimeout(900);
  const vorher = await seite.locator('#address iframe').getAttribute('src');
  pruefe(!vorher, `${slug}: Karte laedt nicht ungefragt`);
  await seite.locator('#address [data-map-load]').click({ timeout: 10000 });
  await seite.waitForTimeout(500);
  const nachher = await seite.locator('#address iframe').getAttribute('src');
  pruefe(!!nachher && nachher.includes('google'), `${slug}: Karte laedt auf Knopfdruck`);
  pruefe(!(await seite.locator('#address .mapph').isVisible()),
         `${slug}: Platzhalter verschwindet dabei`);
}

// --- Alte Adressen -------------------------------------------------------
for (const [slug, , alt] of ORTE) {
  await seite.goto(BASIS + '/' + alt + '/');
  await seite.waitForTimeout(700);
  const wo = seite.url();
  pruefe(wo.includes(slug + '/'), `${alt} landet auf ${slug} (${wo.replace(BASIS, '')})`);
}

await browser.close();
console.log(fehler === 0 ? '\nStandorte: alle Pruefungen bestanden.' : `\nStandorte: ${fehler} Befunde.`);
process.exit(fehler === 0 ? 0 : 1);
