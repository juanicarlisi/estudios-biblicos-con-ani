#!/usr/bin/env python3
"""Arma la app del estudio (un solo HTML) a partir de los datos de trabajo.

Uso: python3 construir.py [salida.html] [--artefacto]
Por defecto arma un documento completo para abrir como archivo (UTF-8, tipografías incrustadas, sin conexión).
Con --artefacto arma la versión para publicar en claude.ai (la plataforma le pone el esqueleto del documento).
Lee: trabajo/plan/plan.json, trabajo/dias/dia_NN.json, trabajo/extracciones/*, trabajo/biblia/rvr1960_genesis.json,
     trabajo/mapas/datos_mapas.json y trabajo/textos/*.json (introducción, cómo usar, fuentes).
"""
import json, glob, os, re, sys, html
sys.path.insert(0, '/home/user/trabajo/scripts')
from insumos_dias import OBRAS_BIBLIO

T = '/home/user/trabajo'
AQUI = os.path.dirname(os.path.abspath(__file__))
ARTEFACTO = '--artefacto' in sys.argv
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
SALIDA = _args[0] if _args else os.path.join(AQUI, '..', 'estudio-genesis.html')
FUENTES_DIR = os.path.join(AQUI, 'tipografias')   # woff2 (latin, latin-ext, hebrew) y su CSS de Google Fonts

COMENTARIOS = {
    'kline': ('Kline', 'Meredith G. Kline, «Génesis», en Nuevo Comentario Bíblico (Casa Bautista de Publicaciones)', 'pág.'),
    'beacon': ('Beacon', 'George Herbert Livingston, «Génesis», Comentario Bíblico Beacon, tomo 1 (Casa Nazarena de Publicaciones)', 'pág.'),
    'cbmh': ('Mundo Hispano', 'Comentario Bíblico Mundo Hispano, tomo 1: Génesis (Editorial Mundo Hispano)', 'pág.'),
    'edersheim': ('Edersheim', 'Alfred Edersheim, Comentario Bíblico Histórico (Editorial Clie)', 'pág.'),
    'macarthur': ('MacArthur', 'John MacArthur, Biblia de Estudio MacArthur (Editorial Portavoz)', 'pág.'),
    'dbmh': ('Diccionario MH', 'Diccionario Bíblico Mundo Hispano (Editorial Mundo Hispano)', 'pág.'),
}

TOLEDOT = [
    ('prologo', 'Prólogo', 'La creación', '1:1–2:3', (1, 1)),
    ('cielos', 'Primera sección', 'Los cielos y la tierra', '2:4–4:26', (2, 4)),
    ('adan', 'Segunda sección', 'Adán', '5:1–6:8', (5, 1)),
    ('noe', 'Tercera sección', 'Noé', '6:9–9:29', (6, 9)),
    ('hijos_noe', 'Cuarta sección', 'Los hijos de Noé', '10:1–11:9', (10, 1)),
    ('sem', 'Quinta sección', 'Sem', '11:10–26', (11, 10)),
    ('tare', 'Sexta sección', 'Taré: la historia de Abraham', '11:27–25:11', (11, 27)),
    ('ismael', 'Séptima sección', 'Ismael', '25:12–18', (25, 12)),
    ('isaac', 'Octava sección', 'Isaac: la historia de Jacob', '25:19–35:29', (25, 19)),
    ('esau', 'Novena sección', 'Esaú', '36:1–37:1', (36, 1)),
    ('jacob', 'Décima sección', 'Jacob: la historia de José', '37:2–50:26', (37, 2)),
]

