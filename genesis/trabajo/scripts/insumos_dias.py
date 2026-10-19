#!/usr/bin/env python3
"""Arma, para cada día del plan, un archivo con todo el material que le corresponde.

Cada nota recibe un id estable «bloque#n» que la síntesis cita en `fuentes`. Las notas que abarcan
mucho texto van a los panoramas de la parte o del libro; las de "intro" y "tema", a sus propios archivos.
"""
import json, glob, re, os, collections

BASE = '/home/user/trabajo'
V = [31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,55,32,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26]
ACUM = [0]
for n in V:
    ACUM.append(ACUM[-1] + n)

FUENTES = {
    'kline': 'Kline, Nuevo Comentario Bíblico', 'beacon': 'Comentario Bíblico Beacon (Livingston)',
    'cbmh': 'Comentario Bíblico Mundo Hispano', 'edersheim': 'Edersheim, Comentario Bíblico Histórico',
    'macarthur': 'Biblia de Estudio MacArthur', 'dbmh': 'Diccionario Bíblico Mundo Hispano',
}


def idx(c, v):
    c = max(1, min(50, c))
    v = max(1, min(V[c - 1], v))
    return ACUM[c - 1] + v


def rango(ref):
    """Devuelve (inicio, fin) en índice de versículo, o None si no es un pasaje."""
    r = ref.strip().replace('–', '-').replace('—', '-').replace(' ', '')
    r = re.sub(r'^(Gn|Gén|Génesis)\.?', '', r, flags=re.I)
    m = re.fullmatch(r'(\d+)(?::(\d+))?(?:-(\d+)(?::(\d+))?)?(?:[a-z])?', r)
    if not m:
        m2 = re.match(r'(\d+):(\d+)', r)
        if m2:
            c, v = int(m2.group(1)), int(m2.group(2))
            return idx(c, v), idx(c, v)
        return None
    c1 = int(m.group(1)); v1 = m.group(2); a = m.group(3); b = m.group(4)
    if not 1 <= c1 <= 50:
        return None
    if v1 is None:                       # "12" o "12-13"
        c2 = int(a) if a else c1
        return idx(c1, 1), idx(c2, V[min(50, c2) - 1])
    v1 = int(v1)
    if a is None:
        return idx(c1, v1), idx(c1, v1)
    if b is None:                        # "12:1-9"
        return idx(c1, v1), idx(c1, int(a))
    return idx(c1, v1), idx(int(a), int(b))   # "11:27-25:11"


def cargar():
    notas = []
    for f in sorted(glob.glob(f'{BASE}/extracciones/biblio/*.json')):
        blq = os.path.basename(f)[:-5]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            n = dict(n); n['id'] = f'{blq}#{i}'; n['origen'] = 'biblio'
            n['fuente'] = FUENTES.get(blq.split('_')[0], blq)
            notas.append(n)
    # obras eliminadas por no confiables (no aportan nada aunque alguna nota se haya colado)
    borrados = set(json.load(open(f'{BASE}/borrado/archivos_borrados_claves.json')))
    autores_fuera = ('barclay', 'white', 'pikaza', 'iafrancesco', 'deiros', 'adventista', 'flores', 'hanegraaff')
    for f in sorted(glob.glob(f'{BASE}/extracciones/ref3/*.json')):
        blq = os.path.basename(f)[:-5]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            if n.get('archivo') in borrados or any(a in (n.get('autor', '') + n.get('obra', '')).lower() for a in autores_fuera):
                continue
            n = dict(n); n['id'] = f'{blq}#{i}'; n['origen'] = 'ref3'
            n['fuente'] = f"{n.get('autor','')}, {n.get('obra','')}"
            notas.append(n)
    return notas


def linea(n):
    partes = [f"[{n['id']}] Gn {n['ref']} · {n.get('tipo','')} · imp {n.get('importancia','')} · {n['fuente']} ({n.get('pagina','')})",
              f"  {n.get('titulo','')}: {n.get('contenido','')}"]
    if n.get('cita'):
        partes.append(f"  CITA: «{n['cita']}»")
    if n.get('hebreo'):
        h = n['hebreo']; partes.append(f"  HEBREO: {h.get('palabra','')} ({h.get('transliteracion','')}): {h.get('significado','')}")
    if n.get('postura'):
        partes.append(f"  POSTURAS: {n['postura']}")
    if n.get('refs_biblicas'):
        partes.append(f"  REFS: {', '.join(n['refs_biblicas'][:12])}")
    return '\n'.join(partes)


