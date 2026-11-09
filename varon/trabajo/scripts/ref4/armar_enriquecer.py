import json,glob,re,os,sys,unicodedata,collections
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
S='/tmp/claude-0/-home-user/446b7ea4-e7f3-5663-b395-6889a80e8fc5/scratchpad'
F=json.load(open(f'{V}/fuentes.json'))
def nrm(s):
    s=unicodedata.normalize('NFKD',s.lower());s=''.join(c for c in s if not unicodedata.combining(c))
    return ' '.join(re.findall(r'[a-z0-9]+',s))
notas={};btxt={}
for f in sorted(glob.glob(f'{V}/notas/[ro]_*.json')):
    b=f.split('/')[-1][:-5]
    if b.startswith('o_') and not os.path.exists(f'{S}/bloques/{b}.txt'): continue
    for i,n in enumerate(json.load(open(f))['notas'],1): notas[f'{b}#{i}']=n
    btxt[b]=nrm(open(f'{S}/bloques/{b}.txt',errors='ignore').read())
M=json.load(open(f'{S}/mapa_final.json'))['por_dia']
def fl(x):
    if isinstance(x,str):return x
    if isinstance(x,dict):return ' '.join(fl(v) for k,v in x.items() if k not in('fuentes','refs'))
    if isinstance(x,list):return ' '.join(fl(v) for v in x)
    return ''
def dia_txt(n):
    d=json.load(open(f'{V}/dias/dia_{n:03d}.json'))
    w=len(fl({k:d[k] for k in('entrada','apartados') if k in d}).split())
    L=[f"=== DÍA {n} · {d['titulo']} · palabras del cuerpo (entrada+apartados): {w} (tope 2600) ===",f"Bajada: {d['bajada']}",
       f"Lectura: {d['lectura']['pasaje']} | Versículos: "+'; '.join(v['ref'] for v in d.get('versiculos',[])),
       f"ENTRADA: {d['entrada']['texto']}"]
    for a,ap in enumerate(d.get('apartados',[])):
        L.append(f"APARTADO {a} «{ap['titulo']}»")
        for p,pa in enumerate(ap['parrafos']): L.append(f"  P{p}: {pa['texto']}")
        if ap.get('destacado'): L.append(f"  (destacado: {ap['destacado']['texto']})")
    for i,c in enumerate(d.get('citas',[])): L.append(f"CITA {i}: «{c['texto']}» — {c['autor']}, {c['obra']}")
    for i,c in enumerate(d.get('datos',[])): L.append(f"DATO {i}: {c['valor']} — {c['texto']}")
    if d.get('modelo'): L.append(f"MODELO: {d['modelo']['persona']} — {d['modelo']['texto']}")
    for i,c in enumerate(d.get('palabras',[])): L.append(f"PALABRA {i}: {c.get('translit','')} — {c['significado'][:120]}")
    for i,c in enumerate(d.get('interpretaciones',[])): L.append(f"INTERPRETACIÓN {i}: {c['tema']} → "+' | '.join(p['postura'][:90] for p in c['posturas']))
    for i,c in enumerate(d.get('conexiones',[])): L.append(f"CONEXIÓN {i}: {c['ref']} — {c['nota'][:140]}")
    for i,c in enumerate(d.get('para_vivir',[])): L.append(f"PARA_VIVIR {i}: {c['texto']}")
    for i,c in enumerate(d.get('profundizar',[])): L.append(f"PROFUNDIZAR {i}: {c['titulo']} — {c['texto'][:160]}…")
    return '\n'.join(L)
def nota_txt(i):
    n=notas[i];src=F.get(n['fuente'],{})
    L=[f"[{i}] (importancia {n['importancia']} · {n['tipo']} · {src.get('autor','?')}, {src.get('obra','?')}, pág. {n.get('pagina','')}) {n['titulo']}",n['contenido']]
    c=n.get('cita','')
    if c and nrm(c) in btxt[i.split('#')[0]]: L.append(f"Cita textual verificada: «{c}»")
    if n.get('refs'): L.append('Versículos: '+', '.join(n['refs']))
    if n.get('persona'): L.append('Persona: '+n['persona'])
    return '\n'.join(L)
def insumo_extra(n):
    ids=M[str(n)]
    return '\n\n## NOTAS NUEVAS (libros de REFERENCIA4)\n'+'\n'.join(nota_txt(i) for i in ids)+'\n'
if __name__=='__main__':
    # tier y grupos
    A=[];B=[]
    for d,L in sorted(M.items(),key=lambda x:int(x[0])):
        imps=[notas[i]['importancia'] for i in L if i in notas]
        (A if (len(L)>=3 or 3 in imps) else B).append(int(d))
    grupos=[]
    for lst,tam,t in ((A,6,'A'),(B,10,'B')):
        for k in range(0,len(lst),tam): grupos.append((f'{t}{k//tam+1:02d}',lst[k:k+tam]))
    idx={}
    for g,ds in grupos:
        with open(f'{S}/enr/in_{g}.txt','w') as fh:
            for d in ds: fh.write(dia_txt(d)+'\n\n# NOTAS NUEVAS ASIGNADAS AL DÍA %d\n'%d+'\n'.join(nota_txt(i) for i in M[str(d)])+'\n\n\n')
        idx[g]=ds
    json.dump(idx,open(f'{S}/enr/grupos.json','w'))
    print(len(grupos),'grupos',{g:len(d) for g,d in grupos[:3]},'A:',len(A),'B:',len(B))
    tot=sum(os.path.getsize(f'{S}/enr/in_{g}.txt') for g,_ in grupos);print(tot//4000,'k tokens de insumo total')
