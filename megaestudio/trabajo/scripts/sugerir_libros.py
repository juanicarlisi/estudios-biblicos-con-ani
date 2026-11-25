#!/usr/bin/env python3
"""Sugiere, para el tema de un día, los libros de TODA la biblioteca registrada que más hablan de él, con sus mejores páginas.
Por defecto solo muestra libros que no son comentarios ni teologías sistemáticas (vida cristiana, sermones, apologética, devocionales, historia, estudios temáticos).
Uso: sugerir_libros.py N [--top 15] [--todos] [--extra "regex adicional"]
Toma las palabras de búsqueda del título del día y de la ficha plan/specs/dia_NNN.md (sección «Pistas de búsqueda» y títulos); se puede sumar --extra."""
import json, os, re, sys, unicodedata
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(AQUI, '..')); sys.path.insert(0, AQUI)
from tipos import tipo
PAGS = os.environ.get('MEGA_TXT', '/home/user/lib/pages')
LIB = json.load(open(f'{V}/libros.json'))
STOP = set('sobre entre desde hasta cuando donde porque como para cada todo toda todos todas esto esta este estos estas otros otras tiene tienen puede pueden segun dice dicen cual cuales mismo misma serie estudio fuentes libros autores pistas busqueda regex'.split())
def norm(t): return ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if not unicodedata.combining(c))
def terminos(n, extra):
    plan = {p['dia']: p for p in json.load(open(f'{V}/plan/plan.json'))}[n]
    ficha = open(f'{V}/plan/specs/dia_{n:03d}.md', encoding='utf-8').read()
    piezas = []
    m = re.search(r'\*\*Pistas de búsqueda\*\*[^:]*:(.*)', ficha, re.S)
    if m:
        for x in re.split(r'[;|,]', m.group(1)):
            x = x.strip().strip('.')
            if '(' in x or ')' in x or x.lower().startswith(('comentario', 'diccionario', 'libros ', 'fuentes ')): continue
            if x and 3 <= len(x) <= 40 and not re.match(r'^(web_|ver |ids )', x) and ' ' not in x.strip() or (x and len(x.split()) <= 4 and 3 <= len(x) <= 40 and not x.startswith(('web_', 'ver '))): piezas.append(x)
    for w in re.findall(r'[A-Za-zÁÉÍÓÚáéíóúñÑ]{6,}', plan['titulo']):
        if norm(w) not in STOP: piezas.append(w)
    if extra: piezas += [x for x in extra.split('|') if x.strip()]
    out = []; vistos = set()
    for p in piezas:
        k = norm(p)
        if k in vistos or k in STOP or re.fullmatch(r'[a-z0-9_]+', k) and k in LIB: continue
        vistos.add(k); out.append(p)
    return out[:40]
def puntuar(args):
    i, pat = args
    try: pags = json.load(open(f'{PAGS}/{i}.json'))
    except Exception: return (i, 0, [])
    rx = re.compile('|'.join(re.escape(t) for t in pat), re.I); mejores = []
    for n, p in enumerate(pags, 1):
        h = rx.findall(p)
        if h:
            d = len({norm(x) for x in h}); mejores.append((d * 3 + min(len(h), 8), n))
    mejores.sort(reverse=True); top = mejores[:3]
    return (i, sum(s for s, _ in top), [n for _, n in top])
if __name__ == '__main__':
    n = int(sys.argv[1]); topn = int(sys.argv[sys.argv.index('--top') + 1]) if '--top' in sys.argv else 15
    extra = sys.argv[sys.argv.index('--extra') + 1] if '--extra' in sys.argv else ''
    todos = '--todos' in sys.argv
    T = terminos(n, extra); print('Términos:', ', '.join(T))
    cand = [i for i, b in LIB.items() if b['repo'] != 'web' and (todos or tipo(b) == 'otros') and os.path.exists(f'{PAGS}/{i}.json')]
    with Pool(3) as pool: res = pool.map(puntuar, [(i, T) for i in cand], chunksize=8)
    res = [r for r in res if r[1] > 0]; res.sort(key=lambda r: -r[1])
    print(f'{len(cand)} libros revisados; los {topn} más pertinentes:\n')
    for i, s, ps in res[:topn]:
        b = LIB[i]; p = json.load(open(f'{PAGS}/{i}.json'))[ps[0] - 1]; m = re.search('|'.join(re.escape(t) for t in T), p, re.I)
        ext = re.sub(r'\s+', ' ', p[max(0, m.start() - 60):m.start() + 160]) if m else ''
        print(f"[{i}] {b['autor']} — {b['obra'][:60]} · páginas {', '.join(map(str, ps))} · puntaje {s}\n    …{ext}…")
