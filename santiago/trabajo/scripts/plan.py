#!/usr/bin/env python3
"""Arma plan/plan.json a partir de la lista de días de abajo y controla que cubra Santiago entero, sin huecos ni superposiciones.

Cada día es (desde, hasta, título, parte) y, si el pasaje se estudia en varios días, un diccionario con
  {'foco': 'Lo que dice el texto', 'tipos': [tipos de nota que le tocan]} (los días de un mismo pasaje van seguidos y repiten desde/hasta).
La cantidad de días sale del material disponible (scripts/plan_densidad.py), no de un tope de versículos: 20 a 30 minutos de lectura por día.
"""
import json, os, sys, statistics
sys.path.insert(0, os.path.dirname(__file__))
import config as C

# Tipos de nota por enfoque (para los pasajes que se estudian en varios días)
TIPOS_TEXTO = ['explicacion_texto', 'contexto_historico', 'cultura_costumbres', 'arqueologia_geografia', 'griego_palabra', 'estructura_bosquejo', 'cronologia_fechas', 'personaje']
TIPOS_DEBATE = ['teologia_doctrina', 'dificultad_interpretaciones', 'apologetica', 'conexion_biblica', 'cristo_en_santiago', 'eco_de_jesus']
TIPOS_VIDA = ['aplicacion_practica', 'ilustracion', 'pregunta_reflexion', 'matrimonio_familia']

DIAS = []   # se completa después de medir el material: ('1:1', '1:1', 'Título', 'I')  o  ('2:14', '2:14', 'Título', 'II', {'foco': '…', 'tipos': TIPOS_TEXTO})


def main():
    dias, prev, i = [], 0, 0
    grupos = {}
    for d in DIAS:
        a, b, t, p = d[:4]
        extra = d[4] if len(d) > 4 else None
        grupos.setdefault((a, b), []).append(extra)
    for n, d in enumerate(DIAS, 1):
        a, b, t, p = d[:4]
        extra = d[4] if len(d) > 4 else None
        ia, ib = C.idx(*map(int, a.split(':'))), C.idx(*map(int, b.split(':')))
        rep = n >= 2 and (DIAS[n - 2][0], DIAS[n - 2][1]) == (a, b)
        assert (ia == prev + 1) or rep, f'día {n}: empieza en {a} pero el anterior terminó en el índice {prev}'
        assert ib >= ia, f'día {n}: rango invertido'
        reg = {'dia': n, 'desde': a, 'hasta': b, 'titulo': t, 'parte': p, 'versiculos': ib - ia + 1}
        if extra:
            k = grupos[(a, b)]
            posicion = 1 + sum(1 for q in DIAS[:n - 1] if (q[0], q[1]) == (a, b))
            reg['compartido'] = {'n': posicion, 'de': len(k)}
            reg.update(extra)
        dias.append(reg); prev = max(prev, ib)
    assert prev == C.TOTAL_VERSICULOS, f'el plan termina en el versículo {prev} de {C.TOTAL_VERSICULOS}'
    os.makedirs(os.path.join(C.REPO_TRABAJO, 'plan'), exist_ok=True)
    json.dump(dias, open(os.path.join(C.REPO_TRABAJO, 'plan', 'plan.json'), 'w'), ensure_ascii=False, indent=1)
    vs = [d['versiculos'] for d in dias]
    print(len(dias), 'días; versículos por día: promedio', round(statistics.mean(vs), 1), 'mín', min(vs), 'máx', max(vs), '| días de un versículo:', sum(1 for v in vs if v == 1))
    for p in ('I', 'II', 'III', 'IV', 'V'):
        print(p, sum(1 for d in dias if d['parte'] == p), 'días')


if __name__ == '__main__':
    main()
