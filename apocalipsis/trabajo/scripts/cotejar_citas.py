#!/usr/bin/env python3
"""Cotejo automático: toda frase entre «» en días, artículos y diagramas debe ser literal de la RVR1960 de Apocalipsis
(sin distinguir mayúsculas, tildes ni puntuación; se admiten '…' como corte). Muestra SOLO las que no coinciden.
Uso: cotejar_citas.py [--max N]"""
import glob, json, os, re, sys, unicodedata
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
AQUI = os.path.dirname(os.path.abspath(__file__)); T = AQUI + '/..'
def n(s): return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.category(c).startswith('M')))).strip()
texto = json.load(open(S + '/biblia/rvr1960_apocalipsis.json'))['texto']
B = ' ' + n(' '.join(v for c in texto.values() for v in c.values())) + ' '
def textos(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ('fuentes', 'ref'): yield from textos(v)
    elif isinstance(o, list):
        for v in o: yield from textos(v)
mal = {}; total = 0
for f in sorted(glob.glob(T + '/dias/*.json') + glob.glob(T + '/articulos/*.json') + glob.glob(T + '/diagramas/*.json')):
    for t in textos(json.load(open(f))):
        for q in re.findall(r'«([^»]+)»', t):
            total += 1
            partes = [p for p in re.split(r'…|\.\.\.|\[[^\]]*\]', q) if len(n(p)) > 0]
            if not all(' ' + n(p) + ' ' in B for p in partes): mal.setdefault(os.path.basename(f), []).append(q)
mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 3
print(f'{total} frases «» revisadas; {sum(map(len, mal.values()))} sin coincidencia en {len(mal)} archivos')
for f, l in mal.items():
    print(f'{f}: {len(l)}', *[f'   «{x[:90]}»' for x in l[:mx]], sep='\n')
