import json,os
f=json.load(open('/home/user/trabajo/clasif/fichas.json'))
os.makedirs('/home/user/trabajo/clasif/lotes',exist_ok=True)
N=30; lotes=[]
for i in range(0,len(f),N):
    k=i//N+1; fn=f'/home/user/trabajo/clasif/lotes/lote_{k:02d}.json'
    json.dump(f[i:i+N],open(fn,'w'),ensure_ascii=False,indent=1)
    lotes.append({'id':f'lote_{k:02d}','archivo':fn,'n':len(f[i:i+N])})
json.dump(lotes,open('/home/user/trabajo/clasif/lotes/_lotes.json','w'))
print(len(lotes),'lotes')
