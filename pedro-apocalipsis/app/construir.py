#!/usr/bin/env python3
"""Arma la app combinada «1 Pedro a Apocalipsis» (un solo HTML, sin conexión) con los dos estudios.

Uso: python3 pedro-apocalipsis/app/construir.py [salida.html]
Por defecto escribe pedro-apocalipsis/estudio-pedro-a-apocalipsis.html.
Lee (solo lectura) apocalipsis/trabajo/ y pedro-judas/trabajo/ (plan, días, artículos, diagramas, extracciones, mapas, griego) y,
fuera del repositorio, SCRATCH/biblia/rvr1960_apocalipsis.json y rvr1960_pedro_judas.json (RVR1960: no se commitea; se incrustan
solo los versículos clave de días y artículos de los dos estudios, con un tope de 500 en total).
Tolera días, artículos y diagramas que falten (se muestran «en preparación»): basta volver a correrlo cuando aparezcan.
Para probar faltantes: OMITIR=pj-T1,pj-dg-hogar,ap-T3 (ids prefijados por estudio).
Modelo: apocalipsis/app/construir.py (misma idea: plantilla + window.DATOS + tipografías en base64), generalizado a dos estudios.
"""
import json, glob, os, re, sys, base64, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, '..', '..'))
SCRATCH = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
SALIDA = _args[0] if _args else os.path.normpath(os.path.join(AQUI, '..', 'estudio-pedro-a-apocalipsis.html'))
FUENTES_DIR = os.path.join(AQUI, 'tipografias')
TOPE_RVR = 500
OMITIR = set(filter(None, (os.environ.get('OMITIR', '') + ',' + os.environ.get('OMITIR_ARTICULOS', '')).split(',')))

LIBROS = [  # orden canónico
    {'id': '1P', 'nombre': '1 Pedro', 'est': 'pj', 'gr': 'Πέτρου Α'},
    {'id': '2P', 'nombre': '2 Pedro', 'est': 'pj', 'gr': 'Πέτρου Β'},
    {'id': '1J', 'nombre': '1 Juan', 'est': 'pj', 'gr': 'Ἰωάννου Α'},
    {'id': '2J', 'nombre': '2 Juan', 'est': 'pj', 'gr': 'Ἰωάννου Β'},
    {'id': '3J', 'nombre': '3 Juan', 'est': 'pj', 'gr': 'Ἰωάννου Γ'},
    {'id': 'Jd', 'nombre': 'Judas', 'est': 'pj', 'gr': 'Ἰούδα'},
    {'id': 'Ap', 'nombre': 'Apocalipsis', 'est': 'ap', 'gr': 'Ἀποκάλυψις'},
]
UNICAP = {'2J', '3J', 'Jd'}   # libros de un solo capítulo: refs «Jd 3-4»

