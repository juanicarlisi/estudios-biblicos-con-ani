#!/usr/bin/env python3
"""Pasa los resultados de la investigación web (workflow varon-investigar-web) a varon/web/datos.json con ids W.

Datos estadísticos → W0001…; artículos de sitios cristianos → W5001…  (orden estable: tema, luego posición).
Solo entran los datos que el agente verificó en la página de la fuente (verificado_en_fuente = true).
Uso: web_datos.py [run_id]
"""
import json, glob, os, re, sys

V = '/home/user/trabajo/varon'
RUN = sys.argv[1] if len(sys.argv) > 1 else 'wf_0bd39a80-248'
ORDEN = ['salud_mental', 'mortalidad', 'adicciones', 'pornografia', 'familia', 'educacion_trabajo', 'soledad', 'fe_iglesia',
         'violencia_delito', 'masculinidad_cultura', 'articulos_identidad', 'articulos_roles']


def corta(fuente):
    """Etiqueta breve de la fuente: lo que va antes del primer paréntesis, guion o coma."""
    e = re.split(r'\s+[-–—]\s+|\(|,|;|:', fuente or '')[0].strip()
    return (e[:38] + '…') if len(e) > 40 else (e or 'Web')


def main():
    j = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{RUN}/journal.jsonl', recursive=True)[0]
    lab, res = {}, {}
    for l in open(j):
        e = json.loads(l)
        if e.get('type') == 'started':
            lab[e['agentId']] = e.get('label', '')
        elif e.get('type') == 'result' and lab.get(e.get('agentId'), '').startswith('web:'):
            v = e['result']; v = json.loads(v) if isinstance(v, str) else v
            res[lab[e['agentId']][4:]] = v
    faltan = [t for t in ORDEN if t not in res]
    out, nd, na, descartados = {}, 0, 0, 0
    for t in ORDEN:
        r = res.get(t)
        if not r:
            continue
        for d in r.get('datos', []):
            if not d.get('verificado_en_fuente'):
                descartados += 1
                continue
            nd += 1
            out[f'W{nd:04d}'] = {
                'clase': 'dato', 'tema': t, 'subtema': d.get('tema', ''), 'etiqueta': corta(d.get('fuente')), 'fuente': d.get('fuente', ''),
                'detalle': f"{d.get('indicador', '')} ({d.get('ambito', '')}, {d.get('anio', '')})", 'url': d.get('url', ''),
                'indicador': d.get('indicador', ''), 'valor': d.get('valor', ''), 'ambito': d.get('ambito', ''), 'anio': d.get('anio', ''),
                'cita_textual': d.get('cita_textual', ''), 'tipo_fuente': d.get('tipo_fuente', ''), 'notas': d.get('notas', ''),
            }
        for a in r.get('articulos', []):
            na += 1
            out[f'W{5000 + na:04d}'] = {
                'clase': 'articulo', 'tema': t, 'etiqueta': corta(a.get('sitio')), 'fuente': f"{a.get('autor', '')}, «{a.get('titulo', '')}», {a.get('sitio', '')}",
                'detalle': a.get('fecha', ''), 'url': a.get('url', ''), 'titulo': a.get('titulo', ''), 'autor': a.get('autor', ''),
                'sitio': a.get('sitio', ''), 'ideas_clave': a.get('ideas_clave', []), 'cita': a.get('cita', ''), 'refs': a.get('refs_biblicas', []),
            }
    os.makedirs(f'{V}/web', exist_ok=True)
    json.dump(out, open(f'{V}/web/datos.json', 'w'), ensure_ascii=False, indent=1)
    pend = {t: res[t].get('pendientes', '') for t in res}
    json.dump(pend, open(f'{V}/web/pendientes.json', 'w'), ensure_ascii=False, indent=1)
    print(f'datos verificados: {nd} (descartados sin verificar: {descartados}) | artículos: {na} | temas sin resultado: {faltan}')


if __name__ == '__main__':
    main()
