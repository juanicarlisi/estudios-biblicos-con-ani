"""Unidades de sentido (pericopas) de 1 Pedro a Judas y utilidades de versículos.

Índice global 1..324 en orden canónico: 1P (1-105), 2P (106-166), 1J (167-271), 2J (272-284), 3J (285-299), Jd (300-324).
Referencias: «1P 2:4-8», «1J 2:28-3:3», «Jd 3-4», «2J 7» (los libros de un capítulo no llevan capítulo). Sin sigla, `rango`
usa el libro que se le pase en `libro`. Los cortes de U siguen los bosquejos de Kistemaker (1-2 Pedro y Judas; 1-3 Juan),
MacArthur (capítulos del Comentario del NT), Beacon y Mundo Hispano; son solo cortes de lectura.
"""
import re
LIBROS = [('1P', '1 Pedro', [25, 25, 22, 19, 14]), ('2P', '2 Pedro', [21, 22, 18]), ('1J', '1 Juan', [10, 29, 24, 21, 21]),
          ('2J', '2 Juan', [13]), ('3J', '3 Juan', [15]), ('Jd', 'Judas', [25])]
SIGLAS = [s for s, _, _ in LIBROS]
NOMBRE = {s: n for s, n, _ in LIBROS}
VV = {s: v for s, _, v in LIBROS}
INI = {}; FIN = {}; _acc = 0; ACUM = {}
for s, _, v in LIBROS:
    INI[s] = _acc + 1; a = [_acc]
    for n in v: a.append(a[-1] + n)
    ACUM[s] = a; _acc = a[-1]; FIN[s] = _acc
TOTAL = _acc
assert TOTAL == 324 and [FIN[s] - INI[s] + 1 for s in SIGLAS] == [105, 61, 105, 13, 15, 25]
# grafías aceptadas para la sigla (en notas, días e índices)
ALIAS = {'1p': '1P', '1pe': '1P', '1ped': '1P', '1pedro': '1P', 'ip': '1P', 'ipe': '1P', 'ipedro': '1P',
         '2p': '2P', '2pe': '2P', '2ped': '2P', '2pedro': '2P', 'iip': '2P', 'iipe': '2P', 'iipedro': '2P',
         '1j': '1J', '1jn': '1J', '1jua': '1J', '1juan': '1J', 'ij': '1J', 'ijn': '1J', 'ijuan': '1J',
         '2j': '2J', '2jn': '2J', '2jua': '2J', '2juan': '2J', 'iij': '2J', 'iijn': '2J', 'iijuan': '2J',
         '3j': '3J', '3jn': '3J', '3jua': '3J', '3juan': '3J', 'iiij': '3J', 'iiijn': '3J', 'iiijuan': '3J',
         'jd': 'Jd', 'jud': 'Jd', 'judas': 'Jd'}
def sigla(s):
    return ALIAS.get(re.sub(r'[\s.]', '', str(s)).lower())
def idx(lib, c, v):
    caps = VV[lib]; c = min(max(c, 1), len(caps))
    return ACUM[lib][c - 1] + min(max(v, 1), caps[c - 1])
def desde_idx(i):
    """índice global -> (sigla, capítulo, versículo)"""
    for s in SIGLAS:
        if i <= FIN[s]:
            a = ACUM[s]
            for c in range(1, len(a)):
                if i <= a[c]: return s, c, i - a[c - 1]
def libro_de(i): return desde_idx(i)[0]
RE_SIG = re.compile(r'^\s*((?:[123]|I{1,3})\s*(?:P(?:e(?:d(?:ro)?)?)?|J(?:n|ua(?:n)?)?)|J(?:d|ud(?:as)?))\.?\s*(?=[\d:]|$|intro|tema)', re.I)
def _parte(lib, txt, ultimo_cap=None):
    """'2:4' / '4' (cap. entero, o versículo en libro de un capítulo) -> (c, v|None)"""
    m = re.fullmatch(r'(\d+)(?::(\d+))?', txt)
    if not m: return None
    a, b = int(m.group(1)), m.group(2)
    if len(VV[lib]) == 1:
        if b is not None: return (1, int(b)) if a == 1 else None
        return (1, a)
    if b is None:
        if ultimo_cap is not None: return (ultimo_cap, a)   # «2:4-8»: el 8 es versículo
        return (a, None)
    return (a, int(b))