ESTUDIOS = {
    'pj': {'T': os.path.join(RAIZ, 'pedro-judas', 'trabajo'), 'nombre': 'Las cartas de Pedro, Juan y Judas',
           'rvr': 'rvr1960_pedro_judas.json', 'griego': 'griego/pedro_judas_griego.json',
           # visual de mapa → marco del mapa unido
           'mapas': {'mapa-provincias': 'provincias', 'mapa-efeso': 'asia', 'mapa-mediterraneo': 'mediterraneo', 'mapa-oriente': 'oriente'},
           'marcos': {'asia': 'provincias', 'mediterraneo': 'mediterraneo', 'oriente': 'oriente'},
           'lugares': {'ponto': ['Ponto'], 'galacia': ['Galacia'], 'capadocia': ['Capadocia'], 'asia': ['Asia'], 'bitinia': ['Bitinia'],
                       'babilonia': ['Babilonia'], 'roma': ['Roma'], 'efeso': ['Éfeso'], 'patmos': ['Patmos'],
                       'sodoma': ['Sodoma', 'Gomorra'], 'egipto': ['Egipto']}},
    'ap': {'T': os.path.join(RAIZ, 'apocalipsis', 'trabajo'), 'nombre': 'Apocalipsis',
           'rvr': 'rvr1960_apocalipsis.json', 'griego': 'griego/apocalipsis_griego.json',
           'mapas': {'mapa-asia': 'asia', 'mapa-mediterraneo': 'mediterraneo', 'mapa-santa': 'santa'},
           'marcos': {'asia': 'asia', 'mediterraneo': 'mediterraneo', 'santa': 'santa'},
           'lugares': {'patmos': ['Patmos'], 'efeso': ['Éfeso'], 'esmirna': ['Esmirna'], 'pergamo': ['Pérgamo'], 'tiatira': ['Tiatira'],
                       'sardis': ['Sardis'], 'filadelfia': ['Filadelfia'], 'laodicea': ['Laodicea'], 'jerusalen': ['Jerusalén'],
                       'meguido': ['Armagedón'], 'egipto': ['Egipto'], 'babilonia': ['Babilonia'], 'eufrates': ['Éufrates']}},
}
MARCO_MAPA = {'provincias': 'pj-mapa-provincias', 'oriente': 'pj-mapa-oriente', 'mediterraneo': 'pj-mapa-mediterraneo',
              'asia': 'ap-mapa-asia', 'santa': 'ap-mapa-santa'}   # visual que representa a cada marco
MARCO_RUTA = {'provincias': 'provincias', 'asia': 'cartas'}
MARCO_TITULO = {'mediterraneo': 'El Mediterráneo: los lugares de Pedro, Juan, Judas y el Apocalipsis'}
MARCOS_ORDEN = ['provincias', 'asia', 'santa', 'oriente', 'mediterraneo']   # del más chico al más grande (mini mapa)


