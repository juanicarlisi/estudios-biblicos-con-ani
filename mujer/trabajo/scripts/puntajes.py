#!/usr/bin/env python3
"""Puntúa cada página del corpus (REFERENCIA3 confiable + biblioteca) según cuánto trata de la mujer.

Escribe mujer/puntajes.jsonl: {fuente, archivo, pagina, chars, puntaje, temas{...}} por página.
Las páginas sin saltos (\\f) se cortan en trozos de ~3000 caracteres.
"""
import json, glob, os, re, unicodedata, collections

T = '/home/user/trabajo'
OUT = f'{T}/mujer/puntajes.jsonl'


def norm(s):
    return unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()


# (tema, peso, patrón) sobre texto normalizado
TERMINOS = [
    ('identidad', 3, r'feminidad|femenin\w*|ser (una )?mujer\b|mujeres? (de dios|piadosas?|cristianas?|sabias?|virtuosas?|del reino)|mujer (virtuosa|conforme|sabia|de dios|del reino)|hijas? de dios|belleza (interior|verdadera|autentica)|identidad (de la mujer|femenina)|ayuda idonea|mujer de proverbios|\bmujeres?\b(?= (y|de|en|que) (la|su|sus|dios))'),
    ('identidad', 1, r'\bmujer(es)?\b'),
    ('esposa', 3, r'\besposa\b|\bmujer casada|ser (una )?(buena )?esposa|sed sujetas|esposas?,? (someteos|sed sujetas)|sumision de la (mujer|esposa)|respeto (a|por) (su |al )?(esposo|marido)|\bvuestros maridos|\bsu marido\b|a sus maridos'),
    ('madre', 3, r'maternidad|\bmadres?\b|ser (una )?madre|criar (a )?(sus|los) hijos|\bcrianza\b|embaraz\w+|lactan\w*|dar a luz|ama de casa|madre soltera|abuela'),
    ('madre', 1, r'\bhijas?\b'),
    ('trabajo', 2, r'ama de casa|administr\w+ (del |el )?hogar|economia domestica|trabajo (de la mujer|fuera del hogar|en casa)|mujer (que trabaja|profesional)|vocacion de la mujer|cuidar (de )?(la casa|el hogar)|proverbios 31'),
    ('ministro', 3, r'mujeres? (en|y) (el )?(ministerio|liderazgo|la iglesia)|diaconisa\w*|profetisa\w*|mujeres? (pastor|lider|maestra|predicador)\w*|\bfebe\b|primera a timoteo 2|1 timoteo 2|silencio de la mujer|ordenaci\w+ de (las )?mujeres|ensenar a los hombres'),
    ('siervo', 2, r'hospitalidad|misericordia|\bdorcas\b|\bmarta\b|servir a (otros|los demas)|servicio (de la mujer|femenino)'),
    ('joven', 3, r'jovenes (mujeres|solteras)|mujer(es)? joven\w*|adolescente (mujer)|chicas?\b|ninas?\b|senoritas?|noviazgo|solter[ao]s?\b|virginidad|\bnovia\b|esperar a (su|tu) (esposo|futuro)'),
    ('mayor', 3, r'ancianas|mujeres mayores|\bvejez\b|\babuelas?\b|viuda\w*|menopausia|nido vacio|\btito 2\b|mujeres? ancian\w+'),
    ('sociedad', 2, r'feminis\w*|igualdad de genero|ideologia de genero|mujer (moderna|actual|en la sociedad)|cultura (actual|moderna)|redes sociales|\bmoda\b|\baborto\b|\bmedios de comunicacion\b'),
    ('pureza', 3, r'imagen corporal|trastornos? (de la conducta )?alimenti\w+|\bmodestia\b|\bpudor\b|maquillaje|vestim\w+|pornograf\w*|abuso sexual|inmoralidad sexual|\bpureza\b|\bseduccion\b|cuerpo de la mujer'),
    ('caracter', 2, r'ansiedad|\bafan\w*|\bchism\w+|contienda|contenta\w*|espiritu (afable|apacible|tranquilo|manso)|mansedumbre|envidia|\bcelos\b|perfeccionis\w*|comparaci\w+|\btemor\b|\bmiedo\b|\bcontrol\b|manipul\w+'),
    ('crisis', 3, r'depresion|ansiedad|soledad|divorcio|infertilidad|esterilidad|perdida (de un|del) (bebe|embarazo)|\bduelo\b|\babuso\b|violencia (domestica|familiar|de genero)|adicci\w+|autoestima|baja estima|estres\b|agotamiento|burnout|\bcansancio\b'),
    ('liderazgo', 2, r'complementari\w+|igualitari\w+|roles? (de|del) (hombre|mujer|genero)|liderazgo (femenino|de la mujer)|mujeres lideres|sumision|jefatura'),
    ('amistad', 2, r'\bamistad\w*|\bamigas?\b|mentoria|discipular\w* a (las )?mujeres|hermandad|ministerio de mujeres|reunion de mujeres'),
    ('personajes', 3, r'\b(eva|sara|agar|rebeca|raquel|tamar|noemi|debora|jael|abigail|betsabe|vasti|elisabet|isabel|lidia|priscila|dorcas|jezabel|atalia|rahab|miriam|sarepta|sunamita|samaritana|sirofenicia|safira|herodias|hulda|ester|rut|ana la profetisa|maria magdalena|virgen maria)\b'),
    ('personajes', 1, r'\bmaria\b|\bana\b'),
]
RX = [(t, w, re.compile(p)) for t, w, p in TERMINOS]


