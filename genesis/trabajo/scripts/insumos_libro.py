#!/usr/bin/env python3
"""Material para la introducción, las partes y los temas del estudio.

Paso 1 (sin argumentos): junta las notas generales del libro (intro, tema y las que abarcan varias partes)
y las doctrinales de importancia 3 que la curaduría dejó fuera de los días, y las parte en
insumos/libro/cand_NN.txt (formato compacto) para que un clasificador las asigne a una sección.

Paso 2 (`--secciones <run_id | plan/asignacion_secciones.json>`): lee la asignación del clasificador y escribe
insumos/libro/sec_<ID>.txt con las notas completas de cada sección (biblioteca primero, luego por importancia).
"""
import json, glob, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import insumos_dias as I

BASE = '/home/user/trabajo'
DST = f'{BASE}/insumos/libro'
TIPOS_SOBRANTES = {'teologia_doctrina', 'cristo_en_genesis', 'matrimonio_familia', 'apologetica', 'dificultad_interpretaciones'}


def candidatas():
    plan = json.load(open(f'{BASE}/plan/plan.json'))
    dias = []
    for d in plan:
        c1, v1 = map(int, d['desde'].split(':')); c2, v2 = map(int, d['hasta'].split(':'))
        dias.append((I.idx(c1, v1), I.idx(c2, v2)))
    notas = I.cargar()
    por_id = {n['id']: n for n in notas}
    libro = []
    for n in notas:
        ref = str(n.get('ref', '')).strip().lower()
        if ref in ('intro', 'tema', ''):
            libro.append(n); continue
        r = I.rango(ref)
        if not r:
            continue
        a, b = r
        if b - a + 1 <= 60:
            continue
        ps = {plan[i]['parte'] for i, (x, y) in enumerate(dias) if not (b < x or a > y)}
        if len(ps) == 1 and b - a + 1 <= 900:
            continue                      # va al panorama de su parte
        libro.append(n)
    sob = []
    for f in sorted(glob.glob(f'{BASE}/insumos/sobrantes/*.json')):
        for i in json.load(open(f)):
            n = por_id.get(i)
            if n and int(n.get('importancia', 1)) == 3 and n.get('tipo') in TIPOS_SOBRANTES:
                sob.append(n)
    return libro, sob, por_id


def compacta(n):
    c = n.get('contenido', '').replace('\n', ' ')
    return f"[{n['id']}] Gn {n.get('ref','')} · {n.get('tipo','')} · imp {n.get('importancia','')} · {n['fuente'][:70]} | {n.get('titulo','')}: {c[:260]}"


def paso1():
    libro, sob, _ = candidatas()
    os.makedirs(DST, exist_ok=True)
    for f in glob.glob(f'{DST}/cand_*.txt'):
        os.remove(f)
    lineas = [compacta(n) for n in libro + sob]
    trozos, cur, tam = [], [], 0
    for l in lineas:
        if tam + len(l) > 95000 and cur:
            trozos.append(cur); cur, tam = [], 0
        cur.append(l); tam += len(l) + 1
    if cur:
        trozos.append(cur)
    for i, t in enumerate(trozos, 1):
        open(f'{DST}/cand_{i:02d}.txt', 'w').write('\n'.join(t) + '\n')
    print('libro', len(libro), '| sobrantes doctrinales', len(sob), '| archivos', len(trozos))


GRUPO = {'intro': 'Introducción a Génesis', 'parte': 'Panorama de una parte del libro', 'tema': 'Tema de Génesis'}
TOPE = 150000   # caracteres de notas por artículo


def cabecera(a, arts, plan):
    otras = '\n'.join(f"- {o['id']} «{o['titulo']}»: {o['alcance']}" for o in arts if o['id'] != a['id'] and o['grupo'] != 'parte')
    h = [f"ARTÍCULO {a['id']} · «{a['titulo']}» · {GRUPO[a['grupo']]}",
         f"Alcance: {a['alcance']}.", f"Largo del cuerpo principal: {a['largo']} palabras.", '',
         'Las otras secciones de la introducción y de los temas (no desarrolles lo que les toca a ellas; a lo sumo mencionalo en una frase):', otras]
    if a['grupo'] == 'parte':
        h += ['', f"Los días del plan de lectura en esta parte (Gn {a['rango']}):"]
        h += [f"Día {d['dia']} · Gn {d['desde']}–{d['hasta']} · {d['titulo']}" for d in plan if d['parte'] == a['parte']]
    return '\n'.join(h)


def paso2(run):
    _, _, por_id = candidatas()
    arts = json.load(open(f'{BASE}/plan/articulos.json'))
    plan = json.load(open(f'{BASE}/plan/plan.json'))
    labels, secs = {}, collections.defaultdict(list)
    if run.endswith('.json'):            # asignación ya guardada (plan/asignacion_secciones.json)
        for k, ids in json.load(open(run)).items():
            secs[k] = [i for i in ids if i in por_id]
        fs = [os.devnull]
    else:
        fs = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)
    for line in open(fs[0]):
        ev = json.loads(line)
        if ev.get('type') == 'started':
            labels[ev['agentId']] = ev.get('label', '')
        elif ev.get('type') == 'result' and labels.get(ev.get('agentId'), '').startswith('clasificar:'):
            v = ev.get('result')
            v = json.loads(v) if isinstance(v, str) else v
            for a in v.get('asignaciones', []):
                for i in a.get('ids', []):
                    if i in por_id:
                        secs[a['seccion'].strip().upper()].append(i)
    vistos = set()
    for a in arts:
        if a['grupo'] == 'parte':
            cuerpo = open(f"{BASE}/insumos/panorama_parte_{a['parte']}.txt").read()
            n_notas = cuerpo.count('\n[') + 1
        else:
            ns = []
            for i in secs.get(a['id'], []):
                if i not in vistos:
                    vistos.add(i); ns.append(por_id[i])
            ns.sort(key=lambda n: (-int(n.get('importancia', 1)), n['origen'] != 'biblio', n['id']))
            tomadas, tam = [], 0
            for n in ns:
                l = I.linea(n)
                if tam + len(l) > TOPE:
                    continue
                tomadas.append(l); tam += len(l) + 2
            cuerpo = '\n\n'.join(tomadas); n_notas = len(tomadas)
            if len(tomadas) < len(ns):
                print(f"  {a['id']}: quedaron afuera por tamaño {len(ns) - len(tomadas)} notas de importancia baja")
        open(f"{DST}/art_{a['id']}.txt", 'w').write(cabecera(a, arts, plan) + f'\n\n=== NOTAS ({n_notas}) ===\n' + cuerpo + '\n')
        print(a['id'], n_notas, len(cuerpo))


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--secciones':
        paso2(sys.argv[2])
    else:
        paso1()
