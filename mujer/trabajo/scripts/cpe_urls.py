#!/usr/bin/env python3
"""Baja los mapas del sitio de Coalición por el Evangelio y arma la lista de direcciones por sección. Sin IA."""
import re, json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = 'https://www.coalicionporelevangelio.org'
D = '/home/user/trabajo/mujer/fuentes_web/cpe'
UA = 'Mozilla/5.0 (compatible; estudio-biblico-privado)'

def get(u):
    r = subprocess.run(['curl', '-s', '-m', '40', '-L', '-A', UA, u], capture_output=True, text=True)
    return r.stdout

idx = get(f'{H}/sitemap.xml')
mapas = re.findall(r'<loc>([^<]*-sitemap\d*\.xml)</loc>', idx)
quiero = [m for m in mapas if re.search(r'/(mujeres|para-ser-sinceras|article|book-review|publication|essay|teologia-y-praxis|series|ebook|piensa|revista-coalicion)-sitemap\d*\.xml', m)]
def uno(m):
    return m.rsplit('/', 1)[1], re.findall(r'<loc>([^<]*)</loc>', get(m))
with ThreadPoolExecutor(6) as ex:
    res = dict(ex.map(uno, quiero))
por = {}
for k, v in res.items():
    s = re.sub(r'-sitemap\d*\.xml', '', k)
    por.setdefault(s, []).extend(v)
json.dump(por, open(f'{D}/urls.json', 'w'), ensure_ascii=False)
print({s: len(v) for s, v in por.items()})
