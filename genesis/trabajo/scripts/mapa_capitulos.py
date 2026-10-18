"""Asigna a cada página de cada comentario el capítulo de Génesis que trata (heurística + suavizado)."""
import re,json,collections
FUENTES={
 'kline':('kline_ncb_genesis.txt',1,25),
 'beacon':('beacon_t1.txt',16,121),
 'cbmh':('cbmh_genesis.txt',1,249),
 'edersheim':('edersheim_genesis.txt',1,102),
 'macarthur':('macarthur_be.txt',78,189),
}
LIBROS=r'(?:Éx|Ex|Lv|Lev|Nm|Núm|Num|Dt|Deut|Jos|Jue|Jueces|Rt|S|R|Cr|Esd|Neh|Est|Job|Sal|Pr|Prov|Ec|Cnt|Is|Isa|Jer|Lm|Ez|Dn|Dan|Os|Jl|Am|Abd|Jon|Mi|Nah|Hab|Sof|Hag|Zac|Mal|Mt|Mat|Mr|Mc|Lc|Luc|Jn|Juan|Hch|Hech|Ro|Rom|Co|Cor|Gá|Gál|Ef|Fil|Col|Ts|Tes|Ti|Tim|Tit|Flm|He|Heb|Stg|Sant|P|Pe|Ped|Jud|Ap|Apoc)'
pat=re.compile(r'(?<![\w.])(?:(%s)\.?\s*)?(\d{1,2}):\s?(\d{1,3})'%LIBROS)
out={}
for k,(fn,a,b) in FUENTES.items():
    pags=open('/home/user/trabajo/corpus_biblio/'+fn,errors='ignore').read().split('\f')
    caps=[]
    for i in range(a-1,b):
        c=collections.Counter()
        for m in pat.finditer(pags[i]):
            if m.group(1): continue
            ch=int(m.group(2))
            if 1<=ch<=50: c[ch]+=1
        caps.append(c.most_common(1)[0][0] if c else None)
    # suavizado: rellenar huecos y forzar no decreciente con mediana móvil
    lleno=[];ult=1
    for x in caps:
        ult=x if x else ult; lleno.append(ult)
    sm=[]
    for i in range(len(lleno)):
        w=sorted(lleno[max(0,i-2):i+3]); sm.append(w[len(w)//2])
    mono=[];m=1
    for x in sm:
        m=max(m,x); mono.append(m)
    out[k]={'archivo':fn,'pagina_inicio':a,'capitulo_por_pagina':{str(a+i):mono[i] for i in range(len(mono))}}
    resumen=collections.OrderedDict()
    for i,x in enumerate(mono): resumen.setdefault(x,[a+i,a+i]); resumen[x][1]=a+i
    print(k,' '.join(f'{c}:{v[0]}-{v[1]}' for c,v in resumen.items()))
json.dump(out,open('/home/user/trabajo/segmentos/mapa_paginas.json','w'),indent=1)
