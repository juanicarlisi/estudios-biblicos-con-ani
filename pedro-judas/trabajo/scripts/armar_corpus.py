#!/usr/bin/env python3
"""Arma los bloques de lectura de 1 Pedro a Judas (texto con marcas de página) a partir de los libros extraídos.

Cuatro familias (espejo de apocalipsis/trabajo/scripts/armar_corpus.py):
  A) comentarios completos por libro (se leen enteros): MATERIAL SOPORTE 60-65 (MacArthur, Kistemaker, McGee) y los tramos de
     1P-Jd de los tomos generales (Beacon t. 10, Mundo Hispano t. 23 y 24, Nuevo Comentario Bíblico, Biblia de Estudio MacArthur).
     Un bloque por obra y libro (2 y 3 Juan juntos): el prefijo del id dice obra y libro (p. ej. kis1p_02, bea23j_01).
  B) Diccionario Bíblico Mundo Hispano: páginas con 2+ citas <60CCVV>..<65CCVV> (60=1P, 61=2P, 62=1J, 63=2J, 64=3J, 65=Jd).
  C) libros de REFERENCIA3 (solo categoría A de la clasificación): tramos con señal fuerte (r1) y ventanas alrededor de citas (r2),
     según SCRATCH/indice_ref3_pj.json (indice_pedro_judas.py).
  D) REFERENCIA4 (SCRATCH/ref4_triage.json, solo categoría A, nivel alto o medio, que toquen estos libros): comentarios dedicados
     se leen enteros (o en su tramo); el resto, como C (r4a tramos, r4b ventanas) con SCRATCH/indice_ref4_pj.json.
Uso: armar_corpus.py [--solo A,B,C,D]   (lee SCRATCH, escribe SCRATCH/pj_bloques/*.txt y SCRATCH/pj_bloques/_indice.json)
No lanza la extracción.
"""
import json, os, re, hashlib, sys, subprocess, collections
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
OUT = S + '/pj_bloques'; os.makedirs(OUT, exist_ok=True)
AQUI = os.path.dirname(os.path.abspath(__file__))
MAX = 90000
sys.path.insert(0, AQUI)
from indice_pedro_judas import citas, RE_F, puntaje
SEIS = {'1P', '2P', '1J', '2J', '3J', 'Jd'}

RUIDO = [r'Descargado de http://www\.yahwehjireh\.org', r'IGLESIA CRISTIANA MINISTERIO DEL REINO DE CRISTO\s*Pastor Uriel Campos',
         r'Elaborado por el Pastor Uriel Campos', r'Web: http://ucampos\.jimdo\.com', r'Correo: ucampos074@yahoo\.com',
         r'Escanee el código para ver más productos', r'atravesdelabiblia\.org', r'COMENTARIO BIBLICO HIS[A]?PANOAMERICANO']
def limpiar(t):
    for r in RUIDO: t = re.sub(r, '', t)
    t = re.sub(r'[ \t\xa0]{2,}', ' ', t)
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()
def pags(path): return open(path, errors='ignore').read().split('\f')

