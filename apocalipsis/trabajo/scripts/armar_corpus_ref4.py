#!/usr/bin/env python3
"""Arma los bloques de lectura de Apocalipsis (texto con marcas de página) a partir del material NUEVO de REFERENCIA4.

Imita armar_corpus.py (mismos volcar(), limpiar(), MAX y rótulos «=== [id | pág. PDF N] ===»; mismo puntaje de
indice_apocalipsis.py para elegir páginas). Tres familias:
  A) libros enteros sobre Apocalipsis o el fin (se leen completos)
  B) libros amplios: solo páginas con señal (puntaje >= 3, o ventana de ±1 página alrededor de una cita explícita)
  C) comentarios generales (Matthew Henry y Comentario Bíblico Moody NT): solo la sección de Apocalipsis, y
     Foxe: solo las páginas de las persecuciones de Nerón y Domiciano, Juan en Patmos, Policarpo y las ciudades de Asia
Correcciones de extracción: «Cristo en el milenio» (443) es un escaneo de doble página con texto OCR defectuoso
(palabras partidas, columnas mezcladas): se vuelve a pasar por Tesseract (spa) partiendo cada página en dos mitades.
El Moody NT (225) trae columnas entrelazadas con `-layout`: se re-extrae con pdftotext en orden de lectura.
Uso: armar_corpus_ref4.py   (lee SCRATCH/ref4txt/<id>.txt; escribe SCRATCH/bloques_r4/r4_<id>_<NN>.txt,
     _indice.json y _notas.json con lo omitido y los rangos)
"""
import json, os, re, subprocess, sys, tempfile, collections
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
T = S + '/ref4txt'
OUT = S + '/bloques_r4'; os.makedirs(OUT, exist_ok=True)
LIB = '/home/user/libros-referencia4'
MAX = 90000
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indice_apocalipsis import citas, RE_F

RUIDO = [r'Descargado de http://www\.yahwehjireh\.org', r'IGLESIA CRISTIANA MINISTERIO DEL REINO DE CRISTO\s*Pastor Uriel Campos',
         r'Escanee el código para ver más productos', r'atravesdelabiblia\.org',
         r'Traducci[oó]n\s*:\s*@jm?alca07\s*/\s*Jaime Isaac Malca A\.?', r'Edici[oó]n\s*:\s*@jmalca07\s*/\s*Jaime Isaac Malca A\.?',
         r'Copyrighted materia[l!]']

# Errores de extracción/OCR evidentes (letra a letra; no se reponen palabras faltantes)
FIX = [(r'\bhaberio\b', 'haberlo'), (r'\bomados\b', 'ornados'), (r'\bienía\b', 'tenía'), (r'\bidolátfico\b', 'idolátrico'),
       (r'\bcontrastarnos\b', 'contrastamos'), (r'\bhonor al verlas\b', 'horror al verlas'), (r'\bRegó a ser\b', 'llegó a ser'),
       (r'habiendo negado a Esmirna', 'habiendo llegado a Esmirna'), (r'\bNicolaitas\b', 'nicolaítas')]

def limpiar(t):
    for r in RUIDO: t = re.sub(r, '', t)
    t = t.replace('­\n', '').replace('­', '')          # guiones blandos (Moody NT)
    for a, b in FIX: t = re.sub(a, b, t)
    t = re.sub(r'[ \t\xa0]{2,}', ' ', t)
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

indice = []; notas = {}
def volcar(id_, items, obra):
    """items: [(rotulo_pagina, texto)] -> bloques de <= MAX caracteres"""
    cur = ''; n = 0
    def cerrar():
        nonlocal cur, n
        if cur.strip():
            n += 1; fn = f'{OUT}/{id_}_{n:02d}.txt'
            open(fn, 'w').write(f'# {obra}\n\n' + cur)
            indice.append({'id': f'{id_}_{n:02d}', 'archivo': fn, 'obra': obra, 'chars': len(cur)})
        cur = ''
    for rot, txt in items:
        b = f'=== [{id_} | {rot}] ===\n{txt}\n\n'
        if len(cur) + len(b) > MAX and cur: cerrar()
        cur += b
    cerrar()

