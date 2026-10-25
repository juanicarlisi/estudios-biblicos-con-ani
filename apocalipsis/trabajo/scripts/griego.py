#!/usr/bin/env python3
"""Griego de Apocalipsis (SBLGNT con análisis MorphGNT) y léxico de Strong.

Uso: griego.py 3:20            -> palabras del versículo (con Strong y definición)
     griego.py 3:20 3:22       -> rango
     griego.py --buscar ἀγάπη  -> versículos donde aparece ese lema
     griego.py --construir     -> baja los datos y arma griego/apocalipsis_griego.json
Fuentes: MorphGNT-SBLGNT (texto SBLGNT © SBL y Faithlife, CC BY 4.0; análisis CC BY-SA 3.0, J. K. Tauber) y
Strong's Greek Dictionary (OpenScriptures, CC BY-SA).
"""
import sys, re, json, os, unicodedata, urllib.request
AQUI = os.path.dirname(os.path.abspath(__file__)); DIR = os.path.join(AQUI, '..', 'griego'); os.makedirs(DIR, exist_ok=True)
URL_RE = 'https://raw.githubusercontent.com/morphgnt/sblgnt/master/87-Re-morphgnt.txt'
URL_ST = 'https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.js'
def nfc(s): return unicodedata.normalize('NFC', s)
def sin_acentos(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.category(c).startswith('M')).replace('ς', 'σ')
def construir():
    t = urllib.request.urlopen(URL_RE, timeout=60).read().decode('utf-8')
    s = urllib.request.urlopen(URL_ST, timeout=60).read().decode('utf-8')
    st = json.loads(s[s.index('{'):s.rindex('}') + 1])
    por_lema = {}
    for k, v in st.items():
        por_lema.setdefault(sin_acentos(v.get('lemma', '')), []).append(k)
    out = {}; sin_strong = set()
    for l in t.splitlines():
        ref, pos, parse, texto, palabra, norm, lema = l.split(' ')
        c, v = int(ref[2:4]), int(ref[4:6])
        cand = por_lema.get(sin_acentos(lema), [])
        sn = cand[0] if cand else ''
        if not sn: sin_strong.add(lema)
        out.setdefault(f'{c}:{v}', []).append({'t': nfc(texto), 'p': nfc(palabra), 'l': nfc(lema), 's': sn, 'm': pos + ' ' + parse})
    lex = {k: {'lemma': nfc(v.get('lemma', '')), 'xlit': v.get('translit', ''), 'def': v.get('strongs_def', ''), 'kjv': v.get('kjv_def', '')} for k, v in st.items()}
    json.dump({'versiculos': out, 'lexico': lex}, open(os.path.join(DIR, 'apocalipsis_griego.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    print('versículos', len(out), 'palabras', sum(len(v) for v in out.values()), 'lemas sin Strong', len(sin_strong), list(sin_strong)[:15])
def cargar(): return json.load(open(os.path.join(DIR, 'apocalipsis_griego.json')))
def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    if a[0] == '--construir': construir(); return
    D = cargar(); V, L = D['versiculos'], D['lexico']
    if a[0] == '--buscar':
        q = sin_acentos(a[1]); print([k for k, ws in V.items() if any(sin_acentos(w['l']) == q or sin_acentos(w['p']) == q for w in ws)]); return
    def p(x): c, n = x.split(':'); return int(c), int(n)
    d = p(a[0]); h = p(a[1]) if len(a) > 1 else d
    for k in sorted(V, key=lambda x: p(x)):
        if d <= p(k) <= h:
            print('Ap', k, ' '.join(w['t'] for w in V[k]))
            for w in V[k]:
                e = L.get(w['s'], {}); print(f"   {w['p']}\t{w['l']}\t{w['s']}\t{e.get('xlit','')}\t{(e.get('def') or '')[:70]}")
if __name__ == '__main__': main()
