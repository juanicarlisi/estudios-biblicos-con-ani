#!/usr/bin/env python3
"""Arma los datos de los mapas: geometría base en dos marcos (Cercano Oriente y Canaán), lugares y recorridos.

Geometría: Natural Earth (dominio público). Coordenadas: OpenBible.info Bible Geocoding Data (CC BY 4.0),
con el puntaje de confianza que da esa fuente; las regiones van en posiciones aproximadas y así se indica.
Los recorridos siguen el orden de lugares que da el texto de Génesis.
"""
import json, math
import shapefile
from shapely.geometry import shape, box
from shapely.ops import unary_union

G = '/home/user/trabajo/geo/'
MARCOS = {
    'oriente': (24.0, 52.0, 21.0, 42.5, 1000, 0.025),
    'canaan': (33.6, 37.6, 29.2, 34.6, 760, 0.004),
}
LAGOS_ANTIGUOS = {'Sea of Galilee', 'Dead Sea', 'Lake Van', 'Lake Urmia', 'Lake Tuz', 'Great Bitter Lake', 'Lake Sevan'}
RIOS = {'Nile': 'Nilo', 'Rosetta Branch': '', 'Damietta Branch': '', 'Tigris': 'Tigris', 'Dicle': 'Tigris',
        'Euphrates': 'Éufrates', 'Firat': 'Éufrates', 'Al Furat': 'Éufrates', 'Murat': '', 'Jordan': 'Jordán',
        'Shatt al-Arab': '', 'Karkheh': '', 'Ceyhan': '', 'Kızılırmak': ''}


def proyectar(marco):
    lon0, lon1, lat0, lat1, W, _ = MARCOS[marco]
    k = math.cos(math.radians((lat0 + lat1) / 2))
    H = W * (lat1 - lat0) / ((lon1 - lon0) * k)
    return (lambda lon, lat: ((lon - lon0) / (lon1 - lon0) * W, (lat1 - lat) / (lat1 - lat0) * H)), W, H


def a_path(geom, P, simp, cerrar=True):
    geom = geom.simplify(simp, preserve_topology=True)
    out = []
    def anillo(cs, c):
        pts = [P(x, y) for x, y in cs]
        if len(pts) < 2:
            return ''
        return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ('Z' if c else '')
    def rec(g):
        t = g.geom_type
        if t == 'Polygon':
            out.append(anillo(g.exterior.coords, True)); out.extend(anillo(i.coords, True) for i in g.interiors)
        elif t == 'LineString':
            out.append(anillo(g.coords, False))
        elif hasattr(g, 'geoms'):
            for h in g.geoms:
                rec(h)
    rec(geom)
    return ''.join(out)


def leer(nombre):
    r = shapefile.Reader(G + nombre + '/' + nombre + '.shp')
    campos = [f[0] for f in r.fields[1:]]
    for sr in r.shapeRecords():
        yield shape(sr.shape.__geo_interface__), dict(zip(campos, sr.record))


def base(marco):
    lon0, lon1, lat0, lat1, W, simp = MARCOS[marco]
    P, W, H = proyectar(marco)
    clip = box(lon0, lat0, lon1, lat1)
    tierra = unary_union([g.intersection(clip) for g, _ in leer('ne_10m_land') if g.intersects(clip)])
    lagos = [g.intersection(clip) for g, r in leer('ne_10m_lakes') if g.intersects(clip) and (r.get('name') or '') in LAGOS_ANTIGUOS]
    rios = {}
    for g, r in leer('ne_10m_rivers_lake_centerlines'):
        nm = r.get('name') or ''
        if nm in RIOS and g.intersects(clip):
            rios.setdefault(RIOS[nm] or nm, []).append(g.intersection(clip))
    return {'W': W, 'H': round(H, 1), 'bbox': [lon0, lon1, lat0, lat1],
            'tierra': a_path(tierra, P, simp),
            'lagos': a_path(unary_union(lagos), P, simp / 4) if lagos else '',
            'rios': {k: a_path(unary_union(v), P, simp / 2, False) for k, v in rios.items()}}


