/**
 * Pruefung der Bedienung des Highlights-Bandes und der Lightbox.
 * Geprueft wird ausdruecklich auch das Schieben ueber dem Bildbereich,
 * denn genau dort startete zuvor das Bild-Ziehen des Browsers.
 */
import { chromium, devices } from 'playwright';

const BASIS = 'http://localhost:8777';
const befunde = [];
const browser = await chromium.launch();

async function vorbereiten(ctx) {
  await ctx.addInitScript(() => {
    try { localStorage.setItem('katech-demo-consent', 'nein'); } catch (e) { /* egal */ }
  });
  const page = await ctx.newPage();
  await page.goto(BASIS + '/', { waitUntil: 'load' });
  await page.evaluate(() => document.querySelectorAll('.rv').forEach(e => e.classList.add('in')));
  await page.evaluate(() => document.querySelector('.hl').scrollIntoView({ block: 'center' }));
  // Das Blaettern laeuft weich; ohne Abwarten misst man an der falschen Stelle.
  await page.evaluate(() => new Promise(r => {
    let letzte = -1, gleich = 0;
    const t = setInterval(() => {
      if (window.scrollY === letzte) { if (++gleich > 3) { clearInterval(t); r(); } }
      else { gleich = 0; letzte = window.scrollY; }
    }, 100);
  }));
  await page.waitForTimeout(400);
  return page;
}

