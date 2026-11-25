#!/usr/bin/env python3
"""Quita el campo «para_orar» (oración final) de todos los días. Regla del estudio: los días no llevan oraciones escritas.
Uso: quitar_oraciones.py   (idempotente; se corre al terminar cada tanda de redactores)"""
import json, glob, os
V = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
n = 0
for f in sorted(glob.glob(f'{V}/dias/dia_*.json')):
    d = json.load(open(f))
    if 'para_orar' in d:
        del d['para_orar']; json.dump(d, open(f, 'w'), ensure_ascii=False, indent=2); n += 1
print('días sin oración final:', n)
