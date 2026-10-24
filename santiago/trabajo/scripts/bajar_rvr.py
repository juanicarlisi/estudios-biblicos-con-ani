#!/usr/bin/env python3
"""Baja Santiago en la Reina-Valera 1960 desde BibleGateway, lo cotejo contra una segunda fuente (bolls.life, RV1960)
y deja santiago/trabajo/biblia/rvr1960_santiago.json con {"texto": {cap: {verso: texto}}}.

Texto bíblico: Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.
Se usa dentro del tope de citas (menos de 500 versículos en total) y siempre con esa leyenda. No se guardan los títulos
de sección de la edición (son parte de la edición, no del texto bíblico).
"""
import json, os, re, subprocess, sys, time, unicodedata
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(__file__))
import config as C

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
CACHE = os.path.join(C.TMP, 'biblia')
os.makedirs(os.path.join(CACHE, 'bg'), exist_ok=True)
os.makedirs(os.path.join(CACHE, 'bolls'), exist_ok=True)


class P(HTMLParser):
    def __init__(s, c):
        super().__init__(); s.c = c; s.stack = []; s.verses = {}; s.skip = 0; s.inh = 0
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); cls = a.get('class', '') or ''
        m = re.search(r'\bJas-%d-(\d+)\b' % s.c, cls)
        if tag == 'h3':
            s.inh += 1; s.stack.append(('h3', None)); return
        if tag == 'span' and m and 'text' in cls.split():
            v = int(m.group(1))
            if v in s.verses and s.verses[v].strip():
                s.verses[v] += '\n'
            s.stack.append(('verse', v)); return
        if tag == 'sup' or (tag == 'span' and 'chapternum' in cls) or (tag == 'div' and ('footnotes' in cls or 'crossrefs' in cls)):
            s.stack.append(('skip', None)); s.skip += 1; return
        s.stack.append((tag, None))
    def handle_endtag(s, tag):
        if not s.stack:
            return
        kind, v = s.stack.pop()
        if kind == 'skip':
            s.skip -= 1
        if kind == 'h3':
            s.inh -= 1
    def handle_data(s, d):
        if s.skip or s.inh:
            return
        vs = [v for k, v in s.stack if k == 'verse']
        if vs:
            s.verses[vs[-1]] = s.verses.get(vs[-1], '') + d


def bajar_bg():
    res = {}
    for c in range(1, 6):
        fn = os.path.join(CACHE, 'bg', f'stg{c}.html')
        if not os.path.exists(fn) or os.path.getsize(fn) < 50000:
            subprocess.run(['curl', '-sS', '-A', UA, f'https://www.biblegateway.com/passage/?search=Santiago%20{c}&version=RVR1960', '-o', fn])
            time.sleep(2)
        t = open(fn, errors='ignore').read()
        i = t.find('<div class="passage-text">'); j = t.find('<div class="footnotes">', i)
        p = P(c); p.feed(t[i:j if j > 0 else None])
        res[c] = {str(v): '\n'.join(re.sub(r'[ \t\r\xa0]+', ' ', l).strip() for l in txt.split('\n') if l.strip())
                  for v, txt in sorted(p.verses.items())}
    return res


def norm(s):
    s = re.sub(r'<[^>]+>', '', s); s = unicodedata.normalize('NFC', s).lower()
    return re.sub(r'[^a-záéíóúüñ]', '', s)


def cotejar(res):
    dif = 0
    for c in range(1, 6):
        fn = os.path.join(CACHE, 'bolls', f'{c}.json')
        if not os.path.exists(fn):
            subprocess.run(['curl', '-sS', f'https://bolls.life/get-chapter/RV1960/59/{c}/', '-o', fn]); time.sleep(0.5)
        b = {str(x['verse']): x['text'] for x in json.load(open(fn))}
        for v, t in res[c].items():
            if norm(t) != norm(b.get(v, '')):
                dif += 1
                print(f'  DIF {c}:{v}\n   BG: {t!r}\n   BO: {re.sub(r"<[^>]+>", "", b.get(v, ""))!r}')
    return dif


if __name__ == '__main__':
    res = bajar_bg()
    tot = 0
    for c in range(1, 6):
        n = len(res[c]); tot += n
        if n != C.V[c - 1] or sorted(map(int, res[c])) != list(range(1, n + 1)):
            print('DIF capítulo', c, n, C.V[c - 1])
    print('total versículos', tot, 'esperado', C.TOTAL_VERSICULOS)
    print('diferencias con la segunda fuente:', cotejar(res))
    destino = os.path.join(C.REPO_TRABAJO, 'biblia', 'rvr1960_santiago.json')
    json.dump({'version': 'RVR1960', 'leyenda': 'Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.',
               'texto': {str(c): res[c] for c in res}}, open(destino, 'w'), ensure_ascii=False, indent=0)
    print('escrito', destino)
    print(res[1]['1']); print(res[2]['26']); print(res[5]['20'])
