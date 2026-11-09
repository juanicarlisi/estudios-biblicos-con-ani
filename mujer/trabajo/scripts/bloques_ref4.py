#!/usr/bin/env python3
"""Arma los bloques r_NNN.txt con las páginas relevantes de los libros de REFERENCIA4 clasificados como A (protestante confiable).

Entrada: ref4_candidatos.json (páginas puntuadas), clasif_ref4/clasificacion.json (de wf_clasificar_ref4.js; ver clasif_ref4.py).
Ids de fuente R6001…; se registran en bloques/_fuentes.json. Uso: bloques_ref4.py [--tam N] [--categorias A]
"""
import json, os, re, sys, collections
sys.path.insert(0, '/home/user/trabajo/mujer/scripts')
from puntajes import paginas  # noqa: E402
from bloques import limpiar  # noqa: E402
V = '/home/user/trabajo/mujer'; C = '/home/user/trabajo/corpus_ref4'
TAM = int(sys.argv[sys.argv.index('--tam') + 1]) if '--tam' in sys.argv else 120000
CATS = set(sys.argv[sys.argv.index('--categorias') + 1]) if '--categorias' in sys.argv else {'A'}
UMB = [(r'nuevos/05 ', 3), (r'nuevos/06 ', 10), (r'nuevos/(14|07) ', 8), (r'nuevos/(09|13) ', 8)]
def umbral(a):
    for rx, t in UMB:
        if re.match(rx, a): return t
    return 22
cand = json.load(open(f'{V}/ref4_candidatos.json'))['paginas']
clas = json.load(open(f'{V}/clasif_ref4/clasificacion.json'))
fuentes_f = f'{V}/bloques/_fuentes.json'; fuentes = json.load(open(fuentes_f))
for k in [k for k in fuentes if k.startswith('R6')]: del fuentes[k]
for f in os.listdir(f'{V}/bloques'):
    if f.startswith('r_'): os.remove(f'{V}/bloques/{f}')
libros = sorted(a for a in cand if clas.get(a, {}).get('categoria') in CATS)
bloques, act, tam, ids, n = [], [], 0, [], 0
chars = 0
for a in libros:
    pags = [p for p in cand[a] if p['puntaje'] >= umbral(a)]
    if not pags: continue
    n += 1; fid = f'R{6000 + n}'; c = clas[a]
    fuentes[fid] = {'clave': 'ref4:' + a, 'fuente': 'ref4', 'archivo': a, 'autor': c['autor'], 'obra': c['titulo']}
    texto = paginas(open(f"{C}/{pags[0]['txt']}", errors='ignore').read())
    for p in sorted(pags, key=lambda p: p['pagina']):
        if p['pagina'] - 1 >= len(texto): continue
        trozo = f"=== [{fid} | pág. {p['pagina']}] ===\n{limpiar(texto[p['pagina'] - 1])}\n"
        if tam + len(trozo) > TAM and act:
            bloques.append((act, ids)); act, tam, ids = [], 0, []
        act.append(trozo); tam += len(trozo); chars += len(trozo)
        if fid not in ids: ids.append(fid)
if act: bloques.append((act, ids))
for k, (tr, ii) in enumerate(bloques, 1):
    cab = ['FUENTES DE ESTE BLOQUE (id = autor, obra):'] + [f"{i} = {fuentes[i]['autor']}, {fuentes[i]['obra']}" for i in ii]
    open(f'{V}/bloques/r_{k:03d}.txt', 'w').write('\n'.join(cab) + '\n\n' + ''.join(tr))
json.dump(fuentes, open(fuentes_f, 'w'), ensure_ascii=False, indent=1)
print('libros', n, '| bloques r_', len(bloques), '| caracteres', chars)
