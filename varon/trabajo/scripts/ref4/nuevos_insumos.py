import json,sys,os,re
V='/home/user/trabajo/varon'
sys.path.insert(0,f'{V}/scripts')
from grupos_entrada import notas,VACIAS
from sklearn.feature_extraction.text import TfidfVectorizer
S='/tmp/claude-0/-home-user/446b7ea4-e7f3-5663-b395-6889a80e8fc5/scratchpad'
props=json.load(open(f'{S}/nuevos.json'))['props']
plan=json.load(open(f'{V}/plan/plan.json'))
det={int(k):v for k,v in json.load(open(f'{V}/plan/dias_plan.json')).items()}
partes={p['id']:p for p in json.load(open(f'{V}/plan/partes.json'))}
fuentes=json.load(open(f'{V}/bloques/_fuentes.json'))
citas=json.load(open(f'{V}/revision/citas.json')) if os.path.exists(f'{V}/revision/citas.json') else {}
todas=dict(notas())
ids=[i for i,n in todas.items()]
corpus=[todas[i].get('titulo','')+' '+todas[i].get('subtema','')+' '+todas[i].get('contenido','')[:600] for i in ids]
vec=TfidfVectorizer(stop_words=list(VACIAS),sublinear_tf=True,min_df=2);X=vec.fit_transform(corpus)
total=len(plan)
def nota_txt(i):
    n=todas[i];src=fuentes.get(n.get('fuente'),{});imp=n.get('importancia',2)
    out=[f"[{i}] (importancia {imp} · {n.get('tipo')} · {src.get('autor','?')}, {src.get('obra','?')}, pág. {n.get('pagina','')}) {n.get('titulo','')}",n.get('contenido','')]
    cv=citas.get(i,{})
    if n.get('cita') and cv.get('estado') in('ok','ocr'): out.append(f"Cita textual: «{n['cita']}»")
    if n.get('refs'): out.append('Versículos: '+', '.join(n['refs']))
    if n.get('persona'): out.append('Persona: '+n['persona'])
    return out
resumen=[]
for p in props:
    d=p['dia_nuevo'];x=det[d];pt=partes[x['parte']]
    cit=[]
    for it in p['items_texto']:
        for f in it['fuentes']:
            if f in todas and f not in cit: cit.append(f)
    q=vec.transform([p['titulo']+' '+p['objetivo']+' '+' '.join(it['titulo']+' '+it['texto'] for it in p['items_texto'])])
    sim=(X@q.T).toarray().ravel()
    # misma sección (parte) y no citadas
    cand=[(sim[k],ids[k]) for k in range(len(ids)) if ids[k] not in cit and todas[ids[k]].get('seccion')==x['parte'] and todas[ids[k]].get('importancia',2)>=2 and sim[k]>0.08]
    extra=[i for _,i in sorted(cand,reverse=True)[:14]]
    dias_parte=[e for e in plan if e['parte']==x['parte']]
    cab=[f"# DÍA {d} de {total} · Parte {pt['numero']}: {pt['titulo']}",f"Título previsto: {x['titulo']}",f"Objetivo: {x['objetivo']}",f"Qué cubre: {x['contenido']}",f"Lectura prevista: {x['lectura']}",'',f"## Esta parte ({pt['bajada']})"]
    for e in dias_parte:
        marca='  ← HOY' if e['dia']==d else ''
        extra_t=f" — {det[e['dia']]['objetivo']}" if abs(e['dia']-d)==1 else ''
        cab.append(f"- Día {e['dia']}: {e['titulo']}{extra_t}{marca}")
    cab+=['','## ENFOQUE PROPIO DE ESTE DÍA (día nuevo, creado porque el material de este tema no cabía en los días vecinos)',
      '- Desarrollá este tema como día completo y propio; los días vecinos lo tocan de pasada y no lo repiten.',
      '- Ejes sugeridos (salen de los ítems de «profundizar» que se movieron acá): '+' / '.join(it['titulo'] for it in p['items_texto'])]
    out=cab+['','## NOTAS (primero las que respaldaban los ejes; después otras de la misma parte sobre el tema)']
    out+=['','### Notas centrales']
    for i in cit: out+=nota_txt(i)
    out+=['','### Notas relacionadas de la misma parte']
    for i in extra: out+=nota_txt(i)
    txt='\n'.join(out)+'\n'
    open(f'{V}/insumos/dia_{d:03d}.txt','w').write(txt)
    resumen.append((d,len(cit),len(extra),len(txt)))
for r in resumen: print(r)
