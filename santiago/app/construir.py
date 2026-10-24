#!/usr/bin/env python3
"""Arma la app del estudio de Santiago (un solo HTML) a partir de los datos de trabajo.

Uso: python3 construir.py [salida.html] [--artefacto]
Por defecto arma un documento completo para abrir como archivo (UTF-8, tipografías incrustadas, sin conexión).
Con --artefacto arma la versión para publicar en claude.ai (la plataforma le pone el esqueleto del documento).
Lee (en santiago/trabajo): plan/plan.json y plan/partes.json, dias/dia_NN.json, articulos/art_*.json con plan/articulos.json,
extracciones/* y extracciones_ref3/* (para las etiquetas de fuente), biblia/rvr1960_santiago.json, griego/sblgnt_santiago_morphgnt.txt,
mapas/datos_mapas.json, plan/linea.json y textos/*.json (introducción, cómo usar, fuentes).
Con DIAS=borrador_ arma con los borradores de los días en vez de los definitivos.
"""
import json, glob, os, re, sys, base64
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'trabajo', 'scripts'))
import config as C

T = C.REPO_TRABAJO
ARTEFACTO = '--artefacto' in sys.argv
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
SALIDA = _args[0] if _args else os.path.join(HERE, '..', 'estudio-santiago.html')
FUENTES_DIR = os.path.join(HERE, 'tipografias')   # woff2 (latin, latin-ext, hebrew, griego) y su CSS de Google Fonts

COMENTARIOS = {
    'macarthur': ('MacArthur', 'John MacArthur, Santiago, Comentario MacArthur del Nuevo Testamento (Editorial Portavoz)'),
    'kistemaker': ('Kistemaker', 'Simon J. Kistemaker, Exposición de la Epístola de Santiago, en Comentario al Nuevo Testamento (2001)'),
    'carballosa': ('Carballosa', 'Evis L. Carballosa, Santiago: una fe en acción, edición actualizada (Editorial Portavoz, 1986, 2014)'),
    'george': ('E. George', 'Elizabeth George, Santiago: crece en sabiduría y fe (Editorial Portavoz, 2013)'),
    'cbmh': ('Mundo Hispano', 'Daniel Carro, «Santiago», Comentario Bíblico Mundo Hispano, tomo 23 (Editorial Mundo Hispano)'),
    'beacon': ('Beacon', 'A. F. Harper, «Santiago», Comentario Bíblico Beacon, tomo 10 (Casa Nazarena de Publicaciones)'),
    'macarthur_be': ('Biblia MacArthur', 'John MacArthur, Biblia de Estudio MacArthur, notas de Santiago (Editorial Portavoz)'),
    'dbmh': ('Diccionario MH', 'Diccionario Bíblico Mundo Hispano (Editorial Mundo Hispano)'),
}

# etiquetas cortas que el apellido final no resuelve bien (apellidos compuestos, obras colectivas)
ETIQUETAS = [
    (r'^comentario b[ií]blico mundo hispano', 'Mundo Hispano'), (r'editores generales: juan carlos cevallos', 'Mundo Hispano'),
    (r'p[ée]rez millos', 'Pérez Millos'), (r'de haan', 'De Haan'), (r'juan c\. de la cruz', 'De la Cruz'),
    (r'^antonio cruz', 'A. Cruz'), (r'coleman jr', 'Coleman'), (r'^varios \(plumer', 'Portavoz de la Gracia'),
    (r'^varios \(jeremy pierre', '9Marcas'), (r'^varios autores \(compilaci', 'Antología'),
    (r'^elizabeth george', 'E. George'), (r'^jim george', 'J. George'), (r'^joel b\. green', 'J. B. Green'),
    (r'^les thompson', 'L. Thompson'), (r'^w\. oscar thompson', 'O. Thompson'), (r'^norman geisler', 'Geisler'),
    (r'^samuel v[ií]la', 'S. Vila'), (r'^warren', 'Wiersbe'), (r'wayne grudem', 'Grudem'),
]


def etiqueta_ref3(autor, ape):
    for pat, et in ETIQUETAS:
        if re.search(pat, autor, re.I):
            return et
    return ape


def prefijo(bloque):
    return re.sub(r'_\d+$', '', bloque)


def pagina_biblio(p):
    p = str(p or '')
    m_imp = re.search(r'\[P\.\s*(\d+)\]', p)
    m_pdf = re.search(r'PÁGINA PDF (\d+)', p)
    ent = re.search(r'entrada:\s*(.+)$', p)
    if m_imp and m_pdf:
        return f'pág. {m_imp.group(1)} (PDF {m_pdf.group(1)})'
    if ent and m_pdf:
        return f'entrada «{ent.group(1).strip()}», pág. PDF {m_pdf.group(1)}'
    if m_pdf:
        return f'pág. PDF {m_pdf.group(1)}'
    return re.sub(r'^\w+\s*\|\s*', '', p)


