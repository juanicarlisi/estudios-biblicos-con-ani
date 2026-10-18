import json,subprocess,re,unicodedata,time,os
bg=json.load(open('/home/user/trabajo/biblia/rvr1960_genesis.json'))['texto']
def norm(s):
    s=re.sub(r'<[^>]+>','',s); s=unicodedata.normalize('NFC',s).lower()
    return re.sub(r'[^a-záéíóúüñ]','',s)
os.makedirs('/home/user/trabajo/biblia/bolls',exist_ok=True)
dif=0
for c in range(1,51):
    fn=f'/home/user/trabajo/biblia/bolls/{c}.json'
    if not os.path.exists(fn):
        subprocess.run(['curl','-sS',f'https://bolls.life/get-chapter/RV1960/1/{c}/','-o',fn]); time.sleep(0.5)
    b={str(x['verse']):x['text'] for x in json.load(open(fn))}
    for v,t in bg[str(c)].items():
        if norm(t)!=norm(b.get(v,'')):
            dif+=1
            if dif<=15: print(c,v,'\n BG:',t.replace('\n',' / '),'\n BO:',re.sub(r'<[^>]+>','',b.get(v,''))[:300])
print('diferencias',dif)
