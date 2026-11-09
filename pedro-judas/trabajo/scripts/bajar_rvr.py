#!/usr/bin/env python3
"""Baja la RVR1960 de 1 Pedro a Judas (BibleGateway) a SCRATCH/biblia/rvr1960_pedro_judas.json (NO se commitea).
Forma: {"texto": {"1P": {"1": {"1": "..."}}}, "titulos": {...}}. Adaptado de apocalipsis/trabajo/scripts/bajar_rvr.py."""
import re, json, time, subprocess, os, sys
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
OSIS = {'1P': ('1Pet', '1 Pedro'), '2P': ('2Pet', '2 Pedro'), '1J': ('1John', '1 Juan'), '2J': ('2John', '2 Juan'), '3J': ('3John', '3 Juan'), 'Jd': ('Jude', 'Judas')}
class P(HTMLParser):
    def __init__(s, osis, c):
        super().__init__(); s.pat = re.compile(r'\b%s-%d-(\d+)\b' % (osis, c)); s.stack = []; s.verses = {}; s.headings = {}; s.skip = 0; s.inh = False; s.htxt = ''; s.lastv = 0
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); cls = a.get('class', '') or ''
        m = s.pat.search(cls)
        if tag == 'span' and m and 'text' in cls.split():
            v = int(m.group(1))
            if v in s.verses and s.verses[v].strip(): s.verses[v] += '\n'
            s.stack.append(('verse', v)); return
        if tag == 'sup' or (tag == 'span' and 'chapternum' in cls) or (tag == 'div' and ('footnotes' in cls or 'crossrefs' in cls)):
            s.stack.append(('skip', None)); s.skip += 1; return
        if tag == 'h3': s.inh = True; s.htxt = ''
        s.stack.append((tag, None))
    def handle_endtag(s, tag):
        if tag == 'h3' and s.inh: s.inh = False; s.headings[s.lastv + 1] = s.htxt.strip()
        if not s.stack: return
        kind, v = s.stack.pop()
        if kind == 'skip': s.skip -= 1
        if kind == 'verse': s.lastv = v
    def handle_data(s, d):
        if s.inh and not s.skip: s.htxt += d; return
        if s.skip: return
        vs = [v for k, v in s.stack if k == 'verse']
        if vs: s.verses[vs[-1]] = s.verses.get(vs[-1], '') + d
D = S + '/biblia/bg_pj'; os.makedirs(D, exist_ok=True)
res = {}; tit = {}; mal = 0
for lib, caps in U.VV.items():
    osis, nombre = OSIS[lib]; res[lib] = {}; tit[lib] = {}
    for c in range(1, len(caps) + 1):
        fn = f'{D}/{osis}{c}.html'
        if not os.path.exists(fn) or os.path.getsize(fn) < 50000:
            q = nombre.replace(' ', '%20') + ('%20' + str(c) if len(caps) > 1 else '')
            subprocess.run(['curl', '-sS', '-A', UA, f'https://www.biblegateway.com/passage/?search={q}&version=RVR1960', '-o', fn]); time.sleep(2)
        t = open(fn).read(); i = t.find('<div class="passage-text">'); j = t.find('<div class="footnotes">', i)
        p = P(osis, c); p.feed(t[i:j if j > 0 else None])
        res[lib][str(c)] = {str(v): '\n'.join(re.sub(r'[ \t\r\xa0]+', ' ', l).strip() for l in x.split('\n') if l.strip()) for v, x in sorted(p.verses.items())}
        tit[lib][str(c)] = p.headings
        n = len(res[lib][str(c)])
        if n != caps[c - 1]: print('DIF', lib, c, n, caps[c - 1]); mal += 1
json.dump({'texto': res, 'titulos': tit}, open(S + '/biblia/rvr1960_pedro_judas.json', 'w'), ensure_ascii=False, indent=0)
print('total', sum(len(v) for l in res.values() for v in l.values()), 'capítulos con diferencias', mal)
print(res['1P']['1']['1']); print(res['Jd']['1']['25'])
