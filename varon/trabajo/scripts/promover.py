#!/usr/bin/env python3
"""Pasa a dias/ (definitivos) los borradores sin flags bloqueantes según verificar_dia.py. Uso: promover.py"""
import json, glob, os, shutil
V = '/home/user/trabajo/varon'
NO_BLOQ = {'cifras_laxo', 'biblia_sin_dato'}
ok, quedan = [], []
for f in sorted(glob.glob(f'{V}/revision/verif/dia_*.json')):
    d = int(f[-8:-5]); r = json.load(open(f))
    src = f'{V}/dias/borradores/dia_{d:03d}.json'
    if not os.path.exists(src):
        continue
    if [y for y in r['flags'] if y['tipo'] not in NO_BLOQ]:
        quedan.append(d)
    else:
        shutil.copy(src, f'{V}/dias/dia_{d:03d}.json'); ok.append(d)
print(f'promovidos {len(ok)} · pendientes de reparar {len(quedan)} · definitivos en total {len(glob.glob(V + "/dias/dia_*.json"))}')
