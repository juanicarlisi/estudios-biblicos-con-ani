#!/usr/bin/env python3
"""Arma el insumo de cada día (varon/insumos/dia_NNN.txt): su plan, su lugar en la parte y todas sus notas y datos.

Las «citas textuales» solo entran si verificar_citas.py las encontró en el libro.
Si un insumo pasa de TOPE caracteres, deja afuera primero las notas de importancia 1 y después acorta las de importancia 2.
Uso: insumos.py [dia ...]   (por defecto, todos)
"""
import json, os, re, sys

V = '/home/user/trabajo/varon'
TOPE = 160000
sys.path.insert(0, f'{V}/scripts')
from grupos_entrada import notas  # noqa: E402


def main():
    plan = json.load(open(f'{V}/plan/plan.json'))
    partes = {p['id']: p for p in json.load(open(f'{V}/plan/partes.json'))}
    det = {int(k): v for k, v in json.load(open(f'{V}/plan/dias_plan.json')).items()}
    grupos = json.load(open(f'{V}/plan/grupos/_grupos.json'))
    web = json.load(open(f'{V}/web/datos.json'))
    fuentes = json.load(open(f'{V}/bloques/_fuentes.json'))
    todas = dict(notas())
    citas = json.load(open(f'{V}/revision/citas.json')) if os.path.exists(f'{V}/revision/citas.json') else {}
    total = len(plan)
    pedidos = [int(x) for x in sys.argv[1:]] or [p['dia'] for p in plan]
    os.makedirs(f'{V}/insumos', exist_ok=True)
    tams = []
    for d in pedidos:
        x = det[d]; pt = partes[x['parte']]
        dias_parte = [p for p in plan if p['parte'] == x['parte']]
        cab = [f"# DÍA {d} de {total} · Parte {pt['numero']}: {pt['titulo']}",
               f"Título previsto: {x['titulo']}", f"Objetivo: {x['objetivo']}", f"Qué cubre: {x['contenido']}", f"Lectura prevista: {x['lectura']}", '',
               f"## Esta parte ({pt['bajada']})"]
        for p in dias_parte:
            marca = '  ← HOY' if p['dia'] == d else ''
            extra = f" — {det[p['dia']]['objetivo']}" if abs(p['dia'] - d) == 1 else ''
            cab.append(f"- Día {p['dia']}: {p['titulo']}{extra}{marca}")
        if d > 1 and plan[d - 2]['parte'] != x['parte']:
            cab.append(f"(El día anterior, {d - 1}, cerró la parte previa: «{plan[d - 2]['titulo']}».)")

        def bloque_notas(nivel):
            out = ['', '## NOTAS (agrupadas por tema)']
            for g in x['grupos']:
                G = grupos[g]
                out += ['', f"### {G['tema']} — {G['resumen']}"]
                for i in G['ids']:
                    n = todas[i]; imp = n.get('importancia', 2)
                    if imp == 1 and nivel >= 1:
                        continue
                    src = fuentes.get(n.get('fuente'), {})
                    cont = n.get('contenido', '')
                    if imp == 2 and nivel >= 2 and len(cont) > 500:
                        cont = cont[:500].rsplit(' ', 1)[0] + '…'
                    out.append(f"[{i}] (importancia {imp} · {n.get('tipo')} · {src.get('autor', '?')}, {src.get('obra', '?')}, pág. {n.get('pagina', '')}) {n.get('titulo', '')}")
                    out.append(cont)
                    cv = citas.get(i, {})
                    if n.get('cita') and cv.get('estado') in ('ok', 'ocr'):
                        out.append(f"Cita textual: «{n['cita']}»")
                    elif n.get('cita') and cv.get('estado') == 'otra':
                        out.append(f"Cita textual (pág. {cv['pagina_real']}): «{n['cita']}»")
                    if n.get('refs'):
                        out.append('Versículos: ' + ', '.join(n['refs']))
                    if n.get('persona'):
                        out.append('Persona: ' + n['persona'])
            return out

        wl = []
        datos = [w for w in x['web'] if web[w]['clase'] == 'dato']
        arts = [w for w in x['web'] if web[w]['clase'] == 'articulo']
        if datos:
            wl += ['', '## DATOS DE LA WEB (verificados en su fuente)']
            for w in datos:
                v = web[w]
                wl.append(f"[{w}] {v['valor']} — {v['indicador']} ({v['ambito']}, {v['anio']}). Fuente: {v['fuente']}. Lo que dice la fuente: «{v['cita_textual']}»" + (f" Nota: {v['notas']}" if v.get('notas') else ''))
        if arts:
            wl += ['', '## ARTÍCULOS DE SITIOS CRISTIANOS CONFIABLES']
            for w in arts:
                v = web[w]
                wl.append(f"[{w}] «{v['titulo']}», {v['autor']}, {v['sitio']} ({v['detalle']}). Ideas clave: " + ' / '.join(v['ideas_clave'])
                          + (f" Cita textual: «{v['cita']}»" if v.get('cita') else '') + (f" Versículos: {', '.join(v['refs'])}" if v.get('refs') else ''))
        for nivel in (0, 1, 2):
            txt = '\n'.join(cab + bloque_notas(nivel) + wl) + '\n'
            if len(txt) <= TOPE:
                break
        open(f'{V}/insumos/dia_{d:03d}.txt', 'w').write(txt)
        tams.append((len(txt), d, nivel))
    tams.sort()
    print('insumos:', len(tams), '| caracteres: mín', tams[0][0], 'máx', tams[-1][0], '| recortados:', [(d, n) for _, d, n in tams if n])


if __name__ == '__main__':
    main()
