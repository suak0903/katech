/** Prueft die Fusszeile: jeder Link fuehrt irgendwohin, die Anker der
 *  Solutions-Seite springen wirklich, und nichts steht mehr in der falschen
 *  Spalte. */
import { chromium } from 'playwright';

const BASIS = 'http://localhost:8777';
let fehler = 0;
const pruefe = (b, was) => { console.log((b ? '  ok    ' : '  FEHLER') + '  ' + was); if (!b) fehler++; };

const browser = await chromium.launch();
const seite = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await seite.goto(BASIS + '/');

// Spalten und ihre Eintraege einlesen
const spalten = await seite.$$eval('.foot nav[aria-labelledby^="foot-"]', navs =>
  navs.map(n => ({
    titel: n.querySelector('h2').textContent.trim(),
    punkte: [...n.querySelectorAll('a')].map(a => ({ text: a.textContent.trim(), ziel: a.getAttribute('href') })),
  })));

const alle = spalten.flatMap(s => s.punkte.map(p => s.titel + ' / ' + p.text));
pruefe(!alle.some(x => x.startsWith('Expertise / How we work')), 'How we work steht nicht unter Expertise');
pruefe(!alle.some(x => x.startsWith('Expertise / Our people')), 'Our people steht nicht unter Expertise');
pruefe(alle.includes('Company / How we work'), 'How we work steht unter Company');
pruefe(alle.includes('Company / Our people'), 'Our people steht unter Company');
pruefe(!alle.some(x => x.includes('Our facilities')), 'Our facilities steht nicht mehr im Fuss');
pruefe(!alle.some(x => x.startsWith('Company / Find us')), 'Find us steht nicht mehr unter Company');
pruefe(alle.includes('Solutions / Vegan solutions'), 'Vegan solutions steht unter Solutions');
pruefe(!alle.some(x => x.includes('Plant-based meat and fish')), 'alte Bezeichnung ist weg');

const knopfZiele = await seite.$$eval('.foot__social', a => a.map(x => x.getAttribute('href')));
pruefe(knopfZiele.some(z => z.includes('find-us')), 'Find us liegt als Knopf neben LinkedIn');

// Jeder Fusslink muss erreichbar sein
for (const s of spalten) {
  for (const p of s.punkte) {
    const antwort = await seite.request.get(BASIS + '/' + p.ziel.split('#')[0]);
    pruefe(antwort.ok(), `${s.titel} / ${p.text} -> ${p.ziel}`);
  }
}

// Die vier Anker muessen auf der Solutions-Seite wirklich etwas treffen
for (const anker of ['dairy', 'plant', 'savoury', 'bakery']) {
  await seite.goto(BASIS + '/solutions/#' + anker);
  await seite.waitForTimeout(700);
  const da = await seite.locator('#' + anker).count();
  const y = da ? await seite.locator('#' + anker).evaluate(el => el.getBoundingClientRect().top) : null;
  pruefe(da === 1 && Math.abs(y) < 260, `Anker #${anker} springt (Abstand ${y === null ? '-' : Math.round(y)} px)`);
}

// Der Knopf im Hero der Solutions-Seite
await seite.goto(BASIS + '/solutions/');
await seite.waitForTimeout(400);
const heroZiel = await seite.locator('.subhero__cta a').first().getAttribute('href');
const heroText = await seite.locator('.subhero__cta a').first().innerText();
pruefe(heroZiel.includes('vegan/'), 'Hero-Knopf fuehrt auf die Vegan-Seite');
pruefe(heroText.trim() === 'Vegan solutions', `Hero-Knopf heisst "Vegan solutions" (steht: "${heroText.trim()}")`);

await browser.close();
console.log(fehler === 0 ? '\nFuss: alle Pruefungen bestanden.' : `\nFuss: ${fehler} Befunde.`);
process.exit(fehler === 0 ? 0 : 1);
