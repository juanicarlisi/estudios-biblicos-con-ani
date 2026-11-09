#!/usr/bin/env python3
"""Estado compacto del estudio de 1 Pedro a Judas (reemplaza ls + leer RETOMAR + validar uno por uno).
Uso: estado.py            -> cuenta hechos/faltantes por tipo (días, artículos, diagramas)
     estado.py --validar  -> además valida lo existente y muestra SOLO los errores
     estado.py --bloques  -> además lista los bloques sin extraer"""
import json, os, re, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); T = AQUI + '/..'
def ids_plan():
    dias = [d['dia'] for d in json.load(open(T + '/plan/plan.json'))['dias']]
    arts = [a['id'] for a in json.load(open(T + '/plan/articulos.json'))]
    dgs = list(json.load(open(T + '/plan/visuales.json'))['diagramas'])
    return dias, arts, dgs
def hay(ruta): return os.path.exists(ruta)
def validar(script, ids):
    if not ids: return
    r = subprocess.run([sys.executable, f'{AQUI}/{script}', *map(str, ids)], capture_output=True, text=True)
    bloque = None
    for l in r.stdout.splitlines():
        if not l.startswith('  '): bloque = l
        elif 'ERROR' in l: print(f'  {bloque} {l.strip()}')
dias, arts, dgs = ids_plan()
import glob
ext = {os.path.basename(f)[:-5].rsplit('_', 1)[0] if re.search(r'_[a-z]{1,2}\.json$', f) else os.path.basename(f)[:-5] for f in glob.glob(T + '/extracciones/*.json')}
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
try: bl = [b['id'] for b in json.load(open(S + '/pj_bloques/_indice.json'))]
except FileNotFoundError: bl = []
print(f'extracción {len([b for b in bl if b in ext])}/{len(bl)} bloques' + (' (plan de días PROVISORIO: rehacer con plan_dias.py al terminar la extracción)' if len([b for b in bl if b in ext]) < len(bl) else ''))
hd = [d for d in dias if hay(f'{T}/dias/dia_{d:02d}.json')]
ha = [a for a in arts if hay(f'{T}/articulos/art_{a}.json')]
hg = [g for g in dgs if hay(f'{T}/diagramas/{g}.json')]
print(f'días {len(hd)}/{len(dias)} · artículos {len(ha)}/{len(arts)} · diagramas {len(hg)}/{len(dgs)}')
if '--bloques' in sys.argv: print('faltan bloques:', [b for b in bl if b not in ext] or '-')
print('faltan días:', [d for d in dias if d not in hd] or '-')
print('faltan artículos:', [a for a in arts if a not in ha] or '-')
print('faltan diagramas:', [g for g in dgs if g not in hg] or '-')
if '--validar' in sys.argv:
    validar('validar_dia.py', hd); validar('validar_articulo.py', ha); validar('validar_diagrama.py', hg)
    print('validación: sin más errores que los listados arriba')
