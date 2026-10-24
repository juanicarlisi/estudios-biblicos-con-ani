#!/usr/bin/env python3
"""Material para la introducción, los panoramas de las partes, los temas y los anexos del estudio.

Paso 1 (`--candidatas`): junta las notas que no son de un día (las de «intro» y «tema», y las que abarcan más de 14 versículos) y las parte en
TMP/insumos/libro/cand_NN.txt (formato compacto) para que un clasificador las asigne a una sección.
Paso 2 (`--secciones`): lee la asignación de los clasificadores (TMP/insumos/libro/clasif_NN.json) y escribe TMP/insumos/libro/art_<ID>.txt con las notas
completas de cada sección: las que le asignaron + las de los pasajes que la sección trata (plan/articulos.json, campo «pasajes») de los tipos que le sirven,
primero las de la biblioteca y por importancia, hasta un tope de caracteres.
"""
import collections, glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C
import notas as N

DST = os.path.join(C.TMP, 'insumos', 'libro')
TOPE = 140000
TRAMO_DIA = 14
TIPOS_POR_GRUPO = {
    'intro': ['contexto_historico', 'cultura_costumbres', 'arqueologia_geografia', 'cronologia_fechas', 'personaje', 'estructura_bosquejo', 'dificultad_interpretaciones', 'teologia_doctrina'],
    'parte': ['estructura_bosquejo', 'explicacion_texto', 'teologia_doctrina', 'contexto_historico', 'conexion_biblica'],
    'tema': ['teologia_doctrina', 'dificultad_interpretaciones', 'apologetica', 'cristo_en_santiago', 'eco_de_jesus', 'conexion_biblica', 'aplicacion_practica', 'ilustracion', 'griego_palabra', 'matrimonio_familia', 'explicacion_texto'],
    'anexo': ['personaje', 'contexto_historico', 'cultura_costumbres', 'arqueologia_geografia', 'conexion_biblica', 'eco_de_jesus', 'griego_palabra', 'cronologia_fechas', 'explicacion_texto', 'ilustracion', 'teologia_doctrina'],
}
GRUPO = {'intro': 'Introducción a Santiago', 'parte': 'Panorama de una parte de la carta', 'tema': 'Tema de Santiago', 'anexo': 'Anexo de consulta'}


def compacta(n):
    c = str(n.get('contenido', '')).replace('\n', ' ')
    return f"[{n['id']}] Stg {n.get('ref', '')} · {n.get('tipo', '')} · imp {n.get('importancia', '')} · {n['fuente'][:60]} | {n.get('titulo', '')}: {c[:240]}"


def candidatas():
    notas = N.cargar()
    out = []
    for n in notas:
        r = N.rango(n.get('ref', ''))
        if r is None or r[1] - r[0] + 1 > TRAMO_DIA:
            out.append(n)
    return out


def paso1():
    os.makedirs(DST, exist_ok=True)
    for f in glob.glob(os.path.join(DST, 'cand_*.txt')):
        os.remove(f)
    lineas = [compacta(n) for n in candidatas()]
    trozos, cur, tam = [], [], 0
    for l in lineas:
        if tam + len(l) > 90000 and cur:
            trozos.append(cur); cur, tam = [], 0
        cur.append(l); tam += len(l) + 1
    if cur:
        trozos.append(cur)
    for i, t in enumerate(trozos, 1):
        open(os.path.join(DST, f'cand_{i:02d}.txt'), 'w').write('\n'.join(t) + '\n')
    print('notas candidatas', len(lineas), '| archivos', len(trozos))


def cabecera(a, arts, plan):
    otras = '\n'.join(f"- {o['id']} «{o['titulo']}»: {o['alcance']}" for o in arts if o['id'] != a['id'] and o['grupo'] != 'parte')
    h = [f"ARTÍCULO {a['id']} · «{a['titulo']}» · {GRUPO[a['grupo']]}", f"Alcance: {a['alcance']}.", f"Largo del cuerpo principal: {a['largo']} palabras.", '',
         'Las otras secciones de la introducción, los temas y los anexos (no desarrolles lo que les toca a ellas; a lo sumo mencionalo en una frase):', otras]
    if a['grupo'] == 'parte':
        h += ['', f"Los días del plan de lectura en esta parte (Stg {a['rango']}):"]
        h += [f"Día {d['dia']} · Stg {d['desde']}–{d['hasta']} · {d['titulo']}" for d in plan if d['parte'] == a['parte']]
    h += ['', 'Los temas y anexos a los que un día puede enviar a la persona (ids para el campo «anexos» de los días): ' + ', '.join(f"{o['id']} {o['titulo']}" for o in arts if o['grupo'] in ('tema', 'anexo'))]
    return '\n'.join(h)


def paso2():
    notas = N.cargar()
    por_id = {n['id']: n for n in notas}
    arts = json.load(open(os.path.join(C.REPO_TRABAJO, 'plan', 'articulos.json')))
    plan = json.load(open(os.path.join(C.REPO_TRABAJO, 'plan', 'plan.json')))
    asign = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(DST, 'clasif_*.json'))):
        for a in json.load(open(f)).get('asignaciones', []):
            for i in a.get('ids', []):
                if i in por_id:
                    asign[a['seccion'].strip().upper()].append(i)
    vistos_exclusivos = set()
    for a in arts:
        ids = list(dict.fromkeys(asign.get(a['id'], [])))
        extra = []
        tipos = set(TIPOS_POR_GRUPO[a['grupo']])
        rangos = [N.rango(p) for p in a.get('pasajes', [])]
        rangos = [r for r in rangos if r]
        if rangos:
            for n in notas:
                r = N.rango(n.get('ref', ''))
                if not r or n['id'] in ids or n.get('tipo') not in tipos:
                    continue
                if any(not (r[1] < x[0] or r[0] > x[1]) for x in rangos):
                    if a['grupo'] == 'parte' and r[1] - r[0] + 1 <= TRAMO_DIA and n.get('tipo') != 'estructura_bosquejo':
                        continue
                    extra.append(n['id'])
        todos = [por_id[i] for i in dict.fromkeys(ids + extra)]
        # prioridad: lo que asignó el clasificador, importancia, biblioteca primero
        asignadas = set(ids)
        todos.sort(key=lambda n: (n['id'] not in asignadas, -int(n.get('importancia', 1)), n['origen'] != 'biblio', n['id']))
        tomadas, tam = [], 0
        for n in todos:
            l = N.linea(n)
            if tam + len(l) > TOPE:
                continue
            tomadas.append(l); tam += len(l) + 2
        cuerpo = '\n\n'.join(tomadas)
        open(os.path.join(DST, f"art_{a['id']}.txt"), 'w').write(cabecera(a, arts, plan) + f'\n\n=== NOTAS ({len(tomadas)}) ===\n' + cuerpo + '\n')
        print(f"{a['id']:4s} asignadas {len(ids):4d} + por pasaje {len(extra):4d} → {len(tomadas):4d} notas, {len(cuerpo):7d} caracteres" + (f"  (quedaron afuera {len(todos) - len(tomadas)} por tamaño)" if len(todos) > len(tomadas) else ''))


if __name__ == '__main__':
    if '--secciones' in sys.argv:
        paso2()
    else:
        paso1()
