#!/usr/bin/env python3
"""Arma bloques de extracción w_NNN.txt con páginas web confiables (Coalición por el Evangelio y Aviva Nuestros Corazones).

Cada página web es una «fuente» (id R5xxx, con autor, título, sitio y URL) y una sola «página». Se eligen las páginas con
densidad suficiente de temas de mujer (puntajes.TERMINOS) y se empaquetan en bloques de ~TAM caracteres.
Uso: web_a_bloques.py [--min D] [--tam N] [--solo-contar]
"""
import json, os, re, sys, collections
sys.path.insert(0, '/home/user/trabajo/mujer/scripts')
from puntajes import RX, norm  # noqa: E402

V = '/home/user/trabajo/mujer'
TAM = 70000
MINIMO = float(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 6.0   # puntos por 1000 caracteres
if '--tam' in sys.argv:
    TAM = int(sys.argv[sys.argv.index('--tam') + 1])


EXTRA = [re.compile(p) for p in (
    r'fruto del espiritu|galatas 5[:.] ?22|amor, gozo, paz|paciencia|benignidad|\bbondad\b|mansedumbre|dominio propio|autocontrol',
    r'emocion\w*|sentimientos?|tristeza|enojo|\bira\b|\bmiedo\b|verguenza|\bculpa\b|\bcelos\b|soledad|\bduelo\b|ansiedad|esperanza|gratitud|agradecimient\w+|\bperdon\b|amargura|resentimiento|autoestima|descanso|cansancio')]


def densidad(t):
    n = norm(t)
    return (sum(w * len(rx.findall(n)) for _, w, rx in RX) + 3 * sum(len(rx.findall(n)) for rx in EXTRA)) / max(1, len(t) / 1000)


def paginas():
    for l in open(f'{V}/fuentes_web/cpe/pages.jsonl'):
        p = json.loads(l)
        if p.get('error') or len(p.get('texto', '')) < 1500:
            continue
        a = re.search(r'\|\s*([^|]+)$', p.get('cab', ''))
        yield {'url': p['url'], 'sitio': 'Coalición por el Evangelio', 'sec': p['sec'], 'titulo': p['titulo'], 'autor': (a.group(1).strip() if a else 'Coalición por el Evangelio'), 'texto': p['texto']}
    if os.path.exists(f'{V}/fuentes_web/aviva/pages.jsonl'):
        for l in open(f'{V}/fuentes_web/aviva/pages.jsonl'):
            p = json.loads(l)
            if p.get('error') or len(p.get('texto', '')) < 3000:
                continue
            yield {'url': p['url'], 'sitio': 'Aviva Nuestros Corazones', 'sec': 'podcast:' + p['pod'], 'titulo': p['titulo'], 'autor': 'Nancy DeMoss Wolgemuth y colaboradoras (Aviva Nuestros Corazones)', 'texto': p['texto']}


def main():
    todas = list(paginas())
    sel = []
    for p in todas:
        p['dens'] = densidad(p['texto'])
        # secciones de mujeres entran siempre; el resto, por densidad
        if p['sec'] in ('mujeres', 'para-ser-sinceras') or p['dens'] >= (MINIMO * 0.6 if p['sec'].startswith('podcast:') else MINIMO):
            sel.append(p)
    print('páginas', len(todas), '| elegidas', len(sel), '| caracteres', sum(len(p['texto']) for p in sel))
    print(collections.Counter(p['sec'] for p in sel).most_common(12))
    if '--solo-contar' in sys.argv:
        return
    fuentes_f = f'{V}/bloques/_fuentes.json'
    fuentes = json.load(open(fuentes_f))
    for k in [k for k in fuentes if k.startswith('R5')]:
        del fuentes[k]
    for f in os.listdir(f'{V}/bloques'):
        if f.startswith('w_'):
            os.remove(f'{V}/bloques/{f}')
    sel.sort(key=lambda p: (p['sec'], p['url']))
    bloques, act, tam = [], [], 0
    for p in sel:
        if tam + len(p['texto']) > TAM and act:
            bloques.append(act); act, tam = [], 0
        act.append(p); tam += len(p['texto'])
    if act:
        bloques.append(act)
    n = 0
    for k, b in enumerate(bloques, 1):
        cab, cuerpo = ['FUENTES DE ESTE BLOQUE (id = autor, obra):'], []
        for p in b:
            n += 1
            i = f'R{5000 + n}'
            obra = f"{p['titulo']} ({p['sitio']})"
            fuentes[i] = {'clave': 'web:' + p['url'], 'fuente': 'web', 'archivo': p['url'], 'autor': p['autor'], 'obra': obra, 'url': p['url']}
            cab.append(f"{i} = {p['autor']}, {obra}")
            cuerpo.append(f"=== [{i} | pág. 1] ===\n{p['texto']}\n")
        open(f'{V}/bloques/w_{k:03d}.txt', 'w').write('\n'.join(cab) + '\n\n' + '\n'.join(cuerpo))
    json.dump(fuentes, open(fuentes_f, 'w'), ensure_ascii=False, indent=1)
    print('bloques w_:', len(bloques), '| fuentes web:', n)


if __name__ == '__main__':
    main()
