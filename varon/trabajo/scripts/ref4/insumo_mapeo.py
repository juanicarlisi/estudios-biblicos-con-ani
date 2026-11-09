import json,glob,os,re,sys
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
pref=sys.argv[1] if len(sys.argv)>1 else 'r'
det={int(k):v for k,v in json.load(open(f'{V}/plan/dias_plan.json')).items()}
partes={p['id']:p['titulo'] for p in json.load(open(f'{V}/plan/partes.json'))}
dias={}
for f in glob.glob(f'{V}/dias/dia_*.json'):
    d=json.load(open(f));dias[int(d['dia'])]=d
mapa={m['id']:m for m in json.load(open('mapa_ref4.json'))} if os.path.exists('mapa_ref4.json') else {}
por={}
for f in sorted(glob.glob(f'{V}/notas/{pref}_*.json')):
    b=os.path.basename(f)[:-5]
    for i,n in enumerate(json.load(open(f))['notas'],1):
        por.setdefault(n['seccion'],[]).append((f'{b}#{i}',n))
out={}
for s in sorted(por):
    L=[f"# PARTE {s}: {partes[s]} — índice de días del estudio (día | título | apartados)"]
    for n in sorted(d for d in dias if det.get(d,{}).get('parte')==s):
        d=dias[n];L.append(f"{n} | {d['titulo']} | "+'; '.join(a['titulo'] for a in d.get('apartados',[])))
    L.append(f"\n# NOTAS NUEVAS de la sección {s} (id | imp | tipo | título | subtema | resumen) — sugerencia automática entre []")
    for i,n in por[s]:
        m=mapa.get(i,{});sug=m.get('dias',[[0,0]])[0] if m.get('dias') else [0,0]
        c=re.sub(r'\s+',' ',n['contenido'])[:230]
        L.append(f"{i} | {n['importancia']} | {n['tipo']} | {n['titulo']} | {n['subtema']} | {c} [{sug[0]}]")
    open(f'mapeo/{pref}_parte_{s}.txt','w').write('\n'.join(L));out[s]=(len(por[s]),sum(len(x) for x in L)//4)
print(out)
