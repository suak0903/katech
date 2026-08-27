/**
 * Maschinelle Funktionspruefung des Demonstrators.
 * Klickt jede interaktive Komponente einmal durch und meldet Konsolenfehler.
 * Aufruf: npx playwright test gibt es hier nicht, daher direkt:
 *   node qa.mjs   (benoetigt eine laufende Instanz auf http://localhost:8777)
 */
import { chromium, devices } from 'playwright';

const BASIS = 'http://localhost:8777';
const befunde = [];
const notiz = (bereich, text) => { befunde.push(`${bereich}: ${text}`); };

const browser = await chromium.launch();

// ---------------------------------------------------------------- Desktop
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const konsole = [];
  page.on('console', m => { if (m.type() === 'error') konsole.push(m.text()); });
  page.on('pageerror', e => konsole.push('pageerror: ' + e.message));

  await page.goto(BASIS + '/', { waitUntil: 'networkidle' });

  // Consent-Banner sichtbar, Demo-Leiste tritt zurueck
  const consentSichtbar = await page.locator('#consent').isVisible();
  if (!consentSichtbar) notiz('Consent', 'Banner erscheint beim ersten Besuch nicht');
  const demobarVerdeckt = await page.locator('#demobar').evaluate(
    el => getComputedStyle(el).visibility);
  if (demobarVerdeckt !== 'hidden') notiz('Consent', 'Demo-Leiste tritt nicht zurueck');

  await page.locator('#consent button[data-consent="nein"]').click();
  if (await page.locator('#consent').isVisible()) notiz('Consent', 'Banner schliesst nicht');
  await page.waitForTimeout(200);
  if (await page.locator('#demobar').evaluate(el => getComputedStyle(el).visibility) === 'hidden')
    notiz('Consent', 'Demo-Leiste kehrt nach der Wahl nicht zurueck');

  // Demo-Leiste schliessbar
  await page.locator('#demoClose').click();
  if (await page.locator('#demobar').isVisible()) notiz('Demo-Leiste', 'schliesst nicht');

  // Kopfleiste wird beim Scrollen solide
  await page.evaluate(() => window.scrollTo(0, 400));
  await page.waitForTimeout(350);
  if (!(await page.locator('.nav').evaluate(el => el.classList.contains('scrolled'))))
    notiz('Kopfleiste', 'scrolled-Zustand greift nicht');
  const logoDunkel = await page.locator('.logo-dark').isVisible();
  if (!logoDunkel) notiz('Kopfleiste', 'dunkles Logo erscheint im gescrollten Zustand nicht');

  // Parallaxe bewegt den Hintergrund
  const t = await page.locator('#heroBg').evaluate(el => el.style.transform);
  if (!t || t === 'none') notiz('Hero', 'Parallaxe setzt keine Transformation');

  // Reveal-Elemente sind sichtbar geworden. Das Einblenden laeuft ueber einen
  // Beobachter und braucht einen Moment; ohne Abwarten misst man zu frueh.
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForFunction(() => document.querySelectorAll('.rv:not(.in)').length === 0,
                             null, { timeout: 6000 }).catch(() => {});
  const unsichtbar = await page.locator('.rv:not(.in)').count();
  if (unsichtbar > 0) notiz('Reveal', `${unsichtbar} Elemente bleiben unsichtbar`);

  // Galerie und Lightbox
  await page.goto(BASIS + '/our-facilities/', { waitUntil: 'networkidle' });
  await page.locator('.gallery button').first().click();
  if (!(await page.locator('#lb').isVisible())) notiz('Lightbox', 'oeffnet nicht');
  const ersterZaehler = await page.locator('.lb__count').textContent();
  await page.locator('.lb__next').click();
  const zweiterZaehler = await page.locator('.lb__count').textContent();
  if (ersterZaehler === zweiterZaehler) notiz('Lightbox', 'Weiterblaettern aendert den Zaehler nicht');
  await page.keyboard.press('Escape');
  if (await page.locator('#lb').isVisible()) notiz('Lightbox', 'schliesst nicht mit Escape');

  // Formular-Attrappe
  await page.goto(BASIS + '/contact-us/', { waitUntil: 'networkidle' });
  await page.locator('#f-name').fill('Test');
  await page.locator('#f-company').fill('Testfirma');
  await page.locator('#f-mail').fill('test@example.com');
  await page.locator('#f-msg').fill('Testanfrage');
  await page.locator('input[name="privacy"]').check();
  await page.locator('#enquiry button[type="submit"]').click();
  await page.waitForTimeout(400);
  if (!(await page.locator('#formNote').isVisible()))
    notiz('Formular', 'Hinweis nach dem Absenden erscheint nicht');

  // Consent-gated Karte
  const iframeSrc = await page.locator('.mapwrap iframe').getAttribute('src');
  if (iframeSrc) notiz('Karte', 'iframe laedt vor der Einwilligung');
  await page.locator('[data-map-load]').first().click();
  await page.waitForTimeout(400);
  const iframeSrc2 = await page.locator('.mapwrap iframe').getAttribute('src');
  if (!iframeSrc2) notiz('Karte', 'iframe laedt nach der Einwilligung nicht');

  // Cookie-Einstellungen im Fuss
  await page.locator('[data-consent-revoke]').click();
  await page.waitForTimeout(300);
  if (!(await page.locator('#consent').isVisible()))
    notiz('Consent', 'Widerruf ueber den Fusszeilen-Link zeigt das Banner nicht erneut');

  // Sprachumschalter meldet sich
  page.once('dialog', d => d.dismiss());
  await page.locator('.lang button[data-lang="de"]').click();

  // Parallaxe der Unterseiten-Heroes
  for (const pfad of ['/vegan/', '/our-facilities/', '/news/']) {
    await page.goto(BASIS + pfad, { waitUntil: 'networkidle' });
    const start = await page.locator('#subheroBg').evaluate(el => el.style.transform);
    await page.evaluate(() => window.scrollBy(0, 500));
    await page.waitForTimeout(300);
    const nach = await page.locator('#subheroBg').evaluate(el => el.style.transform);
    if (!nach || nach === 'none' || nach === start) notiz('Parallaxe', `fehlt auf ${pfad}`);
  }

  // Noch nicht ausgebaute Seiten sind sichtbar gekennzeichnet
  await page.goto(BASIS + '/customer-area/', { waitUntil: 'networkidle' });
  if (!(await page.locator('.stubtag').isVisible()))
    notiz('Platzhalterseite', 'Marke im Seitenkopf fehlt');
  if (!(await page.locator('.stub').isVisible()))
    notiz('Platzhalterseite', 'Hinweiskasten fehlt');

  // 404
  const antwort = await page.goto(BASIS + '/404.html', { waitUntil: 'networkidle' });
  if (!antwort.ok()) notiz('404', 'Fehlerseite nicht erreichbar');

  if (konsole.length) notiz('Konsole (Desktop)', konsole.slice(0, 5).join(' | '));
  await ctx.close();
}

