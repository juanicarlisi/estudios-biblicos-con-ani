#!/usr/bin/env python3
"""Arma una ficha por archivo de REF3 (nombre, portada, datos de edición) para clasificar autores."""
import json, os, re, subprocess, tempfile
REPO='/home/user/libros-referencia3'; CORP='/home/user/trabajo/corpus_ref3'
recs=[json.loads(l) for l in open(f'{CORP}/_manifiesto.jsonl')]
recs=[r for r in recs if r['ext'] not in ('', '.md')]
recs.sort(key=lambda r:r['path'])
def ocr_primeras(sha):
    with tempfile.TemporaryDirectory(dir='/home/user/trabajo/tmp') as td:
        src=os.path.join(td,'in.pdf')
        with open(src,'wb') as f: subprocess.run(['git','-C',REPO,'cat-file','blob',sha],stdout=f)
        subprocess.run(['pdftoppm','-f','1','-l','4','-r','200','-gray','-png',src,os.path.join(td,'p')],capture_output=True)
        out=[]
        for img in sorted(x for x in os.listdir(td) if x.endswith('.png')):
            out.append(subprocess.run(['tesseract',os.path.join(td,img),'stdout','-l','spa'],capture_output=True,text=True).stdout)
        return '\n'.join(out)
fichas=[]
import hashlib
os.makedirs('/home/user/trabajo/clasif/cache',exist_ok=True)
for i,r in enumerate(recs,1):
    cf='/home/user/trabajo/clasif/cache/'+hashlib.md5(r['path'].encode()).hexdigest()+'.json'
    if os.path.exists(cf):
        fc=json.load(open(cf)); fc['id']=i; fichas.append(fc); continue
    txt=open(os.path.join(CORP,r['path']+'.txt'),errors='ignore').read() if os.path.exists(os.path.join(CORP,r['path']+'.txt')) else ''
    if r.get('escaneado') or len(txt.strip())<800:
        if r['ext']=='.pdf':
            txt=ocr_primeras(r['sha']); fuente='ocr'
        else: fuente='texto'
    else: fuente='texto'
    pags=txt.split('\f')
    inicio=re.sub(r'\s+',' ',' '.join(pags[:6]))[:3500]
    meta=[]
    for p in pags[:15]:
        for line in p.splitlines():
            if re.search(r'©|copyright|isbn|editorial|publicado|publicad[oa] por|traduc|edici[oó]n|impreso|t[ií]tulo original|originally published|published by',line,re.I):
                meta.append(line.strip())
    meta=' / '.join(dict.fromkeys(meta))[:1200]
    fc={'id':i,'path':r['path'],'paginas':r['pages'],'escaneado':bool(r.get('escaneado')),'fuente_texto':fuente,'inicio':inicio,'datos_edicion':meta}
    json.dump(fc,open(cf,'w'),ensure_ascii=False); fichas.append(fc)
    if i%50==0: print(i,flush=True)
json.dump(fichas,open('/home/user/trabajo/clasif/fichas.json','w'),ensure_ascii=False)
print(len(fichas),'fichas')
