#!/usr/bin/env python3
"""Busca palabras clave en los libros y devuelve las páginas más densas (para elegir qué leer).
Uso: buscar.py "regex" [id ...] [--top 8] [--ver]   (con --ver imprime un extracto de cada página)"""
import json, os, re, sys, unicodedata
OUT = os.environ.get('MEGA_TXT', '/home/user/lib/pages')
args = [a for a in sys.argv[1:] if not a.startswith('--')]
top = int(sys.argv[sys.argv.index('--top') + 1]) if '--top' in sys.argv else 8
if '--top' in sys.argv: args.remove(str(top))
pat = re.compile(unicodedata.normalize('NFC', args[0]), re.I)
ids = args[1:] or [f[:-5] for f in sorted(os.listdir(OUT)) if f.endswith('.json')]
for i in ids:
    pags = json.load(open(f'{OUT}/{i}.json'))
    pt = sorted(((len(pat.findall(p)), n + 1) for n, p in enumerate(pags) if pat.search(p)), reverse=True)[:top]
    print(f'== {i}: ' + ', '.join(f'p{n}({c})' for c, n in pt))
    if '--ver' in sys.argv:
        for c, n in pt[:3]:
            p = re.sub(r'\s+', ' ', pags[n - 1]); m = pat.search(p); s = max(0, m.start() - 150)
            print(f'   p{n}: …{p[s:s+350]}…')
