#!/usr/bin/env python3
"""Aplica a dias/borradores/ las reparaciones de wf_varon_reparar.js. Después hay que volver a correr verificar_dia.py.
Uso: aplicar_reparaciones.py <run_id> [<run_id> ...]"""
import json, glob, re, sys
V = '/home/user/trabajo/varon'
sys.path.insert(0, f'{V}/scripts')
from dia_util import poner  # noqa: E402


def nodo(x, ruta):
    partes = re.findall(r'[^.\[\]]+|\[\d+\]', ruta)
    cur = x
    for p in partes[:-1]:
        cur = cur[int(p[1:-1])] if p.startswith('[') else cur[p]
    last = partes[-1]
    return cur, (int(last[1:-1]) if last.startswith('[') else last)


def main():
    cambios, aplicados, borrados, fallos = {}, 0, 0, 0
    for run in sys.argv[1:]:
        fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
        lab = {}
        for l in open(fs[0]):
            e = json.loads(l)
            if e.get('type') == 'started':
                lab[e['agentId']] = e.get('label', '')
            elif e.get('type') == 'result':
                et = lab.get(e.get('agentId'), '')
                v = e['result']; v = json.loads(v) if isinstance(v, str) else v
                m = re.match(r'reparar:dia(\d+)', et)
                if m and v:
                    cambios.setdefault(int(m.group(1)), []).extend(v['cambios'])
                elif et.startswith('reparar:grupo') and v:
                    for c in v['cambios']:
                        cambios.setdefault(int(c['dia']), []).append(c)
    for d, cs in cambios.items():
        fn = f'{V}/dias/borradores/dia_{d:03d}.json'
        x = json.load(open(fn))
        borrar = []
        for c in cs:
            try:
                if not c['texto'].strip():
                    borrar.append(c['ruta']); continue
                poner(x, c['ruta'], c['texto'])
                if c['ruta'].endswith('.texto') and c.get('fuentes'):
                    cont, k = nodo(x, c['ruta'])
                    if isinstance(cont, dict):
                        cont['fuentes'] = c['fuentes']
                aplicados += 1
            except (KeyError, IndexError, TypeError):
                fallos += 1
        # borrar de atrás hacia adelante los elementos de listas
        for ruta in sorted(borrar, reverse=True):
            m = re.match(r'^(.*)\[(\d+)\](?:\.texto|\.nota|\.postura|\.significado)$', ruta)
            try:
                if m and m.group(1):
                    cont, k = nodo(x, m.group(1) + '[0]')
                    lista = nodo(x, m.group(1) + '[0]')[0]
                    del lista[int(m.group(2))]; borrados += 1
                else:
                    fallos += 1
            except (KeyError, IndexError, TypeError):
                fallos += 1
        json.dump(x, open(fn, 'w'), ensure_ascii=False, indent=1)
    print(f'días reparados {len(cambios)} · textos corregidos {aplicados} · borrados {borrados} · fallos {fallos}')


if __name__ == '__main__':
    main()
