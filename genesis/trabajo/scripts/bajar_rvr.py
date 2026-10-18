import re,html,json,time,subprocess,os
res={}
for c in range(1,51):
    fn=f'/home/user/trabajo/biblia/html/gen{c}.html'
    os.makedirs(os.path.dirname(fn),exist_ok=True)
    if not os.path.exists(fn) or os.path.getsize(fn)<10000:
        subprocess.run(['curl','-sS','-A','Mozilla/5.0',f'https://www.bible.com/es/bible/149/GEN.{c}.RVR1960','-o',fn])
        time.sleep(1.5)
    t=open(fn).read()
    spans=re.findall(r'data-usfm="(GEN\.%d\.\d+)">(.*?)(?=<span class="[^"]*verse[^"]*" data-usfm=|</div></div>)'%c,t,re.S)
    ch={}
    for usfm,body in spans:
        body=re.sub(r'<span class="[^"]*label[^"]*">.*?</span>','',body,flags=re.S)
        body=re.sub(r'<span class="[^"]*note[^"]*">.*?</span></span>','',body,flags=re.S)
        txt=html.unescape(re.sub(r'<[^>]+>','',body)).strip()
        v=int(usfm.split('.')[2])
        ch[v]=(ch.get(v,'')+' '+txt).strip()
    res[c]=ch
json.dump(res,open('/home/user/trabajo/biblia/rvr1960_genesis.json','w'),ensure_ascii=False,indent=0)
esperado=[31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,55,32,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26]
tot=0
for c in range(1,51):
    n=len(res[c]); tot+=n
    if n!=esperado[c-1] or sorted(res[c])!=list(range(1,n+1)): print('DIF cap',c,n,esperado[c-1])
print('total versos',tot,'esperado',sum(esperado))
