"""Unidades de sentido de Apocalipsis (pericopas) y utilidades de versículos.
Los rangos siguen los bosquejos de Mundo Hispano, MacArthur y Beacon; son solo cortes de lectura."""
import re
V = [20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20, 8, 21, 18, 24, 21, 15, 27, 21]
ACUM = [0]
for n in V: ACUM.append(ACUM[-1] + n)
def idx(c, v): return ACUM[c - 1] + min(max(v, 1), V[c - 1])
def desde_idx(i):
    for c in range(1, 23):
        if i <= ACUM[c]: return c, i - ACUM[c - 1]
def rango(ref):
    r = str(ref).replace('–', '-').replace('—', '-').replace(' ', '')
    r = re.sub(r'[a-z]$', '', r); r = re.sub(r'(\d)[a-z]', r'\1', r)
    if r in ('intro', 'tema'): return None
    m = re.fullmatch(r'(\d+)(?::(\d+))?(?:-(\d+)(?::(\d+))?)?', r)
    if not m: return None
    c1 = int(m.group(1))
    if not 1 <= c1 <= 22: return None
    v1, a, b = m.group(2), m.group(3), m.group(4)
    if v1 is None:
        c2 = int(a) if a else c1; c2 = min(max(c2, c1), 22)
        return idx(c1, 1), idx(c2, V[c2 - 1])
    v1 = int(v1)
    if a is None: return idx(c1, v1), idx(c1, v1)
    if b is None: return idx(c1, v1), idx(c1, int(a))
    return idx(c1, v1), idx(min(int(a), 22), int(b))
def etiqueta(i0, i1):
    c0, v0 = desde_idx(i0); c1, v1 = desde_idx(i1)
    return f'{c0}:{v0}' + ('' if i0 == i1 else (f'-{v1}' if c0 == c1 else f'-{c1}:{v1}'))
# (id, desde, hasta, título provisional, parte)
U = [
 ('prologo', '1:1-3', 'Prólogo: la revelación de Jesucristo'), ('saludo', '1:4-8', 'Saludo y tema del libro'),
 ('visionpatmos', '1:9-20', 'La visión del Cristo glorificado'),
 ('efeso', '2:1-7', 'Éfeso'), ('esmirna', '2:8-11', 'Esmirna'), ('pergamo', '2:12-17', 'Pérgamo'), ('tiatira', '2:18-29', 'Tiatira'),
 ('sardis', '3:1-6', 'Sardis'), ('filadelfia', '3:7-13', 'Filadelfia'), ('laodicea', '3:14-22', 'Laodicea'),
 ('trono', '4:1-11', 'El trono en el cielo'), ('libro', '5:1-14', 'El libro sellado y el Cordero'),
 ('sellos14', '6:1-8', 'Los cuatro primeros sellos'), ('sello5', '6:9-11', 'El quinto sello'), ('sello6', '6:12-17', 'El sexto sello'),
 ('sellados', '7:1-8', 'Los sellados'), ('multitud', '7:9-17', 'La multitud vestida de blanco'), ('sello7', '8:1-5', 'El séptimo sello'),
 ('trom14', '8:6-13', 'Las cuatro primeras trompetas'), ('trom5', '9:1-12', 'La quinta trompeta'), ('trom6', '9:13-21', 'La sexta trompeta'),
 ('angel', '10:1-11', 'El ángel y el librito'), ('testigos', '11:1-14', 'Los dos testigos'), ('trom7', '11:15-19', 'La séptima trompeta'),
 ('mujer', '12:1-6', 'La mujer y el dragón'), ('guerra', '12:7-17', 'Guerra en el cielo'),
 ('bestiamar', '13:1-10', 'La bestia que sube del mar'), ('bestiatierra', '13:11-18', 'La bestia de la tierra y el 666'),
 ('cordero144', '14:1-5', 'El Cordero y los 144.000'), ('tresangeles', '14:6-13', 'Tres ángeles'), ('cosecha', '14:14-20', 'La siega y la vendimia'),
 ('copas0', '15:1-8', 'El cántico de Moisés y las siete copas'), ('copas15', '16:1-11', 'Las primeras cinco copas'), ('copas67', '16:12-21', 'Las copas sexta y séptima: Armagedón'),
 ('ramera', '17:1-6', 'La gran ramera'), ('ramera2', '17:7-18', 'El misterio de la bestia y la ramera'),
 ('babilonia1', '18:1-8', 'La caída de Babilonia'), ('babilonia2', '18:9-24', 'El lamento por Babilonia'),
 ('aleluya', '19:1-10', 'Aleluya: las bodas del Cordero'), ('jinete', '19:11-21', 'El Jinete del caballo blanco'),
 ('milenio', '20:1-6', 'Los mil años'), ('gog', '20:7-10', 'La rebelión final'), ('tronoblanco', '20:11-15', 'El gran trono blanco'),
 ('nuevocielo', '21:1-8', 'Cielo nuevo y tierra nueva'), ('jerusalen', '21:9-27', 'La nueva Jerusalén'), ('rio', '22:1-5', 'El río de vida'), ('epilogo', '22:6-21', 'Epílogo: «Ven, Señor Jesús»'),
]
UNIDADES = []
for id_, r, t in U:
    a, b = rango(r); UNIDADES.append({'id': id_, 'rango': r, 'ini': a, 'fin': b, 'titulo': t})
assert UNIDADES[0]['ini'] == 1 and UNIDADES[-1]['fin'] == 404
for x, y in zip(UNIDADES, UNIDADES[1:]): assert y['ini'] == x['fin'] + 1, (x, y)
