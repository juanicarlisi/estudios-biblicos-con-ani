#!/usr/bin/env python3
"""Consulta el hebreo de Génesis (WLC, OpenScriptures) con números Strong y definición del léxico Strong.
Uso: hebreo.py 3:15            -> palabras del versículo
     hebreo.py 3:15 3:20       -> rango
     hebreo.py --strong 7225   -> entrada del léxico
     hebreo.py --buscar 1285   -> versículos de Génesis donde aparece ese Strong
"""
import sys,re,json
import xml.etree.ElementTree as ET
NS={'o':'http://www.bibletechnologies.net/2003/OSIS/namespace'}
def lex():
    t=open('/home/user/trabajo/hebreo/strongs-hebrew.js').read()
    j=t[t.index('{'):t.rindex('}')+1]
    return json.loads(j)
def versos():
    root=ET.parse('/home/user/trabajo/hebreo/Gen.xml').getroot()
    out={}
    for v in root.iter('{%s}verse'%NS['o']):
        _,c,n=v.get('osisID').split('.')
        ws=[]
        for w in v.iter('{%s}w'%NS['o']):
            lem=w.get('lemma','')
            nums=re.findall(r'(\d+)',lem.split('/')[-1]) if lem else []
            ws.append((''.join(w.itertext()).replace('/',''),nums[0] if nums else '',w.get('morph','')))
        out[(int(c),int(n))]=ws
    return out
def main():
    L=lex()
    if sys.argv[1]=='--strong':
        e=L.get('H'+sys.argv[2]); print(json.dumps(e,ensure_ascii=False,indent=1)); return
    V=versos()
    if sys.argv[1]=='--buscar':
        s=sys.argv[2]; print([f'{c}:{n}' for (c,n),ws in sorted(V.items()) if any(w[1]==s for w in ws)]); return
    def p(x): c,n=x.split(':'); return int(c),int(n)
    a=p(sys.argv[1]); b=p(sys.argv[2]) if len(sys.argv)>2 else a
    for k in sorted(V):
        if a<=k<=b:
            print(f'Gn {k[0]}:{k[1]}')
            for heb,num,morph in V[k]:
                e=L.get('H'+num,{}) if num else {}
                print(f'  {heb}\tH{num}\t{e.get("xlit","")}\t{(e.get("strongs_def") or "")[:90]}\t[{morph}]')
main()
