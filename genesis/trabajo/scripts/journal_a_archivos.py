#!/usr/bin/env python3
"""Vuelca a archivos JSON los resultados estructurados de un workflow (journal.jsonl).

Uso: journal_a_archivos.py <run_id> <dir_salida> [prefijo_label]
Toma cada agente cuyo label empieza con el prefijo (por defecto «extraer:»), y guarda su resultado en
<dir_salida>/<id>.json, sin pisar un archivo existente con más notas.
"""
import json, os, sys, glob

run, dst = sys.argv[1], sys.argv[2]
pref = sys.argv[3] if len(sys.argv) > 3 else 'extraer:'
base = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
if not base:
    sys.exit(f'no encuentro el journal de {run}')
labels, n = {}, 0
for line in open(base[0]):
    ev = json.loads(line)
    if ev.get('type') == 'started':
        labels[ev['agentId']] = ev.get('label', '')
    elif ev.get('type') == 'result':
        lab = labels.get(ev.get('agentId'), '')
        if not lab.startswith(pref):
            continue
        val = ev.get('result')
        if isinstance(val, str):
            try:
                val = json.loads(val)
            except Exception:
                continue
        if not isinstance(val, dict) or 'notas' not in val:
            continue
        cid = lab[len(pref):]
        fn = os.path.join(dst, cid + '.json')
        if os.path.exists(fn):
            try:
                if len(json.load(open(fn)).get('notas', [])) >= len(val['notas']):
                    continue
            except Exception:
                pass
        val['bloque'] = cid
        os.makedirs(dst, exist_ok=True)
        json.dump(val, open(fn, 'w'), ensure_ascii=False, indent=1)
        n += 1
print(n, 'archivos escritos en', dst)
