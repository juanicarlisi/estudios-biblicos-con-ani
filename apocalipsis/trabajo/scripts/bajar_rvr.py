import re,html,json,time,subprocess,os
from html.parser import HTMLParser
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
class P(HTMLParser):
    def __init__(s,c):
        super().__init__(); s.c=c; s.stack=[]; s.verses={}; s.headings={}; s.cur=None; s.skip=0; s.inh=False; s.htxt=''; s.lastv=0
    def handle_starttag(s,tag,attrs):
        a=dict(attrs); cls=a.get('class','') or ''
        m=re.search(r'\bRev-%d-(\d+)\b'%s.c,cls)
        if tag=='span' and m and 'text' in cls.split():
            v=int(m.group(1))
            if v in s.verses and s.verses[v].strip(): s.verses[v]+='\n'
            s.stack.append(('verse',v)); s.cur=v; return
        if tag in('sup',) or (tag=='span' and 'chapternum' in cls) or (tag=='div' and ('footnotes' in cls or 'crossrefs' in cls)):
            s.stack.append(('skip',None)); s.skip+=1; return
        if tag=='h3': s.inh=True; s.htxt=''
        s.stack.append((tag,None))
    def handle_endtag(s,tag):
        if tag=='h3' and s.inh:
            s.inh=False; s.headings[s.lastv+1]=s.htxt.strip()
        if not s.stack: return
        kind,v=s.stack.pop()
        if kind=='skip': s.skip-=1
        if kind=='verse': s.lastv=v; s.cur=None if not any(k=='verse' for k,_ in s.stack) else s.cur
    def handle_data(s,d):
        if s.inh and not s.skip: s.htxt+=d; return
        if s.skip: return
        vs=[v for k,v in s.stack if k=='verse']
        if vs: s.verses[vs[-1]]=s.verses.get(vs[-1],'')+d
res={}; tit={}
os.makedirs('/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad/biblia/bg',exist_ok=True)
for c in range(1,23):
    fn=f'/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad/biblia/bg/rev{c}.html'
    if not os.path.exists(fn) or os.path.getsize(fn)<50000:
        subprocess.run(['curl','-sS','-A',UA,f'https://www.biblegateway.com/passage/?search=Apocalipsis%20{c}&version=RVR1960','-o',fn]); time.sleep(2)
    t=open(fn).read()
    i=t.find('<div class="passage-text">'); j=t.find('<div class="footnotes">',i)
    p=P(c); p.feed(t[i:j if j>0 else None])
    res[c]={v:'\n'.join(re.sub(r'[ \t\r\xa0]+',' ',l).strip() for l in txt.split('\n') if l.strip()) for v,txt in sorted(p.verses.items())}
    tit[c]=p.headings
json.dump({'texto':res,'titulos':tit},open('/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad/biblia/rvr1960_apocalipsis.json','w'),ensure_ascii=False,indent=0)
esperado=[20,29,22,11,14,17,17,13,21,11,19,17,18,20,8,21,18,24,21,15,27,21]
tot=0
for c in range(1,23):
    n=len(res[c]); tot+=n
    if n!=esperado[c-1] or sorted(res[c])!=list(range(1,n+1)): print('DIF cap',c,n,esperado[c-1])
print('total',tot)
print(res[1][1]); print(res[22][21])
