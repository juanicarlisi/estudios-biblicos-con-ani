#!/usr/bin/env python3
"""Junta los grupos temáticos (workflow varon-agrupar) y arma la entrada de los planificadores de cada parte.

Escribe varon/plan/grupos/<tanda>.json, varon/plan/grupos/_grupos.json {clave: grupo} y varon/plan/planear/<S>.txt
(una línea por grupo) más varon/plan/planear/_web.txt (datos y artículos de la web).
Las notas que un agrupador olvidó van a un grupo «sin agrupar» de su tanda, para que no se pierdan.
Uso: planear_entrada.py [run_id ...]   (por defecto, las corridas «Agrupar» de RUNS.md que no son piloto)
"""
import json, glob, os, re, sys, collections

V = '/home/user/trabajo/varon'
sys.path.insert(0, f'{V}/scripts')
from grupos_entrada import notas  # noqa: E402


def etiqueta(autor):
    a = re.split(r'\s+y\s+|,|\(', autor or '')[0].strip()
    return a.split()[-1] if a else '?'


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
            elif e.get('type') == 'result' and lab.get(e.get('agentId'), '').startswith('agrupar:'):
                v = e['result']; v = json.loads(v) if isinstance(v, str) else v
                out[lab[e['agentId']].split(':', 1)[1]] = v
    return out


def main():
    runs = sys.argv[1:] or [r for l in open(f'{V}/RUNS.md') if 'Agrupar' in l and 'piloto' not in l for r in re.findall(r'wf_[0-9a-f]{8}-[0-9a-f]{3}', l)]
    res = resultados(runs)
    tandas = json.load(open(f'{V}/plan/grupos/_tandas.json'))
    todas = dict(notas())
    fuentes = json.load(open(f'{V}/bloques/_fuentes.json'))
    grupos, faltan_tandas, sueltas, fuera_n = {}, [], 0, 0
    for t in tandas:
        nombre = t['tanda']; r = res.get(nombre)
        if not r:
            faltan_tandas.append(nombre); continue
        json.dump(r, open(f'{V}/plan/grupos/{nombre}.json', 'w'), ensure_ascii=False, indent=0)
        ids_tanda = [l.split(' | ', 1)[0] for l in open(f'{V}/plan/grupos/{nombre}.txt') if l.strip()]
        vistos = set()
        clave_base = nombre[3:]                       # in_G_01 → G_01
        for k, g in enumerate(r['grupos'], 1):
            ids = [i for i in g['ids'] if i in todas and i not in vistos]
            vistos.update(ids)
            if ids:
                grupos[f'{clave_base}.{k:02d}'] = {'seccion': t['seccion'], 'tema': g['tema'], 'resumen': g['resumen'], 'ids': ids, 'refs': g.get('refs', [])}
        fuera = {f['id'] for f in r['fuera'] if f['id'] in todas and f['id'] not in vistos}
        fuera_n += len(fuera); vistos |= fuera
        resto = [i for i in ids_tanda if i not in vistos]
        if resto:
            sueltas += len(resto)
            grupos[f'{clave_base}.99'] = {'seccion': t['seccion'], 'tema': 'Notas sin agrupar de esta tanda', 'resumen': '; '.join(todas[i]['titulo'] for i in resto[:12]), 'ids': resto, 'refs': []}
    json.dump(grupos, open(f'{V}/plan/grupos/_grupos.json', 'w'), ensure_ascii=False, indent=0)
    os.makedirs(f'{V}/plan/planear', exist_ok=True)
    por = collections.defaultdict(list)
    for c, g in grupos.items():
        ns = [todas[i] for i in g['ids']]
        imp3 = sum(1 for n in ns if n.get('importancia') == 3)
        autores = collections.Counter(etiqueta(fuentes.get(n.get('fuente'), {}).get('autor')) for n in ns)
        personas = sorted({n['persona'] for n in ns if n.get('persona')})
        tipos = collections.Counter(n.get('tipo') for n in ns)
        por[g['seccion']].append(' | '.join([
            c, f"{len(ns)} notas ({imp3} de importancia 3)", g['tema'], g['resumen'], 'versículos: ' + ', '.join(g['refs'][:5]),
            'autores: ' + ', '.join(a for a, _ in autores.most_common(6)), ('personas: ' + ', '.join(personas[:6])) if personas else '',
            'tipos: ' + ', '.join(f'{k} {v}' for k, v in tipos.most_common(4))]))
    for s, ls in por.items():
        open(f'{V}/plan/planear/{s}.txt', 'w').write('\n'.join(ls) + '\n')
    web = json.load(open(f'{V}/web/datos.json')) if os.path.exists(f'{V}/web/datos.json') else {}
    lw = []
    for wid, w in web.items():
        if w['clase'] == 'dato':
            lw.append(f"{wid} | dato | {w['tema']} | {w['valor']} | {w['indicador']} | {w['ambito']} | {w['anio']} | {w['fuente']}")
        else:
            lw.append(f"{wid} | artículo | {w['tema']} | «{w['titulo']}» de {w['autor']} ({w['sitio']}) | ideas: {' / '.join(w['ideas_clave'][:3])}")
    open(f'{V}/plan/planear/_web.txt', 'w').write('\n'.join(lw) + '\n')
    # versión corta para las partes donde los datos son complemento
    lc = []
    for wid, w in web.items():
        if w['clase'] == 'dato':
            lc.append(f"{wid} | dato | {w['tema']} | {w['valor'][:110]} | {w['indicador'][:110]} | {w['ambito']} | {w['anio']}")
        else:
            lc.append(f"{wid} | artículo | {w['tema']} | «{w['titulo']}» de {w['autor']} ({w['etiqueta']})")
    open(f'{V}/plan/planear/_web_corto.txt', 'w').write('\n'.join(lc) + '\n')
    print(f'grupos: {len(grupos)} | notas fuera: {fuera_n} | sueltas: {sueltas} | tandas sin resultado: {faltan_tandas}')
    print('grupos por sección:', {s: len(v) for s, v in sorted(por.items())})


if __name__ == '__main__':
    main()
