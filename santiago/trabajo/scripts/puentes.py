#!/usr/bin/env python3
"""Arma los bloques «puente» de la biblioteca: la última página de cada bloque de lectura junto con la primera del bloque siguiente.

Los bloques de lectura son rangos de páginas contiguos, sin superposición: la idea que empieza al final de una página del bloque N y sigue al comienzo del
bloque N+1 quedó cortada para los dos agentes y no se extrajo. Cada puente reúne, en pares, las dos páginas del salto para recuperar esas ideas.

Uso: puentes.py [--por-bloque 8]
Escribe TMP/segmentos/biblio/<obra>_1NN.txt (ids 101, 102… dentro de cada obra, así la etiqueta de la obra se resuelve igual que en los bloques normales)
y TMP/puentes.json con los pares de cada puente. Las obras que no se leen de corrido (el diccionario, DBMH) no llevan puentes.
"""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

DIR = os.path.join(C.TMP, 'segmentos', 'biblio')
SIN_PUENTES = {'dbmh'}


def paginas(txt):
    """Lista ordenada de (n_pdf, encabezado, texto) de un bloque."""
    partes = re.split(r'^(=== \[.+?\] ===)\s*$', txt, flags=re.M)
    out = []
    for i in range(1, len(partes) - 1, 2):
        m = re.search(r'PÁGINA PDF (\d+)', partes[i])
        if m:
            out.append((int(m.group(1)), partes[i], partes[i + 1].strip('\n')))
    return out


def main():
    por = 8
    if '--por-bloque' in sys.argv:
        por = int(sys.argv[sys.argv.index('--por-bloque') + 1])
    indice = json.load(open(os.path.join(DIR, '_indice.json')))
    por_obra = collections.OrderedDict()
    for b in indice:
        por_obra.setdefault(b['fuente'], []).append(b)
    resumen = {}
    for obra, bloques in por_obra.items():
        if obra in SIN_PUENTES or len(bloques) < 2:
            continue
        pares = []
        for a, b in zip(bloques, bloques[1:]):
            pa = paginas(open(a['archivo'], errors='ignore').read())
            pb = paginas(open(b['archivo'], errors='ignore').read())
            if not pa or not pb:
                continue
            ult, prim = pa[-1], pb[0]
            if not 0 < prim[0] - ult[0] <= 3:
                continue
            pares.append({'entre': [a['id'], b['id']], 'paginas': [ult[0], prim[0]], 'texto': [ult, prim]})
        trozos = [pares[i:i + por] for i in range(0, len(pares), por)]
        for k, grupo in enumerate(trozos, 1):
            bid = f'{obra}_{100 + k}'
            desc = bloques[0]['descripcion']
            cuerpo = [f'OBRA: {desc}', f"BLOQUE: {bid} (PUENTES: {len(grupo)} pares de páginas contiguas, la última de un bloque de lectura y la primera del siguiente)", '']
            for p in grupo:
                cuerpo.append(f"##### PUENTE entre {p['entre'][0]} y {p['entre'][1]}: la primera página termina el bloque anterior y la segunda abre el siguiente #####")
                for n, cab, tx in p['texto']:
                    cuerpo += [cab, tx, '']
            ruta = os.path.join(DIR, bid + '.txt')
            open(ruta, 'w').write('\n'.join(cuerpo))
            resumen[bid] = {'obra': obra, 'pares': [p['entre'] + p['paginas'] for p in grupo], 'archivo': ruta, 'chars': os.path.getsize(ruta)}
    json.dump(resumen, open(os.path.join(C.TMP, 'puentes.json'), 'w'), ensure_ascii=False, indent=1)
    for bid, r in resumen.items():
        print(f"{bid:16s} {len(r['pares']):2d} pares  {r['chars']:7d} caracteres  páginas {[p[2:] for p in r['pares']]}")
    print(len(resumen), 'bloques puente,', sum(len(r['pares']) for r in resumen.values()), 'pares')


if __name__ == '__main__':
    main()
