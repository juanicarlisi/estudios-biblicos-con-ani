import os,subprocess,json,re
BASE='/home/user/biblioteca-estudios-biblicos/MATERIAL SOPORTE'
OUT='/home/user/trabajo/corpus_biblio/todo'
man=[]
vistos={}
for root,_,files in os.walk(BASE):
    for f in sorted(files):
        if not f.lower().endswith('.pdf'): continue
        p=os.path.join(root,f); rel=os.path.relpath(p,BASE)
        md5=subprocess.run(['md5sum',p],capture_output=True,text=True).stdout.split()[0]
        dst=os.path.join(OUT,rel+'.txt'); os.makedirs(os.path.dirname(dst),exist_ok=True)
        dup=vistos.get(md5)
        if not dup:
            vistos[md5]=rel
            if not os.path.exists(dst): subprocess.run(['pdftotext','-enc','UTF-8',p,dst],capture_output=True)
        info=subprocess.run(['pdfinfo',p],capture_output=True,text=True).stdout
        m=re.search(r'^Pages:\s+(\d+)',info,re.M); pages=int(m.group(1)) if m else 0
        chars=len(open(dst,errors='ignore').read()) if os.path.exists(dst) else 0
        man.append({'path':rel,'md5':md5,'duplicado_de':dup,'pages':pages,'chars':chars,'escaneado':(not dup) and pages>0 and chars/pages<300})
json.dump(man,open(OUT+'/_manifiesto.json','w'),ensure_ascii=False,indent=1)
u=[m for m in man if not m['duplicado_de']]
print('pdfs',len(man),'unicos',len(u),'escaneados',[ (m['path'],m['pages']) for m in u if m['escaneado']])
