#!/usr/bin/env python3
"""Prepara, por día de Apocalipsis, las notas NUEVAS (r4_*) que caen en su rango, para revisar el día con ellas.
Salida: SCRATCH/r4_dias/dia_NN.txt (notas con id, ref, tipo, contenido, cita, página) y un resumen por día.
Las notas «tema»/«intro» se juntan en SCRATCH/r4_dias/_temas.txt (para los artículos).
Uso: integrar_r4.py [--min N]   (N = notas mínimas de importancia>=2 para listar el día; por defecto 2)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U, pesos
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
OUT = S + '/r4_dias'; os.makedirs(OUT, exist_ok=True)
AQUI = os.path.dirname(os.path.abspath(__file__))
mn = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 2
plan = json.load(open(AQUI + '/../plan/plan.json'))['dias']
notas = [n for n in pesos.notas() if n['id'].startswith('r4_')]
def fmt(n):
    s = f"[{n['id']}] {n['ref']} · {n['tipo']} · imp {n['importancia']} · {n.get('pagina','')}\n{n['contenido']}"
    if n.get('cita'): s += f"\nCITA: «{n['cita']}»"
    if n.get('postura'): s += f"\nPOSTURA: {n['postura']}"
    return s
res = []; ya = set()
for d in plan:
    ini, fin = d['ini'], d['fin']; sel = []
    for n in notas:
        r = U.rango(n['ref'])
        if not r or n['importancia'] < 2: continue
        a, b = r
        if b - a + 1 > 40 and not (ini <= a and b <= fin): continue   # notas de más de 40 vv: van a artículos
        if a <= fin and b >= ini and (a >= ini - 2 or (b <= fin + 2)): sel.append(n)
    if len(sel) >= mn:
        sel.sort(key=lambda n: (-n['importancia'], n['id']))
        open(f"{OUT}/dia_{d['dia']:02d}.txt", 'w').write('\n\n'.join(fmt(n) for n in sel))
        res.append((d['dia'], len(sel), sum(len(n['contenido']) for n in sel)))
        ya.update(n['id'] for n in sel)
tem = [n for n in notas if n['importancia'] >= 2 and (U.rango(n['ref']) is None or (U.rango(n['ref'])[1] - U.rango(n['ref'])[0] + 1) > 40) and n['id'] not in ya]
open(OUT + '/_temas.txt', 'w').write('\n\n'.join(fmt(n) for n in tem))
print(f'notas r4: {len(notas)}; días con material: {len(res)}/{len(plan)}; notas sueltas para artículos: {len(tem)}')
print('días (n.º, notas, chars):', res)