LUGAR_CLAVES = {
    'ur_sur': ['Ur de los caldeos'], 'haran': ['Harán', 'Padan-aram'], 'siquem': ['Siquem', 'More'], 'betel': ['Bet-el', 'Betel', 'Luz'],
    'hai': ['Hai'], 'hebron': ['Hebrón', 'Mamre', 'Macpela'], 'beerseba': ['Beerseba'], 'gerar': ['Gerar'], 'cades': ['Cades'],
    'shur': ['Shur'], 'lahairoi': ['Beer-lahai-roi'], 'sodoma': ['Sodoma'], 'zoar': ['Zoar'], 'salem': ['Salem'], 'moriah': ['Moriah'],
    'hoba': ['Hoba'], 'damasco': ['Damasco'], 'mahanaim': ['Mahanaim'], 'peniel': ['Peniel', 'Penuel'], 'sucot': ['Sucot'],
    'galaad': ['Galaad', 'Mizpa'], 'belen': ['Efrata', 'Belén'], 'edar': ['Edar'], 'dotan': ['Dotán'], 'adulam': ['Adulam'],
    'timnat': ['Timnat'], 'on': ['de On'], 'gosen': ['Gosén'], 'egipto': ['Egipto'], 'ararat': ['Ararat'], 'babel': ['Babel', 'Sinar'],
    'ninive': ['Nínive'], 'cala': ['Cala'], 'erec': ['Erec'], 'acad': ['Acad'], 'eden': ['Edén'], 'canaan': ['Canaán'],
    'edom': ['Edom', 'Seir'], 'sidon': ['Sidón'], 'gaza': ['Gaza'], 'elam': ['Elam'], 'asiria': ['Asiria'], 'aram': ['Aram'],
}

# Línea de tiempo: años contados desde la creación con las cifras del texto (RVR1960)
PERSONAS = [
    ('Adán', 0, 930, 'Vivió 930 años (5:5)', 'antes'), ('Set', 130, 1042, 'Adán tenía 130 (5:3); vivió 912 (5:8)', 'antes'),
    ('Enós', 235, 1140, 'Set tenía 105 (5:6); vivió 905 (5:11)', 'antes'), ('Cainán', 325, 1235, 'Enós tenía 90 (5:9); vivió 910 (5:14)', 'antes'),
    ('Mahalaleel', 395, 1290, 'Cainán tenía 70 (5:12); vivió 895 (5:17)', 'antes'), ('Jared', 460, 1422, 'Mahalaleel tenía 65 (5:15); vivió 962 (5:20)', 'antes'),
    ('Enoc', 622, 987, 'Jared tenía 162 (5:18); 365 años, y Dios se lo llevó (5:23-24)', 'antes'), ('Matusalén', 687, 1656, 'Enoc tenía 65 (5:21); vivió 969 (5:27)', 'antes'),
    ('Lamec', 874, 1651, 'Matusalén tenía 187 (5:25); vivió 777 (5:31)', 'antes'), ('Noé', 1056, 2006, 'Lamec tenía 182 (5:28); vivió 950 (9:29)', 'antes'),
    ('Sem', 1558, 2158, 'Tenía 100 años dos años después del diluvio (11:10); vivió 600', 'despues'),
    ('Arfaxad', 1658, 2096, 'Sem tenía 100 (11:10); vivió 438 (11:12-13)', 'despues'), ('Sala', 1693, 2126, 'Arfaxad tenía 35 (11:12); vivió 433', 'despues'),
    ('Heber', 1723, 2187, 'Sala tenía 30 (11:14); vivió 464', 'despues'), ('Peleg', 1757, 1996, 'Heber tenía 34 (11:16); vivió 239', 'despues'),
    ('Reu', 1787, 2026, 'Peleg tenía 30 (11:18); vivió 239', 'despues'), ('Serug', 1819, 2049, 'Reu tenía 32 (11:20); vivió 230', 'despues'),
    ('Nacor', 1849, 1997, 'Serug tenía 30 (11:22); vivió 148', 'despues'), ('Taré', 1878, 2083, 'Nacor tenía 29 (11:24); vivió 205 (11:32)', 'despues'),
    ('Abraham', 2008, 2183, 'Nace cuando Taré tiene 130 (ver la nota); vivió 175 (25:7)', 'patriarcas'), ('Sara', 2018, 2145, 'Diez años menor que Abraham (17:17); vivió 127 (23:1)', 'patriarcas'),
    ('Ismael', 2094, 2231, 'Abram tenía 86 (16:16); vivió 137 (25:17)', 'patriarcas'), ('Isaac', 2108, 2288, 'Abraham tenía 100 (21:5); vivió 180 (35:28)', 'patriarcas'),
    ('Jacob', 2168, 2315, 'Isaac tenía 60 (25:26); vivió 147 (47:28)', 'patriarcas'),
    ('José', 2259, 2369, 'Jacob tenía 91 (tenía 130 en Egipto, 47:9, cuando José tenía 39: 41:46 y 45:6); vivió 110 (50:26)', 'patriarcas'),
]
HITOS = [('Diluvio', 1656), ('Llamado de Abram', 2083), ('Jacob a Egipto', 2298)]
FIN = 2369
LINEA_CAP = [  # (desde_cap, hasta_cap, año_desde, año_hasta, texto)
    (1, 2, 0, 0, 'La creación: el comienzo de la cuenta de años.'),
    (3, 4, 0, 235, 'De Adán a Enós: los primeros años de la humanidad.'),
    (5, 5, 0, 1556, 'De Adán a Noé: más de mil quinientos años, según las cifras del texto.'),
    (6, 6, 1536, 1656, 'Los últimos tiempos antes del diluvio.'),
    (7, 8, 1656, 1657, 'El diluvio, en el año 600 de Noé (7:6, 11): el año 1656 de la cuenta.'),
    (9, 9, 1657, 2006, 'Después del diluvio, hasta la muerte de Noé.'),
    (10, 11, 1656, 2083, 'De los hijos de Noé a Taré.'),
    (12, 15, 2083, 2093, 'Abram tiene 75 años al salir de Harán (12:4).'),
    (16, 16, 2093, 2094, 'Nace Ismael: Abram tiene 86 años (16:16).'),
    (17, 21, 2107, 2108, 'Abraham tiene 99 y 100 años: nace Isaac (17:1; 21:5).'),
    (22, 22, 2108, 2145, 'Isaac joven, antes de la muerte de Sara.'),
    (23, 24, 2145, 2148, 'Muere Sara (23:1); Isaac se casa a los 40 (25:20).'),
    (25, 25, 2168, 2183, 'Nacen Esaú y Jacob (Isaac tiene 60) y muere Abraham.'),
    (26, 27, 2168, 2245, 'Isaac en Gerar; Esaú se casa a los 40 (26:34).'),
    (28, 31, 2245, 2265, 'Jacob en Harán: unos veinte años (31:38).'),
    (32, 35, 2265, 2288, 'El regreso de Jacob; muere Isaac a los 180 (35:28).'),
    (36, 36, 2208, 2288, 'Los descendientes de Esaú.'),
    (37, 38, 2276, 2289, 'José tiene 17 años (37:2).'),
    (39, 40, 2276, 2289, 'José esclavo y preso en Egipto.'),
    (41, 41, 2289, 2297, 'José ante Faraón a los 30 (41:46).'),
    (42, 45, 2297, 2298, 'Los años de hambre (45:6).'),
    (46, 47, 2298, 2315, 'Jacob baja a Egipto a los 130 (47:9).'),
    (48, 50, 2315, 2369, 'Mueren Jacob (147 años) y José (110 años).'),
]


