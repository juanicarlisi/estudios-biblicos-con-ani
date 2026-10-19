#!/usr/bin/env python3
"""Aplica a trabajo/dias/ las correcciones de continuidad que el revisor escéptico confirmó.

Uso: aplicar_continuidad.py <run_id> [<run_id> ...]
Solo reemplaza un fragmento exacto dentro del campo indicado (p. ej. contexto.despues, secciones[2].notas[1]);
lo que no encuentra tal cual lo informa y no lo toca. Deja el registro en trabajo/logs/continuidad.json.
"""
import json, glob, re, sys

BASE = '/home/user/trabajo'
labels, hall, ver = {}, {}, {}
lineas = []
for run in sys.argv[1:]:
    fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
    lineas += open(fs[0]).read().splitlines()
for line in lineas:
    ev = json.loads(line)
    if ev.get('type') == 'started':
        labels[ev['agentId']] = ev.get('label', '')
    elif ev.get('type') == 'result':
        lab = labels.get(ev.get('agentId'), ''); v = ev['result']
        v = json.loads(v) if isinstance(v, str) else v
        k = int(lab.split(':v')[-1])
        (hall if lab.startswith('revisar:') else ver)[k] = v


def nodo(d, campo):
    """Devuelve (contenedor, clave) del campo, siguiendo «a.b[2].c[1]»; si el último es una nota, apunta a su texto."""
    partes = re.findall(r'[^.\[\]]+|\[\d+\]', campo)
    cur = d
    for p in partes[:-1]:
        cur = cur[int(p[1:-1])] if p.startswith('[') else cur[p]
    last = partes[-1]
    key = int(last[1:-1]) if last.startswith('[') else last
    if isinstance(cur[key], dict) and 'texto' in cur[key]:
        return cur[key], 'texto'
    return cur, key


registro = []
for k, h in sorted(hall.items()):
    vs = {x['indice']: x for x in (ver.get(k) or {}).get('veredictos', [])}
    for i, x in enumerate(h['hallazgos']):
        v = vs.get(i)
        estado = {'ventana': k, 'dia': x['dia'], 'campo': x['campo'], 'tipo': x['tipo'], 'problema': x['problema']}
        if not v or not v['real']:
            estado['resultado'] = 'descartado' + (f": {v['motivo']}" if v else ' (sin veredicto)')
            registro.append(estado); continue
        f = f"{BASE}/dias/dia_{x['dia']:02d}.json"
        d = json.load(open(f))
        try:
            cont, key = nodo(d, x['campo'])
            actual = cont[key]
        except (KeyError, IndexError, TypeError, ValueError):
            estado['resultado'] = 'campo no encontrado'; registro.append(estado); continue
        if not isinstance(actual, str) or x['texto_actual'] not in actual:
            estado['resultado'] = 'fragmento no encontrado tal cual'; registro.append(estado); continue
        cont[key] = actual.replace(x['texto_actual'], v['texto_nuevo'], 1)
        json.dump(d, open(f, 'w'), ensure_ascii=False, indent=1)
        estado.update(resultado='aplicado', antes=x['texto_actual'], despues=v['texto_nuevo'])
        registro.append(estado)
json.dump(registro, open(f'{BASE}/logs/continuidad.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(r['resultado'].split(':')[0] for r in registro))
for r in registro:
    if r['resultado'] != 'aplicado' and not r['resultado'].startswith('descartado'):
        print('  ', r['dia'], r['campo'], r['resultado'])
