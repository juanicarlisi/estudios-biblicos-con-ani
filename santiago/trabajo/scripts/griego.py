#!/usr/bin/env python3
"""Consulta el griego de Santiago (SBLGNT con el análisis de MorphGNT) y el léxico de Strong.

Uso: griego.py 2:14               -> palabras del versículo con lema, análisis y número Strong
     griego.py 2:14 2:17          -> rango
     griego.py --buscar δικαιόω   -> versículos donde aparece ese lema o forma (sin acentos también)
     griego.py --verificar "πίστις" "ἔργα"   -> dice si cada palabra figura en el texto (forma o lema)

Texto griego: SBL Greek New Testament (SBLGNT), © 2010 Society of Biblical Literature y Logos Bible Software, con el análisis
morfológico de MorphGNT (CC BY-SA, J. K. Tauber). Léxico: Strong's Greek Dictionary (Open Scriptures, CC BY-SA).
El léxico se baja una vez de github.com/openscriptures/strongs a TRABAJO_SANTIAGO/griego/strongs-greek.js.
"""
import sys, os, re, json, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
import config as C

TXT = os.path.join(C.REPO_TRABAJO, 'griego', 'sblgnt_santiago_morphgnt.txt')
LEX = os.path.join(C.TMP, 'griego', 'strongs-greek.js')


def sin_acentos(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', s).lower().replace('ς', 'σ')


def lexico():
    t = open(LEX).read()
    j = json.loads(t[t.index('{'):t.rindex('}')+1])
    por_lema = {}
    for k, e in j.items():
        por_lema.setdefault(sin_acentos(e.get('lemma', '')), []).append((k, e))
    return j, por_lema


def versos():
    out = {}
    for linea in open(TXT, encoding='utf-8'):
        p = linea.split()
        if len(p) < 7:
            continue
        ref, pos, parse, texto, palabra, norm, lema = p[:7]
        c, v = int(ref[2:4]), int(ref[4:6])
        out.setdefault((c, v), []).append({'texto': texto, 'palabra': palabra, 'norm': norm, 'lema': lema, 'pos': pos, 'parse': parse})
    return out


def strong_de(lema, por_lema):
    c = por_lema.get(sin_acentos(lema), [])
    return c[0] if c else (None, {})


def p(x):
    c, n = x.split(':')
    return int(c), int(n)


if __name__ == '__main__':
    V = versos()
    if len(sys.argv) < 2:
        print(__doc__); sys.exit()
    if sys.argv[1] == '--buscar':
        b = sin_acentos(sys.argv[2])
        print([f'{c}:{v}' for (c, v), ws in sorted(V.items()) if any(sin_acentos(w['palabra']) == b or sin_acentos(w['lema']) == b for w in ws)])
    elif sys.argv[1] == '--verificar':
        formas = set(); lemas = set()
        for ws in V.values():
            for w in ws:
                formas.add(sin_acentos(w['palabra'])); lemas.add(sin_acentos(w['lema']))
        for w in sys.argv[2:]:
            b = sin_acentos(w)
            print(w, '->', 'forma del texto' if b in formas else 'lema del texto' if b in lemas else 'NO figura en Santiago')
    else:
        _, por_lema = lexico()
        a = p(sys.argv[1]); b = p(sys.argv[2]) if len(sys.argv) > 2 else a
        for k in sorted(V):
            if a <= k <= b:
                print(f'Stg {k[0]}:{k[1]}')
                for w in V[k]:
                    num, e = strong_de(w['lema'], por_lema)
                    print(f"  {w['palabra']}\t{w['lema']}\t{num or ''}\t{e.get('translit', '')}\t{(e.get('strongs_def') or '').strip()[:70]}\t[{w['pos']} {w['parse']}]")
