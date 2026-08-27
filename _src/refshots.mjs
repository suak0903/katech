/**
 * Startseiten-Bilder der Referenzprojekte fuer die Referenz-Riege.
 *
 * Der Vorgaenger lief ueber Edge headless mit virtueller Zeit. Das reicht
 * nicht: die Seiten blenden ihre Texte beim Scrollen ein, und ohne echtes
 * Scrollen feuert kein IntersectionObserver - auf den Bildern fehlte
 * deshalb der halbe Text (Suat 27.08.).
 *
 * Hier wird jede Seite wirklich durchgescrollt, danach wieder nach oben,
 * und es wird gewartet, bis kein Bild mehr nachlaedt. Zustimmungsbanner
 * werden ausgeblendet, damit sie nicht das Motiv verdecken.
 *
 * Auf networkidle wird bewusst nicht gewartet: Seiten mit dauerhaften
 * Verbindungen erreichen diesen Zustand nie, der Lauf hing dann fest.
 * Jeder Schritt hat stattdessen seine eigene Frist.
 */
import { chromium } from 'playwright';
import { execFileSync } from 'child_process';
import { mkdirSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const ZIEL = path.join(HIER, '..', 'media', 'refs');
const TMP = path.join(HIER, '_shots');
mkdirSync(ZIEL, { recursive: true });
mkdirSync(TMP, { recursive: true });

const REFS = [
  ['cancontrols', 'https://suak0903.github.io/cancontrols/'],
  ['seitec', 'https://suak0903.github.io/seitec/'],
  ['akyol', 'https://www.akyol.de'],
  ['coreform', 'https://www.core-form.de'],
  ['barista', 'https://barista-biker.de/'],
  ['msrodenkirchen', 'https://suak0903.github.io/ms-rodenkirchen/'],
];

// Was ein Zustimmungsbanner sein koennte. Wird ausgeblendet, nicht geklickt:
// ein Klick setzt Einwilligungen, die hier niemand geben will.
const BANNER = [
  '[id*="cookie" i]', '[class*="cookie" i]', '[id*="consent" i]',
  '[class*="consent" i]', '[class*="cmplz" i]', '[id*="cmplz" i]',
  '.demobar', '#demobar', '[class*="banner" i][class*="privacy" i]',
];

/** Fuehrt aus, bricht nach der Frist ab statt haengen zu bleiben. */
function mitFrist(versprechen, ms, was) {
  return Promise.race([
    versprechen,
    new Promise((_, ab) => setTimeout(() => ab(new Error('Frist ueberschritten: ' + was)), ms)),
  ]);
}

const browser = await chromium.launch();
let fehler = 0;

for (const [name, url] of REFS) {
  const kontext = await browser.newContext({
    viewport: { width: 1366, height: 854 },
    deviceScaleFactor: 2,
    // Bewegungsarme Darstellung: Einblendungen stehen damit sofort am Ziel
    reducedMotion: 'reduce',
  });
  const seite = await kontext.newPage();
  let status = '?';
  try {
    const antwort = await seite.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    status = antwort ? antwort.status() : '?';
    await seite.waitForLoadState('load', { timeout: 30000 }).catch(() => {});

    // Einmal durch die Seite, damit jeder Beobachter ausloest
    await mitFrist(seite.evaluate(async () => {
      const schritt = Math.round(window.innerHeight * 0.8);
      const ende = Math.min(document.body.scrollHeight, schritt * 12);
      for (let y = 0; y < ende; y += schritt) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 110));
      }
      window.scrollTo(0, 0);
    }), 25000, 'Durchlauf').catch(e => console.log('     ' + e.message));
    await seite.waitForTimeout(1200);

    // Nachzuegler: was noch als "einblenden" markiert ist, wird sichtbar gesetzt
    await seite.evaluate(() => {
      for (const el of document.querySelectorAll(
          '.rv, .reveal, [data-reveal], [class*="fade"], [class*="animate"]')) {
        el.classList.add('an', 'in', 'is-visible', 'visible', 'sichtbar', 'aktiv');
        el.style.opacity = '1';
        el.style.transform = 'none';
      }
    }).catch(() => {});

    await seite.evaluate(auswahl => {
      for (const a of auswahl) {
        for (const el of document.querySelectorAll(a)) {
          const r = el.getBoundingClientRect();
          // Nur Leisten am Rand, nicht den halben Seiteninhalt
          if (r.height > 0 && r.height < window.innerHeight * 0.5) el.style.display = 'none';
        }
      }
    }, BANNER).catch(() => {});

    // Warten, bis jedes Bild geladen ist, aber nicht ewig
    await mitFrist(seite.evaluate(() => Promise.all(
      [...document.images].filter(i => !i.complete)
        .map(i => new Promise(r => { i.onload = i.onerror = r; })))),
      15000, 'Bilder').catch(() => {});
    await seite.waitForTimeout(900);

    const png = path.join(TMP, name + '.png');
    await seite.screenshot({ path: png });

    for (const [endung, guete] of [['webp', '82'], ['jpg', '85']]) {
      execFileSync('magick', [png, '-strip', '-resize', '1280x', '-gravity', 'north',
                              '-crop', '1280x800+0+0', '+repage', '-quality', guete,
                              path.join(ZIEL, name + '.' + endung)]);
    }
    console.log(`  ${name.padEnd(16)} HTTP ${status}  Bild aufgenommen`);
  } catch (e) {
    fehler++;
    console.log(`  ${name.padEnd(16)} FEHLER: ${String(e).split('\n')[0]}`);
  }
  await kontext.close();
}

await browser.close();
console.log(fehler === 0 ? 'Alle Referenzbilder neu aufgenommen.' : `${fehler} Referenzbilder fehlen.`);
