#!/usr/bin/env python3
"""Junta los planes de cada parte (workflow varon-planear) y numera los días de todo el estudio.

Escribe varon/plan/partes.json, varon/plan/plan.json [{dia, parte, titulo}] y varon/plan/dias_plan.json (detalle de cada día).
Avisa si quedaron grupos sin día ni descarte, o grupos repetidos.
Uso: plan_armar.py [run_id ...]   (por defecto, las corridas «Planear» de RUNS.md)
"""
import json, glob, re, sys

V = '/home/user/trabajo/varon'
ORDEN = 'ABCDEFGHIJKLMNOPQ'


def resultados(runs):
    out = {}
    for run in runs:
        fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
        if not fs:
            continue
        lab = {}
        for l in open(fs[0]):
            e = json.loads(l)
            if e.get('type') == 'started':
                lab[e['agentId']] = e.get('label', '')
            elif e.get('type') == 'result' and lab.get(e.get('agentId'), '').startswith('planear:'):
                v = e['result']; v = json.loads(v) if isinstance(v, str) else v
                out[lab[e['agentId']].split(':', 1)[1]] = v
    return out


def main():
    runs = sys.argv[1:] or [r for l in open(f'{V}/RUNS.md') if 'Planear' in l and 'piloto' not in l for r in re.findall(r'wf_[0-9a-f]{8}-[0-9a-f]{3}', l)]
    res = resultados(runs)
    grupos = json.load(open(f'{V}/plan/grupos/_grupos.json'))
    web = json.load(open(f'{V}/web/datos.json'))
    partes, plan, detalle, usados, problemas = [], [], {}, {}, []
    n = 0
    for k, s in enumerate(ORDEN, 1):
        r = res.get(s)
        if not r:
            problemas.append(f'parte {s}: sin plan'); continue
        partes.append({'id': s, 'numero': str(k), 'titulo': r['parte']['titulo'], 'bajada': r['parte']['bajada']})
        for d in r['dias']:
            n += 1
            gs = []
            for g in d['grupos']:
                if g not in grupos:
                    problemas.append(f'día {n}: grupo inexistente {g}')
                elif g in usados:
                    problemas.append(f'grupo {g} repetido en los días {usados[g]} y {n}')
                else:
                    usados[g] = n; gs.append(g)
            ws = [w for w in d['web'] if w in web]
            plan.append({'dia': n, 'parte': s, 'titulo': d['titulo']})
            detalle[n] = {**d, 'dia': n, 'parte': s, 'grupos': gs, 'web': ws,
                          'n_notas': sum(len(grupos[g]['ids']) for g in gs)}
        desc = {x['grupo'] for x in r['descartados']}
        for g, v in grupos.items():
            if v['seccion'] == s and g not in usados and g not in desc:
                problemas.append(f'grupo {g} ({v["tema"]}) sin día ni descarte')
    json.dump(partes, open(f'{V}/plan/partes.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(plan, open(f'{V}/plan/plan.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(detalle, open(f'{V}/plan/dias_plan.json', 'w'), ensure_ascii=False, indent=1)
    # texto del plan entero para la revisión (wf_varon_revisar_plan.js)
    rv = []
    for p in partes:
        rv += ['', f"# PARTE {p['numero']} · {p['titulo']} — {p['bajada']}"]
        for x in plan:
            if x['parte'] != p['id']:
                continue
            d = detalle[x['dia']]
            rv.append(f"\nDía {x['dia']}: {d['titulo']} ({d['n_notas']} notas) · lectura: {d['lectura']}\n  objetivo: {d['objetivo']}\n  cubre: {d['contenido']}")
            rv += [f"  - {g}: {grupos[g]['tema']} ({len(grupos[g]['ids'])})" for g in d['grupos']]
    open(f'{V}/plan/revision_plan.txt', 'w').write('\n'.join(rv) + '\n')
    print('días:', n, '| por parte:', {p['id']: sum(1 for x in plan if x['parte'] == p['id']) for p in partes})
    tam = sorted(d['n_notas'] for d in detalle.values())
    if tam:
        print('notas por día: mín', tam[0], '| mediana', tam[len(tam) // 2], '| máx', tam[-1])
    print('problemas:', len(problemas)); print('\n'.join(problemas[:40]))


if __name__ == '__main__':
    main()
