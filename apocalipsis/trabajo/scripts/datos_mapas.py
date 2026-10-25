#!/usr/bin/env python3
"""Datos de los mapas de Apocalipsis: geometría base en tres marcos (Asia Menor, Mediterráneo oriental, Tierra Santa), lugares y recorridos.

Geometría: Natural Earth (dominio público). Coordenadas: OpenBible.info, Bible Geocoding Data (CC BY 4.0).
Descarga previa (en SCRATCH/geo): ne_10m_land, ne_10m_lakes, ne_10m_rivers_lake_centerlines (geojson de nvkelso/natural-earth-vector).
"""
import json, math, os, sys
from shapely.geometry import shape, box
from shapely.ops import unary_union
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
G = S + '/geo/'
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mapas', 'datos_mapas.json')
MARCOS = {  # lon0, lon1, lat0, lat1, ancho, simplificación
    'asia': (25.0, 31.5, 36.5, 40.2, 1000, 0.004),
    'mediterraneo': (8.0, 40.0, 30.0, 45.0, 1000, 0.03),
    'santa': (34.0, 36.4, 31.0, 33.4, 760, 0.003),
}
def proyectar(m):
    lon0, lon1, lat0, lat1, W, _ = MARCOS[m]
    k = math.cos(math.radians((lat0 + lat1) / 2)); H = W * (lat1 - lat0) / ((lon1 - lon0) * k)
    return (lambda lon, lat: ((lon - lon0) / (lon1 - lon0) * W, (lat1 - lat) / (lat1 - lat0) * H)), W, H
def a_path(geom, P, simp, cerrar=True):
    if geom.is_empty: return ''
    geom = geom.simplify(simp, preserve_topology=True); out = []
    def anillo(cs, c):
        pts = [P(x, y) for x, y in cs]
        return '' if len(pts) < 2 else 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ('Z' if c else '')
    def rec(g):
        t = g.geom_type
        if t == 'Polygon': out.append(anillo(g.exterior.coords, True)); out.extend(anillo(i.coords, True) for i in g.interiors)
        elif t == 'LineString': out.append(anillo(g.coords, False))
        elif hasattr(g, 'geoms'):
            for h in g.geoms: rec(h)
    rec(geom); return ''.join(out)
def feats(n): return [(shape(f['geometry']), f['properties']) for f in json.load(open(G + n + '.geojson'))['features']]
RIOS = {'Jordan': 'Jordán', 'Euphrates': 'Éufrates', 'Firat': 'Éufrates', 'Tigris': 'Tigris', 'Nile': 'Nilo', 'Büyük Menderes': 'Meandro', 'Gediz': 'Hermo', 'Küçük Menderes': 'Caístro'}
def base(m):
    lon0, lon1, lat0, lat1, W, simp = MARCOS[m]; P, W, H = proyectar(m); clip = box(lon0, lat0, lon1, lat1)
    tierra = unary_union([g.intersection(clip) for g, _ in feats('ne_10m_land') if g.intersects(clip)])
    lagos = [g.intersection(clip) for g, r in feats('ne_10m_lakes') if g.intersects(clip) and (r.get('name') or '') in ('Sea of Galilee', 'Dead Sea')]
    rios = {}
    for g, r in feats('ne_10m_rivers_lake_centerlines'):
        nm = r.get('name') or ''
        if g.intersects(clip) and nm in RIOS: rios.setdefault(RIOS[nm], []).append(g.intersection(clip))
    return {'W': W, 'H': round(H, 1), 'bbox': [lon0, lon1, lat0, lat1], 'tierra': a_path(tierra, P, simp),
            'lagos': a_path(unary_union(lagos), P, simp / 4) if lagos else '',
            'rios': {k: a_path(unary_union(v), P, simp / 2, False) for k, v in rios.items()}}
