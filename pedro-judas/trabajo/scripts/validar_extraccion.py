#!/usr/bin/env python3
"""Valida (y reúne) las notas extraídas de un bloque: pedro-judas/trabajo/extracciones/<bloque>*.json
Uso: validar_extraccion.py <bloque>   -> imprime cantidad de notas y problemas; sale con 1 si hay errores.
Cada archivo: {"bloque": id, "notas": [ {ref,tipo,titulo,contenido,pagina,importancia, ...} ], "problemas": ""}
Referencias: «1P 2:4-8», «1J 2:28-3:3», «Jd 3-4», «2J 7», «1P 3» (capítulo), «2P» (libro entero), «1P intro», «intro», «tema», «1J tema».
"""
import json, sys, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'extracciones')
TIPOS = {'contexto', 'cultura', 'geografia', 'autoria_fecha', 'estructura', 'exegesis', 'griego_palabra', 'cristo', 'doctrina',
         'AT_en_NT', 'conexion_biblica', 'extrabiblico', 'falsos_maestros', 'interpretacion_discutida', 'aplicacion', 'ilustracion',
         'personaje', 'pregunta_reflexion', 'apologetica'}
def revisar(n, i):
    errs = []
    for k in ('ref', 'tipo', 'titulo', 'contenido', 'pagina', 'importancia'):
        if k not in n or n[k] in (None, ''): errs.append(f'nota {i}: falta {k}')
    if errs: return errs
    if n['tipo'] not in TIPOS: errs.append(f"nota {i}: tipo inválido {n['tipo']}")
    ref = str(n['ref'])
    if not U.especial(ref):
        lib, _ = U.separar(ref)
        if lib is None: errs.append(f"nota {i}: ref sin sigla de libro (1P, 2P, 1J, 2J, 3J, Jd) {ref!r}")
        elif U.rango(ref) is None: errs.append(f"nota {i}: ref mal formada o versículo inexistente {ref!r}")
    if n['importancia'] not in (1, 2, 3): errs.append(f'nota {i}: importancia debe ser 1, 2 o 3')
    if len(n['contenido']) < 40: errs.append(f'nota {i}: contenido muy corto')
    return errs
def cargar(bloque):
    fs = sorted(glob.glob(f'{BASE}/{bloque}.json') + glob.glob(f'{BASE}/{bloque}_[a-z].json') + glob.glob(f'{BASE}/{bloque}_[a-z][a-z].json'))
    notas = []; problemas = []; errs = []
    for f in fs:
        try: d = json.load(open(f))
        except Exception as e: errs.append(f'{os.path.basename(f)}: JSON inválido: {e}'); continue
        for i, n in enumerate(d.get('notas', []), 1):
            errs += revisar(n, f'{os.path.basename(f)}#{i}'); notas.append(n)
        if d.get('problemas'): problemas.append(d['problemas'])
    return fs, notas, problemas, errs
if __name__ == '__main__':
    fs, notas, problemas, errs = cargar(sys.argv[1])
    print(f'{sys.argv[1]}: {len(fs)} archivo(s), {len(notas)} notas, importancia 3={sum(1 for n in notas if n.get("importancia")==3)}')
    for e in errs[:25]: print('ERROR', e)
    if len(errs) > 25: print('... y', len(errs) - 25, 'errores más')
    if problemas: print('problemas:', ' | '.join(problemas)[:300])
    sys.exit(1 if errs or not notas else 0)
