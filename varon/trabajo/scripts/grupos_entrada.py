#!/usr/bin/env python3
"""Arma las tandas de notas por sección para agruparlas por tema (paso 1 del plan).

Escribe varon/plan/grupos/in_<S>_<k>.txt (≈ TAM caracteres cada una) y varon/plan/grupos/_tandas.json.
Cada línea: id | importancia | tipo | título | subtema | refs | persona | comienzo del contenido.
Dentro de cada sección las notas se ordenan por parecido (TF-IDF + k-means), para que cada tanda junte un mismo
tema de muchos autores y los grupos salgan más completos.
"""
import json, glob, os, re, collections
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

V = '/home/user/trabajo/varon'
TAM = 120000
SECCIONES = 'ABCDEFGHIJKLMNOPQ'


def notas():
    for f in sorted(glob.glob(f'{V}/notas/*.json'), key=lambda x: (os.path.basename(x)[0], x)):
        b = os.path.basename(f)[:-5]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            yield f'{b}#{i}', n


def linea(i, n):
    c = re.sub(r'\s+', ' ', n.get('contenido', ''))[:240]
    return ' | '.join([i, str(n.get('importancia', '')), n.get('tipo', ''), n.get('titulo', ''), n.get('subtema', ''),
                       ', '.join(n.get('refs', [])[:4]), n.get('persona', '') or '', c])


VACIAS = set("""a al algo ante antes aquel aquella as así aun aunque cada como con contra cual cuando de del desde donde dos
el ella ellas ellos en entre era es esa ese eso esta este esto estos estas fue han hasta hay la las le les lo los más mas me mi
muy no nos o otra otro para pero poco por porque que qué se sea ser si sí sin sino sobre son su sus también tan tanto te tiene
todo todos tu un una uno unos y ya autor según dice afirma sostiene señala explica cuenta nota hace puede debe""".split())


def ordenar(items):
    """Ordena las notas de una sección por parecido temático."""
    if len(items) < 60:
        return items
    textos = [f"{n.get('titulo', '')} {n.get('subtema', '')} {n.get('subtema', '')} {n.get('contenido', '')[:400]} {' '.join(n.get('refs', []))} {n.get('persona', '') or ''}" for _, n in items]
    X = TfidfVectorizer(stop_words=list(VACIAS), min_df=2, max_df=0.5, sublinear_tf=True).fit_transform(textos)
    k = max(2, len(items) // 40)
    km = KMeans(n_clusters=k, n_init=4, random_state=0).fit(X)
    # ordenar los grupos en una cadena: cada uno seguido del más parecido que quede
    C = km.cluster_centers_; C = C / (np.linalg.norm(C, axis=1, keepdims=True) + 1e-9)
    sim = C @ C.T; orden = [int(np.argmax(np.bincount(km.labels_)))]; resto = set(range(k)) - set(orden)
    while resto:
        sig = max(resto, key=lambda j: sim[orden[-1], j]); orden.append(sig); resto.remove(sig)
    pos = {c: i for i, c in enumerate(orden)}
    return [it for _, it in sorted(enumerate(items), key=lambda x: (pos[km.labels_[x[0]]], x[0]))]


def main():
    crudo = collections.defaultdict(list)
    for i, n in notas():
        s = n.get('seccion', '?')
        crudo[s if s in SECCIONES else 'D'].append((i, n))
    por = {s: [linea(i, n) for i, n in ordenar(v)] for s, v in crudo.items()}
    d = f'{V}/plan/grupos'
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(f'{d}/in_*.txt'):
        os.remove(f)
    tandas = []
    for s in SECCIONES:
        ls = por.get(s, [])
        partes, actual, tam = [], [], 0
        for l in ls:
            if tam + len(l) > TAM and actual:
                partes.append(actual); actual, tam = [], 0
            actual.append(l); tam += len(l) + 1
        if actual:
            partes.append(actual)
        # repartir parejo: evitar una última tanda muy chica
        if len(partes) > 1 and len(partes[-1]) < len(partes[0]) / 3:
            todo = [l for p in partes for l in p]; k = len(partes) - 1
            partes = [todo[j * len(todo) // k:(j + 1) * len(todo) // k] for j in range(k)]
        for k, p in enumerate(partes, 1):
            nombre = f'in_{s}_{k:02d}'
            open(f'{d}/{nombre}.txt', 'w').write('\n'.join(p) + '\n')
            tandas.append({'tanda': nombre, 'seccion': s, 'notas': len(p)})
    json.dump(tandas, open(f'{d}/_tandas.json', 'w'), ensure_ascii=False, indent=0)
    print('tandas:', len(tandas), '| por sección:', {s: sum(1 for t in tandas if t['seccion'] == s) for s in SECCIONES},
          '| notas:', sum(t['notas'] for t in tandas))


if __name__ == '__main__':
    main()
