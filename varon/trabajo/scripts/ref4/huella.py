import json,glob,re,unicodedata,collections,os
def norm(s):
    s=unicodedata.normalize('NFKD',s.lower());s=''.join(c for c in s if not unicodedata.combining(c))
    return re.findall(r'[a-z0-9]+',s)
N=10
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
fuentes=json.load(open(f'{V}/fuentes.json'))
sh=collections.defaultdict(set)   # shingle -> {fuente}
nc=0
for f in glob.glob(f'{V}/notas/*.json'):
    d=json.load(open(f))
    for n in d.get('notas',[]):
        c=n.get('cita','')
        w=norm(c)
        if len(w)<N+2: continue
        nc+=1
        for i in range(0,len(w)-N+1): sh[hash(tuple(w[i:i+N]))].add(n.get('fuente'))
print('citas',nc,'shingles',len(sh))
man=json.load(open('ref4_puntajes.json'))
res=[]
for m in man:
    txt=open(f"ref4txt/{m['h']}.txt",errors='ignore').read()
    w=norm(txt);hits=collections.Counter()
    for i in range(0,len(w)-N+1):
        s=sh.get(hash(tuple(w[i:i+N])))
        if s:
            for x in s: hits[x]+=1
    top=hits.most_common(1)
    m['hit']=top[0][1] if top else 0
    m['hit_fuente']=top[0][0] if top else None
    res.append(m)
json.dump(res,open('ref4_huella.json','w'),ensure_ascii=False)
import statistics
print(sum(1 for m in res if m['hit']>=20),'libros ya usados (>=20 coincidencias);',sum(1 for m in res if 3<=m['hit']<20),'dudosos;',sum(1 for m in res if m['hit']<3),'sin huella')