# Lugares: (id, nombre, lon, lat, tipo, certeza, nota). certeza: alta / media / baja / region
L = [
    ('ur_sur', 'Ur de los caldeos (sur)', 46.103, 30.962, 'ciudad', 'media', 'Ubicación tradicional, en la baja Mesopotamia (Tell el-Muqayyar). La defiende Edersheim.'),
    ('ur_norte', 'Ur (alternativa del norte)', 38.784, 37.148, 'ciudad', 'baja', 'Kline considera cuestionable el Ur del sur y menciona una ubicación más al norte, en la ruta a Harán.'),
    ('haran', 'Harán', 39.033, 36.864, 'ciudad', 'alta', 'Padan-aram: la región de Harán.'),
    ('siquem', 'Siquem (encina de More)', 35.282, 32.214, 'ciudad', 'alta', ''),
    ('betel', 'Betel (Luz)', 35.241, 31.923, 'ciudad', 'alta', ''),
    ('hai', 'Hai', 35.261, 31.917, 'ciudad', 'media', ''),
    ('hebron', 'Hebrón (Mamre, Macpela)', 35.102, 31.525, 'ciudad', 'alta', ''),
    ('beerseba', 'Beerseba', 34.793, 31.237, 'ciudad', 'alta', ''),
    ('gerar', 'Gerar', 34.607, 31.382, 'ciudad', 'media', ''),
    ('cades', 'Cades', 34.422, 30.648, 'ciudad', 'media', ''),
    ('shur', 'Desierto de Shur', 32.957, 30.493, 'region', 'region', ''),
    ('lahairoi', 'Beer-lahai-roi', 34.333, 30.688, 'pozo', 'baja', 'El pozo del Viviente que me ve (16:14).'),
    ('sodoma', 'Sodoma', 35.523, 31.249, 'ciudad', 'baja', 'Ubicación discutida, en la zona del mar Muerto.'),
    ('zoar', 'Zoar', 35.488, 31.037, 'ciudad', 'baja', ''),
    ('salem', 'Salem (Jerusalén)', 35.235, 31.777, 'ciudad', 'media', 'Ciudad de Melquisedec (14:18).'),
    ('moriah', 'Monte Moriah', 35.236, 31.778, 'monte', 'baja', 'La tierra de Moriah (22:2); 2 Crónicas 3:1 ubica allí el templo.'),
    ('dan', 'Dan', 35.652, 33.249, 'ciudad', 'alta', ''),
    ('hoba', 'Hoba', 37.067, 34.250, 'ciudad', 'baja', 'Al norte de Damasco (14:15).'),
    ('damasco', 'Damasco', 36.306, 33.511, 'ciudad', 'alta', ''),
    ('mahanaim', 'Mahanaim', 35.687, 32.186, 'ciudad', 'media', ''),
    ('peniel', 'Peniel', 35.692, 32.187, 'lugar', 'media', 'Junto al vado de Jaboc (32:22-31).'),
    ('sucot', 'Sucot', 35.621, 32.197, 'ciudad', 'media', ''),
    ('galaad', 'Monte de Galaad (Mizpa)', 35.80, 32.33, 'region', 'region', 'El majano de Galaad (31:47-49); ubicación aproximada.'),
    ('belen', 'Efrata (Belén)', 35.208, 31.704, 'ciudad', 'alta', 'Donde murió Raquel (35:19).'),
    ('edar', 'Migdal-edar', 35.230, 31.707, 'lugar', 'baja', ''),
    ('dotan', 'Dotán', 35.240, 32.414, 'ciudad', 'alta', ''),
    ('adulam', 'Adulam', 35.002, 31.652, 'ciudad', 'alta', ''),
    ('timnat', 'Timnat', 35.049, 31.694, 'ciudad', 'baja', ''),
    ('on', 'On (Heliópolis)', 31.308, 30.129, 'ciudad', 'alta', 'Ciudad de Potifera, suegro de José (41:45).'),
    ('gosen', 'Gosén', 31.75, 30.80, 'region', 'region', 'Región del delta oriental del Nilo; ubicación aproximada.'),
    ('egipto', 'Egipto', 31.0, 27.6, 'region', 'region', ''),
    ('ararat', 'Montes de Ararat', 44.300, 39.703, 'monte', 'region', 'El arca reposó «sobre los montes de Ararat» (8:4): una región, no un pico identificado.'),
    ('babel', 'Babel (Babilonia), en Sinar', 44.421, 32.536, 'ciudad', 'media', ''),
    ('ninive', 'Nínive', 43.153, 36.359, 'ciudad', 'alta', ''),
    ('cala', 'Cala', 43.329, 36.098, 'ciudad', 'alta', ''),
    ('erec', 'Erec', 45.636, 31.322, 'ciudad', 'alta', ''),
    ('acad', 'Acad', 44.392, 33.026, 'ciudad', 'baja', ''),
    ('eden', 'Edén (región aproximada)', 45.0, 32.6, 'region', 'region', 'Las fuentes lo ubican en la región del Tigris y el Éufrates, sin precisar el lugar.'),
    ('canaan', 'Canaán', 35.1, 31.95, 'region', 'region', ''),
    ('edom', 'Edom (Seir)', 35.45, 30.45, 'region', 'region', ''),
    ('sidon', 'Sidón', 35.372, 33.561, 'ciudad', 'alta', ''),
    ('gaza', 'Gaza', 34.464, 31.504, 'ciudad', 'alta', ''),
    ('aram', 'Aram (Mesopotamia)', 39.6, 36.0, 'region', 'region', ''),
    ('elam', 'Elam', 48.5, 32.2, 'region', 'region', ''),
    ('asiria', 'Asiria', 43.4, 36.9, 'region', 'region', ''),
]
RECORRIDOS = {
    'abraham': {'nombre': 'Abraham', 'pasos': [
        ('ur_sur', '11:31'), ('haran', '11:31-12:4'), ('siquem', '12:6'), ('betel', '12:8'), ('egipto', '12:10'),
        ('betel', '13:3'), ('hebron', '13:18'), ('gerar', '20:1'), ('beerseba', '21:31-33'), ('moriah', '22:2'),
        ('beerseba', '22:19'), ('hebron', '23:2')]},
    'lot': {'nombre': 'Lot', 'pasos': [('betel', '13:3'), ('sodoma', '13:12'), ('zoar', '19:22-23')]},
    'campana': {'nombre': 'La persecución de los reyes (Gn 14)', 'pasos': [('hebron', '14:13'), ('dan', '14:14'), ('hoba', '14:15'), ('salem', '14:18')]},
    'agar': {'nombre': 'Agar', 'pasos': [('hebron', '16:1'), ('lahairoi', '16:7-14')]},
    'jacob': {'nombre': 'Jacob', 'pasos': [
        ('beerseba', '28:10'), ('betel', '28:19'), ('haran', '29:4'), ('galaad', '31:21-25'), ('mahanaim', '32:2'),
        ('peniel', '32:30'), ('sucot', '33:17'), ('siquem', '33:18'), ('betel', '35:6'), ('belen', '35:19'),
        ('edar', '35:21'), ('hebron', '35:27'), ('beerseba', '46:1'), ('gosen', '46:28')]},
    'jose': {'nombre': 'José', 'pasos': [('hebron', '37:14'), ('siquem', '37:14'), ('dotan', '37:17'), ('egipto', '37:28-36')]},
}


