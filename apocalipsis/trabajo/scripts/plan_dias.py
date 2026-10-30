#!/usr/bin/env python3
"""Arma el plan de días de Apocalipsis a partir del peso del material por pasaje.

Reglas: sin tope de versículos; cada día apunta a ~OBJ unidades de material (≈ 20-30 minutos de estudio).
Una unidad de sentido (pericopa) se parte en varios días si pesa mucho (cortes por versículo, con peso parejo) y las
unidades vecinas de la misma parte se juntan si pesan poco. Salida: ../plan/plan.json
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U, pesos
OBJ = float(os.environ.get('OBJ', 40000))
PARTES = [
 ('p1', 'Parte 1', 'La revelación de Jesucristo', '1:1-20', 1, 1), ('p2', 'Parte 2', 'Las siete cartas a las iglesias', '2:1-3:22', 2, 3),
 ('p3', 'Parte 3', 'El trono y el Cordero', '4:1-5:14', 4, 5), ('p4', 'Parte 4', 'Los siete sellos', '6:1-8:5', 6, 8),
 ('p5', 'Parte 5', 'Las siete trompetas', '8:6-11:19', 8, 11), ('p6', 'Parte 6', 'La mujer, el dragón y las bestias', '12:1-14:20', 12, 14),
 ('p7', 'Parte 7', 'Las siete copas', '15:1-16:21', 15, 16), ('p8', 'Parte 8', 'Babilonia cae y viene el Rey', '17:1-19:21', 17, 19),
 ('p9', 'Parte 9', 'El milenio y el juicio final', '20:1-15', 20, 20), ('p10', 'Parte 10', 'Cielo nuevo y tierra nueva', '21:1-22:21', 21, 22),
]
def parte_de(i):
    c, v = U.desde_idx(i)
    for p in PARTES:
        if (p[4], 1) <= (c, v) <= (p[5], 99) and not (p[0] == 'p4' and c == 8 and v > 5) and not (p[0] == 'p5' and c == 8 and v <= 5):
            return p[0]
def main():
    w = pesos.pesos(); base = 250.0
    wv = [0.0] + [w[i] + base for i in range(1, 405)]
    pieces = []   # (ini, fin, titulo, unidad)
    for u in U.UNIDADES:
        W = sum(wv[u['ini']:u['fin'] + 1]); n = max(1, round(W / OBJ))
        n = min(n, u['fin'] - u['ini'] + 1)
        if n == 1: pieces.append([u['ini'], u['fin'], u['titulo'], [u['id']]]); continue
        # cortes: para cada k, el versículo cuyo acumulado queda más cerca de k*W/n (estrictamente creciente)
        vs = list(range(u['ini'], u['fin'] + 1)); cum = []; acc = 0
        for i in vs: acc += wv[i]; cum.append(acc)
        cortes = []; ult = -1
        for k in range(1, n):
            mejor = min(range(ult + 1, len(vs) - (n - k)), key=lambda j: abs(cum[j] - W * k / n))
            cortes.append(mejor); ult = mejor
        ini = u['ini']
        for k, j in enumerate(cortes, 1):
            pieces.append([ini, vs[j], f"{u['titulo']} ({k} de {n})", [u['id']]]); ini = vs[j] + 1
        pieces.append([ini, u['fin'], f"{u['titulo']} ({n} de {n})", [u['id']]])
    # juntar piezas pequeñas vecinas de la misma parte
    out = []
    for p in pieces:
        pw = sum(wv[p[0]:p[1] + 1])
        if out:
            q = out[-1]; qw = sum(wv[q[0]:q[1] + 1])
            if parte_de(q[0]) == parte_de(p[0]) and q[1] + 1 == p[0] and '(' not in q[2] and '(' not in p[2] and qw + pw <= 1.25 * OBJ and (qw < 0.55 * OBJ or pw < 0.55 * OBJ):
                q[1] = p[1]; q[2] = q[2] + ' y ' + p[2][0].lower() + p[2][1:]; q[3] = q[3] + p[3]; continue
        out.append(p)
    # segunda pasada: una pieza muy chica se une a su vecina de la misma unidad
    cambio = True
    while cambio:
        cambio = False
        for k in range(len(out) - 1):
            a_, b_ = out[k], out[k + 1]
            wa, wb = sum(wv[a_[0]:a_[1] + 1]), sum(wv[b_[0]:b_[1] + 1])
            if a_[3] == b_[3] and min(wa, wb) < 0.5 * OBJ and wa + wb <= 1.3 * OBJ:
                a_[1] = b_[1]; del out[k + 1]; cambio = True; break
    import re as _re
    from collections import Counter
    tot = Counter(tuple(x[3]) for x in out); vis = Counter()
    for x in out:
        base = _re.sub(r' \(\d+ de \d+\)$', '', x[2]); k = tuple(x[3])
        if len(k) == 1 and tot[k] > 1: vis[k] += 1; x[2] = f'{base} ({vis[k]} de {tot[k]})'
        else: x[2] = base
    plan = []
    for d, p in enumerate(out, 1):
        plan.append({'dia': d, 'desde': U.etiqueta(p[0], p[0]).split('-')[0], 'hasta': U.etiqueta(p[1], p[1]),
                     'rango': U.etiqueta(p[0], p[1]), 'versiculos': p[1] - p[0] + 1, 'ini': p[0], 'fin': p[1], 'titulo_provisional': p[2],
                     'unidades': p[3], 'parte': parte_de(p[0]), 'peso': int(sum(wv[p[0]:p[1] + 1]))})
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plan'), exist_ok=True)
    json.dump({'partes': [{'id': a, 'etiqueta': b, 'titulo': c, 'rango': r} for a, b, c, r, _, _ in PARTES], 'dias': plan},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plan', 'plan.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(plan), 'días; peso medio', int(sum(x['peso'] for x in plan) / len(plan)))
    for x in plan: print(f"{x['dia']:3d} {x['parte']:3s} {x['rango']:>12} v={x['versiculos']:2d} w={x['peso']:6d} {x['titulo_provisional'][:60]}")
if __name__ == '__main__': main()
