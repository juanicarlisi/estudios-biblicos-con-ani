#!/usr/bin/env python3
"""Arma la app del estudio de Apocalipsis (un solo HTML, sin conexión) a partir de los datos de trabajo.

Uso: python3 apocalipsis/app/construir.py [salida.html]
Por defecto escribe apocalipsis/estudio-apocalipsis.html (documento completo, UTF-8, tipografías incrustadas).
Lee (todo en apocalipsis/trabajo/): plan/plan.json, plan/articulos.json, plan/visuales.json, plan/fuentes_comentarios.json,
     dias/dia_NN.json, articulos/art_<ID>.json (tolera los que falten), diagramas/dg-*.json, extracciones/*.json,
     mapas/datos_mapas.json, griego/apocalipsis_griego.json y, fuera del repositorio, SCRATCH/biblia/rvr1960_apocalipsis.json
     (RVR1960: no se commitea; se incrustan solo los versículos clave, con un tope de 500).
Modelo: genesis/app/construir.py (misma idea: plantilla + window.DATOS + tipografías en base64).
"""
import json, glob, os, re, sys, base64, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
T = os.path.normpath(os.path.join(AQUI, '..', 'trabajo'))
SCRATCH = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
RVR_ARCHIVO = os.path.join(SCRATCH, 'biblia', 'rvr1960_apocalipsis.json')
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
SALIDA = _args[0] if _args else os.path.normpath(os.path.join(AQUI, '..', 'estudio-apocalipsis.html'))
FUENTES_DIR = os.path.join(AQUI, 'tipografias')   # woff2 (latin, latin-ext, greek, greek-ext) y su CSS de Google Fonts
TOPE_RVR = 500
MAPA_MARCO = {'mapa-asia': 'asia', 'mapa-mediterraneo': 'mediterraneo', 'mapa-santa': 'santa'}

# lugares de los mapas que se buscan en el texto bíblico de cada día (para el mini mapa)
LUGAR_CLAVES = {
    'patmos': ['Patmos'], 'efeso': ['Éfeso'], 'esmirna': ['Esmirna'], 'pergamo': ['Pérgamo'], 'tiatira': ['Tiatira'],
    'sardis': ['Sardis'], 'filadelfia': ['Filadelfia'], 'laodicea': ['Laodicea'], 'jerusalen': ['Jerusalén'],
    'meguido': ['Armagedón'], 'egipto': ['Egipto'], 'babilonia': ['Babilonia'], 'eufrates': ['Éufrates'],
}


