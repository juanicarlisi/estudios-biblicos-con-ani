#!/usr/bin/env python3
"""Junta en una carpeta los días escritos por wf_varon_escribir2.js (sin pisar los que ya están).
Uso: recoger_dias.py <carpeta destino dentro de dias/> <run_id> [<run_id> ...]   (p. ej. borradores wf_xxx wf_yyy)
Si no se pasan run_id, usa las corridas «Escribir2» anotadas en RUNS.md."""
import json, glob, os, re, sys
V = '/home/user/trabajo/varon'
dest = f'{V}/dias/{sys.argv[1]}'
runs = sys.argv[2:] or [r for l in open(f'{V}/RUNS.md') if 'Escribir2' in l for r in re.findall(r'wf_[0-9a-f]{8}-[0-9a-f]{3}', l)]
os.makedirs(dest, exist_ok=True)
nuevos = []
for run in runs:
    fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
    if not fs:
        continue
    lab = {}
    for l in open(fs[0]):
        e = json.loads(l)
        if e.get('type') == 'started':
            lab[e['agentId']] = e.get('label', '')
        elif e.get('type') == 'result':
            m = re.match(r'escribir:dia(\d+)', lab.get(e.get('agentId'), ''))
            v = e['result']; v = json.loads(v) if isinstance(v, str) else v
            if m and v:
                d = int(m.group(1)); v['dia'] = d; fn = f'{dest}/dia_{d:03d}.json'
                if not os.path.exists(fn):
                    json.dump(v, open(fn, 'w'), ensure_ascii=False, indent=1); nuevos.append(d)
print(f'{len(nuevos)} días nuevos en dias/{sys.argv[1]}/ · total {len(glob.glob(dest + "/dia_*.json"))}')
