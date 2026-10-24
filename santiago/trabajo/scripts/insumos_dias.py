#!/usr/bin/env python3
"""Arma, para cada día del plan, un archivo con todo el material que le corresponde.

Cada nota recibe un id estable «bloque#n» que quien escribe el día cita en `fuentes`.
- Las notas de la biblioteca (comentarios) van a todos los días cuyo pasaje tocan.
- Las de REFERENCIA3 (libros de referencia) van a un solo día: el de mayor superposición (así no se repite lo mismo en días seguidos);
  si hay una curaduría guardada para ese día (curaduria/dia_NN.json), solo entran las elegidas.
- Las que abarcan mucho texto (más de 14 versículos) van al panorama de su parte o a la introducción y los temas; las de «intro» y «tema», también.
- Si varios días comparten versículos (el plan los marca con «compartido» y «tipos»), cada día recibe las notas de los tipos que le tocan.
Salida: TMP/insumos/dia_NN.txt, panorama_parte_X.txt, libro_intro_y_temas.txt y el resumen de tamaños.
"""
import collections, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C
import notas as N

DST = os.path.join(C.TMP, 'insumos')
TRAMO_DIA = 14


def rvr():
    d = json.load(open(os.path.join(C.REPO_TRABAJO, 'biblia', 'rvr1960_santiago.json')))['texto']
    return {f'{c}:{v}': t for c, vs in d.items() for v, t in vs.items()}


def main():
    plan = json.load(open(os.path.join(C.REPO_TRABAJO, 'plan', 'plan.json')))
    texto = rvr()
    notas = N.cargar()
    curadas = {}
    cdir = os.path.join(C.REPO_TRABAJO, 'curaduria')
    if os.path.isdir(cdir):
        for f in os.listdir(cdir):
            if f.startswith('dia_') and f.endswith('.json'):
                dd = json.load(open(os.path.join(cdir, f))); curadas[dd['dia']] = set(dd['ids'])
    for p in plan:
        p['a'] = C.idx(*map(int, p['desde'].split(':'))); p['b'] = C.idx(*map(int, p['hasta'].split(':')))
    partes_rango = {}
    for p in plan:
        x = partes_rango.get(p['parte'], (p['a'], p['b'])); partes_rango[p['parte']] = (min(x[0], p['a']), max(x[1], p['b']))
    por_dia = collections.defaultdict(list); panorama = collections.defaultdict(list); libro = []; sobrantes = collections.defaultdict(list)
    for n in notas:
        r = N.rango(n.get('ref', ''))
        if not r:
            libro.append(n); continue
        a, b = r
        tocados = [p for p in plan if not (b < p['a'] or a > p['b'])]
        if b - a + 1 <= TRAMO_DIA and tocados:
            if n['origen'] == 'ref3':
                mejor = max(tocados, key=lambda p: (min(b, p['b']) - max(a, p['a']), -p['dia']))
                grupo = [p for p in tocados if (p['desde'], p['hasta']) == (mejor['desde'], mejor['hasta'])] if mejor.get('compartido') else [mejor]
                destino = elegir_dia_compartido(n, grupo or [mejor])
                sel = curadas.get(destino['dia'])
                if sel is None or n['id'] in sel:
                    por_dia[destino['dia']].append(n)
                else:
                    sobrantes[destino['dia']].append(n['id'])
            else:
                vistos = set()
                for p in tocados:
                    clave = (p['desde'], p['hasta'])
                    if p.get('compartido'):
                        grupo = [q for q in plan if (q['desde'], q['hasta']) == clave]
                        destino = elegir_dia_compartido(n, grupo)
                        if destino['dia'] in vistos:
                            continue
                        vistos.add(destino['dia']); por_dia[destino['dia']].append(n)
                    else:
                        por_dia[p['dia']].append(n)
        else:
            ps = sorted({p['parte'] for p in tocados})
            if len(ps) == 1:
                panorama[ps[0]].append(n)
            else:
                libro.append(n)
    os.makedirs(DST, exist_ok=True)
    stats = []
    for i, p in enumerate(plan):
        ant = plan[i - 1] if i else None; sig = plan[i + 1] if i + 1 < len(plan) else None
        pas = []
        for k in range(p['a'], p['b'] + 1):
            c, v = C.de_idx(k); pas.append(f'{c}:{v} {texto[f"{c}:{v}"]}')
        ns = sorted(por_dia[p['dia']], key=lambda n: (N.rango(n['ref'])[0], n['origen'] != 'biblio', -int(n.get('importancia', 1))))
        cab = [f"DÍA {p['dia']} · Santiago {p['desde']}–{p['hasta']} · {p['titulo']} · Parte {p['parte']} · {p['b'] - p['a'] + 1} versículos"]
        if p.get('compartido'):
            cab.append(f"ESTE PASAJE SE ESTUDIA EN {p['compartido']['de']} DÍAS; este es el día {p['compartido']['n']}. Enfoque de este día: {p.get('foco', '')}. "
                       f"Tipos de nota que le tocan: {', '.join(p.get('tipos', []))}. No repitas lo que corresponde a los otros días del mismo pasaje.")
        cab += [f"Día anterior: {ant['dia']} · Stg {ant['desde']}–{ant['hasta']} · {ant['titulo']}" if ant else 'Día anterior: (es el primero)',
                f"Día siguiente: {sig['dia']} · Stg {sig['desde']}–{sig['hasta']} · {sig['titulo']}" if sig else 'Día siguiente: (es el último)',
                '', '=== TEXTO DEL PASAJE (RVR1960) ===', *pas, '', f'=== NOTAS ({len(ns)}) ===']
        cuerpo = '\n\n'.join(N.linea(n) for n in ns)
        open(os.path.join(DST, f"dia_{p['dia']:02d}.txt"), 'w').write('\n'.join(cab) + '\n' + cuerpo + '\n')
        stats.append((p['dia'], len(ns), len(cuerpo)))
    os.makedirs(os.path.join(DST, 'sobrantes'), exist_ok=True)
    for d, ids in sobrantes.items():
        json.dump(ids, open(os.path.join(DST, 'sobrantes', f'dia_{d:02d}.json'), 'w'))
    for par, ns in panorama.items():
        open(os.path.join(DST, f'panorama_parte_{par}.txt'), 'w').write('\n\n'.join(N.linea(n) for n in sorted(ns, key=lambda n: N.rango(n['ref'])[0])))
    open(os.path.join(DST, 'libro_intro_y_temas.txt'), 'w').write('\n\n'.join(N.linea(n) for n in libro))
    print('notas', len(notas), '| libro/temas', len(libro), '| panoramas', {p: len(v) for p, v in panorama.items()})
    cs = [s[2] for s in stats]
    print('por día: notas min/máx', min(s[1] for s in stats), max(s[1] for s in stats), '| caracteres min/prom/máx', min(cs), sum(cs) // len(cs), max(cs))
    for d, n, c in stats:
        print(f'  día {d:2d}: {n:4d} notas, {c:7d} caracteres')


def elegir_dia_compartido(n, grupo):
    """Entre los días que comparten pasaje, el que tiene el tipo de la nota (o el primero)."""
    if len(grupo) == 1:
        return grupo[0]
    for p in grupo:
        if n.get('tipo') in p.get('tipos', []):
            return p
    return grupo[0]


if __name__ == '__main__':
    main()
