#!/usr/bin/env python3
"""Controles automáticos sobre los días y los artículos ya escritos.

- Cada id de «fuentes» debe existir y, en un día, figurar en su archivo de insumos (si no, la afirmación cita una nota que el escritor no tenía delante).
- El versículo clave y los rangos de las secciones deben caer dentro del pasaje del día.
- La grafía griega debe ser griega y figurar en el texto griego de Santiago; los versículos clave de los artículos deben ser referencias válidas.
- Campos vacíos que la app espera con contenido; extensión del cuerpo principal (20 a 30 minutos de lectura); estructura de los diagramas.
- Citas entre «» de más de cuatro palabras que no figuran en la RVR1960 de Santiago: aviso (pueden ser de otro libro; en ese caso conviene parafrasear).
Uso: validar.py [--dias 3,4] [--borradores] [--articulos]   (imprime un resumen y escribe trabajo/logs/validacion.json)
"""
import json, glob, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
import config as C
import notas as N
import griego as G

BASE = C.REPO_TRABAJO
PREF = 'borrador_' if '--borradores' in sys.argv else 'dia_'
SOLO = set(map(int, sys.argv[sys.argv.index('--dias') + 1].split(','))) if '--dias' in sys.argv else None
plan = {d['dia']: d for d in json.load(open(f'{BASE}/plan/plan.json'))}
texto_rvr = json.load(open(f'{BASE}/biblia/rvr1960_santiago.json'))['texto']
rvr_plano = ''
existentes = {n['id'] for n in N.cargar()}
problemas = {}
TIPOS_DIAGRAMA = {'pasos', 'escalera', 'comparacion', 'imagenes', 'tabla'}
ICONOS = set('ola hierba espejo freno timon fuego bestia fuente hoja uvas nube lluvia aceite corona balanza libro corazon boca oido moneda camino mano'.split())
formas_g, lemas_g = set(), set()
for ws in G.versos().values():
    for w in ws:
        formas_g.add(G.sin_acentos(w['palabra'])); lemas_g.add(G.sin_acentos(w['lema']))


def norm(s):
    s = unicodedata.normalize('NFKD', s)
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s if not unicodedata.combining(c)).lower())


rvr_plano = norm(' '.join(t for c in texto_rvr.values() for t in c.values()))


