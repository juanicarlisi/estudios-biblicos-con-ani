#!/usr/bin/env python3
"""OCR de un PDF escaneado a texto con \\f entre páginas (Tesseract, español).

Uso: ocr_pdf.py <entrada.pdf> <salida.txt> [procesos]
Renderiza cada página a 300 ppp en grises, sube el contraste y pasa Tesseract. Guarda páginas parciales para retomar.
"""
import os, subprocess, sys, tempfile
from multiprocessing import Pool
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(__file__))
import config as C


def paginas(pdf):
    out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith('Pages:'):
            return int(line.split()[1])
    return 0


def ocr_pagina(args):
    pdf, n, cache = args
    dst = os.path.join(cache, f'{n:05d}.txt')
    if os.path.exists(dst):
        return n
    with tempfile.TemporaryDirectory(dir=os.path.join(C.TMP, 'tmp')) as td:
        base = os.path.join(td, 'p')
        subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-r', '300', '-gray', '-png', pdf, base], capture_output=True, timeout=600)
        imgs = [f for f in os.listdir(td) if f.endswith('.png')]
        texto = ''
        if imgs:
            p = os.path.join(td, imgs[0])
            ImageOps.autocontrast(Image.open(p).convert('L')).save(p)
            r = subprocess.run(['tesseract', p, 'stdout', '-l', 'spa', '--psm', '3'], capture_output=True, text=True, timeout=900,
                               env={**os.environ, 'OMP_THREAD_LIMIT': '1'})
            texto = r.stdout
    tmp = dst + '.tmp'
    open(tmp, 'w').write(texto)
    os.replace(tmp, dst)
    return n


if __name__ == '__main__':
    pdf, salida = sys.argv[1], sys.argv[2]
    procs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    os.makedirs(os.path.join(C.TMP, 'tmp'), exist_ok=True)
    cache = salida + '.paginas'
    os.makedirs(cache, exist_ok=True)
    total = paginas(pdf)
    with Pool(procs) as pool:
        for i, _ in enumerate(pool.imap_unordered(ocr_pagina, [(pdf, n, cache) for n in range(1, total + 1)]), 1):
            if i % 20 == 0:
                print(f'{i}/{total}', flush=True)
    open(salida, 'w').write('\f'.join(open(os.path.join(cache, f'{n:05d}.txt')).read() for n in range(1, total + 1)))
    print('FIN', total, flush=True)