T = S + '/txt/'
BEACON = 'Comentario Bíblico Beacon, tomo 10: Hebreos hasta Apocalipsis (Casa Nazarena de Publicaciones)'
CBMH23 = 'Comentario Bíblico Mundo Hispano, tomo 23: Hebreos, Santiago, 1 y 2 Pedro, Judas (Editorial Mundo Hispano)'
CBMH24 = 'Comentario Bíblico Mundo Hispano, tomo 24: 1, 2 y 3 Juan, Apocalipsis (Editorial Mundo Hispano)'
NCB = 'Nuevo Comentario Bíblico (Clie); el PDF se rotula «Biblia Matthew Henry», pero el texto es del Nuevo Comentario Bíblico'
MBIB = 'John MacArthur, Biblia de Estudio MacArthur (Portavoz): introducción y notas de '
CB24 = S + '/ref3txt/Escatologia y Ultimos Tiempos__Apocalipsis 1, 2, 3.pdf.txt'
# id -> txt, páginas PDF desde-hasta (inclusive), obra, libros. Rangos verificados con los encabezados de cada libro (09-11-2026).
FAM_A = {
    'mac1p': dict(txt=T + 'pj_macarthur_pe.txt', desde=5, hasta=202, libros='1P', obra='John MacArthur, Comentario MacArthur del Nuevo Testamento: 1 y 2 Pedro (Portavoz)'),
    'mac2p': dict(txt=T + 'pj_macarthur_pe.txt', desde=203, hasta=293, libros='2P', obra='John MacArthur, Comentario MacArthur del Nuevo Testamento: 1 y 2 Pedro (Portavoz)'),
    'kis1p': dict(txt=T + 'pj_kistemaker_pe.txt', desde=7, hasta=177, libros='1P', obra='Simon J. Kistemaker, Comentario al Nuevo Testamento: 1 y 2 Pedro y Judas (Libros Desafío)'),
    'kis2p': dict(txt=T + 'pj_kistemaker_pe.txt', desde=178, hasta=289, libros='2P', obra='Simon J. Kistemaker, Comentario al Nuevo Testamento: 1 y 2 Pedro y Judas (Libros Desafío)'),
    'kisjd': dict(txt=T + 'pj_kistemaker_pe.txt', desde=290, hasta=339, libros='Jd', obra='Simon J. Kistemaker, Comentario al Nuevo Testamento: 1 y 2 Pedro y Judas (Libros Desafío)'),
    'mcg2p': dict(txt=T + 'pj_mcgee_2p.txt', libros='2P', obra='J. Vernon McGee, Comentario bíblico «A través de la Biblia»: 2 Pedro (transcripción de los programas de radio)'),
    'mac1j': dict(txt=T + 'pj_macarthur_jn.txt', desde=5, hasta=149, libros='1J', obra='John MacArthur, Comentario MacArthur del Nuevo Testamento: 1, 2 y 3 Juan (Portavoz)'),
    'mac23j': dict(txt=T + 'pj_macarthur_jn.txt', desde=150, hasta=182, libros='2J 3J', obra='John MacArthur, Comentario MacArthur del Nuevo Testamento: 1, 2 y 3 Juan (Portavoz)'),
    'kis1j': dict(txt=T + 'pj_hendriksen_jn.txt', desde=160, hasta=308, libros='1J', obra='Simon J. Kistemaker, Comentario al Nuevo Testamento: Santiago y 1, 2 y 3 Juan (Libros Desafío; serie de W. Hendriksen)'),
    'kis23j': dict(txt=T + 'pj_hendriksen_jn.txt', desde=309, hasta=333, libros='2J 3J', obra='Simon J. Kistemaker, Comentario al Nuevo Testamento: Santiago y 1, 2 y 3 Juan (Libros Desafío; serie de W. Hendriksen)'),
    'mcg2j': dict(txt=T + 'pj_mcgee_2j.txt', libros='2J', obra='J. Vernon McGee, Comentario bíblico «A través de la Biblia»: 2 Juan (transcripción de los programas de radio)'),
    # Judas de MacArthur: texto digital de REFERENCIA4 (id 118); si falta, el OCR del escaneo de MATERIAL SOPORTE 65
    'macjd': dict(txt=T + 'pj_r4_118.txt', alt=T + 'pj_macarthur_jd.txt', libros='Jd', obra='John MacArthur, Comentario MacArthur del Nuevo Testamento: Judas (Portavoz)'),
    'bea1p': dict(txt=T + 'Comentario_Biblico_B.txt', desde=172, hasta=211, libros='1P', obra='Roy S. Nicholson, «Primera Epístola de Pedro», ' + BEACON),
    'bea2p': dict(txt=T + 'Comentario_Biblico_B.txt', desde=212, hasta=232, libros='2P', obra='Eldon R. Fuhrman, «Segunda Epístola de Pedro», ' + BEACON),
    'bea1j': dict(txt=T + 'Comentario_Biblico_B.txt', desde=232, hasta=273, libros='1J', obra='Harvey J. S. Blaney, «Primera Epístola de Juan», ' + BEACON),
    'bea23j': dict(txt=T + 'Comentario_Biblico_B.txt', desde=274, hasta=281, libros='2J 3J', obra='Harvey J. S. Blaney, «Segunda y Tercera Epístolas de Juan», ' + BEACON),
    'beajd': dict(txt=T + 'Comentario_Biblico_B.txt', desde=282, hasta=306, libros='Jd', obra='Delbert R. Rose, «La Epístola de Judas», ' + BEACON),
    'cbmh1p': dict(txt=T + 'pj_cbmh_pe.txt', desde=224, hasta=278, libros='1P', obra='Cecilio McConnell (exposición) y Hebert Palomino (ayudas prácticas), «1 Pedro», ' + CBMH23),
    'cbmh2p': dict(txt=T + 'pj_cbmh_pe.txt', desde=279, hasta=301, libros='2P', obra='Alberto F. Roldán (exposición) y Rubén O. Zorzoli (ayudas prácticas), «2 Pedro», ' + CBMH23),
    'cbmhjd': dict(txt=T + 'pj_cbmh_pe.txt', desde=302, hasta=321, libros='Jd', obra='Sergio Valle Ruiz (exposición) y Guillermo Graves (ayudas prácticas), «Judas», ' + CBMH23),
    'cbmh1j': dict(txt=CB24, desde=19, hasta=67, libros='1J', obra='Benjamín Bedford (exposición y ayudas prácticas), «1 Juan», ' + CBMH24),
    'cbmh23j': dict(txt=CB24, desde=68, hasta=96, libros='2J 3J', obra='Guillermo Catalán y Betty de Missena («2 Juan»), Ramón Salazar y Jorge Ángel Rodríguez («3 Juan»), ' + CBMH24),
    'ncb1p': dict(txt=S + '/corpus/henry.txt', desde=141, hasta=149, libros='1P', obra='«1 Pedro», ' + NCB),
    'ncb2p': dict(txt=S + '/corpus/henry.txt', desde=150, hasta=157, libros='2P', obra='«2 Pedro», ' + NCB),
    'ncb1j': dict(txt=S + '/corpus/henry.txt', desde=158, hasta=166, libros='1J', obra='«1 Juan», ' + NCB),
    'ncb23j': dict(txt=S + '/corpus/henry.txt', desde=167, hasta=168, libros='2J 3J', obra='«2 y 3 Juan», ' + NCB),
    'ncbjd': dict(txt=S + '/corpus/henry.txt', desde=169, hasta=172, libros='Jd', obra='«Judas», ' + NCB),
    'mbib1p': dict(txt=S + '/corpus/macarthur_biblia.txt', desde=3244, hasta=3287, libros='1P', obra=MBIB + '1 Pedro'),
    'mbib2p': dict(txt=S + '/corpus/macarthur_biblia.txt', desde=3287, hasta=3319, libros='2P', obra=MBIB + '2 Pedro'),
    'mbib1j': dict(txt=S + '/corpus/macarthur_biblia.txt', desde=3320, hasta=3362, libros='1J', obra=MBIB + '1 Juan'),
    'mbib23j': dict(txt=S + '/corpus/macarthur_biblia.txt', desde=3362, hasta=3375, libros='2J 3J', obra=MBIB + '2 y 3 Juan'),
    'mbibjd': dict(txt=S + '/corpus/macarthur_biblia.txt', desde=3375, hasta=3389, libros='Jd', obra=MBIB + 'Judas'),
}
# Descartados a propósito (documentado): duplicados de MATERIAL SOPORTE («1 y 2 Pedro - John MacArthur» = mac1p/mac2p; «1,2y3 Juan» y
# «22 I II y III JUAN» = otra edición de mac1j; «Comentario Bíblico Moody - 2 Juan» = tramo del Moody NT completo de REFERENCIA4) y
# «Desafíos para jóvenes: Juan» (Tosoni; devocional sobre el Evangelio de Juan, no sobre 3 Juan).

