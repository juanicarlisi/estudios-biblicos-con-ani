#!/usr/bin/env python3
"""Arma, para cada día del plan, un archivo con todo el material que le corresponde.

Cada nota recibe un id estable «archivo#n» (el nombre del archivo de extracción y su posición) que la redacción cita en `fuentes`.
Reparto: cada nota con pasaje de hasta 12 versículos va a UN solo día (el de mayor solapamiento; si empata, se reparte en
ronda entre los días empatados). Las notas de más de 12 versículos, las de «intro»/«1P intro» y las de «tema»/«1J tema» no van
a los días: alimentan las introducciones, los panoramas de cada parte y los temas (insumos de artículos).
Uso: insumos_dias.py   -> SCRATCH/pj_insumos/dia_NN.txt, SCRATCH/pj_insumos/_indice.json, _intro/_tema/_amplias.txt, _dias_resumen.txt
"""
import json, os, sys, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U, pesos
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = S + '/pj_insumos'; os.makedirs(OUT, exist_ok=True)
FUENTES = json.load(open(AQUI + '/../plan/fuentes_comentarios.json'))
TOPE_DIA = 12
def etiqueta_fuente(nid):
    pref = nid.split('_')[0]
    if pref in FUENTES: return FUENTES[pref]['corto'], FUENTES[pref].get('tradicion', '')
    return 'referencia', ''
def cabecera(n):
    corto, trad = etiqueta_fuente(n['id'])
    return (f"[{n['id']}] {n['ref']} · {n['tipo']} · imp {n['importancia']} · {corto}"
            + (f" · {n['escuela']}" if n.get('escuela') else (f' · {trad}' if trad else '')) + f" · {n['pagina']}")
def main():
    plan = json.load(open(AQUI + '/../plan/plan.json'))['dias']
    rvr = json.load(open(S + '/biblia/rvr1960_pedro_judas.json'))['texto']
    gr = json.load(open(AQUI + '/../griego/pedro_judas_griego.json'))['versiculos']
    N = pesos.notas()
    por_dia = {d['dia']: [] for d in plan}; fuera = {'intro': [], 'tema': [], 'amplias': []}
    for n in N:
        e = U.especial(n['ref'])
        if e: fuera[e[0]].append(n); continue
        r = U.rango(n['ref'])
        if not r: fuera['tema'].append(n); continue
        a, b = r
        if b - a + 1 > TOPE_DIA: fuera['amplias'].append(n); continue
        sol = [(max(0, min(b, d['fin']) - max(a, d['ini']) + 1), d['dia']) for d in plan]
        m = max(s for s, _ in sol); cand = [dia for s, dia in sol if s == m]
        dia = cand[zlib.crc32(n['id'].encode()) % len(cand)] if len(cand) > 1 else cand[0]
        por_dia[dia].append(n)
    idx = []; resumen = []
    for k, d in enumerate(plan):
        ant = plan[k - 1] if k else None; sig = plan[k + 1] if k + 1 < len(plan) else None
        libro = ' y '.join(U.NOMBRE[x] for x in d['libro'].split('+'))
        h = [f"# DÍA {d['dia']} · {libro} · {d['rango']} · {d['titulo_provisional']} · {d['parte']}"]
        h.append('Anterior: ' + (f"día {ant['dia']} ({ant['rango']}, {ant['titulo_provisional']})" if ant else 'ninguno (es el primer día de 1 Pedro a Judas; antes viene Apocalipsis solo en el orden de la app)'))
        h.append('Siguiente: ' + (f"día {sig['dia']} ({sig['rango']}, {sig['titulo_provisional']})" if sig else 'ninguno (es el último día; después sigue Apocalipsis)'))
        h.append('\n## TEXTO BÍBLICO DEL DÍA (RVR1960, solo para tu lectura; en el JSON no se transcribe: lo inserta la app por referencia)')
        for i in range(d['ini'], d['fin'] + 1):
            lib, c, v = U.desde_idx(i); h.append(f"{U.cv(i)} {rvr[lib][str(c)][str(v)]}")
        h.append('\n## GRIEGO (SBLGNT) DE LOS MISMOS VERSÍCULOS')
        for i in range(d['ini'], d['fin'] + 1):
            h.append(f"{U.cv(i)} " + ' '.join(w['t'] for w in gr[U.cv(i)]))
        notas = sorted(por_dia[d['dia']], key=lambda n: (U.rango(n['ref'])[0], -n['importancia']))
        h.append(f"\n## NOTAS EXTRAÍDAS ({len(notas)}); id · pasaje · tipo · importancia · fuente · tradición o postura del autor · página")
        for n in notas:
            cuerpo = f"{n['titulo']}: {n['contenido']}"
            if n.get('cita'): cuerpo += f" CITA: «{n['cita']}»"
            if n.get('griego'): cuerpo += f" GRIEGO: {json.dumps(n['griego'], ensure_ascii=False)}"
            if n.get('postura'): cuerpo += f" POSTURA: {n['postura']}"
            if n.get('refs_biblicas'): cuerpo += f" REFS: {', '.join(n['refs_biblicas'])}"
            h.append(cabecera(n) + f"\n{cuerpo}\n")
        txt = '\n'.join(h); fn = f"{OUT}/dia_{d['dia']:02d}.txt"; open(fn, 'w').write(txt)
        idx.append({'dia': d['dia'], 'libro': d['libro'], 'rango': d['rango'], 'notas': len(notas), 'chars': len(txt), 'archivo': fn})
        resumen.append(f"día {d['dia']} · {d['rango']} · {d['parte']} · {d['titulo_provisional']}")
    open(OUT + '/_dias_resumen.txt', 'w').write('\n'.join(resumen) + '\n')
    for nombre, lista in fuera.items():
        cuerpo = []
        for n in sorted(lista, key=lambda n: ((U.rango(n['ref']) or (0,))[0], -n['importancia'])):
            cuerpo.append(cabecera(n) + f"\n{n['titulo']}: {n['contenido']}" + (f" POSTURA: {n['postura']}" if n.get('postura') else '') + '\n')
        open(f'{OUT}/_{nombre}.txt', 'w').write('\n'.join(cuerpo)); print(nombre, len(lista), sum(len(c) for c in cuerpo))
    json.dump(idx, open(OUT + '/_indice.json', 'w'), indent=0)
    import statistics
    print('días', len(idx), 'notas en días', sum(i['notas'] for i in idx), 'media chars', int(statistics.mean(i['chars'] for i in idx)), 'máx', max(i['chars'] for i in idx))
if __name__ == '__main__': main()
