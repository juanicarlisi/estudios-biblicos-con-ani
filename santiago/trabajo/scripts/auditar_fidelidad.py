#!/usr/bin/env python3
"""Auditoría automática de fidelidad de las notas extraídas: ¿lo que dice la nota está en la página que cita?

Para cada nota compara las palabras de su «contenido» y «título» con el texto de la página citada (y la anterior y la siguiente, porque una idea
puede cruzar el salto de página), y revisa que los números que menciona (años, cantidades) figuren en esas páginas.
No reemplaza la lectura: marca las notas más dudosas (poca cobertura de palabras, números que no están) para revisarlas a mano o rehacer el bloque.

Uso:
  auditar_fidelidad.py [--ref3] [--bloque ID ...] [--peor N] [--umbral 0.35]
Sin --bloque recorre todos los bloques ya unidos (extracciones/ o extracciones_ref3/ con --ref3).
"""
import argparse, collections, glob, json, os, re, statistics, sys, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
import config as C

PARADAS = set('''
que los las del una uno unos unas con por para como pero sino sobre entre desde hasta cuando donde porque aunque mientras tambien cada esta este estos estas
esto esos esas ese esa eso solo todo todos toda todas otro otra otros otras mismo misma mismos mismas sido siendo tiene tienen tener hace hacen hacer puede
pueden poder debe deben deber seria sera seran esta estan estar muy mas menos tanto tanta ante bajo contra segun tras donde quien quienes cual cuales
autor autores nota texto pasaje pasajes versiculo versiculos santiago carta epistola capitulo dice dicen afirma afirman explica explican senala senalan
sostiene sostienen enseña enseñan ensena ensenan indica indican menciona mencionan describe describen plantea plantean considera consideran
interpreta interpretan presenta presentan resume resumen aclara aclaran destaca destacan subraya subrayan observa observan nota notan
comenta comentan argumenta argumentan propone proponen insiste insisten advierte advierten recuerda recuerdan llama llaman
'''.split())


def sin_acentos(s):
    s = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in s if not unicodedata.combining(c))


def tokens(s):
    s = sin_acentos(s).lower()
    return re.findall(r'[a-zñ]{4,}', s)


def tallo(w):
    return w[:6]


def tallos(s):
    return {tallo(w) for w in tokens(s) if w not in PARADAS and len(w) >= 5}


def numeros(s):
    s = re.sub(r'\b\d+:\d+(?:[-–]\d+)?\b', ' ', s)          # citas bíblicas C:V
    return set(re.findall(r'(?<![\d:])\d{2,4}(?![\d:])', s))


def paginas_biblio(txt):
    out = {}
    partes = re.split(r'^=== \[(.+?)\] ===\s*$', txt, flags=re.M)
    for i in range(1, len(partes) - 1, 2):
        m = re.search(r'PÁGINA PDF (\d+)', partes[i])
        if m:
            out[int(m.group(1))] = out.get(int(m.group(1)), '') + '\n' + partes[i + 1]
    return out


def paginas_ref3(txt):
    """{archivo: {pagina: texto}}"""
    out = collections.defaultdict(dict)
    for parte in txt.split('##### ')[1:]:
        cab, _, cuerpo = parte.partition('\n')
        m = re.search(r'ARCHIVO: (.+?) \| (páginas PDF (\d+)-(\d+)|pág\. PDF (\d+))', cab)
        if not m:
            continue
        arch = m.group(1).strip()
        primera = int(m.group(3)) if m.group(3) else int(m.group(5))
        trozos = re.split(r'^--- \[pág\. PDF (\d+)\] ---\s*$', cuerpo, flags=re.M)
        out[arch][primera] = out[arch].get(primera, '') + '\n' + trozos[0]
        for i in range(1, len(trozos) - 1, 2):
            p = int(trozos[i])
            out[arch][p] = out[arch].get(p, '') + '\n' + trozos[i + 1]
    return out


