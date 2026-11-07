#!/usr/bin/env python3
"""Baja el texto de las páginas de Coalición por el Evangelio (lista en fuentes_web/cpe/urls.json) a pages.jsonl. Sin IA; reanudable."""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
D = '/home/user/trabajo/mujer/fuentes_web/cpe'
UA = 'Mozilla/5.0 (compatible; estudio-biblico-privado)'
SECS = ['mujeres', 'para-ser-sinceras', 'piensa', 'teologia-y-praxis', 'publication', 'series', 'article']
urls = json.load(open(f'{D}/urls.json'))
hechas = set()
if os.path.exists(f'{D}/pages.jsonl'):
    hechas = {json.loads(l)['url'] for l in open(f'{D}/pages.jsonl')}
cola = [(s, u) for s in SECS for u in urls.get(s, []) if u not in hechas and u.count('/') > 4]

def uno(su):
    s, u = su
    for _ in range(2):
        r = subprocess.run(['curl', '-s', '-m', '40', '-L', '-A', UA, u], capture_output=True, text=True)
        if len(r.stdout) > 2000:
            break
        time.sleep(1)
    else:
        return {'url': u, 'sec': s, 'error': True}
    b = BeautifulSoup(r.stdout, 'html.parser')
    e = b.select_one('.entry-content') or b.select_one('article')
    t = b.select_one('h1')
    art = b.select_one('article')
    cab = ''
    if art:
        cab = re.sub(r'\s+', ' ', ' '.join(art.get_text(' ', strip=True).split(' Compartir')[0:1]))[:200]
    if not e:
        return {'url': u, 'sec': s, 'error': True}
    for x in e.select('script,style,.share,.sharedaddy,form,aside'):
        x.decompose()
    return {'url': u, 'sec': s, 'titulo': t.get_text(' ', strip=True) if t else '', 'cab': cab, 'texto': re.sub(r'\s+', ' ', e.get_text(' ', strip=True))}

n = 0
with open(f'{D}/pages.jsonl', 'a') as f, ThreadPoolExecutor(8) as ex:
    for r in ex.map(uno, cola):
        f.write(json.dumps(r, ensure_ascii=False) + '\n'); n += 1
        if n % 500 == 0:
            f.flush(); print(n, len(cola), flush=True)
print('listo', n)
