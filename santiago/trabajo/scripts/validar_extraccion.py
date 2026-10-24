#!/usr/bin/env python3
"""Controla un archivo de notas extraídas de un bloque (comentarios de la biblioteca o barrido de REFERENCIA3).

Uso: validar_extraccion.py <notas.json> [--ref3]
Errores (el archivo no sirve hasta corregirlos):
  - estructura, campos obligatorios, tipo e importancia válidos, referencia dentro de Santiago 1:1–5:20 (o «intro» / «tema»);
  - la página rotulada tiene que existir en el bloque que se leyó;
  - en --ref3, el ARCHIVO tiene que ser uno de los del bloque.
Avisos (conviene revisarlos): citas textuales que no figuran tal cual en el bloque; palabras griegas que no figuran en Santiago.
"""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
import config as C

TIPOS = {'contexto_historico', 'cultura_costumbres', 'arqueologia_geografia', 'griego_palabra', 'explicacion_texto', 'teologia_doctrina',
         'cristo_en_santiago', 'eco_de_jesus', 'conexion_biblica', 'aplicacion_practica', 'ilustracion', 'dificultad_interpretaciones',
         'estructura_bosquejo', 'cronologia_fechas', 'personaje', 'pregunta_reflexion',
         # solo en el barrido de REFERENCIA3
         'apologetica', 'matrimonio_familia'}
OBLIG = ('ref', 'tipo', 'titulo', 'contenido', 'pagina', 'importancia')


def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]', '', s)


def ref_valida(ref):
    r = str(ref).strip().replace('–', '-').replace('—', '-').replace(' ', '')
    if r in ('intro', 'tema'):
        return True
    m = re.fullmatch(r'([1-5])(?::(\d+)(?:-(?:([1-5]):)?(\d+))?)?', r)
    if not m:
        return False
    c1 = int(m.group(1))
    if m.group(2) is None:
        return True
    v1 = int(m.group(2))
    if not 1 <= v1 <= C.V[c1 - 1]:
        return False
    if m.group(4) is None:
        return True
    c2 = int(m.group(3)) if m.group(3) else c1
    v2 = int(m.group(4))
    return v2 >= 1 and v2 <= C.V[c2 - 1] and C.idx(c2, v2) >= C.idx(c1, v1)


def paginas_del_bloque(texto):
    pags = set(re.findall(r'PÁGINA PDF (\d+)', texto))
    return {int(p) for p in pags}


def fragmentos_ref3(texto):
    """{archivo: conjunto de páginas PDF presentes en el bloque} para los bloques de REFERENCIA3."""
    out = {}
    for parte in texto.split('##### ')[1:]:
        cab = parte.split('\n', 1)[0]
        m = re.search(r'ARCHIVO: (.+?) \| (páginas PDF (\d+)-(\d+)|pág\. PDF (\d+))', cab)
        if not m:
            continue
        pags = set(range(int(m.group(3)), int(m.group(4)) + 1)) if m.group(3) else {int(m.group(5))}
        pags |= {int(x) for x in re.findall(r'\[pág\. PDF (\d+)\]', parte)}
        out.setdefault(m.group(1).strip(), set()).update(pags)
    return out


