#!/usr/bin/env python3
"""Aplica a varon/dias/ las correcciones de la revisión de continuidad y doctrina que el escéptico confirmó.

Uso: aplicar_continuidad.py <run_id> [<run_id> ...]
Solo reemplaza un fragmento exacto dentro del campo indicado (p. ej. apartados[2].parrafos[1].texto); lo que no
encuentra tal cual lo informa y no lo toca. Registro en varon/revision/continuidad_aplicada.json.
"""
import json, glob, re, sys, collections

V = '/home/user/trabajo/varon'
MIRADAS = ['continuidad', 'doctrina', '']   # '' = flujo de un solo agente por ventana (wf_varon_continuidad2.js)
rev, ver = collections.defaultdict(dict), {}
for run in sys.argv[1:]:
    fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
    labels = {}
    for line in open(fs[0]):
        ev = json.loads(line)
        if ev.get('type') == 'started':
            labels[ev['agentId']] = ev.get('label', '')
        elif ev.get('type') == 'result':
            lab = labels.get(ev.get('agentId'), ''); v = ev['result']
            v = json.loads(v) if isinstance(v, str) else v
            k = int(lab.split(':v')[-1])
            if lab.startswith('revisar:'):
                rev[k][lab.split(':')[1] if lab.count(':') > 1 else ''] = v
            elif lab.startswith('verificar:'):
                ver[k] = v


def nodo(d, campo):
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
for k in sorted(rev):
    hs = [h for m in MIRADAS if rev[k].get(m) for h in rev[k][m]['hallazgos']]
    vs = {x['indice']: x for x in (ver.get(k) or {}).get('veredictos', [])}
    for i, x in enumerate(hs):
        v = vs.get(i)
        if not ver.get(k) and x.get('texto_nuevo') is not None:
            v = {'real': True, 'texto_nuevo': x['texto_nuevo'], 'motivo': 'sin verificador (flujo de un agente)'}
        estado = {'ventana': k, 'dia': x['dia'], 'campo': x['campo'], 'tipo': x['tipo'], 'problema': x['problema']}
        if not v or not v['real']:
            estado['resultado'] = 'descartado' + (f": {v['motivo']}" if v else ' (sin veredicto)')
            registro.append(estado); continue
        f = f"{V}/dias/dia_{x['dia']:03d}.json"
        try:
            d = json.load(open(f))
            cont, key = nodo(d, x['campo'])
            actual = cont[key]
        except (OSError, KeyError, IndexError, TypeError, ValueError):
            estado['resultado'] = 'campo no encontrado'; registro.append(estado); continue
        if not isinstance(actual, str) or x['texto_actual'] not in actual:
            estado['resultado'] = 'fragmento no encontrado tal cual'; registro.append(estado); continue
        cont[key] = re.sub(r'\s{2,}', ' ', actual.replace(x['texto_actual'], v['texto_nuevo'], 1)).strip()
        json.dump(d, open(f, 'w'), ensure_ascii=False, indent=1)
        estado.update(resultado='aplicado', antes=x['texto_actual'], despues=v['texto_nuevo'])
        registro.append(estado)
viejo = json.load(open(f'{V}/revision/continuidad_aplicada.json')) if glob.glob(f'{V}/revision/continuidad_aplicada.json') else []
json.dump(viejo + registro, open(f'{V}/revision/continuidad_aplicada.json', 'w'), ensure_ascii=False, indent=1)
print(collections.Counter(r['resultado'].split(':')[0] for r in registro))
for r in registro:
    if r['resultado'] != 'aplicado' and not r['resultado'].startswith('descartado'):
        print('  ', r['dia'], r['campo'], r['resultado'])
