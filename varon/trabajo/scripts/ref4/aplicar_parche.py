import json,sys,os,re,copy
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
def fl(x):
    if isinstance(x,str):return x
    if isinstance(x,dict):return ' '.join(fl(v) for k,v in x.items() if k not in('fuentes','refs'))
    if isinstance(x,list):return ' '.join(fl(v) for v in x)
    return ''
def cuerpo(d): return len(fl({k:d[k] for k in('entrada','apartados') if k in d}).split())
def aplicar(parche_file):
    P=json.load(open(parche_file))['dias'];res=[]
    for k,p in P.items():
        n=int(k);fn=f'{V}/dias/dia_{n:03d}.json'
        d=json.load(open(fn));orig=cuerpo(d);log=[]
        for campo,lst in p.get('agregar',{}).items():
            if not isinstance(lst,list) or not lst: continue
            d.setdefault(campo,[]);d[campo]+=lst;log.append(f'+{len(lst)} {campo}')
        for campo,v in p.get('reemplazar',{}).items():
            if v: d[campo]=v;log.append(f'reemp {campo}')
        # insertar de atrás hacia adelante para no correr índices
        ins=sorted(p.get('insertar_parrafos',[]),key=lambda x:(x['apartado'],x['despues_de']),reverse=True)
        for it in ins:
            try:
                d['apartados'][it['apartado']]['parrafos'].insert(it['despues_de']+1,{'texto':it['texto'],'fuentes':it['fuentes']});log.append('+párrafo')
            except Exception as e: log.append(f'ERR insertar {e}')
        if cuerpo(d)>2600:
            res.append((n,'RECHAZADO cuerpo %d palabras'%cuerpo(d)));continue
        if p.get('no_incorporadas'): d['notas_no_usadas']=(d.get('notas_no_usadas','')+' | R4: '+p['no_incorporadas']).strip(' |')
        json.dump(d,open(fn,'w'),ensure_ascii=False,indent=1)
        res.append((n,'%d→%d palabras; '%(orig,cuerpo(d))+', '.join(log)))
    return res
if __name__=='__main__':
    for f in sys.argv[1:]:
        for r in aplicar(f): print(f.split('/')[-1],r)