def main():
    fn = sys.argv[1]
    ref3 = '--ref3' in sys.argv
    errores, avisos = [], []
    try:
        d = json.load(open(fn))
    except Exception as e:
        print('ERROR: no es JSON válido:', e); sys.exit(1)
    bid = os.path.basename(fn)[:-5]
    if d.get('bloque') != bid:
        errores.append(f"«bloque» debe ser «{bid}» (es {d.get('bloque')!r})")
    if not isinstance(d.get('notas'), list) or not d['notas']:
        errores.append('«notas» debe ser una lista con notas'); d['notas'] = []
    if not isinstance(d.get('problemas', ''), str):
        errores.append('«problemas» debe ser texto (vacío si no hubo)')
    bloque_txt = ''
    carpeta = os.path.join(C.TMP, 'segmentos', 'ref3' if ref3 else 'biblio')
    p = os.path.join(carpeta, bid + '.txt')
    if os.path.exists(p):
        bloque_txt = open(p, errors='ignore').read()
    else:
        avisos.append(f'no encontré el bloque {p} para cotejar páginas y citas')
    pags = paginas_del_bloque(bloque_txt) if (bloque_txt and not ref3) else set()
    frag = fragmentos_ref3(bloque_txt) if (bloque_txt and ref3) else {}
    plano = norm(bloque_txt)
    sin_griego = []
    if True:
        import griego as G
        formas = set(); lemas = set()
        for ws in G.versos().values():
            for w in ws:
                formas.add(G.sin_acentos(w['palabra'])); lemas.add(G.sin_acentos(w['lema']))
    for i, n in enumerate(d['notas'], 1):
        et = f"nota {i} «{str(n.get('titulo', ''))[:40]}»"
        for k in OBLIG:
            if n.get(k) in (None, '', []):
                errores.append(f'{et}: falta «{k}»')
        if n.get('tipo') not in TIPOS:
            errores.append(f"{et}: tipo inválido {n.get('tipo')!r}")
        if not isinstance(n.get('importancia'), int) or not 1 <= n['importancia'] <= 3:
            errores.append(f"{et}: importancia debe ser 1, 2 o 3")
        if n.get('ref') is not None and not ref_valida(n['ref']):
            errores.append(f"{et}: ref inválida {n.get('ref')!r} (use «C:V», «C:V-V», «C:V-C:V», «C», «intro» o «tema»; Santiago llega hasta 5:20)")
        if isinstance(n.get('contenido'), str) and len(n['contenido']) < 40:
            errores.append(f'{et}: contenido demasiado corto')
        pg = str(n.get('pagina', ''))
        if pags:
            m = re.search(r'PÁGINA PDF (\d+)', pg) or re.search(r'p[áa]g\.?\s*PDF\s*(\d+)', pg, re.I)
            if not m:
                errores.append(f'{et}: «pagina» debe copiar el rótulo del encabezado (con «PÁGINA PDF n»): {pg!r}')
            elif int(m.group(1)) not in pags:
                errores.append(f'{et}: la página PDF {m.group(1)} no está en este bloque')
        if ref3:
            for k in ('tema', 'autor', 'obra', 'archivo'):
                if not n.get(k):
                    errores.append(f'{et}: falta «{k}»')
            if frag:
                a = n.get('archivo')
                m = re.search(r'(\d+)', pg)
                if a not in frag:
                    errores.append(f"{et}: «archivo» no figura entre los del bloque: {a!r}")
                elif not m:
                    errores.append(f'{et}: «pagina» debe ser el número de página PDF: {pg!r}')
                elif int(m.group(1)) not in frag[a]:
                    errores.append(f"{et}: la página PDF {m.group(1)} no corresponde a ese archivo en este bloque")
        cita = n.get('cita')
        if cita:
            if len(cita.split()) > 60:
                errores.append(f'{et}: «cita» de más de 60 palabras')
            if plano and norm(cita) not in plano:
                avisos.append(f"{et}: la cita no figura tal cual en el bloque: {cita[:70]!r}")
        g = n.get('griego')
        if g:
            if not isinstance(g, dict) or not g.get('palabra'):
                errores.append(f'{et}: «griego» debe tener «palabra»')
            else:
                for w in re.findall(r'[Ͱ-Ͽἀ-῿]+', g['palabra']):
                    b = G.sin_acentos(w)
                    if b not in formas and b not in lemas:
                        sin_griego.append(f'{et}: «{w}» no figura en el griego de Santiago (puede ser un término de comparación)')
    avisos += sin_griego
    print(f'{fn}: {len(d["notas"])} notas | {len(errores)} errores | {len(avisos)} avisos')
    for e in errores[:60]:
        print('  ERROR', e)
    for a in avisos[:25]:
        print('  aviso', a)
    if len(avisos) > 25:
        print(f'  … y {len(avisos) - 25} avisos más')
    sys.exit(1 if errores else 0)


if __name__ == '__main__':
    main()