def nodo(n, hijos=None, linea=False, nota=''):
    return {'n': n, 'hijos': hijos or [], 'linea': linea, 'nota': nota}


FAMILIAS = [
    {'titulo': 'De Adán a Noé', 'texto': 'Génesis 4 y 5: la línea de Caín y la línea de Set, por la que sigue la promesa.',
     'raiz': nodo('Adán y Eva', [
         nodo('Caín', [nodo('Enoc', [nodo('Irad', [nodo('Mehujael', [nodo('Metusael', [nodo('Lamec', [nodo('Jabal'), nodo('Jubal'), nodo('Tubal-caín'), nodo('Naama')])])])])])]),
         nodo('Abel', nota='muerto por Caín'),
         nodo('Set', [nodo('Enós', [nodo('Cainán', [nodo('Mahalaleel', [nodo('Jared', [nodo('Enoc', [nodo('Matusalén', [nodo('Lamec', [nodo('Noé', linea=True)], True)], True)], True)], True)], True)], True)], True)], True)], True)},
    {'titulo': 'Los hijos de Noé y las naciones', 'texto': 'Génesis 10: algunos de los pueblos que salen de Sem, Cam y Jafet.',
     'raiz': nodo('Noé', [
         nodo('Jafet', [nodo('Gomer'), nodo('Magog'), nodo('Madai'), nodo('Javán'), nodo('Tubal'), nodo('Mesec'), nodo('Tiras')]),
         nodo('Cam', [nodo('Cus', [nodo('Nimrod')]), nodo('Mizraim'), nodo('Fut'), nodo('Canaán')]),
         nodo('Sem', [nodo('Elam'), nodo('Asur'), nodo('Arfaxad', [nodo('Sala', [nodo('Heber', [nodo('Peleg', linea=True), nodo('Joctán')], True)], True)], True), nodo('Lud'), nodo('Aram')], True)], True)},
    {'titulo': 'La familia de Taré', 'texto': 'Génesis 11:27-32; 22:20-24; 24 y 29: de Taré a Rebeca, Lea y Raquel.',
     'raiz': nodo('Taré', [
         nodo('Abram (Abraham)', [nodo('Ismael', nota='hijo de Agar'), nodo('Isaac', nota='hijo de Sara', linea=True), nodo('Hijos de Cetura', nota='25:1-4')], True),
         nodo('Nacor', [nodo('Betuel', [nodo('Rebeca', nota='esposa de Isaac'), nodo('Labán', [nodo('Lea'), nodo('Raquel')])])]),
         nodo('Harán', [nodo('Lot', [nodo('Moab'), nodo('Ben-ammi')]), nodo('Milca', nota='esposa de Nacor'), nodo('Isca')])], True)},
    {'titulo': 'Los hijos de Jacob', 'texto': 'Génesis 29:31–30:24; 35:16-18; 41:50-52: las doce tribus, por madre.',
     'raiz': nodo('Jacob (Israel)', [
         nodo('Lea', [nodo('Rubén'), nodo('Simeón'), nodo('Leví'), nodo('Judá', linea=True), nodo('Isacar'), nodo('Zabulón'), nodo('Dina')]),
         nodo('Bilha', [nodo('Dan'), nodo('Neftalí')], nota='sierva de Raquel'),
         nodo('Zilpa', [nodo('Gad'), nodo('Aser')], nota='sierva de Lea'),
         nodo('Raquel', [nodo('José', [nodo('Manasés'), nodo('Efraín')]), nodo('Benjamín')])], True)},
    {'titulo': 'Isaac, Esaú y Judá', 'texto': 'Génesis 25:19-26 y 38: de Isaac a Fares, por quien sigue la línea de Judá.',
     'raiz': nodo('Isaac y Rebeca', [nodo('Esaú (Edom)'), nodo('Jacob', [nodo('Judá', [nodo('Er'), nodo('Onán'), nodo('Sela'), nodo('Fares', nota='hijo de Tamar', linea=True), nodo('Zara', nota='hijo de Tamar')], True)], True)], True)},
]


