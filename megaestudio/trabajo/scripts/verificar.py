#!/usr/bin/env python3
"""Verificación por programa (sin IA) de los días del megaestudio.

Controla, en cada día:
  forma     campos obligatorios, apartados, preguntas y oración.
  fuentes   cada texto lleva fuentes; cada «libro#pág» existe en libros.json y la página existe ('biblia' = texto bíblico citado).
  citas     cada cita textual (campo citas[].texto) está, palabra por palabra, en las páginas citadas.
  comillas  cada frase entre «» de 5 o más palabras está en las páginas citadas del mismo texto o en la RVR1960 de algún capítulo citado en el día.
  biblia    cada referencia «Libro C:V» existe (capítulo y versículo) en la RVR1960.
  cifras    cada número de 3 o más cifras (no de referencias) aparece en las páginas citadas del texto.
  autores   el autor de cada libro nombrado en un texto figura entre sus fuentes (advertencia).
Salida: una línea por día (OK / flags). Uso: verificar.py [N ...]   (sin números: todos los días)"""
import json, os, re, sys, glob, unicodedata
AQUI = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(AQUI, '..'))
sys.path.insert(0, AQUI)
from rvr import normalizar, capitulo, LIBROS  # noqa: E402
PAGS = os.environ.get('MEGA_TXT', '/home/user/lib/pages')
LIB = json.load(open(f'{V}/libros.json'))
_cache = {}
GENERICAS = {'varios', 'autores', 'editores', 'serie', 'otros', 'otras', 'colaboradores', 'equipo', 'redaccion', 'general', 'generales', 'internacional', 'consta', 'reina', 'valera', 'nueva', 'version', 'biblia', 'santa', 'sociedad', 'sociedades', 'iglesia', 'editorial', 'ministerio', 'ministerios', 'casa', 'mundo', 'hispano', 'comentario', 'diccionario', 'estudio', 'estudios', 'bautista', 'cristiano', 'cristiana', 'antiguo', 'testamento', 'tomo', 'volumen', 'instituto', 'seminario', 'universidad', 'moody', 'beacon'}
for _n, _o, _a in LIBROS:
    for _w in (_n + ' ' + _a).split():
        GENERICAS.add(''.join(c for c in unicodedata.normalize('NFD', _w.lower()) if not unicodedata.combining(c)))
def paginas(i):
    if i not in _cache: _cache[i] = json.load(open(f'{PAGS}/{i}.json'))
    return _cache[i]
