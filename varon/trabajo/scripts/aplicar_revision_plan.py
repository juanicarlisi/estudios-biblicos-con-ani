#!/usr/bin/env python3
"""Aplica al plan las propuestas de la revisión (wf_varon_revisar_plan.js) que el verificador aceptó, y renumera.

Parte de plan/plan_v1.json y plan/dias_plan_v1.json (el plan tal como lo dejaron los planificadores).
Orden de aplicación: mover grupos, fusionar, separar, retitular, reordenar. Las «nota» se juntan en un informe.
Escribe plan/plan.json, plan/dias_plan.json, plan/revision/cambios.json y plan/revision/renumeracion.json.
Uso: aplicar_revision_plan.py [run_id ...]   (por defecto, las corridas «Revisar plan» de RUNS.md)
"""
import json, glob, re, sys, collections

V = '/home/user/trabajo/varon'
MIRADAS = ['superposicion', 'huecos']   # mismo orden que en wf_varon_revisar_plan.js


def leer(runs):
    rev, ver = {}, {}
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
                v = e['result']; v = json.loads(v) if isinstance(v, str) else v
                et = lab.get(e.get('agentId'), '')
                if et.startswith('revisar:'):
                    rev[et.split(':', 1)[1]] = v
                elif et.startswith('verificar:'):
                    ver[et.split(':', 1)[1]] = v
    aceptadas, todas = [], []
    items = sorted({k[len('parte_'):] for k in rev if k.startswith('parte_')} | ({'global'} if any(m in rev for m in MIRADAS) else set()))
    for it in items:
        ps = [p for m in MIRADAS if rev.get(m) for p in rev[m]['propuestas']] if it == 'global' else (rev.get(f'parte_{it}') or {}).get('propuestas', [])
        vs = {x['indice']: x for x in (ver.get(it) or {}).get('veredictos', [])}
        for i, p in enumerate(ps):
            v = vs.get(i)
            reg = {'item': it, 'propuesta': p, 'aceptada': bool(v and v['aceptar']), 'motivo': v['motivo'] if v else 'sin veredicto'}
            todas.append(reg)
            if v and v['aceptar']:
                aceptadas.append({**p, **{k: x for k, x in (v.get('corregida') or {}).items() if x not in (None, '', [], 0)}, 'item': it})
    return aceptadas, todas