# ---------------------------------------------------------------- fuentes
OBRA = {
 '442': 'Mark Hitchcock, 101 respuestas a preguntas sobre el libro del Apocalipsis (Harvest House Publishers, 2012; edición en español digital)',
 '455': 'John MacArthur, Un recorrido en avión por el Apocalipsis (Gracia a Vosotros, código GAV-1290; edición digital en español)',
 '451': 'Billy Graham, Los cuatro jinetes del Apocalipsis se acercan a galope (1983; edición en español digital)',
 '443': 'Evis L. Carballosa, Cristo en el milenio (Editorial Portavoz; escaneo, texto vuelto a reconocer por OCR)',
 '460': 'John C. Lennox, Dios, la IA y el final de la historia: entendiendo el libro de Apocalipsis en una era de máquinas inteligentes (SPCK, 2025; edición en español)',
 '449': 'Thomas Ice, La batalla de Gog y Magog: una interpretación de Ezequiel 38 y 39 (Llamada de Medianoche; edición en español digital)',
 '450': 'John F. Walvoord, La cuestión del rapto (edición revisada y ampliada; edición en español digital)',
 '453': 'Charles H. Dyer, ¿Qué dice la Biblia sobre el futuro? (Moody Publishers, 2022; edición en español) [solo páginas con señal de Apocalipsis]',
 '454': 'David Jeremiah, Respuestas a tus preguntas acerca del cielo (Tyndale House Publishers, 2013; edición en español) [solo páginas con señal de Apocalipsis]',
 '445': 'Billy Graham, Enfrentando la muerte y la vida en el más allá (Editorial Unilit, 1987) [solo páginas con señal de Apocalipsis]',
 '448': 'Erwin W. Lutzer, Tu primer minuto después de morir [solo páginas con señal de Apocalipsis]',
 '291': 'Erwin W. Lutzer, Cómo puede estar seguro de que pasará la eternidad con Dios [solo páginas con señal de Apocalipsis]',
 '470': 'Erwin W. Lutzer, La iglesia en Babilonia (Moody Publishers, 2018; edición en español) [solo páginas con señal de Apocalipsis]',
 '479': 'John Foxe, El libro de los mártires (edición abreviada en español) [solo las páginas de Nerón, Domiciano, Juan en Patmos, Policarpo y las ciudades de Asia]',
 '319': 'Juan Calvino, El libro de oro de la verdadera vida cristiana [solo páginas con señal de Apocalipsis]',
 '257': 'R. C. Sproul, La santidad de Dios (Unilit, 1991) [solo páginas con señal de Apocalipsis]',
 '2': 'Matthew Henry, Comentario bíblico (un tomo; castellano): sección Apocalipsis',
 '225': 'Everett F. Harrison (ed.), Comentario Bíblico Moody: Nuevo Testamento (Moody Press / Editorial Portavoz): sección Apocalipsis',
}
FAM_A = ['442', '455', '451', '443', '460', '449', '450']
FAM_B = ['453', '454', '445', '448', '291', '470', '319', '257']
HENRY = (1083, 1108)      # pág. PDF: del encabezado «APOCALIPSIS» (al final de 1083) al versículo final (1108)
MOODY = (543, 575)        # pág. PDF: «APOCALIPSIS» introducción (543) a bibliografía (575); 576 = colofón
FOXE_RANGO = (16, 25)
FOXE_CLAVES = ['Nerón', 'Domiciano', 'Patmos', 'Policarpo', 'Antipas', 'Esmirna', 'Pérgamo', 'Pergamópolis', 'Éfeso', 'Tiatira',
               'Sardis', 'Filadelfia', 'Laodicea', 'Apocalipsis', 'Asia']

def ruta_pdf(id_):
    for l in open(S + '/ref4_lista.tsv'):
        a, b = l.rstrip('\n').split('\t', 1)
        if a == str(id_): return os.path.join(LIB, b)
    raise KeyError(id_)

def pags(id_):
    return open(f'{T}/{id_}.txt', errors='ignore').read().split('\f')

# ---------------------------------------------------------------- re-extracción
def ocr_mitades(pdf, cache, n_pags, dpi=260, psm=4, procs=4):
    """OCR (Tesseract spa) página por página; una página apaisada (doble página) se parte en dos mitades izquierda/derecha."""
    from multiprocessing import Pool
    os.makedirs(cache, exist_ok=True)
    pend = [n for n in range(1, n_pags + 1) if not os.path.exists(f'{cache}/{n:04d}.txt')]
    if pend:
        with Pool(procs) as p: p.starmap(_ocr_una, [(pdf, cache, n, dpi, psm) for n in pend])
    return [open(f'{cache}/{n:04d}.txt').read().replace('<<<MITAD>>>', '') for n in range(1, n_pags + 1)]

