#!/usr/bin/env python3
"""Recoge las secciones (introducción, partes y temas) escritas por el workflow de artículos.

Uso: articulos_desde_journal.py <run_id> [<run_id> ...]
Guarda la versión verificada en trabajo/articulos/art_<ID>.json y el borrador en borrador_<ID>.json.
Nunca pisa una versión verificada con un borrador.
"""
import json, glob, sys, os

DST = '/home/user/trabajo/articulos'
os.makedirs(DST, exist_ok=True)
verif, borr = {}, {}
for run in sys.argv[1:]:
    fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
    if not fs:
        print('sin journal:', run); continue
    labels = {}
    for line in open(fs[0]):
        ev = json.loads(line)
        if ev.get('type') == 'started':
            labels[ev['agentId']] = ev.get('label', '')
        elif ev.get('type') == 'result':
            lab = labels.get(ev.get('agentId'), ''); v = ev.get('result')
            if isinstance(v, str):
                try:
                    v = json.loads(v)
                except Exception:
                    continue
            if not isinstance(v, dict) or 'apartados' not in v or ':art' not in lab:
                continue
            i = lab.split(':art')[-1]; v['id'] = i
            (verif if lab.startswith('verificar:') else borr)[i] = v
for i, v in verif.items():
    if not os.path.exists(f'{DST}/art_{i}.json'):   # no pisar correcciones hechas a mano
        json.dump(v, open(f'{DST}/art_{i}.json', 'w'), ensure_ascii=False, indent=1)
for i, v in borr.items():
    json.dump(v, open(f'{DST}/borrador_{i}.json', 'w'), ensure_ascii=False, indent=1)
arts = [a['id'] for a in json.load(open('/home/user/trabajo/plan/articulos.json'))]
listos = [a for a in arts if os.path.exists(f'{DST}/art_{a}.json')]
print('verificados en esta pasada:', sorted(verif), '| borradores:', sorted(borr))
print('listos:', len(listos), 'de', len(arts), '| faltan:', [a for a in arts if a not in listos])
