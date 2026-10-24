#!/usr/bin/env python3
"""Propone la lista de días (la variable DIAS de plan.py) según cuánto material hay, respetando las unidades de sentido (pericopas de plan_densidad.py).

Reglas (sin tope de versículos por día; cada día es de 20 a 30 minutos de lectura, o sea un peso de material de unas T palabras ponderadas):
- una pericopa se estudia en ceil(peso / (1,3·T)) días (mínimo 1);
- si hace falta más de un día, el reparto es por versículos, con la partición que minimiza el día más pesado;
- si un solo versículo pesa más de 1,3·T, se estudia en varios días seguidos con enfoques distintos (el texto / lo que se enseña y discute / cómo se vive);
- las pericopas livianas vecinas (de la misma parte) se sugieren como fusión, para decidirla a mano.
Uso: plan_auto.py [--T 4200]   (imprime la propuesta como líneas de DIAS y un resumen; no escribe nada)
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C
import plan_densidad as P

PARTE = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'}
FOCOS = {
    2: [('Lo que dice el texto', 'TIPOS_TEXTO'), ('Lo que se enseña, lo que se discute y cómo se vive', 'TIPOS_DEBATE + TIPOS_VIDA')],
    3: [('Lo que dice el texto', 'TIPOS_TEXTO'), ('Lo que se enseña y lo que se discute', 'TIPOS_DEBATE'), ('Cómo se vive', 'TIPOS_VIDA')],
}


def particion(pesos, n):
    """Parte la lista de pesos (uno por versículo) en n tramos contiguos minimizando el tramo más pesado; devuelve [(i, j)] con j exclusivo."""
    m = len(pesos); n = min(n, m)
    pref = [0.0]
    for p in pesos:
        pref.append(pref[-1] + p)
    INF = (float('inf'), float('inf'))
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    corte = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = (0.0, 0.0)
    for k in range(1, n + 1):
        for j in range(k, m + 1):
            for i in range(k - 1, j):
                prev = dp[k - 1][i]
                if prev == INF:
                    continue
                w = pref[j] - pref[i]
                cand = (max(prev[0], w), prev[1] + w * w)
                if cand < dp[k][j]:
                    dp[k][j] = cand; corte[k][j] = i
    out, j = [], m
    for k in range(n, 0, -1):
        i = corte[k][j]; out.append((i, j)); j = i
    return out[::-1]


def main():
    T = 4200
    if '--T' in sys.argv:
        T = int(sys.argv[sys.argv.index('--T') + 1])
    tope = 1.3 * T
    dens, cnt, amplias, n_notas = P.calcular()
    print(f'# {n_notas} notas | T = {T} (un día admite hasta {tope:.0f}) | sin pasaje corto: {dict(amplias)}')
    lineas, pesos_dia, livianas = [], [], []
    for d, h, nombre in P.PERICOPAS:
        a = C.idx(*map(int, d.split(':'))); b = C.idx(*map(int, h.split(':')))
        pesos = [dens[i] for i in range(a, b + 1)]
        w = sum(pesos)
        parte = PARTE[int(d.split(':')[0])]
        # átomos: versículos muy pesados van solos (varios días); los demás se agrupan
        grupos, cur = [], []
        for k, p in enumerate(pesos):
            if p > tope:
                if cur:
                    grupos.append(('grupo', cur)); cur = []
                grupos.append(('verso', [k]))
            else:
                cur.append(k)
        if cur:
            grupos.append(('grupo', cur))
        tramos = []
        for tipo, ks in grupos:
            sub = [pesos[k] for k in ks]; wg = sum(sub)
            if tipo == 'verso':
                nd = max(2, math.ceil(wg / tope))
                for q in range(nd):
                    tramos.append((ks[0], ks[0], nd, q))
            else:
                nd = max(1, math.ceil(wg / tope))
                for i, j in particion(sub, nd):
                    tramos.append((ks[i], ks[j - 1], 1, 0))
        if len(tramos) == 1:
            livianas.append((d, h, nombre, w, parte))
        for (i, j, nd, q) in tramos:
            ini = C.de_idx(a + i); fin = C.de_idx(a + j)
            pw = sum(pesos[i:j + 1]) / (nd if nd > 1 else 1)
            pesos_dia.append(pw)
            ref = (f'{ini[0]}:{ini[1]}', f'{fin[0]}:{fin[1]}')
            if nd > 1:
                foco = FOCOS.get(nd)
                extra = f", {{'foco': {foco[q][0]!r}, 'tipos': {foco[q][1]}}}" if foco else f", {{'foco': 'ENFOQUE {q + 1} DE {nd}', 'tipos': []}}"
                lineas.append(f"    ({ref[0]!r}, {ref[1]!r}, {nombre + ' (' + str(q + 1) + '/' + str(nd) + ')'!r}, {parte!r}{extra}),  # peso {pw:.0f}")
            else:
                lineas.append(f"    ({ref[0]!r}, {ref[1]!r}, {nombre!r}, {parte!r}),  # peso {pw:.0f}" + (f'  [{j - i + 1} vers.]' if j > i else ''))
    print('DIAS = [')
    print('\n'.join(lineas))
    print(']')
    print(f'\n# {len(lineas)} días | peso por día: mín {min(pesos_dia):.0f}, mediana {sorted(pesos_dia)[len(pesos_dia) // 2]:.0f}, máx {max(pesos_dia):.0f}')
    print('# Fusiones sugeridas (pericopas de un día, misma parte, que juntas caben en un día):')
    for x, y in zip(livianas, livianas[1:]):
        if x[4] == y[4] and x[3] + y[3] <= 1.2 * T and C.idx(*map(int, y[0].split(':'))) == C.idx(*map(int, x[1].split(':'))) + 1:
            print(f'#   {x[0]}–{y[1]}: {x[2]} ({x[3]:.0f}) + {y[2]} ({y[3]:.0f})')


if __name__ == '__main__':
    main()
