#!/usr/bin/env python3
"""Extrae el texto de cada libro del registro (trabajo/libros.json) página por página (página PDF, desde 1).
Los textos NO se suben al repo (derechos): quedan en $MEGA_TXT (por defecto /home/user/lib/pages/<id>.json).
Uso: textos.py [id ...]   (sin ids: todos los que estén bajados)
Los PDF se bajan antes con: git -C /home/user/lib/r3 sparse-checkout add '<carpeta>' && git checkout   (clon parcial de libros-referencia3/4)"""
import json, os, sys, subprocess
AQUI = os.path.dirname(os.path.abspath(__file__))
LIB = json.load(open(f'{AQUI}/../libros.json'))
RAICES = {'ref3': '/home/user/lib/r3', 'ref4': '/home/user/lib/r4', 'biblio': '/home/user/lib/bib'}
OUT = os.environ.get('MEGA_TXT', '/home/user/lib/pages'); os.makedirs(OUT, exist_ok=True)
ids = sys.argv[1:] or list(LIB)
for i in ids:
    b = LIB[i]; pdf = os.path.join(RAICES[b['repo']], b['path'])
    if not os.path.exists(pdf): print('FALTA', i, pdf); continue
    txt = subprocess.run(['pdftotext', pdf, '-'], capture_output=True).stdout.decode('utf-8', 'replace')
    pags = txt.split('\f')
    if pags and not pags[-1].strip(): pags.pop()
    json.dump(pags, open(f'{OUT}/{i}.json', 'w'), ensure_ascii=False)
    n = sum(len(p) for p in pags)
    print(f'{i}: {len(pags)} págs, {n//max(1,len(pags))} c/pág')