# 1 Pedro y 1 Juan se citan mucho de paso en libros de teología: umbrales más altos que en Apocalipsis (6 y cualquier señal)
UMBRAL_R1 = float(os.environ.get('UMBRAL_R1', 9)); MIN_R2 = float(os.environ.get('MIN_R2', 6))
indice = []
def volcar(id_, items, obra, libros=''):
    """items: [(rotulo_pagina, texto)] -> bloques de <= MAX caracteres"""
    cur = ''; n = 0
    def cerrar():
        nonlocal cur, n
        if cur.strip():
            n += 1; fn = f'{OUT}/{id_}_{n:02d}.txt'
            open(fn, 'w').write(f'# {obra}\n' + (f'# Libros: {libros}\n' if libros else '') + '\n' + cur)
            indice.append({'id': f'{id_}_{n:02d}', 'archivo': fn, 'obra': obra, 'libros': libros, 'chars': len(cur)})
        cur = ''
    for rot, txt in items:
        b = f'=== [{id_} | {rot}] ===\n{txt}\n\n'
        if len(cur) + len(b) > MAX and cur: cerrar()
        cur += b
    cerrar()

def leer_entero(id_, d):
    txt = d['txt']
    if (not os.path.exists(txt) or os.path.getsize(txt) < 2000) and d.get('alt'): txt = d['alt']
    if not os.path.exists(txt) or os.path.getsize(txt) < 2000:
        print('FALTA', id_, txt); return
    P = pags(txt); desde = d.get('desde', 1); hasta = min(d.get('hasta') or len(P), len(P))
    items = []
    for n in range(desde, hasta + 1):
        t = limpiar(P[n - 1])
        if len(t) > 80: items.append((f'pág. PDF {n}', t))
    volcar(id_, items, d['obra'], d.get('libros', ''))