def leer(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------- fuentes (chips)
ETIQUETAS = [  # etiquetas cortas que el apellido final no resuelve bien
    (r'^TTL Training', 'TTL'), (r'^Diccionario de Jes[uú]s y los Evangelios', 'Dicc. de Jesús y los Evangelios'),
    (r"Master'?s Seminary", 'MacArthur y TMS'), (r'^(J\. )?K(œ|oe)chlin', 'Kœchlin'), (r'^Ministerios Ligonier', 'Ligonier'),
    (r'Lloyd-Jones', 'Lloyd-Jones'), (r'^Varios autores', 'Varios autores'),
]


def apellido(autor):
    for pat, et in ETIQUETAS:
        if re.search(pat, autor):
            return et
    autor = re.sub(r'\([^)]*\)', '', autor)
    autor = re.sub(r',?\s+Jr\.?(?=\s|$|,)', '', autor).strip()
    partes = [p.strip() for p in re.split(r'\s+y\s+', autor) if p.strip()][:2]
    return ' y '.join(p.split()[-1] for p in partes) if partes else ''


def pagina_corta(p):
    m = re.search(r'p[áa]g(?:ina)?s?\.?\s*(?:PDF\s*)?([\d][\d\s,\-–y]*)', p or '', re.I)
    return ('p. ' + m.group(1).strip(' ,-')) if m else ''


def etiqueta_web(pagina, pref):
    """«Título, Autor, URL» → (corto, obra, url)."""
    url = ''
    m = re.search(r'(https?://\S+)\s*$', pagina or '')
    resto = pagina or ''
    if m:
        url = m.group(1); resto = pagina[:m.start()].strip().rstrip(',')
    partes = [x.strip() for x in resto.split(', ')]
    autor = partes[-1] if len(partes) > 1 else ''
    titulo = ', '.join(partes[:-1]) if len(partes) > 1 else resto
    sitio = 'Coalición por el Evangelio' if pref == 'cpe' else (re.sub(r'^www\.', '', url.split('/')[2]) if url.count('/') >= 2 else 'artículo web')
    anonimo = not autor or re.search(r'sin autor|equipo|redacci', autor, re.I)
    corto = ('Coalición' if pref == 'cpe' else sitio) if anonimo else apellido(autor)
    obra = (f'{autor}, ' if not anonimo else '') + f'«{titulo}» ({sitio})'
    return corto, obra, url


def _resumen(n, cont):
    t = (n.get('titulo') or '').strip()
    return [t, cont[:1].upper() + cont[1:]]


def fuentes_por_id():
    """id de nota → [corto, obra, página, resumen, escuela]."""
    FC = leer(f'{T}/plan/fuentes_comentarios.json')
    out = {}
    for f in sorted(glob.glob(f'{T}/extracciones/*.json')):
        b = os.path.basename(f)[:-5]; pref = b.split('_')[0]
        for i, n in enumerate(leer(f)['notas'], 1):
            pag = str(n.get('pagina', '') or '')
            cont = (n.get('contenido') or '').strip()
            escuela = n.get('escuela') or ''
            if pref in ('cpe', 'web'):
                corto, obra, url = etiqueta_web(pag, pref)
                m = re.match(r'^((?:[^:]|:(?=\S)){3,160}?):\s', cont)
                if m and corto.split()[0].lower() in m.group(1).lower():
                    cont = cont[m.end():]
                out[f'{b}#{i}'] = [corto, obra, url, _resumen(n, cont), escuela]
            elif pref in FC:
                c = FC[pref]
                out[f'{b}#{i}'] = [c['corto'], c['obra'], pag.replace('PÁGINA PDF', 'pág. PDF'), _resumen(n, cont), escuela or c.get('escuela', '')]
            else:   # r1, r2: «Autor, Obra:» al comienzo del contenido
                m = re.match(r'^((?:[^:]|:(?=\S)){3,200}?):\s', cont)
                autor, obra = '', ''
                if m and ', ' in m.group(1):
                    autor, obra = m.group(1).split(', ', 1)
                    obra = re.sub(r'\s*\([^)]*\d+[:.]\d+[^)]*\)\s*$', '', obra)
                    cont = cont[m.end():]
                if not obra:
                    arch = pag.split(', pág')[0]
                    obra = re.sub(r'\.pdf$', '', arch.split('/')[-1], flags=re.I) if '/' in arch or arch.lower().endswith('.pdf') else 'libro de referencia'
                corto = apellido(autor) if autor and len(autor) < 70 else ''
                p = re.search(r'p[áa]g\..*$', pag)
                out[f'{b}#{i}'] = [corto or 'Referencia', f'{autor}, {obra}' if corto else obra, p.group(0) if p else pag, _resumen(n, cont), escuela]
    return out


# ---------------------------------------------------------------- texto bíblico y griego
def rango_ref(ref):
    """'C:V' o 'C:V-V' o 'C:V-C:V' → lista de (c, v)."""
    ref = re.sub(r'^(Ap|Apoc|Apocalipsis)\.?\s*', '', ref.strip()).replace('–', '-').replace(' ', '')
    m = re.match(r'^(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?$', ref)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    c2 = int(m.group(3) or c1); v2 = int(m.group(4) or v1)
    if c2 == c1:
        return [(c1, v) for v in range(v1, v2 + 1)]
    return [(c1, v) for v in range(v1, 40)] + [(c2, v) for v in range(1, v2 + 1)]


def sin_marcas(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r'[^\w]', '', s.lower()).replace('ς', 'σ')


def strong_de(palabra, griego, lexico):
    """Busca la palabra comentada entre las del versículo para darle número de Strong y lema."""
    toks = griego.get(re.sub(r'-.*$', '', palabra.get('ref', '')), [])
    if not toks:
        return
    for w in (palabra.get('griego') or '').split():
        k = sin_marcas(w)
        if len(k) < 3 and len((palabra.get('griego') or '').split()) > 1:
            continue
        for t in toks:
            if sin_marcas(t['p']) == k or sin_marcas(t['l']) == k:
                palabra['strong'] = t['s']; palabra['lema'] = t['l']
                lx = lexico.get(t['s'])
                if lx:
                    palabra['xlit'] = lx.get('xlit', '')
                return


# ---------------------------------------------------------------- principal
def main():
    plan_json = leer(f'{T}/plan/plan.json')
    partes, plan = plan_json['partes'], plan_json['dias']
    dias = {}
    for f in sorted(glob.glob(f'{T}/dias/dia_*.json')):
        d = leer(f); dias[d['dia']] = d
    for p in plan:
        p['titulo'] = dias[p['dia']]['titulo'] if p['dia'] in dias else p.get('titulo_provisional', '')
        for k in ('titulo_provisional', 'unidades', 'peso', 'ini', 'fin'):
            p.pop(k, None)
    meta_arts = leer(f'{T}/plan/articulos.json')
    articulos, faltan = {}, []
    omitir = set(filter(None, os.environ.get('OMITIR_ARTICULOS', '').split(',')))   # para probar artículos ausentes
    for a in meta_arts:
        f = f"{T}/articulos/art_{a['id']}.json"
        if os.path.exists(f) and a['id'] not in omitir:
            x = leer(f); x.pop('notas_no_usadas', None)
            for v in x.get('versiculos', []):
                v['ref'] = re.sub(r'^(Ap|Apoc|Apocalipsis)\.?\s*', '', v['ref'].strip())
            articulos[a['id']] = x
        else:
            faltan.append(a['id'])
    visuales = leer(f'{T}/plan/visuales.json')
    diagramas = {}
    for g in visuales['diagramas']:
        f = f'{T}/diagramas/{g}.json'
        if os.path.exists(f):
            diagramas[g] = leer(f)
    mapas = leer(f'{T}/mapas/datos_mapas.json')

    # griego: Strong para las palabras comentadas; texto SBLGNT de los versículos clave
    G = leer(f'{T}/griego/apocalipsis_griego.json')
    gv, lexico = G['versiculos'], G['lexico']
    for x in list(dias.values()) + list(articulos.values()):
        for w in x.get('palabras', []) or []:
            strong_de(w, gv, lexico)

    # fuentes efectivamente citadas
    todas = fuentes_por_id()
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
    recoger(dias); recoger(articulos); recoger(diagramas)
    fuentes = {i: todas[i] for i in sorted(usados) if i in todas}
    sin_fuente = sorted(i for i in usados if i not in todas)

    # versículos clave (RVR1960) y su griego: solo los de los días y los artículos, con tope de 500
    refs = [d['versiculo_clave']['ref'] for d in dias.values() if d.get('versiculo_clave', {}).get('ref')]
    for x in articulos.values():
        refs += [v['ref'] for v in x.get('versiculos', [])]
    versos = set()
    for r in refs:
        versos.update(rango_ref(r))
    n_vers = len(versos)
    assert n_vers <= TOPE_RVR, f'demasiados versículos RVR1960 citados: {n_vers} (tope {TOPE_RVR})'
    rvr, griego_clave = {}, {}
    hay_rvr = os.path.exists(RVR_ARCHIVO)
    if hay_rvr:
        texto = leer(RVR_ARCHIVO)['texto']
    else:
        print(f'AVISO: falta {RVR_ARCHIVO}; la app se arma sin texto bíblico (solo las referencias).', file=sys.stderr)
    for r in sorted(set(refs)):
        vs = rango_ref(r)
        if hay_rvr:
            partes_t = [texto.get(str(c), {}).get(str(v)) for c, v in vs]
            if all(partes_t):
                rvr[r] = ' '.join(partes_t)
        gt = [' '.join(w['t'] for w in gv.get(f'{c}:{v}', [])) for c, v in vs]
        if all(gt):
            griego_clave[r] = ' '.join(gt)

    # lugares por día: los que nombra el texto bíblico del día (o, sin RVR, el «dónde» del contexto)
    lugares_dia = {}
    for p in plan:
        if hay_rvr:
            txt = ' '.join(texto.get(str(c), {}).get(str(v), '') for c, v in rango_ref(p['desde'] + '-' + p['hasta']))
        else:
            txt = ''
        x = dias.get(p['dia'])
        if x:
            txt += ' ' + x['contexto'].get('donde', '')
        ids = [k for k, claves in LUGAR_CLAVES.items() if any(re.search(r'(?<!\w)' + re.escape(w) + r'(?!\w)', txt) for w in claves)]
        if ids:
            lugares_dia[p['dia']] = ids

    # obras citadas (para la página de fuentes)
    FC = leer(f'{T}/plan/fuentes_comentarios.json')
    pref_usados = {i.split('_')[0] for i in fuentes}
    comentarios = [[v['corto'], v['obra'], v.get('escuela', '')] for k, v in FC.items() if k in pref_usados]
    referencia = sorted({(f[0], f[1]) for i, f in fuentes.items() if i.split('_')[0] in ('r1', 'r2')}, key=lambda t: t[1].lower())
    web = sorted({(f[0], f[1]) for i, f in fuentes.items() if i.split('_')[0] in ('cpe', 'web')}, key=lambda t: t[1].lower())

    datos = {
        'partes': partes, 'plan': plan, 'dias': dias,
        'articulos': articulos, 'articulos_orden': [{k: a[k] for k in ('id', 'grupo', 'titulo', 'rango') if k in a} for a in meta_arts],
        'diagramas': diagramas, 'visuales': visuales, 'mapas': mapas, 'mapa_marco': MAPA_MARCO,
        'fuentes': fuentes, 'rvr': rvr, 'griego_clave': griego_clave, 'hay_rvr': hay_rvr, 'lugares_dia': lugares_dia,
        'obras': {'comentarios': comentarios, 'referencia': [list(o) for o in referencia], 'web': [list(o) for o in web]},
        'aviso_rvr': 'Texto bíblico: Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988. '
                     'Utilizado con permiso. Reina-Valera 1960™ es una marca registrada de la American Bible Society, y puede ser usada solamente bajo licencia. '
                     f'Se citan solo los versículos clave ({n_vers}, menos de {TOPE_RVR}).',
        'aviso_griego': 'Texto griego: SBL Greek New Testament (SBLGNT) © Society of Biblical Literature y Faithlife, CC BY 4.0. '
                        'Números de Strong: Strong\'s Greek Dictionary (OpenScriptures, CC BY-SA).',
    }
    plantilla = open(os.path.join(AQUI, 'plantilla.html'), encoding='utf-8').read()
    js = 'window.DATOS = ' + json.dumps(datos, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
    out = documento_local(plantilla.replace('/*__DATOS__*/', js))
    with open(SALIDA, 'w', encoding='utf-8') as f:
        f.write(out)
    tam = os.path.getsize(SALIDA)
    print('escrito', SALIDA, f'{tam / 1e6:.2f} MB', '| días', len(dias), '| artículos', len(articulos),
          ('(faltan: ' + ', '.join(faltan) + ')') if faltan else '', '| diagramas', len(diagramas), '| fuentes', len(fuentes),
          '| versículos RVR', n_vers if hay_rvr else '0 (sin archivo)', '| lugares en días', len(lugares_dia))
    if sin_fuente:
        print('AVISO: ids de fuente sin nota extraída:', len(sin_fuente), sin_fuente[:10], file=sys.stderr)


def documento_local(pagina):
    """Envuelve la página en un documento completo e incrusta las tipografías (base64) para usarla sin conexión."""
    css = open(os.path.join(FUENTES_DIR, 'fuentes.css'), encoding='utf-8').read()
    grupos = {}
    for subset, cara in re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
        if subset not in ('latin', 'latin-ext', 'greek', 'greek-ext'):
            continue
        campo = lambda k: re.search(k + r':\s*([^;]+);', cara).group(1).strip()
        url = re.search(r'url\((https://[^)]+)\)', campo('src')).group(1)
        archivo = os.path.join(FUENTES_DIR, url.rsplit('/', 1)[1])
        if not os.path.exists(archivo):
            continue
        clave = (campo('font-family'), campo('font-style'), archivo, campo('unicode-range'))
        grupos.setdefault(clave, []).append(int(campo('font-weight')))
    caras = []
    for (familia, estilo, archivo, rango), pesos in grupos.items():
        datos = base64.b64encode(open(archivo, 'rb').read()).decode()
        peso = str(pesos[0]) if len(set(pesos)) == 1 else f'{min(pesos)} {max(pesos)}'
        caras.append(f"@font-face {{ font-family: {familia}; font-style: {estilo}; font-weight: {peso}; font-display: swap; "
                     f"src: url(data:font/woff2;base64,{datos}) format('woff2'); unicode-range: {rango}; }}")
    pagina = pagina.replace('/*__TIPOGRAFIAS__*/', '\n'.join(caras))
    return pagina


if __name__ == '__main__':
    main()