def separar(ref, libro=None):
    """'1P 2:4-8' -> ('1P', '2:4-8'); sin sigla usa `libro`."""
    r = str(ref).strip()
    m = RE_SIG.match(r)
    if m:
        s = sigla(m.group(1))
        if s: return s, r[m.end():].strip()
    return libro, r
def rango(ref, libro=None):
    """Referencia -> (ini, fin) en el índice global, o None ('intro', 'tema', '1P intro', mal formada)."""
    r = str(ref).replace('–', '-').replace('—', '-').replace('\xa0', ' ').strip()
    # rango que cruza libros: «2J 12-3J 4»
    if r.count('-') == 1:
        izq, der = r.split('-')
        if RE_SIG.match(der.strip()) and sigla(RE_SIG.match(der.strip()).group(1)):
            a = rango(izq, libro); b = rango(der)
            return (a[0], b[1]) if a and b and a[0] <= b[1] else None
    lib, r = separar(r, libro)
    if lib not in VV: return None
    r = r.replace(' ', '')
    r = re.sub(r'(\d)[a-z](?=$|[-,])', r'\1', r)
    if r == '': return INI[lib], FIN[lib]
    if r in ('intro', 'tema'): return None
    if '-' in r:
        a, b = r.split('-', 1)
        pa = _parte(lib, a)
        if not pa: return None
        c1, v1 = pa
        if v1 is None:
            pb = _parte(lib, b)
            if not pb or pb[1] is not None: return None
            c2 = pb[0]
            if not (1 <= c1 <= c2 <= len(VV[lib])): return None
            return idx(lib, c1, 1), idx(lib, c2, VV[lib][c2 - 1])
        pb = _parte(lib, b, ultimo_cap=c1 if ':' not in b else None) if ':' not in b else _parte(lib, b)
        if not pb: return None
        c2, v2 = pb
        if not (1 <= c1 <= len(VV[lib]) and 1 <= c2 <= len(VV[lib])): return None
        if v1 > VV[lib][c1 - 1] or v2 > VV[lib][c2 - 1]: return None
        i0, i1 = idx(lib, c1, v1), idx(lib, c2, v2)
        return (i0, i1) if i0 <= i1 else None
    pa = _parte(lib, r)
    if not pa: return None
    c, v = pa
    if not 1 <= c <= len(VV[lib]): return None
    if v is None: return idx(lib, c, 1), idx(lib, c, VV[lib][c - 1])
    if v > VV[lib][c - 1]: return None
    return idx(lib, c, v), idx(lib, c, v)
def especial(ref):
    """'intro' / 'tema' / '1P intro' / '2J tema' -> ('intro'|'tema', sigla o None); cualquier otra cosa -> None."""
    m = re.fullmatch(r'\s*(?:(\S+)\s+)?(intro|tema)\s*', str(ref))
    if not m: return None
    s = sigla(m.group(1)) if m.group(1) else None
    if m.group(1) and not s: return None
    return m.group(2), s
def cv(i, con_sigla=True):
    s, c, v = desde_idx(i)
    t = f'{v}' if len(VV[s]) == 1 else f'{c}:{v}'
    return f'{s} {t}' if con_sigla else t
def etiqueta(i0, i1):
    """(ini, fin) -> '1P 2:4-8', '1J 2:28-3:3', 'Jd 3-4', '2J 7', '2J 12-3J 4'"""
    s0, c0, v0 = desde_idx(i0); s1, c1, v1 = desde_idx(i1)
    if i0 == i1: return cv(i0)
    if s0 != s1: return f'{cv(i0)}-{cv(i1)}'
    if c0 == c1: return f'{cv(i0)}-{v1}'
    return f'{cv(i0)}-{c1}:{v1}'
