import json,sys,collections
sys.path.insert(0,'/home/user/estudios-biblicos-con-ani/varon/trabajo/scripts')
from puntajes import RX,norm,paginas
man=json.load(open('ref4_manifest.json')) if len(sys.argv)<2 else json.load(open(sys.argv[1]))
out=[]
for m in man:
    f=f"ref4txt/{m['h']}.txt"
    try: txt=open(f,errors='ignore').read()
    except: continue
    pgs=paginas(txt);tot=collections.Counter();sc=0;util=0;chars=0
    for pg in pgs:
        if len(pg.strip())<200: continue
        t=norm(pg);chars+=len(pg);p=0
        for tema,w,rx in RX:
            k=len(rx.findall(t))
            if k: tot[tema]+=w*k;p+=w*k
        punt=p*3000/max(len(pg),800)
        if punt>=6: util+=1
    m.update(chars=chars,paginas=len(pgs),pag_utiles=util,dens=round(sum(tot.values())*3000/max(chars,1),1),temas=dict(tot.most_common(4)))
    out.append(m)
json.dump(out,open('ref4_puntajes.json','w'),ensure_ascii=False)
print(len(out))
