import json,glob,collections
base=glob.glob('/root/.claude/projects/**/subagents/workflows/wf_c5b57a4c-120/journal.jsonl',recursive=True)[0]
labels={};libros=[]
for line in open(base):
    ev=json.loads(line)
    if ev.get('type')=='started': labels[ev['agentId']]=ev.get('label','')
    elif ev.get('type')=='result':
        v=ev.get('result')
        if isinstance(v,str):
            try: v=json.loads(v)
            except: continue
        if isinstance(v,dict) and 'libros' in v: libros+=v['libros']
fichas={f['path']:f for f in json.load(open('clasif/fichas.json'))}
vistos=set();out=[]
for l in libros:
    if l['path'] in vistos: continue
    vistos.add(l['path']); out.append(l)
falt=[p for p in fichas if p not in vistos]
json.dump(out,open('clasif/clasificacion.json','w'),ensure_ascii=False,indent=1)
c=collections.Counter(l['categoria'] for l in out)
print('clasificados',len(out),'faltan',len(falt),falt[:5]); print(c)
print('confianza',collections.Counter((l['categoria'],l['confianza']) for l in out))
