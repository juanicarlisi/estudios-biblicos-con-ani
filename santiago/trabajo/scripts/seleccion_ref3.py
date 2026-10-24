#!/usr/bin/env python3
"""Selecciona, en dos niveles, el texto de los libros confiables (REFERENCIA3, categoría A) que trata Santiago.

Nivel 1: tramos de 3 o más páginas seguidas con mucha señal (o 2 páginas con señal muy alta): se toman completos.
Nivel 2: ventanas de líneas alrededor de las citas de Santiago en el resto de las páginas.
Quita obras repetidas (la que comparte más de la mitad de sus líneas con otra mayor) y las ventanas que son solo listas de citas.
Luego arma los bloques de lectura TMP/segmentos/ref3/r1_NNN.txt (nivel 1) y r2_NNN.txt (nivel 2).
Uso: seleccion_ref3.py [--umbral1 6] [--tope-bloque 80000]
"""
import hashlib, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import config as C
from indice_santiago import citas, RE_F

UMBRAL1 = float(sys.argv[sys.argv.index('--umbral1') + 1]) if '--umbral1' in sys.argv else 6.0
MAX = int(sys.argv[sys.argv.index('--tope-bloque') + 1]) if '--tope-bloque' in sys.argv else 80000
IDX = os.path.join(C.TMP, 'indice', 'indice_todo.json')
DEST = os.path.join(C.TMP, 'segmentos', 'ref3')


def lineas_clave(txt):
    out = set()
    for l in txt.split('\n'):
        l = re.sub(r'\W+', '', l.lower())
        if len(l) > 45:
            out.add(hashlib.md5(l.encode()).hexdigest()[:12])
    return out


def es_lista(t):
    refs = len(re.findall(r'\d{1,3}:\d{1,3}', t)); words = len(t.split())
    return words == 0 or refs / words > 0.12


def main():
    idx = json.load(open(IDX))
    cl = {x['path']: x for x in json.load(open(C.CLASIFICACION))}
    # 1) niveles
    t1, t2 = [], []
    vistos = set()
    for k, v in sorted(idx.items()):
        txt = open(v['txt'], errors='ignore').read()
        h = hashlib.md5(re.sub(r'\s+', '', txt[:200000]).encode()).hexdigest()
        if h in vistos:
            continue
        vistos.add(h)
        pags = txt.split('\f')
        sc = {x['pag']: x['score'] for x in v['paginas']}
        fuertes = sorted(p for p, s in sc.items() if s >= UMBRAL1 and len(pags[p - 1]) < 12000)
        runs, cur = [], []
        for p in fuertes:
            if cur and p == cur[-1] + 1:
                cur.append(p)
            else:
                if cur: runs.append(cur)
                cur = [p]
        if cur: runs.append(cur)
        usadas = set()
        for r in runs:
            if len(r) >= 3 or (len(r) == 2 and sum(sc[p] for p in r) >= 4 * UMBRAL1):
                usadas.update(r)
                t1.append({'k': k, 'pags': r, 'texto': '\n'.join(f'--- [pág. PDF {p}] ---\n' + pags[p - 1].strip() for p in r)})
        for pn, p in enumerate(pags, 1):
            if pn in usadas or pn not in sc:
                continue
            lines = p.split('\n'); marcas = []
            for i, l in enumerate(lines):
                if citas(l) or len(RE_F.findall(l)) >= 2:
                    marcas.append(i)
            if not marcas:
                continue
            win = set()
            for i in marcas:
                win.update(range(max(0, i - 6), min(len(lines), i + 7)))
            segs, cur = [], []
            for j in sorted(win):
                if cur and j != cur[-1] + 1:
                    segs.append(cur); cur = []
                cur.append(j)
            if cur: segs.append(cur)
            for s in segs:
                t = ' '.join(lines[j].strip() for j in s)
                if len(t) > 250:
                    t2.append({'k': k, 'pag': pn, 'texto': t[:3000]})
    # 2) obras repetidas
    keys = sorted({x['k'] for x in t1} | {x['k'] for x in t2})
    tam = {k: len(open(idx[k]['txt'], errors='ignore').read()) for k in keys}
    sets = {k: lineas_clave(open(idx[k]['txt'], errors='ignore').read()) for k in keys}
    drop = {}
    ks = sorted(keys, key=lambda k: -tam[k])
    for i, a in enumerate(ks):
        if a in drop:
            continue
        for b in ks[i + 1:]:
            if b in drop or not sets[b]:
                continue
            ov = len(sets[a] & sets[b]) / len(sets[b])
            if ov > 0.5:
                drop[b] = (a, round(ov, 2))
    t1 = [x for x in t1 if x['k'] not in drop]
    t2 = [x for x in t2 if x['k'] not in drop and not es_lista(x['texto']) and len(x['texto']) >= 400]
    c1 = sum(len(x['texto']) for x in t1); c2 = sum(len(x['texto']) for x in t2)
    print(f'umbral {UMBRAL1}: nivel 1: {len(t1)} tramos, {c1} caracteres | nivel 2: {len(t2)} ventanas, {c2} caracteres | duplicados descartados: {len(drop)}')
    print(f'  → bloques de {MAX}: unos {(c1 + c2) // MAX + 2}')
    # 3) bloques
    os.makedirs(DEST, exist_ok=True)
    for f in os.listdir(DEST):
        os.remove(os.path.join(DEST, f))

    def meta(k):
        x = cl.get(k, {})
        return x.get('autor') or 'autor no consignado', x.get('titulo') or os.path.basename(k)

    indice = []

    def volcar(items, pref):
        cur, out = '', []
        for it in items:
            a, t = meta(it['k'])
            if 'pags' in it:
                b = f"\n##### OBRA: {t} | AUTOR: {a} | ARCHIVO: {it['k']} | páginas PDF {it['pags'][0]}-{it['pags'][-1]}\n{it['texto']}\n"
            else:
                b = f"\n##### OBRA: {t} | AUTOR: {a} | ARCHIVO: {it['k']} | pág. PDF {it['pag']} (fragmento)\n{it['texto']}\n"
            if len(b) > MAX:
                b = b[:MAX]
            if len(cur) + len(b) > MAX and cur:
                out.append(cur); cur = ''
            cur += b
        if cur:
            out.append(cur)
        for i, t in enumerate(out, 1):
            fn = os.path.join(DEST, f'{pref}_{i:03d}.txt')
            open(fn, 'w').write(t)
            indice.append({'id': f'{pref}_{i:03d}', 'archivo': fn, 'chars': len(t)})

    volcar(sorted(t1, key=lambda x: (x['k'], x['pags'][0])), 'r1')
    volcar(sorted(t2, key=lambda x: (x['k'], x['pag'])), 'r2')
    json.dump(indice, open(os.path.join(DEST, '_indice.json'), 'w'), indent=0)
    cc = collections.Counter(i['id'][:2] for i in indice)
    print('bloques', dict(cc), 'caracteres', sum(i['chars'] for i in indice))
    por_obra = collections.Counter()
    for x in t1: por_obra[x['k']] += len(x['texto'])
    for x in t2: por_obra[x['k']] += len(x['texto'])
    print('obras con más texto seleccionado:')
    for k, n in por_obra.most_common(25):
        print(f'  {n:8d} {k[:100]}')
    json.dump({'duplicados': drop}, open(os.path.join(C.TMP, 'indice', 'duplicados.json'), 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
