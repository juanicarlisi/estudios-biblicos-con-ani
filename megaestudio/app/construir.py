#!/usr/bin/env python3
"""Arma la app «Estudio bíblico integral» (un solo HTML) a partir de los datos de trabajo.

Uso: python3 construir.py [salida.html] [--artefacto]
Lee de ../trabajo/: plan/ciclos.json (ciclos y series), plan/plan.json (días detallados, orden recomendado),
dias/dia_NNN.json, libros.json (autor y obra de cada fuente), biblia/rvr.json (versículos clave RVR1960) y textos/*.json.
Los ids de día son fijos (no cambian aunque se detallen más días); la app muestra «Ciclo · Serie · día k de K»."""
import json, glob, os, re, sys, base64
AQUI = os.path.dirname(os.path.abspath(__file__))
V = os.path.abspath(os.path.join(AQUI, '..', 'trabajo'))
ARTEFACTO = '--artefacto' in sys.argv
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
SALIDA = _args[0] if _args else os.path.join(AQUI, '..', 'estudio-biblico-integral.html')
FUENTES_DIR = os.path.join(AQUI, 'tipografias')
AVISO_RVR = 'Texto bíblico: Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.'

# reutiliza el armado del documento local (tipografías incrustadas) del estudio del varón
def documento_local(pagina):
    css = open(os.path.join(FUENTES_DIR, 'fuentes.css')).read()
    grupos = {}
    for subset, cara in re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
        if subset not in ('latin', 'latin-ext', 'hebrew', 'greek'):
            continue
        campo = lambda k: re.search(k + r':\s*([^;]+);', cara).group(1).strip()
        clave = (campo('font-family'), campo('font-style'), campo('src'), campo('unicode-range'))
        grupos.setdefault(clave, []).append(int(campo('font-weight')))
    caras = []
    for (familia, estilo, src, rango), pesos in grupos.items():
        url = re.search(r'url\((https://[^)]+)\)', src).group(1)
        datos = base64.b64encode(open(os.path.join(FUENTES_DIR, url.rsplit('/', 1)[1]), 'rb').read()).decode()
        peso = str(pesos[0]) if len(set(pesos)) == 1 else f'{min(pesos)} {max(pesos)}'
        caras.append(f"@font-face {{ font-family: {familia}; font-style: {estilo}; font-weight: {peso}; font-display: swap; "
                     f"src: url(data:font/woff2;base64,{datos}) format('woff2'); unicode-range: {rango}; }}")
    pagina = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', '<style>\n' + '\n'.join(caras) + '\n</style>', pagina)
    pagina = pagina.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    corte = pagina.index('<header')
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<style>[hidden] { display: none !important; } img { max-width: 100%; }</style>\n'
            + pagina[:corte] + '</head>\n<body>\n' + pagina[corte:] + '\n</body>\n</html>\n')


def etiqueta(autor):
    a = re.split(r'\s+y\s+|,|\(', autor or '')[0].strip()
    return a.split()[-1] if a else 'Fuente'


def recoger(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'fuentes' and isinstance(v, list): acc.update(v)
            else: recoger(v, acc)
    elif isinstance(o, list):
        for v in o: recoger(v, acc)
    return acc


def main():
    ciclos = json.load(open(f'{V}/plan/ciclos.json'))['ciclos']
    plan = json.load(open(f'{V}/plan/plan.json'))            # [{dia, ciclo, serie, n, titulo}] en orden recomendado
    libros = json.load(open(f'{V}/libros.json'))
    series = {s['id']: s for c in ciclos for s in c['series']}
    partes = [{'id': c['id'], 'numero': c['numero'], 'titulo': c['titulo'], 'bajada': c['bajada'], 'series': [{'id': s['id'], 'titulo': s['titulo'], 'dias': s['dias'], 'enfoque': s['enfoque']} for s in c['series']]} for c in ciclos]
    por_serie = {}
    for p in plan: por_serie[p['serie']] = por_serie.get(p['serie'], 0) + 1
    PLAN = [{'dia': p['dia'], 'parte': p['ciclo'], 'serie': p['serie'], 'serie_titulo': series[p['serie']]['titulo'], 'n': p['n'], 'de': por_serie[p['serie']], 'titulo': p['titulo']} for p in plan]
    dias = {}
    for f in sorted(glob.glob(f'{V}/dias/dia_*.json')):
        d = json.load(open(f)); dias[d['dia']] = d
    usados = recoger(dias, set())
    fuentes, obras, webs = {}, set(), set()
    for i in usados:
        if i == 'biblia': fuentes[i] = ['Biblia', 'Texto bíblico citado', 'RVR1960']; continue
        lib, pag = i.split('#'); b = libros[lib]
        if b['repo'] == 'web':
            fuentes[i] = [b['autor'], f"{b['autor']}, {b['obra']}", f"sección {pag} · consultado el {b['consultado']}", b['url']]
            webs.add((b['autor'], b['obra'], b['url']))
            continue
        fuentes[i] = [etiqueta(b['autor']), f"{b['autor']}, {b['obra']}", f'pág. {pag} (del PDF)']
        obras.add((b['autor'], b['obra']))
    rvr_todo = json.load(open(f'{V}/biblia/rvr.json')) if os.path.exists(f'{V}/biblia/rvr.json') else {}
    rvr = {}; gastado = 0
    for n, d in sorted(dias.items()):
        for v in d.get('versiculos', []):
            if v['ref'] in rvr_todo and gastado < 500:
                rvr[v['ref']] = rvr_todo[v['ref']]; gastado += 1 + len(re.findall(r'\s*[-–]\s*\d+', v['ref']))
    textos = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f'{V}/textos/*.json')}
    textos.setdefault('como-usar', {'ojo': 'Guía', 'titulo': 'Cómo usar el estudio', 'html': '<p>Un día por vez: leé el pasaje, recorré el estudio y terminá con las preguntas y la oración.</p>'})
    datos = {'partes': partes, 'plan': PLAN, 'dias': dias, 'fuentes': fuentes, 'rvr': rvr, 'textos': textos, 'ayuda': {'consultado': '', 'temas': {}},
             'obras': {'libros': [list(o) for o in sorted(obras)], 'web': [list(o) for o in sorted(webs)]}, 'aviso_rvr': AVISO_RVR}
    plantilla = open(os.path.join(AQUI, 'plantilla.html')).read()
    js = 'window.DATOS = ' + json.dumps(datos, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
    out = plantilla.replace('/*__DATOS__*/', js)
    if not ARTEFACTO: out = documento_local(out)
    open(SALIDA, 'w').write(out)
    print(f'{len(PLAN)} días en el plan, {len(dias)} escritos, {len(rvr)} versículos RVR, {len(obras)} obras → {SALIDA}')


if __name__ == '__main__':
    main()
