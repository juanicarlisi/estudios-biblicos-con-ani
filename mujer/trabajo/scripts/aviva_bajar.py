#!/usr/bin/env python3
"""Baja las transcripciones de los podcasts de Aviva Nuestros Corazones (Nancy DeMoss Wolgemuth) a fuentes_web/aviva/pages.jsonl. Sin IA; reanudable."""
import json, os, re, subprocess, time
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
D = '/home/user/trabajo/mujer/fuentes_web/aviva'
UA = 'Mozilla/5.0 (compatible; estudio-biblico-privado)'
POD = ('aviva-nuestros-corazones', 'que-amen-a-sus-hijos', 'arraigadas', 'joven-verdadera')
urls = [u.strip() for u in open(f'{D}/ep.txt') if re.search(r'/podcast/(%s)/' % '|'.join(POD), u)]
hechas = {json.loads(l)['url'] for l in open(f'{D}/pages.jsonl')} if os.path.exists(f'{D}/pages.jsonl') else set()
cola = [u for u in urls if u not in hechas]

def uno(u):
    for _ in range(2):
        r = subprocess.run(['curl', '-s', '-m', '40', '-L', '-A', UA, u], capture_output=True, text=True)
        if len(r.stdout) > 3000:
            break
        time.sleep(1)
    else:
        return {'url': u, 'error': True}
    b = BeautifulSoup(r.stdout, 'html.parser')
    e = b.select_one('[class*=transcript]')
    if not e:
        return {'url': u, 'error': True}
    t = b.title.string.split('|')[0].strip() if b.title and b.title.string else ''
    return {'url': u, 'pod': u.split('/podcast/')[1].split('/')[0], 'titulo': t, 'texto': re.sub(r'\s+', ' ', e.get_text(' ', strip=True))}

n = 0
with open(f'{D}/pages.jsonl', 'a') as f, ThreadPoolExecutor(6) as ex:
    for r in ex.map(uno, cola):
        f.write(json.dumps(r, ensure_ascii=False) + '\n'); n += 1
        if n % 100 == 0:
            f.flush(); print(n, len(cola), flush=True)
print('listo', n)