def idx_toledot(desde):
    c, v = map(int, desde.split(':'))
    actual = TOLEDOT[0][0]
    for t in TOLEDOT:
        if (c, v) >= t[4]:
            actual = t[0]
    return actual


# etiquetas cortas que el apellido final no resuelve bien (apellidos compuestos, obras colectivas)
ETIQUETAS = [
    (r'^comentario b[ií]blico mundo hispano', 'Mundo Hispano'), (r'editores generales: juan carlos cevallos', 'Mundo Hispano'),
    (r'p[ée]rez millos', 'Pérez Millos'), (r'de haan', 'De Haan'), (r'juan c\. de la cruz', 'De la Cruz'),
    (r'^antonio cruz', 'A. Cruz'), (r'coleman jr', 'Coleman'), (r'^varios \(plumer', 'Portavoz de la Gracia'),
    (r'^varios \(jeremy pierre', '9Marcas'), (r'^varios autores \(compilaci', 'Antología'),
    (r'^elizabeth george', 'E. George'), (r'^jim george', 'J. George'), (r'^joel b\. green', 'J. B. Green'),
    (r'^les thompson', 'L. Thompson'), (r'^w\. oscar thompson', 'O. Thompson'),
]


def etiqueta_ref3(autor, ape):
    for pat, et in ETIQUETAS:
        if re.search(pat, autor, re.I):
            return et
    return ape


