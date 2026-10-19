import asyncio, sys
from playwright.async_api import async_playwright
URL='file:///home/user/trabajo/estudio-prueba.html'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        errores=[]
        async def tomar(nombre, hash_, w=1440, h=900, oscuro=False, full=False):
            ctx = await b.new_context(viewport={'width':w,'height':h}, color_scheme='dark' if oscuro else 'light')
            pg = await ctx.new_page()
            pg.on('console', lambda m: errores.append(f'{nombre}: {m.type}: {m.text}') if m.type in ('error','warning') else None)
            pg.on('pageerror', lambda e: errores.append(f'{nombre}: pageerror {e}'))
            await pg.goto(URL+'#'+hash_); await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f'capturas/{nombre}.png', full_page=full)
            ancho = await pg.evaluate('document.documentElement.scrollWidth')
            if ancho > w: errores.append(f'{nombre}: scroll horizontal {ancho}>{w}')
            await ctx.close()
        for a in sys.argv[1:]:
            n,hsh,w,h,osc,full=a.split('|')
            await tomar(n,hsh,int(w),int(h),osc=='1',full=='1')
        await b.close()
        print('\n'.join(errores) or 'sin errores')
asyncio.run(main())
