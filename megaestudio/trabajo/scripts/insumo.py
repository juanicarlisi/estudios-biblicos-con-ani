#!/usr/bin/env python3
"""Arma el insumo de un día: el texto de las páginas elegidas de cada libro, con marcas [[id#pág]].
Uso: insumo.py <dia.spec.json> > insumo.md     spec: {"dia":1,"lecturas":{"packer":[[15,24]],"pink":[[3,3],[10,12]]}}"""
import json, os, sys, re
OUT = os.environ.get('MEGA_TXT', '/home/user/lib/pages')
AQUI = os.path.dirname(os.path.abspath(__file__)); LIB = json.load(open(f'{AQUI}/../libros.json'))
spec = json.load(open(sys.argv[1])); res = []
for i, rangos in spec['lecturas'].items():
    pags = json.load(open(f'{OUT}/{i}.json'))
    res.append(f"\n######## {i} · {LIB[i]['autor']}, {LIB[i]['obra']}\n")
    for a, b in rangos:
        for n in range(a, b + 1):
            t = re.sub(r'\n{3,}', '\n\n', pags[n - 1]).strip()
            res.append(f'[[{i}#{n}]]\n{t}\n')
print('\n'.join(res))
