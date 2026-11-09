#!/usr/bin/env python3
"""Indexa, página por página, todo lo que toca 1 Pedro, 2 Pedro, 1-3 Juan y Judas en un corpus de textos (páginas separadas por \\f).

Cuenta citas explícitas a los seis libros (con todas sus grafías: «1 Pedro», «1 Pe.», «I Pedro», «1P», «2 Ped.», «1 Juan», «1 Jn»,
«III Juan», «Judas», «Jud.», «Jds»…; sigue las encadenadas con «;») y menciones propias de estos libros: nombres y temas fuertes
(peso 1) y temas generales (peso 1/3, no bastan solos). Salida: JSON por archivo con las páginas con señal y su puntaje.
Uso: indice_pedro_judas.py <lista.json> <salida.json>   (lista: [{"id","txt","etiqueta"}])
     indice_pedro_judas.py --probar "texto"             (muestra citas y menciones de un texto)
"""
import json, re, sys, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidades import VV, sigla

NUM = r'(?:[123]|I{1,3})\s*(?:ª|a\.|era\.?|da\.?)?\s*'
LIBRO = (r'(?P<lib>' + NUM + r'(?:Pedro|Ped\.?|Pe\.?|Pet\.?|P\.?|Juan|Jua\.?|Jn\.?|John|J\.?)'
         r'|Judas|Jud\.?|Jds\.?|Jude|Jd\.?)')
NO_LIB = r'(?!\d)(?!\s*[ªa]?\.?\s*[A-Za-zÁ-úñ]{1,8}\.?\s*\d)'   # el número no es el ordinal del libro siguiente («9, 2 Jn 7»)
RE_CITA = re.compile(r'(?<![A-Za-zÁ-úñ\d])' + LIBRO + r'\s*(\d{1,2})' + NO_LIB + r'(?:\s*[:.,]\s*(\d{1,3})' + NO_LIB + r'(?:\s*[-–—]\s*(\d{1,3}))?)?')
RE_CONT = re.compile(r'\s*[;,]\s*(?:y\s+)?(\d{1,2})' + NO_LIB + r'(?:\s*[:.]\s*(\d{1,3}))?(?:\s*[-–—]\s*(\d{1,3}))?')

def _sig(txt):
    t = re.sub(r'\s|\.', '', txt).replace('ª', '').lower()
    t = re.sub(r'^(\d|i{1,3})(?:a|era|da)(?=[a-z])', r'\1', t)
    t = {'jds': 'jd', 'jude': 'jd'}.get(t, t)
    t = re.sub(r'^(\d|i{1,3})(?:pet|pe|ped|pedro|p)$', lambda m: m.group(1) + 'p', t)
    t = re.sub(r'^(\d|i{1,3})(?:john|jua|juan|jn|j)$', lambda m: m.group(1) + 'j', t)
    t = t.replace('iii', '3').replace('ii', '2').replace('i', '1') if re.match(r'^i{1,3}[pj]$', t) else t
    return sigla(t)

FUERTES = ['extranjeros y peregrinos', 'expatriados', 'expatriados de la dispersión', 'la dispersión', 'esperanza viva', 'renacer',
           'renacidos', 'nacido de nuevo', 'nacidos de nuevo', 'nacer de nuevo', 'nuevo nacimiento', 'regeneración', 'piedras vivas',
           'piedra viva', 'piedra angular', 'piedra de tropiezo', 'real sacerdocio', 'sacerdocio santo', 'linaje escogido', 'nación santa',
           'pueblo adquirido', 'espíritus encarcelados', 'espíritus en prisión', 'descenso a los infiernos', 'descendió a los infiernos',
           'descendió al infierno', 'Silvano', 'Silas', 'Ponto', 'Capadocia', 'Bitinia', 'Galacia', 'Asia Menor', 'Nerón', 'Simón Pedro',
           'Simeón Pedro', 'falsos maestros', 'falsos profetas', 'apostasía', 'apóstatas', 'escarnecedores', 'burladores',
           'día del Señor', 'cielos nuevos', 'nuevos cielos', 'tierra nueva', 'los elementos', 'transfiguración', 'monte santo',
           'palabra profética', 'interpretación privada', 'Balaam', 'Coré', 'Caín', 'Sodoma', 'Gomorra', 'Enoc', 'libro de Enoc',
           '1 Enoc', 'Asunción de Moisés', 'arcángel Miguel', 'Miguel', 'ángeles que pecaron', 'Tártaro', 'hermano de Jacobo',
           'contendáis ardientemente', 'contender por la fe', 'la fe que ha sido una vez dada', 'anticristo', 'anticristos',
           'espíritu del anticristo', 'unción del Santo', 'la unción', 'propiciación', 'Abogado', 'gnosticismo', 'gnósticos',
           'gnóstico', 'protognósticos', 'docetismo', 'docetas', 'docético', 'Cerinto', 'Diótrefes', 'Gayo', 'Demetrio',
           'señora elegida', 'el anciano', 'el Presbítero', 'perfecto amor', 'pecado de muerte', 'pecado que no es de muerte',
           'mandamiento nuevo', 'Dios es amor', 'Dios es luz', 'Verbo de vida', 'Palabra de vida', 'andar en luz', 'andemos en luz',
           'luz y tinieblas', 'agua y sangre', 'tres que dan testimonio', 'Comma Johanneum', 'coma joánica', 'epístolas generales',
           'epístolas católicas', 'epístolas universales', 'epístolas joaninas', 'epístolas juaninas', 'epístolas petrinas',
           'escritos joaninos', 'escritos juaninos', 'anciano Juan', 'Juan el anciano', 'Juan el apóstol', 'apóstol Juan',
           'apóstol Pedro', 'Pedro y Juan', 'Babilonia', 'Marcos, mi hijo', 'sufrimiento injusto', 'padecimientos de Cristo',
           'prueba de fuego', 'fuego de prueba', 'apacentad la grey', 'Príncipe de los pastores', 'león rugiente', 'adversario',
           'participantes de la naturaleza divina', 'naturaleza divina', 'mil años como un día', 'como ladrón en la noche',
           'no queriendo que ninguno perezca', 'seudoepigrafía', 'seudónimo', 'pseudónimo', 'canonicidad', 'antilegomena']
