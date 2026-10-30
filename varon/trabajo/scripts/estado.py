#!/usr/bin/env python3
"""Estado compacto del estudio del varón en UNA línea (lo imprime el hook de arranque de sesión). Sin argumentos."""
import json, glob, os
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = lambda p: len(glob.glob(os.path.join(V, p)))
try:
    plan = len(json.load(open(f'{V}/plan/plan.json')))
except OSError:
    plan = 0
flags = 0
for f in glob.glob(f'{V}/revision/verif/dia_*.json'):
    try:
        flags += any(y['tipo'] not in ('cifras_laxo', 'biblia_sin_dato') for y in json.load(open(f))['flags']) and not os.path.exists(f'{V}/dias/dia_{os.path.basename(f)[4:7]}.json')
    except (OSError, ValueError):
        pass
print(f'VARÓN · notas {n("notas/*.json")}/490 bloques · plan {plan} días · escritos {n("dias/borradores/dia_*.json")} · definitivos {n("dias/dia_*.json")} · con flags sin reparar {flags} · '
      f'web {n("web/datos.json")} · RETOMAR.md (leer solo la sección pertinente; grep -n "^## ")')