// ----------------------------------------------------------------- Mobil
{
  const ctx = await browser.newContext({ ...devices['iPhone 12'] });
  const page = await ctx.newPage();
  const konsole = [];
  page.on('console', m => { if (m.type() === 'error') konsole.push(m.text()); });
  page.on('pageerror', e => konsole.push('pageerror: ' + e.message));

  await page.goto(BASIS + '/', { waitUntil: 'networkidle' });
  await page.locator('#consent button[data-consent="nein"]').click();

  // Menue oeffnen. Es darf genau ein Logo sichtbar sein, und es muss an
  // seinem Platz bleiben, auch wenn im offenen Menue gescrollt wird.
  const vorher = await page.locator('.brand img.logo-light').boundingBox();
  await page.locator('#burger').click();
  await page.waitForTimeout(600);
  if (!(await page.locator('#mmenu').isVisible())) notiz('Mobiles Menue', 'oeffnet nicht');

  const logosOffen = await page.locator('.nav img:visible, .mmenu img:visible').count();
  if (logosOffen !== 1) notiz('Mobiles Menue', `${logosOffen} sichtbare Logos im Kopfbereich statt genau einem`);

  await page.evaluate(() => window.scrollBy(0, 400));
  await page.locator('#mmenu').evaluate(el => el.scrollBy(0, 300));
  await page.waitForTimeout(400);
  const logosGescrollt = await page.locator('.nav img:visible, .mmenu img:visible').count();
  if (logosGescrollt !== 1) notiz('Mobiles Menue', `nach dem Scrollen ${logosGescrollt} sichtbare Logos statt genau einem`);
  const nachher = await page.locator('.brand img.logo-light').boundingBox();
  if (vorher && nachher) {
    const dx = Math.abs(vorher.x - nachher.x);
    const dy = Math.abs(vorher.y - nachher.y);
    if (dx > 1 || dy > 1)
      notiz('Mobiles Menue', `Logo wandert beim Scrollen (dx ${dx.toFixed(1)}, dy ${dy.toFixed(1)})`);
  } else {
    notiz('Mobiles Menue', 'Logo-Position nicht messbar');
  }

  // Escape schliesst
  await page.keyboard.press('Escape');
  await page.waitForTimeout(600);
  if (await page.locator('#mmenu').evaluate(el => el.classList.contains('open')))
    notiz('Mobiles Menue', 'schliesst nicht mit Escape');

  // Linkklick schliesst und navigiert
  await page.locator('#burger').click();
  await page.waitForTimeout(500);
  await page.locator('#mmenu a[href$="solutions/"]').first().click();
  await page.waitForLoadState('networkidle');
  if (!page.url().includes('/solutions/')) notiz('Mobiles Menue', 'Navigation ueber das Menue schlaegt fehl');

  if (konsole.length) notiz('Konsole (Mobil)', konsole.slice(0, 5).join(' | '));
  await ctx.close();
}

await browser.close();

if (befunde.length === 0) {
  console.log('QA: alle Pruefungen bestanden.');
} else {
  console.log(`QA: ${befunde.length} Befund(e)`);
  befunde.forEach(b => console.log('  - ' + b));
}
