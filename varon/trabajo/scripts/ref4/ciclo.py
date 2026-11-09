import sys,subprocess,json,os,shutil
S='/tmp/claude-0/-home-user/446b7ea4-e7f3-5663-b395-6889a80e8fc5/scratchpad'
sys.path.insert(0,S)
import armar_enriquecer as AE, aplicar_parche as AP
SC='/home/user/trabajo/varon/scripts';V='/home/user/trabajo/varon'
def verif(dias,extra):
    env=dict(os.environ,INSUMO_TOPE='400000')
    subprocess.run(['python3','insumos.py']+[str(d) for d in dias],cwd=SC,capture_output=True,env=env)
    if extra:
        for d in dias:
            if str(d) in AE.M: open(f'{V}/insumos/dia_{d:03d}.txt','a').write(AE.insumo_extra(d))
    subprocess.run(['python3','verificar_dia.py','--dias']+[str(d) for d in dias],cwd=SC,capture_output=True,env=env)
    out={}
    for d in dias:
        f=f'{V}/revision/verif/dia_{d:03d}.json'
        out[d]=json.load(open(f))['flags'] if os.path.exists(f) else []
    return out
def clave(x): return (x['ruta'],x['tipo'],x.get('detalle','')[:60])
g=sys.argv[1];patch=f'{S}/enr/out_{g}.json'
dias=[int(k) for k in json.load(open(patch))['dias']]
base=verif(dias,False)
for r in AP.aplicar(patch): print(r)
desp=verif(dias,True)
nuevos={}
for d in dias:
    b={clave(x) for x in base[d]}
    nuevos[d]=[x for x in desp[d] if clave(x) not in b]
print('base',{d:len(v) for d,v in base.items()},'después',{d:len(v) for d,v in desp.items()},'NUEVAS',{d:len(v) for d,v in nuevos.items()})
json.dump({'nuevas':nuevos,'base':base},open(f'{S}/enr/flags_{g}.json','w'),ensure_ascii=False)
