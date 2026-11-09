#!/usr/bin/env python3
"""Depura las notas extraídas por IA de bloques (r_, w_, b_, o_) contra el texto del bloque, sin IA:
 · quita la «cita» que no está en el bloque (la nota queda sin cita);
 · descarta la nota si su contenido casi no tiene apoyo léxico en todo el bloque (<30 %) o trae cifras ausentes del bloque.
Uso: depurar_notas.py [prefijo ...]   (por defecto r_). Deja revision/notas_descartadas.json."""
import json, glob, re, sys, unicodedata, os
V = '/home/user/trabajo/mujer'
def nz(s): return re.sub(r'\s+', ' ', re.sub(r'[^\w]+', ' ', ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(c)))).strip()
st = lambda t: {w[:5] for w in nz(t).split() if len(w) >= 5}
pref = tuple(sys.argv[1:]) or ('r_',)
desc, citas_q, total = [], 0, 0
for f in sorted(glob.glob(f'{V}/notas/*.json')):
    b = os.path.basename(f)[:-5]
    if not b.startswith(pref): continue
    txt = open(f'{V}/bloques/{b}.txt', errors='ignore').read()
    nt, ts, dg = nz(txt), st(txt), re.sub(r'\D', '', txt)
    d = json.load(open(f)); keep = []
    for n in d['notas']:
        total += 1
        c = n.get('cita')
        if c and nz(c) not in nt:
            n['cita'] = ''; citas_q += 1
        s = st(n['contenido'])
        r = len(s & ts) / len(s) if len(s) >= 8 else 1
        nu = [re.sub(r'\D', '', x) for x in re.findall(r'\d[\d.,]*\d', n['contenido']) if len(x) >= 3]
        mal = [x for x in nu if x not in dg]
        if r < 0.30 or mal:
            desc.append({'bloque': b, 'titulo': n['titulo'], 'fuente': n['fuente'], 'pagina': n.get('pagina'), 'apoyo': round(r, 2), 'cifras_ausentes': mal[:3]}); continue
        keep.append(n)
    if len(keep) != len(d['notas']) or True:
        d['notas'] = keep; json.dump(d, open(f, 'w'), ensure_ascii=False)
os.makedirs(f'{V}/revision', exist_ok=True)
json.dump(desc, open(f'{V}/revision/notas_descartadas.json', 'w'), ensure_ascii=False, indent=0)
print(f'notas {total} | citas quitadas {citas_q} | notas descartadas {len(desc)} ({len(desc)/max(total,1):.1%})')
