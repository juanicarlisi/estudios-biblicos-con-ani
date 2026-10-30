#!/usr/bin/env python3
"""Arma biblia/rvr.json (texto RVR1960 de los versículos clave de dias/) desde los capítulos ya bajados a biblia/cap/ (sin red).
Uso: rvr_desde_cache.py"""
import json, glob, os, sys
V = '/home/user/trabajo/varon'
sys.path.insert(0, f'{V}/scripts')
from rvr import normalizar
res, fallas, total = {}, [], 0
for f in sorted(glob.glob(f'{V}/dias/dia_*.json')):
    for v in json.load(open(f)).get('versiculos', []):
        r = v['ref']; n = normalizar(r)
        if not n:
            fallas.append(r); continue
        (nombre, osis), c, v1, v2 = n
        cap = json.load(open(f'{V}/biblia/cap/{osis}_{c}.json')) if os.path.exists(f'{V}/biblia/cap/{osis}_{c}.json') else {}
        vs = [cap.get(str(k), '') for k in range(v1, v2 + 1)]
        if all(vs):
            res[r] = ' '.join(vs); total += v2 - v1 + 1
        else:
            fallas.append(r)
json.dump(res, open(f'{V}/biblia/rvr.json', 'w'), ensure_ascii=False, indent=0)
print(f'{len(res)} referencias con texto · {total} versículos en total · sin texto: {len(fallas)} {fallas[:6]}')
