import re, html, json, os, sys, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad/web/cpe'
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
urls=[u.strip() for u in open(S+'/urls.txt') if '/articulo/' in u]
os.makedirs(S+'/art',exist_ok=True)
def limpiar(t):
    t=re.sub(r'<(script|style|figure|aside|nav)[^>]*>.*?</\1>',' ',t,flags=re.S)
    t=re.sub(r'<br\s*/?>|</p>|</h\d>|</li>|</blockquote>','\n',t)
    t=re.sub(r'<[^>]+>','',t)
    t=html.unescape(t)
    return re.sub(r'\n\s*\n+','\n\n',re.sub(r'[ \t\xa0]+',' ',t)).strip()
def go(u):
    slug=u.rstrip('/').split('/')[-1]; dst=f'{S}/art/{slug}.json'
    if os.path.exists(dst): return 1
    for _ in range(3):
        try:
            req=urllib.request.Request(u,headers={'User-Agent':UA})
            t=urllib.request.urlopen(req,timeout=40).read().decode('utf-8','ignore'); break
        except Exception as e: t=None
    if not t: return 0
    ti=re.search(r'<title>(.*?)</title>',t,re.S); ti=html.unescape(ti.group(1)).replace(' | Coalición por el Evangelio','') if ti else ''
    m=re.search(r'<div class="entry-content">(.*?)<div class="article_author_bio"',t,re.S) or re.search(r'<div class="entry-content">(.*?)</article>',t,re.S)
    body=limpiar(m.group(1)) if m else ''
    au=re.search(r'<div class="article_author[^"]*"[^>]*>(.*?)</div>',t,re.S)
    au=limpiar(au.group(1)) if au else ''
    d=re.search(r'datePublished"\s*:\s*"([^"]+)"',t); 
    json.dump({'url':u,'titulo':ti,'autor':au[:80],'fecha':d.group(1)[:10] if d else '','texto':body},open(dst,'w'),ensure_ascii=False)
    return 1
with ThreadPoolExecutor(10) as ex:
    n=0
    for r in ex.map(go,urls):
        n+=1
        if n%500==0: print(n,flush=True)
print('FIN',flush=True)
