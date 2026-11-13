#!/usr/bin/env python3
"""Arma fichas para clasificar libros sin clasificar: nombre, carpeta, páginas y un extracto de las primeras páginas.
Uso: fichas.py <salida_dir> [lote=40]   → lote_NN.json con [{n, repo, path, paginas, extracto}] de todo el catálogo con categoria '?'.
Los comentarios de «biblio» se deduplican por contenido (el mismo PDF aparece en varias carpetas de libros)."""
import json, os, re, subprocess, sys, hashlib, zipfile
AQUI = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(AQUI, '..'))
RAICES = {'ref3': '/home/user/lib/r3', 'ref4': '/home/user/lib/r4', 'biblio': '/home/user/lib/bib'}
out = sys.argv[1]; lote = int(sys.argv[2]) if len(sys.argv) > 2 else 40; os.makedirs(out, exist_ok=True)
cat = json.load(open(f'{V}/catalogo/catalogo.json'))
def extracto(f):
    try:
        if f.lower().endswith('.pdf'):
            t = subprocess.run(['pdftotext', '-f', '1', '-l', '4', f, '-'], capture_output=True, timeout=60).stdout.decode('utf-8', 'replace')
            n = next((int(l.split()[1]) for l in subprocess.run(['pdfinfo', f], capture_output=True, text=True, timeout=30).stdout.splitlines() if l.startswith('Pages:')), 0)
        elif f.lower().endswith('.docx'):
            x = zipfile.ZipFile(f).read('word/document.xml').decode('utf-8', 'replace'); t = re.sub(r'<[^>]+>', ' ', x); n = 0
        else: return '', 0
    except Exception as e: return f'[no se pudo leer: {e}]', 0
    return re.sub(r'\s+', ' ', t).strip()[:1400], n
fichas = []; vistos = {}
for c in cat:
    if c['categoria'] != '?': continue
    f = os.path.join(RAICES[c['repo']], c['path'])
    if not os.path.exists(f): continue
    h = hashlib.md5(open(f, 'rb').read(2_000_000)).hexdigest() + str(os.path.getsize(f))
    if h in vistos: vistos[h]['copias'].append(c['path']); continue
    e, n = extracto(f)
    fi = {'repo': c['repo'], 'path': c['path'], 'paginas': n, 'extracto': e, 'copias': []}; vistos[h] = fi; fichas.append(fi)
for k in range(0, len(fichas), lote):
    json.dump([{'n': k + j, **x} for j, x in enumerate(fichas[k:k + lote])], open(f'{out}/lote_{k // lote:02d}.json', 'w'), ensure_ascii=False)
print(len(fichas), 'fichas únicas en', (len(fichas) + lote - 1) // lote, 'lotes')
