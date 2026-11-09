import json,glob,os,sys,shutil
S='/tmp/claude-0/-home-user/446b7ea4-e7f3-5663-b395-6889a80e8fc5/scratchpad/nd/dias'
V='/home/user/estudios-biblicos-con-ani/varon/trabajo'
ok=[];mal=[]
for f in sorted(glob.glob(f'{S}/dia_*.json')):
    n=int(os.path.basename(f)[4:7])
    if os.path.exists(f"{V}/dias/dia_{n:03d}.json"): continue
    try:
        x=json.load(open(f));x['dia']=n
        json.dump(x,open(f'{V}/dias/dia_{n:03d}.json','w'),ensure_ascii=False,indent=1);ok.append(n)
    except Exception as e: mal.append((n,str(e)[:80]))
print('instalados',ok);print('mal',mal)
