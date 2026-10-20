#!/usr/bin/env python3
"""Detecta libros repetidos (mismo texto con otro nombre) en REFERENCIA3 y la biblioteca.
Compara huellas de 8-gramas de palabras tomadas de todo el texto; Jaccard ≥ 0,5 = duplicado.
Conserva el de más texto. Escribe varon/duplicados.json {archivo_descartado: archivo_conservado}."""
import json, re, sys, hashlib, collections
sys.path.insert(0, '/home/user/trabajo/varon/scripts')
from puntajes import fuentes, norm

def huella(t):
    pal = re.findall(r'[a-z]{3,}', norm(t))
    hs = set()
    for i in range(0, max(0, len(pal) - 8), 7):
        h = int(hashlib.md5(' '.join(pal[i:i + 8]).encode()).hexdigest()[:8], 16)
        if h % 8 == 0:
            hs.add(h)
    return hs

items = []
for fu, arch, f in fuentes():
    t = open(f, errors='ignore').read()
    if len(t) < 5000:
        continue
    items.append((f'{fu}:{arch}', len(t), huella(t)))
idx = collections.defaultdict(set)
for k, (nombre, n, hs) in enumerate(items):
    for h in hs:
        idx[h].add(k)
dup = {}
for k, (nombre, n, hs) in enumerate(items):
    if not hs:
        continue
    cand = collections.Counter()
    for h in hs:
        for j in idx[h]:
            if j != k:
                cand[j] += 1
    for j, c in cand.items():
        inter = c; uni = len(hs) + len(items[j][2]) - c
        if inter / uni >= 0.5:
            a, b = (k, j) if (n, nombre) < (items[j][1], items[j][0]) else (j, k)   # a = el más chico
            dup[items[a][0]] = items[b][0]
json.dump(dup, open('/home/user/trabajo/varon/duplicados.json', 'w'), ensure_ascii=False, indent=1)
print('duplicados:', len(dup))
for a, b in list(dup.items())[:40]:
    print(' ', a[:70], '→', b[:70])
