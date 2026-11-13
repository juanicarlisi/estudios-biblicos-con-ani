#!/usr/bin/env python3
"""Une las clasificaciones de los agentes (res_NN.json) al catálogo (catalogo.json) y regenera resumen.md.
Uso: juntar_clasif.py <dir con lote_NN.json y res_NN.json>   (las copias idénticas heredan la clasificación; las fichas sin resultado quedan en '?')"""
import json, os, sys, glob, collections
AQUI = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(AQUI, '..'))
D = sys.argv[1]
cat = json.load(open(f'{V}/catalogo/catalogo.json')); idx = {(c['repo'], c['path']): c for c in cat}; por_ruta = collections.defaultdict(list)
for c in cat: por_ruta[c['path']].append(c)
hechas = faltan = 0; invalidas = []
for lf in sorted(glob.glob(f'{D}/lote_*.json')):
    k = lf[-7:-5]; rf = f'{D}/res_{k}.json'
    fichas = json.load(open(lf))
    if not os.path.exists(rf): faltan += len(fichas); continue
    res = {r['n']: r for r in json.load(open(rf))}
    for f in fichas:
        r = res.get(f['n'])
        if not r or r.get('categoria') not in list('ABCDE'): faltan += 1; invalidas.append(f['path']); continue
        for p in [f['path']] + f.get('copias', []):
            for c in (por_ruta.get(p) or []):
                c['categoria'] = r['categoria']; c['autor'] = r.get('autor', ''); c['titulo'] = r.get('titulo', '')
                c['editorial'] = r.get('editorial', ''); c['razon'] = r.get('razon', ''); c['confianza'] = r.get('confianza', '')
                if p != f['path']: c['duplicado_de'] = f['path']
        hechas += 1
json.dump(cat, open(f'{V}/catalogo/catalogo.json', 'w'), ensure_ascii=False, indent=0)
res = collections.defaultdict(collections.Counter)
for c in cat: res[(c['repo'], c['area'])][c['categoria']] += 1
L = ['# Catálogo de la biblioteca', '', 'A = protestante confiable (se usa); B = con reservas; C = excluido; D = autor no identificable; E = material propio; ? = sin clasificar todavía.', '',
     '| Repo | Área | A | B | C | D | E | ? | Total |', '|---|---|--:|--:|--:|--:|--:|--:|--:|']
for (r, a), c in sorted(res.items()): L.append(f"| {r} | {a} | " + ' | '.join(str(c.get(k, 0)) for k in 'ABCDE?') + f' | {sum(c.values())} |')
tot = collections.Counter(c['categoria'] for c in cat)
L += ['', f"**Total:** {len(cat)} archivos · " + ' · '.join(f'{k}: {v}' for k, v in sorted(tot.items()))]
open(f'{V}/catalogo/resumen.md', 'w').write('\n'.join(L) + '\n')
print(f'fichas aplicadas {hechas}, pendientes {faltan}'); print(L[-1])
if invalidas: print('sin resultado válido:', invalidas[:5])