def analizar(ruta, ref3):
    d = json.load(open(ruta))
    bid = d['bloque']
    seg = os.path.join(C.TMP, 'segmentos', 'ref3' if ref3 else 'biblio', bid + '.txt')
    txt = open(seg, errors='ignore').read()
    pg_b = None if ref3 else paginas_biblio(txt)
    pg_r = paginas_ref3(txt) if ref3 else None
    res = []
    for i, n in enumerate(d['notas'], 1):
        m = re.search(r'(?:PÁGINA PDF |^)(\d+)', str(n.get('pagina', '')))
        if not m:
            continue
        p = int(m.group(1))
        pag = pg_r.get(n.get('archivo'), {}) if ref3 else pg_b
        if p not in pag:
            continue
        ventana = '\n'.join(pag.get(q, '') for q in (p - 1, p, p + 1))
        pagina_sola = pag.get(p, '')
        t_nota = tallos(str(n.get('titulo', '')) + ' ' + str(n.get('contenido', '')) + ' ' + str(n.get('postura', '')))
        t_vent = tallos(ventana)
        cob = len(t_nota & t_vent) / len(t_nota) if t_nota else 1.0
        cob_sola = len(t_nota & tallos(pagina_sola)) / len(t_nota) if t_nota else 1.0
        nums = numeros(str(n.get('contenido', '')) + ' ' + str(n.get('titulo', '')))
        falt = sorted(x for x in nums if not re.search(r'(?<!\d)' + x + r'(?!\d)', ventana))
        res.append({'bloque': bid, 'n': i, 'titulo': n.get('titulo', ''), 'ref': n.get('ref', ''), 'cob': round(cob, 2), 'cob_sola': round(cob_sola, 2),
                    'numeros_faltantes': falt, 'pagina': n.get('pagina', ''), 'palabras': len(str(n.get('contenido', '')).split())})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref3', action='store_true')
    ap.add_argument('--bloque', nargs='*')
    ap.add_argument('--peor', type=int, default=25)
    ap.add_argument('--umbral', type=float, default=0.35)
    ap.add_argument('--solo-resumen', action='store_true')
    a = ap.parse_args()
    carpeta = os.path.join(C.REPO_TRABAJO, 'extracciones_ref3' if a.ref3 else 'extracciones')
    rutas = sorted(glob.glob(os.path.join(carpeta, '*.json')))
    if a.bloque:
        rutas = [r for r in rutas if os.path.basename(r)[:-5] in a.bloque]
    todas = []
    print(f"{'bloque':16s} {'notas':>5s} {'cob.mediana':>11s} {'<umbral':>8s} {'núm.faltan':>10s}")
    for r in rutas:
        res = analizar(r, a.ref3)
        todas += res
        if not res:
            continue
        cobs = [x['cob'] for x in res]
        bajas = sum(1 for c in cobs if c < a.umbral)
        nf = sum(1 for x in res if x['numeros_faltantes'])
        print(f"{res[0]['bloque']:16s} {len(res):5d} {statistics.median(cobs):11.2f} {bajas:8d} {nf:10d}")
    if todas:
        cobs = [x['cob'] for x in todas]
        print(f"TOTAL {len(todas)} notas | cobertura mediana {statistics.median(cobs):.2f} | bajo el umbral {sum(1 for c in cobs if c < a.umbral)} | con números que no están en la página {sum(1 for x in todas if x['numeros_faltantes'])}")
    if a.solo_resumen:
        return
    print(f'\n--- las {a.peor} notas de menor cobertura ---')
    for x in sorted(todas, key=lambda x: x['cob'])[:a.peor]:
        print(f"{x['bloque']}#{x['n']} cob {x['cob']} (sola {x['cob_sola']}) · {x['ref']} · {x['titulo'][:60]} · pág {x['pagina']}")
    conn = [x for x in todas if x['numeros_faltantes']]
    print(f'\n--- notas con números que la página no trae ({len(conn)}), primeras 25 ---')
    for x in conn[:25]:
        print(f"{x['bloque']}#{x['n']} {x['numeros_faltantes']} · {x['titulo'][:60]} · pág {x['pagina']}")


if __name__ == '__main__':
    main()
