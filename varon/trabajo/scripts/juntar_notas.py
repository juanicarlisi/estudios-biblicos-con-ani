#!/usr/bin/env python3
"""Junta las notas extraídas (journals de los workflows) en varon/notas/<bloque>.json y muestra el avance.
Uso: juntar_notas.py <run_id> [<run_id> ...]   (por defecto, las corridas anotadas en varon/RUNS.md)"""
import json, glob, os, re, sys, collections
V = '/home/user/trabajo/varon'
runs = sys.argv[1:] or [r for l in open(f'{V}/RUNS.md') if 'Web' not in l and 'piloto' not in l for r in re.findall(r'wf_[0-9a-f]{8}-[0-9a-f]{3}', l)]
os.makedirs(f'{V}/notas', exist_ok=True)
nuevos = 0
for run in runs:
    fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
    if not fs:
        continue
    lab = {}
    for l in open(fs[0]):
        e = json.loads(l)
        if e.get('type') == 'started':
            lab[e['agentId']] = e.get('label', '')
        elif e.get('type') == 'result' and lab.get(e.get('agentId'), '').startswith('extraer:'):
            v = e['result']; v = json.loads(v) if isinstance(v, str) else v
            b = lab[e['agentId']].split(':', 1)[1]
            dst = f'{V}/notas/{b}.json'
            if not os.path.exists(dst):
                json.dump(v, open(dst, 'w'), ensure_ascii=False); nuevos += 1
bl = sorted(glob.glob(f'{V}/notas/*.json'))
tot = collections.Counter(); n = 0
for f in bl:
    for x in json.load(open(f))['notas']:
        tot[x['seccion']] += 1; n += 1
esperados = len(glob.glob(f'{V}/bloques/b_*.txt')) + len(glob.glob(f'{V}/bloques/o_*.txt'))
print(f'bloques con notas: {len(bl)} de {esperados} (nuevos: {nuevos}) | notas: {n}')
print('por sección:', dict(sorted(tot.items())))
