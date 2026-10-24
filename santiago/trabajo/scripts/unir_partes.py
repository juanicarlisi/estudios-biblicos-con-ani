#!/usr/bin/env python3
"""Une las tandas de notas de un bloque en su archivo definitivo.

Uso: unir_partes.py <id_bloque> [--ref3]
Lee TMP/partes/<id>.p1.json, .p2.json… (cada una: {"notas": [...], "problemas": "..." (opcional), "descartados": N (opcional)}),
las junta en orden y escribe santiago/trabajo/extracciones/<id>.json (o extracciones_ref3/ con --ref3) con la forma
{"bloque": id, "notas": [...], "problemas": "..." } (en ref3, «descartados» en vez de «problemas»).
Si alguna tanda no es JSON válido, dice cuál y en qué línea para corregirla; no escribe nada.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

bid = sys.argv[1]
ref3 = '--ref3' in sys.argv
partes = sorted(glob.glob(os.path.join(C.TMP, 'partes', f'{bid}.p*.json')), key=lambda f: int(re.search(r'\.p(\d+)\.json$', f).group(1)))
if not partes:
    print(f'No hay tandas en {C.TMP}/partes/{bid}.p1.json …'); sys.exit(1)
notas, problemas, descartados = [], [], 0
for f in partes:
    try:
        d = json.load(open(f))
    except json.JSONDecodeError as e:
        print(f'ERROR: {os.path.basename(f)} no es JSON válido: {e}'); sys.exit(1)
    if isinstance(d, list):
        d = {'notas': d}
    notas += d.get('notas', [])
    if d.get('problemas'):
        problemas.append(d['problemas'])
    descartados += int(d.get('descartados') or 0)
destino = os.path.join(C.REPO_TRABAJO, 'extracciones_ref3' if ref3 else 'extracciones')
os.makedirs(destino, exist_ok=True)
salida = {'bloque': bid, 'notas': notas}
if ref3:
    salida['descartados'] = descartados
else:
    salida['problemas'] = ' '.join(problemas)
json.dump(salida, open(os.path.join(destino, bid + '.json'), 'w'), ensure_ascii=False, indent=1)
print(f'{bid}: {len(notas)} notas de {len(partes)} tandas → {destino}/{bid}.json')
