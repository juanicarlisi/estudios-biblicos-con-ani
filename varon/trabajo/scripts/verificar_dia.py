#!/usr/bin/env python3
"""Verificación por programa (sin IA) de los días escritos: reemplaza al verificador de IA día por día.

Controla, por cada texto del día con sus fuentes:
  ids        los ids citados existen en el insumo del día y los párrafos llevan fuentes;
  cifras     cada número (≥10 o con decimales) está en las fuentes citadas (o, al menos, en el insumo);
  comillas   cada frase entre «» (≥4 palabras) está en las fuentes citadas o en el texto RVR1960 de algún capítulo citado;
  autores    cada autor de la biblioteca nombrado figura entre las fuentes citadas del texto;
  apoyo      las palabras de contenido del párrafo aparecen en las fuentes citadas (detecta lo que las notas no dicen);
  biblia     las referencias «Libro C:V» existen (capítulo y versículo) en la RVR1960;
  forma      largo, cantidades, «vos», sin «ESTIMACIÓN propia».
Salida: varon/revision/verif/dia_NNN.json {ok, flags:[{ruta,tipo,detalle}]}; un resumen de una línea por corrida.
Uso: verificar_dia.py [--borradores|--dias] [dia ...]   (por defecto: todos los de dias/borradores/)
"""
import json, os, re, sys, glob, collections
V = '/home/user/trabajo/varon'
sys.path.insert(0, f'{V}/scripts')
from dia_util import unidades, insumo, norm, capitulo, traer_capitulos, refs_en, RE_REF  # noqa: E402
from rvr import normalizar  # noqa: E402

VACIAS = set(norm("""a al algo ante antes aquel aqui asi aun aunque cada como con contra cual cuando de del desde donde dos el ella ellas ellos en entre era es esa ese eso
esta este esto estos estas fue han hasta hay la las le les lo los mas me mi muy no nos o otra otro para pero poco por porque que se sea ser si sin sino sobre son su sus tambien tan tanto te
tiene todo todos tu un una uno unos y ya vos tu tus vas va ver hace hacer puede debe dice dijo hay esto eso hoy dia dias cada algun alguna cosa cosas""").split())
VERBOS = 'dice|cuenta|explica|señala|afirma|escribe|advierte|enseña|propone|plantea|observa|recuerda|destaca|sostiene|sugiere|insiste|agrega|aclara|define|llama|cree|piensa|aconseja|muestra|relata|describe|distingue|resume|pregunta|pide|reconoce|admite|subraya|ve|lo ve|lo llama|lo resume|nota|dedica|compara|usa|critica|lamenta|propone'
SECUNDARIAS = 0.15     # proporción mínima de palabras de contenido respaldadas por las fuentes
MIN_PALABRAS_APOYO = 22


def stems(t):
    return {w[:5] for w in norm(t).split() if len(w) >= 5 and w not in VACIAS}


def apellidos():
    f = json.load(open(f'{V}/bloques/_fuentes.json'))
    out = {}
    for v in f.values():
        for a in re.split(r'\s+y\s+|,|\(', v.get('autor') or ''):
            w = a.strip().split()
            if len(w) >= 2 and w[-1][0].isupper() and len(w[-1]) > 3:
                out.setdefault(norm(w[-1]), set()).add(norm(v['autor']))
    for k in ('moody', 'beacon', 'mundo', 'varios', 'moore', 'smith', 'white', 'black', 'young', 'king', 'jones'):
        out.pop(k, None)
    return out


def solo_cifras(t):
    return {re.sub(r'\D', '', m) for m in re.findall(r'\d[\d.,]*\d|\d', t)}


def numeros(texto):
    """Cifras del texto (sin referencias bíblicas ni «día N»), solo dígitos; se ignoran los números chicos sueltos."""
    t = RE_REF.sub(' ', texto)
    t = re.sub(r'\b\d+:\d+(?:[-–]\d+)?', ' ', t)
    t = re.sub(r'\b(?:d[ií]as?|cap[ií]tulos?|vers[ií]culos?|salmos?|parte|partes)\s+\d+(?:\s*(?:,|y|a|al|e|o|–|-)\s*\d+)*', ' ', t, flags=re.I)
    out = []
    for m in re.findall(r'\d[\d.,]*\d|\d', t):
        d = re.sub(r'\D', '', m)
        if len(m) >= 3 or (len(d) >= 2 and int(d) >= 10):
            out.append(d)
    return out


