#!/usr/bin/env python3
"""Baja de la API del Banco Mundial (gratuita, sin clave) series por sexo para los gráficos de la app → web/series.json.
Países/regiones: Argentina (ARG), América Latina y el Caribe (LCN), Mundo (WLD). Uso: series_api.py"""
import json, urllib.request, datetime
V = '/home/user/trabajo/mujer'
IND = {
    'esperanza_vida_varones': ('SP.DYN.LE00.MA.IN', 'Esperanza de vida al nacer, varones (años)'),
    'esperanza_vida_mujeres': ('SP.DYN.LE00.FE.IN', 'Esperanza de vida al nacer, mujeres (años)'),
    'suicidio_varones': ('SH.STA.SUIC.MA.P5', 'Muertes por suicidio, varones (cada 100.000 varones)'),
    'suicidio_mujeres': ('SH.STA.SUIC.FE.P5', 'Muertes por suicidio, mujeres (cada 100.000 mujeres)'),
    'secundaria_varones': ('SE.SEC.ENRR.MA', 'Matrícula bruta en secundaria, varones (%)'),
    'secundaria_mujeres': ('SE.SEC.ENRR.FE', 'Matrícula bruta en secundaria, mujeres (%)'),
    'terciaria_varones': ('SE.TER.ENRR.MA', 'Matrícula bruta en educación superior, varones (%)'),
    'terciaria_mujeres': ('SE.TER.ENRR.FE', 'Matrícula bruta en educación superior, mujeres (%)'),
    'trabajo_varones': ('SL.TLF.CACT.MA.ZS', 'Participación en la fuerza laboral, varones de 15 años o más (%)'),
    'trabajo_mujeres': ('SL.TLF.CACT.FE.ZS', 'Participación en la fuerza laboral, mujeres de 15 años o más (%)'),
    'desempleo_varones': ('SL.UEM.TOTL.MA.ZS', 'Desempleo, varones (% de la fuerza laboral masculina)'),
    'desempleo_mujeres': ('SL.UEM.TOTL.FE.ZS', 'Desempleo, mujeres (% de la fuerza laboral femenina)'),
}
PAISES = {'ARG': 'Argentina', 'LCN': 'América Latina y el Caribe', 'WLD': 'Mundo'}
out = {'fuente': 'Banco Mundial, API de indicadores (data.worldbank.org)', 'consultado': datetime.date.today().isoformat(), 'series': {}}
for k, (cod, nombre) in IND.items():
    out['series'][k] = {'indicador': cod, 'nombre': nombre, 'paises': {}}
    for iso in PAISES:
        u = f'https://api.worldbank.org/v2/country/{iso}/indicator/{cod}?format=json&per_page=80&date=1990:2025'
        try:
            d = json.load(urllib.request.urlopen(u, timeout=30))[1] or []
        except Exception:
            d = []
        pts = sorted((int(r['date']), round(r['value'], 2)) for r in d if r.get('value') is not None)
        if pts:
            out['series'][k]['paises'][iso] = pts
json.dump(out, open(f'{V}/web/series.json', 'w'), ensure_ascii=False)
print({k: {i: (len(p), p[-1]) for i, p in v['paises'].items()} for k, v in out['series'].items()})
