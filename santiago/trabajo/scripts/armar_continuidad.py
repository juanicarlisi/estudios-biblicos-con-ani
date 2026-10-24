#!/usr/bin/env python3
"""Arma las ventanas de revisión de continuidad: seis días seguidos por archivo (con uno de solapamiento), para que un revisor detecte
problemas ENTRE días (el «antes» y el «después» que no empalman, fechas o edades que se contradicen, explicaciones repetidas).
Salida: TMP/revision/continuidad_NN.txt. Uso: armar_continuidad.py [--ventana 6]
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

V = int(sys.argv[sys.argv.index('--ventana') + 1]) if '--ventana' in sys.argv else 6
dias = {}
for f in sorted(glob.glob(os.path.join(C.REPO_TRABAJO, 'dias', 'dia_*.json'))):
    d = json.load(open(f)); dias[d['dia']] = d
orden = sorted(dias)
os.makedirs(os.path.join(C.TMP, 'revision'), exist_ok=True)
for f in glob.glob(os.path.join(C.TMP, 'revision', 'continuidad_*.txt')):
    os.remove(f)


def texto_dia(d):
    c = d['contexto']
    out = [f"=== DÍA {d['dia']} · Santiago {d['desde']}–{d['hasta']} · {d['titulo']} ===",
           f"contexto.antes: {c['antes']}", f"contexto.ahora: {c['ahora']}", f"contexto.donde: {c['donde']}", f"contexto.cuando: {c['cuando']}", f"contexto.despues: {c['despues']}",
           f"panorama.texto: {d['panorama']['texto']}"]
    for i, s in enumerate(d['secciones']):
        for j, n in enumerate(s['notas']):
            out.append(f"secciones[{i}].notas[{j}] ({s['rango']} · {s['titulo']}): {n['texto']}")
    for i, k in enumerate(d.get('cristo', [])):
        out.append(f"cristo[{i}].texto: {k['texto']}")
    for i, k in enumerate(d.get('eco_de_jesus', [])):
        out.append(f"eco_de_jesus[{i}].texto: {k['texto']}")
    for i, k in enumerate(d.get('para_vivir', [])):
        out.append(f"para_vivir[{i}].texto: {k['texto']}")
    return '\n'.join(out)


n = 0
paso = V - 1
for ini in range(0, max(1, len(orden) - 1), paso):
    ventana = orden[ini:ini + V]
    if len(ventana) < 2:
        break
    n += 1
    open(os.path.join(C.TMP, 'revision', f'continuidad_{n:02d}.txt'), 'w').write('\n\n'.join(texto_dia(dias[k]) for k in ventana) + '\n')
    print(f'ventana {n:02d}: días {ventana[0]}–{ventana[-1]}')
print(n, 'ventanas')
