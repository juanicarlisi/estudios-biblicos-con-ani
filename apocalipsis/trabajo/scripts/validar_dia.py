#!/usr/bin/env python3
"""Valida el JSON de un día. Uso: validar_dia.py N [N ...]   (sale con 1 si hay errores; avisos no cuentan)"""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U, pesos
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
AQUI = os.path.dirname(os.path.abspath(__file__))
_ids = None
def ids():
    global _ids
    if _ids is None: _ids = {n['id']: n for n in pesos.notas()}
    return _ids
def sin(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.category(c).startswith('M')).replace('ς', 'σ')
def palabras(o):
    t = 0
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('fuentes', 'refs', 'ref', 'rango', 'desde', 'hasta', 'tipo', 'dia', 'minutos', 'visuales', 'anexos', 'pagina', 'obra', 'autor', 'quien', 'griego', 'translit'): continue
            t += palabras(v)
    elif isinstance(o, list):
        for v in o: t += palabras(v)
    elif isinstance(o, str): t += len(o.split())
    return t
def revisar(n):
    errs = []; avis = []
    plan = {d['dia']: d for d in json.load(open(AQUI + '/../plan/plan.json'))['dias']}
    f = f'{AQUI}/../dias/dia_{n:02d}.json'
    try: d = json.load(open(f))
    except Exception as e: return [f'JSON inválido: {e}'], []
    p = plan[n]; I = ids()
    for k in ('dia', 'desde', 'hasta', 'titulo', 'minutos', 'contexto', 'versiculo_clave', 'panorama', 'secciones', 'para_conversar', 'para_orar'):
        if k not in d: errs.append(f'falta {k}')
    if errs: return errs, avis
    if d['dia'] != n: errs.append('número de día distinto')
    if d['desde'] != p['desde'] or d['hasta'] != p['hasta']: errs.append(f"rango {d['desde']}-{d['hasta']} distinto del plan {p['desde']}-{p['hasta']}")
    usados = []
    def rec(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'fuentes' and isinstance(v, list): usados.extend(v)
                else: rec(v)
        elif isinstance(o, list):
            for v in o: rec(v)
    rec(d)
    mal = sorted({u for u in usados if u not in I})
    if mal: errs.append(f'fuentes inexistentes: {mal[:8]}')
    r = U.rango(d['versiculo_clave'].get('ref', ''))
    if not r or r[0] < p['ini'] or r[1] > p['fin']: errs.append(f"versículo clave fuera del día: {d['versiculo_clave'].get('ref')}")
    elif r[1] - r[0] > 2: errs.append('versículo clave de más de 3 versículos')
    if len(d['para_conversar']) != 3: errs.append('para_conversar debe tener 3 preguntas')
    if not 1 <= len(d['secciones']) <= 8: errs.append(f"{len(d['secciones'])} secciones")
    for s in d['secciones']:
        rr = U.rango(s.get('rango', ''))
        if not rr or rr[0] < p['ini'] or rr[1] > p['fin']: errs.append(f"sección fuera del día: {s.get('rango')}")
        for nt in s.get('notas', []):
            if not nt.get('fuentes'): errs.append(f"nota sin fuentes en {s.get('rango')}")
    for k in ('contexto', 'panorama'):
        if not d[k].get('fuentes'): errs.append(f'{k} sin fuentes')
    gr = json.load(open(AQUI + '/../griego/apocalipsis_griego.json'))['versiculos']
    texto_gr = sin(' '.join(w['t'] + ' ' + w['l'] for i in range(p['ini'], p['fin'] + 1) for w in gr['%d:%d' % U.desde_idx(i)]))
    notas_gr = sin(' '.join(json.dumps(I[u].get('griego', ''), ensure_ascii=False) for u in usados if u in I))
    for w in d.get('palabras', []):
        g = sin(re.sub(r'[^\w]', '', w.get('griego', '')))
        if g and g not in texto_gr and g not in notas_gr: avis.append(f"griego no verificado en el texto del día: {w.get('griego')}")
    vis = json.load(open(AQUI + '/../plan/visuales.json')); ok = set(vis['mapas']) | set(vis['diagramas'])
    for v in d.get('visuales', []):
        if v not in ok: errs.append(f'visual desconocido {v}')
    if len(d.get('visuales', [])) > 3: errs.append('más de 3 visuales')
    arts = {a['id'] for a in json.load(open(AQUI + '/../plan/articulos.json'))}
    for a in d.get('anexos', []):
        if a not in arts: errs.append(f'anexo desconocido {a}')
    pal = palabras({k: v for k, v in d.items() if k != 'profundizar'})
    if pal < 900: avis.append(f'estudio corto: {pal} palabras')
    if pal > 3200: avis.append(f'estudio largo: {pal} palabras')
    d['_palabras'] = pal
    return errs, avis + [f'{pal} palabras, {len(set(usados))} fuentes distintas']
if __name__ == '__main__':
    mal = 0
    for a in sys.argv[1:]:
        e, v = revisar(int(a))
        print(f'día {a}:', 'OK' if not e else 'ERRORES'); [print('  ERROR', x) for x in e]; [print('  aviso', x) for x in v]
        mal += bool(e)
    sys.exit(1 if mal else 0)
