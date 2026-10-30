#!/usr/bin/env python3
"""Arma la app «El varón según Dios» (un solo HTML) a partir de los datos de trabajo.

Uso: python3 construir.py [salida.html] [--artefacto]
Por defecto arma un documento completo para abrir como archivo (UTF-8, tipografías incluidas, sin conexión).
Lee de trabajo/varon/: plan/partes.json, plan/plan.json, dias/dia_NNN.json, notas/*.json (notas extraídas),
bloques/_fuentes.json (autor y obra de cada fuente), web/datos.json (estadísticas y artículos), biblia/rvr.json
(versículos clave RVR1960) y textos/*.json.
"""
import json, glob, os, re, sys, base64

V = os.environ.get('VARON', '/home/user/trabajo/varon')
AQUI = os.path.dirname(os.path.abspath(__file__))
ARTEFACTO = '--artefacto' in sys.argv
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
SALIDA = _args[0] if _args else os.path.join(AQUI, '..', 'el-varon-segun-dios.html')
FUENTES_DIR = os.path.join(AQUI, 'tipografias')
AVISO_RVR = 'Texto bíblico: Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.'


def etiqueta(autor):
    """Apellido corto para la etiqueta de fuente."""
    a = re.split(r'\s+y\s+|,|\(', autor or '')[0].strip()
    especiales = {'Comentario Bíblico Beacon': 'Beacon', 'Comentario Bíblico Mundo Hispano': 'Mundo Hispano', 'Diccionario Bíblico Mundo Hispano': 'Dicc. Mundo Hispano',
                  'Biblia de bosquejos y sermones': 'Bosquejos y sermones', 'Comentario Bíblico Moody': 'Moody', 'Varios': 'Varios'}
    for k, v in especiales.items():
        if a.startswith(k):
            return v
    m = re.search(r'(P[ée]rez Millos|Lloyd-Jones|De Haan|de la Cruz|Mac[Aa]rthur)', a)
    if m:
        return {'MacArthur': 'MacArthur', 'Macarthur': 'MacArthur'}.get(m.group(1), m.group(1))
    return a.split()[-1] if a else 'Fuente'


def registro_fuentes():
    fuentes = json.load(open(f'{V}/bloques/_fuentes.json'))
    out = {}
    for f in sorted(glob.glob(f'{V}/notas/*.json')):
        b = os.path.basename(f)[:-5]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            src = fuentes.get(n.get('fuente'), {})
            out[f'{b}#{i}'] = [etiqueta(src.get('autor')), f"{src.get('autor', '')}, {src.get('obra', '')}", f"pág. {n.get('pagina', '')}"]
    web = json.load(open(f'{V}/web/datos.json')) if os.path.exists(f'{V}/web/datos.json') else {}
    for wid, w in web.items():
        out[wid] = [w.get('etiqueta') or w.get('fuente', 'Web'), w.get('fuente', ''), w.get('detalle', ''), w.get('url', '')]
    return out, web


