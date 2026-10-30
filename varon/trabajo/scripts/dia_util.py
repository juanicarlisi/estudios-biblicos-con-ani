#!/usr/bin/env python3
"""Utilidades compartidas del flujo de días: unidades de texto de un día, insumo parseado, capítulos RVR en caché local.

Las unidades de texto son los campos con «texto» (o cadena) que el lector ve; cada una se identifica con una ruta
(p. ej. «apartados[1].parrafos[0].texto») y puede llevar «fuentes» (ids de notas o datos W).
"""
import json, os, re, time, subprocess, html, unicodedata
from concurrent.futures import ThreadPoolExecutor

V = '/home/user/trabajo/varon'
CAP = f'{V}/biblia/cap'      # capítulos RVR1960 para verificar (caché local, NO se sube al repositorio)


def unidades(x):
    """Devuelve [(ruta, texto, fuentes|None)] de todo el texto visible de un día."""
    out = []

    def add(ruta, texto, fuentes=None):
        if isinstance(texto, str) and texto.strip():
            out.append((ruta, texto, fuentes))

    add('bajada', x.get('bajada'))
    add('lectura.porque', x.get('lectura', {}).get('porque'))
    for k, v in enumerate(x.get('versiculos', [])):
        add(f'versiculos[{k}].porque', v.get('porque'))
    add('entrada.texto', x.get('entrada', {}).get('texto'), x.get('entrada', {}).get('fuentes'))
    for a, s in enumerate(x.get('apartados', [])):
        add(f'apartados[{a}].titulo', s.get('titulo'))
        for p, q in enumerate(s.get('parrafos', [])):
            add(f'apartados[{a}].parrafos[{p}].texto', q.get('texto'), q.get('fuentes'))
        d = s.get('destacado') or {}
        add(f'apartados[{a}].destacado.texto', d.get('texto'), d.get('fuentes'))
    for k, c in enumerate(x.get('citas', [])):
        add(f'citas[{k}].texto', c.get('texto'), c.get('fuentes'))
    for k, d in enumerate(x.get('datos', [])):
        add(f'datos[{k}].texto', d.get('texto'), d.get('fuentes'))
    m = x.get('modelo') or {}
    add('modelo.texto', m.get('texto'), m.get('fuentes'))
    for k, w in enumerate(x.get('palabras', [])):
        add(f'palabras[{k}].significado', w.get('significado'), w.get('fuentes'))
    for k, i in enumerate(x.get('interpretaciones', [])):
        for j, p in enumerate(i.get('posturas', [])):
            add(f'interpretaciones[{k}].posturas[{j}].postura', p.get('postura'), p.get('fuentes'))
        add(f'interpretaciones[{k}].nota', i.get('nota'))
    for k, c in enumerate(x.get('conexiones', [])):
        add(f'conexiones[{k}].nota', c.get('nota'), c.get('fuentes'))
    for k, v in enumerate(x.get('para_vivir', [])):
        add(f'para_vivir[{k}].texto', v.get('texto'), v.get('fuentes'))
    for k, q in enumerate(x.get('para_reflexionar', [])):
        add(f'para_reflexionar[{k}]', q)
    for k, q in enumerate(x.get('para_conversar', [])):
        add(f'para_conversar[{k}]', q)
    add('para_orar', x.get('para_orar'))
    for k, f in enumerate(x.get('profundizar', [])):
        add(f'profundizar[{k}].texto', f.get('texto'), f.get('fuentes'))
    return out


def poner(x, ruta, texto):
    """Reemplaza el texto de una ruta (la misma que devuelve unidades())."""
    partes = re.findall(r'[^.\[\]]+|\[\d+\]', ruta)
    cur = x
    for p in partes[:-1]:
        cur = cur[int(p[1:-1])] if p.startswith('[') else cur[p]
    last = partes[-1]
    cur[int(last[1:-1]) if last.startswith('[') else last] = texto


def insumo(d):
    """{id: texto} de las notas y datos del insumo de un día."""
    t = open(f'{V}/insumos/dia_{d:03d}.txt', errors='ignore').read()
    out, cur = {}, None
    for l in t.split('\n'):
        m = re.match(r'^\[([^\]]+)\]\s', l)
        if m:
            cur = m.group(1); out[cur] = l
        elif cur and l.startswith('### '):
            cur = None
        elif cur:
            out[cur] += '\n' + l
    return out


def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', re.sub(r'[^\w]+', ' ', s)).strip()


# ---------- capítulos RVR1960 (caché local) ----------
def _bajar_cap(osis, nombre, c):
    from rvr import P, UA
    fn = f'{CAP}/{osis}_{c}.json'
    if os.path.exists(fn):
        return json.load(open(fn))
    os.makedirs(CAP, exist_ok=True)
    r = subprocess.run(['curl', '-sS', '-m', '40', '-A', UA, '-G', 'https://www.biblegateway.com/passage/', '--data-urlencode', f'search={nombre} {c}',
                        '--data-urlencode', 'version=RVR1960'], capture_output=True, text=True)
    t = r.stdout
    i = t.find('<div class="passage-text">'); j = t.find('<div class="footnotes">', i)
    p = P(osis, c); p.feed(t[i:j if j > 0 else None])
    vs = {str(v): re.sub(r'\s+', ' ', html.unescape(s)).strip() for v, s in p.verses.items() if s.strip()}
    if vs:
        json.dump(vs, open(fn, 'w'), ensure_ascii=False)
    return vs


def capitulo(nombre_osis_c):
    return _bajar_cap(*nombre_osis_c)


def traer_capitulos(refs, hilos=4):
    """refs: iterable de textos de referencia; baja a la caché los capítulos que falten y devuelve cuántos."""
    from rvr import normalizar
    need = set()
    for r in refs:
        n = normalizar(r)
        if n:
            (nombre, osis), c, v1, v2 = n
            if not os.path.exists(f'{CAP}/{osis}_{c}.json'):
                need.add((osis, nombre, c))
    need = sorted(need)

    def uno(t):
        time.sleep(0.3)
        try:
            return bool(_bajar_cap(*t))
        except Exception:
            return False
    with ThreadPoolExecutor(hilos) as ex:
        ok = sum(ex.map(uno, need))
    return ok, len(need)


RE_REF = re.compile(r'\b((?:[123]\s)?[A-ZÁÉÍÓÚ][a-záéíóúñ]+(?:\s[a-záéíóú]+)?)\s(\d{1,3}):(\d{1,3})(?:\s?[-–]\s?(\d{1,3}))?')


def refs_en(texto):
    """Referencias bíblicas escritas en un texto (con nombre de libro reconocible)."""
    from rvr import normalizar
    out = []
    for m in RE_REF.finditer(texto):
        s = m.group(0)
        n = normalizar(s)
        if not n:
            n = normalizar(m.group(1).split()[0] + ' ' + s[len(m.group(1)):].strip()) if ' ' in m.group(1) else None
        if n:
            out.append((s, n))
    return out
