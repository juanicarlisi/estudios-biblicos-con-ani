#!/usr/bin/env python3
"""Arma, para cada día con flags bloqueantes (verificar_dia.py), el archivo de reparación con SOLO lo que hay que corregir:
cada texto marcado, sus flags, las notas que cita (recortadas) y los versículos RVR que hagan falta.
Escribe varon/reparar/dia_NNN.txt y lista los días en varon/reparar/_dias.json.
Uso: reparar_entrada.py [--base borradores|dias]"""
import json, glob, os, re, sys
V = '/home/user/trabajo/varon'
sys.path.insert(0, f'{V}/scripts')
from dia_util import unidades, insumo, capitulo, refs_en  # noqa: E402
from rvr import normalizar  # noqa: E402
NO_BLOQ = {'cifras_laxo', 'biblia_sin_dato'}


def main():
    base = 'dias' if '--base' in sys.argv and sys.argv[sys.argv.index('--base') + 1] == 'dias' else 'borradores'
    os.makedirs(f'{V}/reparar', exist_ok=True)
    for f in glob.glob(f'{V}/reparar/dia_*.txt'):
        os.remove(f)
    dias = []
    for f in sorted(glob.glob(f'{V}/revision/verif/dia_*.json')):
        d = int(f[-8:-5]); r = json.load(open(f))
        fl = [x for x in r['flags'] if x['tipo'] not in NO_BLOQ]
        if not fl:
            continue
        x = json.load(open(f'{V}/dias/{base}/dia_{d:03d}.json')) if base != 'dias' else json.load(open(f'{V}/dias/dia_{d:03d}.json'))
        U = {ru: (t, fu) for ru, t, fu in unidades(x)}
        ins = insumo(d)
        por = {}
        for y in fl:
            por.setdefault(y['ruta'], []).append(y)
        out = [f'DÍA {d}: {x.get("titulo", "")}']
        for ru, ys in por.items():
            if ru not in U:
                continue
            t, fu = U[ru]
            out += ['', f'## ruta: {ru}', 'PROBLEMAS: ' + ' | '.join(f'{y["tipo"]}: {y["detalle"]}' for y in ys), f'TEXTO ACTUAL: {t}', f'FUENTES ACTUALES: {fu}']
            for i in (fu or [])[:8]:
                out.append(f'-- [{i}] ' + re.sub(r'\s+', ' ', ins.get(i, '(no está en el insumo)'))[:1500])
            if any(y['tipo'] in ('comillas', 'biblia') for y in ys):
                vistos = set()
                for s, n in refs_en(t) + [(v['ref'], normalizar(v['ref'])) for v in x.get('versiculos', []) if normalizar(v['ref'])]:
                    (nombre, osis), c, v1, v2 = n
                    if (osis, c) in vistos:
                        continue
                    vistos.add((osis, c))
                    cap = capitulo((osis, nombre, c)) or {}
                    out.append(f'-- RVR1960 {nombre} {c}: ' + ' '.join(f'({k}) {v}' for k, v in list(cap.items())[:40])[:2500])
            out.append('-- Resto de notas del insumo con el mismo tema (por si falta la fuente): ' + ', '.join(list(ins)[:60]))
        open(f'{V}/reparar/dia_{d:03d}.txt', 'w').write('\n'.join(out) + '\n')
        dias.append(d)
    json.dump(dias, open(f'{V}/reparar/_dias.json', 'w'))
    print(f'{len(dias)} días a reparar · tamaño medio {sum(os.path.getsize(f"{V}/reparar/dia_{d:03d}.txt") for d in dias) // max(1, len(dias))} bytes')


if __name__ == '__main__':
    main()