def main():
    out = {'marcos': {}, 'lugares': [], 'recorridos': {}, 'credito': 'Costas, ríos y lagos: Natural Earth (dominio público). Ubicaciones: OpenBible.info, Bible Geocoding Data (CC BY 4.0); las regiones van en posición aproximada.'}
    for m in MARCOS:
        out['marcos'][m] = base(m)
    proy = {m: proyectar(m)[0] for m in MARCOS}
    for (i, n, lon, lat, t, c, nota) in L:
        d = {'id': i, 'nombre': n, 'tipo': t, 'certeza': c, 'nota': nota}
        for m, P in proy.items():
            lon0, lon1, lat0, lat1 = MARCOS[m][:4]
            if lon0 <= lon <= lon1 and lat0 <= lat <= lat1:
                x, y = P(lon, lat); d[m] = [round(x, 1), round(y, 1)]
        out['lugares'].append(d)
    out['recorridos'] = {k: {'nombre': v['nombre'], 'pasos': [{'lugar': a, 'ref': b} for a, b in v['pasos']]} for k, v in RECORRIDOS.items()}
    json.dump(out, open('/home/user/trabajo/mapas/datos_mapas.json', 'w'), ensure_ascii=False)
    for m, b in out['marcos'].items():
        print(m, 'W', b['W'], 'H', b['H'], 'tierra', len(b['tierra']), 'lagos', len(b['lagos']), 'ríos', {k: len(v) for k, v in b['rios'].items()})


if __name__ == '__main__':
    main()