def notas_por_id():
    out = {}
    for f in glob.glob(f'{T}/extracciones/*.json'):
        b = os.path.basename(f)[:-5]
        ab, nombre = COMENTARIOS.get(prefijo(b), (prefijo(b), prefijo(b)))
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            out[f'{b}#{i}'] = [ab, nombre, pagina_biblio(n.get('pagina'))]
    for f in glob.glob(f'{T}/extracciones_ref3/*.json'):
        b = os.path.basename(f)[:-5]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            autor = (n.get('autor') or '').strip(); obra = (n.get('obra') or '').strip()
            ape = re.split(r'\s+y\s+|,|\(', autor)[0].strip().split()[-1] if autor else 'Referencia'
            ape = etiqueta_ref3(autor, ape)
            m = re.search(r'citado por ([^)]+)\)', autor)
            if autor.lower().startswith('autor no identificado') and m:
                ape = m.group(1).split()[-1]; autor = f'Cita recogida por {m.group(1)}'
            out[f'{b}#{i}'] = [ape, f'{autor}, {obra}', f"pág. PDF {re.sub(r'[^0-9]', '', str(n.get('pagina', '')))}"]
    return out


def cargar_json(ruta, defecto):
    return json.load(open(ruta)) if os.path.exists(ruta) else defecto


def griego_por_verso():
    ruta = f'{T}/griego/sblgnt_santiago_morphgnt.txt'
    out = {}
    if not os.path.exists(ruta):
        return out
    for linea in open(ruta, encoding='utf-8'):
        p = linea.split()
        if len(p) < 7:
            continue
        ref = p[0]; c, v = int(ref[2:4]), int(ref[4:6])
        out.setdefault(f'{c}:{v}', []).append(p[3])
    return {k: ' '.join(v) for k, v in out.items()}


