#!/usr/bin/env python3
"""Arma los bloques de lectura de Apocalipsis (texto con marcas de página) a partir de los libros extraídos.

Tres familias:
  A) comentarios de Apocalipsis completos (se leen enteros): macarthur, mcgee, mcgeer (radio), larkin, ladd, beacon, cbmh,
     carballosa, henry, mbiblia (notas de la Biblia de Estudio MacArthur)
  B) Diccionario Bíblico Mundo Hispano: páginas con citas <66CCVV> (= Apocalipsis CC:VV)
  C) libros confiables de REFERENCIA3: tramos con señal fuerte (r1) y ventanas alrededor de citas (r2)
Uso: armar_corpus.py   (lee SCRATCH, escribe SCRATCH/bloques/*.txt y SCRATCH/bloques/_indice.json)
"""
import json, os, re, hashlib, sys
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
OUT = S + '/bloques'; os.makedirs(OUT, exist_ok=True)
MAX = 90000
sys.path.insert(0, os.path.dirname(__file__))
from indice_apocalipsis import citas, RE_F

RUIDO = [r'Descargado de http://www\.yahwehjireh\.org', r'IGLESIA CRISTIANA MINISTERIO DEL REINO DE CRISTO\s*Pastor Uriel Campos',
         r'Escanee el código para ver más productos', r'atravesdelabiblia\.org']
def limpiar(t):
    for r in RUIDO: t = re.sub(r, '', t)
    t = re.sub(r'[ \t\xa0]{2,}', ' ', t)
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

def pags(path): return open(path, errors='ignore').read().split('\f')

FAM_A = {
    'macarthur': dict(txt=S + '/txt/23_MacArthur__John_C.txt', desde=1, hasta=None, obra='John MacArthur, Comentario MacArthur del Nuevo Testamento: Apocalipsis (Portavoz)'),
    'mcgee': dict(txt=S + '/txt/Apocalipsis__Un_Come.txt', obra='J. Vernon McGee, Apocalipsis: un comentario (Thru the Bible Radio Network, 2019)'),
    'mcgeer': dict(txt=S + '/txt/27_Vernon_McGee_Come.txt', obra='J. Vernon McGee, Comentario bíblico «A través de la Biblia»: Apocalipsis (transcripción de los programas de radio)'),
    'larkin': dict(txt=S + '/txt/Apocalipsis_-_Claren.txt', obra='Clarence Larkin, El libro de Apocalipsis (con sus cuadros y diagramas)'),
    'ladd': dict(txt=S + '/txt/Comentario_del_Apoca.txt', obra='George Eldon Ladd, Comentario del Apocalipsis'),
    'beacon': dict(txt=S + '/txt/Comentario_Biblico_B.txt', desde=307, hasta=None, obra='Ralph Earle, «Apocalipsis», Comentario Bíblico Beacon, tomo 10 (Casa Nazarena de Publicaciones)'),
    'cbmh': dict(txt=S + '/ref3txt/Escatologia y Ultimos Tiempos__Apocalipsis 1, 2, 3.pdf.txt', desde=97, hasta=None, obra='Comentario Bíblico Mundo Hispano, tomo 24: Apocalipsis (exposición de N. Alirio Eustache Vilaire; ayudas prácticas de Juan Carlos Cevallos)'),
    'carballosa': dict(txt=S + '/corpus/carballosa.txt', obra='Evis L. Carballosa, Apocalipsis: el drama de los siglos (Portavoz)'),
    'henry': dict(txt=S + '/corpus/henry.txt', desde=173, hasta=195, obra='G. R. Beasley-Murray, «Apocalipsis», Nuevo Comentario Bíblico (Clie); el PDF se rotula como «Biblia Matthew Henry», pero el texto es de Beasley-Murray'),
    'mbiblia': dict(txt=S + '/corpus/macarthur_biblia.txt', desde=3390, hasta=3479, obra='John MacArthur, Biblia de Estudio MacArthur: introducción y notas de Apocalipsis'),
}
indice = []
def volcar(id_, items, obra):
    """items: [(rotulo_pagina, texto)] -> bloques de <= MAX caracteres"""
    cur = ''; n = 0
    def cerrar():
        nonlocal cur, n
        if cur.strip():
            n += 1; fn = f'{OUT}/{id_}_{n:02d}.txt'
            open(fn, 'w').write(f'# {obra}\n\n' + cur)
            indice.append({'id': f'{id_}_{n:02d}', 'archivo': fn, 'obra': obra, 'chars': len(cur)})
        cur = ''
    for rot, txt in items:
        b = f'=== [{id_} | {rot}] ===\n{txt}\n\n'
        if len(cur) + len(b) > MAX and cur: cerrar()
        cur += b
    cerrar()

def fam_a():
    for id_, d in FAM_A.items():
        if not os.path.exists(d['txt']):
            print('FALTA', id_); continue
        P = pags(d['txt']); desde = d.get('desde', 1); hasta = d.get('hasta') or len(P)
        items = []
        for n in range(desde, hasta + 1):
            t = limpiar(P[n - 1])
            if len(t) > 80: items.append((f'pág. PDF {n}', t))
        volcar(id_, items, d['obra'])

def fam_b():
    items = []
    for vol, fn in (('I', 'dbmh1'), ('II', 'dbmh2')):
        P = pags(f'{S}/corpus/{fn}.txt')
        for n, p in enumerate(P, 1):
            if len(re.findall(r'<66\d{4}>', p)) >= 2: items.append((f'vol. {vol} pág. PDF {n}', limpiar(p)))
    volcar('dbmh', items, 'Diccionario Bíblico Mundo Hispano (Editorial Mundo Hispano): páginas que citan Apocalipsis (<66CCVV> = Apocalipsis CC:VV)')
    print('dbmh páginas', len(items))

