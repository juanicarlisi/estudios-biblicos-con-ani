import re,json
OUT='/home/user/trabajo/segmentos/biblio/'
pags_sel=[]
for vol,fn in [('I','dbmh_1.txt'),('II','dbmh_2.txt')]:
    pags=open('/home/user/trabajo/corpus_biblio/'+fn,errors='ignore').read().split('\f')
    for pn,p in enumerate(pags,1):
        g=len(re.findall(r'<01\d{4}>',p))
        if g>=2: pags_sel.append((vol,pn,g,p))
print('paginas',len(pags_sel),'chars',sum(len(x[3]) for x in pags_sel))
MAX=42000; trozos=[];cur=''
for vol,pn,g,p in pags_sel:
    b=f"=== [dbmh | Diccionario Bíblico Mundo Hispano, vol. {vol} | PÁGINA PDF {pn}] ===\n{p.strip()}\n\n"
    if len(cur)+len(b)>MAX and cur: trozos.append(cur); cur=''
    cur+=b
if cur: trozos.append(cur)
idx=[]
for i,t in enumerate(trozos,1):
    fn=f'{OUT}dbmh_{i:02d}.txt'; open(fn,'w').write(t)
    idx.append({'id':f'dbmh_{i:02d}','descripcion':'Diccionario Bíblico Mundo Hispano (Editorial Mundo Hispano), páginas que citan Génesis (las citas aparecen codificadas como <01CCVV> = Génesis capítulo CC versículo VV). Extraer SOLO lo que aporta a entender Génesis (personas, lugares, costumbres, palabras, temas de Génesis); ignorar entradas ajenas a Génesis','paginas':'varias (ver encabezados)','archivo':fn})
json.dump({'chunks':idx},open(OUT+'grupo_D.json','w'),ensure_ascii=False)
print(len(idx),'trozos')