def verificar(d, base='borradores', AUT=None):
    x = json.load(open(f'{V}/dias/{base}/dia_{d:03d}.json')) if base != 'dias' else json.load(open(f'{V}/dias/dia_{d:03d}.json'))
    ins = insumo(d)
    todo_ins = norm(' '.join(ins.values()))
    flags = []
    texto_unidades = unidades(x)
    # capítulos RVR de este día (los que cita el texto)
    refs = [v['ref'] for v in x.get('versiculos', [])] + [x.get('lectura', {}).get('pasaje', '')]
    for _, t, _ in texto_unidades:
        refs += [s for s, _ in refs_en(t)]
    caps = {}
    for r in refs:
        n = normalizar(r) if r else None
        if n:
            (nombre, osis), c, v1, v2 = n
            if (osis, c) not in caps:
                caps[(osis, c)] = capitulo((osis, nombre, c)) or {}
    rvr_norm = norm(' '.join(' '.join(v.values()) for v in caps.values()))
    cuerpo = 0
    for ruta, t, fu in texto_unidades:
        if not ruta.startswith(('bajada', 'lectura', 'versiculos', 'para_', 'profundizar')) and not ruta.endswith('titulo'):
            cuerpo += len(t.split())
        fuentes = [i for i in (fu or [])]
        malos = [i for i in fuentes if i not in ins and re.match(r'^(?:[bo]_\d+#\d+|W\d+)$', i)]
        if malos:
            flags.append((ruta, 'ids', f'ids que no están en el insumo: {malos[:4]}'))
        citado = norm(' '.join(ins.get(i, '') for i in fuentes)) if fuentes else ''
        # cifras
        if fuentes:
            raw = ' '.join(ins.get(i, '') for i in fuentes)
            c_cit, c_all = solo_cifras(raw), solo_cifras(' '.join(ins.values()))
            for n in numeros(t):
                if n not in c_cit and n not in c_all:
                    flags.append((ruta, 'cifras', f'la cifra {n} no está en el insumo'))
        # comillas «»
        for q in re.findall(r'«([^»]{12,})»', t):
            if re.search(r'[¿¡?!]', q):
                continue
            for frag in re.split(r'…|\.\.\.|\[\.\.\.\]', q):
                if len(frag.split()) >= 6:
                    qn = norm(frag)
                    if qn not in citado and qn not in rvr_norm and qn not in todo_ins:
                        flags.append((ruta, 'comillas', f'«{frag.strip()[:70]}» no está en las fuentes ni en la RVR de los capítulos citados'))
                        break
        # autores
        if AUT and fuentes:
            for ap, autores in AUT.items():
                cap = ap.capitalize()
                if re.search(rf'\b[Ss]eg[uú]n\s+(?:[A-ZÁÉÍÓÚ]\w+\s+)?{cap}\b|\b{cap}\s+(?:{VERBOS})\b', t) and not re.search(rf'\b{re.escape(ap)}\b', citado):
                    flags.append((ruta, 'autor', f'atribuye algo a {ap} pero no figura en sus fuentes'))
                    break
        # apoyo léxico (sin lo que va entre «», que se controla aparte); sin fuentes: contra todo el insumo
        if len(t.split()) >= MIN_PALABRAS_APOYO and ruta.endswith('.texto') and not ruta.startswith('profundizar'):
            s_ = stems(re.sub(r'«[^»]*»', ' ', t))
            base = citado if fuentes else todo_ins
            if len(s_) >= 12:
                r = len(s_ & stems(base)) / len(s_)
                if r < (SECUNDARIAS if fuentes else 0.30):
                    flags.append((ruta, 'apoyo' if fuentes else 'ids', f'solo {r:.0%} de sus palabras están en {"las fuentes citadas" if fuentes else "el insumo del día (y no cita fuentes)"}'))
        # biblia
        for s, n in refs_en(t):
            (nombre, osis), c, v1, v2 = n
            cap = caps.get((osis, c))
            if cap is not None and cap and str(v1) not in cap:
                flags.append((ruta, 'biblia', f'{s}: el versículo no existe en la RVR1960'))
            elif cap is not None and not cap:
                flags.append((ruta, 'biblia_sin_dato', f'{s}: no se pudo bajar el capítulo'))
        # forma
        if re.search(r'\b(ustedes|vosotros)\b', re.sub(r'«[^»]*»', ' ', t), re.I):
            flags.append((ruta, 'forma', 'usa «ustedes»/«vosotros»'))
        if 'ESTIMACIÓN' in t or re.search(r'\bestimaci[oó]n propia', t.lower()):
            flags.append((ruta, 'forma', 'usa una estimación propia'))
    if not 1700 <= cuerpo <= 2800:
        flags.append(('cuerpo', 'largo', f'{cuerpo} palabras'))
    if not 1 <= len(x.get('versiculos', [])) <= 3:
        flags.append(('versiculos', 'forma', 'deben ser 1 a 3'))
    if len(x.get('para_reflexionar', [])) != 3:
        flags.append(('para_reflexionar', 'forma', 'deben ser 3'))
    if not 3 <= len(x.get('apartados', [])) <= 7:
        flags.append(('apartados', 'forma', f'{len(x.get("apartados", []))} apartados'))
    for v in x.get('versiculos', []):
        r = v['ref']
        if not normalizar(r) and not normalizar(re.sub(r'[-–]\d+:\d+$', '', r)) and not re.match(r'^(?:[123]\s)?[A-Za-zÁÉÍÓÚáéíóúñ]+\s\d+(?:[-–]\d+)?$', r):
            flags.append(('versiculos', 'biblia', f'referencia no reconocida {r}'))
    return [{'ruta': r, 'tipo': t, 'detalle': dt} for r, t, dt in flags], cuerpo


