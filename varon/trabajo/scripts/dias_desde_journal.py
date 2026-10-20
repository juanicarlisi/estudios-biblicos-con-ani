#!/usr/bin/env python3
"""Guarda los días verificados (workflow varon-escribir) en varon/dias/dia_NNN.json; los borradores sin verificar, en dias/borradores/.

No pisa un día ya guardado (puede tener correcciones a mano), salvo con --pisar.
Uso: dias_desde_journal.py [--pisar] [run_id ...]   (por defecto, las corridas «Escribir» de RUNS.md)
"""
import json, glob, os, re, sys

V = '/home/user/trabajo/varon'
PISAR = '--pisar' in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith('--')]
runs = args or [r for l in open(f'{V}/RUNS.md') if 'Escribir' in l and 'piloto' not in l for r in re.findall(r'wf_[0-9a-f]{8}-[0-9a-f]{3}', l)]
os.makedirs(f'{V}/dias/borradores', exist_ok=True)
nuevos, borr = [], []
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
            et = lab.get(e.get('agentId'), '')
            m = re.match(r'(escribir|verificar):dia(\d+)', et)
            if not m:
                continue
            v = e['result']; v = json.loads(v) if isinstance(v, str) else v
            if not v:
                continue
            d = int(m.group(2)); v['dia'] = d
            if m.group(1) == 'escribir':
                json.dump(v, open(f'{V}/dias/borradores/dia_{d:03d}.json', 'w'), ensure_ascii=False, indent=1); borr.append(d)
            else:
                dst = f'{V}/dias/dia_{d:03d}.json'
                if PISAR or not os.path.exists(dst):
                    json.dump(v, open(dst, 'w'), ensure_ascii=False, indent=1); nuevos.append(d)
print('días verificados nuevos:', sorted(set(nuevos)), '| borradores:', len(set(borr)), '| total verificados:', len(glob.glob(f'{V}/dias/dia_*.json')))
