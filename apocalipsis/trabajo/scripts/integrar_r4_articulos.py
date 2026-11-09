#!/usr/bin/env python3
"""Notas NUEVAS (r4_*) para revisar cada artículo de Apocalipsis. Salida: SCRATCH/r4_arts/art_<ID>.txt
Misma selección que insumos_articulos.py (palabras clave, rango, panoramas), pero solo con notas r4."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U, pesos, insumos_articulos as IA
S = IA.S; OUT = S + '/r4_arts'; os.makedirs(OUT, exist_ok=True)
TOPE = int(os.environ.get('TOPE_R4', 70000))
N = [n for n in pesos.notas() if n['id'].startswith('r4_') and n['importancia'] >= 2]
def fuera_de_dias(n):
    r = U.rango(n['ref']); return n['ref'] in ('intro', 'tema') or not r or r[1] - r[0] + 1 > 12
for aid, a in IA.ARTS.items():
    base = []
    if a['grupo'] == 'panorama':
        ini, fin = U.rango(a['rango'].replace('–', '-'))
        base = [n for n in N if U.rango(n['ref']) and U.rango(n['ref'])[0] <= fin and U.rango(n['ref'])[1] >= ini and fuera_de_dias(n)]
    else:
        kw = IA.KW[aid]
        base = [n for n in N if re.search(kw, n['titulo'] + ' ' + n['contenido'] + ' ' + n.get('postura', ''), re.I)]
        if a['grupo'] == 'tema' and a['rango'] != 'libro':
            rr = U.rango(a['rango'])
            if rr: base = [n for n in base if (lambda r: (not r) or (r[0] <= rr[1] and r[1] >= rr[0]))(U.rango(n['ref']))]
        if aid in ('I1','I2','I3','I5'): base = [n for n in base if fuera_de_dias(n)] or base
    base.sort(key=lambda n: (-n['importancia'], -len(n['contenido'])))
    out = []; tot = 0
    for n in base:
        l = IA.linea(n)
        if tot + len(l) > TOPE: break
        out.append(l); tot += len(l)
    open(f'{OUT}/art_{aid}.txt', 'w').write(f"# ARTÍCULO {aid}: {a['titulo']} ({a['rango']}) — notas nuevas r4\n\n" + '\n'.join(out))
    print(aid, len(base), '->', len(out), tot)
