#!/usr/bin/env python3
"""Arma el plan de días de 1 Pedro a Judas a partir del peso del material por pasaje.

Reglas: sin tope de versículos; cada día apunta a ~OBJ unidades de material (≈ 20-30 minutos de estudio). OBJ = 40.000, el mismo
objetivo que dio los 95 días de Apocalipsis (peso medio 39.800 por día, contando la base de 250 por versículo); se puede cambiar
con la variable de entorno OBJ. Una unidad de sentido (pericopa) se parte en varios días si pesa mucho (cortes por versículo, con
peso parejo) y las unidades vecinas de la misma parte se juntan si pesan poco. Cada día es de un solo libro, salvo 2 Juan + 3 Juan
(la parte p10 los reúne y el plan puede juntarlos). Salida: ../plan/plan.json
"""
import json, os, sys, re
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U, pesos
OBJ = float(os.environ.get('OBJ', 40000))
BASE = 250.0
# (id, etiqueta, título, rango, libro)
PARTES = [
 ('p1', '1 Pedro · Parte 1', 'Una salvación viva y un pueblo santo', '1P 1:1-2:10'),
 ('p2', '1 Pedro · Parte 2', 'Extranjeros y peregrinos: vivir sometidos por causa del Señor', '1P 2:11-3:12'),
 ('p3', '1 Pedro · Parte 3', 'Sufrimiento y gloria', '1P 3:13-5:14'),
 ('p4', '2 Pedro · Parte 1', 'Crecer en la fe y la palabra segura', '2P 1:1-21'),
 ('p5', '2 Pedro · Parte 2', 'Los falsos maestros', '2P 2:1-22'),
 ('p6', '2 Pedro · Parte 3', 'El día del Señor', '2P 3:1-18'),
 ('p7', '1 Juan · Parte 1', 'Andar en la luz', '1J 1:1-2:17'),
 ('p8', '1 Juan · Parte 2', 'Permanecer en él: hijos de Dios', '1J 2:18-3:24'),
 ('p9', '1 Juan · Parte 3', 'Dios es amor: la fe que vence', '1J 4:1-5:21'),
 ('p10', '2 y 3 Juan', 'La verdad, el amor y la hospitalidad', '2J 1-3J 15'),
 ('p11', 'Judas', 'Contender por la fe', 'Jd 1-25'),
]
RP = [(p[0], *U.rango(p[3])) for p in PARTES]
assert RP[0][1] == 1 and RP[-1][2] == U.TOTAL and all(b[1] == a[2] + 1 for a, b in zip(RP, RP[1:]))
def parte_de(i):
    for pid, a, b in RP:
        if a <= i <= b: return pid
def libro_dia(ini, fin):
    a, b = U.libro_de(ini), U.libro_de(fin)
    return a if a == b else f'{a}+{b}'
def main():
    w = pesos.pesos()
    wv = [0.0] + [w[i] + BASE for i in range(1, U.TOTAL + 1)]
    pieces = []   # (ini, fin, titulo, unidades)
    for u in U.UNIDADES:
        W = sum(wv[u['ini']:u['fin'] + 1]); n = max(1, round(W / OBJ))
        n = min(n, u['fin'] - u['ini'] + 1)
        if n == 1: pieces.append([u['ini'], u['fin'], u['titulo'], [u['id']]]); continue
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
    # juntar piezas pequeñas vecinas de la misma parte (nunca de libros distintos, salvo 2J+3J dentro de p10)
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
    tot = Counter(tuple(x[3]) for x in out); vis = Counter()
    for x in out:
        base = re.sub(r' \(\d+ de \d+\)$', '', x[2]); k = tuple(x[3])
        if len(k) == 1 and tot[k] > 1: vis[k] += 1; x[2] = f'{base} ({vis[k]} de {tot[k]})'
        else: x[2] = base
    plan = []
    for d, p in enumerate(out, 1):
        lib = libro_dia(p[0], p[1])
        assert '+' not in lib or lib == '2J+3J', (p, lib)
        plan.append({'dia': d, 'libro': lib, 'desde': U.cv(p[0]), 'hasta': U.cv(p[1]), 'rango': U.etiqueta(p[0], p[1]),
                     'versiculos': p[1] - p[0] + 1, 'ini': p[0], 'fin': p[1], 'titulo_provisional': p[2],
                     'unidades': p[3], 'parte': parte_de(p[0]), 'peso': int(sum(wv[p[0]:p[1] + 1]))})
    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plan'); os.makedirs(dst, exist_ok=True)
    json.dump({'partes': [{'id': a, 'etiqueta': b, 'titulo': c, 'rango': r} for a, b, c, r in PARTES], 'dias': plan},
              open(os.path.join(dst, 'plan.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(plan), 'días; peso medio', int(sum(x['peso'] for x in plan) / len(plan)), '| por libro', dict(Counter(x['libro'] for x in plan)))
    for x in plan: print(f"{x['dia']:3d} {x['parte']:3s} {x['rango']:>14} v={x['versiculos']:2d} w={x['peso']:6d} {x['titulo_provisional'][:60]}")
if __name__ == '__main__': main()
