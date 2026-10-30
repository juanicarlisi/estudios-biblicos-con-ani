#!/usr/bin/env python3
"""Arma las ventanas de revisión de continuidad: 6 días seguidos (con 1 de solapamiento) por archivo.

Escribe varon/revision/continuidad_NNN.txt y varon/revision/_ventanas.json. Cada texto lleva su ruta de campo
(p. ej. «apartados[1].parrafos[0].texto») para que las correcciones se apliquen en el lugar exacto.
Uso: continuidad_entrada.py [desde hasta]
"""
import json, glob, os, sys

V = '/home/user/trabajo/varon'
TAM, PASO = 10, 9


def campos(x):
    yield 'titulo', x.get('titulo', '')
    yield 'bajada', x.get('bajada', '')
    yield 'lectura.porque', f"({x.get('lectura', {}).get('pasaje', '')}) {x.get('lectura', {}).get('porque', '')}"
    for k, v in enumerate(x.get('versiculos', [])):
        yield f'versiculos[{k}].porque', f"({v['ref']}) {v['porque']}"
    yield 'entrada.texto', x['entrada']['texto']
    for a, s in enumerate(x.get('apartados', [])):
        yield f'apartados[{a}].titulo', '## ' + s['titulo']
        for p, q in enumerate(s.get('parrafos', [])):
            yield f'apartados[{a}].parrafos[{p}].texto', q['texto']
        if s.get('destacado', {}).get('texto'):
            yield f'apartados[{a}].destacado.texto', s['destacado']['texto']
    for k, c in enumerate(x.get('citas', [])):
        yield f'citas[{k}].texto', f"«{c['texto']}» ({c['autor']})"
    for k, d in enumerate(x.get('datos', [])):
        yield f'datos[{k}].texto', f"[{d['valor']}] {d['texto']}"
    if x.get('modelo', {}).get('texto'):
        yield 'modelo.texto', f"({x['modelo']['persona']}) {x['modelo']['texto']}"
    for k, w in enumerate(x.get('palabras', [])):
        yield f'palabras[{k}].significado', f"({w['translit']}) {w['significado']}"
    for k, i in enumerate(x.get('interpretaciones', [])):
        for j, p in enumerate(i['posturas']):
            yield f'interpretaciones[{k}].posturas[{j}].postura', f"({i['tema']} · {p['quien']}) {p['postura']}"
    for k, c in enumerate(x.get('conexiones', [])):
        yield f'conexiones[{k}].nota', f"({c['ref']}) {c['nota']}"
    for k, v in enumerate(x.get('para_vivir', [])):
        yield f'para_vivir[{k}].texto', v['texto']
    for k, q in enumerate(x.get('para_reflexionar', [])):
        yield f'para_reflexionar[{k}]', q
    for k, q in enumerate(x.get('para_conversar', [])):
        yield f'para_conversar[{k}]', q
    yield 'para_orar', x.get('para_orar', '')
    for k, f in enumerate(x.get('profundizar', [])):
        yield f'profundizar[{k}].texto', f"({f['titulo']}) {f['texto']}"


def main():
    plan = json.load(open(f'{V}/plan/plan.json'))
    partes = {p['id']: p for p in json.load(open(f'{V}/plan/partes.json'))}
    hay = {int(os.path.basename(f)[4:7]) for f in glob.glob(f'{V}/dias/dia_*.json')}
    desde, hasta = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1, len(plan))
    os.makedirs(f'{V}/revision', exist_ok=True)
    ventanas, k, ini = [], 0, desde
    while ini <= hasta:
        dias = [d for d in range(ini, min(ini + TAM - 1, hasta) + 1) if d in hay]
        if len(dias) >= 2:
            k += 1
            out = [f'# Ventana {k}: días {dias[0]} a {dias[-1]}']
            for d in dias:
                x = json.load(open(f'{V}/dias/dia_{d:03d}.json')); p = plan[d - 1]
                out += ['', f"========== DÍA {d} · Parte {partes[p['parte']]['numero']}: {partes[p['parte']]['titulo']} =========="]
                out += [f'[{c}] {t}' for c, t in campos(x) if t]
            open(f'{V}/revision/continuidad_{k:03d}.txt', 'w').write('\n'.join(out) + '\n')
            ventanas.append({'ventana': k, 'dias': dias})
        ini += PASO
    json.dump(ventanas, open(f'{V}/revision/_ventanas.json', 'w'), indent=0)
    print('ventanas:', len(ventanas))


if __name__ == '__main__':
    main()
