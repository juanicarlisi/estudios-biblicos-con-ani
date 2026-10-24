#!/usr/bin/env python3
"""Corta en bloques de lectura los comentarios de la biblioteca que tratan Santiago.

Cada bloque es un archivo de texto de hasta ~42.000 caracteres con encabezados «=== [obra | PÁGINA PDF n | pág. impresa m] ===»
para que quien lo lea pueda rotular cada nota con su página. Lee el texto ya convertido en TMP/corpus_biblio/*.txt
(pdftotext; \\f separa las páginas) y escribe TMP/segmentos/biblio/<obra>_NN.txt y _indice.json.

Los rangos de páginas son los que ocupa Santiago dentro de cada archivo (los volúmenes de varias cartas se recortan).
"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import config as C

CORPUS = os.path.join(C.TMP, 'corpus_biblio')
DEST = os.path.join(C.TMP, 'segmentos', 'biblio')
MAX = 30000

# id: (archivo, página PDF inicial, final, descripción, desplazamiento a la página impresa o None)
FUENTES = {
    'macarthur': ('macarthur_santiago.txt', 3, 296,
                  'John MacArthur, Santiago, Comentario MacArthur del Nuevo Testamento (Editorial Portavoz)', None),
    'kistemaker': ('kistemaker_santiago_juan.txt', 7, 159,
                   'Simon J. Kistemaker, Exposición de la Epístola de Santiago, en Comentario al Nuevo Testamento (2001)', None),
    'carballosa': ('carballosa_b.txt', 5, 312,
                   'Evis L. Carballosa, Santiago: una fe en acción, edición actualizada (Editorial Portavoz, 1986, 2014). '
                   'Primera parte: hermenéutica y la epístola; segunda parte: exégesis; tercera parte (desde la página PDF 281): '
                   'predicación expositiva (rescatar solo lo que enseñe sobre el texto de Santiago, no el método homilético)', None),
    'george': ('george_santiago.txt', 15, 206,
               'Elizabeth George, Santiago: crece en sabiduría y fe (Editorial Portavoz, 2013): 25 lecciones de estudio', None),
    'cbmh': ('cbmh_t23.txt', 129, 223,
             'Daniel Carro (exposición) y Julio Beltrán Patarroyo (ayudas prácticas), «Santiago», Comentario Bíblico Mundo Hispano, tomo 23 '
             '(Editorial Mundo Hispano); las marcas [P. n] son la página impresa', None),
    'beacon': ('beacon_t10.txt', 126, 172,
               'A. F. Harper, «Santiago», Comentario Bíblico Beacon, tomo 10 (Casa Nazarena de Publicaciones)', None),
    'macarthur_be': ('macarthur_biblia_estudio.txt', 3212, 3244,
                     'John MacArthur, Biblia de Estudio MacArthur (Editorial Portavoz): introducción y notas de Santiago '
                     '(al final entra el comienzo de 1 Pedro: ignorarlo)', None),
}

BASURA = [
    re.compile(r'^(IGLESIA CRISTIANA MINISTERIO DEL REINO DE CRISTO|Pastor Uriel Campos|Elaborado por el Pastor Uriel Campos|'
               r'Web: http://ucampos\.jimdo\.com|Correo: ucampos074@yahoo\.com)\s*$', re.M),
    re.compile(r'^Descargado de http://www\.yahwehjireh\.org\s*$', re.M),
    re.compile(r'^(Este ebook utiliza tecnología de protección de gestión de derechos digitales\.|Pertenece a Ricardo Ochoa - Rickbooks84@gmail\.com)\s*$', re.M),
]


def limpiar(t):
    for r in BASURA:
        t = r.sub('', t)
    return re.sub(r'\n{3,}', '\n\n', t).strip()


def bloques_de_fuente(k, fn, a, b, off):
    pags = open(os.path.join(CORPUS, fn), errors='ignore').read().split('\f')
    trozos, cur, ini = [], '', a
    for n in range(a, b + 1):
        t = limpiar(pags[n - 1])
        if not t:
            continue
        lab = f'=== [{k} | PÁGINA PDF {n}' + (f' | pág. impresa {n + off}' if off else '') + '] ==='
        blq = lab + '\n' + t + '\n'
        if len(cur) + len(blq) > MAX and cur:
            trozos.append((ini, n - 1, cur)); cur, ini = '', n
        cur += blq
    if cur:
        trozos.append((ini, b, cur))
    return trozos


def recortar(texto, corto=6000, ventana=900):
    """Entradas largas (Pablo, Jacob, Judío…): se conserva el comienzo y lo que rodea a cada cita de Santiago."""
    if len(texto) <= corto:
        return texto
    marcas = [m.start() for m in re.finditer(r'<59\d{4}>', texto)]
    cortes = [(0, 1500)] + [(max(0, m - ventana), min(len(texto), m + ventana)) for m in marcas]
    cortes.sort(); fus = []
    for a, b in cortes:
        if fus and a <= fus[-1][1]:
            fus[-1] = (fus[-1][0], max(fus[-1][1], b))
        else:
            fus.append((a, b))
    return '\n[…]\n'.join(texto[a:b].strip() for a, b in fus)


def diccionario():
    """Entradas del Diccionario Bíblico Mundo Hispano que citan Santiago (<59CCVV>) o tratan de él."""
    sel = []
    for vol, fn in (('I', 'dbmh_1.txt'), ('II', 'dbmh_2.txt')):
        pags = open(os.path.join(CORPUS, fn), errors='ignore').read().split('\f')
        entradas, cur = [], None
        for pn, p in enumerate(pags, 1):
            lines = p.split('\n')
            for i, l in enumerate(lines):
                prev_blank = (i == 0) or (lines[i - 1].strip() == '')
                m = (re.match(r'^([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñüÁÉÍÓÚÑ\'’\-]+(?:[ ,][A-Za-záéíóúñüÁÉÍÓÚÑ\'’\-]+){0,3})\s\(', l)
                     or re.match(r'^([A-ZÁÉÍÓÚÑ]{3,}(?:[ ,]+[A-ZÁÉÍÓÚÑ]{2,}){0,3})\.?\s*$', l))
                if prev_blank and m:
                    cur = {'vol': vol, 'titulo': m.group(1).strip(), 'pag': pn, 'texto': ''}; entradas.append(cur)
                if cur is not None:
                    cur['texto'] += l + '\n'
        for e in entradas:
            e['citas'] = len(re.findall(r'<59\d{4}>', e['texto']))
            if e['citas'] >= 1 or re.match(r'^SANTIAGO', e['titulo'].upper()):
                e['texto'] = recortar(e['texto'])
                sel.append(e)
    sel.sort(key=lambda e: (e['vol'], e['pag']))
    trozos, cur = [], ''
    for e in sel:
        b = f"=== [dbmh | Diccionario Bíblico Mundo Hispano, vol. {e['vol']} | PÁGINA PDF {e['pag']} | entrada: {e['titulo']}] ===\n{e['texto'].strip()}\n\n"
        if len(cur) + len(b) > MAX and cur:
            trozos.append(cur); cur = ''
        cur += b
    if cur:
        trozos.append(cur)
    return trozos, sel


def main():
    os.makedirs(DEST, exist_ok=True)
    for f in os.listdir(DEST):
        os.remove(os.path.join(DEST, f))
    idx = []
    for k, (fn, a, b, desc, off) in FUENTES.items():
        for i, (x, y, c) in enumerate(bloques_de_fuente(k, fn, a, b, off), 1):
            out = os.path.join(DEST, f'{k}_{i:02d}.txt')
            c = f'OBRA: {desc}\nBLOQUE: {k}_{i:02d} (páginas PDF {x}-{y})\n\n' + c
            open(out, 'w').write(c)
            idx.append({'id': f'{k}_{i:02d}', 'fuente': k, 'descripcion': desc, 'paginas': f'{x}-{y}', 'archivo': out, 'chars': len(c)})
    trozos, sel = diccionario()
    desc = ('Diccionario Bíblico Mundo Hispano (Editorial Mundo Hispano): entradas que citan Santiago; las citas aparecen codificadas '
            'como <59CCVV> = Santiago capítulo CC versículo VV. Extraer SOLO lo que aporta a entender la carta de Santiago '
            '(personas, lugares, costumbres, palabras, temas); ignorar lo ajeno a Santiago')
    for i, t in enumerate(trozos, 1):
        out = os.path.join(DEST, f'dbmh_{i:02d}.txt')
        t = f'OBRA: {desc}\nBLOQUE: dbmh_{i:02d}\n\n' + t
        open(out, 'w').write(t)
        idx.append({'id': f'dbmh_{i:02d}', 'fuente': 'dbmh', 'descripcion': desc, 'paginas': 'varias (ver encabezados)', 'archivo': out, 'chars': len(t)})
    json.dump(idx, open(os.path.join(DEST, '_indice.json'), 'w'), ensure_ascii=False, indent=1)
    cnt = collections.Counter(i['fuente'] for i in idx)
    print(len(idx), 'bloques', dict(cnt), '| caracteres', sum(i['chars'] for i in idx))
    print('entradas del diccionario:', len(sel), [e['titulo'] for e in sel][:60])


if __name__ == '__main__':
    main()
