import json,re,os,sys,glob
sys.path.insert(0,'/home/user/estudios-biblicos-con-ani/varon/trabajo/scripts')
from puntajes import paginas
P=json.load(open('ref4_paginas.json'));C=json.load(open('clas.json'))
C['309']['cat']='A';C['309']['autor']='RBC Ministries (Radio Bible Class)';C['309']['obra']='Cuando la mirada de un hombre se desvía'
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
F=json.load(open(f'{V}/fuentes.json'))
prefijo=sys.argv[1] if len(sys.argv)>1 else 'r'   # r = texto, o = OCR
solo=set(map(int,sys.argv[2].split(','))) if len(sys.argv)>2 else None
def key(s): return re.sub(r'[^a-z]','',s.lower())[:22]
n0=max([int(k[2:]) for k in F if k.startswith('R4')]+[4000])
seen=set();libros=[]
for i,m in enumerate(P):
    c=C[str(i)]
    if c['cat']!='A' or key(c['obra']) in seen: continue
    seen.add(key(c['obra']))
    if solo is not None and i not in solo: continue
    is_ocr=m['txt'].endswith('.ocr.txt')
    if solo is None and is_ocr: continue
    mujer=m['rel'].startswith('nuevos/05') or re.search(r'(?i)mujer|madre|joven conforme|esposa|ester|rut|rahab|elisabet|nancy',m['rel'].split('/')[-1]) is not None
    th=35 if mujer else 20
    pg=[x for x in m['pags'] if x[1]>=th]
    if not pg: continue
    libros.append((i,m,pg))
add={};bl=[];cur=[];sz=0
def cerrar():
    global cur,sz
    if cur: bl.append(cur);cur=[];sz=0
for i,m,pg in libros:
    clave=f"ref4:{m['rel']}"
    ya=[k for k,v in F.items() if v['clave']==clave]
    if ya: rid=ya[0]
    else:
        n0+=1;rid=f'R{n0}'
        F[rid]={'clave':clave,'fuente':'ref4','archivo':m['rel'],'autor':C[str(i)]['autor'],'obra':C[str(i)]['obra']}
    txt=open(m['txt'],errors='ignore').read();pgs=paginas(txt)
    for (p,s,ch) in pg:
        t=pgs[p-1].strip()
        if sz+len(t)>110000: cerrar()
        cur.append((rid,p,t));sz+=len(t)+30
cerrar()
base=len(glob.glob(f'bloques/{prefijo}_*.txt'))
out=[]
for k,b in enumerate(bl,1):
    ids=sorted({r for r,_,_ in b})
    head='FUENTES:\n'+'\n'.join(f"{r}: {F[r]['autor']} — {F[r]['obra']}" for r in ids)+'\n\n'
    body=''.join(f"=== [{r} | pág. {p}] ===\n{t}\n\n" for r,p,t in b)
    name=f'{prefijo}_{base+k:03d}'
    open(f'bloques/{name}.txt','w').write(head+body);out.append((name,len(head+body)))
json.dump(F,open(f'{V}/fuentes.json','w'),ensure_ascii=False,indent=1)
print(len(libros),'libros',len(bl),'bloques',sum(s for _,s in out)//1000,'k')