def main():
    plan = json.load(open(f'{BASE}/plan/plan.json'))
    rvr = json.load(open(f'{BASE}/biblia/rvr1960_genesis.json'))['texto']
    notas = cargar()
    dias = []
    for d in plan:
        c1, v1 = map(int, d['desde'].split(':')); c2, v2 = map(int, d['hasta'].split(':'))
        dias.append((idx(c1, v1), idx(c2, v2)))
    por_dia = collections.defaultdict(list); panorama = collections.defaultdict(list); libro = []; sin = []
    sobrantes = collections.defaultdict(list)
    selecciones = {}   # día (índice 0) -> ids de referencia elegidos por la curaduría
    for f in glob.glob(f'{BASE}/insumos/curaduria/dia_*.json'):
        dd = json.load(open(f)); selecciones[dd['dia'] - 1] = set(dd['ids'])
    partes_rango = {}
    for d, (a, b) in zip(plan, dias):
        p = d['parte']; x = partes_rango.get(p, (a, b)); partes_rango[p] = (min(x[0], a), max(x[1], b))
    for n in notas:
        ref = str(n.get('ref', '')).strip().lower()
        if ref in ('intro', 'tema', ''):
            libro.append(n); continue
        r = rango(ref)
        if not r:
            sin.append(n); continue
        a, b = r; span = b - a + 1
        tocados = [i for i, (x, y) in enumerate(dias) if not (b < x or a > y)]
        if span <= 60:
            if n['origen'] == 'ref3':
                # una nota de referencia va a un solo día: el de mayor superposición (evita repetir ideas en días seguidos)
                mejor = max(tocados, key=lambda i: (min(b, dias[i][1]) - max(a, dias[i][0]), -i))
                sel = selecciones.get(mejor)
                if sel is None or n['id'] in sel:
                    por_dia[mejor].append(n)
                else:
                    sobrantes[mejor].append(n)
            else:
                for i in tocados:
                    por_dia[i].append(n)
        else:
            ps = sorted({plan[i]['parte'] for i in tocados})
            if len(ps) == 1 and span <= 900:
                panorama[ps[0]].append(n)
            else:
                libro.append(n)
    os.makedirs(f'{BASE}/insumos', exist_ok=True)
    stats = []
    for i, d in enumerate(plan):
        a, b = dias[i]
        texto = []
        for c in range(1, 51):
            for v, t in rvr[str(c)].items():
                k = idx(c, int(v))
                if a <= k <= b:
                    texto.append(f'{c}:{v} {t}')
        ant = plan[i - 1] if i else None; sig = plan[i + 1] if i + 1 < len(plan) else None
        ns = sorted(por_dia[i], key=lambda n: (rango(n['ref'])[0], n['origen'] != 'biblio', -int(n.get('importancia', 1))))
        cab = [f"DÍA {d['dia']} · Génesis {d['desde']}–{d['hasta']} · {d['titulo']} · Parte {d['parte']} · {d['versiculos']} versículos",
               f"Día anterior: {ant['dia']} · Gn {ant['desde']}–{ant['hasta']} · {ant['titulo']}" if ant else 'Día anterior: (es el primero)',
               f"Día siguiente: {sig['dia']} · Gn {sig['desde']}–{sig['hasta']} · {sig['titulo']}" if sig else 'Día siguiente: (es el último)',
               '', '=== TEXTO DEL PASAJE (RVR1960) ===', *texto, '',
               f'=== NOTAS ({len(ns)}) ===']
        open(f'{BASE}/insumos/dia_{d["dia"]:02d}.txt', 'w').write('\n'.join(cab) + '\n' + '\n\n'.join(linea(n) for n in ns) + '\n')
        stats.append((d['dia'], len(ns), sum(len(linea(n)) for n in ns)))
    os.makedirs(f'{BASE}/insumos/sobrantes', exist_ok=True)
    for i, ns in sobrantes.items():
        json.dump([n['id'] for n in ns], open(f'{BASE}/insumos/sobrantes/dia_{i+1:02d}.json', 'w'))
    ref3_dia = {plan[i]['dia']: sum(len(linea(n)) for n in ns if n['origen'] == 'ref3') for i, ns in por_dia.items()}
    json.dump(ref3_dia, open(f'{BASE}/insumos/_ref3_por_dia.json', 'w'))
    for p, ns in panorama.items():
        open(f'{BASE}/insumos/panorama_parte_{p}.txt', 'w').write('\n\n'.join(linea(n) for n in sorted(ns, key=lambda n: rango(n['ref'])[0])))
    open(f'{BASE}/insumos/libro_intro_y_temas.txt', 'w').write('\n\n'.join(linea(n) for n in libro))
    open(f'{BASE}/insumos/_sin_ref.txt', 'w').write('\n\n'.join(linea(n) for n in sin))
    print('notas', len(notas), '| libro/temas', len(libro), '| panoramas', {p: len(v) for p, v in panorama.items()}, '| sin ref', len(sin))
    cs = [s[2] for s in stats]
    print('por día: notas min/máx', min(s[1] for s in stats), max(s[1] for s in stats), '| chars min/prom/máx', min(cs), sum(cs) // len(cs), max(cs))


if __name__ == '__main__':
    main()
