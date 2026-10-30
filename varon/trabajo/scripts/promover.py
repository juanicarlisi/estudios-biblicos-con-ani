#!/usr/bin/env python3
"""Pasa a dias/ (definitivos) los borradores sin flags bloqueantes según verificar_dia.py. Uso: promover.py"""
import json, glob, os, re
V = '/home/user/trabajo/varon'
NO_BLOQ = {'cifras_laxo', 'biblia_sin_dato'}
ok, quedan = [], []
MANUAL = set(json.load(open(f'{V}/plan/aceptados_manual.json'))) if os.path.exists(f'{V}/plan/aceptados_manual.json') else set()   # días revisados a mano (solo «apoyo» en párrafos de entrada)
for f in sorted(glob.glob(f'{V}/revision/verif/dia_*.json')):
    d = int(f[-8:-5]); r = json.load(open(f))
    src = f'{V}/dias/borradores/dia_{d:03d}.json'
    if not os.path.exists(src):
        continue
    if [y for y in r['flags'] if y['tipo'] not in NO_BLOQ] and d not in MANUAL:
        quedan.append(d)
    else:
        x = json.load(open(src))
        def limpiar(o):
            if isinstance(o, dict):
                for k, v in list(o.items()):
                    if k == 'fuentes' and isinstance(v, list):
                        o[k] = [i for i in v if re.match(r'^(?:[bo]_\d+#\d+|W\d+)$', i)]
                    else:
                        limpiar(v)
            elif isinstance(o, list):
                for v in o:
                    limpiar(v)
        limpiar(x)
        json.dump(x, open(f'{V}/dias/dia_{d:03d}.json', 'w'), ensure_ascii=False, indent=1); ok.append(d)
print(f'promovidos {len(ok)} · pendientes de reparar {len(quedan)} · definitivos en total {len(glob.glob(V + "/dias/dia_*.json"))}')
