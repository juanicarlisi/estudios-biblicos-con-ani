#!/usr/bin/env python3
"""Arma el catálogo de la biblioteca (ref3 + ref4 + biblioteca) reutilizando las clasificaciones de autores ya hechas.
Salida: trabajo/catalogo/catalogo.json y trabajo/catalogo/resumen.md
Uso: python3 catalogo.py <dir con tree_libros-referencia3.tsv, tree_libros-referencia4.tsv, tree_biblioteca-estudios-biblicos.tsv>"""
import json, sys, os, collections
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
T = sys.argv[1]
def arbol(n):
    out = []
    for l in open(f'{T}/tree_{n}.tsv', encoding='utf-8'):
        s, p = l.rstrip('\n').split('\t', 1)
        if p.lower().endswith(('.pdf', '.docx', '.doc', '.epub')): out.append((p, int(s)))
    return out
g = {x['path']: x for x in json.load(open(f'{RAIZ}/genesis/trabajo/clasificacion/clasificacion.json'))}
r4 = json.load(open(f'{RAIZ}/mujer/trabajo/ref4/clasificacion.json'))
r4 = dict(r4) if isinstance(r4, list) and r4 and isinstance(r4[0], list) else (r4 if isinstance(r4, dict) else {x['path']: x for x in r4})
cat = []
for repo, nombre, base in (('ref3', 'libros-referencia3', g), ('ref4', 'libros-referencia4', r4), ('biblio', 'biblioteca-estudios-biblicos', {})):
    for p, s in arbol(nombre):
        c = base.get(p)
        area = p.split('/')[0] if repo != 'biblio' else 'Comentarios por libro (MATERIAL SOPORTE)'
        cat.append({'repo': repo, 'path': p, 'area': area, 'mb': round(s / 1e6, 1),
                    'categoria': c['categoria'] if c else '?', 'autor': c.get('autor', '') if c else '', 'titulo': c.get('titulo', '') if c else '',
                    'duplicado_de': c.get('duplicado_de', '') if c else ''})
os.makedirs(f'{RAIZ}/megaestudio/trabajo/catalogo', exist_ok=True)
json.dump(cat, open(f'{RAIZ}/megaestudio/trabajo/catalogo/catalogo.json', 'w'), ensure_ascii=False, indent=0)
res = collections.defaultdict(collections.Counter)
for c in cat: res[(c['repo'], c['area'])][c['categoria']] += 1
L = ['# Catálogo de la biblioteca', '', 'A = protestante confiable (se usa); B = con reservas; C = excluido; D = autor no identificable; E = material propio; ? = sin clasificar todavía.', '',
     '| Repo | Área | A | B | C | D | E | ? | Total |', '|---|---|--:|--:|--:|--:|--:|--:|--:|']
for (r, a), c in sorted(res.items()):
    L.append(f"| {r} | {a} | " + ' | '.join(str(c.get(k, 0)) for k in 'ABCDE?') + f' | {sum(c.values())} |')
tot = collections.Counter(c['categoria'] for c in cat)
L += ['', f"**Total:** {len(cat)} archivos · " + ' · '.join(f'{k}: {v}' for k, v in sorted(tot.items()))]
open(f'{RAIZ}/megaestudio/trabajo/catalogo/resumen.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L[-1:]), '\n', tot)
