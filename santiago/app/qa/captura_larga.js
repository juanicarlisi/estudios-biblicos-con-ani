// Uso: node captura_larga.js <archivo.html> <hash> <salida_prefijo> [--movil] -> varias capturas de 900px de alto
const { chromium } = require('playwright');
const [,, archivo, hash, prefijo, movil] = process.argv;
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: movil === '--movil' ? { width: 390, height: 844 } : { width: 1360, height: 900 } });
  const p = await ctx.newPage();
  const errores = [];
  p.on('pageerror', e => errores.push(e.message));
  await p.goto('file://' + archivo);
  await p.evaluate(h => { location.hash = h; }, hash);
  await p.waitForTimeout(500);
  const alto = await p.evaluate(() => document.documentElement.scrollHeight);
  let n = 0;
  for (let y = 0; y < alto && n < 8; y += 820) {
    await p.evaluate(y => window.scrollTo(0, y), y);
    await p.waitForTimeout(150);
    await p.screenshot({ path: `${prefijo}_${n}.png` });
    n++;
  }
  console.log('alto', alto, 'capturas', n, errores.length ? 'ERRORES ' + errores.join('|') : 'sin errores');
  await b.close();
})();