# (id, nombre, lon, lat, tipo, certeza, nota)
L = [
 ('patmos', 'Patmos', 26.5417, 37.3250, 'isla', 'alta', 'Isla donde estaba Juan «por causa de la palabra de Dios y del testimonio de Jesucristo» (1:9).'),
 ('efeso', 'Éfeso', 27.3407, 37.9391, 'ciudad', 'alta', 'Primera carta (2:1-7). Puerto y capital de la provincia de Asia.'),
 ('esmirna', 'Esmirna', 27.1378, 38.4189, 'ciudad', 'alta', 'Segunda carta (2:8-11).'),
 ('pergamo', 'Pérgamo', 27.1842, 39.1322, 'ciudad', 'alta', 'Tercera carta (2:12-17).'),
 ('tiatira', 'Tiatira', 27.8366, 38.9202, 'ciudad', 'alta', 'Cuarta carta (2:18-29).'),
 ('sardis', 'Sardis', 28.0403, 38.4883, 'ciudad', 'alta', 'Quinta carta (3:1-6).'),
 ('filadelfia', 'Filadelfia', 28.5167, 38.3500, 'ciudad', 'alta', 'Sexta carta (3:7-13).'),
 ('laodicea', 'Laodicea', 29.1075, 37.8358, 'ciudad', 'alta', 'Séptima carta (3:14-22).'),
 ('hierapolis', 'Hierápolis', 29.1274, 37.9266, 'ciudad', 'alta', 'Vecina de Laodicea y Colosas (Col 4:13); no recibe carta.'),
 ('colosas', 'Colosas', 29.2599, 37.7866, 'ciudad', 'alta', 'Vecina de Laodicea (Col 4:13-16); no recibe carta.'),
 ('troas', 'Troas', 26.1586, 39.7519, 'ciudad', 'alta', 'Puerto del norte, fuera de las siete.'),
 ('mileto', 'Mileto', 27.2756, 37.5311, 'ciudad', 'alta', 'Puerto al sur de Éfeso.'),
 ('roma', 'Roma', 12.4852, 41.8922, 'ciudad', 'alta', 'Las fuentes que ven en la ciudad de las siete colinas (17:9) a Roma la identifican con la ramera; otras lecturas difieren.'),
 ('jerusalen', 'Jerusalén', 35.2342, 31.7767, 'ciudad', 'alta', 'La ciudad santa; la nueva Jerusalén baja del cielo (21:2).'),
 ('meguido', 'Meguido (Har-Magedón)', 35.1844, 32.5853, 'ciudad', 'media', '«Armagedón» (16:16) viene del hebreo har-Megiddó, «monte de Meguido».'),
 ('egipto', 'Egipto', 31.3075, 30.1294, 'region', 'region', '«Sodoma y Egipto» (11:8), nombres simbólicos de la ciudad donde su Señor fue crucificado.'),
 ('babilonia', 'Babilonia (Mesopotamia)', 44.42, 32.54, 'ciudad', 'media', 'Babilonia la grande (14:8; 16:19; 17–18). Las fuentes discuten si es Roma, una Babilonia reconstruida o un símbolo.'),
 ('eufrates', 'Éufrates', 40.0, 36.5, 'region', 'region', 'Frontera oriental del imperio; el sexto ángel derrama su copa sobre el río (16:12).'),
]
RECORRIDOS = {
 'cartas': {'nombre': 'Las siete cartas, en el orden de entrega', 'pasos': [('efeso', '2:1'), ('esmirna', '2:8'), ('pergamo', '2:12'), ('tiatira', '2:18'), ('sardis', '3:1'), ('filadelfia', '3:7'), ('laodicea', '3:14')]},
}
def main():
    out = {'marcos': {m: base(m) for m in MARCOS}, 'lugares': [], 'recorridos': {},
           'credito': 'Costas, ríos y lagos: Natural Earth (dominio público). Ubicaciones: OpenBible.info, Bible Geocoding Data (CC BY 4.0); las regiones y los lugares discutidos van en posición aproximada.'}
    proy = {m: proyectar(m)[0] for m in MARCOS}
    for (i, n, lon, lat, t, c, nota) in L:
        d = {'id': i, 'nombre': n, 'tipo': t, 'certeza': c, 'nota': nota}
        for m, P in proy.items():
            lon0, lon1, lat0, lat1 = MARCOS[m][:4]
            if lon0 <= lon <= lon1 and lat0 <= lat <= lat1: x, y = P(lon, lat); d[m] = [round(x, 1), round(y, 1)]
        out['lugares'].append(d)
    out['recorridos'] = {k: {'nombre': v['nombre'], 'pasos': [{'lugar': a, 'ref': b} for a, b in v['pasos']]} for k, v in RECORRIDOS.items()}
    json.dump(out, open(SALIDA, 'w'), ensure_ascii=False)
    for m, b in out['marcos'].items(): print(m, 'W', b['W'], 'H', b['H'], 'tierra', len(b['tierra']), 'ríos', {k: len(v) for k, v in b['rios'].items()})
if __name__ == '__main__': main()
