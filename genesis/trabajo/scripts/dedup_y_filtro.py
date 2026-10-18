import json,re,collections,hashlib
sel=json.load(open('indice/seleccion_niveles.json'))
idx=json.load(open('indice/indice_todo.json'))
def lineset(k):
    t=open(idx[k]['txt'],errors='ignore').read()
    L=[re.sub(r'\W+','',l.lower()) for l in t.split('\n')]
    return {hashlib.md5(l.encode()).hexdigest()[:12] for l in L if len(l)>45}
keys=sorted({x['k'] for x in sel['t1']}|{x['k'] for x in sel['t2']})
size={k:len(open(idx[k]['txt'],errors='ignore').read()) for k in keys}
sets={k:lineset(k) for k in keys}
drop={}
ks=sorted(keys,key=lambda k:-size[k])
for i,a in enumerate(ks):
    if a in drop: continue
    for b in ks[i+1:]:
        if b in drop: continue
        sa,sb=sets[a],sets[b]
        if not sb: continue
        ov=len(sa&sb)/len(sb)
        if ov>0.5: drop[b]=(a,round(ov,2))
print('duplicados descartados',len(drop))
for b,(a,ov) in list(drop.items())[:40]: print(' ',ov,b[:70],'⊂',a[:60])
def es_lista(t):
    refs=len(re.findall(r'\d{1,3}:\d{1,3}',t)); words=len(t.split())
    return words==0 or refs/words>0.12
t1=[x for x in sel['t1'] if x['k'] not in drop]
t2=[x for x in sel['t2'] if x['k'] not in drop and not es_lista(x['texto']) and len(x['texto'])>=400]
c1=sum(len(x['texto']) for x in t1); c2=sum(len(x['texto']) for x in t2)
print('nivel1',len(t1),c1,'| nivel2',len(t2),c2,'| total',c1+c2,'≈ bloques 60k',(c1+c2)//60000)
json.dump({'t1':t1,'t2':t2,'duplicados':drop},open('indice/seleccion_final.json','w'),ensure_ascii=False)
