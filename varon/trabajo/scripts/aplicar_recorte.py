#!/usr/bin/env python3
"""Aplica a dias/borradores/ lo que eligió wf_varon_recortar.js: los párrafos elegidos pasan a «profundizar» (con el título de su apartado).
Uso: aplicar_recorte.py <run_id> [...]"""
import json, glob, re, sys
V = '/home/user/trabajo/varon'
mov, hechos, saltos = {}, 0, 0
for run in sys.argv[1:]:
    fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
    lab = {}
    for l in open(fs[0]):
        e = json.loads(l)
        if e.get('type') == 'started':
            lab[e['agentId']] = e.get('label', '')
        elif e.get('type') == 'result' and lab.get(e.get('agentId'), '').startswith('recortar:'):
            v = e['result']; v = json.loads(v) if isinstance(v, str) else v
            for x in (v or {}).get('dias', []):
                mov[x['dia']] = x['mover']
for d, pares in mov.items():
    fn = f'{V}/dias/borradores/dia_{d:03d}.json'
    x = json.load(open(fn))
    sacar = sorted({(a, p) for a, p in pares if 0 <= a < len(x['apartados']) and 0 <= p < len(x['apartados'][a]['parrafos'])}, reverse=True)
    for a, p in sacar:
        ap = x['apartados'][a]
        if len(ap['parrafos']) <= 1:
            saltos += 1; continue
        q = ap['parrafos'].pop(p)
        x.setdefault('profundizar', []).append({'titulo': ap['titulo'], 'texto': q['texto'], 'fuentes': q.get('fuentes', [])})
        hechos += 1
    json.dump(x, open(fn, 'w'), ensure_ascii=False, indent=1)
print(f'{len(mov)} días recortados · {hechos} párrafos pasaron a profundizar · {saltos} salteados (dejaban un apartado vacío)')
