#!/usr/bin/env python3
"""Recoge los días escritos por los workflows de síntesis y los guarda en trabajo/dias/.

Uso: dias_desde_journal.py <run_id> [<run_id> ...]
Prefiere la versión verificada («verificar:diaNN»); si no está, guarda el borrador como dias/borrador_NN.json
y lo informa. Nunca pisa una versión verificada con un borrador.
"""
import json, glob, sys, os

DST = '/home/user/trabajo/dias'
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
            if not isinstance(v, dict) or 'dia' not in v:
                continue
            d = int(lab.split('dia')[-1]) if 'dia' in lab else v['dia']
            v['dia'] = d
            (verif if lab.startswith('verificar:') else borr)[d] = v
for d, v in verif.items():
    if not os.path.exists(f'{DST}/dia_{d:02d}.json'):   # no pisar correcciones hechas a mano
        json.dump(v, open(f'{DST}/dia_{d:02d}.json', 'w'), ensure_ascii=False, indent=1)
sin_verif = []
for d, v in borr.items():
    json.dump(v, open(f'{DST}/borrador_{d:02d}.json', 'w'), ensure_ascii=False, indent=1)
    if d not in verif and not os.path.exists(f'{DST}/dia_{d:02d}.json'):
        sin_verif.append(d)
listos = sorted(int(os.path.basename(f)[4:6]) for f in glob.glob(f'{DST}/dia_*.json'))
print('verificados en esta pasada:', sorted(verif), '| borradores sin verificar:', sorted(sin_verif))
print('días listos en total:', len(listos), '| faltan:', [d for d in range(1, 70) if d not in listos])
