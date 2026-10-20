#!/usr/bin/env python3
"""Coteja cada «cita textual» de las notas con el texto del libro (su bloque y su página).

Resultado en varon/revision/citas.json {id: {estado, pagina_real?, parecido}}:
  'ok'      la cita está en la página indicada (o a una página de distancia)
  'otra'    está en el libro pero en otra página (se guarda la página real)
  'ocr'     coincide con un parecido ≥ 90 % (texto escaneado con errores de reconocimiento)
  'no'      no aparece: la cita no se usa como textual (el contenido de la nota sigue valiendo)
Uso: verificar_citas.py
"""
import json, glob, os, re, unicodedata, collections
from rapidfuzz import fuzz

V = '/home/user/trabajo/varon'


def norm(s):
    s = unicodedata.normalize('NFKC', s).lower()
    s = re.sub(r'(\w)-\s+(\w)', r'\1\2', s)          # palabras cortadas al final de la línea
    s = re.sub(r'[^\w]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def paginas_bloque(b):
    t = open(f'{V}/bloques/{b}.txt', errors='ignore').read()
    out = collections.defaultdict(dict)
    partes = re.split(r'^=== \[(\w+) \| pág\. ([^\]]+)\] ===$', t, flags=re.M)
    for k in range(1, len(partes) - 2, 3):
        fid, pag, txt = partes[k], partes[k + 1].strip(), partes[k + 2]
        try:
            out[fid][int(pag)] = norm(txt)
        except ValueError:
            pass
    return out


def rango(p):
    ns = [int(x) for x in re.findall(r'\d+', p or '')]
    if not ns:
        return set()
    a, b = ns[0], ns[-1] if len(ns) > 1 and ns[-1] >= ns[0] and ns[-1] - ns[0] < 40 else ns[0]
    return set(range(a - 1, b + 2))


def main():
    res, cache = {}, {}
    cuenta = collections.Counter()
    for f in sorted(glob.glob(f'{V}/notas/*.json')):
        b = os.path.basename(f)[:-5]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            c = (n.get('cita') or '').strip()
            if not c:
                continue
            nid = f'{b}#{i}'
            if b not in cache:
                cache = {b: paginas_bloque(b)}
            pags = cache[b].get(n.get('fuente'), {})
            trozos = [norm(x) for x in re.split(r'\.\.\.|…|\[\.\.\.\]', c) if len(norm(x).split()) >= 3] or [norm(c)]
            cerca = [pags[p] for p in sorted(rango(n.get('pagina'))) if p in pags]
            # unir páginas vecinas por si la cita cruza de una a otra
            cerca_t = ' '.join(cerca)
            if all(t in cerca_t for t in trozos):
                r = {'estado': 'ok'}
            else:
                reales = [p for p, txt in pags.items() if all(t in txt for t in trozos)]
                if reales:
                    r = {'estado': 'otra', 'pagina_real': str(reales[0])}
                else:
                    sc = min(fuzz.partial_ratio(t, cerca_t) if cerca_t else 0 for t in trozos)
                    if sc < 90:
                        todo = ' '.join(pags.values())
                        sc = max(sc, min(fuzz.partial_ratio(t, todo) for t in trozos) if todo and len(todo) < 400000 else 0)
                    r = {'estado': 'ocr' if sc >= 90 else 'no', 'parecido': round(sc)}
            res[nid] = r; cuenta[r['estado']] += 1
    os.makedirs(f'{V}/revision', exist_ok=True)
    json.dump(res, open(f'{V}/revision/citas.json', 'w'), ensure_ascii=False, indent=0)
    print('citas revisadas:', sum(cuenta.values()), dict(cuenta))


if __name__ == '__main__':
    main()