// -------------------------------------------------------------- Desktop
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await vorbereiten(ctx);

  // Schieben ueber Bild- und Textbereich. Die Punkte werden jeweils frisch
  // bestimmt, weil sich das Band zwischen den Versuchen weiterbewegt.
  // Fuer den zweiten Versuch eine mittlere Karte: die erste ist nach dem
  // ersten Zug halb aus dem sichtbaren Bereich gewandert.
  for (const [name, wahl] of [['bild', '.hl__card .hl__media'],
                              ['text', '.hl__card:nth-child(3) .hl__body']]) {
    const pt = await page.evaluate(w => {
      const r = document.querySelector(w).getBoundingClientRect();
      return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
    }, wahl);
    const vor = await page.locator('#hlTrack').evaluate(el => el.style.transform);
    await page.mouse.move(pt.x, pt.y);
    await page.waitForTimeout(250);
    await page.mouse.down();
    await page.mouse.move(pt.x - 200, pt.y, { steps: 16 });
    const waehrend = await page.locator('#hlTrack').evaluate(el => el.style.transform);
    await page.mouse.up();
    await page.waitForTimeout(150);
    const gezogen = Math.abs(parseFloat(waehrend.replace(/.*\(([-\d.]+)px.*/, '$1'))
      - parseFloat(vor.replace(/.*\(([-\d.]+)px.*/, '$1')));
    if (gezogen < 120) befunde.push(`Desktop: Schieben ueber dem ${name}bereich bewegt nur ${gezogen.toFixed(0)} statt 200 px`);
  }

  // Lightbox mit Blaettern
  await page.evaluate(() => document.querySelector('.hl__card[data-hl="0"]').click());
  await page.waitForTimeout(500);
  if (!(await page.locator('#hlBox').isVisible())) befunde.push('Desktop: Lightbox oeffnet nicht');
  const z1 = await page.locator('#hlCount').textContent();
  await page.locator('.hlbox__next').click();
  await page.waitForTimeout(350);
  const z2 = await page.locator('#hlCount').textContent();
  if (z1 === z2) befunde.push(`Desktop: Weiterblaettern aendert nichts (${z1})`);
  await page.locator('.hlbox__prev').click();
  await page.waitForTimeout(350);
  if ((await page.locator('#hlCount').textContent()) !== z1) befunde.push('Desktop: Zurueckblaettern landet woanders');
  // ueber den Rand hinaus blaettern
  await page.locator('.hlbox__prev').click();
  await page.waitForTimeout(350);
  const zEnde = await page.locator('#hlCount').textContent();
  if (!zEnde.startsWith('7')) befunde.push(`Desktop: Blaettern springt am Anfang nicht ans Ende (${zEnde})`);
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(300);
  if (!(await page.locator('#hlCount').textContent()).startsWith('1')) befunde.push('Desktop: Pfeiltaste blaettert nicht');
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  if (await page.locator('#hlBox').isVisible()) befunde.push('Desktop: Lightbox schliesst nicht');

  // Flaggen in der Kopfleiste
  const flaggen = await page.locator('.nav .lang button svg').count();
  if (flaggen !== 3) befunde.push(`Kopfleiste: ${flaggen} Flaggen statt drei`);
  await ctx.close();
}

// ---------------------------------------------------------------- Mobil
{
  const ctx = await browser.newContext({ ...devices['iPhone 12'], hasTouch: true });
  const page = await vorbereiten(ctx);

  const pt = await page.evaluate(() => {
    const m = document.querySelector('.hl__card .hl__media').getBoundingClientRect();
    return { x: m.left + m.width / 2, y: m.top + m.height / 2 };
  });

  // Wischen ueber dem Bild muss das Band bewegen
  const vor = await page.locator('#hlTrack').evaluate(el => el.style.transform);
  await page.touchscreen.tap(pt.x, pt.y);
  await page.waitForTimeout(200);
  await page.evaluate(async (p) => {
    const rail = document.getElementById('hlRail');
    const senden = (typ, x) => rail.dispatchEvent(new PointerEvent(typ, {
      pointerId: 1, pointerType: 'touch', clientX: x, clientY: p.y, bubbles: true, cancelable: true,
    }));
    senden('pointerdown', p.x);
    for (let i = 1; i <= 12; i++) { senden('pointermove', p.x - i * 18); await new Promise(r => setTimeout(r, 16)); }
    senden('pointerup', p.x - 216);
  }, pt);
  await page.waitForTimeout(200);
  const nach = await page.locator('#hlTrack').evaluate(el => el.style.transform);
  const weg = Math.abs(parseFloat(nach.replace(/.*\(([-\d.]+)px.*/, '$1'))
    - parseFloat(vor.replace(/.*\(([-\d.]+)px.*/, '$1')));
  if (weg < 120) befunde.push(`Mobil: Wischen bewegt nur ${weg.toFixed(0)} statt rund 216 px`);

  // Nach dem Loslassen muss das Band von allein weiterlaufen
  const a = await page.locator('#hlTrack').evaluate(el => el.style.transform);
  await page.waitForTimeout(900);
  const b2 = await page.locator('#hlTrack').evaluate(el => el.style.transform);
  if (a === b2) befunde.push('Mobil: Band laeuft nach dem Loslassen nicht weiter');

  // Lightbox: Knoepfe vorhanden und sichtbar
  await page.evaluate(() => document.querySelector('.hl__card[data-hl="2"]').click());
  await page.waitForTimeout(600);
  for (const [name, wahl] of [['Schliessen', '.hlbox__close'], ['Zurueck', '.hlbox__prev'], ['Vor', '.hlbox__next'], ['Zaehler', '#hlCount']]) {
    if (!(await page.locator(wahl).isVisible())) befunde.push(`Mobil: ${name} in der Lightbox nicht sichtbar`);
  }
  // Kontrast des Schliessen-Knopfes
  const stil = await page.locator('.hlbox__close').evaluate(el => {
    const c = getComputedStyle(el);
    return { hg: c.backgroundColor, rand: c.borderTopColor, farbe: c.color };
  });
  if (stil.hg === 'rgba(0, 0, 0, 0)') befunde.push('Mobil: Schliessen-Knopf ohne eigene Flaeche');
  await ctx.close();
}

await browser.close();
if (befunde.length === 0) console.log('Band und Lightbox: alle Pruefungen bestanden.');
else { console.log(`${befunde.length} Befund(e)`); befunde.forEach(b => console.log('  - ' + b)); }
