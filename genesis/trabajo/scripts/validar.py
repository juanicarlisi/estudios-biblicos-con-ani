#!/usr/bin/env python3
"""Controles automáticos sobre los días y los artículos ya escritos.

- Cada id de "fuentes" debe existir y, en un día, figurar en su archivo de insumos (si no, la afirmación cita una nota
  que el escritor no tenía delante).
- El versículo clave y los rangos de las secciones deben caer dentro del pasaje del día.
- La grafía hebrea debe ser hebrea; los versículos clave de los artículos deben ser referencias de Génesis válidas.
- Campos vacíos que la app espera con contenido.
Uso: validar.py   (imprime un resumen y escribe trabajo/logs/validacion.json)
"""
import json, glob, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import insumos_dias as I

BASE = '/home/user/trabajo'
plan = {d['dia']: d for d in json.load(open(f'{BASE}/plan/plan.json'))}
rvr = json.load(open(f'{BASE}/biblia/rvr1960_genesis.json'))['texto']
existentes = {n['id'] for n in I.cargar()}
# ids de obras eliminadas o no confiables: no deben citarse nunca
_borr = set(json.load(open(f'{BASE}/borrado/archivos_borrados_claves.json')))
prohibidos = set()
for _f in glob.glob(f'{BASE}/extracciones/ref3/*.json'):
    _b = os.path.basename(_f)[:-5]
    for _i, _n in enumerate(json.load(open(_f))['notas'], 1):
        if _n.get('archivo') in _borr or 'adventista' in ((_n.get('autor') or '') + (_n.get('obra') or '')).lower():
            prohibidos.add(f'{_b}#{_i}')
problemas = {}


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


def dentro(ref, a, b):
    r = I.rango(ref)
    return r is not None and a <= r[0] and r[1] <= b


def ref_valida(ref):
    ref = re.sub(r'^(Gn|Gén|Génesis)\.?\s*', '', ref.strip())
    m = re.fullmatch(r'(\d+):(\d+)(?:-(\d+))?', ref.replace(' ', ''))
    if not m:
        return False
    c, v1, v2 = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2))
    return 1 <= c <= 50 and str(v1) in rvr[str(c)] and str(v2) in rvr[str(c)] and v2 >= v1


for f in sorted(glob.glob(f'{BASE}/dias/dia_*.json')):
    d = json.load(open(f)); n = d['dia']; p = plan[n]; mal = []
    c1, v1 = map(int, p['desde'].split(':')); c2, v2 = map(int, p['hasta'].split(':'))
    a, b = I.idx(c1, v1), I.idx(c2, v2)
    insumo = set(re.findall(r'^\[([^\]]+)\]', open(f'{BASE}/insumos/dia_{n:02d}.txt').read(), re.M))
    ids = ids_de(d, set())
    falt = sorted(i for i in ids if i not in existentes)
    if ids & prohibidos:
        mal.append(f'cita obras eliminadas: {sorted(ids & prohibidos)}')
    ajenos = sorted(i for i in ids if i in existentes and i not in insumo)
    if falt:
        mal.append(f'ids inexistentes: {falt}')
    if ajenos:
        mal.append(f'ids fuera de su insumo: {ajenos}')
    vk = d['versiculo_clave']['ref']
    if not dentro(vk, a, b):
        mal.append(f'versículo clave fuera del pasaje: {vk}')
    for s in d['secciones']:
        if not dentro(s['rango'], a, b):
            mal.append(f"sección fuera del pasaje: {s['rango']}")
        if not s['notas']:
            mal.append(f"sección vacía: {s['rango']}")
    for w in d['palabras']:
        if w.get('hebreo') and not re.search(r'[֐-׿]', w['hebreo']):
            mal.append(f"hebreo sin letras hebreas: {w['hebreo']}")
    sin = [k for k in ('para_conversar', 'para_orar', 'para_vivir') if not d.get(k)]
    if sin:
        mal.append(f'vacíos: {sin}')
    if mal:
        problemas[f'dia {n}'] = mal

for f in sorted(glob.glob(f'{BASE}/articulos/art_*.json')):
    x = json.load(open(f)); i = x['id']; mal = []
    insumo = set(re.findall(r'^\[([^\]]+)\]', open(f'{BASE}/insumos/libro/art_{i}.txt').read(), re.M))
    ids = ids_de(x, set())
    falt = sorted(j for j in ids if j not in existentes)
    if ids & prohibidos:
        mal.append(f'cita obras eliminadas: {sorted(ids & prohibidos)}')
    ajenos = sorted(j for j in ids if j in existentes and j not in insumo)
    if falt:
        mal.append(f'ids inexistentes: {falt}')
    if ajenos:
        mal.append(f'ids fuera de su insumo: {ajenos}')
    for v in x.get('versiculos', []):
        if not ref_valida(v['ref']):
            mal.append(f"versículo no válido: {v['ref']}")
    for w in x.get('palabras', []):
        if w.get('hebreo') and not re.search(r'[֐-׿]', w['hebreo']):
            mal.append(f"hebreo sin letras hebreas: {w['hebreo']}")
    if mal:
        problemas[f'art {i}'] = mal

os.makedirs(f'{BASE}/logs', exist_ok=True)
json.dump(problemas, open(f'{BASE}/logs/validacion.json', 'w'), ensure_ascii=False, indent=1)
for k, v in problemas.items():
    print(k)
    for m in v:
        print('   ', m[:300])
print('con observaciones:', len(problemas))
