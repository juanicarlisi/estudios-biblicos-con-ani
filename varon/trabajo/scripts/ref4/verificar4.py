import sys,subprocess,json,os
sys.path.insert(0,'/tmp/claude-0/-home-user/446b7ea4-e7f3-5663-b395-6889a80e8fc5/scratchpad')
import armar_enriquecer as AE
SC='/home/user/trabajo/varon/scripts'
dias=[int(x) for x in sys.argv[1:]]
for d in dias:
    subprocess.run(['python3','insumos.py',str(d)],cwd=SC,capture_output=True)
    if str(d) in AE.M:
        p=f'/home/user/trabajo/varon/insumos/dia_{d:03d}.txt'
        open(p,'a').write(AE.insumo_extra(d))
r=subprocess.run(['python3','verificar_dia.py','--dias']+[str(d) for d in dias],cwd=SC,capture_output=True,text=True)
print(r.stdout[-600:],r.stderr[-300:])
for d in dias:
    f=f'/home/user/trabajo/varon/revision/verif/dia_{d:03d}.json'
    if os.path.exists(f):
        v=json.load(open(f))
        if not v['ok'] or v.get('flags'): print(d,'FLAGS',len(v['flags']),[ (x['ruta'],x['tipo']) for x in v['flags'][:6]])