def norm(t):
    t = unicodedata.normalize('NFD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()
def limpio(t):  # une saltos de línea y guiones de corte
    return norm(re.sub(r'-\n', '', t))
RE_ID = re.compile(r'^([a-z0-9_]+)#(\d+)$')
RE_REF = re.compile(r'(?<![\w])((?:[123]\s?)?[A-ZÁÉÍÓÚ][a-záéíóúñ]+)\.?\s+(\d+):(\d+)(?:\s*[-–]\s*(\d+))?')
RE_COM = re.compile(r'«([^»]+)»')
_cap = {}
def cap(libro, c):
    k = (libro[0], c)
    if k not in _cap: _cap[k] = capitulo(libro[0], libro[1], c)
    return _cap[k]

def unidades(o, ruta=''):
    """Cada dict con 'fuentes': (ruta, texto completo del dict, fuentes)."""
    if isinstance(o, dict):
        if 'fuentes' in o and isinstance(o['fuentes'], list):
            txt = ' '.join(str(v) for k, v in o.items() if isinstance(v, str))
            yield ruta, txt, o['fuentes'], o
        for k, v in o.items():
            if k != 'fuentes': yield from unidades(v, f'{ruta}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from unidades(v, f'{ruta}[{i}]')


def vecino_citado(txt, ap, citados):
    """True si, junto a la palabra `ap` escrita con mayúscula (hasta dos palabras de distancia), hay un apellido de un autor citado
    (p. ej. «George Eldon Ladd»: George es nombre de pila, Ladd es el autor citado)."""
    toks = re.findall(r"[\wáéíóúñüÁÉÍÓÚÑ]+", txt)
    for i, t in enumerate(toks):
        if norm(t) == ap and t[:1].isupper():
            for j in range(max(0, i - 2), min(len(toks), i + 3)):
                if j != i and toks[j][:1].isupper() and norm(toks[j]) in citados: return True
    return False

def verificar(n):
    d = json.load(open(f'{V}/dias/dia_{n:03d}.json')); flags = []
    def f(ruta, tipo, det): flags.append(f'{tipo} {ruta}: {det}')
    for k in ('titulo', 'bajada', 'minutos', 'lectura', 'versiculos', 'entrada', 'apartados', 'para_vivir', 'para_reflexionar', 'para_orar'):
        if not d.get(k): f('', 'forma', f'falta {k}')
    if not 3 <= len(d.get('apartados', [])) <= 8: f('', 'forma', f'apartados={len(d.get("apartados", []))}')
    if len(d.get('para_reflexionar', [])) < 3: f('', 'forma', 'menos de 3 preguntas')
    tot = 0; refs_dia = set(); com_dia = []
    for ruta, txt, fu, obj in unidades(d):
        tot += len(txt.split())
        if not fu: f(ruta, 'fuentes', 'sin fuentes'); continue
        sin_bib = [x for x in fu if x != 'biblia']
        textos = []
        for x in fu:
            if x == 'biblia': continue
            m = RE_ID.match(x)
            if not m or m.group(1) not in LIB: f(ruta, 'fuentes', f'id inválido {x}'); continue
            ps = paginas(m.group(1)); p = int(m.group(2))
            if not 1 <= p <= len(ps): f(ruta, 'fuentes', f'página fuera de rango {x}'); continue
            textos.append((m.group(1), limpio(ps[p - 1])))
        base = ' '.join(t for _, t in textos)
        # citas textuales
        if 'autor' in obj and 'texto' in obj and ruta.startswith('.citas'):
            if norm(obj['texto']) not in base: f(ruta, 'citas', f'no está literal: «{obj["texto"][:70]}»')
        # frases entre «»
        for c in RE_COM.findall(txt):
            if len(c.split()) >= 5 and ruta.startswith('.citas') is False:
                com_dia.append((ruta, c, base))
        # cifras
        txt_cif = ' '.join(str(v) for k, v in obj.items() if isinstance(v, str) and k != 'obra')   # el título de una obra (p. ej. «101 respuestas…») no es una cifra afirmada
        sinref = RE_REF.sub(' ', txt_cif)
        for num in re.findall(r'\b\d[\d.]{2,}\b', sinref):
            dig = re.sub(r'\D', '', num)
            if dig not in re.sub(r'\D', '', ' ' + base) and dig not in base.replace(' ', ''):
                f(ruta, 'cifras', f'{num} no figura en las fuentes citadas')
        # autores nombrados: se compara por apellido (el apellido del autor de algún libro citado, o que aparezca en la página citada)
        ap_citados = set()
        for i2, _ in textos:
            if LIB[i2]['repo'] == 'web': continue
            for a in re.split(r'\s+y\s+|,|;', re.sub(r'\(.*?\)', '', LIB[i2]['autor'] or '')):
                w = norm(a).split()
                if w: ap_citados.add(w[-1])
        ntxt = norm(txt)
        mayus = {norm(w) for w in re.findall(r'\b[A-ZÁÉÍÓÚÑ][\wáéíóúñü]+', txt)}   # solo cuentan las palabras escritas con mayúscula (apellidos, no palabras comunes)
        base_aut = base + ' ' + ' '.join(norm(LIB[i2].get('url', '')) + ' ' + ' '.join(limpio(x) for x in paginas(i2)) for i2 in {i3 for i3, _ in textos} if LIB[i2]['repo'] == 'web')   # el autor de una fuente web puede figurar en su URL
        for ap in sorted({norm(a).split()[-1] for b in LIB.values() if b['repo'] != 'web' for a in re.split(r'\s+y\s+|,|;', re.sub(r'\(.*?\)', '', b['autor'] or '')) if norm(a).split()} - GENERICAS):
            if len(ap) > 4 and ap not in ap_citados and ap in mayus and not vecino_citado(txt, ap, ap_citados) and not re.search(rf'\b{ap}\b', base_aut):
                f(ruta, 'autores', f'nombra a «{ap}» sin citar un libro suyo ni figurar en las páginas citadas')
        for m in RE_REF.finditer(txt):
            refs_dia.add(m.group(0))
    for v in d.get('versiculos', []): refs_dia.add(v['ref'])
    for c in d.get('conexiones', []): refs_dia.add(c['ref'])
    # biblia: existencia + texto de capítulos
    texto_rvr = ''
    vistos = set()
    for r in sorted(refs_dia):
        r2 = re.sub(r'(\d+:\d+)\s*[-–]\s*(\d+).*', r'\1-\2', r)
        r2 = re.sub(r'^((?:2|3)\s?Jn|(?:2|3)\s?Juan|Jud|Judas|Abd|Abdías|Flm|Filemón)\s+(\d+)', r'\1 1:\2', r2)   # libros de un solo capítulo
        nz = normalizar(r2.replace('–', '-'))
        if not nz: f('', 'biblia', f'referencia no reconocida: {r}'); continue
        libro, c, v1, v2 = nz
        try: vs = cap(libro, c)
        except Exception as e: f('', 'biblia', f'no se pudo bajar {r}: {e}'); continue
        if not vs: f('', 'biblia', f'capítulo inexistente: {r}'); continue
        if any(v not in vs for v in range(v1, v2 + 1)): f('', 'biblia', f'versículo inexistente: {r}')
        if (libro[0], c) not in vistos: vistos.add((libro[0], c)); texto_rvr += ' ' + ' '.join(vs.values())
    rvr_n = norm(texto_rvr)
    for ruta, c, base in com_dia:
        cn = norm(c)
        if cn not in base and cn not in rvr_n: f(ruta, 'comillas', f'«{c[:80]}» no está en las fuentes ni en la RVR1960 citada')
    if not 1800 <= tot <= 3300: f('', 'forma', f'palabras={tot} (esperado 1.800-3.300; la guía apunta a 2.800)')
    return tot, flags

if __name__ == '__main__':
    ns = [int(a) for a in sys.argv[1:]] or sorted(int(os.path.basename(p)[4:7]) for p in glob.glob(f'{V}/dias/dia_*.json'))
    for n in ns:
        if not os.path.exists(f'{V}/dias/dia_{n:03d}.json'): print(f'día {n}: todavía no existe'); continue
        tot, fl = verificar(n)
        print(f'día {n}: {"OK" if not fl else f"{len(fl)} marcas"} · {tot} palabras')
        for x in fl: print('   ', x)