def ids_de(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'fuentes' and isinstance(v, list):
                out.update(v)
            else:
                ids_de(v, out)
    elif isinstance(o, list):
        for v in o:
            ids_de(v, out)
    return out


def textos_de(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in ('fuentes', 'notas_no_usadas'):
                textos_de(v, out)
    elif isinstance(o, list):
        for v in o:
            textos_de(v, out)
    elif isinstance(o, str):
        out.append(o)
    return out


def palabras_cuerpo(d):
    c = {k: v for k, v in d.items() if k not in ('profundizar', 'notas_no_usadas', 'minutos')}
    return sum(len(t.split()) for t in textos_de(c, []))


def dentro(ref, a, b):
    r = N.rango(ref)
    return r is not None and a <= r[0] and r[1] <= b


def citas_dudosas(d):
    out = []
    for t in textos_de(d, []):
        for q in re.findall(r'«([^»]{20,})»', t):
            if len(q.split()) >= 5 and norm(q) not in rvr_plano:
                out.append(q[:80])
    return out


def ref_valida(ref):
    ref = re.sub(r'^(Stg|Santiago)\.?\s*', '', ref.strip())
    return N.rango(ref) is not None and ':' in ref


def validar_dia(d, n):
    p = plan[n]; mal = []
    a, b = C.idx(*map(int, p['desde'].split(':'))), C.idx(*map(int, p['hasta'].split(':')))
    ins = os.path.join(C.TMP, 'insumos', f'dia_{n:02d}.txt')
    insumo = set(re.findall(r'^\[([^\]]+)\]', open(ins).read(), re.M)) if os.path.exists(ins) else None
    ids = ids_de(d, set())
    falt = sorted(i for i in ids if i not in existentes)
    if falt:
        mal.append(f'ids inexistentes: {falt}')
    if insumo is not None:
        ajenos = sorted(i for i in ids if i in existentes and i not in insumo)
        if ajenos:
            mal.append(f'ids fuera de su insumo: {ajenos}')
    for k in ('titulo', 'contexto', 'versiculo_clave', 'panorama', 'secciones', 'palabras', 'cristo', 'interpretaciones', 'biblioteca', 'conexiones',
              'para_vivir', 'para_conversar', 'para_orar', 'profundizar', 'minutos'):
        if k not in d:
            mal.append(f'falta el campo «{k}»')
    if mal and any(m.startswith('falta') for m in mal):
        return mal
    for k in ('antes', 'ahora', 'donde', 'cuando', 'despues'):
        if not str(d['contexto'].get(k, '')).strip():
            mal.append(f'contexto.{k} vacío')
    if (d['desde'], d['hasta']) != (p['desde'], p['hasta']) or d['dia'] != n:
        mal.append('desde/hasta/dia no coinciden con el plan')
    vk = d['versiculo_clave'].get('ref', '')
    if not dentro(vk, a, b):
        mal.append(f'versículo clave fuera del pasaje: {vk}')
    for s in d['secciones']:
        if not dentro(s['rango'], a, b):
            mal.append(f"sección fuera del pasaje: {s['rango']}")
        if not s['notas']:
            mal.append(f"sección vacía: {s['rango']}")
        for nt in s['notas']:
            if not nt.get('fuentes'):
                mal.append(f"nota sin fuentes en {s['rango']}: {nt['texto'][:50]}")
    for w in d['palabras']:
        g = w.get('griego', '')
        if g:
            for pal in re.findall(r'[Ͱ-Ͽἀ-῿]+', g):
                if G.sin_acentos(pal) not in formas_g and G.sin_acentos(pal) not in lemas_g:
                    mal.append(f'palabra griega que no figura en Santiago: {pal}')
            if not re.search(r'[Ͱ-Ͽἀ-῿]', g):
                mal.append(f'«griego» sin letras griegas: {g}')
    if len(d['para_conversar']) != 3:
        mal.append('para_conversar debe tener 3 preguntas')
    if not d['para_vivir']:
        mal.append('para_vivir vacío')
    g = d.get('diagrama')
    if g:
        if g.get('tipo') not in TIPOS_DIAGRAMA:
            mal.append(f"diagrama: tipo inválido {g.get('tipo')!r}")
        if g.get('tipo') in ('pasos', 'escalera', 'imagenes') and len(g.get('items', [])) < 2:
            mal.append('diagrama: faltan items')
        if g.get('tipo') == 'imagenes':
            for it in g.get('items', []):
                if it.get('icono') not in ICONOS:
                    mal.append(f"diagrama: icono desconocido {it.get('icono')!r}")
        if g.get('tipo') in ('comparacion', 'tabla') and (not g.get('columnas') or not g.get('filas')):
            mal.append('diagrama: faltan columnas o filas')
        if not g.get('fuentes'):
            mal.append('diagrama sin fuentes')
    for x in d.get('anexos', []):
        if not re.fullmatch(r'[TAI]\d+', x.get('id', '')):
            mal.append(f"anexo con id inválido: {x.get('id')}")
    pal = palabras_cuerpo(d)
    dudosas = citas_dudosas(d)
    if dudosas:
        mal.append(f'AVISO citas entre «» que no figuran en Santiago (RVR1960): {dudosas[:4]}')
    if pal > 3400:
        mal.append(f'AVISO cuerpo principal largo: {pal} palabras (objetivo 2.000 a 3.000)')
    d['_palabras'] = pal
    return mal


def validar_articulo(x, i):
    mal = []
    ins = os.path.join(C.TMP, 'insumos', 'libro', f'art_{i}.txt')
    insumo = set(re.findall(r'^\[([^\]]+)\]', open(ins).read(), re.M)) if os.path.exists(ins) else None
    ids = ids_de(x, set())
    falt = sorted(j for j in ids if j not in existentes)
    if falt:
        mal.append(f'ids inexistentes: {falt}')
    if insumo is not None:
        ajenos = sorted(j for j in ids if j in existentes and j not in insumo)
        if ajenos:
            mal.append(f'ids fuera de su insumo: {ajenos}')
    for v in x.get('versiculos', []):
        if not ref_valida(v['ref']):
            mal.append(f"versículo no válido: {v['ref']}")
    for w in x.get('palabras', []):
        g = w.get('griego', '')
        for pal in re.findall(r'[Ͱ-Ͽἀ-῿]+', g or ''):
            if G.sin_acentos(pal) not in formas_g and G.sin_acentos(pal) not in lemas_g:
                mal.append(f'palabra griega que no figura en Santiago: {pal}')
    dudosas = citas_dudosas(x)
    if dudosas:
        mal.append(f'AVISO citas entre «» que no figuran en Santiago (RVR1960): {dudosas[:4]}')
    return mal


if __name__ == '__main__':
    resumen = []
    for f in sorted(glob.glob(f'{BASE}/dias/{PREF}*.json')):
        d = json.load(open(f)); n = d['dia']
        if SOLO and n not in SOLO:
            continue
        mal = validar_dia(d, n)
        resumen.append((n, d.get('_palabras', 0)))
        if mal:
            problemas[f'dia {n}'] = mal
    if '--articulos' in sys.argv or not SOLO:
        for f in sorted(glob.glob(f'{BASE}/articulos/art_*.json')):
            x = json.load(open(f)); i = x['id']
            mal = validar_articulo(x, i)
            if mal:
                problemas[f'art {i}'] = mal
    os.makedirs(f'{BASE}/logs', exist_ok=True)
    json.dump(problemas, open(f'{BASE}/logs/validacion.json', 'w'), ensure_ascii=False, indent=1)
    for k, v in problemas.items():
        print(k)
        for m in v:
            print('   ', m[:300])
    print('días revisados:', len(resumen), '| palabras del cuerpo principal (mín/prom/máx):',
          (min(p for _, p in resumen), sum(p for _, p in resumen) // max(1, len(resumen)), max(p for _, p in resumen)) if resumen else '-')
    print('con observaciones:', len(problemas))
