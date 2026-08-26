/**
 * Abnahme-Screenshots aller Kernseiten in Desktop- und Mobilbreite.
 * Die Einwilligung wird vorab gesetzt, damit das Banner die Ansicht nicht
 * verdeckt; die Demo-Leiste bleibt sichtbar, sie gehoert zum Auslieferungsstand.
 */
import { chromium, devices } from 'playwright';
import { mkdirSync } from 'fs';

const BASIS = 'http://localhost:8777';
const ZIEL = '_abnahme';
mkdirSync(ZIEL, { recursive: true });

const SEITEN = [
  ['start', '/'],
  ['solutions', '/solutions/'],
  ['vegan', '/vegan/'],
  ['produktseite', '/vegan/plant-based-mince/'],
  ['how-we-work', '/how-we-work/'],
  ['our-people', '/our-people/'],
  ['carrat', '/cyril-carrat/'],
  ['facilities', '/our-facilities/'],
  ['news', '/news/'],
  ['news-brc', '/katech-receives-highest-brc-food-aa-rating-for-food-safety/'],
  ['contact', '/contact-us/'],
  ['about-this-preview', '/about-this-preview/'],
];

const browser = await chromium.launch();

for (const [modus, opts] of [
  ['desktop', { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }],
  ['mobil', { ...devices['iPhone 12'] }],
]) {
  const ctx = await browser.newContext(opts);
  await ctx.addInitScript(() => {
    try { window.localStorage.setItem('katech-demo-consent', 'nein'); } catch (e) { /* egal */ }
  });
  const page = await ctx.newPage();
  for (const [name, pfad] of SEITEN) {
    await page.goto(BASIS + pfad, { waitUntil: 'networkidle' });
    // Reveal-Elemente einblenden, damit der Screenshot den Endzustand zeigt
    await page.evaluate(() => {
      document.querySelectorAll('.rv').forEach(el => el.classList.add('in'));
    });
    await page.waitForTimeout(500);
    await page.screenshot({ path: `${ZIEL}/${modus}-${name}.png`, fullPage: true });
    console.log(`  ${modus}/${name}`);
  }
  await ctx.close();
}

// Mobiles Menue geoeffnet, als Beleg der Deckungsgleichheit
{
  const ctx = await browser.newContext({ ...devices['iPhone 12'] });
  await ctx.addInitScript(() => {
    try { window.localStorage.setItem('katech-demo-consent', 'nein'); } catch (e) { /* egal */ }
  });
  const page = await ctx.newPage();
  await page.goto(BASIS + '/', { waitUntil: 'networkidle' });
  await page.screenshot({ path: `${ZIEL}/mobil-menue-zu.png` });
  await page.locator('#burger').click();
  await page.waitForTimeout(700);
  await page.screenshot({ path: `${ZIEL}/mobil-menue-offen.png` });
  console.log('  mobil/menue');
  await ctx.close();
}

await browser.close();
console.log('Screenshots in ' + ZIEL);
