import json,re,os
FUENTES={
 'kline':('kline_ncb_genesis.txt',1,25,'Meredith G. Kline, «Génesis», en Nuevo Comentario Bíblico (Guthrie, Motyer y otros; Casa Bautista)',74),
 'beacon':('beacon_t1.txt',17,121,'George Herbert Livingston, «Génesis», Comentario Bíblico Beacon, tomo 1 (CNP)',None),
 'cbmh':('cbmh_genesis.txt',1,249,'Comentario Bíblico Mundo Hispano, tomo 1: Génesis (Editorial Mundo Hispano)',None),
 'edersheim':('edersheim_genesis.txt',1,102,'Alfred Edersheim, Comentario Bíblico Histórico: Génesis (Clie)',None),
 'macarthur':('macarthur_be.txt',78,189,'John MacArthur, Biblia de Estudio MacArthur (Portavoz): introducción y notas de Génesis',None),
}
BASURA=re.compile(r'^(IGLESIA CRISTIANA MINISTERIO DEL REINO DE CRISTO|Pastor Uriel Campos|Descargado de http://www\.yahwehjireh\.org)\s*$',re.M)
MAX=42000
idx=[]
for k,(fn,a,b,desc,off) in FUENTES.items():
    pags=open('/home/user/trabajo/corpus_biblio/'+fn,errors='ignore').read().split('\f')
    trozos=[];cur='';ini=a
    for n in range(a,b+1):
        t=BASURA.sub('',pags[n-1]).strip()
        t=re.sub(r'\n{3,}','\n\n',t)
        lab=f'=== [{k} | PÁGINA PDF {n}' + (f' | pág. impresa {n+off}' if off else '') + '] ==='
        bloque=lab+'\n'+t+'\n'
        if len(cur)+len(bloque)>MAX and cur:
            trozos.append((ini,n-1,cur)); cur=''; ini=n
        cur+=bloque
    if cur: trozos.append((ini,b,cur))
    for i,(x,y,c) in enumerate(trozos,1):
        fnout=f'/home/user/trabajo/segmentos/biblio/{k}_{i:02d}.txt'
        open(fnout,'w').write(c)
        idx.append({'id':f'{k}_{i:02d}','fuente':k,'descripcion':desc,'paginas':f'{x}-{y}','archivo':fnout,'chars':len(c)})
json.dump(idx,open('/home/user/trabajo/segmentos/biblio/_indice.json','w'),ensure_ascii=False,indent=1)
import collections
print(len(idx),'trozos', collections.Counter(i['fuente'] for i in idx), sum(i['chars'] for i in idx))