def notas_por_id():
    out = {}
    for f in glob.glob(f'{T}/extracciones/biblio/*.json'):
        b = os.path.basename(f)[:-5]; pref = b.split('_')[0]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            ab, nombre, _ = COMENTARIOS.get(pref, (pref, pref, ''))
            pag = re.sub(r'^\w+\s*\|\s*', '', str(n.get('pagina', ''))).replace('PÁGINA PDF', 'pág. PDF')
            out[f'{b}#{i}'] = [ab, nombre, pag]
    for f in glob.glob(f'{T}/extracciones/ref3/*.json'):
        b = os.path.basename(f)[:-5]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            autor = (n.get('autor') or '').strip(); obra = (n.get('obra') or '').strip()
            ape = re.split(r'\s+y\s+|,|\(', autor)[0].strip().split()[-1] if autor else 'Referencia'
            if n.get('archivo') in OBRAS_BIBLIO:
                autor, obra, ape = OBRAS_BIBLIO[n['archivo']]
            ape = etiqueta_ref3(autor, ape)
            m = re.search(r'citado por ([^)]+)\)', autor)
            if autor.lower().startswith('autor no identificado') and m:
                ape = m.group(1).split()[-1]; autor = f'Cita recogida por {m.group(1)}'
            out[f'{b}#{i}'] = [ape, f'{autor}, {obra}', f"pág. PDF {n.get('pagina', '')}".replace('pág. PDF pág. PDF', 'pág. PDF')]
    return out


