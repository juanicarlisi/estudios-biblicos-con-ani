#!/usr/bin/env python3
"""Valida artículos: validar_articulo.py ID [ID ...]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pesos
AQUI = os.path.dirname(os.path.abspath(__file__))
def palabras(d):
    t = 0
    def rec(o):
        nonlocal t
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('fuentes', 'ref', 'refs_apocalipsis', 'visuales', 'dias_relacionados', 'notas_no_usadas', 'id', 'citas', 'pagina', 'obra', 'autor', 'griego', 'translit'): continue
                rec(v)
        elif isinstance(o, list):
            for v in o: rec(v)
        elif isinstance(o, str): t += len(o.split())
    rec(d); return t
def revisar(aid):
    errs = []; avis = []
    f = f'{AQUI}/../articulos/art_{aid}.json'
    try: d = json.load(open(f))
    except Exception as e: return [f'JSON inválido: {e}'], []
    I = {n['id'] for n in pesos.notas()}
    for k in ('id', 'titulo', 'bajada', 'entrada', 'apartados', 'para_conversar'):
        if k not in d: errs.append(f'falta {k}')
    if errs: return errs, avis
    if d['id'] != aid: errs.append('id distinto')
    usados = []
    def rec(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('fuentes', 'notas_no_usadas') and isinstance(v, list): usados.extend(v)
                else: rec(v)
        elif isinstance(o, list):
            for v in o: rec(v)
    rec(d)
    mal = sorted({u for u in usados if u not in I})
    if mal: errs.append(f'fuentes inexistentes: {mal[:8]}')
    for ap in d['apartados']:
        for p in ap.get('parrafos', []):
            if not p.get('fuentes'): errs.append(f"párrafo sin fuentes en «{ap.get('titulo')}»")
    if not d['entrada'].get('fuentes'): errs.append('entrada sin fuentes')
    if len(d['para_conversar']) != 3: errs.append('para_conversar debe tener 3 preguntas')
    vis = json.load(open(AQUI + '/../plan/visuales.json')); ok = set(vis['mapas']) | set(vis['diagramas'])
    for v in d.get('visuales', []):
        if v not in ok: errs.append(f'visual desconocido {v}')
    plan = {x['dia'] for x in json.load(open(AQUI + '/../plan/plan.json'))['dias']}
    for x in d.get('dias_relacionados', []):
        if x not in plan: errs.append(f'día inexistente {x}')
    avis.append(f'{palabras(d)} palabras, {len(set(usados))} fuentes distintas')
    return errs, avis
if __name__ == '__main__':
    mal = 0
    for a in sys.argv[1:]:
        e, v = revisar(a); print(f'{a}:', 'OK' if not e else 'ERRORES'); [print('  ERROR', x) for x in e]; [print('  aviso', x) for x in v]; mal += bool(e)
    sys.exit(1 if mal else 0)