def main():
    plan = json.load(open(f'{T}/plan/plan.json'))
    partes = json.load(open(f'{T}/plan/partes.json'))
    rvr_json = json.load(open(f'{T}/biblia/rvr1960_santiago.json'))
    rvr = {f'{c}:{v}': t for c, vs in rvr_json['texto'].items() for v, t in vs.items()}
    assert len(rvr) <= 500, f'demasiados versículos RVR citados: {len(rvr)}'
    dias = {}
    for f in sorted(glob.glob(f"{T}/dias/{os.environ.get('DIAS', 'dia_')}*.json")):
        d = json.load(open(f)); dias[d['dia']] = d
    meta_arts = cargar_json(f'{T}/plan/articulos.json', [])
    articulos = {}
    for a in meta_arts:
        f = f"{T}/articulos/art_{a['id']}.json"
        if os.path.exists(f):
            x = json.load(open(f))
            x['refs_santiago'] = [re.sub(r'^(Stg|Santiago)\.?\s*', '', r.strip()) for r in x.get('refs_santiago', x.get('refs', []))]
            articulos[a['id']] = x
    todas = notas_por_id()
    usados = set()

    def recoger(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'fuentes' and isinstance(v, list):
                    usados.update(v)
                else:
                    recoger(v)
        elif isinstance(o, list):
            for v in o:
                recoger(v)
    recoger(dias); recoger(articulos)
    mapas = cargar_json(f'{T}/mapas/datos_mapas.json', None)
    if mapas:
        recoger(mapas)
    linea = cargar_json(f'{T}/plan/linea.json', None)
    if linea:
        recoger(linea)
    fuentes = {i: todas[i] for i in usados if i in todas}
    lugares_dia = {p['dia']: dias.get(p['dia'], {}).get('lugares', p.get('lugares', [])) for p in plan}
    linea_dia = cargar_json(f'{T}/plan/linea_dia.json', {})
    ref_obras = sorted({tuple(todas[i][1].split(', ', 1)) for i in usados if i in todas and not i.startswith(tuple(f'{k}_' for k in COMENTARIOS))})
    textos = {}
    for f in glob.glob(f'{T}/textos/*.json'):
        textos[os.path.basename(f)[:-5]] = json.load(open(f))
    textos.setdefault('introduccion', {'ojo': 'Antes de empezar', 'titulo': 'Introducción a Santiago', 'html': '<p>La introducción se está escribiendo con el material de la biblioteca.</p>'})
    textos.setdefault('como-usar', {'ojo': 'Guía', 'titulo': 'Cómo usar el estudio', 'html': '<p>Cada día: lean el pasaje, recorran el estudio y terminen con las preguntas y la oración.</p>'})
    textos.setdefault('fuentes', {'html': '<p>Cada afirmación del estudio lleva etiquetas con sus fuentes: tocándolas se ve la obra y la página.</p>'})
    if not mapas:
        mapas = {'marcos': {'oriente': {'W': 1000, 'H': 900, 'tierra': '', 'lagos': '', 'rios': {}}}, 'lugares': [], 'vistas': [{'id': 'x', 'nombre': 'Mapa', 'marco': 'oriente', 'lugares': [], 'texto': 'En preparación.'}], 'credito': ''}
    if not linea:
        linea = {'desde': 25, 'hasta': 70, 'paso': 5, 'eventos': [], 'explicacion': 'En preparación.', 'advertencia': '', 'fuentes': [], 'inicio_et': '', 'fin_et': ''}
    datos = {
        'plan': plan, 'partes': partes,
        'articulos': articulos, 'articulos_orden': [{k: a[k] for k in ('id', 'grupo', 'titulo', 'parte', 'rango') if k in a} for a in meta_arts],
        'dias': dias, 'fuentes': fuentes, 'rvr': rvr, 'griego': griego_por_verso(),
        'mapas': mapas, 'lugares_dia': lugares_dia, 'linea_dia': linea_dia, 'linea': linea, 'textos': textos,
        'obras': {'comentarios': [[v[0], v[1]] for v in COMENTARIOS.values()], 'referencia': [list(o) for o in ref_obras]},
        'aviso_rvr': rvr_json.get('leyenda', 'Texto bíblico: Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.'),
        'aviso_griego': 'Texto griego: The Greek New Testament: SBL Edition (SBLGNT), © 2010 Society of Biblical Literature y Logos Bible Software, licencia CC BY 4.0 (sblgnt.com/license).',
    }
    plantilla = open(os.path.join(HERE, 'plantilla.html')).read()
    motor = open(os.path.join(HERE, 'motor.js')).read()
    js = 'window.DATOS = ' + json.dumps(datos, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
    out = plantilla.replace('/*__DATOS__*/', js).replace('/*__MOTOR__*/', motor)
    if not ARTEFACTO:
        out = documento_local(out)
    open(SALIDA, 'w').write(out)
    print('escrito', os.path.abspath(SALIDA), f'{len(out)/1e6:.2f} MB', '| días', len(dias), 'de', len(plan), '| artículos', len(articulos), '| fuentes', len(fuentes), '| versículos RVR', len(rvr))


def documento_local(pagina):
    """Envuelve la página en un documento completo e incrusta las tipografías para usarla sin conexión."""
    css = open(os.path.join(FUENTES_DIR, 'fuentes.css')).read()
    grupos = {}
    for subset, cara in re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
        campo = lambda k: re.search(k + r':\s*([^;]+);', cara).group(1).strip()
        familia = campo('font-family').strip("'\"")
        if subset not in ('latin', 'latin-ext', 'hebrew') and not (familia == 'Gentium Plus' and subset in ('greek', 'greek-ext')):
            continue
        if familia == 'Gentium Plus' and subset not in ('latin', 'greek', 'greek-ext'):
            continue
        clave = (campo('font-family'), campo('font-style'), campo('src'), campo('unicode-range'))
        grupos.setdefault(clave, []).append(int(campo('font-weight')))
    caras = []
    for (familia, estilo, src, rango), pesos in grupos.items():
        url = re.search(r'url\((https://[^)]+)\)', src).group(1)
        datos = base64.b64encode(open(os.path.join(FUENTES_DIR, url.rsplit('/', 1)[1]), 'rb').read()).decode()
        peso = str(pesos[0]) if len(set(pesos)) == 1 else f'{min(pesos)} {max(pesos)}'
        caras.append(f"@font-face {{ font-family: {familia}; font-style: {estilo}; font-weight: {peso}; font-display: swap; "
                     f"src: url(data:font/woff2;base64,{datos}) format('woff2'); unicode-range: {rango}; }}")
    pagina = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', pagina)
    pagina = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', '<style>\n' + '\n'.join(caras) + '\n</style>', pagina)
    pagina = pagina.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    corte = pagina.index('<header')
    cabeza, cuerpo = pagina[:corte], pagina[corte:]
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<style>[hidden] { display: none !important; } img { max-width: 100%; }</style>\n'
            + cabeza + '</head>\n<body>\n' + cuerpo + '\n</body>\n</html>\n')


if __name__ == '__main__':
    main()
