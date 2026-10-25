#!/usr/bin/env python3
"""Arma la entrada de la revisión del plan: el plan corto entero (título, objetivo, lectura) y el detalle de cada parte.

Escribe varon/plan/revision/plan_corto.txt y varon/plan/revision/parte_<S>.txt (con los grupos de cada día).
"""
import json, os

V = '/home/user/trabajo/varon'


def main():
    plan = json.load(open(f'{V}/plan/plan.json'))
    partes = json.load(open(f'{V}/plan/partes.json'))
    det = {int(k): v for k, v in json.load(open(f'{V}/plan/dias_plan.json')).items()}
    grupos = json.load(open(f'{V}/plan/grupos/_grupos.json'))
    d = f'{V}/plan/revision'
    os.makedirs(d, exist_ok=True)
    corto = []
    for p in partes:
        corto.append(f"\n# PARTE {p['numero']} ({p['id']}) · {p['titulo']} — {p['bajada']}")
        det_p = [f"# PARTE {p['numero']} ({p['id']}) · {p['titulo']} — {p['bajada']}"]
        for x in plan:
            if x['parte'] != p['id']:
                continue
            y = det[x['dia']]
            corto.append(f"Día {x['dia']}: {y['titulo']} — {y['objetivo']} ({y['n_notas']} notas · {y['lectura']})")
            det_p.append(f"\nDía {x['dia']}: {y['titulo']} ({y['n_notas']} notas) · lectura: {y['lectura']}\n  objetivo: {y['objetivo']}\n  cubre: {y['contenido']}")
            det_p += [f"  - {g}: {grupos[g]['tema']} ({len(grupos[g]['ids'])}) — {grupos[g]['resumen']}" for g in y['grupos']]
        open(f'{d}/parte_{p["id"]}.txt', 'w').write('\n'.join(det_p) + '\n')
    open(f'{d}/plan_corto.txt', 'w').write('\n'.join(corto) + '\n')
    print('plan corto:', len('\n'.join(corto)), 'caracteres | partes:', {p['id']: os.path.getsize(f"{d}/parte_{p['id']}.txt") for p in partes})


if __name__ == '__main__':
    main()
