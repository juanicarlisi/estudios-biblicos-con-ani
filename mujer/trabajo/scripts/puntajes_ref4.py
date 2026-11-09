#!/usr/bin/env python3
"""Puntúa con el lente de mujer las páginas de los libros de REFERENCIA4 (corpus_ref4). Uso: puntajes_ref4.py [archivo.txt ...]  (por defecto, todos)"""
import json, os, sys, collections
sys.path.insert(0, '/home/user/trabajo/mujer/scripts')
from puntajes import RX, norm, paginas  # noqa: E402
C = '/home/user/trabajo/corpus_ref4'
OUT = '/home/user/trabajo/mujer/puntajes_ref4.jsonl'
man = {json.loads(l)['path']: json.loads(l) for l in open(f'{C}/_manifiesto.jsonl')}
n = 0
with open(OUT, 'w') as out:
    for p, m in man.items():
        f = f'{C}/{p}.txt'; ocr = f'{C}/{p}.ocr.txt'
        if os.path.exists(ocr) and os.path.getsize(ocr) > os.path.getsize(f):
            f = ocr
        elif m['escaneado']:
            continue
        txt = open(f, errors='ignore').read()
        for i, pg in enumerate(paginas(txt), 1):
            if len(pg.strip()) < 200:
                continue
            t = norm(pg); temas = collections.Counter()
            for tema, w, rx in RX:
                k = len(rx.findall(t))
                if k:
                    temas[tema] += w * k
            punt = sum(temas.values()) * 3000 / max(len(pg), 800)
            out.write(json.dumps({'archivo': p, 'txt': os.path.relpath(f, C), 'pagina': i, 'chars': len(pg), 'puntaje': round(punt, 1), 'temas': dict(temas)}, ensure_ascii=False) + '\n')
            n += 1
print('páginas puntuadas', n)
