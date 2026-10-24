#!/usr/bin/env python3
"""Aplica a santiago/trabajo/dias/ las correcciones de continuidad que el revisor escéptico confirmó.

Lee TMP/revision/hallazgos_NN.json (del revisor) y TMP/revision/veredictos_NN.json (del escéptico) y reemplaza un fragmento exacto dentro del campo
indicado (p. ej. contexto.despues, secciones[2].notas[1]); lo que no encuentra tal cual lo informa y no lo toca. Deja el registro en trabajo/logs/continuidad.json.
Uso: aplicar_continuidad.py
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

REV = os.path.join(C.TMP, 'revision')
BASE = C.REPO_TRABAJO


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
for fh in sorted(glob.glob(os.path.join(REV, 'hallazgos_*.json'))):
    k = re.search(r'hallazgos_(\d+)', fh).group(1)
    hall = json.load(open(fh)).get('hallazgos', [])
    fv = os.path.join(REV, f'veredictos_{k}.json')
    vs = {x['indice']: x for x in (json.load(open(fv)).get('veredictos', []) if os.path.exists(fv) else [])}
    for i, x in enumerate(hall):
        v = vs.get(i)
        estado = {'ventana': k, 'dia': x['dia'], 'campo': x['campo'], 'tipo': x['tipo'], 'problema': x['problema']}
        if not v or not v['real']:
            estado['resultado'] = 'descartado' + (f": {v['motivo']}" if v else ' (sin veredicto)'); registro.append(estado); continue
        f = f"{BASE}/dias/dia_{x['dia']:02d}.json"
        d = json.load(open(f))
        try:
            cont, key = nodo(d, x['campo']); actual = cont[key]
        except (KeyError, IndexError, TypeError, ValueError):
            estado['resultado'] = 'campo no encontrado'; registro.append(estado); continue
        if not isinstance(actual, str) or x['texto_actual'] not in actual:
            estado['resultado'] = 'fragmento no encontrado tal cual'; registro.append(estado); continue
        cont[key] = actual.replace(x['texto_actual'], v['texto_nuevo'], 1)
        json.dump(d, open(f, 'w'), ensure_ascii=False, indent=1)
        estado.update(resultado='aplicado', antes=x['texto_actual'], despues=v['texto_nuevo']); registro.append(estado)
os.makedirs(f'{BASE}/logs', exist_ok=True)
json.dump(registro, open(f'{BASE}/logs/continuidad.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(r['resultado'].split(':')[0] for r in registro))
for r in registro:
    if r['resultado'] != 'aplicado' and not r['resultado'].startswith('descartado'):
        print('  ', r['dia'], r['campo'], r['resultado'])
