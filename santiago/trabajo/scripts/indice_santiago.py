#!/usr/bin/env python3
"""Indexa, página por página, todo lo que toca Santiago en el texto de los libros de REFERENCIA3 (categoría A).

Para cada archivo cuenta las citas explícitas de la carta (con capítulo y versículo, siguiendo las citas encadenadas con «;»)
y las frases y nombres propios de Santiago (fe sin obras, la lengua, el doble ánimo, Rahab, Elías, la unción con aceite…).
Salida: TMP/indice/indice_todo.json con, por archivo, las páginas con señal y su puntaje.
Uso: indice_santiago.py
"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import config as C

CORPUS = os.path.join(C.TMP, 'corpus_ref3')
DEST = os.path.join(C.TMP, 'indice')

LIBRO = r'(?:Santiago|Stgo?|Sant|Jac)'
# Cita: libro + cap[:vers[-vers]] y continuaciones «; cap:vers» o «, vers»
RE_STG = re.compile(r'(?<![\wÁ-ú])' + LIBRO + r'\.?\s*(\d{1,2})(?:\s*[:.,]\s*(\d{1,3})(?:\s*[-–—]\s*(\d{1,3}))?)?')
RE_CONT = re.compile(r'\s*[;,]\s*(?:y\s+)?(\d{1,2})\s*[:.]\s*(\d{1,3})(?:\s*[-–—]\s*(\d{1,3}))?')

FUERTES = [
    'fe sin obras', 'fe y obras', 'fe muerta', 'fe viva', 'obras de la fe', 'justificado por las obras', 'justificados por las obras',
    'la fe sin las obras', 'Santiago y Pablo', 'Pablo y Santiago', 'epístola de Santiago', 'carta de Santiago', 'libro de Santiago',
    'Epístola de Santiago', 'Carta de Santiago', 'hermano del Señor', 'Jacobo el justo', 'Jacobo, hermano', 'Santiago el justo',
    'doble ánimo', 'doblez de ánimo', 'ley perfecta', 'ley de la libertad', 'ley real', 'hacedores de la palabra', 'hacedores de la Palabra',
    'oidores', 'acepción de personas', 'sabiduría de lo alto', 'sabiduría de arriba', 'sabiduría terrenal', 'sabiduría de abajo',
    'lluvia temprana', 'lluvia tardía', 'unción con aceite', 'ungiéndole con aceite', 'ungirlo con aceite', 'confesaos vuestros pecados',
    'oración de fe', 'oración eficaz', 'ferviente oración', 'amistad con el mundo', 'amigo del mundo', 'el que sabe hacer lo bueno',
    'Dios no tienta', 'ni él tienta', 'corona de vida', 'primicias de sus criaturas', 'palabra implantada', 'doce tribus',
    'la dispersión', 'espejo', 'refrenar la lengua', 'refrenar su lengua', 'freno en la boca', 'la lengua es un fuego', 'veneno mortal',
    'fuente de agua dulce', 'sí sea sí', 'vuestro sí sea sí', 'no juréis', 'rey de Rahab', 'Rahab', 'Elías', 'la paciencia de Job',
    'paciencia de Job', 'prueba de vuestra fe', 'varón perfecto', 'padre de las luces', 'Padre de las luces', 'riqueza se ha podrido',
    'Abraham fue justificado', 'amigo de Dios', 'Dios resiste a los soberbios', 'acercaos a Dios', 'sed hacedores', 'religión pura',
    'pura y sin mácula', 'huérfanos y a las viudas', 'si el Señor quiere', 'si el Señor quisiere',
]
DEBILES = ['obras', 'lengua', 'tentación', 'pruebas', 'paciencia', 'perseverancia', 'sabiduría', 'ricos', 'pobres', 'juzgar', 'jactancia',
           'envidia', 'sufrimiento', 'oración', 'enfermo', 'ancianos de la iglesia']
RE_F = re.compile(r'(?<![\wÁ-ú])(' + '|'.join(re.escape(x) for x in FUERTES) + r')(?![\wÁ-ú])')
RE_D = re.compile(r'(?<![\wÁ-ú])(' + '|'.join(re.escape(x) for x in DEBILES) + r')(?![\wÁ-ú])', re.I)


def citas(texto):
    """Lista de (capítulo, versículo|None) citados de Santiago en el texto."""
    out = []
    for m in RE_STG.finditer(texto):
        c = int(m.group(1))
        if not 1 <= c <= 5:
            continue
        v = int(m.group(2)) if m.group(2) else None
        if v is not None and v > C.V[c - 1]:
            continue
        if v is None and m.group(0).strip().lower().startswith(('jac', 'sant.')) and False:
            continue
        out.append((c, v))
        pos = m.end()
        while True:
            m2 = RE_CONT.match(texto, pos)
            if not m2:
                break
            c2 = int(m2.group(1)); v2 = int(m2.group(2))
            if not 1 <= c2 <= 5 or v2 > C.V[c2 - 1]:
                break
            out.append((c2, v2))
            pos = m2.end()
    return out


def main():
    os.makedirs(DEST, exist_ok=True)
    manif = [json.loads(l) for l in open(os.path.join(CORPUS, '_manifiesto.jsonl'))]
    cl = {x['path']: x for x in json.load(open(C.CLASIFICACION))}
    res = {}
    for r in manif:
        if r['escaneado'] and not os.path.exists(os.path.join(CORPUS, r['path'] + '.txt')):
            continue
        fn = os.path.join(CORPUS, r['path'] + '.txt')
        if r['escaneado']:       # los escaneados que se pasaron por OCR quedan en el mismo lugar
            if not os.path.exists(fn) or os.path.getsize(fn) < 5000:
                continue
        pags = open(fn, errors='ignore').read().split('\f')
        info = []
        for n, p in enumerate(pags, 1):
            cs = citas(p)
            f = RE_F.findall(p)
            d = RE_D.findall(p)
            score = 3 * len(cs) + len(f) + 0.2 * len(d)
            if cs or len(f) >= 2:
                caps = collections.Counter(c for c, _ in cs)
                info.append({'pag': n, 'score': round(score, 1), 'citas': [f'{c}:{v}' if v else f'{c}' for c, v in cs][:40],
                             'caps': dict(caps), 'menciones': dict(collections.Counter(f).most_common(8))})
        c = cl.get('' + r['path'], {})
        res[r['path']] = {'autor': c.get('autor'), 'titulo': c.get('titulo'), 'txt': fn, 'paginas_total': len(pags),
                          'paginas_con_senal': len(info), 'citas_total': sum(len(x['citas']) for x in info),
                          'score_total': round(sum(x['score'] for x in info), 1), 'paginas': info}
    json.dump(res, open(os.path.join(DEST, 'indice_todo.json'), 'w'), ensure_ascii=False)
    tot_c = sum(v['citas_total'] for v in res.values())
    print(len(res), 'archivos indexados;', tot_c, 'citas de Santiago;', sum(v['paginas_con_senal'] for v in res.values()), 'páginas con señal')
    top = sorted(res.items(), key=lambda kv: -kv[1]['score_total'])[:30]
    for k, v in top:
        print(f"  {v['score_total']:8.1f} {v['citas_total']:4d} citas {v['paginas_con_senal']:4d} págs  {k[:90]}")


if __name__ == '__main__':
    main()
