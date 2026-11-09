#!/usr/bin/env python3
"""Divide las entradas de plan/planear/<S>.txt que pasan de ~90 KB en fragmentos S_1.txt, S_2.txt… (por grupos, en el orden de parecido).
Escribe plan/planear/_fragmentos.json {S: [S_1, S_2, ...]}. Los planificadores corren un fragmento tras otro y cada uno ve los días ya planeados."""
import json, math, os, glob
D = '/home/user/trabajo/mujer/plan/planear'
for f in glob.glob(f'{D}/?_[0-9].txt'): os.remove(f)
frag = {}
for S in 'ABCDEFGHIJKLMNOPQ':
    ls = [l for l in open(f'{D}/{S}.txt') if l.strip()]
    tam = sum(len(l) for l in ls)
    n = max(1, math.ceil(tam / 90000))
    parte = [ls[i * len(ls) // n:(i + 1) * len(ls) // n] for i in range(n)]
    frag[S] = []
    for k, p in enumerate(parte, 1):
        nombre = f'{S}_{k}'
        open(f'{D}/{nombre}.txt', 'w').writelines(p)
        frag[S].append(nombre)
json.dump(frag, open(f'{D}/_fragmentos.json', 'w'))
print({S: len(v) for S, v in frag.items()}, '| fragmentos', sum(len(v) for v in frag.values()))
