#!/usr/bin/env python3
"""Valida (y reúne) las notas extraídas de un bloque: apocalipsis/trabajo/extracciones/<bloque>*.json
Uso: validar_extraccion.py <bloque>   -> imprime cantidad de notas y problemas; sale con 1 si hay errores.
Cada archivo: {"bloque": id, "notas": [ {ref,tipo,titulo,contenido,pagina,importancia, ...} ], "problemas": ""}
"""
import json, sys, glob, re, os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'extracciones')
TIPOS = {'contexto_historico', 'cultura_costumbres', 'arqueologia_geografia', 'griego_palabra', 'explicacion_texto', 'teologia_doctrina',
         'cristo_en_apocalipsis', 'conexion_biblica', 'aplicacion_practica', 'ilustracion', 'dificultad_interpretaciones', 'estructura_bosquejo',
         'cronologia_fechas', 'simbolo_numero', 'personaje', 'pregunta_reflexion', 'escuelas_interpretacion', 'apologetica'}
V = [20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20, 8, 21, 18, 24, 21, 15, 27, 21]
RE_REF = re.compile(r'^(intro|tema|\d{1,2}(:\d{1,2}[a-z]?)?(-\d{1,2}[a-z]?)?|\d{1,2}:\d{1,2}[a-z]?-\d{1,2}:\d{1,2}|\d{1,2}-\d{1,2})$')
def revisar(n, i):
    errs = []
    for k in ('ref', 'tipo', 'titulo', 'contenido', 'pagina', 'importancia'):
        if k not in n or n[k] in (None, ''): errs.append(f'nota {i}: falta {k}')
    if errs: return errs
    if n['tipo'] not in TIPOS: errs.append(f"nota {i}: tipo inválido {n['tipo']}")
    r = str(n['ref']).replace(' ', '')
    if not RE_REF.match(r): errs.append(f"nota {i}: ref mal formada {n['ref']!r}")
    else:
        m = re.match(r'^(\d{1,2})', r)
        if m and r not in ('intro', 'tema') and not 1 <= int(m.group(1)) <= 22: errs.append(f"nota {i}: capítulo fuera de rango {n['ref']}")
        for c, v in re.findall(r'(\d{1,2}):(\d{1,2})', r):
            if int(c) <= 22 and int(v) > V[int(c) - 1]: errs.append(f"nota {i}: versículo inexistente {c}:{v}")
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
            e = revisar(n, f'{os.path.basename(f)}#{i}'); errs += e
            notas.append(n)
        if d.get('problemas'): problemas.append(d['problemas'])
    return fs, notas, problemas, errs
if __name__ == '__main__':
    fs, notas, problemas, errs = cargar(sys.argv[1])
    print(f'{sys.argv[1]}: {len(fs)} archivo(s), {len(notas)} notas, importancia 3={sum(1 for n in notas if n.get("importancia")==3)}')
    for e in errs[:25]: print('ERROR', e)
    if len(errs) > 25: print('... y', len(errs) - 25, 'errores más')
    if problemas: print('problemas:', ' | '.join(problemas)[:300])
    sys.exit(1 if errs or not notas else 0)
