import re,json
OUT='/home/user/trabajo/segmentos/biblio/'
sel=[]
for vol,fn in [('I','dbmh_1.txt'),('II','dbmh_2.txt')]:
    pags=open('/home/user/trabajo/corpus_biblio/'+fn,errors='ignore').read().split('\f')
    # reconstruir texto con marcas de página
    entradas=[];cur=None
    for pn,p in enumerate(pags,1):
        lines=p.split('\n')
        for i,l in enumerate(lines):
            prev_blank = (i==0) or (lines[i-1].strip()=='')
            m=re.match(r'^([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñüÁÉÍÓÚÑ\'’\-]+(?:[ ,][A-Za-záéíóúñüÁÉÍÓÚÑ\'’\-]+){0,3})\s\(',l) or re.match(r'^([A-ZÁÉÍÓÚÑ]{3,}(?:[ ,]+[A-ZÁÉÍÓÚÑ]{2,}){0,3})\.?\s*$',l)
            if prev_blank and m:
                cur={'vol':vol,'titulo':m.group(1).strip(),'pag':pn,'texto':''}; entradas.append(cur)
            if cur is not None: cur['texto']+=l+'\n'
    for e in entradas:
        g=len(re.findall(r'<01\d{4}>',e['texto']))
        e['citas_gn']=g
        if g>=1: sel.append(e)
print('entradas con citas de Génesis',len(sel), 'chars',sum(len(e['texto']) for e in sel))
sel.sort(key=lambda e:(e['vol'],e['pag']))
MAX=42000; trozos=[];cur='';n=0
for e in sel:
    b=f"=== [dbmh | Diccionario Bíblico Mundo Hispano, vol. {e['vol']} | PÁGINA PDF {e['pag']} | entrada: {e['titulo']}] ===\n{e['texto'].strip()}\n\n"
    if len(cur)+len(b)>MAX and cur:
        trozos.append(cur); cur=''
    cur+=b
if cur: trozos.append(cur)
idx=[]
for i,t in enumerate(trozos,1):
    fn=f'{OUT}dbmh_{i:02d}.txt'; open(fn,'w').write(t)
    idx.append({'id':f'dbmh_{i:02d}','descripcion':'Diccionario Bíblico Mundo Hispano (Douglas y Tenney; Editorial Mundo Hispano): entradas que citan Génesis','paginas':'varias (ver encabezados)','archivo':fn})
json.dump({'chunks':idx},open(OUT+'grupo_D.json','w'),ensure_ascii=False)
print(len(idx),'trozos'); print([e['titulo'] for e in sel][:80])
