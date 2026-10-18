"""Selecciona el texto de los libros confiables que trata Génesis, en dos niveles, y arma bloques para leer."""
import json,hashlib,re,os,sys
sys.path.insert(0,'/home/user/trabajo/scripts')
from indice_genesis import citas, RE_F
c={l['path']:l for l in json.load(open('clasif/clasificacion.json'))}
idx=json.load(open('indice/indice_todo.json'))
EXCL_BIB=['DICCIONARIOS','Barclay','Pikaza','Iafrancesco','Aproximaci','código del apocalipsis','Josué.pdf','05 - Génesis','Génesis parte 2','Desafios_para_Jóvenes','Judas - J. L. Flores','04 - NÚMEROS/Comentario Biblico Beacon','John MacArthur - Biblia de estudio','Walvoord']
def autor_de(k):
    if k.startswith('REF3/'): return c[k[5:]]['autor']
    return 'biblioteca'
vistos=set(); t1=[]; t2=[]
for k,v in idx.items():
    if k.startswith('REF3/'):
        l=c.get(k[5:])
        if not l or l['categoria']!='A': continue
    elif any(x in k for x in EXCL_BIB): continue
    txt=open(v['txt'],errors='ignore').read()
    h=hashlib.md5(re.sub(r'\s+','',txt[:200000]).encode()).hexdigest()
    if h in vistos: continue
    vistos.add(h)
    pags=txt.split('\f')
    sc={x['pag']:x['score'] for x in v['paginas']}
    # nivel 1: tramos de >=3 páginas seguidas con score>=6 (o 2 páginas con score>=12)
    fuertes=sorted(p for p,s in sc.items() if s>=6 and len(pags[p-1])<12000)
    runs=[];cur=[]
    for p in fuertes:
        if cur and p==cur[-1]+1: cur.append(p)
        else:
            if cur: runs.append(cur)
            cur=[p]
    if cur: runs.append(cur)
    usadas=set()
    for r in runs:
        if len(r)>=3 or (len(r)==2 and sum(sc[p] for p in r)>=24):
            for p in r: usadas.add(p)
            t1.append({'k':k,'pags':r,'texto':'\n'.join(f'--- [pág. PDF {p}] ---\n'+pags[p-1].strip() for p in r)})
    # nivel 2: ventanas de líneas alrededor de citas de Génesis fuera de los tramos del nivel 1
    for pn,p in enumerate(pags,1):
        if pn in usadas or pn not in sc: continue
        lines=p.split('\n'); marcas=[]
        for i,l in enumerate(lines):
            if citas(l) or len(RE_F.findall(l))>=2: marcas.append(i)
        if not marcas: continue
        win=set()
        for i in marcas:
            for j in range(max(0,i-6),min(len(lines),i+7)): win.add(j)
        segs=[];cur=[]
        for j in sorted(win):
            if cur and j!=cur[-1]+1: segs.append(cur); cur=[]
            cur.append(j)
        if cur: segs.append(cur)
        for s in segs:
            t=' '.join(lines[j].strip() for j in s)
            if len(t)>250: t2.append({'k':k,'pag':pn,'texto':t[:3000]})
c1=sum(len(x['texto']) for x in t1); c2=sum(len(x['texto']) for x in t2)
print('nivel 1: tramos',len(t1),'chars',c1,'| nivel 2: ventanas',len(t2),'chars',c2)
json.dump({'t1':t1,'t2':t2},open('indice/seleccion_niveles.json','w'),ensure_ascii=False)
import collections
cc=collections.Counter(x['k'] for x in t2); print('top nivel2',[(k[:60],n) for k,n in cc.most_common(12)])
cc=collections.Counter(); 
for x in t1: cc[x['k']]+=len(x['texto'])
print('top nivel1',[(k[:60],n) for k,n in cc.most_common(25)])
