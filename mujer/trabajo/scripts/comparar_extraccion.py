#!/usr/bin/env python3
"""Compara dos corridas de extracción sobre los mismos bloques: cantidad de notas, importancia, citas textuales presentes en el bloque, cobertura de versículos."""
import json, glob, re, sys, unicodedata, collections
def nz(s): return re.sub(r'\s+', ' ', re.sub(r'[^\w]+', ' ', ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(c)))).strip()
def res(run):
    j = glob.glob(f'/root/.claude/projects/**/subagents/workflows/{run}/journal.jsonl', recursive=True)[0]; lab = {}; out = {}
    for l in open(j):
        e = json.loads(l)
        if e.get('type') == 'started': lab[e['agentId']] = e['label']
        elif e.get('type') == 'result' and lab.get(e['agentId'], '').startswith('extraer:'):
            v = e['result']; out[lab[e['agentId']][8:]] = json.loads(v) if isinstance(v, str) else v
    return out
for b in sorted(res(sys.argv[1])):
    txt = nz(open(f'/home/user/trabajo/mujer/bloques/{b}.txt', errors='ignore').read())
    for run in sys.argv[1:]:
        notas = res(run).get(b, {}).get('notas', [])
        citas = [n['cita'] for n in notas if n.get('cita')]
        ok = sum(1 for c in citas if nz(c) in txt)
        imp = collections.Counter(n['importancia'] for n in notas)
        chars = sum(len(n['contenido']) for n in notas)
        refs = len({r for n in notas for r in n.get('refs', [])})
        print(f'{b} {run[-7:]}: notas {len(notas)} | imp {dict(sorted(imp.items()))} | citas {ok}/{len(citas)} verificadas | texto notas {chars//1000}k | refs {refs}')
