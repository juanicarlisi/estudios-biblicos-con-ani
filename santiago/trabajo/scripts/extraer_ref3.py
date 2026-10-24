#!/usr/bin/env python3
"""Pasa a texto los libros de LIBROS-REFERENCIA3 que entran al estudio.

Entran solo los de la categoría A (autor protestante confiable) de la clasificación hecha para Génesis, sin duplicados
y sin los «resúmenes» de autor no identificado. Cada archivo queda como texto con \\f entre páginas, y un manifiesto
indica páginas, caracteres y si parece escaneado (menos de 300 caracteres por página: habría que pasarle OCR).
Uso: extraer_ref3.py [procesos]
"""
import json, os, re, subprocess, sys, tempfile, zipfile, html
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import config as C

OUT = os.path.join(C.TMP, 'corpus_ref3')
MANIF = os.path.join(OUT, '_manifiesto.jsonl')


def elegidos():
    cl = {x['path']: x for x in json.load(open(C.CLASIFICACION))}
    lista, fuera = [], []
    for root, _, files in os.walk(C.REF3):
        if '/.git' in root:
            continue
        for f in files:
            p = os.path.relpath(os.path.join(root, f), C.REF3)
            if p in ('README.md', '.gitattributes'):
                continue
            x = cl.get(p)
            if not x or x['categoria'] != 'A' or x.get('duplicado_de') or 'resumen' in p.lower():
                fuera.append((p, 'no entra: ' + (x['categoria'] if x else 'sin clasificar')))
                continue
            lista.append(p)
    return sorted(lista), fuera


def pdf_a_texto(src, dst):
    subprocess.run(['pdftotext', '-enc', 'UTF-8', src, dst], capture_output=True, timeout=1800)
    try:
        info = subprocess.run(['pdfinfo', src], capture_output=True, text=True, timeout=120).stdout
        m = re.search(r'^Pages:\s+(\d+)', info, re.M)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def docx_a_texto(src, dst):
    import docx
    d = docx.Document(src)
    partes = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            partes.append(' | '.join(c.text for c in row.cells))
    open(dst, 'w').write('\n'.join(partes))


def epub_a_texto(src, dst):
    z = zipfile.ZipFile(src)
    partes = []
    for n in sorted(z.namelist()):
        if n.lower().endswith(('.xhtml', '.html', '.htm')):
            t = z.read(n).decode('utf-8', 'ignore')
            t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', t, flags=re.S)
            t = re.sub(r'<br\s*/?>|</p>|</h\d>|</div>', '\n', t)
            t = re.sub(r'<[^>]+>', '', t)
            partes.append('\f' + html.unescape(t))
    open(dst, 'w').write('\n'.join(partes))


def doc_a_texto(src, dst, tmpdir):
    subprocess.run(['soffice', '--headless', f'-env:UserInstallation=file://{tmpdir}/lo',
                    '--convert-to', 'txt:Text (encoded):UTF8', '--outdir', tmpdir, src], capture_output=True, timeout=600)
    p = os.path.join(tmpdir, os.path.splitext(os.path.basename(src))[0] + '.txt')
    if os.path.exists(p):
        os.replace(p, dst)


def procesar(path):
    ext = os.path.splitext(path)[1].lower()
    src = os.path.join(C.REF3, path)
    dst = os.path.join(OUT, path + '.txt')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    rec = {'path': path, 'size': os.path.getsize(src), 'ext': ext, 'pages': 0, 'chars': 0, 'error': None}
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        rec['cached'] = True
        rec['chars'] = len(open(dst, errors='ignore').read())
    else:
        with tempfile.TemporaryDirectory(dir=os.path.join(C.TMP, 'tmp')) as td:
            try:
                if ext == '.pdf':
                    rec['pages'] = pdf_a_texto(src, dst)
                elif ext == '.docx':
                    docx_a_texto(src, dst)
                elif ext == '.epub':
                    epub_a_texto(src, dst)
                elif ext == '.doc':
                    doc_a_texto(src, dst, td)
                elif ext in ('.md', '.txt'):
                    open(dst, 'wb').write(open(src, 'rb').read())
                else:
                    rec['error'] = 'tipo no soportado'
            except Exception as e:
                rec['error'] = repr(e)[:300]
        if os.path.exists(dst):
            rec['chars'] = len(open(dst, errors='ignore').read())
    if ext == '.pdf' and not rec['pages'] and os.path.exists(dst):
        rec['pages'] = open(dst, errors='ignore').read().count('\f')
    rec['chars_por_pagina'] = round(rec['chars'] / rec['pages']) if rec['pages'] else None
    rec['escaneado'] = bool(ext == '.pdf' and rec['pages'] and rec['chars'] / rec['pages'] < 300)
    return rec


if __name__ == '__main__':
    os.makedirs(os.path.join(C.TMP, 'tmp'), exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    lista, fuera = elegidos()
    print(len(lista), 'archivos entran;', len(fuera), 'quedan afuera', flush=True)
    json.dump(fuera, open(os.path.join(OUT, '_fuera.json'), 'w'), ensure_ascii=False, indent=0)
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    with Pool(procs) as pool, open(MANIF, 'w') as mf:
        for i, rec in enumerate(pool.imap_unordered(procesar, lista, chunksize=1), 1):
            mf.write(json.dumps(rec, ensure_ascii=False) + '\n')
            mf.flush()
            if i % 25 == 0:
                print(i, 'hechos', flush=True)
    print('FIN', flush=True)