def main():
    runs = sys.argv[1:] or [r for l in open(f'{V}/RUNS.md') if 'Revisar plan' in l for r in re.findall(r'wf_[0-9a-f]{8}-[0-9a-f]{3}', l)]
    acept, todas = leer(runs)
    plan = json.load(open(f'{V}/plan/plan_v1.json'))
    det = {int(k): v for k, v in json.load(open(f'{V}/plan/dias_plan_v1.json')).items()}
    grupos = json.load(open(f'{V}/plan/grupos/_grupos.json'))
    partes = [p['id'] for p in json.load(open(f'{V}/plan/partes.json'))]
    dias = {str(k): {**v, 'id': str(k), 'grupos': list(v['grupos']), 'web': list(v['web'])} for k, v in det.items()}
    orden = {s: [str(x['dia']) for x in plan if x['parte'] == s] for s in partes}
    alias, fuera, log = {}, set(), []

    def res(d):
        d = str(d)
        while d in alias:
            d = alias[d]
        return d if d in dias and d not in fuera else None

    def donde(g):
        for k, v in dias.items():
            if k not in fuera and g in v['grupos']:
                return k
        return None

    def campos(dst, p):
        for a, b in (('titulo_nuevo', 'titulo'), ('objetivo_nuevo', 'objetivo'), ('contenido_nuevo', 'contenido'), ('lectura_nueva', 'lectura')):
            if p.get(a):
                dst[b] = p[a]

    por_tipo = collections.defaultdict(list)
    for p in acept:
        por_tipo[p['tipo']].append(p)
    for p in por_tipo['mover_grupos']:
        dst = res(p.get('destino'))
        if not dst:
            log.append(('mover_grupos', 'destino inexistente', p)); continue
        movidos = []
        for g in p.get('grupos', []):
            o = donde(g)
            if o and o != dst:
                dias[o]['grupos'].remove(g); dias[dst]['grupos'].append(g); movidos.append(g)
        campos(dias[dst], {k: v for k, v in p.items() if k != 'titulo_nuevo' and k != 'lectura_nueva'})
        log.append(('mover_grupos', f'{movidos} → {dst}', p['problema']))
    for p in por_tipo['fusionar']:
        ds = [res(d) for d in p.get('dias', [])]
        ds = [d for i, d in enumerate(ds) if d and d not in ds[:i]]
        if len(ds) < 2:
            log.append(('fusionar', 'días ya no disponibles', p)); continue
        base = ds[0]
        for o in ds[1:]:
            dias[base]['grupos'] += dias[o]['grupos']; dias[base]['web'] += [w for w in dias[o]['web'] if w not in dias[base]['web']]
            dias[o]['grupos'] = []; fuera.add(o); alias[o] = base
        campos(dias[base], p)
        log.append(('fusionar', f'{ds} → {base}', p['problema']))
    for p in por_tipo['separar']:
        d = res((p.get('dias') or [0])[0])
        gs = [g for g in p.get('grupos', []) if d and g in dias[d]['grupos']]
        if not d or not gs or len(gs) == len(dias[d]['grupos']):
            log.append(('separar', 'no aplicable', p)); continue
        nuevo = d + 'b'
        while nuevo in dias:
            nuevo += 'b'
        dias[nuevo] = {**dias[d], 'id': nuevo, 'grupos': gs, 'web': [], 'titulo': p.get('titulo_nuevo') or dias[d]['titulo'] + ' (II)',
                       'objetivo': p.get('objetivo_nuevo') or dias[d]['objetivo'], 'contenido': p.get('contenido_nuevo') or '', 'lectura': p.get('lectura_nueva') or dias[d]['lectura']}
        dias[d]['grupos'] = [g for g in dias[d]['grupos'] if g not in gs]
        s = dias[d]['parte']; orden[s].insert(orden[s].index(d) + 1, nuevo)
        log.append(('separar', f'{d} → {nuevo}', p['problema']))
    for p in por_tipo['retitular']:
        d = res((p.get('dias') or [0])[0])
        if d:
            campos(dias[d], p); log.append(('retitular', d, p.get('titulo_nuevo')))
    for p in por_tipo['reordenar']:
        nuevo = [res(x) for x in p.get('orden_nuevo', [])]
        nuevo = [x for i, x in enumerate(nuevo) if x and x not in nuevo[:i]]
        if not nuevo:
            continue
        s = dias[nuevo[0]]['parte']
        actual = [x for x in orden[s] if x not in fuera]
        es_sep = lambda x: bool(re.search(r'b+$', x))
        base = [x for x in nuevo if x in actual and not es_sep(x)]
        base += [x for x in actual if not es_sep(x) and x not in base]
        final = []
        for x in base:
            final.append(x)
            final += [y for y in actual if re.fullmatch(re.escape(x) + 'b+', y)]
        orden[s] = final
        log.append(('reordenar', s, p['problema']))
    # los días que quedaron sin grupos (todo se mudó a otros días) desaparecen
    for d, x in dias.items():
        if d not in fuera and not x['grupos']:
            fuera.add(d); log.append(('vaciado', d, x['titulo']))
    # renumerar
    nuevo_plan, nuevo_det, ren, n = [], {}, {}, 0
    for s in partes:
        for d in orden[s]:
            if d in fuera:
                continue
            n += 1; x = dias[d]
            x['n_notas'] = sum(len(grupos[g]['ids']) for g in x['grupos'])
            ren[d] = n
            nuevo_plan.append({'dia': n, 'parte': s, 'titulo': x['titulo']})
            nuevo_det[n] = {k: v for k, v in x.items() if k != 'id'} | {'dia': n}
    usados = [g for x in nuevo_det.values() for g in x['grupos']]
    assert len(usados) == len(set(usados)), 'grupo repetido'
    perdidos = {g for x in det.values() for g in x['grupos']} - set(usados)
    assert not perdidos, f'grupos perdidos: {sorted(perdidos)[:10]}'
    json.dump(nuevo_plan, open(f'{V}/plan/plan.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(nuevo_det, open(f'{V}/plan/dias_plan.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(ren, open(f'{V}/plan/revision/renumeracion.json', 'w'), indent=0)
    mapa = {}
    for k in det:
        d = str(k)
        while d in alias:
            d = alias[d]
        mapa[str(k)] = ren.get(d)
    json.dump(mapa, open(f'{V}/plan/revision/mapa_v1_v2.json', 'w'), indent=0)
    json.dump({'aplicado': log, 'propuestas': todas}, open(f'{V}/plan/revision/cambios.json', 'w'), ensure_ascii=False, indent=1, default=str)
    tam = sorted(x['n_notas'] for x in nuevo_det.values())
    print(f'propuestas: {len(todas)} | aceptadas: {len(acept)} | por tipo:', dict(collections.Counter(p["tipo"] for p in acept)))
    print('días:', n, '| notas por día: mín', tam[0], 'mediana', tam[len(tam) // 2], 'máx', tam[-1])
    print('fuera de rango:', [(d, x['n_notas']) for d, x in nuevo_det.items() if not 15 <= x['n_notas'] <= 100])
    print('no aplicadas:', [(a, b) for a, b, _ in log if b in ('destino inexistente', 'días ya no disponibles', 'no aplicable')])


if __name__ == '__main__':
    main()