EXCL = ['390 - Apocalipsis - John MacArthur', 'Apocalipsis - Clarence Larkin', 'Apocalipsis 1, 2, 3', 'Apocalipsis - Evis Carballosa']
def fam_c():
    cl = {x['path']: x for x in json.load(open('/home/user/estudios-biblicos-con-ani/genesis/trabajo/clasificacion/clasificacion.json'))}
    idx = json.load(open(S + '/indice_ref3.json'))
    vistos = set(); t1 = []; t2 = []
    for k, v in idx.items():
        rel = k[5:]
        if any(x in rel for x in EXCL): continue
        txt = open(v['txt'], errors='ignore').read()
        h = hashlib.md5(re.sub(r'\s+', '', txt[50000:80000]).encode()).hexdigest()
        if h in vistos: continue
        vistos.add(h)
        P = txt.split('\f'); sc = {x['pag']: x['score'] for x in v['paginas']}
        fuertes = sorted(p for p, s in sc.items() if s >= 6 and len(P[p - 1]) < 12000)
        runs = []; cur = []
        for p in fuertes:
            if cur and p == cur[-1] + 1: cur.append(p)
            else:
                if cur: runs.append(cur)
                cur = [p]
        if cur: runs.append(cur)
        usadas = set()
        for r in runs:
            if len(r) >= 3 or (len(r) == 2 and sum(sc[p] for p in r) >= 24):
                usadas.update(r)
                t1.append({'k': k, 'rel': rel, 'pags': r, 'texto': '\n'.join(f'--- [pág. PDF {p}] ---\n' + limpiar(P[p - 1]) for p in r)})
        for pn, p in enumerate(P, 1):
            if pn in usadas or pn not in sc: continue
            lines = p.split('\n'); marcas = [i for i, l in enumerate(lines) if citas(l) or len(RE_F.findall(l)) >= 2]
            if not marcas: continue
            win = set()
            for i in marcas: win.update(range(max(0, i - 6), min(len(lines), i + 7)))
            segs = []; cur = []
            for j in sorted(win):
                if cur and j != cur[-1] + 1: segs.append(cur); cur = []
                cur.append(j)
            if cur: segs.append(cur)
            for s in segs:
                t = ' '.join(lines[j].strip() for j in s)
                if len(t) > 250: t2.append({'k': k, 'rel': rel, 'pag': pn, 'texto': t[:3000]})
    print('r1 tramos', len(t1), sum(len(x['texto']) for x in t1), '| r2 ventanas', len(t2), sum(len(x['texto']) for x in t2))
    def meta(rel):
        l = cl.get(rel, {}); return l.get('autor', '?'), l.get('titulo') or rel.split('/')[-1]
    def vol(items, pref):
        cur = ''; n = 0; out = []
        for it in sorted(items, key=lambda x: (x['k'], x.get('pags', [x.get('pag')])[0])):
            a, t = meta(it['rel'])
            if 'pags' in it: b = f"\n##### OBRA: {t} | AUTOR: {a} | ARCHIVO: {it['rel']} | páginas PDF {it['pags'][0]}-{it['pags'][-1]}\n{it['texto']}\n"
            else: b = f"\n##### OBRA: {t} | AUTOR: {a} | ARCHIVO: {it['rel']} | pág. PDF {it['pag']} (fragmento)\n{it['texto']}\n"
            b = b[:MAX]
            if len(cur) + len(b) > MAX and cur: out.append(cur); cur = ''
            cur += b
        if cur: out.append(cur)
        for i, t in enumerate(out, 1):
            fn = f'{OUT}/{pref}_{i:03d}.txt'; open(fn, 'w').write(t)
            indice.append({'id': f'{pref}_{i:03d}', 'archivo': fn, 'obra': 'libros de REFERENCIA3 (fragmentos rotulados)', 'chars': len(t)})
    vol(t1, 'r1'); vol(t2, 'r2')

def fam_d():
    """Artículos web: Coalición por el Evangelio (rastreados con crawl_cpe.py) y otros sitios (SCRATCH/web/otros)."""
    import glob
    for fuente, patron, umbral in (('cpe', S + '/web/cpe/art/*.json', 14), ('web', S + '/web/otros/*/*.json', 0)):
        arts = []
        for f in glob.glob(patron):
            try: d = json.load(open(f))
            except Exception: continue
            t = d.get('texto', '')
            if len(t) < 1200: continue
            sc = 3 * len(citas(t)) + len(RE_F.findall(t))
            if sc >= umbral: arts.append((sc, d))
        arts.sort(key=lambda x: -x[0])
        items = []
        for sc, d in arts:
            cab = f"{d.get('titulo','')} | {d.get('autor','')} | {d.get('fecha','')} | {d.get('fuente') or 'Coalición por el Evangelio'} | {d.get('url','')}"
            items.append((cab, d['texto'][:(45000 if 'guzik' in str(d.get('url','')).lower() or 'guzik' in str(d.get('fuente','')).lower() else 25000)]))
        volcar(fuente, items, 'Artículos web de acceso libre (' + ('Coalición por el Evangelio' if fuente == 'cpe' else 'TTL, MiSion y otros sitios') + ')')
        print(fuente, 'artículos', len(arts))

if __name__ == '__main__':
    fam_a(); fam_b(); fam_c(); fam_d()
    json.dump(indice, open(OUT + '/_indice.json', 'w'), ensure_ascii=False, indent=0)
    import collections
    c = collections.Counter(i['id'].split('_')[0] for i in indice); print(c, sum(i['chars'] for i in indice))