def recoger(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'fuentes' and isinstance(v, list):
                acc.update(v)
            else:
                recoger(v, acc)
    elif isinstance(o, list):
        for v in o:
            recoger(v, acc)
    return acc


def recoger_textos(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in ('fuentes', 'notas_no_usadas'):
                recoger_textos(v, acc)
    elif isinstance(o, list):
        for v in o:
            recoger_textos(v, acc)
    elif isinstance(o, str):
        acc.append(o)
    return acc


def documento_local(pagina):
    """Documento completo con las tipografías incrustadas (una cara por archivo, con rango de grosor)."""
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


def main():
    partes = json.load(open(f'{V}/plan/partes.json'))
    plan = json.load(open(f'{V}/plan/plan.json'))
    dias = {}
    patron = os.environ.get('DIAS', 'dia_')
    for f in sorted(glob.glob(f'{V}/dias/{patron}*.json')):
        d = json.load(open(f)); dias[d['dia']] = d
    todas, web = registro_fuentes()
    usados = recoger(dias, set())
    fuentes = {i: todas[i] for i in usados if i in todas}
    rvr_todo = json.load(open(f'{V}/biblia/rvr.json')) if os.path.exists(f'{V}/biblia/rvr.json') else {}
    # texto RVR1960: tope de 500 versículos en todo el estudio → un versículo clave por día (el más corto),
    # empezando por los de 1 versículo y siguiendo con los de 2, hasta completar el cupo; el resto va solo con su referencia y el enlace
    CUPO = 500
    def costo(ref):
        m = re.search(r':(\d+)-(\d+)$', ref)
        return 1 + (int(m.group(2)) - int(m.group(1)) if m else 0)
    cand = []
    for n, d in sorted(dias.items()):
        refs = [v['ref'] for v in d.get('versiculos', []) if v['ref'] in rvr_todo]
        if refs:
            r = min(refs, key=costo)
            cand.append((costo(r), n, r))
    rvr, gastado = {}, 0
    for c, n, r in sorted(cand):
        if c <= 2 and gastado + c <= CUPO:
            rvr[r] = rvr_todo[r]; gastado += c
    n_vers = gastado
    assert n_vers <= CUPO, f'demasiados versículos RVR citados: {n_vers}'
    libros = sorted({tuple(todas[i][1].split(', ', 1)) for i in usados if i in todas and not i.startswith('W')})
    web_usadas = sorted({(todas[i][0], todas[i][1], todas[i][3]) for i in usados if i.startswith('W') and i in todas})
    textos = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f'{V}/textos/*.json')}
    # líneas de ayuda oficiales (verificadas a mano) en los días que tratan temas delicados
    ayuda = json.load(open(f'{V}/web/ayuda.json')) if os.path.exists(f'{V}/web/ayuda.json') else {'temas': {}}
    for d in dias.values():
        texto = ' '.join(recoger_textos(d, [])).lower()
        cabeza = ' '.join([d.get('titulo', ''), d.get('bajada', ''), d.get('entrada', {}).get('texto', '')]).lower()
        # el recuadro aparece solo si el tema está en el título, la bajada o la entrada, o si el día lo nombra 4 veces o más
        d['ayuda'] = [k for k, t in ayuda['temas'].items() if re.search(t['patron'], cabeza) or len(re.findall(t['patron'], texto)) >= 4]
    ayuda_app = {'consultado': ayuda.get('consultado', ''), 'temas': {k: {'titulo': t['titulo'], 'lineas': t['lineas']} for k, t in ayuda['temas'].items()}}
    textos.setdefault('como-usar', {'ojo': 'Guía', 'titulo': 'Cómo usar el estudio', 'html': '<p>Un día por vez: leé el pasaje, recorré el estudio y terminá con las preguntas y la oración.</p>'})
    series = json.load(open(f'{V}/web/series.json')) if os.path.exists(f'{V}/web/series.json') else None
    datos = {'series': series, 'partes': partes, 'plan': plan, 'dias': dias, 'fuentes': fuentes, 'rvr': rvr, 'textos': textos, 'ayuda': ayuda_app,
             'obras': {'libros': [list(o) for o in libros], 'web': [list(o) for o in web_usadas]}, 'aviso_rvr': AVISO_RVR}
    plantilla = open(os.path.join(AQUI, 'plantilla.html')).read()
    js = 'window.DATOS = ' + json.dumps(datos, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
    out = plantilla.replace('/*__DATOS__*/', js)
    if not ARTEFACTO:
        out = documento_local(out)
    open(SALIDA, 'w').write(out)
    print('escrito', os.path.abspath(SALIDA), f'{len(out)/1e6:.2f} MB', '| días', len(dias), '| fuentes', len(fuentes), '| versículos RVR', n_vers)


if __name__ == '__main__':
    main()
