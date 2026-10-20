#!/usr/bin/env python3
"""Baja de BibleGateway el texto RVR1960 de los versículos clave que usan los días (cualquier libro).

Uso: rvr.py              (toma las referencias de varon/dias/dia_*.json → campo "versiculos")
     rvr.py "Efesios 5:25" "1 Timoteo 3:1-2"   (prueba con referencias sueltas)
Guarda varon/biblia/rvr.json {referencia normalizada: texto} y cachea el HTML en varon/biblia/bg/.
Normaliza la referencia al nombre castellano completo ("Ef 5:25" → "Efesios 5:25").
"""
import re, json, os, sys, glob, time, subprocess, html, unicodedata
from html.parser import HTMLParser

V = '/home/user/trabajo/varon'
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
LIBROS = [  # (nombre, OSIS, abreviaturas)
    ('Génesis', 'Gen', 'gn gen ge'), ('Éxodo', 'Exod', 'ex exo exod'), ('Levítico', 'Lev', 'lv lev'), ('Números', 'Num', 'nm num'),
    ('Deuteronomio', 'Deut', 'dt deut deu'), ('Josué', 'Josh', 'jos josh'), ('Jueces', 'Judg', 'jue jc'), ('Rut', 'Ruth', 'rt rut'),
    ('1 Samuel', '1Sam', '1s 1sa 1sam'), ('2 Samuel', '2Sam', '2s 2sa 2sam'), ('1 Reyes', '1Kgs', '1r 1re 1rey'), ('2 Reyes', '2Kgs', '2r 2re 2rey'),
    ('1 Crónicas', '1Chr', '1cr 1cro'), ('2 Crónicas', '2Chr', '2cr 2cro'), ('Esdras', 'Ezra', 'esd'), ('Nehemías', 'Neh', 'neh ne'),
    ('Ester', 'Esth', 'est'), ('Job', 'Job', 'job jb'), ('Salmos', 'Ps', 'sal salmo ps'), ('Proverbios', 'Prov', 'pr prov pro'),
    ('Eclesiastés', 'Eccl', 'ec ecl'), ('Cantares', 'Song', 'cnt cant cantar cantares'), ('Isaías', 'Isa', 'is isa'), ('Jeremías', 'Jer', 'jer jr'),
    ('Lamentaciones', 'Lam', 'lm lam'), ('Ezequiel', 'Ezek', 'ez eze'), ('Daniel', 'Dan', 'dn dan'), ('Oseas', 'Hos', 'os'),
    ('Joel', 'Joel', 'jl'), ('Amós', 'Amos', 'am'), ('Abdías', 'Obad', 'abd'), ('Jonás', 'Jonah', 'jon'), ('Miqueas', 'Mic', 'mi miq'),
    ('Nahúm', 'Nah', 'nah'), ('Habacuc', 'Hab', 'hab'), ('Sofonías', 'Zeph', 'sof'), ('Hageo', 'Hag', 'hag'), ('Zacarías', 'Zech', 'zac'),
    ('Malaquías', 'Mal', 'mal ml'), ('Mateo', 'Matt', 'mt mat'), ('Marcos', 'Mark', 'mr mc mar'), ('Lucas', 'Luke', 'lc luc'),
    ('Juan', 'John', 'jn jua'), ('Hechos', 'Acts', 'hch hech'), ('Romanos', 'Rom', 'ro rom rm'), ('1 Corintios', '1Cor', '1co 1cor'),
    ('2 Corintios', '2Cor', '2co 2cor'), ('Gálatas', 'Gal', 'ga gal gá'), ('Efesios', 'Eph', 'ef efe'), ('Filipenses', 'Phil', 'fil flp'),
    ('Colosenses', 'Col', 'col'), ('1 Tesalonicenses', '1Thess', '1ts 1tes'), ('2 Tesalonicenses', '2Thess', '2ts 2tes'),
    ('1 Timoteo', '1Tim', '1ti 1tim'), ('2 Timoteo', '2Tim', '2ti 2tim'), ('Tito', 'Titus', 'tit'), ('Filemón', 'Phlm', 'flm filem'),
    ('Hebreos', 'Heb', 'he heb'), ('Santiago', 'Jas', 'stg sant'), ('1 Pedro', '1Pet', '1p 1pe 1ped'), ('2 Pedro', '2Pet', '2p 2pe 2ped'),
    ('1 Juan', '1John', '1jn 1jua'), ('2 Juan', '2John', '2jn'), ('3 Juan', '3John', '3jn'), ('Judas', 'Jude', 'jud'), ('Apocalipsis', 'Rev', 'ap apoc'),
]


