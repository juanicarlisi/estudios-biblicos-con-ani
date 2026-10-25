#!/usr/bin/env python3
"""Indexa, página por página, todo lo que toca Apocalipsis en un corpus de textos (páginas separadas por \\f).

Cuenta citas explícitas (con capítulo y versículo, siguiendo las encadenadas con «;») y menciones de
nombres y temas propios del libro. Salida: JSON por archivo con las páginas con señal y su puntaje.
Uso: indice_apocalipsis.py <lista.json> <salida.json>   (lista: [{"id","txt","etiqueta"}])
"""
import json, re, sys, collections

LIBRO = r'(?:Apocalipsis|Apoc\.?|Ap\.?|Revelaci[óo]n|Rev\.?|Revelation)'
RE_AP = re.compile(r'(?<![A-Za-zÁ-úñ])' + LIBRO + r'\s*(\d{1,2})(?:\s*[:.,]\s*(\d{1,3})(?:\s*[-–—]\s*(\d{1,3}))?)?')
RE_CONT = re.compile(r'\s*[;,]\s*(?:y\s+)?(\d{1,2})\s*[:.]\s*(\d{1,3})(?:\s*[-–—]\s*(\d{1,3}))?')
FUERTES = ['Apocalipsis', 'Armagedón', 'Armagedon', 'Har-Magedón', 'Babilonia la grande', 'Gran Babilonia', 'anticristo', 'Anticristo',
           'la bestia', 'marca de la bestia', 'falso profeta', 'gran tribulación', 'milenio', 'milenial', 'milenarismo',
           'premilenial', 'amilenial', 'posmilenial', 'postmilenial', 'arrebatamiento', 'siete iglesias', 'siete sellos', 'siete trompetas',
           'siete copas', 'copas de la ira', 'Laodicea', 'Éfeso', 'Esmirna', 'Pérgamo', 'Tiatira', 'Sardis', 'Filadelfia', 'Patmos',
           '666', '144.000', '144 000', 'dos testigos', 'lago de fuego', 'nueva Jerusalén', 'cielo nuevo', 'cielos nuevos', 'nuevos cielos',
           'tierra nueva', 'segunda venida', 'las bodas del Cordero', 'bodas del Cordero', 'la gran ramera', 'ramera', 'preterismo', 'preterista',
           'historicismo', 'futurismo', 'idealismo', 'dispensacionalismo', 'dispensacional', 'trono blanco', 'Gog y Magog', 'Gog', 'Magog',
           'la mujer vestida del sol', 'el dragón', 'cuatro jinetes', 'jinetes del Apocalipsis', 'siete espíritus', 'candeleros',
           'Alfa y Omega', 'Alfa y la Omega', 'día del Señor', 'setenta semanas', 'Nerón', 'Domiciano', 'culto al emperador', 'nicolaítas',
           'Jezabel', 'Balaam', 'vencedor', 'sellos', 'trompetas', 'ángel de la iglesia', 'ángeles de las iglesias', 'cuatro seres vivientes',
           'veinticuatro ancianos', '24 ancianos', 'mar de vidrio', 'Abadón', 'Apolión', 'el Cordero', 'rapto', 'tribulación']
RE_F = re.compile(r'(?<![A-Za-zÁ-úñ])(' + '|'.join(re.escape(x) for x in sorted(set(FUERTES), key=len, reverse=True)) + r')(?![A-Za-zÁ-úñ])')

def citas(texto):
    out = []
    for m in RE_AP.finditer(texto):
        c = int(m.group(1))
        if not 1 <= c <= 22: continue
        out.append((c, int(m.group(2)) if m.group(2) else None))
        pos = m.end()
        while True:
            m2 = RE_CONT.match(texto, pos)
            if not m2: break
            c2 = int(m2.group(1))
            if not 1 <= c2 <= 22: break
            out.append((c2, int(m2.group(2)))); pos = m2.end()
    return out

def main():
    lista = json.load(open(sys.argv[1])); res = {}
    for it in lista:
        try: pags = open(it['txt'], errors='ignore').read().split('\f')
        except FileNotFoundError: continue
        info = []
        for n, p in enumerate(pags, 1):
            cs = citas(p); f = RE_F.findall(p)
            score = 3 * len(cs) + len(f)
            if cs or len(f) >= 2:
                info.append({'pag': n, 'score': round(score, 1), 'citas': [f'{c}:{v}' if v else f'{c}' for c, v in cs][:40],
                             'menciones': dict(collections.Counter(f).most_common(8))})
        res[it['id']] = {'etiqueta': it.get('etiqueta'), 'txt': it['txt'], 'paginas_total': len(pags),
                         'paginas_con_senal': len(info), 'score_total': round(sum(x['score'] for x in info), 1), 'paginas': info}
    json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False)
    for k, v in sorted(res.items(), key=lambda kv: -kv[1]['score_total'])[:60]:
        print(f"{v['score_total']:8.0f} {v['paginas_con_senal']:4d}/{v['paginas_total']:5d}  {k[:90]}")

if __name__ == '__main__': main()
