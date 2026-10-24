#!/usr/bin/env python3
"""Carga de todas las notas extraídas (comentarios de la biblioteca y barrido de REFERENCIA3), con ids estables «bloque#n».

Las notas de la biblioteca viven en santiago/trabajo/extracciones/<bloque>.json; las de REFERENCIA3, en extracciones_ref3/.
Este módulo lo usan el plan, los insumos de cada día, el validador y el armador.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

COMENTARIOS = {
    'macarthur': 'MacArthur, Comentario del NT: Santiago', 'kistemaker': 'Kistemaker, Comentario al NT: Santiago',
    'carballosa': 'Carballosa, Santiago: una fe en acción', 'george': 'Elizabeth George, Santiago: crece en sabiduría y fe',
    'cbmh': 'Comentario Bíblico Mundo Hispano (Carro)', 'beacon': 'Comentario Bíblico Beacon (Harper)',
    'macarthur_be': 'Biblia de Estudio MacArthur', 'dbmh': 'Diccionario Bíblico Mundo Hispano',
}


def prefijo(bloque):
    return re.sub(r'_\d+$', '', bloque)


def rango(ref):
    """(inicio, fin) en índice de versículo (1 a 108), o None si no es un pasaje (intro, tema)."""
    r = str(ref).strip().replace('–', '-').replace('—', '-').replace(' ', '')
    r = re.sub(r'^(Stg|Santiago)\.?', '', r, flags=re.I)
    m = re.fullmatch(r'(\d+)(?::(\d+)(?:-(?:(\d+):)?(\d+))?)?', r)
    if not m:
        return None
    c1 = int(m.group(1))
    if not 1 <= c1 <= 5:
        return None
    if m.group(2) is None:
        return C.idx(c1, 1), C.idx(c1, C.V[c1 - 1])
    v1 = int(m.group(2))
    if m.group(4) is None:
        return C.idx(c1, v1), C.idx(c1, v1)
    c2 = int(m.group(3)) if m.group(3) else c1
    return C.idx(c1, v1), C.idx(c2, int(m.group(4)))


def cargar(incluir_ref3=True):
    notas = []
    for f in sorted(glob.glob(os.path.join(C.REPO_TRABAJO, 'extracciones', '*.json'))):
        b = os.path.basename(f)[:-5]
        for i, n in enumerate(json.load(open(f))['notas'], 1):
            n = dict(n); n['id'] = f'{b}#{i}'; n['origen'] = 'biblio'; n['bloque'] = b
            n['fuente'] = COMENTARIOS.get(prefijo(b), prefijo(b))
            notas.append(n)
    if incluir_ref3:
        for f in sorted(glob.glob(os.path.join(C.REPO_TRABAJO, 'extracciones_ref3', '*.json'))):
            b = os.path.basename(f)[:-5]
            for i, n in enumerate(json.load(open(f))['notas'], 1):
                n = dict(n); n['id'] = f'{b}#{i}'; n['origen'] = 'ref3'; n['bloque'] = b
                n['fuente'] = f"{n.get('autor', '')}, {n.get('obra', '')}"
                notas.append(n)
    return notas


def linea(n):
    """Texto de una nota tal como lo lee quien escribe el día."""
    pag = n.get('pagina', '')
    partes = [f"[{n['id']}] Stg {n['ref']} · {n.get('tipo', '')} · imp {n.get('importancia', '')} · {n['fuente']} ({pag})",
              f"  {n.get('titulo', '')}: {n.get('contenido', '')}"]
    if n.get('cita'):
        partes.append(f"  CITA: «{n['cita']}»")
    if n.get('griego'):
        g = n['griego']; partes.append(f"  GRIEGO: {g.get('palabra', '')} ({g.get('transliteracion', '')}): {g.get('significado', '')}")
    if n.get('postura'):
        partes.append(f"  POSTURAS: {n['postura']}")
    if n.get('refs_biblicas'):
        partes.append(f"  REFS: {', '.join(n['refs_biblicas'][:12])}")
    return '\n'.join(partes)


def palabras(n):
    return len(str(n.get('contenido', '')).split()) + len(str(n.get('titulo', '')).split())
