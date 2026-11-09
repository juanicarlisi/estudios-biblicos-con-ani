import json,glob,collections,re
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
det={int(k):v for k,v in json.load(open(f'{V}/plan/dias_plan.json')).items()}
mapa={m['id']:m for m in json.load(open('mapa_ref4.json'))}
notas={}
for f in sorted(glob.glob(f'{V}/notas/r_*.json')):
    b=f.split('/')[-1][:-5]
    for i,n in enumerate(json.load(open(f))['notas'],1): notas[f'{b}#{i}']=n
asig={};nuevos=[];prob=collections.Counter()
for f in sorted(glob.glob('mapeo/res_*.json')):
    try: d=json.load(open(f))
    except Exception as e: print('ERROR',f,e);continue
    for k,v in d.get('asignaciones',{}).items():
        if k not in notas: prob['id_inexistente']+=1;continue
        asig[k]=str(v)
    for n in d.get('nuevos',[]): nuevos.append(n)
for k in notas:
    if k not in asig:
        prob['sin_asignar']+=1;s=mapa[k]['dias'][0][0] if mapa[k]['dias'] else None;asig[k]=str(s) if s else 'cub'
por=collections.defaultdict(list);cub=[];nv=collections.defaultdict(list)
for k,v in asig.items():
    sec=notas[k]['seccion']
    if v.isdigit():
        d=int(v)
        if d not in det or det[d]['parte']!=sec:
            prob['dia_fuera_de_parte']+=1
            s=mapa[k]['dias'][0][0] if mapa[k]['dias'] else None
            if d in det: pass
            else: d=s
        por[d].append(k)
    elif v=='cub': cub.append(k)
    elif v.startswith('n'): nv[(notas[k]['seccion'],v)].append(k)
    else: prob['otra:'+v]+=1;s=mapa[k]['dias'][0][0] if mapa[k]['dias'] else None;por[s].append(k)
print(len(notas),'notas;',len(asig),'asignadas;',dict(prob))
print('a días:',sum(len(v) for v in por.values()),'en',len(por),'días distintos; cub:',len(cub),'; nuevos:',{k:len(v) for k,v in nv.items()})
c=collections.Counter({d:len(v) for d,v in por.items()});print('top:',c.most_common(6))
print('días con ≥3:',sum(1 for v in c.values() if v>=3),'≥5:',sum(1 for v in c.values() if v>=5))
json.dump({'por_dia':{str(d):v for d,v in por.items()},'cub':cub,'nuevos_notas':{f'{a}:{b}':v for (a,b),v in nv.items()},'nuevos':nuevos},open('mapa_final.json','w'),ensure_ascii=False)
print(nuevos)
