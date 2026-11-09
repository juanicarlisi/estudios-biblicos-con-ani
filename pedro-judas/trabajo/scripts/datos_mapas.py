#!/usr/bin/env python3
"""Datos de los mapas de 1 Pedro, 2 Pedro, 1, 2 y 3 Juan y Judas: geometría base en tres marcos (Asia Menor, Mediterráneo oriental, Tierra Santa), lugares y recorridos.

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
    'asia': (25.0, 42.0, 36.0, 42.5, 1000, 0.008),   # Ponto, Galacia, Capadocia, Asia, Bitinia (1P 1:1)
    'mediterraneo': (8.0, 40.0, 30.0, 45.0, 1000, 0.03),
    'oriente': (28.0, 50.0, 28.0, 38.0, 1000, 0.02),  # Egipto/Sinaí, Sodoma y Babilonia de Mesopotamia
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
RIOS = {'Jordan': 'Jordán', 'Euphrates': 'Éufrates', 'Firat': 'Éufrates', 'Tigris': 'Tigris', 'Nile': 'Nilo', 'Büyük Menderes': 'Meandro', 'Kızılırmak': 'Halis'}
def base(m):
    lon0, lon1, lat0, lat1, W, simp = MARCOS[m]; P, W, H = proyectar(m); clip = box(lon0, lat0, lon1, lat1)
    tierra = unary_union([g.intersection(clip) for g, _ in feats('ne_10m_land') if g.intersects(clip)])
    lagos = [g.intersection(clip) for g, r in feats('ne_10m_lakes') if g.intersects(clip) and (r.get('name') or '') in ('Dead Sea',)]
    rios = {}
    for g, r in feats('ne_10m_rivers_lake_centerlines'):
        nm = r.get('name') or ''
        if g.intersects(clip) and nm in RIOS: rios.setdefault(RIOS[nm], []).append(g.intersection(clip))
    return {'W': W, 'H': round(H, 1), 'bbox': [lon0, lon1, lat0, lat1], 'tierra': a_path(tierra, P, simp),
            'lagos': a_path(unary_union(lagos), P, simp / 4) if lagos else '',
            'rios': {k: a_path(unary_union(v), P, simp / 2, False) for k, v in rios.items()}}
# (id, nombre, lon, lat, tipo, certeza, nota)
# Provincias de 1P 1:1: puntos aproximados en el centro de cada región (certeza 'region'); las ciudades y regiones discutidas van aparte.
L = [
 ('ponto', 'Ponto', 38.0, 40.9, 'region', 'region', 'Primera provincia nombrada en 1P 1:1; costa sur del mar Negro. Posición aproximada.'),
 ('galacia', 'Galacia', 32.5, 39.5, 'region', 'region', 'Provincia de 1P 1:1; centro de Anatolia. Posición aproximada.'),
 ('capadocia', 'Capadocia', 35.0, 38.5, 'region', 'region', 'Provincia de 1P 1:1; centro-este de Anatolia. Posición aproximada.'),
 ('asia', 'Asia (provincia romana)', 28.5, 38.5, 'region', 'region', 'Provincia de 1P 1:1; el oeste de Anatolia, con Éfeso como capital. Posición aproximada.'),
 ('bitinia', 'Bitinia', 30.5, 40.6, 'region', 'region', 'Última provincia nombrada en 1P 1:1; noroeste de Anatolia. Posición aproximada.'),
 ('babilonia', 'Babilonia (Mesopotamia)', 44.42, 32.54, 'ciudad', 'media', 'Desde donde escribe Pedro (1P 5:13: «la que está en Babilonia»). Las fuentes discuten si es la Babilonia del Éufrates, Roma o un nombre simbólico.'),
 ('roma', 'Roma', 12.4852, 41.8922, 'ciudad', 'alta', 'Muchas fuentes ven en la «Babilonia» de 1P 5:13 a Roma; otras defienden la Babilonia mesopotámica o Babilonia de Egipto.'),
 ('efeso', 'Éfeso', 27.3407, 37.9391, 'ciudad', 'alta', 'Capital de la provincia de Asia; tradicionalmente ligada a Juan y a sus cartas.'),
 ('patmos', 'Patmos', 26.5417, 37.3250, 'isla', 'alta', 'Isla del destierro de Juan (Ap 1:9); referencia para ubicar el entorno de Éfeso.'),
 ('sodoma', 'Sodoma y Gomorra (región del mar Muerto)', 35.45, 31.15, 'region', 'region', 'Ciudades reducidas a ceniza como ejemplo (2P 2:6; Jd 7). Ubicación discutida (sur o norte del mar Muerto); posición aproximada.'),
 ('egipto', 'Egipto', 31.3075, 30.1294, 'region', 'region', 'De donde el Señor salvó al pueblo y luego destruyó a los incrédulos (Jd 5).'),
 ('desierto', 'Desierto del Sinaí', 33.9, 28.9, 'region', 'region', 'Región del desierto por donde anduvo el pueblo tras salir de Egipto (Jd 5). Posición aproximada.'),
]
RECORRIDOS = {
 'provincias': {'nombre': 'Las cinco provincias de 1P 1:1, en el orden en que las nombra Pedro', 'pasos': [('ponto', '1P 1:1'), ('galacia', '1P 1:1'), ('capadocia', '1P 1:1'), ('asia', '1P 1:1'), ('bitinia', '1P 1:1')]},
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