def _ocr_una(pdf, cache, n, dpi, psm):
    from PIL import Image, ImageOps
    with tempfile.TemporaryDirectory(dir=S + '/tmp' if os.path.isdir(S + '/tmp') else None) as td:
        subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-r', str(dpi), '-gray', '-png', pdf, td + '/p'], capture_output=True)
        f = [x for x in os.listdir(td) if x.endswith('.png')]
        txt = []
        if f:
            im = Image.open(td + '/' + f[0]).convert('L'); w, h = im.size
            partes = [im] if w < h else [im.crop((0, 0, w // 2 + 20, h)), im.crop((w // 2 - 20, 0, w, h))]
            for i, pt in enumerate(partes):
                p = f'{td}/h{i}.png'; ImageOps.autocontrast(pt).save(p)
                r = subprocess.run(['tesseract', p, 'stdout', '-l', 'spa', '--psm', str(psm)], capture_output=True, text=True,
                                   env={**os.environ, 'OMP_THREAD_LIMIT': '1'})
                txt.append(r.stdout)
        open(f'{cache}/{n:04d}.txt', 'w').write('\n\n'.join(txt))

def n_paginas(pdf):
    for l in subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.splitlines():
        if l.startswith('Pages:'): return int(l.split()[1])

def pags_ocr(id_):
    pdf = ruta_pdf(id_)
    return ocr_mitades(pdf, f'{S}/ocr{id_}', n_paginas(pdf))

def vocabulario(ids, minimo=3):
    c = collections.Counter()
    for i in ids: c.update(re.findall(r'[a-záéíóúñü]+', open(f'{T}/{i}.txt', errors='ignore').read().lower()))
    return {w for w, n in c.items() if n >= minimo}

def tasa_oov(t, voc):
    ws = [w for w in re.findall(r'[a-záéíóúñü]+', t.lower()) if len(w) > 1]
    return sum(w not in voc for w in ws) / max(1, len(ws))

RE_CAB = re.compile(r'^[ \t]*(?:r~\s*)?A\s*P\s*O\s*C\s*A\s*L\s*I\s*P\s*S\s*I\s*S\b[ \t]*([0-9:;,.\-–—ij\s]{0,24})?[ \t]*', re.M)
def sin_cabecera(t):
    """Quita el encabezado corrido «A P O C A L I P S I S 1:7-20» y reune las palabras partidas por guion de fin de línea."""
    t = RE_CAB.sub('', t, count=1)
    return re.sub(r'([a-záéíóúñü])-\n([a-záéíóúñü])', r'\1\2', t)

def pags_moody():
    """Moody NT: la capa de texto del PDF trae columnas entrelazadas con -layout y errores de OCR. De cada página de la sección
    de Apocalipsis se arman dos lecturas (pdftotext en orden de lectura; Tesseract spa propio) y se elige la de menor tasa de
    palabras fuera de vocabulario (vocabulario = otros libros en español de REFERENCIA4). Devuelve lista indexada por pág. PDF."""
    d, h = MOODY; pdf = ruta_pdf('225')
    A = subprocess.run(['pdftotext', '-f', str(d), '-l', str(h), pdf, '-'], capture_output=True, text=True).stdout.split('\f')
    ocr_mitades_rango(pdf, S + '/ocr225', d, h, dpi=300, psm=3)
    voc = vocabulario(['442', '451', '460', '450', '449', '2'])
    P = [''] * (d - 1); elegidas = collections.Counter()
    for k, n in enumerate(range(d, h + 1)):
        a = sin_cabecera(A[k]) if k < len(A) else ''
        b = sin_cabecera(open(f'{S}/ocr225/{n:04d}.txt').read())
        ta, tb = tasa_oov(a, voc), tasa_oov(b, voc)
        if len(b) > 0.8 * len(a) and tb <= ta: P.append(b); elegidas['tesseract'] += 1
        else: P.append(a); elegidas['pdftotext'] += 1
    notas['225_lecturas'] = dict(elegidas)
    return P

def ocr_mitades_rango(pdf, cache, d, h, dpi, psm, procs=4):
    from multiprocessing import Pool
    os.makedirs(cache, exist_ok=True)
    pend = [n for n in range(d, h + 1) if not os.path.exists(f'{cache}/{n:04d}.txt')]
    if pend:
        with Pool(procs) as p: p.starmap(_ocr_una, [(pdf, cache, n, dpi, psm) for n in pend])

# ---------------------------------------------------------------- selección
def puntaje(P):
    sc = {}; cit = set()
    for n, p in enumerate(P, 1):
        cs = citas(p); f = RE_F.findall(p)
        sc[n] = 3 * len(cs) + len(f)
        if cs: cit.add(n)
    return sc, cit

def seleccion(P):
    sc, cit = puntaje(P)
    sel = {n for n, s in sc.items() if s >= 3}
    for n in cit: sel |= {n - 1, n, n + 1}
    return sorted(n for n in sel if 1 <= n <= len(P)), sc, cit

def items(P, nums, minimo=80):
    out = []
    for n in nums:
        t = limpiar(P[n - 1])
        if len(t) > minimo: out.append((f'pág. PDF {n}', t))
    return out

def rangos(nums):
    r = []; cur = []
    for n in nums:
        if cur and n == cur[-1] + 1: cur.append(n)
        else:
            if cur: r.append(cur)
            cur = [n]
    if cur: r.append(cur)
    return ','.join(f'{c[0]}' if len(c) == 1 else f'{c[0]}-{c[-1]}' for c in r)

def fam_a():
    for id_ in FAM_A:
        P = pags_ocr(id_) if id_ == '443' else pags(id_)
        its = items(P, range(1, len(P) + 1))
        volcar(f'r4_{id_}', its, OBRA[id_])
        notas[id_] = {'modo': 'completo', 'paginas_leidas': len(its), 'paginas_pdf': len(P),
                      'obs': 'OCR propio (Tesseract spa, doble página partida)' if id_ == '443' else ''}

def fam_b():
    for id_ in FAM_B:
        P = pags(id_)
        sel, sc, cit = seleccion(P)
        if id_ == '319' and not sel:      # texto de imagen: se pasa OCR para decidir si hay señal
            P = pags_ocr(id_); sel, sc, cit = seleccion(P)
        if id_ in ('319', '257'):          # solo con señal clara de Apocalipsis (>= 3 páginas con cita explícita)
            clara = len(cit) >= 3
            if not clara:
                notas[id_] = {'modo': 'omitido', 'motivo': f'sin señal clara de Apocalipsis (páginas con cita explícita: {sorted(cit)}; puntaje total {sum(sc.values())})'}
                continue
        its = items(P, sel)
        volcar(f'r4_{id_}', its, OBRA[id_])
        notas[id_] = {'modo': 'señal', 'paginas_elegidas': len(its), 'paginas_pdf': len(P), 'paginas_con_cita': sorted(cit),
                      'seleccion': rangos([n for n in sel if len(limpiar(P[n - 1])) > 80])}

def fam_c():
    P = pags('2'); d, h = HENRY
    volcar('r4_2', items(P, range(d, h + 1)), OBRA['2'] + f' (pág. PDF {d}-{h})')
    notas['2'] = {'modo': 'rango', 'rango_pdf': f'{d}-{h}', 'obs': 'Apocalipsis arranca al final de la pág. 1083 (tras Judas); el tomo es de 1109 págs.'}
    P = pags_moody(); d, h = MOODY
    volcar('r4_225', items(P, range(d, h + 1)), OBRA['225'] + f' (pág. PDF {d}-{h}; texto re-extraído, ver notas)')
    notas['225'] = {'modo': 'rango', 'rango_pdf': f'{d}-{h}', 'obs': 'columnas entrelazadas y OCR defectuoso en la extracción original; por página se eligió la mejor entre pdftotext (orden de lectura) y Tesseract propio; encabezado corrido quitado'}
    P = pags('479'); a, b = FOXE_RANGO
    nums = [n for n in range(a, b + 1) if any(k in P[n - 1] for k in FOXE_CLAVES)]
    volcar('r4_479', items(P, nums), OBRA['479'])
    notas['479'] = {'modo': 'claves', 'paginas': rangos(nums), 'claves': FOXE_CLAVES,
                    'obs': 'Antipas no aparece en esta edición abreviada; el resto del libro (persecuciones medievales y modernas) se omite'}

if __name__ == '__main__':
    for f in os.listdir(OUT):
        if f.startswith('r4_') and f.endswith('.txt'): os.remove(os.path.join(OUT, f))
    fam_a(); fam_b(); fam_c()
    json.dump(indice, open(OUT + '/_indice.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(notas, open(OUT + '/_notas.json', 'w'), ensure_ascii=False, indent=1)
    print(f'{"fuente":8s} {"bloques":>7s} {"chars":>9s}  obra')
    tb = tc = 0
    for id_ in OBRA:
        b = [i for i in indice if i['id'].startswith(f'r4_{id_}_')]
        c = sum(i['chars'] for i in b); tb += len(b); tc += c
        print(f'{id_:8s} {len(b):7d} {c:9d}  {OBRA[id_][:70]}' + ('' if b else '   [OMITIDO: ' + notas.get(id_, {}).get('motivo', '') + ']'))
    print('TOTAL', tb, 'bloques', tc, 'caracteres')
