#!/usr/bin/env python3
"""Reutiliza las notas del estudio del varón que sirven igual para una mujer (temas universales de la vida cristiana).

Toma varon/notas/*.json de las secciones universales, descarta las que hablan del varón (marcadores en título, subtema y
contenido) y las copia a mujer/notas/v_<bloque>.json con ids «v_b_014#7» y fuentes «vR0001» (el registro de fuentes del varón se
suma al de la mujer con ese prefijo). Uso: reusar_varon.py [--minimo 2]"""
import json, glob, os, re, sys, unicodedata
T = '/home/user/trabajo'
SEC = set('CDFJKPBOE')          # secciones universales: Dios, carácter, trabajo, siervo, relaciones, pruebas, diseño, sociedad, pureza
NO = set('QGHILMNA')            # propias del varón (esposo, padre, líder, joven, adulto, mayor, crisis) o de personajes masculinos
MIN = int(sys.argv[sys.argv.index('--minimo') + 1]) if '--minimo' in sys.argv else 2


def norm(s):
    return unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()


MARC = re.compile(r'\bvaron(es|il)?\b|masculin\w*|virilidad|hombria|\besposos?\b|\bmaridos?\b|\bpadres? (de familia|cristiano|piadoso)|paternidad|\bser (un )?hombre\b|hombres? (de dios|cristianos?|piadosos?|casados?|solteros?|jovenes|maduros?)|\blos hombres\b|\bun hombre (cristiano|piadoso|de dios)|a los hombres|\bsu esposa\b|\bcabeza del hogar|sacerdote del hogar|\bmi esposa\b|\bpastores?\b (varon|hombre)')


def main():
    vf = json.load(open(f'{T}/varon/bloques/_fuentes.json'))
    mf = json.load(open(f'{T}/mujer/bloques/_fuentes.json'))
    for k, v in vf.items():
        mf['v' + k] = {**v, 'clave': 'varon:' + v.get('clave', '')}
    json.dump(mf, open(f'{T}/mujer/bloques/_fuentes.json', 'w'), ensure_ascii=False, indent=1)
    os.makedirs(f'{T}/mujer/notas', exist_ok=True)
    tot = pas = 0
    for f in sorted(glob.glob(f'{T}/varon/notas/*.json')):
        b = os.path.basename(f)[:-5]
        out = []
        for n in json.load(open(f))['notas']:
            tot += 1
            if n['seccion'] not in SEC or n.get('importancia', 2) < MIN:
                continue
            t = norm(' '.join([n.get('titulo', ''), n.get('subtema', ''), n.get('contenido', ''), n.get('cita', '')]))
            if MARC.search(t) or (n.get('persona') and n['seccion'] == 'Q'):
                continue
            n = dict(n); n['fuente'] = 'v' + n['fuente']
            out.append(n)
        if out:
            json.dump({'notas': out}, open(f'{T}/mujer/notas/v_{b}.json', 'w'), ensure_ascii=False); pas += len(out)
    print(f'notas del varón {tot} → reutilizables {pas} (secciones {"".join(sorted(SEC))}, importancia ≥ {MIN})')


if __name__ == '__main__':
    main()
