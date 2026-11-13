#!/usr/bin/env python3
"""OCR (Tesseract, español) de las páginas SIN texto de un libro del registro, y las reintegra en $MEGA_TXT/<id>.json.
Uso: ocr.py <id> [procesos]   (retoma si se corta: guarda cada página en $MEGA_TXT/ocr/<id>/NNNNN.txt)
Solo se pasa OCR a las páginas con menos de 150 caracteres de texto."""
import json, os, subprocess, sys, tempfile
from multiprocessing import Pool
from PIL import Image, ImageOps
AQUI = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(AQUI, '..'))
LIB = json.load(open(f'{V}/libros.json')); OUT = os.environ.get('MEGA_TXT', '/home/user/lib/pages')
RAICES = {'ref3': '/home/user/lib/r3', 'ref4': '/home/user/lib/r4', 'biblio': '/home/user/lib/bib'}
def pdf_de(i): b = LIB[i]; return os.path.join(RAICES[b['repo']], b['path'])
def ocr_pagina(a):
    pdf, n, dst = a
    if os.path.exists(dst): return n
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, 'p')
        subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-r', '250', '-gray', '-png', pdf, base], capture_output=True, timeout=600)
        imgs = [f for f in os.listdir(td) if f.endswith('.png')]; texto = ''
        if imgs:
            p = os.path.join(td, imgs[0]); ImageOps.autocontrast(Image.open(p).convert('L')).save(p)
            texto = subprocess.run(['tesseract', p, 'stdout', '-l', 'spa', '--psm', '3'], capture_output=True, text=True, timeout=900, env={**os.environ, 'OMP_THREAD_LIMIT': '1'}).stdout
    open(dst + '.tmp', 'w').write(texto); os.replace(dst + '.tmp', dst); return n
if __name__ == '__main__':
    i = sys.argv[1]; procs = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    pdf = pdf_de(i); ruta = f'{OUT}/{i}.json'
    total = int(next((l.split()[1] for l in subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages:')), 0))
    pags = json.load(open(ruta)) if os.path.exists(ruta) else []
    pags += [''] * (total - len(pags))
    falta = [n for n in range(1, total + 1) if len(pags[n - 1].strip()) < 150]
    cache = f'{OUT}/ocr/{i}'; os.makedirs(cache, exist_ok=True)
    print(f'{i}: {total} págs, {len(falta)} sin texto', flush=True)
    with Pool(procs) as pool:
        for k, _ in enumerate(pool.imap_unordered(ocr_pagina, [(pdf, n, f'{cache}/{n:05d}.txt') for n in falta]), 1):
            if k % 25 == 0: print(f'  {k}/{len(falta)}', flush=True)
    for n in falta: pags[n - 1] = open(f'{cache}/{n:05d}.txt').read()
    json.dump(pags, open(ruta, 'w'), ensure_ascii=False)
    print(f'{i}: listo, {sum(len(p) for p in pags)//max(1,len(pags))} c/pág', flush=True)
