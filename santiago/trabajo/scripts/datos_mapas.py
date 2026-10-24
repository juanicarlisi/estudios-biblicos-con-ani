#!/usr/bin/env python3
"""Arma los datos de los mapas del estudio de Santiago: geometría base (Natural Earth, dominio público; la misma de Génesis, guardada en
mapas/base_marcos.json), lugares con sus coordenadas y las vistas (qué lugares muestra cada mapa y con qué fuentes).

Los lugares y las vistas salen de mapas/lugares_santiago.json (editado a mano con lo que dicen las notas); este script solo proyecta las
coordenadas (longitud, latitud) a los dos marcos de la base y escribe mapas/datos_mapas.json, que lee la app.
Marcos: oriente = lon 24–52, lat 21–42,5 (ancho 1000); canaan = lon 33,6–37,6, lat 29,2–34,6 (ancho 760).
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

MARCOS = {'oriente': (24.0, 52.0, 21.0, 42.5, 1000), 'canaan': (33.6, 37.6, 29.2, 34.6, 760)}
DIR = os.path.join(C.REPO_TRABAJO, 'mapas')


def proyectar(marco, lon, lat):
    lon0, lon1, lat0, lat1, W = MARCOS[marco]
    k = math.cos(math.radians((lat0 + lat1) / 2))
    H = W * (lat1 - lat0) / ((lon1 - lon0) * k)
    x, y = (lon - lon0) / (lon1 - lon0) * W, (lat1 - lat) / (lat1 - lat0) * H
    return [round(x, 1), round(y, 1)] if 0 <= x <= W and 0 <= y <= H else None


def main():
    base = json.load(open(os.path.join(DIR, 'base_marcos.json')))
    datos = json.load(open(os.path.join(DIR, 'lugares_santiago.json')))
    lugares = []
    for l in datos['lugares']:
        o = {k: v for k, v in l.items() if k not in ('lon', 'lat')}
        for m in MARCOS:
            p = proyectar(m, l['lon'], l['lat'])
            if p:
                o[m] = p
        lugares.append(o)
    marcos = {m: {k: v for k, v in base['marcos'][m].items() if k != 'bbox'} for m in MARCOS}
    salida = {'marcos': marcos, 'lugares': lugares, 'vistas': datos['vistas'],
              'credito': base['credito_base'] + ' ' + datos.get('credito', '')}
    json.dump(salida, open(os.path.join(DIR, 'datos_mapas.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    print('lugares', len(lugares), '| vistas', [v['id'] for v in datos['vistas']], '| fuera de marco:', [l['id'] for l in lugares if 'oriente' not in l and 'canaan' not in l])


if __name__ == '__main__':
    main()
