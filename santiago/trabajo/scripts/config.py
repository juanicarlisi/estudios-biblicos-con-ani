"""Rutas y constantes del estudio de Santiago.

REPO_TRABAJO guarda lo que se versiona (notas extraídas, plan, días, artículos, textos, scripts).
TMP guarda lo voluminoso y regenerable (texto completo de los libros, bloques de lectura, insumos de cada día),
que no se sube al repositorio.
"""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO_TRABAJO = os.environ.get('SANTIAGO_TRABAJO') or os.path.abspath(os.path.join(AQUI, '..'))   # santiago/trabajo (SANTIAGO_TRABAJO sirve para pruebas)
REPO_SANTIAGO = os.path.abspath(os.path.join(AQUI, '..', '..'))          # santiago
REPO_RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))        # estudios-biblicos-con-ani
TMP = os.environ.get('TRABAJO_SANTIAGO', '/home/user/trabajo_santiago')
BIBLIOTECA = os.environ.get('BIBLIOTECA', '/home/user/biblioteca-estudios-biblicos/MATERIAL SOPORTE')
REF3 = os.environ.get('REF3', '/home/user/libros-referencia3')
CLASIFICACION = os.path.join(REPO_RAIZ, 'genesis', 'trabajo', 'clasificacion', 'clasificacion.json')

# Versículos por capítulo de Santiago (1:27, 2:26, 3:18, 4:17, 5:20 = 108)
V = [27, 26, 18, 17, 20]
ACUM = [0]
for _n in V:
    ACUM.append(ACUM[-1] + _n)
TOTAL_VERSICULOS = ACUM[-1]


def idx(c, v):
    """Índice (1 a 108) del versículo c:v."""
    c = max(1, min(5, c))
    v = max(1, min(V[c - 1], v))
    return ACUM[c - 1] + v


def de_idx(i):
    """Inverso de idx: (capítulo, versículo)."""
    for c in range(1, 6):
        if i <= ACUM[c]:
            return c, i - ACUM[c - 1]
    return 5, V[4]
