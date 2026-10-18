import json,collections
sel=json.load(open('indice/seleccion_final.json'))
c={l['path']:l for l in json.load(open('clasif/clasificacion.json'))}
def meta(k):
    if k.startswith('REF3/'):
        l=c[k[5:]]; return l['autor'], l.get('titulo') or k.split('/')[-1]
    return 'biblioteca de comentarios', k.split('/',1)[1]
idx=[]
def volcar(items,pref,MAX):
    cur='';n=0;out=[]
    for it in items:
        a,t=meta(it['k'])
        if 'pags' in it:
            b=f"\n##### OBRA: {t} | AUTOR: {a} | ARCHIVO: {it['k']} | páginas PDF {it['pags'][0]}-{it['pags'][-1]}\n{it['texto']}\n"
        else:
            b=f"\n##### OBRA: {t} | AUTOR: {a} | ARCHIVO: {it['k']} | pág. PDF {it['pag']} (fragmento)\n{it['texto']}\n"
        if len(b)>MAX: b=b[:MAX]
        if len(cur)+len(b)>MAX and cur:
            out.append(cur); cur=''
        cur+=b
    if cur: out.append(cur)
    for i,t in enumerate(out,1):
        fn=f'segmentos/ref3/{pref}_{i:03d}.txt'; open(fn,'w').write(t)
        idx.append({'id':f'{pref}_{i:03d}','archivo':'/home/user/trabajo/'+fn,'chars':len(t)})
t1=sorted(sel['t1'],key=lambda x:(x['k'],x['pags'][0]))
t2=sorted(sel['t2'],key=lambda x:(x['k'],x['pag']))
volcar(t1,'r1',80000); volcar(t2,'r2',100000)
json.dump(idx,open('segmentos/ref3/_indice.json','w'),indent=0)
cc=collections.Counter(i['id'][:2] for i in idx); print(cc, sum(i['chars'] for i in idx))