def main():
    plan = json.load(open(f'{T}/plan/plan.json'))
    for p in plan:
        p['toledot'] = idx_toledot(p['desde'])
    rvr = json.load(open(f'{T}/biblia/rvr1960_genesis.json'))['texto']
    dias = {}
    for f in sorted(glob.glob(f"{T}/dias/{os.environ.get('DIAS', 'dia_')}*.json")):   # DIAS=borrador_ para probar con borradores
        d = json.load(open(f)); dias[d['dia']] = d
    meta_arts = json.load(open(f'{T}/plan/articulos.json'))
    articulos = {}
    for a in meta_arts:
        f = f"{T}/articulos/art_{a['id']}.json"
        if os.path.exists(f):
            x = json.load(open(f))
            for v in x.get('versiculos', []):
                v['ref'] = re.sub(r'^(Gn|Gén|Génesis)\.?\s*', '', v['ref'].strip())
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
    # versículos clave (RVR1960; menos de 500 versículos en total)
    clave = {}
    def poner(ref):
        m = re.match(r'(\d+):(\d+)(?:-(\d+))?$', ref.replace(' ', ''))
        if m:
            c, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2))
            if 1 <= c <= 50 and b - a < 6:
                clave[ref] = ' '.join(rvr[str(c)][str(v)] for v in range(a, b + 1) if str(v) in rvr[str(c)])
    for d in dias.values():
        poner(d['versiculo_clave']['ref'])
    for x in articulos.values():
        for v in x.get('versiculos', []):
            poner(v['ref'])
    n_vers = sum(1 + (int(m.group(2)) - int(m.group(1)) if (m := re.search(r':(\d+)-(\d+)$', r)) else 0) for r in clave)
    assert n_vers <= 500, f'demasiados versículos RVR citados: {n_vers}'
    # lugares por día (según el texto del pasaje)
    lugares_dia = {}
    V = [len(rvr[str(c)]) for c in range(1, 51)]
    for p in plan:
        c1, v1 = map(int, p['desde'].split(':')); c2, v2 = map(int, p['hasta'].split(':'))
        txt = ' '.join(t for c in range(c1, c2 + 1) for v, t in rvr[str(c)].items() if (c, int(v)) >= (c1, v1) and (c, int(v)) <= (c2, v2))
        ids = [k for k, claves in LUGAR_CLAVES.items() if any(re.search(r'\b' + re.escape(w) + r'\b', txt) for w in claves)]
        if 'ur_sur' in ids:
            ids.append('ur_norte')
        lugares_dia[p['dia']] = ids
    linea_dia = {}
    for p in plan:
        c = int(p['desde'].split(':')[0])
        for a, b, y0, y1, t in LINEA_CAP:
            if a <= c <= b:
                linea_dia[p['dia']] = {'texto': t, 'desde': round(100 * y0 / FIN, 2), 'hasta': round(100 * y1 / FIN, 2)}
                break
    advert_ids = [i for i in ('kline_02#45', 'kline_03#10', 'kline_03#12', 'macarthur_02#25', 'beacon_02#86', 'cbmh_06#48') if i in todas]
    usados.update(advert_ids)
    linea = {'personas': [{'nombre': n, 'nace': a, 'muere': b, 'dato': t, 'grupo': g} for n, a, b, t, g in PERSONAS],
             'hitos': [{'nombre': n, 'anio': a} for n, a in HITOS],
             'explicacion': 'Las barras muestran cuántos años vivió cada uno y cómo se superponen sus vidas, sumando las edades que da el texto (por ejemplo, «vivió Adán ciento treinta años, y engendró…», 5:3). Para Abraham se toma que nació cuando Taré tenía 130 años: es lo que resulta de 11:32 y 12:4 junto con Hechos 7:4, como explica Kline.',
             'advertencia': 'Kline, Beacon, Mundo Hispano y MacArthur coinciden en que las genealogías de Génesis 5 y 11 son selectivas o representativas, no completas: pueden saltar generaciones. Por eso estas cuentas sirven para ver el orden y la duración de las vidas tal como el texto las presenta, pero no para fechar la creación ni el diluvio.',
             'fuentes': advert_ids}
    fuentes = {i: todas[i] for i in usados if i in todas}
    # versículos de cada sección del libro (para el diagrama de la estructura)
    orden = [(c, int(v)) for c in range(1, 51) for v in sorted(map(int, rvr[str(c)]))]
    versos_toledot = {}
    for k, t in enumerate(TOLEDOT):
        fin = TOLEDOT[k + 1][4] if k + 1 < len(TOLEDOT) else (51, 0)
        versos_toledot[t[0]] = sum(1 for x in orden if t[4] <= x < fin)
    ref_obras = sorted({tuple(todas[i][1].split(', ', 1)) for i in usados if i in todas and i.startswith(('r1_', 'r2_'))})
    textos = {}
    for f in glob.glob(f'{T}/textos/*.json'):
        textos[os.path.basename(f)[:-5]] = json.load(open(f))
    textos.setdefault('introduccion', {'ojo': 'Antes de empezar', 'titulo': 'Introducción a Génesis', 'html': '<p>La introducción se está escribiendo con el material de la biblioteca: título, autor y fecha, propósito, estructura, temas y cómo apunta a Cristo.</p>'})
    textos.setdefault('como-usar', {'ojo': 'Guía', 'titulo': 'Cómo usar el estudio', 'html': '<p>Cada día: lean el pasaje en su Biblia o con el botón «Leer el pasaje», después recorran el estudio y terminen con las preguntas y la oración.</p>'})
    textos.setdefault('fuentes', {'html': '<p>Cada afirmación del estudio lleva etiquetas con sus fuentes: tocándolas se ve la obra y la página.</p>'})
    datos = {
        'plan': plan,
        'toledot': [{'id': a, 'etiqueta': b, 'titulo': c, 'rango': d, 'inicio': f'{e[0]}:{e[1]}', 'versos': versos_toledot[a]} for a, b, c, d, e in TOLEDOT],
        'articulos': articulos, 'articulos_orden': [{k: a[k] for k in ('id', 'grupo', 'titulo', 'parte', 'rango') if k in a} for a in meta_arts],
        'dias': dias, 'fuentes': fuentes, 'rvr': clave,
        'mapas': json.load(open(f'{T}/mapas/datos_mapas.json')),
        'lugares_dia': lugares_dia, 'linea_dia': linea_dia, 'linea': linea, 'familias': FAMILIAS, 'textos': textos,
        'obras': {'comentarios': [[v[0], v[1]] for v in COMENTARIOS.values()], 'referencia': [list(o) for o in ref_obras]},
        'aviso_rvr': 'Texto bíblico: Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.',
    }
    plantilla = open(os.path.join(AQUI, 'plantilla.html')).read()
    js = 'window.DATOS = ' + json.dumps(datos, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
    out = plantilla.replace('/*__DATOS__*/', js)
    if not ARTEFACTO:
        out = documento_local(out)
    open(SALIDA, 'w').write(out)
    print('escrito', os.path.abspath(SALIDA), f'{len(out)/1e6:.2f} MB', '| días', len(dias), '| artículos', len(articulos), '| fuentes', len(fuentes), '| versículos RVR', n_vers)


def documento_local(pagina):
    """Envuelve la página en un documento completo e incrusta las tipografías para usarla sin conexión."""
    import base64
    css = open(os.path.join(FUENTES_DIR, 'fuentes.css')).read()
    # las fuentes variables usan el mismo archivo para varios grosores: una sola cara con rango de grosor
    grupos = {}
    for subset, cara in re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
        if subset not in ('latin', 'latin-ext', 'hebrew'):
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