TEMAS = ['sufrimiento', 'sufrimientos', 'padecer', 'padecimiento', 'persecución', 'santidad', 'sumisión', 'esperanza', 'herencia',
         'comunión', 'permanecer', 'permanece', 'obediencia', 'mandamientos', 'amor fraternal', 'hospitalidad', 'verdad', 'engañadores',
         'herejía', 'herejías', 'segunda venida', 'venida del Señor', 'parusía', 'juicio', 'vida eterna', 'seguridad de la salvación',
         'certeza de la salvación', 'humildad', 'ancianos', 'pastores', 'dones espirituales', 'bautismo', 'diluvio', 'Noé', 'Lot']
_alt = lambda xs: '|'.join(re.escape(x) for x in sorted(set(xs), key=len, reverse=True))
RE_F = re.compile(r'(?<![A-Za-zÁ-úñ])(' + _alt(FUERTES) + r')(?![A-Za-zÁ-úñ])')
RE_T = re.compile(r'(?<![A-Za-zÁ-úñ])(' + _alt(TEMAS) + r')(?![A-Za-zÁ-úñ])', re.I)

def citas(texto):
    """-> [(sigla, cap, vers|None)]"""
    out = []
    for m in RE_CITA.finditer(texto):
        s = _sig(m.group('lib'))
        if not s: continue
        caps = VV[s]; a = int(m.group(2)); b = m.group(3)
        if len(caps) == 1:
            if b is not None and a == 1 and ':' in m.group(0): c, v = 1, int(b)
            elif b is None: c, v = 1, a
            else:   # «Jud. 6, 9»: dos versículos
                vs = [x for x in (a, int(b)) if 1 <= x <= caps[0]]
                out.extend((s, 1, x) for x in vs); continue
            if not 1 <= v <= caps[0]: continue
        else:
            c = a; v = int(b) if b else None
            if not 1 <= c <= len(caps) or (v and v > caps[c - 1]): continue
        # «P» o «J» solos (p. ej. «1 P 2») son ambiguos fuera de citas con versículo
        if re.fullmatch(r'\s*\S+\s*[PJ]\.?', m.group('lib')) and v is None: continue
        out.append((s, c, v)); pos = m.end()
        while True:
            m2 = RE_CONT.match(texto, pos)
            if not m2: break
            x, y = int(m2.group(1)), m2.group(2)
            if len(caps) == 1:
                if y is not None or not 1 <= x <= caps[0]: break
                out.append((s, 1, x))
            else:
                if y is None or not 1 <= x <= len(caps) or int(y) > caps[x - 1]: break
                out.append((s, x, int(y)))
            pos = m2.end()
    return out

def fmt(c):
    s, cap, v = c
    if len(VV[s]) == 1: return f'{s} {v}'
    return f'{s} {cap}:{v}' if v else f'{s} {cap}'

def puntaje(p):
    cs = citas(p); f = RE_F.findall(p); t = RE_T.findall(p)
    score = 3 * len(cs) + len(f) + len(t) / 3
    senal = bool(cs) or len(f) >= 2 or (len(f) >= 1 and len(t) >= 3)
    return cs, f, t, score, senal

def main():
    if sys.argv[1] == '--probar':
        cs, f, t, s, sen = puntaje(sys.argv[2])
        print('citas', [fmt(c) for c in cs]); print('fuertes', f); print('temas', t); print('score', round(s, 1), 'señal', sen); return
    lista = json.load(open(sys.argv[1])); res = {}
    for it in lista:
        try: pags = open(it['txt'], errors='ignore').read().split('\f')
        except FileNotFoundError: continue
        info = []
        for n, p in enumerate(pags, 1):
            cs, f, t, score, senal = puntaje(p)
            if senal:
                info.append({'pag': n, 'score': round(score, 1), 'citas': [fmt(c) for c in cs][:40],
                             'libros': dict(collections.Counter(c[0] for c in cs)),
                             'menciones': dict(collections.Counter(f).most_common(8))})
        res[it['id']] = {'etiqueta': it.get('etiqueta'), 'txt': it['txt'], 'paginas_total': len(pags),
                         'paginas_con_senal': len(info), 'score_total': round(sum(x['score'] for x in info), 1), 'paginas': info}
    json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False)
    for k, v in sorted(res.items(), key=lambda kv: -kv[1]['score_total'])[:40]:
        print(f"{v['score_total']:8.0f} {v['paginas_con_senal']:4d}/{v['paginas_total']:5d}  {k[:90]}")

if __name__ == '__main__': main()
