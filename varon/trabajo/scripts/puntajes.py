#!/usr/bin/env python3
"""Puntúa cada página del corpus (REFERENCIA3 confiable + biblioteca) según cuánto trata del varón.

Escribe varon/puntajes.jsonl: {fuente, archivo, pagina, chars, puntaje, temas{...}} por página.
Las páginas sin saltos (\\f) se cortan en trozos de ~3000 caracteres.
"""
import json, glob, os, re, unicodedata, collections

T = '/home/user/trabajo'
OUT = f'{T}/varon/puntajes.jsonl'


def norm(s):
    return unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()


# (tema, peso, patrón) sobre texto normalizado
TERMINOS = [
    ('identidad', 3, r'\bvaron(es|il)?\b|\bhombria\b|masculin\w*|virilidad|\bser (un )?hombre\b|hombres? de dios\b|hombres? piados\w*|hombres? cristianos?\b|hombre de verdad|verdadero hombre'),
    ('esposo', 3, r'\besposos?\b|\bmaridos?\b|cabeza (de la mujer|del hogar|de (su|la) familia)|amad a vuestras mujeres|ame a su (mujer|esposa)|su esposa\b'),
    ('padre', 3, r'paternidad|padres? de familia|\bcrianza\b|criar (a )?(los|sus) hijos|disciplin\w+ (a )?(los|sus) hijos|instruye al nino|ser (un buen )?padre|como padres?\b|padres? (cristianos?|piadosos?)|hijos varones'),
    ('padre', 1, r'\bpadres?\b|\bhijos?\b'),
    ('trabajo', 2, r'\btrabaj\w*|vocacion\w*|\bempleo\w*|\boficio\b|proveed\w*|\bproveer\b|sudor de tu rostro|desemple\w*|jubilaci\w*|\bnegocios?\b|\bcarrera profesional'),
    ('ministro', 2, r'\bpastor(es|ado)?\b|\bancianos? (de la iglesia|gobernantes?)\b|\bobispos?\b|\bdiacon\w+|llamado al ministerio|\bpredicador\w*|ministerio pastoral'),
    ('siervo', 2, r'\bsiervos?\b|\bservi(r|cio|dor)\w*|lav(ar|o) los pies'),
    ('joven', 2, r'\bjovenes\b|\bjoven\b|juventud|adolescen\w*|\bmuchachos?\b|noviazgo|solter\w+'),
    ('mayor', 3, r'\bvejez\b|edad avanzada|tercera edad|adultos? mayor\w*|jubilad\w*|\bcanas\b|\bancian(o|os|idad)\b(?! de la iglesia)'),
    ('sociedad', 1, r'\bsociedad\b|\bciudadan\w+|\bgobierno\b|\bcultura\b|sal de la tierra|luz del mundo'),
    ('pureza', 3, r'pornograf\w*|lujuria|masturbaci\w*|pureza sexual|tentacion sexual|inmoralidad sexual|fornicaci\w*|adulterio'),
    ('caracter', 1, r'\bira\b|\benojo\b|pasividad|orgullo|\bcoraje\b|valent\w+|domin(io|ar) propio|integridad|disciplina espiritual'),
    ('crisis', 2, r'feminis\w*|crisis de (la )?masculinidad|padres? ausentes?|ausencia del padre|\bdivorcio\w*|suicid\w*|depresi\w+|soledad|adicci\w+|alcohol\w*|violencia (domestica|familiar)'),
    ('liderazgo', 2, r'liderazgo|\blider(es|ar)?\b|guiar a su familia|sumision|jefatura'),
    ('amistad', 2, r'\bamistad\w*|\bamigos?\b|rendicion de cuentas|discipulado de hombres|hierro con hierro'),
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