def fam_a():
    for id_, d in FAM_A.items(): leer_entero(id_, d)

def fam_b():
    items = []
    for vol, fn in (('I', 'dbmh1'), ('II', 'dbmh2')):
        P = pags(f'{S}/corpus/{fn}.txt')
        for n, p in enumerate(P, 1):
            if len(re.findall(r'<6[0-5]\d{4}>', p)) >= 2: items.append((f'vol. {vol} pág. PDF {n}', limpiar(p)))
    volcar('dbmh', items, 'Diccionario Bíblico Mundo Hispano (Editorial Mundo Hispano): páginas que citan 1 Pedro a Judas '
           '(<60CCVV> = 1 Pedro CC:VV; 61 = 2 Pedro; 62 = 1 Juan; 63 = 2 Juan; 64 = 3 Juan; 65 = Judas)')
    print('dbmh páginas', len(items))

def tramos(k, rel, txt, pags_idx, umbral=UMBRAL_R1, min_r2=MIN_R2):
    """Tramos de páginas fuertes seguidas (t1) y ventanas de ±6 líneas alrededor de citas o menciones (t2)."""
    P = txt.split('\f'); sc = {x['pag']: x['score'] for x in pags_idx}
    fuertes = sorted(p for p, s in sc.items() if s >= umbral and p <= len(P) and len(P[p - 1]) < 12000)
    runs = []; cur = []
    for p in fuertes:
        if cur and p == cur[-1] + 1: cur.append(p)
        else:
            if cur: runs.append(cur)
            cur = [p]
    if cur: runs.append(cur)
    usadas = set(); t1 = []; t2 = []
    for r in runs:
        if len(r) >= 3 or (len(r) == 2 and sum(sc[p] for p in r) >= 24):
            usadas.update(r)
            t1.append({'k': k, 'rel': rel, 'pags': r, 'texto': '\n'.join(f'--- [pág. PDF {p}] ---\n' + limpiar(P[p - 1]) for p in r)})
    for pn, p in enumerate(P, 1):
        if pn in usadas or sc.get(pn, 0) < min_r2: continue
        lines = p.split('\n'); marcas = [i for i, l in enumerate(lines) if citas(l) or len(RE_F.findall(l)) >= 2]
        if not marcas: continue
        win = set()
        for i in marcas: win.update(range(max(0, i - 6), min(len(lines), i + 7)))
        segs = []; cur = []
        for j in sorted(win):
            if cur and j != cur[-1] + 1: segs.append(cur); cur = []
            cur.append(j)
        if cur: segs.append(cur)
        for s_ in segs:
            t = ' '.join(lines[j].strip() for j in s_)
            if len(t) > 250: t2.append({'k': k, 'rel': rel, 'pag': pn, 'texto': t[:3000]})
    return t1, t2

