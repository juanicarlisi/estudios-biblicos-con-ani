import asyncio, json, sys, os
from playwright.async_api import async_playwright
ARCH = sys.argv[1]; DIA = int(sys.argv[2]) if len(sys.argv) > 2 else 2
CAP = '/home/user/trabajo/varon/capturas'
OUT = '/tmp/claude-0/-home-user/44c4606d-53a4-5379-822f-2c9154e9fd45/scratchpad'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
        pg = await ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        await pg.goto(f'file://{ARCH}#dia-{DIA}'); await pg.wait_for_timeout(1200)
        # resaltar: seleccionar parte del segundo párrafo
        ok = await pg.evaluate("""() => { const el = document.querySelectorAll('#hoja p.nota.ak')[0]; const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const n = w.nextNode();
          const r = document.createRange(); r.setStart(n, 10); r.setEnd(n, 80); const s = getSelection(); s.removeAllRanges(); s.addRange(r); document.dispatchEvent(new Event('selectionchange')); return n.nodeValue.slice(10, 80); }""")
        await pg.wait_for_timeout(500)
        print('popup visible:', await pg.is_visible('#sel-pop'), '| texto:', ok[:50])
        await pg.click('#sel-pop .sw[data-c="verde"]'); await pg.wait_for_timeout(300)
        print('marcas:', await pg.evaluate("document.querySelectorAll('#hoja mark.hl').length"))
        # nota sobre otra selección
        await pg.evaluate("""() => { const el = document.querySelectorAll('#hoja p.nota.ak')[2]; const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const n = w.nextNode();
          const r = document.createRange(); r.setStart(n, 0); r.setEnd(n, 40); const s = getSelection(); s.removeAllRanges(); s.addRange(r); document.dispatchEvent(new Event('selectionchange')); }""")
        await pg.wait_for_timeout(500); await pg.click('#pop-nota'); await pg.wait_for_timeout(300)
        await pg.keyboard.type('Esto lo tengo que hablar con Ani esta noche.'); await pg.wait_for_timeout(900)
        # lápiz: dos trazos sobre el texto
        await pg.click('#t-lapiz'); await pg.wait_for_timeout(200)
        box = await pg.evaluate("(() => { const r = document.querySelectorAll('#hoja p.nota.ak')[1].getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })()")
        x, y, w, h = box
        await pg.mouse.move(x + 20, y + h - 4); await pg.mouse.down()
        for i in range(30): await pg.mouse.move(x + 20 + i * (w - 60) / 30, y + h - 4 + (i % 3)); 
        await pg.mouse.up()
        await pg.click('#tintas .tinta[data-t="rojo"]')
        await pg.mouse.move(x + w - 30, y + 10); await pg.mouse.down()
        for i in range(24):
            import math; await pg.mouse.move(x + w - 30 + 18 * math.cos(i / 3.8), y + 22 + 14 * math.sin(i / 3.8))
        await pg.mouse.up(); await pg.wait_for_timeout(300)
        await pg.click('#t-leer')
        print('trazos:', await pg.evaluate("document.querySelectorAll('#lienzo path').length"))
        await pg.screenshot(path=f'{CAP}/app-dia.png')
        await pg.evaluate("document.querySelectorAll('#hoja p.nota.ak')[2].scrollIntoView({block:'center'})"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{CAP}/app-dia-nota.png')
        # descargar el día
        async with pg.expect_download() as dd: await pg.click('#t-descargar')
        dl = await dd.value; await dl.save_as(f'{OUT}/dia-exportado.html'); print('día descargado:', dl.suggested_filename, os.path.getsize(f'{OUT}/dia-exportado.html'))
        # guardar el estudio con marcas
        async with pg.expect_download() as dg: await pg.click('#guardar-btn')
        g = await dg.value; await g.save_as(f'{OUT}/estudio-con-marcas.html'); print('estudio guardado:', g.suggested_filename, os.path.getsize(f'{OUT}/estudio-con-marcas.html'))
        print('errores:', errs)
        await ctx.close()
        # abrir el estudio guardado en un navegador limpio (sin localStorage)
        ctx2 = await b.new_context(viewport={'width': 1440, 'height': 900}); pg2 = await ctx2.new_page(); errs2 = []
        pg2.on('pageerror', lambda e: errs2.append(str(e)))
        await pg2.goto(f'file://{OUT}/estudio-con-marcas.html#dia-{DIA}'); await pg2.wait_for_timeout(1500)
        print('en el guardado → marcas:', await pg2.evaluate("document.querySelectorAll('#hoja mark.hl').length"), '| notas:', await pg2.evaluate("[...document.querySelectorAll('.anot-nota textarea')].map(t=>t.value)"), '| trazos:', await pg2.evaluate("document.querySelectorAll('#lienzo path').length"), '| errores:', errs2)
        await ctx2.close()
        # día exportado
        ctx3 = await b.new_context(viewport={'width': 1440, 'height': 900}); pg3 = await ctx3.new_page()
        await pg3.goto(f'file://{OUT}/dia-exportado.html'); await pg3.wait_for_timeout(800)
        await pg3.screenshot(path=f'{CAP}/app-dia-exportado.png')
        print('exportado → marcas:', await pg3.evaluate("document.querySelectorAll('mark.hl').length"), '| trazos:', await pg3.evaluate("document.querySelectorAll('svg.lienzo path').length"))
        # celular
        ctx4 = await b.new_context(viewport={'width': 390, 'height': 844}, color_scheme='dark'); pg4 = await ctx4.new_page()
        await pg4.goto(f'file://{ARCH}#dia-{DIA}'); await pg4.wait_for_timeout(1000); await pg4.screenshot(path=f'{CAP}/app-dia-movil.png')
        print('ancho móvil:', await pg4.evaluate('document.documentElement.scrollWidth'))
        await b.close()
asyncio.run(main())
