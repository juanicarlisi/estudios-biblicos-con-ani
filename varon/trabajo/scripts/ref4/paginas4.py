import json,sys,re,glob,os
sys.path.insert(0,'/home/user/estudios-biblicos-con-ani/varon/trabajo/scripts')
from puntajes import RX,norm,paginas
F=json.load(open('/home/user/estudios-biblicos-con-ani/varon/trabajo/fuentes.json'))
def tk(s):
    s=norm(s);return set(t for t in re.findall(r'[a-z0-9]+',s) if len(t)>3)
ftk={k:tk(v['archivo'].split('/')[-1]+' '+v.get('obra','')) for k,v in F.items()}
r=json.load(open('ref4_huella.json'))
out=[]
for m in r:
    fn=m['rel'].split('/')[-1]
    used=m['hit']>=20
    if 5<=m['hit']<20 and m['hit_fuente'] in ftk:
        a=tk(fn)
        used = len(a&ftk[m['hit_fuente']])/max(len(a),1)>=0.5
    m['usado']=used
    if used: continue
    f=f"ref4txt/{m['h']}.ocr.txt" if os.path.exists(f"ref4txt/{m['h']}.ocr.txt") else f"ref4txt/{m['h']}.txt"
    txt=open(f,errors='ignore').read();sc=[]
    for i,p in enumerate(paginas(txt),1):
        if len(p.strip())<200: continue
        t=norm(p);s=sum(w*len(rx.findall(t)) for _,w,rx in RX)*3000/max(len(p),800)
        sc.append((i,round(s,1),len(p)))
    m['pags']=sc;m['txt']=f;out.append(m)
json.dump(out,open('ref4_paginas.json','w'),ensure_ascii=False)
for th in (2,6,10,15):
    print(th,sum(1 for m in out for _,s,_ in m['pags'] if s>=th),sum(c for m in out for _,s,c in m['pags'] if s>=th)//1000,'k')
print(len(out),'libros nuevos (no usados)')
