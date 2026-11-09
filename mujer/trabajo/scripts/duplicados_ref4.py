#!/usr/bin/env python3
"""Marca los libros de REFERENCIA4 cuyo texto ya está en REFERENCIA3 o la biblioteca (huellas de 8-gramas; contención ≥ 0,5).
Escribe mujer/duplicados_ref4.json {archivo_ref4: archivo_existente}. Sin IA."""
import json, os, re, sys, hashlib, collections
sys.path.insert(0, '/home/user/trabajo/mujer/scripts')
from puntajes import fuentes, norm  # noqa: E402
C = '/home/user/trabajo/corpus_ref4'
def huella(t):
    pal = re.findall(r'[a-z]{3,}', norm(t)); hs = set()
    for i in range(0, max(0, len(pal) - 8), 7):
        h = int(hashlib.md5(' '.join(pal[i:i + 8]).encode()).hexdigest()[:8], 16)
        if h % 8 == 0: hs.add(h)
    return hs
idx = collections.defaultdict(set); nombres = []
for fu, arch, f in fuentes():
    t = open(f, errors='ignore').read()
    if len(t) < 5000: continue
    k = len(nombres); nombres.append(f'{fu}:{arch}')
    for h in huella(t): idx[h].add(k)
print('libros existentes', len(nombres), flush=True)
dup = {}; propios = {}
for l in open(f'{C}/_manifiesto.jsonl'):
    m = json.loads(l); p = m['path']
    f = f'{C}/{p}.ocr.txt' if os.path.exists(f'{C}/{p}.ocr.txt') else f'{C}/{p}.txt'
    if not os.path.exists(f): continue
    t = open(f, errors='ignore').read()
    if len(t) < 5000: continue
    hs = huella(t)
    if not hs: continue
    cont = collections.Counter(k for h in hs if h in idx for k in idx[h])
    if cont:
        k, c = cont.most_common(1)[0]
        if c / len(hs) >= 0.5: dup[p] = nombres[k]
    propios[p] = hs
# repetidos dentro de REFERENCIA4: conservar el de más texto
ks = sorted(propios, key=lambda p: -len(propios[p])); vivos = []
for p in ks:
    if p in dup: continue
    for q in vivos:
        if len(propios[p] & propios[q]) / max(1, len(propios[p])) >= 0.5:
            dup[p] = 'ref4:' + q; break
    else: vivos.append(p)
json.dump(dup, open('/home/user/trabajo/mujer/duplicados_ref4.json', 'w'), ensure_ascii=False, indent=0)
print('duplicados de REFERENCIA4:', len(dup), 'de', len(propios))