def vol(items, pref, meta, rotulo):
    cur = ''; n = 0; out = []
    for it in sorted(items, key=lambda x: (x['k'], x.get('pags', [x.get('pag')])[0])):
        a, t = meta(it)
        if 'pags' in it: b = f"\n##### OBRA: {t} | AUTOR: {a} | ARCHIVO: {it['rel']} | páginas PDF {it['pags'][0]}-{it['pags'][-1]}\n{it['texto']}\n"
        else: b = f"\n##### OBRA: {t} | AUTOR: {a} | ARCHIVO: {it['rel']} | pág. PDF {it['pag']} (fragmento)\n{it['texto']}\n"
        b = b[:MAX]
        if len(cur) + len(b) > MAX and cur: out.append(cur); cur = ''
        cur += b
    if cur: out.append(cur)
    for i, t in enumerate(out, 1):
        fn = f'{OUT}/{pref}_{i:03d}.txt'; open(fn, 'w').write(t)
        indice.append({'id': f'{pref}_{i:03d}', 'archivo': fn, 'obra': rotulo, 'libros': '', 'chars': len(t)})

# comentarios de Apocalipsis o ya leídos enteros en A (no se repiten en C)
EXCL3 = ['Apocalipsis - John MacArthur', 'Apocalipsis - Clarence Larkin', 'Apocalipsis 1, 2, 3', 'Apocalipsis - Evis Carballosa']
def fam_c():
    cl = {x['path']: x for x in json.load(open('/home/user/estudios-biblicos-con-ani/genesis/trabajo/clasificacion/clasificacion.json'))}
    fi = S + '/indice_ref3_pj.json'
    if not os.path.exists(fi):
        subprocess.run([sys.executable, AQUI + '/indice_pedro_judas.py', S + '/lista_ref3.json', fi], check=True, capture_output=True)
    idx = json.load(open(fi))
    vistos = set(); t1 = []; t2 = []; fuera = collections.Counter()
    for k, v in idx.items():
        rel = k[5:]
        if any(x in rel for x in EXCL3): fuera['ya en A o Apocalipsis'] += 1; continue
        c = cl.get(rel)
        if not c or c.get('categoria') != 'A': fuera['no es categoría A' if c else 'sin clasificar'] += 1; continue
        if not v['paginas']: continue
        txt = open(v['txt'], errors='ignore').read()
        h = hashlib.md5(re.sub(r'\s+', '', txt[50000:80000]).encode()).hexdigest()
        if h in vistos: fuera['duplicado'] += 1; continue
        vistos.add(h)
        a, b = tramos(k, rel, txt, v['paginas']); t1 += a; t2 += b
    print('REF3 descartados:', dict(fuera))
    print('r1 tramos', len(t1), sum(len(x['texto']) for x in t1), '| r2 ventanas', len(t2), sum(len(x['texto']) for x in t2))
    def meta(it):
        l = cl.get(it['rel'], {}); return l.get('autor', '?'), l.get('titulo') or it['rel'].split('/')[-1]
    vol(t1, 'r1', meta, 'libros de REFERENCIA3 (fragmentos rotulados)'); vol(t2, 'r2', meta, 'libros de REFERENCIA3 (fragmentos rotulados)')

