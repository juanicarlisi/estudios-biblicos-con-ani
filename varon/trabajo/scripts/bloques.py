#!/usr/bin/env python3
"""Arma los bloques de lectura del estudio del varón.

Selección (sin libros duplicados):
- carpetas núcleo de REFERENCIA3 (y Personajes bíblicos): páginas con puntaje ≥ 2;
- biografías: puntaje ≥ 8;
- resto de REFERENCIA3 y comentarios de la biblioteca: puntaje ≥ 15.
Cada página va con su encabezado «=== [ID | pág. N] ===»; cada bloque empieza con la tabla de sus fuentes.
Uso: bloques.py [--solo-ocr]   (con --solo-ocr arma solo los libros recién pasados por OCR, como bloques o_NNN)
Escribe varon/bloques/b_NNN.txt (u o_NNN.txt) y varon/bloques/_fuentes.json.
"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from puntajes import paginas

T = '/home/user/trabajo'
V = f'{T}/varon'
DST = f'{V}/bloques'
TAM = 120000
NUCLEO = {'Hombre', 'Matrimonio Familia y Noviazgo', 'Jovenes', 'Pecado Tentacion y Sexualidad', 'Liderazgo',
          'Pastorado y Consejeria', 'Ninos', 'Amor y Relaciones', 'Discipulado', 'Servicio y Ministerio',
          'Finanzas y Mayordomia', 'Personajes Biblicos'}

BIBLIO_AUTORES = [   # (patrón en el nombre del archivo, autor, obra)
    (r'Biblia de estudio', 'John MacArthur', 'Biblia de Estudio MacArthur'),
    (r'Vernon_McGee|Vernon McGee', 'J. Vernon McGee', 'Comentario Bíblico A Través de la Biblia'),
    (r'Beacon Tomo (\d+)|Beacon_Tomo_(\d+)', 'Comentario Bíblico Beacon', 'Comentario Bíblico Beacon, tomo {0}'),
    (r'Exeg[ée]tico_al_Texto_Griego', 'Samuel Pérez Millos', 'Comentario exegético al texto griego del NT'),
    (r'Hendriksen y Kistemaker', 'William Hendriksen y Simon Kistemaker', 'Comentario al Nuevo Testamento'),
    (r'kistemaker|Kistemaker', 'Simon Kistemaker', 'Comentario al Nuevo Testamento'),
    (r'Carballosa', 'Evis L. Carballosa', 'Comentario'),
    (r'Walvoord', 'John F. Walvoord y Roy B. Zuck', 'El conocimiento bíblico: comentario del AT'),
    (r'STOTT', 'John Stott', 'El mensaje de Efesios'),
    (r'Spurgeon', 'C. H. Spurgeon', 'El tesoro de David'),
    (r'Lutero', 'Martín Lutero', 'Comentario'),
    (r'Edersheim', 'Alfred Edersheim', 'Comentario bíblico histórico: Génesis'),
    (r'Matthew Henry', 'Matthew Henry', 'Comentario bíblico'),
    (r'Ladd', 'George Eldon Ladd', 'Comentario del Apocalipsis'),
    (r'Elizabeth George', 'Elizabeth George', 'Santiago: crece en sabiduría y fe'),
    (r'Moody', 'Comentario Bíblico Moody', 'Comentario Bíblico Moody'),
    (r'Desmond_Alexander', 'T. Desmond Alexander', 'Enseñar el texto: Éxodo'),
    (r'NVI_1_y_2_Tesalonicenses', 'Michael W. Holmes', 'Comentario bíblico con aplicación NVI: 1 y 2 Tesalonicenses'),
    (r'DICCIONARIO', 'Diccionario Bíblico Mundo Hispano', 'Diccionario Bíblico Mundo Hispano'),
    (r'Romanos - Estudio', 'Biblia de bosquejos y sermones', 'Biblia de bosquejos y sermones, tomo 7: Romanos'),
    (r'Hebreos \(2\)', 'J. N. Darby', 'Notas de conferencias sobre la epístola a los Hebreos'),
    (r'Hebreos, Santiago, 1 y 2 Pedro, Judas', 'Comentario Bíblico Mundo Hispano', 'Comentario Bíblico Mundo Hispano, tomo 23'),
    (r'mundo hispano', 'Comentario Bíblico Mundo Hispano', 'Comentario Bíblico Mundo Hispano'),
    (r'Biblia Popular 37', 'David P. Kuske', 'La Biblia Popular: 1 y 2 Tesalonicenses'),
    (r'Biblia Popular 39', 'Richard E. Lauersdorf', 'La Biblia Popular: Hebreos'),
    (r'MacArthur|Macarthur|MacARTHUR|^\d+ [A-ZÁÉÍÓÚ ]+-John', 'John MacArthur', 'Comentario MacArthur del Nuevo Testamento'),
    (r'1, 2 y 3 Juan|1,2y3 Juan', 'John MacArthur', 'Comentario MacArthur del Nuevo Testamento: 1, 2 y 3 Juan'),
]


def autor_biblio(arch):
    nombre = arch.split('/')[-1]; libro = arch.split('/')[0].split(' - ')[-1].title()
    for pat, autor, obra in BIBLIO_AUTORES:
        m = re.search(pat, nombre)
        if m:
            nums = [g for g in m.groups() if g] if m.groups() else []
            obra = obra.format(*nums) if nums else obra
            if obra.endswith('NT') or obra in ('Comentario', 'Comentario al Nuevo Testamento', 'Comentario Bíblico A Través de la Biblia',
                                                'Comentario MacArthur del Nuevo Testamento', 'Comentario bíblico'):
                obra = f'{obra}: {libro}'
            return autor, obra
    return 'Comentario de la biblioteca', f'{libro} ({nombre})'


def limpiar(pg):
    """Une líneas cortadas, compacta espacios y corta líneas largas para que el agente lea todo."""
    pg = pg.replace('\r', '')
    pg = re.sub(r'-\n(?=[a-záéíóúñ])', '', pg)
    pg = re.sub(r'(?<![.:;!?»”"\n])\n(?!\n)', ' ', pg)
    pg = re.sub(r'[ \t]+', ' ', pg)
    pg = re.sub(r'\n{3,}', '\n\n', pg).strip()
    out = []
    for linea in pg.split('\n'):
        while len(linea) > 400:
            corte = linea.rfind(' ', 0, 400)
            corte = corte if corte > 200 else 400
            out.append(linea[:corte]); linea = linea[corte:].lstrip()
        out.append(linea)
    return '\n'.join(out)


def main():
    solo_ocr = '--solo-ocr' in sys.argv
    clas = {e['path']: e for e in json.load(open(f'{T}/clasif/clasificacion.json'))}
    dup = json.load(open(f'{V}/duplicados.json'))
    ocr_cola = {x['archivo'] for x in json.load(open(f'{V}/ocr/cola.json'))} | {'Pecado Tentacion y Sexualidad/La Homosexualidad, compasión y claridad en el debate - Tomas Schmitd.pdf'}
    nucleo_k = {b for a, b in dup.items() if a.startswith('ref3:') and a.split(':', 1)[1].split('/')[0] in NUCLEO}
    P = [json.loads(l) for l in open(f'{V}/puntajes.jsonl')]
    os.makedirs(DST, exist_ok=True)
    fuentes_f = f'{DST}/_fuentes.json'
    fuentes = json.load(open(fuentes_f)) if os.path.exists(fuentes_f) else {}
    por_archivo = collections.defaultdict(list)
    for p in P:
        k = f"{p['fuente']}:{p['archivo']}"
        if k in dup:
            continue
        es_ocr = p['fuente'] == 'ref3' and p['archivo'] in ocr_cola
        if solo_ocr != es_ocr:
            continue
        carpeta = p['archivo'].split('/')[0]
        nuc = p['fuente'] == 'ref3' and (carpeta in NUCLEO or k in nucleo_k)
        bio = p['fuente'] == 'ref3' and carpeta == 'Historia de la Iglesia y Biografias'
        th = 2 if nuc else 8 if bio else 15
        if p['puntaje'] >= th:
            por_archivo[k].append(p)
    # orden: núcleo primero, después biografías, resto de REFERENCIA3 y biblioteca
    def prioridad(k):
        fu, arch = k.split(':', 1); carpeta = arch.split('/')[0]
        if fu == 'ref3' and (carpeta in NUCLEO or k in nucleo_k): return 0
        if fu == 'ref3' and carpeta == 'Historia de la Iglesia y Biografias': return 1
        return 2 if fu == 'ref3' else 3
    claves = sorted(por_archivo, key=lambda k: (prioridad(k), k))
    textos = {}
    bloques, actual, tam, ids_bloque = [], [], 0, []
    for k in claves:
        fu, arch = k.split(':', 1)
        fid = next((i for i, v in fuentes.items() if v['clave'] == k), None)
        if not fid:
            fid = f"{'R' if fu == 'ref3' else 'B'}{len(fuentes) + 1:04d}"
            if fu == 'ref3':
                c = clas.get(arch, {}); autor, obra = c.get('autor', ''), c.get('titulo', arch.split('/')[-1])
            else:
                autor, obra = autor_biblio(arch)
            fuentes[fid] = {'clave': k, 'fuente': fu, 'archivo': arch, 'autor': autor, 'obra': obra}
        txtf = por_archivo[k][0]['txt']
        if txtf not in textos:
            textos = {txtf: paginas(open(f'{T}/{txtf}', errors='ignore').read())}
        pags = textos[txtf]
        for p in sorted(por_archivo[k], key=lambda p: p['pagina']):
            i = p['pagina']
            if i - 1 >= len(pags):
                continue
            cuerpo = limpiar(pags[i - 1])
            trozo = f"=== [{fid} | pág. {i}] ===\n{cuerpo}\n"
            if tam + len(trozo) > TAM and actual:
                bloques.append((actual, ids_bloque)); actual, tam, ids_bloque = [], 0, []
            actual.append(trozo); tam += len(trozo)
            if fid not in ids_bloque:
                ids_bloque.append(fid)
    if actual:
        bloques.append((actual, ids_bloque))
    pref = 'o' if solo_ocr else 'b'
    for f in os.listdir(DST):
        if f.startswith(pref + '_'):
            os.remove(os.path.join(DST, f))
    for n, (trozos, ids) in enumerate(bloques, 1):
        cab = ['FUENTES DE ESTE BLOQUE (id = autor, obra):'] + [f"{i} = {fuentes[i]['autor']}, {fuentes[i]['obra']}" for i in ids]
        open(f'{DST}/{pref}_{n:03d}.txt', 'w').write('\n'.join(cab) + '\n\n' + ''.join(trozos))
    json.dump(fuentes, open(fuentes_f, 'w'), ensure_ascii=False, indent=1)
    print('bloques', len(bloques), '| fuentes', len(fuentes), '| caracteres', sum(sum(len(t) for t in b[0]) for b in bloques))


if __name__ == '__main__':
    main()
