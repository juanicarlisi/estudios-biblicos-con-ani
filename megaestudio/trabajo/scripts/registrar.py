#!/usr/bin/env python3
"""Agrega a trabajo/libros.json los libros de autores confiables (categoría A) de las carpetas indicadas del catálogo.
Uso: registrar.py ref3 "Apologetica" "Relacion con Dios" ...   (no pisa ids ya existentes; salta duplicados y duplicados de título)"""
import json, os, re, sys, unicodedata
AQUI = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(AQUI, '..'))
cat = json.load(open(f'{V}/catalogo/catalogo.json')); lib = json.load(open(f'{V}/libros.json'))
repo, areas = sys.argv[1], set(sys.argv[2:])
def slug(t): t = unicodedata.normalize('NFD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c)); return re.sub(r'[^a-z0-9]+', '_', t).strip('_')
rutas = {b.get('path') for b in lib.values()}; titulos = {slug(b['obra']) for b in lib.values()}
n = 0
for c in cat:
    if c['repo'] != repo or c['area'] not in areas or c['categoria'] != 'A' or c['duplicado_de'] or not c['path'].lower().endswith('.pdf'): continue
    if c['path'] in rutas or slug(c['titulo'] or c['path']) in titulos: continue
    ap = slug((c['autor'] or 'anon').split(',')[0].split(' y ')[0].split()[-1]) if c['autor'] else 'anon'
    i = '_'.join(slug(c['titulo'] or os.path.basename(c['path'])).split('_')[:3]) + '__' + ap
    k = i; j = 2
    while k in lib: k = f'{i}{j}'; j += 1
    lib[k] = {'repo': repo, 'path': c['path'], 'autor': c['autor'], 'obra': c['titulo'] or os.path.basename(c['path'])}
    rutas.add(c['path']); titulos.add(slug(lib[k]['obra'])); n += 1
json.dump(lib, open(f'{V}/libros.json', 'w'), ensure_ascii=False, indent=1)
print('agregados', n, '· total', len(lib))
