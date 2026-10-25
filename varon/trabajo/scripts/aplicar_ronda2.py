#!/usr/bin/env python3
"""Segunda ronda de la revisión del plan: junta las propuestas, arma el pedido para el verificador y aplica lo aceptado.

Uso:
  aplicar_ronda2.py juntar <run_id ...>       → escribe plan/revision/r2_ops.json y r2_lecturas.json (para el verificador)
  aplicar_ronda2.py aplicar <runs verificadores> → aplica sobre plan/plan_v2.json y deja plan.json, dias_plan.json,
                                                 plan/revision/mapa_v2_v3.json y plan/revision/cambios_r2.json
"""
import json, glob, re, sys, collections

V = '/home/user/trabajo/varon'
R = f'{V}/plan/revision'


def journal(run):
    fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
    lab = {}
    for l in open(fs[0]):
        e = json.loads(l)
        if e.get('type') == 'started':
            lab[e['agentId']] = e.get('label', '')
        elif e.get('type') == 'result':
            v = e['result']; v = json.loads(v) if isinstance(v, str) else v
            yield lab.get(e.get('agentId'), ''), v


def juntar(runs):
    ops, lects = [], []
    por = {}
    for run in runs:
        for et, v in journal(run):
            if v and 'propuestas' in v:
                por[et] = v['propuestas']
    for et in sorted(por):
        (lects if et == 'lecturas' else ops).extend(por[et])
    json.dump(ops, open(f'{R}/r2_ops.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(lects, open(f'{R}/r2_lecturas.json', 'w'), ensure_ascii=False, indent=0)
    print('agentes:', len(por), '| cambios de días y grupos:', len(ops), '| lecturas:', len(lects),
          '| por tipo:', dict(collections.Counter(p['tipo'] for p in ops)))


def aplicar(runs_ver):
    acept = []
    for run in runs_ver:
        for lab, v in journal(run):
            if not lab.startswith('verificar:') or not v:
                continue
            lote = json.load(open(f'{R}/r2_lote_{lab.split(":", 1)[1]}.json'))
            for x in v.get('veredictos', []):
                if x['aceptar'] and 0 <= x['indice'] < len(lote):
                    c = x.get('corregida') or {}
                    acept.append(c if c.get('tipo') else lote[x['indice']])
    plan = json.load(open(f'{V}/plan/plan_v2.json'))
    det = json.load(open(f'{V}/plan/dias_plan_v2.json'))
    grupos = json.load(open(f'{V}/plan/grupos/_grupos.json'))
    partes = [p['id'] for p in json.load(open(f'{V}/plan/partes.json'))]
    dias = {k: {**v, 'grupos': list(v['grupos']), 'web': list(v['web']), 'enfoque': list(v.get('enfoque', []))} for k, v in det.items()}
    orden = {s: [str(x['dia']) for x in plan if x['parte'] == s] for s in partes}
    alias, fuera, log = {}, set(), []

    def res(d):
        d = str(d)
        while d in alias:
            d = alias[d]
        return d if d in dias and d not in fuera else None

    def donde(g):
        return next((k for k, v in dias.items() if k not in fuera and g in v['grupos']), None)

    def campos(dst, p, sin=()):
        for a, b in (('titulo_nuevo', 'titulo'), ('objetivo_nuevo', 'objetivo'), ('contenido_nuevo', 'contenido'), ('lectura_nueva', 'lectura')):
            if p.get(a) and a not in sin:
                dst[b] = p[a]

    por = collections.defaultdict(list)
    for p in acept:
        por[p['tipo']].append(p)
    for p in por['mover_grupos']:
        dst = res(p.get('destino'))
        if not dst:
            log.append(['mover_grupos', 'destino inexistente', p['problema']]); continue
        ms = []
        for g in p.get('grupos', []):
            o = donde(g)
            if o and o != dst:
                dias[o]['grupos'].remove(g); dias[dst]['grupos'].append(g); ms.append(g)
        campos(dias[dst], p, sin=('titulo_nuevo', 'lectura_nueva'))
        log.append(['mover_grupos', f'{ms} → {dst}', p['problema']])
    for k, p in enumerate(por['nuevo_dia']):
        s, tras = p.get('parte'), res(p.get('despues_de'))
        gs = [g for g in p.get('grupos', []) if donde(g)]
        if s not in orden or not gs:
            log.append(['nuevo_dia', 'no aplicable', p['problema']]); continue
        nid = f'n{k + 1}'
        for g in gs:
            dias[donde(g)]['grupos'].remove(g)
        dias[nid] = {'parte': s, 'grupos': gs, 'web': [], 'enfoque': [], 'titulo': p.get('titulo_nuevo', ''), 'objetivo': p.get('objetivo_nuevo', ''),
                     'contenido': p.get('contenido_nuevo', ''), 'lectura': p.get('lectura_nueva', '')}
        pos = orden[s].index(tras) + 1 if tras in orden[s] else len(orden[s])
        orden[s].insert(pos, nid)
        log.append(['nuevo_dia', f'{nid} en {s} tras {tras}', p.get('titulo_nuevo')])
    for p in por['fusionar']:
        ds = [res(d) for d in p.get('dias', [])]
        ds = [d for i, d in enumerate(ds) if d and d not in ds[:i]]
        if len(ds) < 2:
            log.append(['fusionar', 'días ya no disponibles', p['problema']]); continue
        base = ds[0]
        for o in ds[1:]:
            dias[base]['grupos'] += dias[o]['grupos']; dias[base]['web'] += [w for w in dias[o]['web'] if w not in dias[base]['web']]
            dias[base]['enfoque'] += dias[o]['enfoque']; dias[o]['grupos'] = []; fuera.add(o); alias[o] = base
        campos(dias[base], p)
        log.append(['fusionar', f'{ds} → {base}', p['problema']])
    for p in por['retitular']:
        d = res((p.get('dias') or [0])[0])
        if d:
            campos(dias[d], p, sin=('lectura_nueva',)); log.append(['retitular', d, p.get('titulo_nuevo')])
    for p in por['enfoque']:
        d = res((p.get('dias') or [0])[0])
        if d and p.get('enfoque'):
            dias[d]['enfoque'].append(p['enfoque']); log.append(['enfoque', d, p['enfoque'][:100]])
    for p in por['lectura']:
        d = res((p.get('dias') or [0])[0])
        if d and p.get('lectura_nueva'):
            dias[d]['lectura'] = p['lectura_nueva']; log.append(['lectura', d, p['lectura_nueva']])
    for d, x in dias.items():
        if d not in fuera and not x['grupos']:
            fuera.add(d); log.append(['vaciado', d, x['titulo']])
    nuevo_plan, nuevo_det, ren, n = [], {}, {}, 0
    for s in partes:
        for d in orden[s]:
            if d in fuera:
                continue
            n += 1; x = dias[d]
            x['n_notas'] = sum(len(grupos[g]['ids']) for g in x['grupos'])
            ren[d] = n
            nuevo_plan.append({'dia': n, 'parte': s, 'titulo': x['titulo']})
            nuevo_det[n] = {**x, 'dia': n, 'parte': s}
    usados = [g for x in nuevo_det.values() for g in x['grupos']]
    assert len(usados) == len(set(usados)), 'grupo repetido'
    perdidos = {g for x in det.values() for g in x['grupos']} - set(usados)
    assert not perdidos, f'grupos perdidos: {sorted(perdidos)[:10]}'
    mapa = {}
    for k in det:
        d = k
        while d in alias:
            d = alias[d]
        mapa[k] = ren.get(d)
    json.dump(nuevo_plan, open(f'{V}/plan/plan.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(nuevo_det, open(f'{V}/plan/dias_plan.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(mapa, open(f'{R}/mapa_v2_v3.json', 'w'), indent=0)
    json.dump({'aplicado': log, 'aceptadas': acept}, open(f'{R}/cambios_r2.json', 'w'), ensure_ascii=False, indent=1)
    tam = sorted(x['n_notas'] for x in nuevo_det.values())
    print('aceptadas:', len(acept), dict(collections.Counter(p['tipo'] for p in acept)))
    print('días:', n, '| por parte:', {s: sum(1 for x in nuevo_plan if x['parte'] == s) for s in partes})
    print('notas por día: mín', tam[0], 'mediana', tam[len(tam) // 2], 'máx', tam[-1], '| fuera de rango:', [(d, x['n_notas']) for d, x in nuevo_det.items() if not 20 <= x['n_notas'] <= 100])
    print('no aplicadas:', [x for x in log if x[1] in ('destino inexistente', 'días ya no disponibles', 'no aplicable')])
    lect = collections.Counter(x['lectura'] for x in nuevo_det.values())
    print('lecturas repetidas:', [(k, v) for k, v in lect.items() if v > 1])


if __name__ == '__main__':
    if sys.argv[1] == 'juntar':
        juntar(sys.argv[2:])
    else:
        aplicar(sys.argv[2:])
