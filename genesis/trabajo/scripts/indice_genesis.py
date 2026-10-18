#!/usr/bin/env python3
"""Indexa, página por página, todo lo que toca Génesis en un corpus de textos.

Para cada archivo cuenta citas explícitas de Génesis (con capítulo y versículo, siguiendo las
citas encadenadas con «;») y menciones de personajes, lugares y temas propios del libro.
Salida: JSON con, por archivo, las páginas con señal y su puntaje.
Uso: indice_genesis.py <lista_de_archivos.json> <salida.json>
  lista: [{"id":..., "txt": ruta, "etiqueta": ...}, ...]
"""
import json, re, sys, collections

LIBRO_GN = r'(?:G[ée]nesis|G[ée]n\.?|Gn\.?)'
OTROS = (r'(?:[ÉE]xodo|[ÉE]x\.?|Lev[íi]tico|Lv\.?|N[úu]meros|Nm\.?|Deuteronomio|Dt\.?|Josu[ée]|Jos\.?|Jueces|Jue\.?|Rut|Rt\.?|'
         r'Samuel|S\.|Reyes|R\.|Cr[óo]nicas|Cr\.?|Esdras|Esd\.?|Nehem[íi]as|Neh\.?|Ester|Est\.?|Job|Salmos?|Sal\.?|Proverbios|Pr\.?|'
         r'Eclesiast[ée]s|Ec\.?|Cantares|Cnt\.?|Isa[íi]as|Is\.?|Jerem[íi]as|Jer\.?|Lamentaciones|Lm\.?|Ezequiel|Ez\.?|Daniel|Dn\.?|'
         r'Oseas|Os\.?|Joel|Jl\.?|Am[óo]s|Am\.?|Abd[íi]as|Jon[áa]s|Miqueas|Mi\.?|Nah[úu]m|Habacuc|Hab\.?|Sofon[íi]as|Hageo|Zacar[íi]as|Zac\.?|'
         r'Malaqu[íi]as|Mal\.?|Mateo|Mt\.?|Marcos|Mr\.?|Mc\.?|Lucas|Lc\.?|Juan|Jn\.?|Hechos|Hch\.?|Romanos|Ro\.?|Rom\.?|Corintios|Co\.?|Cor\.?|'
         r'G[áa]latas|G[áa]\.?|Efesios|Ef\.?|Filipenses|Fil\.?|Colosenses|Col\.?|Tesalonicenses|Ts\.?|Tes\.?|Timoteo|Ti\.?|Tim\.?|Tito|Tit\.?|'
         r'Filem[óo]n|Hebreos|He\.?|Heb\.?|Santiago|Stg\.?|Pedro|P\.|Pe\.?|Judas|Jud\.?|Apocalipsis|Ap\.?|Apoc\.?)')
# Cita de Génesis: libro + cap[:vers[-vers]] y continuaciones «; cap:vers» o «, vers»
RE_GN = re.compile(LIBRO_GN + r'\s*(\d{1,2})(?:\s*[:.,]\s*(\d{1,3})(?:\s*[-–—]\s*(\d{1,3}))?)?')
RE_CONT = re.compile(r'\s*[;,]\s*(?:y\s+)?(\d{1,2})\s*[:.]\s*(\d{1,3})(?:\s*[-–—]\s*(\d{1,3}))?')
RE_OTRO = re.compile(r'\b' + OTROS + r'\s*\d')

# Menciones con peso (nombres y temas casi exclusivos de Génesis pesan más)
FUERTES = ['Adán', 'Edén', 'Caín', 'Abel', 'Matusalén', 'Noé', 'diluvio', 'Babel', 'Abraham', 'Abram', 'Sarai',
           'Sodoma', 'Gomorra', 'Melquisedec', 'Agar', 'Ismael', 'Isaac', 'Rebeca', 'Esaú', 'Jacob', 'Raquel', 'Labán',
           'Potifar', 'Peniel', 'Moriah', 'Moriat', 'Macpela', 'Siquem', 'Betel', 'Mamre', 'Beerseba', 'Harán',
           'Ur de los caldeos', 'protoevangelio', 'imago Dei', 'imagen de Dios', 'árbol de la ciencia',
           'árbol del conocimiento', 'árbol de la vida', 'primogenitura', 'Efraín y Manasés', 'Enoc', 'Lot',
           'Tamar', 'Dina', 'Rubén', 'Benjamín', 'arco iris', 'torre de Babel', 'Simeón y Leví', 'Siloh', 'Elohim',
           'El Shaddai', 'Jehová-jireh', 'Jehová proveerá', 'creación', 'Creación', 'seis días', 'toledot',
           'Edén', 'serpiente', 'fruto prohibido', 'la caída', 'pecado original', 'Eva']
DEBILES = ['José', 'Sara', 'Faraón', 'Judá', 'Set', 'Egipto', 'Canaán', 'patriarca', 'patriarcas', 'pacto',
           'simiente', 'bendición', 'circuncisión', 'altar']
RE_F = re.compile(r'\b(' + '|'.join(re.escape(x) for x in FUERTES) + r')\b')
RE_D = re.compile(r'\b(' + '|'.join(re.escape(x) for x in DEBILES) + r')\b')


def citas(texto):
    out = []
    for m in RE_GN.finditer(texto):
        c = int(m.group(1))
        if not 1 <= c <= 50:
            continue
        out.append((c, int(m.group(2)) if m.group(2) else None))
        pos = m.end()
        while True:
            m2 = RE_CONT.match(texto, pos)
            if not m2:
                break
            # se corta si antes aparece otro libro
            c2 = int(m2.group(1))
            if not 1 <= c2 <= 50:
                break
            out.append((c2, int(m2.group(2))))
            pos = m2.end()
    return out


def main():
    lista = json.load(open(sys.argv[1]))
    res = {}
    for it in lista:
        try:
            pags = open(it['txt'], errors='ignore').read().split('\f')
        except FileNotFoundError:
            continue
        info = []
        for n, p in enumerate(pags, 1):
            cs = citas(p)
            f = RE_F.findall(p)
            d = RE_D.findall(p)
            score = 3 * len(cs) + len(f) + 0.3 * len(d)
            if cs or len(f) >= 2:
                caps = collections.Counter(c for c, _ in cs)
                info.append({'pag': n, 'score': round(score, 1), 'citas': [f'{c}:{v}' if v else f'{c}' for c, v in cs][:40],
                             'caps': dict(caps), 'menciones': dict(collections.Counter(f).most_common(8))})
        tot = len(pags)
        res[it['id']] = {'etiqueta': it.get('etiqueta'), 'txt': it['txt'], 'paginas_total': tot,
                         'paginas_con_senal': len(info), 'citas_total': sum(len(x['citas']) for x in info),
                         'score_total': round(sum(x['score'] for x in info), 1), 'paginas': info}
    json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False)
    print(len(res), 'archivos indexados')


if __name__ == '__main__':
    main()
