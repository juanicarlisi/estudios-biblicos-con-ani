#!/usr/bin/env python3
"""Estado compacto del estudio de Apocalipsis (reemplaza ls + leer RETOMAR + validar uno por uno).
Uso: estado.py            -> cuenta hechos/faltantes por tipo (días, artículos, diagramas)
     estado.py --validar  -> además valida lo existente y muestra SOLO los errores"""
import json, os, subprocess, sys
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
hd = [d for d in dias if hay(f'{T}/dias/dia_{d:02d}.json')]
ha = [a for a in arts if hay(f'{T}/articulos/art_{a}.json')]
hg = [g for g in dgs if hay(f'{T}/diagramas/{g}.json')]
print(f'días {len(hd)}/{len(dias)} · artículos {len(ha)}/{len(arts)} · diagramas {len(hg)}/{len(dgs)}')
print('faltan días:', [d for d in dias if d not in hd] or '-')
print('faltan artículos:', [a for a in arts if a not in ha] or '-')
print('faltan diagramas:', [g for g in dgs if g not in hg] or '-')
if '--validar' in sys.argv:
    validar('validar_dia.py', hd); validar('validar_articulo.py', ha); validar('validar_diagrama.py', hg)
    print('validación: sin más errores que los listados arriba')
