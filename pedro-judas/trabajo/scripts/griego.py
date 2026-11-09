#!/usr/bin/env python3
"""Griego de 1 Pedro a Judas (SBLGNT con análisis MorphGNT) y léxico de Strong.

Uso: griego.py "1P 3:19"           -> palabras del versículo (con Strong y definición)
     griego.py "1J 4:7" "1J 4:8"   -> rango (mismo libro)
     griego.py --buscar ἀγάπη      -> versículos donde aparece ese lema
     griego.py --construir         -> baja los datos y arma griego/pedro_judas_griego.json (claves «1P 1:1», «Jd 3»)
Fuentes: MorphGNT-SBLGNT (texto SBLGNT © SBL y Faithlife, CC BY 4.0; análisis CC BY-SA 3.0, J. K. Tauber) y
Strong's Greek Dictionary (OpenScriptures, CC BY-SA).
"""
import sys, json, os, unicodedata, urllib.request
AQUI = os.path.dirname(os.path.abspath(__file__)); DIR = os.path.join(AQUI, '..', 'griego'); os.makedirs(DIR, exist_ok=True)
sys.path.insert(0, AQUI)
import unidades as U
ARCH = {'1P': '81-1Pe', '2P': '82-2Pe', '1J': '83-1Jn', '2J': '84-2Jn', '3J': '85-3Jn', 'Jd': '86-Jud'}
URL = 'https://raw.githubusercontent.com/morphgnt/sblgnt/master/{}-morphgnt.txt'
URL_ST = 'https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.js'
SALIDA = os.path.join(DIR, 'pedro_judas_griego.json')
def nfc(s): return unicodedata.normalize('NFC', s)
def sin_acentos(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.category(c).startswith('M')).replace('ς', 'σ')
def clave(lib, c, v): return f'{lib} {v}' if len(U.VV[lib]) == 1 else f'{lib} {c}:{v}'
def construir():
    s = urllib.request.urlopen(URL_ST, timeout=60).read().decode('utf-8')
    st = json.loads(s[s.index('{'):s.rindex('}') + 1])
    por_lema = {}
    for k, v in st.items(): por_lema.setdefault(sin_acentos(v.get('lemma', '')), []).append(k)
    out = {}; sin_strong = set()
    for lib, a in ARCH.items():
        t = urllib.request.urlopen(URL.format(a), timeout=60).read().decode('utf-8')
        for l in t.splitlines():
            ref, pos, parse, texto, palabra, norm, lema = l.split(' ')
            c, v = int(ref[2:4]), int(ref[4:6])
            cand = por_lema.get(sin_acentos(lema), []); sn = cand[0] if cand else ''
            if not sn: sin_strong.add(lema)
            out.setdefault(clave(lib, c, v), []).append({'t': nfc(texto), 'p': nfc(palabra), 'l': nfc(lema), 's': sn, 'm': pos + ' ' + parse})
    lex = {k: {'lemma': nfc(v.get('lemma', '')), 'xlit': v.get('translit', ''), 'def': v.get('strongs_def', ''), 'kjv': v.get('kjv_def', '')} for k, v in st.items()}
    json.dump({'versiculos': out, 'lexico': lex}, open(SALIDA, 'w'), ensure_ascii=False, separators=(',', ':'))
    falt = [U.cv(i) for i in range(1, U.TOTAL + 1) if U.cv(i) not in out]
    print('versículos', len(out), 'de', U.TOTAL, '| faltan', falt[:10], '| palabras', sum(len(v) for v in out.values()), '| lemas sin Strong', len(sin_strong))
def cargar(): return json.load(open(SALIDA))
def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    if a[0] == '--construir': construir(); return
    D = cargar(); V, L = D['versiculos'], D['lexico']
    if a[0] == '--buscar':
        q = sin_acentos(a[1]); print([k for k, ws in V.items() if any(sin_acentos(w['l']) == q or sin_acentos(w['p']) == q for w in ws)]); return
    r0 = U.rango(a[0]); r1 = U.rango(a[1]) if len(a) > 1 else r0
    for i in range(r0[0], r1[1] + 1):
        k = U.cv(i); print(k, ' '.join(w['t'] for w in V.get(k, [])))
        for w in V.get(k, []):
            e = L.get(w['s'], {}); print(f"   {w['p']}\t{w['l']}\t{w['s']}\t{e.get('xlit','')}\t{(e.get('def') or '')[:70]}")
if __name__ == '__main__': main()