def sin_tildes(s):
    return unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()


INDICE = {}
for nombre, osis, abrevs in LIBROS:
    for k in [nombre] + abrevs.split():
        INDICE[sin_tildes(k).replace(' ', '')] = (nombre, osis)


def normalizar(ref):
    m = re.match(r'^\s*((?:[123]\s*)?[A-Za-zÁÉÍÓÚáéíóúñÑ]+)\.?\s+(\d+):(\d+)(?:\s*[-–]\s*(\d+))?\s*$', ref)
    if not m:
        return None
    libro = INDICE.get(sin_tildes(m.group(1)).replace(' ', ''))
    if not libro:
        return None
    c, v1, v2 = int(m.group(2)), int(m.group(3)), int(m.group(4) or m.group(3))
    return libro, c, v1, v2


class P(HTMLParser):
    def __init__(s, osis, c):
        super().__init__(); s.osis = osis; s.c = c; s.stack = []; s.verses = {}; s.skip = 0
    def handle_starttag(s, tag, attrs):
        cls = dict(attrs).get('class', '') or ''
        m = re.search(r'\b%s-%d-(\d+)\b' % (re.escape(s.osis), s.c), cls)
        if tag == 'span' and m and 'text' in cls.split():
            v = int(m.group(1))
            if s.verses.get(v, '').strip():      # nueva línea poética del mismo versículo
                s.verses[v] += ' / '
            s.stack.append(('verse', v)); return
        if tag == 'sup' or (tag == 'span' and 'chapternum' in cls) or (tag == 'div' and ('footnotes' in cls or 'crossrefs' in cls)) or tag == 'h3':
            s.stack.append(('skip', None)); s.skip += 1; return
        s.stack.append((tag, None))
    def handle_endtag(s, tag):
        if s.stack:
            k, _ = s.stack.pop()
            if k == 'skip': s.skip -= 1
    def handle_data(s, d):
        if s.skip: return
        vs = [v for k, v in s.stack if k == 'verse']
        if vs: s.verses[vs[-1]] = s.verses.get(vs[-1], '') + d


def bajar(ref):
    n = normalizar(ref)
    if not n:
        return None, None
    (nombre, osis), c, v1, v2 = n
    clave = f'{nombre} {c}:{v1}' + (f'-{v2}' if v2 != v1 else '')
    os.makedirs(f'{V}/biblia/bg', exist_ok=True)
    fn = f'{V}/biblia/bg/{osis}_{c}_{v1}_{v2}.html'
    if not os.path.exists(fn) or os.path.getsize(fn) < 20000:
        q = f'{nombre} {c}:{v1}' + (f'-{v2}' if v2 != v1 else '')
        subprocess.run(['curl', '-sS', '-A', UA, '-G', 'https://www.biblegateway.com/passage/', '--data-urlencode', f'search={q}', '--data-urlencode', 'version=RVR1960', '-o', fn])
        time.sleep(1.5)
    t = open(fn, errors='ignore').read()
    i = t.find('<div class="passage-text">'); j = t.find('<div class="footnotes">', i)
    p = P(osis, c); p.feed(t[i:j if j > 0 else None])
    vs = [re.sub(r'\s+', ' ', html.unescape(p.verses.get(v, ''))).strip() for v in range(v1, v2 + 1)]
    if not all(vs):
        return clave, None
    return clave, ' '.join(vs)


def main():
    refs = sys.argv[1:]
    if not refs:
        for f in glob.glob(f'{V}/dias/dia_*.json'):
            refs += [v['ref'] for v in json.load(open(f)).get('versiculos', [])]
    dst = f'{V}/biblia/rvr.json'
    res = json.load(open(dst)) if os.path.exists(dst) else {}
    fallas = []
    for r in sorted(set(refs)):
        clave, txt = bajar(r)
        if txt:
            res[r] = txt
            if clave: res[clave] = txt
        else:
            fallas.append(r)
    json.dump(res, open(dst, 'w'), ensure_ascii=False, indent=0)
    print('versículos:', len(res), '| sin texto:', fallas)


if __name__ == '__main__':
    main()
