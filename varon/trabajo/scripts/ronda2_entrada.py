#!/usr/bin/env python3
"""Entrada de la segunda ronda de revisión del plan (sobre el plan v2).

Escribe varon/plan/revision/notas_r2.json (las «nota» aceptadas en la ronda 1, con los números de día pasados al plan v2)
y varon/plan/revision/lecturas.txt (cada día con su lectura y los pasajes que más citan sus notas).
"""
import json, re, sys, collections

V = '/home/user/trabajo/varon'
sys.path.insert(0, f'{V}/scripts')
from grupos_entrada import notas  # noqa: E402
from rvr import normalizar  # noqa: E402


def main():
    mapa = json.load(open(f'{V}/plan/revision/mapa_v1_v2.json'))
    cambios = json.load(open(f'{V}/plan/revision/cambios.json'))
    out = []
    for p in cambios['propuestas']:
        q = p['propuesta']
        if p['aceptada'] and q['tipo'] == 'nota':
            texto = q['problema'] + ' ' + q.get('propuesta', '')
            nums = sorted({int(n) for n in re.findall(r'\b(\d{1,3})\b', texto) if 1 <= int(n) <= 544} | set(q['dias']))
            out.append({'parte': p['item'], 'dias_v1': q['dias'], 'dias_v2': sorted({mapa.get(str(d)) for d in q['dias'] if mapa.get(str(d))}),
                        'mapa_v1_v2': {n: mapa.get(str(n)) for n in nums},
                        'texto': texto, 'motivo_verificador': p['motivo']})
    json.dump(out, open(f'{V}/plan/revision/notas_r2.json', 'w'), ensure_ascii=False, indent=1)
    # lecturas y pasajes de cada día
    plan = json.load(open(f'{V}/plan/plan.json'))
    det = json.load(open(f'{V}/plan/dias_plan.json'))
    grupos = json.load(open(f'{V}/plan/grupos/_grupos.json'))
    todas = dict(notas())
    lin = ['día | parte | título | lectura actual | pasajes más citados por sus notas (veces)']
    for x in plan:
        y = det[str(x['dia'])]
        c = collections.Counter()
        for g in y['grupos']:
            for i in grupos[g]['ids']:
                for r in todas[i].get('refs', []):
                    n = normalizar(r.split(';')[0].strip())
                    if n:
                        (nombre, _), cap, v1, v2 = n
                        c[f'{nombre} {cap}:{v1}' + (f'-{v2}' if v2 != v1 else '')] += 1
        lin.append(f"{x['dia']} | {x['parte']} | {y['titulo']} | {y['lectura']} | " + ', '.join(f'{r} ({k})' for r, k in c.most_common(8)))
    open(f'{V}/plan/revision/lecturas.txt', 'w').write('\n'.join(lin) + '\n')
    print('notas:', len(out), '| días en lecturas.txt:', len(plan))


if __name__ == '__main__':
    main()