def leer(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------- fuentes (chips)
ETIQUETAS = [
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


def etiqueta_web(pagina, pref):
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


def fuentes_por_id(T, FC, pre):
    """id de nota (con prefijo de estudio `pre`) → [corto, obra, página, resumen, escuela]; y los ids de referencia y web."""
    out, ref_ids, web_ids = {}, set(), set()
    for f in sorted(glob.glob(f'{T}/extracciones/*.json')):
        b = os.path.basename(f)[:-5]; pref = b.split('_')[0]
        for i, n in enumerate(leer(f)['notas'], 1):
            pag = str(n.get('pagina', '') or '')
            cont = (n.get('contenido') or '').strip()
            escuela = n.get('escuela') or ''
            k = f'{pre}{b}#{i}'
            if pref in ('cpe', 'web'):
                corto, obra, url = etiqueta_web(pag, pref)
                m = re.match(r'^((?:[^:]|:(?=\S)){3,160}?):\s', cont)
                if m and corto.split()[0].lower() in m.group(1).lower():
                    cont = cont[m.end():]
                out[k] = [corto, obra, url, _resumen(n, cont), escuela]; web_ids.add(k)
            elif pref in FC and FC[pref].get('corto') != 'referencia':
                c = FC[pref]
                out[k] = [c['corto'], c['obra'], pag.replace('PÁGINA PDF', 'pág. PDF'), _resumen(n, cont), escuela or c.get('escuela', '')]
            else:   # libros de referencia: «Autor, Obra:» al comienzo del contenido
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
                out[k] = [corto or 'Referencia', f'{autor}, {obra}' if corto else obra, p.group(0) if p else pag, _resumen(n, cont), escuela]
                ref_ids.add(k)
    return out, ref_ids, web_ids


# ---------------------------------------------------------------- referencias, texto bíblico y griego
SIGLA = re.compile(r'^(1P|2P|1J|2J|3J|Jd|Ap|Apoc|Apocalipsis)\.?\s+(?=\d)')


def libro_y_resto(ref, libro_def):
    ref = (ref or '').strip().replace('–', '-')
    m = SIGLA.match(ref)
    if m:
        L = 'Ap' if m.group(1).startswith('Ap') else m.group(1)
        return L, ref[m.end():]
    return (libro_def if re.match(r'^\d', ref) else None), ref


def norm_ref(ref, libro_def):
    """Referencia con sigla: «1:3» del Apocalipsis → «Ap 1:3»; las que ya traen sigla (o son de otro libro) quedan igual."""
    L, resto = libro_y_resto(ref, libro_def)
    return f'{L} {resto}' if L and resto else ref


def rango_ref(ref, libro_def=None):
    """Referencia → (libro, [(c, v)…]); [] si no es de estos siete libros o no se entiende."""
    L, r = libro_y_resto(ref, libro_def)
    if not L:
        return None, []
    r = re.sub(r'(?<=\d)[a-c](?=$|-)', '', r.replace(' ', ''))
    if L in UNICAP:
        m = re.match(r'^(?:1:)?(\d+)(?:-(?:1:)?(\d+))?$', r)
        if not m:
            return L, []
        v1 = int(m.group(1)); v2 = int(m.group(2) or v1)
        return L, [(1, v) for v in range(v1, v2 + 1)]
    m = re.match(r'^(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?$', r)
    if not m:
        return L, []
    c1, v1 = int(m.group(1)), int(m.group(2))
    c2 = int(m.group(3) or c1); v2 = int(m.group(4) or v1)
    if c2 == c1:
        return L, [(c1, v) for v in range(v1, v2 + 1)]
    out = [(c1, v) for v in range(v1, 60)]
    for c in range(c1 + 1, c2):
        out += [(c, v) for v in range(1, 60)]
    return L, out + [(c2, v) for v in range(1, v2 + 1)]


class Biblia:
    def __init__(self):
        self.griego, self.lexico, self.rvr = {}, {}, {}
        g = leer(os.path.join(ESTUDIOS['ap']['T'], ESTUDIOS['ap']['griego']))
        self.griego.update({('Ap',) + tuple(map(int, k.split(':'))): v for k, v in g['versiculos'].items()})
        self.lexico.update(g['lexico'])
        g = leer(os.path.join(ESTUDIOS['pj']['T'], ESTUDIOS['pj']['griego']))
        for k, v in g['versiculos'].items():
            L, cv = k.split(' ', 1)
            c, vv = (cv.split(':') if ':' in cv else ('1', cv))
            self.griego[(L, int(c), int(vv))] = v
        for k, v in g['lexico'].items():
            self.lexico.setdefault(k, v)
        self.hay_rvr = True
        for e in ('ap', 'pj'):
            ruta = os.path.join(SCRATCH, 'biblia', ESTUDIOS[e]['rvr'])
            if not os.path.exists(ruta):
                print(f'AVISO: falta {ruta}; la app se arma sin ese texto bíblico (solo las referencias).', file=sys.stderr)
                self.hay_rvr = False
                continue
            t = leer(ruta)['texto']
            if e == 'ap':
                t = {'Ap': t}
            for L, caps in t.items():
                for c, vs in caps.items():
                    for v, txt in vs.items():
                        self.rvr[(L, int(c), int(v))] = txt

    def versos(self, ref, libro_def=None):
        """Versículos que existen (según el texto griego, siempre presente)."""
        L, vs = rango_ref(ref, libro_def)
        return [(L, c, v) for c, v in vs if (L, c, v) in self.griego]

    def texto(self, ref, libro_def=None):
        return ' '.join(self.rvr.get(k, '') for k in self.versos(ref, libro_def)).strip()


def sin_marcas(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r'[^\w]', '', s.lower()).replace('ς', 'σ')


def strong_de(palabra, B, libro_def):
    vs = B.versos(re.sub(r'(\d)-.*$', r'\1', palabra.get('ref', '')), libro_def)
    toks = B.griego.get(vs[0], []) if vs else []
    if not toks:
        return
    for w in (palabra.get('griego') or '').split():
        k = sin_marcas(w)
        if len(k) < 3 and len((palabra.get('griego') or '').split()) > 1:
            continue
        for t in toks:
            if sin_marcas(t['p']) == k or sin_marcas(t['l']) == k:
                palabra['strong'] = t['s']; palabra['lema'] = t['l']
                lx = B.lexico.get(t['s'])
                if lx:
                    palabra['xlit'] = lx.get('xlit', '')
                return


def prefijar_fuentes(o, pre):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'fuentes' and isinstance(v, list):
                o[k] = [pre + i for i in v]
            else:
                prefijar_fuentes(v, pre)
    elif isinstance(o, list):
        for v in o:
            prefijar_fuentes(v, pre)


# ---------------------------------------------------------------- un estudio
def cargar_estudio(e, B, nombre_libro):
    C = ESTUDIOS[e]; T = C['T']; pre = e + '-'
    pf = 'pj/' if e == 'pj' else ''          # los ids de notas de Pedro–Judas llevan prefijo (hay archivos con el mismo nombre)
    plan_json = leer(f'{T}/plan/plan.json')
    dias_arch = {}
    for f in sorted(glob.glob(f'{T}/dias/dia_*.json')):
        d = leer(f); dias_arch[d['dia']] = d
    # plan con claves estables por libro: «1P-3», «Ap-45»
    plan, por_libro, clave_de = [], {}, {}
    for p in plan_json['dias']:
        L = p.get('libro') or 'Ap'
        por_libro[L] = por_libro.get(L, 0) + 1
        k = f'{L}-{por_libro[L]}'
        clave_de[p['dia']] = k
        x = dias_arch.get(p['dia'])
        plan.append({'k': k, 'est': e, 'libro': L, 'n': por_libro[L], 'dia': p['dia'], 'parte': pre + p['parte'],
                     'rango': norm_ref(p['rango'], L), 'versiculos': p.get('versiculos', 0),
                     'titulo': x['titulo'] if x else p.get('titulo_provisional', '')})
    dk = lambda lista: [clave_de[d] for d in (lista or []) if d in clave_de]
    vis = lambda lista: [pre + v for v in (lista or [])]

    partes = []
    for pt in plan_json['partes']:
        q = dict(pt); q['id'] = pre + pt['id']; q['est'] = e
        if e == 'ap':
            q['etiqueta'] = 'Apocalipsis · ' + pt['etiqueta']
        q['rango'] = norm_ref(pt['rango'], 'Ap' if e == 'ap' else None)
        partes.append(q)

    # artículos
    meta_arts = leer(f'{T}/plan/articulos.json')
    articulos, orden, faltan = {}, [], []
    for a in meta_arts:
        aid = pre + a['id']
        rango = a.get('rango') or ''
        if a['grupo'] == 'intro' or not re.search(r'\d', rango):
            rtxt = ''
        else:
            rtxt = norm_ref(rango, 'Ap' if e == 'ap' else None)
        orden.append({'id': aid, 'id0': a['id'], 'est': e, 'grupo': a['grupo'], 'titulo': a['titulo'], 'rango': rtxt, 'libros': a.get('libros') or (['Ap'] if e == 'ap' else [])})
        f = f"{T}/articulos/art_{a['id']}.json"
        if os.path.exists(f) and aid not in OMITIR:
            x = leer(f); x.pop('notas_no_usadas', None)
            for w in x.get('palabras', []) or []:
                strong_de(w, B, 'Ap' if e == 'ap' else None)
                w['ref'] = norm_ref(w.get('ref', ''), 'Ap' if e == 'ap' else None)
            for v in x.get('versiculos', []):
                v['ref'] = norm_ref(v['ref'], 'Ap' if e == 'ap' else None)
            x['dias_relacionados'] = dk(x.get('dias_relacionados'))
            x['visuales'] = vis(x.get('visuales'))
            x['id'] = aid
            prefijar_fuentes(x, pf)
            articulos[aid] = x
        else:
            faltan.append(aid)
    # panorama de cada parte: Apocalipsis, P<n> de la parte n; Pedro–Judas, el del libro (P1 1P, P2 2P, P3 1J)
    for q in partes:
        if e == 'ap':
            q['panorama'] = pre + 'P' + re.sub(r'\D', '', q['id'])
        else:
            libs = {p['libro'] for p in plan if p['parte'] == q['id']}
            pan = [a['id'] for a in orden if a['grupo'] == 'panorama' and libs & set(a['libros'])]
            if pan:
                q['panorama'] = pan[0]

    # diagramas
    visuales = leer(f'{T}/plan/visuales.json')
    diagramas, faltan_dg = {}, []
    for g in visuales['diagramas']:
        f = f'{T}/diagramas/{g}.json'
        if os.path.exists(f) and pre + g not in OMITIR:
            x = leer(f)
            x['id0'] = g; x['id'] = pre + g; x['est'] = e
            x['dias'] = dk(x.get('dias'))
            if e == 'ap':
                for r in (x.get('filas') or []) + (x.get('tarjetas') or []):
                    if r.get('ref'):
                        r['ref'] = norm_ref(r['ref'], 'Ap')
            prefijar_fuentes(x, pf)
            diagramas[pre + g] = x
        else:
            faltan_dg.append(pre + g)

    # días
    dias = {}
    for n, d in dias_arch.items():
        if n not in clave_de:
            continue
        L = d.get('libro') or 'Ap'
        d['libro'] = L; d['k'] = clave_de[n]; d['est'] = e; d['n'] = int(clave_de[n].split('-')[1])
        for w in d.get('palabras', []) or []:
            strong_de(w, B, L)
            w['ref'] = norm_ref(w.get('ref', ''), L)
        if e == 'ap':
            for s in d.get('simbolos', []) or []:
                s['refs'] = [norm_ref(r, 'Ap') for r in s.get('refs', [])]
        if d.get('versiculo_clave', {}).get('ref'):
            d['versiculo_clave']['ref'] = norm_ref(d['versiculo_clave']['ref'], L)
        d['visuales'] = vis(d.get('visuales'))
        d['anexos'] = [pre + a for a in d.get('anexos', []) or []]
        prefijar_fuentes(d, pf)
        dias[d['k']] = d

    # lugares por día (texto bíblico del tramo y el «dónde» del contexto)
    lugares_dia = {}
    for p in plan:
        txt = B.texto(p['rango'], p['libro'])
        x = dias.get(p['k'])
        if x:
            txt += ' ' + x['contexto'].get('donde', '')
        ids = [k for k, claves in C['lugares'].items() if any(re.search(r'(?<!\w)' + re.escape(w) + r'(?!\w)', txt) for w in claves)]
        if ids:
            lugares_dia[p['k']] = ids

    FC = leer(f'{T}/plan/fuentes_comentarios.json')
    fuentes, ref_ids, web_ids = fuentes_por_id(T, FC, pf)
    return {'plan': plan, 'partes': partes, 'dias': dias, 'articulos': articulos, 'orden': orden, 'faltan': faltan,
            'diagramas': diagramas, 'faltan_dg': faltan_dg, 'lugares_dia': lugares_dia, 'FC': FC,
            'fuentes': fuentes, 'ref_ids': ref_ids, 'web_ids': web_ids, 'pf': pf,
            'visuales': {'mapas': {pre + k: v for k, v in visuales['mapas'].items()}, 'diagramas': {pre + k: v for k, v in visuales['diagramas'].items()}}}


def unir_mapas():
    marcos, lugares, recorridos, mapa_marco, credito = {}, {}, {}, {}, ''
    for e in ('ap', 'pj'):
        C = ESTUDIOS[e]
        M = leer(os.path.join(C['T'], 'mapas', 'datos_mapas.json'))
        credito = credito or M['credito']
        for k, v in M['marcos'].items():
            nuevo = C['marcos'][k]
            if nuevo in marcos:   # mismo marco en los dos estudios: misma proyección; se queda con el dibujo más completo
                viejo = marcos[nuevo]
                if any(viejo[c] != v[c] for c in ('W', 'H', 'bbox')):
                    raise SystemExit(f'marco {nuevo} con otra proyección en los dos estudios')
                for c in ('tierra', 'lagos'):
                    if len(v.get(c) or '') > len(viejo.get(c) or ''):
                        viejo[c] = v[c]
                viejo['rios'] = {**(v.get('rios') or {}), **(viejo.get('rios') or {})}
                continue
            marcos[nuevo] = v
        for l in M['lugares']:
            q = {kk: vv for kk, vv in l.items() if kk not in M['marcos']}
            for k in M['marcos']:
                if k in l:
                    q[C['marcos'][k]] = l[k]
            if l['id'] in lugares:
                viejo = lugares[l['id']]
                for kk, vv in q.items():
                    if kk in marcos and kk not in viejo:
                        viejo[kk] = vv
                if q.get('nota') and q['nota'] != viejo.get('nota'):
                    viejo['nota'] = f"En Apocalipsis: {viejo.get('nota', '')} En las cartas: {q['nota']}"
            else:
                lugares[l['id']] = q
        for k, v in M['recorridos'].items():
            recorridos[k] = v
        for vid, marco in C['mapas'].items():
            mapa_marco[f'{e}-{vid}'] = marco
    return {'marcos': marcos, 'lugares': list(lugares.values()), 'recorridos': recorridos, 'credito': credito}, mapa_marco


# ---------------------------------------------------------------- principal
def main():
    B = Biblia()
    nombre_libro = {l['id']: l['nombre'] for l in LIBROS}
    E = {e: cargar_estudio(e, B, nombre_libro) for e in ('pj', 'ap')}
    plan = E['pj']['plan'] + E['ap']['plan']   # orden canónico: 1P, 2P, 1J, 2J, 3J, Jd, Ap
    orden_lib = [l['id'] for l in LIBROS]
    plan.sort(key=lambda p: (orden_lib.index(p['libro']), p['n']))
    mapas, mapa_marco = unir_mapas()
    marco_mapa = {m: v for m, v in MARCO_MAPA.items() if mapa_marco.get(v) == m}   # pestañas de la página de mapas

    # fuentes efectivamente citadas
    todas = {**E['ap']['fuentes'], **E['pj']['fuentes']}
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
    for x in E.values():
        recoger(x['dias']); recoger(x['articulos']); recoger(x['diagramas'])
    fuentes = {i: todas[i] for i in sorted(usados) if i in todas}
    sin_fuente = sorted(i for i in usados if i not in todas)

    # versículos clave (RVR1960) y su griego: solo los de días y artículos de los dos estudios, con tope de 500
    refs = []
    for x in E.values():
        refs += [d['versiculo_clave']['ref'] for d in x['dias'].values() if d.get('versiculo_clave', {}).get('ref')]
        for a in x['articulos'].values():
            refs += [v['ref'] for v in a.get('versiculos', [])]
    versos = set()
    for r in refs:
        versos.update(B.versos(r))
    n_vers = len(versos)
    assert n_vers <= TOPE_RVR, f'demasiados versículos RVR1960 citados: {n_vers} (tope {TOPE_RVR})'
    rvr, griego_clave = {}, {}
    for r in sorted(set(refs)):
        vs = B.versos(r)
        if not vs:
            continue
        if B.rvr:
            partes_t = [B.rvr.get(k) for k in vs]
            if all(partes_t):
                rvr[r] = ' '.join(partes_t)
        gt = [' '.join(w['t'] for w in B.griego.get(k, [])) for k in vs]
        if all(gt):
            griego_clave[r] = ' '.join(gt)

    # obras citadas (página de fuentes)
    comentarios = []
    for e, tit in (('pj', 'Comentarios de 1 Pedro a Judas'), ('ap', 'Comentarios del Apocalipsis')):
        FC, pf = E[e]['FC'], E[e]['pf']
        pref_usados = {i[len(pf):].split('_')[0] for i in fuentes if i.startswith(pf) and (e == 'pj' or not i.startswith('pj/'))}
        filas = [[v['corto'], v['obra'], v.get('escuela') or v.get('tradicion', '')] for k, v in FC.items() if k in pref_usados and v.get('corto') != 'referencia']
        comentarios.append([tit, filas])
    ref_ids = E['ap']['ref_ids'] | E['pj']['ref_ids']; web_ids = E['ap']['web_ids'] | E['pj']['web_ids']
    referencia = sorted({(f[0], f[1]) for i, f in fuentes.items() if i in ref_ids}, key=lambda t: t[1].lower())
    web = sorted({(f[0], f[1]) for i, f in fuentes.items() if i in web_ids}, key=lambda t: t[1].lower())

    datos = {
        'libros': LIBROS, 'estudios': {e: ESTUDIOS[e]['nombre'] for e in ESTUDIOS},
        'partes': E['pj']['partes'] + E['ap']['partes'], 'plan': plan, 'dias': {**E['pj']['dias'], **E['ap']['dias']},
        'articulos': {**E['pj']['articulos'], **E['ap']['articulos']}, 'articulos_orden': E['pj']['orden'] + E['ap']['orden'],
        'diagramas': {**E['pj']['diagramas'], **E['ap']['diagramas']},
        'visuales': {'mapas': {**E['pj']['visuales']['mapas'], **E['ap']['visuales']['mapas']},
                     'diagramas': {**E['pj']['visuales']['diagramas'], **E['ap']['visuales']['diagramas']}},
        'mapas': mapas, 'mapa_marco': mapa_marco, 'marco_mapa': marco_mapa, 'marco_ruta': MARCO_RUTA, 'marco_titulo': MARCO_TITULO,
        'marcos_orden': MARCOS_ORDEN,
        'fuentes': fuentes, 'rvr': rvr, 'griego_clave': griego_clave, 'hay_rvr': B.hay_rvr,
        'lugares_dia': {**E['pj']['lugares_dia'], **E['ap']['lugares_dia']},
        'obras': {'comentarios': comentarios, 'referencia': [list(o) for o in referencia], 'web': [list(o) for o in web]},
        'aviso_rvr': 'Texto bíblico: Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988. '
                     'Utilizado con permiso. Reina-Valera 1960™ es una marca registrada de la American Bible Society, y puede ser usada solamente bajo licencia. '
                     f'Se citan solo los versículos clave de los dos estudios ({n_vers}, menos de {TOPE_RVR}).',
        'aviso_griego': 'Texto griego: SBL Greek New Testament (SBLGNT) © Society of Biblical Literature y Faithlife, CC BY 4.0. '
                        'Números de Strong: Strong\'s Greek Dictionary (OpenScriptures, CC BY-SA).',
    }
    plantilla = open(os.path.join(AQUI, 'plantilla.html'), encoding='utf-8').read()
    js = 'window.DATOS = ' + json.dumps(datos, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
    out = documento_local(plantilla.replace('/*__DATOS__*/', js))
    with open(SALIDA, 'w', encoding='utf-8') as f:
        f.write(out)
    tam = os.path.getsize(SALIDA)
    faltan = E['pj']['faltan'] + E['ap']['faltan'] + E['pj']['faltan_dg'] + E['ap']['faltan_dg']
    print('escrito', SALIDA, f'{tam / 1e6:.2f} MB', '| días', len(datos['dias']), 'de', len(plan),
          '| artículos', len(datos['articulos']), '| diagramas', len(datos['diagramas']),
          ('| en preparación: ' + ', '.join(faltan)) if faltan else '', '| fuentes', len(fuentes),
          '| versículos RVR', n_vers if B.rvr else '0 (sin archivo)', '| lugares en días', len(datos['lugares_dia']))
    if sin_fuente:
        print('AVISO: ids de fuente sin nota extraída:', len(sin_fuente), sin_fuente[:10], file=sys.stderr)


def documento_local(pagina):
    """Incrusta las tipografías (base64) para usarla sin conexión."""
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
    return pagina.replace('/*__TIPOGRAFIAS__*/', '\n'.join(caras))


if __name__ == '__main__':
    main()
