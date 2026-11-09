import json,os,subprocess,tempfile,glob,shutil
from concurrent.futures import ThreadPoolExecutor
r=json.load(open('ref4_huella.json'))
KEY=['McDowell','Enfoque-a-la-Familia','mites en el noviazgo','Padre_de_Huerfanos','Pecado_que_la','juan-calvino','mo decir no','Jes','Comienza Ahora','ANSIEDAD','Emociones-sujetas','1. Discipulado','Estrategia_Jetro','Armadura de Dios','qué es el hombre','El padre que yo quiero','Kent Hughes','Jonás - Justo','Jim George','matrimonio si importa','mites en el Matrimonio','acto matrimonial','Locos por Jes']
C=json.load(open('clas.json'));idx={m['rel']:i for i,m in enumerate(json.load(open('ref4_paginas.json')))}
todo=[m for m in r if m['chars']<20000 and m['hit']<5 and any(k.lower() in m['rel'].lower() for k in KEY)]
todo=[m for m in todo if m['rel'] in idx and C[str(idx[m['rel']])]['cat']=='A']
todo.sort(key=lambda m:m['size'])
print(len(todo),[m['rel'].split('/')[-1][:40] for m in todo])
def pag(p):
    n=0
    try:
        o=subprocess.run(['pdfinfo',p],capture_output=True,text=True).stdout
        n=int([l for l in o.splitlines() if l.startswith('Pages')][0].split()[1])
    except: pass
    return n
def ocr_page(a):
    p,i,d=a
    pre=f'{d}/pg{i:04d}_'
    os.environ['OMP_THREAD_LIMIT']='1'
    subprocess.run(['pdftoppm','-r','170','-gray','-f',str(i),'-l',str(i),'-png',p,pre],capture_output=True)
    png=glob.glob(pre+'*.png')
    if not png: return i,''
    t=subprocess.run(['tesseract',png[0],'-','-l','spa'],capture_output=True,text=True).stdout
    os.remove(png[0]);return i,t
for m in todo:
    out=f"ref4txt/{m['h']}.ocr.txt"
    if os.path.exists(out): continue
    p='/home/user/libros-referencia4/'+m['rel'];n=min(pag(p),700)
    d=tempfile.mkdtemp(dir='/tmp')
    with ThreadPoolExecutor(4) as ex: res=sorted(ex.map(ocr_page,[(p,i,d) for i in range(1,n+1)]))
    open(out,'w').write('\f'.join(t for _,t in res));shutil.rmtree(d,ignore_errors=True)
    print('ok',n,m['rel'].split('/')[-1][:50],flush=True)
