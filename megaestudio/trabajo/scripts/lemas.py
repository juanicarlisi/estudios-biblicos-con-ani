#!/usr/bin/env python3
"""Lemas de Strong (OpenScriptures, CC-BY-SA) para comprobar la grafía de las palabras hebreas y griegas de los días.
Se compara sin acentos, espíritus, vocales ni cantilación, y con letras finales unificadas. Los datos quedan en $MEGA_STRONG (no van al repo)."""
import json, os, re, unicodedata
D = os.environ.get('MEGA_STRONG', '/home/user/lib/strong')
FIN = str.maketrans('ךםןףץς', 'כמנפצσ')
def clave(t):
    t = unicodedata.normalize('NFD', t.lower())
    t = ''.join(c for c in t if not unicodedata.combining(c) and c not in '־ֽ')   # marcas combinantes (vocales, acentos) y maqaf
    return re.sub(r'[^Ͱ-Ͽא-ת]', '', t).translate(FIN)
_cache = None
def lemas():
    global _cache
    if _cache is None:
        ruta = f'{D}/lemas.json'
        if not os.path.exists(ruta):
            out = {'el': set(), 'he': set()}
            for f, k in (('strongs-greek-dictionary.js', 'el'), ('strongs-hebrew-dictionary.js', 'he')):
                t = open(f'{D}/{f}', encoding='utf-8').read(); d = json.loads(t[t.index('{'):t.rindex('}') + 1])
                for e in d.values():
                    c = clave(e.get('lemma', ''))
                    if c: out[k].add(c)
            # formas de superficie: Biblia hebrea (WLC, OpenScriptures morphhb) y Nuevo Testamento griego (SBLGNT, MorphGNT)
            import glob
            for f in glob.glob(f'{D}/wlc/*.xml'):
                for w in re.findall(r'<w [^>]*>([^<]+)</w>', open(f, encoding='utf-8').read()):
                    seg = w.split('/'); c = clave(''.join(seg))
                    if c: out['he'].add(c)
                    for x in seg:
                        c = clave(x)
                        if c: out['he'].add(c)
            for f in glob.glob(f'{D}/gnt/*.txt'):
                for l in open(f, encoding='utf-8'):
                    cols = l.split()
                    if len(cols) >= 7:
                        for x in cols[4:7]:
                            c = clave(x)
                            if c: out['el'].add(c)
            json.dump({k: sorted(v) for k, v in out.items()}, open(ruta, 'w'), ensure_ascii=False)
        d = json.load(open(ruta)); _cache = {k: set(v) for k, v in d.items()}
    return _cache
def grafia_valida(original):
    """True si cada palabra de `original` es un lema de Strong (hebreo/arameo o griego)."""
    L = lemas(); ok = True
    for w in re.split(r'[\s/,;]+', original.strip()):
        c = clave(w)
        if not c: continue
        if not (c in L['el'] or c in L['he']): ok = False
    return ok
