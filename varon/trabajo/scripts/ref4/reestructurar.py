import json,glob,re,os,collections,shutil
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
S='/tmp/claude-0/-home-user/446b7ea4-e7f3-5663-b395-6889a80e8fc5/scratchpad'
det={int(k):v for k,v in json.load(open(f'{V}/plan/dias_plan.json')).items()}
plan=json.load(open(f'{V}/plan/plan.json'))
dias={}
for f in glob.glob(f'{V}/dias/dia_*.json'):
    d=json.load(open(f));dias[int(d['dia'])]=d
# 1) propuestas
props=[]
for f in sorted(glob.glob(f'{S}/nd/prop_*.json')):
    for n in json.load(open(f))['nuevos']:
        n['parte']=n.get('parte') or json.load(open(f))['parte'];props.append(n)
for p in props: assert det[p['despues_del_dia']]['parte']==p['parte'],p
props.sort(key=lambda p:(p['despues_del_dia']))
# 2) mapa viejo->nuevo
despues=collections.Counter(p['despues_del_dia'] for p in props)
def nuevo(d): return d+sum(1 for p in props if p['despues_del_dia']<d)
orden=collections.Counter()
for p in props:
    k=orden[p['despues_del_dia']];orden[p['despues_del_dia']]+=1
    p['dia_nuevo']=nuevo(p['despues_del_dia'])+1+k
mapa={d:nuevo(d) for d in range(1,513)}
# 3) extraer ítems movidos
usado=set();movidos={}
for p in props:
    its=[]
    for ref in p['items']:
        d,j=map(int,ref.split(':'))
        if (d,j) in usado: continue
        usado.add((d,j));its.append((d,j))
    p['items_ok']=its
REF=re.compile(r'(?i)\b(d[ií]as?)(\s+)(\d{1,3}(?:\s*(?:,|y|e|a|al|-|–)\s*\d{1,3})*)')
def remap_txt(s):
    def sub(m):
        g=re.sub(r'\d+',lambda x:str(mapa.get(int(x.group(0)),int(x.group(0)))) if 1<=int(x.group(0))<=512 else x.group(0),m.group(3))
        return m.group(1)+m.group(2)+g
    return REF.sub(sub,s)
def walk(x):
    if isinstance(x,str): return remap_txt(x)
    if isinstance(x,dict): return {k:(v if k=='fuentes' else walk(v)) for k,v in x.items()}
    if isinstance(x,list): return [walk(v) for v in x]
    return x
for p in props:
    p['items_texto']=[{'dia_orig':d,'titulo':dias[d]['profundizar'][j]['titulo'],'texto':walk(dias[d]['profundizar'][j]['texto']),'fuentes':dias[d]['profundizar'][j].get('fuentes',[])} for d,j in p['items_ok']]
# 4) quitar ítems de los días de origen
quitar=collections.defaultdict(list)
for d,j in usado: quitar[d].append(j)
for d,js in quitar.items():
    for j in sorted(js,reverse=True): dias[d]['profundizar'].pop(j)
# 5) remapeo de referencias de día en todos los textos y 'dia'
for d in list(dias): dias[d]=walk(dias[d]);dias[d]['dia']=mapa[d]
# 6) nota «sigue en el día N» en los días de origen
for p in props:
    srcs=sorted({d for d,_ in p['items_ok']})
    for d in srcs:
        dias[d]['profundizar'].append({'titulo':f"Este tema sigue en el día {p['dia_nuevo']}",'texto':f"El material que antes estaba acá sobre «{p['titulo']}» ahora tiene su propio día: el día {p['dia_nuevo']}. Si este tema te toca, seguí por ahí.",'fuentes':[]})
# 7) escribir días renumerados (de mayor a menor)
for f in glob.glob(f'{V}/dias/dia_*.json'): os.remove(f)
for d,x in dias.items(): json.dump(x,open(f'{V}/dias/dia_{x["dia"]:03d}.json','w'),ensure_ascii=False,indent=1)
# 8) plan
newplan=[];dp={}
for d in range(1,513):
    e=dict(plan[d-1]);e['dia']=mapa[d];newplan.append(e)
    x=dict(det[d]);x['dia']=mapa[d];dp[mapa[d]]=x
for p in props:
    e={'dia':p['dia_nuevo'],'parte':p['parte'],'titulo':p['titulo']};newplan.append(e)
    dp[p['dia_nuevo']]={'titulo':p['titulo'],'objetivo':p['objetivo'],'contenido':p['objetivo'],'lectura':p['lectura'],'grupos':[],'web':[],'dia':p['dia_nuevo'],'parte':p['parte'],'n_notas':0,'enfoque':[],'nuevo':True}
newplan.sort(key=lambda e:e['dia'])
assert [e['dia'] for e in newplan]==list(range(1,len(newplan)+1)),len(newplan)
json.dump(newplan,open(f'{V}/plan/plan.json','w'),ensure_ascii=False,indent=1)
json.dump({str(k):dp[k] for k in sorted(dp)},open(f'{V}/plan/dias_plan.json','w'),ensure_ascii=False,indent=1)
json.dump({'props':props,'mapa':mapa},open(f'{S}/nuevos.json','w'),ensure_ascii=False)
os.makedirs(f'{V}/ref4',exist_ok=True)
json.dump({'nuevos':[{k:p[k] for k in('dia_nuevo','parte','titulo','objetivo','lectura','despues_del_dia')} for p in props],'mapa_viejo_a_nuevo':mapa},open(f'{V}/ref4/dias_nuevos.json','w'),ensure_ascii=False,indent=1)
print(len(props),'días nuevos;',len(newplan),'días en el plan;',len(usado),'ítems movidos')
