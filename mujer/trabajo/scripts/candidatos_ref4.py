#!/usr/bin/env python3
"""Páginas relevantes (lente de mujer) por libro de REFERENCIA4, sin repetidos. Escribe mujer/ref4_candidatos.json y una lista para clasificar autores."""
import json, collections, re, unicodedata
V = '/home/user/trabajo/mujer'
dup = json.load(open(f'{V}/duplicados_ref4.json'))
def nz(s): return ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(c))
def umbral(a):
    q = nz(a)
    if q.startswith('nuevos/05'): return 2
    if re.match(r'nuevos/(06|07|09|14|13) |05 - matrimonio|06 - discipulado', q): return 6
    if re.match(r'nuevos/12 |07 - historia', q): return 12
    return 22
sel = collections.defaultdict(list); tot = collections.Counter()
for l in open(f'{V}/puntajes_ref4.jsonl'):
    p = json.loads(l); a = p['archivo']; tot[a] += 1
    if a in dup: continue
    if p['puntaje'] >= umbral(a): sel[a].append({'pagina': p['pagina'], 'chars': p['chars'], 'puntaje': p['puntaje'], 'txt': p['txt']})
libros = {a: {'paginas': len(v), 'chars': sum(x['chars'] for x in v), 'de': tot[a], 'txt': v[0]['txt']} for a, v in sel.items()}
json.dump({'libros': libros, 'paginas': sel}, open(f'{V}/ref4_candidatos.json', 'w'), ensure_ascii=False)
print('libros con páginas relevantes', len(libros), '| páginas', sum(x['paginas'] for x in libros.values()), '| caracteres', sum(x['chars'] for x in libros.values()))
print('sin repetidos analizados', len(tot) - sum(1 for a in tot if a in dup), '| descartados por repetidos', sum(1 for a in tot if a in dup))
big = sorted(libros.items(), key=lambda kv: -kv[1]['chars'])
for a, v in big[:12]: print(v['paginas'], v['chars'] // 1000, 'k', a[-85:])
pocas = sum(1 for v in libros.values() if v['paginas'] < 5); print('con menos de 5 páginas:', pocas)
