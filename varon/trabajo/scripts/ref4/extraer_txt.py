import os,subprocess,sys,hashlib,json
from concurrent.futures import ThreadPoolExecutor
root='/home/user/libros-referencia4';out='ref4txt'
files=[]
for dp,_,fn in os.walk(root):
    if '/.git' in dp: continue
    for f in fn:
        if f.lower().endswith('.pdf'): files.append(os.path.join(dp,f))
def run(p):
    rel=os.path.relpath(p,root);h=hashlib.md5(rel.encode()).hexdigest()[:10]
    o=f'{out}/{h}.txt'
    if not os.path.exists(o):
        try: subprocess.run(['pdftotext','-layout','-enc','UTF-8',p,o],timeout=240,capture_output=True)
        except Exception as e: pass
    n=os.path.getsize(o) if os.path.exists(o) else -1
    return {'rel':rel,'h':h,'bytes':n,'size':os.path.getsize(p)}
with ThreadPoolExecutor(8) as ex: res=list(ex.map(run,files))
json.dump(res,open('ref4_manifest.json','w'),ensure_ascii=False)
print(len(res),sum(1 for r in res if r['bytes']<20000))