def paginas(txt):
    if '\f' in txt:
        return txt.split('\f')
    return [txt[i:i + 3000] for i in range(0, len(txt), 3000)]


def fuentes():
    clas = {e['path']: e for e in json.load(open(f'{T}/clasif/clasificacion.json'))}
    borr = set(json.load(open(f'{T}/borrado/archivos_borrados_claves.json')))
    borr |= {'REF3/Teologia Sistematica y Doctrina/001 - Los atributos de Dios - A. W. Pink - Resumen.docx',
             'REF3/Crecimiento y Vida Cristiana/Copia de Los Peligros de la Fe Superficial - A. W. Tozer - Resumen(1).docx'}
    for m in map(json.loads, open(f'{T}/corpus_ref3/_manifiesto.jsonl')):
        p = m['path']; c = clas.get(p)
        if not c or c['categoria'] != 'A' or ('REF3/' + p) in borr:
            continue
        f = f'{T}/corpus_ref3/{p}.txt'
        ocr = f'{T}/corpus_ref3/{p}.ocr.txt'
        if os.path.exists(ocr) and os.path.getsize(ocr) > (os.path.getsize(f) if os.path.exists(f) else 0):
            f = ocr
        if os.path.exists(f):
            yield 'ref3', p, f
    biblio_borr = {l.strip() for l in open(f'{T}/borrado/biblio_rutas.txt') if l.strip()}
    vistos = set()
    for f in sorted(glob.glob(f'{T}/corpus_biblio/todo/**/*.txt', recursive=True)):
        if '.paginas/' in f:          # caché de OCR página por página
            continue
        rel = os.path.relpath(f, f'{T}/corpus_biblio/todo')
        base = re.sub(r'\.(ocr\.)?txt$', '', rel)
        if base in vistos or 'MATERIAL SOPORTE/' + base in biblio_borr:
            continue
        ocr = f'{T}/corpus_biblio/todo/{base}.ocr.txt'; pl = f'{T}/corpus_biblio/todo/{base}.txt'
        elegido = ocr if os.path.exists(ocr) and (not os.path.exists(pl) or os.path.getsize(ocr) > os.path.getsize(pl)) else pl
        vistos.add(base)
        if os.path.exists(elegido):
            yield 'biblio', base, elegido


def main():
    n = 0
    with open(OUT, 'w') as out:
        for fuente, arch, f in fuentes():
            txt = open(f, errors='ignore').read()
            for i, pg in enumerate(paginas(txt), 1):
                if len(pg.strip()) < 200:
                    continue
                t = norm(pg); temas = collections.Counter()
                for tema, w, rx in RX:
                    k = len(rx.findall(t))
                    if k:
                        temas[tema] += w * k
                punt = sum(temas.values()) * 3000 / max(len(pg), 800)
                out.write(json.dumps({'fuente': fuente, 'archivo': arch, 'txt': os.path.relpath(f, T), 'pagina': i,
                                      'chars': len(pg), 'puntaje': round(punt, 1), 'temas': dict(temas)}, ensure_ascii=False) + '\n')
                n += 1
    print('páginas', n)


if __name__ == '__main__':
    main()