def main():
    args = sys.argv[1:]
    base = 'dias' if '--dias' in args else 'borradores'
    ds = [int(a) for a in args if a.isdigit()] or sorted(int(os.path.basename(f)[4:7]) for f in glob.glob(f'{V}/dias/{"" if base == "dias" else "borradores/"}dia_*.json'))
    AUT = apellidos()
    os.makedirs(f'{V}/revision/verif', exist_ok=True)
    # 1) capítulos faltantes, todos de una vez (sin IA, con varios hilos)
    refs = []
    for d in ds:
        try:
            x = json.load(open(f'{V}/dias/{"" if base == "dias" else "borradores/"}dia_{d:03d}.json'))
        except OSError:
            continue
        refs += [v['ref'] for v in x.get('versiculos', [])] + [x.get('lectura', {}).get('pasaje', '')]
        for _, t, _ in unidades(x):
            refs += [s for s, _ in refs_en(t)]
    ok, tot = traer_capitulos(refs)
    cuenta, por_tipo, limpios = 0, collections.Counter(), 0
    for d in ds:
        try:
            fl, cuerpo = verificar(d, base, AUT)
        except (OSError, KeyError) as e:
            continue
        json.dump({'ok': not [f for f in fl if f['tipo'] not in ('cifras_laxo', 'biblia_sin_dato')], 'cuerpo': cuerpo, 'flags': fl}, open(f'{V}/revision/verif/dia_{d:03d}.json', 'w'), ensure_ascii=False)
        cuenta += 1
        por_tipo.update({f['tipo'] for f in fl})
        limpios += not [f for f in fl if f['tipo'] not in ('cifras_laxo', 'biblia_sin_dato')]
    print(f'días {cuenta} | limpios {limpios} | con flags {cuenta - limpios} | días por tipo de flag: {dict(por_tipo)} | capítulos RVR nuevos {ok}/{tot}')


if __name__ == '__main__':
    main()
