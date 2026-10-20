#!/usr/bin/env python3
"""Valida los días escritos: ids de fuentes que existan en su insumo, citas textuales, largo, referencias y campos.

Uso: validar.py [dia ...]   (por defecto, todos los días guardados). Escribe varon/revision/validacion.json.
"""
import json, glob, os, re, sys

V = '/home/user/trabajo/varon'
sys.path.insert(0, f'{V}/scripts')
from rvr import normalizar  # noqa: E402

CUERPO = ['entrada', 'apartados', 'citas', 'datos', 'modelo', 'palabras', 'interpretaciones', 'conexiones', 'para_vivir']


def textos(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in ('fuentes', 'refs', 'ref', 'original', 'idioma'):
                yield from textos(v)
    elif isinstance(o, list):
        for v in o:
            yield from textos(v)
    elif isinstance(o, str):
        yield o


def fuentes(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'fuentes' and isinstance(v, list):
                acc.extend(v)
            else:
                fuentes(v, acc)
    elif isinstance(o, list):
        for v in o:
            fuentes(v, acc)
    return acc


def norm(s):
    return re.sub(r'\W+', ' ', s.lower()).strip()


def main():
    pedidos = [int(x) for x in sys.argv[1:]]
    archivos = sorted(glob.glob(f'{V}/dias/dia_*.json'))
    rep = {}
    for f in archivos:
        x = json.load(open(f)); d = x['dia']
        if pedidos and d not in pedidos:
            continue
        p = []
        ins_f = f'{V}/insumos/dia_{d:03d}.txt'
        ins = open(ins_f).read() if os.path.exists(ins_f) else ''
        ids_ins = set(re.findall(r'^\[([^\]]+)\]', ins, re.M))
        fs = fuentes(x, [])
        malos = sorted({i for i in fs if i not in ids_ins})
        if malos:
            p.append(f'ids que no están en el insumo: {malos[:10]}')
        sin = []
        for k in ('apartados',):
            for s in x.get(k, []):
                for q in s.get('parrafos', []):
                    if not q.get('fuentes'):
                        sin.append(q['texto'][:60])
        if sin:
            p.append(f'párrafos sin fuente: {len(sin)}')
        citas_ins = norm(' '.join(re.findall(r'Cita textual: «(.*?)»', ins)))
        for c in x.get('citas', []):
            if norm(c['texto'])[:80] not in citas_ins:
                p.append(f'cita no textual: «{c["texto"][:70]}»')
        palabras = sum(len(t.split()) for k in CUERPO for t in textos(x.get(k)))
        if not 1800 <= palabras <= 2800:
            p.append(f'largo del cuerpo: {palabras} palabras')
        for v in x.get('versiculos', []):
            if not normalizar(v['ref']):
                p.append(f'referencia no reconocida: {v["ref"]}')
        if not 1 <= len(x.get('versiculos', [])) <= 3:
            p.append('versiculos: debe haber 1 a 3')
        if len(x.get('para_reflexionar', [])) != 3:
            p.append('para_reflexionar: deben ser 3')
        if not 3 <= len(x.get('apartados', [])) <= 6:
            p.append(f'apartados: {len(x.get("apartados", []))}')
        if re.search(r'\b(ustedes|vosotros)\b', ' '.join(textos(x)), re.I):
            p.append('usa «ustedes» o «vosotros» (debe hablarle de vos)')
        rep[d] = {'palabras': palabras, 'problemas': p}
    os.makedirs(f'{V}/revision', exist_ok=True)
    json.dump(rep, open(f'{V}/revision/validacion.json', 'w'), ensure_ascii=False, indent=1)
    con = {d: r for d, r in rep.items() if r['problemas']}
    print(f'días: {len(rep)} | con observaciones: {len(con)}')
    for d, r in sorted(con.items())[:60]:
        print(d, r['palabras'], '|', ' · '.join(r['problemas']))


if __name__ == '__main__':
    main()