# REFERENCIA4. Comentarios dedicados que se leen enteros (o en su tramo), con texto extraído sin -layout (SCRATCH/txt/pj_r4_<id>.txt);
# id de ref4_triage -> (prefijo, desde, hasta, libros, obra). El resto de los seleccionados va por tramos y ventanas.
R4_ENTEROS = {
    2: ('mhenry', 1058, 1082, '1P 2P 1J 2J 3J Jd', 'Matthew Henry, Comentario Bíblico (completo): 1 Pedro a Judas'),
    225: ('moodynt', 493, 542, '1P 2P 1J 2J 3J Jd', 'Comentario Bíblico Moody: Nuevo Testamento (Portavoz): 1 Pedro a Judas'),
    111: ('nunez2p', None, None, '2P Jd', 'Miguel Núñez, 2 Pedro y Judas para ti'),
    119: ('mcgjd', None, None, 'Jd', 'J. Vernon McGee, Comentario bíblico «A través de la Biblia»: Judas (transcripción de los programas de radio)'),
    125: ('rich1j', None, None, '1J', 'Lawrence O. Richards, Comentario Bíblico del Maestro: 1 Juan'),
    133: ('deirosjd', 144, 202, 'Jd', 'Pablo Alberto Deiros, Santiago y Judas (Comentario Bíblico Hispanoamericano): Judas'),
}
# ya cubiertos: en A (MATERIAL SOPORTE y Biblia MacArthur; 118 = texto de macjd) o duplicados de moodynt (102, 120, 122)
R4_CUBIERTOS = {5, 12, 102, 104, 105, 106, 114, 116, 117, 118, 120, 122, 128, 135, 142}
def fam_d():
    ft = S + '/ref4_triage.json'
    if not os.path.exists(ft): print('sin ref4_triage.json: familia D omitida'); return
    tri = [x for x in json.load(open(ft)) if x.get('categoria') == 'A' and x.get('nivel') in ('alto', 'medio') and SEIS & set(x.get('libros', []))]
    lista = {}
    for x in tri:
        i = x['id']
        if i in R4_CUBIERTOS: continue
        if i in R4_ENTEROS:
            pref, a, b, libros, obra = R4_ENTEROS[i]
            src = f'{T}pj_r4_{i}.txt'
            if not os.path.exists(src):   # se extrae sin -layout (las dos columnas quedan en orden)
                ruta = '/home/user/libros-referencia4/' + x['ruta']
                if os.path.exists(ruta): subprocess.run(['pdftotext', ruta, src], capture_output=True)
            leer_entero(pref, dict(txt=src, desde=a or 1, hasta=b, libros=libros, obra=obra + f" [REFERENCIA4 id {i}; {x.get('autor', '')}]"))
        else:
            lista[str(i)] = x
    # temáticos: índice propio y tramos/ventanas
    fi = S + '/indice_ref4_pj.json'
    L = [{'id': k, 'txt': f'{S}/ref4txt/{k}.txt', 'etiqueta': x['ruta']} for k, x in lista.items()]
    json.dump(L, open(S + '/lista_ref4_pj.json', 'w'), ensure_ascii=False)
    subprocess.run([sys.executable, AQUI + '/indice_pedro_judas.py', S + '/lista_ref4_pj.json', fi], check=True, capture_output=True)
    idx = json.load(open(fi)); t1 = []; t2 = []; vistos = set()
    for k, v in idx.items():
        txt = open(v['txt'], errors='ignore').read()
        h = hashlib.md5(re.sub(r'\s+', '', txt[50000:80000]).encode()).hexdigest()
        if h in vistos and len(txt) > 80000: continue
        vistos.add(h)
        a, b = tramos(k, lista[k]['ruta'], txt, v['paginas']); t1 += a; t2 += b
    print('REF4 temáticos', len(lista), '| r4a tramos', len(t1), sum(len(x['texto']) for x in t1), '| r4b ventanas', len(t2), sum(len(x['texto']) for x in t2))
    def meta(it):
        x = lista[it['k']]; return x.get('autor', '?'), x['ruta'].split('/')[-1]
    vol(t1, 'r4a', meta, 'libros de REFERENCIA4 (fragmentos rotulados)'); vol(t2, 'r4b', meta, 'libros de REFERENCIA4 (fragmentos rotulados)')

if __name__ == '__main__':
    fams = (sys.argv[sys.argv.index('--solo') + 1] if '--solo' in sys.argv else 'A,B,C,D').split(',')
    viejo = []
    if os.path.exists(OUT + '/_indice.json') and len(fams) < 4:   # rearmar solo algunas familias: conservar el resto del índice
        fam_de = lambda i: 'B' if i.startswith('dbmh') else 'C' if re.match(r'r[12]_', i) else 'D' if re.match(r'r4[ab]_', i) or i.split('_')[0] in {v[0] for v in R4_ENTEROS.values()} else 'A'
        todos = json.load(open(OUT + '/_indice.json'))
        viejo = [x for x in todos if fam_de(x['id']) not in fams]
        for x in todos:
            if x not in viejo and os.path.exists(x['archivo']): os.remove(x['archivo'])
    elif len(fams) == 4:   # armado completo: se borran los bloques anteriores (solo los de Pedro-Judas)
        for f in os.listdir(OUT):
            if f.endswith('.txt'): os.remove(os.path.join(OUT, f))
    for f in fams: {'A': fam_a, 'B': fam_b, 'C': fam_c, 'D': fam_d}[f]()
    json.dump(viejo + indice, open(OUT + '/_indice.json', 'w'), ensure_ascii=False, indent=0)
    c = collections.Counter(i['id'].split('_')[0] for i in viejo + indice)
    print(len(viejo + indice), 'bloques', sum(i['chars'] for i in viejo + indice), 'chars'); print(dict(c))
