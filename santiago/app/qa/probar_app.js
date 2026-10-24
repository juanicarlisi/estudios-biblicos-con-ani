// Uso: node probar_app.js <archivo.html> <carpeta_capturas> [hash1,hash2,...] [--movil]
const { chromium } = require('playwright');
const [,, archivo, carpeta, lista, movil] = process.argv;
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: movil === '--movil' ? { width: 390, height: 844 } : { width: 1360, height: 900 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  const errores = [];
  p.on('console', m => { if (m.type() === 'error') errores.push('console: ' + m.text()); });
  p.on('pageerror', e => errores.push('pageerror: ' + e.message));
  await p.goto('file://' + archivo);
  await p.waitForTimeout(400);
  const hashes = (lista || 'inicio').split(',');
  for (const h of hashes) {
    await p.evaluate(h => { location.hash = h; }, h);
    await p.waitForTimeout(350);
    const nombre = h.replace(/[^a-z0-9-]/gi, '_') + (movil === '--movil' ? '_m' : '');
    await p.screenshot({ path: `${carpeta}/${nombre}.png`, fullPage: false });
    const desborde = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log(h, 'altura', await p.evaluate(() => document.documentElement.scrollHeight), 'desborde horizontal', desborde);
  }
  console.log(errores.length ? 'ERRORES:\n' + errores.join('\n') : 'sin errores de consola');
  await b.close();
})();
