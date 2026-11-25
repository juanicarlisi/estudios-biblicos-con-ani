#!/usr/bin/env python3
"""Clasifica cada fuente registrada en: 'web', 'comentario' (comentarios, Biblias de estudio, diccionarios), 'doctrina' (teologías sistemáticas y obras doctrinales)
o 'otros' (vida cristiana, devocionales, sermones, apologética, historia, biografías, estudios temáticos…). Lo usan el verificador y sugerir_libros.py."""
import json, os, re
V = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
_area = None
def area_de(path):
    global _area
    if _area is None: _area = {c['path']: c['area'] for c in json.load(open(f'{V}/catalogo/catalogo.json'))}
    return _area.get(path, '')
def tipo(b):
    if b['repo'] == 'web': return 'web'
    a = area_de(b.get('path', '')); t = (b.get('obra', '') + ' ' + b.get('path', '')).lower()
    if a.startswith('01 - Biblia') or a.startswith('Comentarios por libro') or re.search(r'comentario|biblia de estudio|biblia matthew henry|diccionario|exposici[oó]n de|bosquejos', t): return 'comentario'
    if a in ('Teologia Sistematica y Doctrina', '02 - Teología y Doctrina') or re.search(r'teolog[ií]a sistem', t): return 'doctrina'
    return 'otros'
