#!/usr/bin/env python3
"""Para los días cuyo cuerpo pasa de LIMITE palabras: arma archivos (grupos de N días) con cada párrafo, su largo y su comienzo,
para que un agente elija cuáles pasan a «Para profundizar» (solo devuelve índices; no reescribe nada).
Escribe varon/recortar/grupo_NN.txt y _grupos.json. Uso: recortar_entrada.py [--grupo 6]"""
import json, glob, os, sys, re
V = '/home/user/trabajo/varon'
sys.path.insert(0, f'{V}/scripts')
LIMITE, OBJETIVO = 2800, 2550


def main():
    N = int(sys.argv[sys.argv.index('--grupo') + 1]) if '--grupo' in sys.argv else 6
    os.makedirs(f'{V}/recortar', exist_ok=True)
    for f in glob.glob(f'{V}/recortar/*'):
        os.remove(f)
    dias = []
    for f in sorted(glob.glob(f'{V}/revision/verif/dia_*.json')):
        d = int(f[-8:-5]); r = json.load(open(f))
        if r.get('cuerpo', 0) > LIMITE and not os.path.exists(f'{V}/dias/dia_{d:03d}.json'):
            dias.append((d, r['cuerpo']))
    bloques = []
    for d, cuerpo in dias:
        x = json.load(open(f'{V}/dias/borradores/dia_{d:03d}.json'))
        out = [f'DÍA {d}: {x["titulo"]} · cuerpo {cuerpo} palabras · hay que sacar al menos {cuerpo - OBJETIVO} palabras']
        for a, s in enumerate(x['apartados']):
            out.append(f'APARTADO {a}: {s["titulo"]}')
            for p, q in enumerate(s['parrafos']):
                out.append(f'  [{a},{p}] {len(q["texto"].split())} palabras · {len(q.get("fuentes", []))} fuentes · {re.sub(chr(10), " ", q["texto"])[:170]}')
        bloques.append(('\n'.join(out), d))
    grupos = [bloques[i:i + N] for i in range(0, len(bloques), N)]
    for k, g in enumerate(grupos, 1):
        open(f'{V}/recortar/grupo_{k:02d}.txt', 'w').write('\n\n=====\n\n'.join(b for b, _ in g) + '\n')
    json.dump([[d for _, d in g] for g in grupos], open(f'{V}/recortar/_grupos.json', 'w'))
    print(f'{len(dias)} días a recortar en {len(grupos)} grupos')


if __name__ == '__main__':
    main()
