#!/usr/bin/env python3
"""Junta la clasificación de autores de REFERENCIA4 (journals de wf_clasificar_ref4.js) en clasif_ref4/clasificacion.json {ruta: registro}.
Uso: clasif_ref4.py <run_id ...>"""
import json, glob, sys, collections
V = '/home/user/trabajo/mujer/clasif_ref4'
fichas = {f['id']: f['path'] for f in json.load(open(f'{V}/_fichas.json'))['fichas']}
try: out = json.load(open(f'{V}/clasificacion.json'))
except OSError: out = {}
for run in sys.argv[1:]:
    j = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)[0]
    lab = {}
    for l in open(j):
        e = json.loads(l)
        if e.get('type') == 'started': lab[e['agentId']] = e.get('label', '')
        elif e.get('type') == 'result' and lab.get(e.get('agentId'), '').startswith('clasificar:'):
            v = e['result']; v = json.loads(v) if isinstance(v, str) else v
            lote = json.load(open(f"{V}/{lab[e['agentId']].split(':', 1)[1]}.json"))
            for x in v['libros']:
                if x['id'] in fichas: out[fichas[x['id']]] = x
json.dump(out, open(f'{V}/clasificacion.json', 'w'), ensure_ascii=False, indent=0)
print('clasificados', len(out), dict(collections.Counter(x['categoria'] for x in out.values())))
