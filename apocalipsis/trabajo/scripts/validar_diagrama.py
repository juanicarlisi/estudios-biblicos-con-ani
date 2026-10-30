#!/usr/bin/env python3
"""Valida diagramas: validar_diagrama.py ID [ID ...]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pesos
AQUI = os.path.dirname(os.path.abspath(__file__))
def revisar(did):
    errs = []; avis = []
    try: d = json.load(open(f'{AQUI}/../diagramas/{did}.json'))
    except Exception as e: return [f'JSON inválido: {e}'], []
    I = {n['id'] for n in pesos.notas()}
    vis = json.load(open(AQUI + '/../plan/visuales.json'))['diagramas']
    if d.get('id') != did or did not in vis: errs.append('id inválido')
    t = d.get('tipo'); usados = []
    def fu(o, donde):
        f = o.get('fuentes')
        if not f: errs.append(f'{donde}: sin fuentes')
        else: usados.extend(f)
    if t == 'tabla':
        c = d.get('columnas', [])
        if not c or not d.get('filas'): errs.append('tabla vacía')
        for i, f in enumerate(d.get('filas', []), 1):
            if len(f.get('celdas', [])) != len(c): errs.append(f'fila {i}: {len(f.get("celdas", []))} celdas para {len(c)} columnas')
            fu(f, f'fila {i}')
    elif t == 'lineas':
        if not d.get('carriles') or len(d.get('eje', [])) < 2: errs.append('faltan carriles o eje')
        for i, c in enumerate(d.get('carriles', []), 1):
            fu(c, f'carril {i}'); seg = sorted(c.get('segmentos', []), key=lambda s: s['desde'])
            for a, b in zip(seg, seg[1:]):
                if b['desde'] < a['hasta']: errs.append(f'carril {i}: segmentos que se pisan ({a["etiqueta"]} / {b["etiqueta"]})')
            for s in seg:
                if not (0 <= s['desde'] < s['hasta'] <= 100): errs.append(f'carril {i}: segmento fuera de 0-100 ({s["etiqueta"]})')
    elif t == 'tarjetas':
        if not d.get('tarjetas'): errs.append('sin tarjetas')
        for i, c in enumerate(d.get('tarjetas', []), 1): fu(c, f'tarjeta {i}')
    else: errs.append(f'tipo desconocido {t}')
    mal = sorted({u for u in usados if u not in I})
    if mal: errs.append(f'fuentes inexistentes: {mal[:8]}')
    avis.append(f'{t}, {len(set(usados))} fuentes distintas')
    return errs, avis
if __name__ == '__main__':
    mal = 0
    for a in sys.argv[1:]:
        e, v = revisar(a); print(f'{a}:', 'OK' if not e else 'ERRORES'); [print('  ERROR', x) for x in e]; [print('  aviso', x) for x in v]; mal += bool(e)
    sys.exit(1 if mal else 0)
