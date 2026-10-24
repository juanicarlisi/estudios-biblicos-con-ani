#!/usr/bin/env python3
"""Cuánto material hay, versículo por versículo, para decidir cuántos días merece cada tramo de Santiago.

Cada nota que comenta un tramo corto (hasta 8 versículos) reparte su peso entre los versículos que abarca; el peso es el largo del contenido
por su importancia (3, 2 o 1). Las notas de la biblioteca cuentan entero; las de REFERENCIA3, a la mitad (suelen repetir lo que dicen los comentarios).
Imprime la densidad por versículo y por unidad de sentido (las pericopas de abajo) y una propuesta de días según el material.
Uso: plan_densidad.py [--palabras-por-dia 4200]
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import config as C
import notas as N

PESO_IMP = {3: 1.0, 2: 0.7, 1: 0.35}
PERICOPAS = [  # (desde, hasta, nombre)
    ('1:1', '1:1', 'Saludo'), ('1:2', '1:4', 'Gozo en las pruebas'), ('1:5', '1:8', 'Pedir sabiduría con fe'), ('1:9', '1:11', 'El humilde y el rico'),
    ('1:12', '1:12', 'Bienaventurado el que soporta la prueba'), ('1:13', '1:15', 'La tentación: de dónde viene'), ('1:16', '1:18', 'Todo don perfecto; el nuevo nacimiento'),
    ('1:19', '1:21', 'Pronto para oír, tardo para hablar'), ('1:22', '1:25', 'Hacedores de la palabra'), ('1:26', '1:27', 'La religión pura'),
    ('2:1', '2:4', 'Sin acepción de personas'), ('2:5', '2:7', 'Dios escogió a los pobres'), ('2:8', '2:13', 'La ley real y la misericordia'),
    ('2:14', '2:17', 'La fe sin obras es muerta'), ('2:18', '2:20', 'Demuéstrame tu fe'), ('2:21', '2:24', 'Abraham justificado por las obras'), ('2:25', '2:26', 'Rahab y la fe muerta'),
    ('3:1', '3:2', 'Los maestros y la lengua'), ('3:3', '3:5', 'El freno, el timón y la chispa'), ('3:6', '3:8', 'La lengua inflamada'), ('3:9', '3:12', 'Bendecir y maldecir con la misma boca'),
    ('3:13', '3:18', 'Las dos sabidurías'), ('4:1', '4:3', 'De dónde vienen las guerras'), ('4:4', '4:6', 'La amistad con el mundo'), ('4:7', '4:10', 'Sométanse a Dios'),
    ('4:11', '4:12', 'No hablar mal; un solo Legislador'), ('4:13', '4:17', 'Si el Señor quiere'), ('5:1', '5:6', 'Los ricos opresores'), ('5:7', '5:11', 'La paciencia'),
    ('5:12', '5:12', 'No juren'), ('5:13', '5:18', 'La oración por los enfermos'), ('5:19', '5:20', 'Hacer volver al extraviado'),
]


def main():
    ppd = 4200
    if '--palabras-por-dia' in sys.argv:
        ppd = int(sys.argv[sys.argv.index('--palabras-por-dia') + 1])
    notas = N.cargar()
    dens = [0.0] * (C.TOTAL_VERSICULOS + 2)
    cnt = [0] * (C.TOTAL_VERSICULOS + 2)
    amplias = collections.Counter()
    for n in notas:
        r = N.rango(n.get('ref', ''))
        if not r:
            amplias['intro/tema'] += 1; continue
        a, b = r
        if b - a + 1 > 8:
            amplias['tramo largo'] += 1; continue
        w = N.palabras(n) * PESO_IMP.get(int(n.get('importancia', 1)), 0.35) * (1.0 if n['origen'] == 'biblio' else 0.5)
        for i in range(a, b + 1):
            dens[i] += w / (b - a + 1); cnt[i] += 1 / (b - a + 1)
    print('notas', len(notas), '| sin pasaje corto:', dict(amplias))
    print('\nversículo: densidad (palabras ponderadas) y notas')
    for c in range(1, 6):
        fila = []
        for v in range(1, C.V[c - 1] + 1):
            i = C.idx(c, v); fila.append(f'{v}:{dens[i]:.0f}')
        print(f' cap {c}: ' + ' '.join(fila))
    print(f'\n{"unidad":42s} {"vers":>4s} {"notas":>6s} {"palabras":>8s} {"días (a "+str(ppd)+")":>12s}')
    tot_dias = 0
    for d, h, nombre in PERICOPAS:
        a = C.idx(*map(int, d.split(':'))); b = C.idx(*map(int, h.split(':')))
        pal = sum(dens[a:b + 1]); nn = sum(cnt[a:b + 1])
        dias = max(1, round(pal / ppd))
        tot_dias += dias
        print(f'{d + "-" + h:10s} {nombre:31s} {b - a + 1:4d} {nn:6.0f} {pal:8.0f} {pal / ppd:12.1f} → {dias}')
    print('días propuestos:', tot_dias)


if __name__ == '__main__':
    main()
