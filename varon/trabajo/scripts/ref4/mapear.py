import json,glob,os,re,sys,collections
from sklearn.feature_extraction.text import TfidfVectorizer
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
det={int(k):v for k,v in json.load(open(f'{V}/plan/dias_plan.json')).items()}
def flat(x):
    if isinstance(x,str): return x
    if isinstance(x,dict): return ' '.join(flat(v) for k,v in x.items() if k not in('fuente','refs'))
    if isinstance(x,list): return ' '.join(flat(v) for v in x)
    return ''
dias={}
for f in sorted(glob.glob(f'{V}/dias/dia_*.json')):
    d=json.load(open(f));n=int(d['dia']);dias[n]=d
tx={n:flat({k:d[k] for k in ('titulo','bajada','apartados','modelo','para_vivir','interpretaciones','profundizar') if k in d}) for n,d in dias.items()}
notas=[]
for f in sorted(glob.glob(f'{V}/notas/r_*.json'))+sorted(glob.glob(f'{V}/notas/q_*.json')):
    b=os.path.basename(f)[:-5]
    try: d=json.load(open(f))['notas']
    except Exception as e: print('ERROR',f,e);continue
    for i,n in enumerate(d): n['id']=f'{b}#{i+1}';notas.append(n)
ds=sorted(dias)
vec=TfidfVectorizer(sublinear_tf=True,min_df=2,max_df=0.5)
X=vec.fit_transform([tx[n] for n in ds]+[n['titulo']+' '+n['subtema']+' '+n['contenido'] for n in notas])
D=X[:len(ds)];N=X[len(ds):]
S=(N@D.T).toarray()
parte={n:det[n]['parte'] for n in ds if n in det}
res=[]
for i,n in enumerate(notas):
    mis=[j for j,d in enumerate(ds) if parte.get(d)==n['seccion']]
    cand=sorted(mis,key=lambda j:-S[i,j])[:3] if mis else []
    glob_best=max(range(len(ds)),key=lambda j:S[i,j])
    res.append({'id':n['id'],'seccion':n['seccion'],'imp':n['importancia'],'sub':n['subtema'],'tit':n['titulo'],
                'dias':[(ds[j],round(float(S[i,j]),3)) for j in cand],'mejor_global':(ds[glob_best],round(float(S[i,glob_best]),3))})
json.dump(res,open('mapa_ref4.json','w'),ensure_ascii=False)
import numpy as np
b=[r['dias'][0][1] if r['dias'] else 0 for r in res]
print(len(res),'notas; sim mejor-día-misma-sección: mediana',round(float(np.median(b)),3),'p25',round(float(np.percentile(b,25)),3))