# (id, rango, título provisional)
U = [
 # 1 Pedro (Kistemaker; MacArthur caps. 1-24)
 ('1p-saludo', '1P 1:1-2', 'Elegidos y extranjeros: el saludo'), ('1p-esperanza', '1P 1:3-5', 'Una esperanza viva y una herencia guardada'),
 ('1p-gozo', '1P 1:6-9', 'Gozo en medio de las pruebas'), ('1p-profetas', '1P 1:10-12', 'Lo que los profetas indagaron'),
 ('1p-santos', '1P 1:13-16', '«Sed santos»'), ('1p-rescate', '1P 1:17-21', 'Rescatados con la sangre preciosa de Cristo'),
 ('1p-amor', '1P 1:22-25', 'Amor entrañable y la palabra que permanece'), ('1p-leche', '1P 2:1-3', 'Desear la leche espiritual'),
 ('1p-piedras', '1P 2:4-8', 'Piedras vivas y la piedra angular'), ('1p-pueblo', '1P 2:9-10', 'Linaje escogido, real sacerdocio'),
 ('1p-peregrinos', '1P 2:11-12', 'Extranjeros y peregrinos: buena manera de vivir'), ('1p-autoridades', '1P 2:13-17', 'Sumisión a las autoridades'),
 ('1p-siervos', '1P 2:18-20', 'Los siervos y el sufrimiento injusto'), ('1p-ejemplo', '1P 2:21-25', 'Cristo, ejemplo, sustituto y Pastor'),
 ('1p-hogar', '1P 3:1-7', 'Esposas y maridos'), ('1p-unidad', '1P 3:8-12', 'Unidad y bendición'),
 ('1p-defensa', '1P 3:13-17', 'Sufrir por hacer el bien y presentar defensa'), ('1p-espiritus', '1P 3:18-22', 'Cristo padeció una vez: los espíritus y el bautismo'),
 ('1p-armaos', '1P 4:1-6', 'Armarse del mismo pensamiento'), ('1p-fin', '1P 4:7-11', 'El fin de todas las cosas se acerca: dones y servicio'),
 ('1p-fuego', '1P 4:12-19', 'La prueba de fuego: sufrir como cristiano'), ('1p-ancianos', '1P 5:1-4', 'Apacentad la grey de Dios'),
 ('1p-humildad', '1P 5:5-7', 'Revestidos de humildad'), ('1p-adversario', '1P 5:8-11', 'Resistid al adversario'), ('1p-saludos', '1P 5:12-14', 'Silvano, Marcos y Babilonia: saludos'),
 # 2 Pedro (Kistemaker; MacArthur caps. 25-33)
 ('2p-saludo', '2P 1:1-4', 'Una fe igualmente preciosa y las grandes promesas'), ('2p-virtudes', '2P 1:5-11', 'Añadid a vuestra fe: las virtudes'),
 ('2p-legado', '2P 1:12-15', 'El legado de Pedro antes de su partida'), ('2p-testigos', '2P 1:16-18', 'Testigos de su majestad: la transfiguración'),
 ('2p-profecia', '2P 1:19-21', 'La palabra profética más segura'), ('2p-falsos', '2P 2:1-3', 'Habrá falsos maestros'),
 ('2p-juicio', '2P 2:4-10', 'Ángeles, diluvio, Sodoma: Dios sabe librar y juzgar'), ('2p-conducta', '2P 2:11-16', 'Atrevidos y contumaces: el camino de Balaam'),
 ('2p-perdicion', '2P 2:17-22', 'Fuentes sin agua: peor que al principio'), ('2p-burladores', '2P 3:1-7', 'Los burladores y el diluvio'),
 ('2p-paciencia', '2P 3:8-10', 'Mil años como un día: el día del Señor vendrá'), ('2p-consumacion', '2P 3:11-13', 'Cielos nuevos y tierra nueva'),
 ('2p-exhortacion', '2P 3:14-18', 'Pablo, las Escrituras y creced en la gracia'),
 # 1 Juan (Kistemaker; MacArthur caps. 1-18)
 ('1j-prologo', '1J 1:1-4', 'El Verbo de vida: lo que hemos visto y oído'), ('1j-luz', '1J 1:5-10', 'Dios es luz: andar en luz y confesar'),
 ('1j-abogado', '1J 2:1-6', 'Abogado y propiciación: guardar sus mandamientos'), ('1j-mandamiento', '1J 2:7-11', 'El mandamiento nuevo y antiguo'),
 ('1j-hijitos', '1J 2:12-14', 'Hijitos, padres y jóvenes'), ('1j-mundo', '1J 2:15-17', 'No améis al mundo'),
 ('1j-anticristos', '1J 2:18-23', 'Es el último tiempo: los anticristos'), ('1j-uncion', '1J 2:24-27', 'Permanecer y la unción del Santo'),
 ('1j-hijos', '1J 2:28-3:3', 'Hijos de Dios: lo que hemos de ser'), ('1j-pecado', '1J 3:4-10', 'El que es nacido de Dios no practica el pecado'),
 ('1j-cain', '1J 3:11-18', 'Caín y el amor de hecho y en verdad'), ('1j-confianza', '1J 3:19-24', 'Confianza delante de Dios'),
 ('1j-espiritus', '1J 4:1-6', 'Probad los espíritus'), ('1j-amor', '1J 4:7-12', 'Dios es amor'), ('1j-perfecto', '1J 4:13-21', 'El perfecto amor echa fuera el temor'),
 ('1j-vence', '1J 5:1-5', 'La fe que vence al mundo'), ('1j-testimonio', '1J 5:6-12', 'Agua, sangre y Espíritu: el testimonio de Dios'),
 ('1j-oracion', '1J 5:13-17', 'Para que sepáis que tenéis vida eterna: la oración'), ('1j-certezas', '1J 5:18-21', 'Sabemos: certezas finales y los ídolos'),
 # 2 Juan
 ('2j-saludo', '2J 1-3', 'El anciano a la señora elegida'), ('2j-verdad', '2J 4-6', 'Andar en la verdad y en el amor'),
 ('2j-enganadores', '2J 7-11', 'Engañadores: no recibirlos en casa'), ('2j-despedida', '2J 12-13', 'Cara a cara'),
 # 3 Juan
 ('3j-gayo', '3J 1-4', 'Gayo, el amado, anda en la verdad'), ('3j-hospitalidad', '3J 5-8', 'Colaboradores de la verdad: la hospitalidad'),
 ('3j-diotrefes', '3J 9-10', 'Diótrefes, que ama tener el primer lugar'), ('3j-demetrio', '3J 11-12', 'Imitar lo bueno: Demetrio'), ('3j-despedida', '3J 13-15', 'Paz a ti'),
 # Judas (Kistemaker; MacArthur)
 ('jd-saludo', 'Jd 1-2', 'Llamados, amados y guardados'), ('jd-proposito', 'Jd 3-4', 'Contender ardientemente por la fe'),
 ('jd-ejemplos', 'Jd 5-7', 'Israel, los ángeles, Sodoma y Gomorra'), ('jd-sonadores', 'Jd 8-10', 'Soñadores: Miguel y el diablo'),
 ('jd-cain', 'Jd 11-13', 'Caín, Balaam y Coré: nubes sin agua'), ('jd-enoc', 'Jd 14-16', 'La profecía de Enoc'),
 ('jd-exhortacion', 'Jd 17-23', 'Vosotros, amados: edificaos, conservaos, tened misericordia'), ('jd-doxologia', 'Jd 24-25', 'Al que es poderoso para guardaros'),
]
UNIDADES = []
for id_, r, t in U:
    a, b = rango(r); UNIDADES.append({'id': id_, 'rango': r, 'ini': a, 'fin': b, 'titulo': t, 'libro': libro_de(a)})
assert UNIDADES[0]['ini'] == 1 and UNIDADES[-1]['fin'] == TOTAL
for x, y in zip(UNIDADES, UNIDADES[1:]): assert y['ini'] == x['fin'] + 1, (x, y)
for u in UNIDADES: assert libro_de(u['ini']) == libro_de(u['fin']), u
if __name__ == '__main__':
    import collections
    print(len(UNIDADES), 'unidades;', dict(collections.Counter(u['libro'] for u in UNIDADES)))
    for r in ('1P 2:4-8', '1J 2:28-3:3', 'Jd 3-4', '2J 7', '3J 1:5', '1P 2', '2P', '2J 12-3J 4', '1 Pedro 5:13', 'I Jn 4:8', 'Jud. 14-15',
              '4:8', '1P intro', '1P 6:1', 'Jd 26', '1P 1:25-2:3'):
        x = rango(r, libro='1J'); print(f'{r!r:16} -> {x} {etiqueta(*x) if x else ""}')
