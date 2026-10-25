"""Peso del material por versículo y por unidad (a partir de las notas extraídas)."""
import json, glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'extracciones')
def notas():
    out = []
    for f in sorted(glob.glob(BASE + '/*.json')):
        d = json.load(open(f))
        for i, n in enumerate(d['notas'], 1):
            n = dict(n); n['id'] = f'{os.path.basename(f)[:-5]}#{i}'; out.append(n)
    return out
def pesos():
    w = [0.0] * 405
    for n in notas():
        r = U.rango(n['ref'])
        if not r or n['importancia'] < 2: continue
        a, b = r; span = b - a + 1
        for i in range(a, b + 1): w[i] += len(n['contenido']) / (span ** 0.5 if span > 1 else 1) / (span ** 0.5 if span > 1 else 1)
    return w
if __name__ == '__main__':
    w = pesos(); tot = sum(w)
    print('material total (chars ponderados, imp>=2):', int(tot))
    for u in U.UNIDADES:
        s = sum(w[u['ini']:u['fin'] + 1]); print(f"{u['rango']:>10} {u['titulo'][:40]:40} {int(s):7d} {s/tot*100:5.1f}%  v={u['fin']-u['ini']+1}")
