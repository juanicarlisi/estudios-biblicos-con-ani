#!/usr/bin/env python3
"""Arma el material de cada artículo (introducciones I1-I5, panoramas P1-P3, temas T1-T6) a partir de las notas fuera de los días:
notas «intro»/«1P intro», «tema»/«1J tema» y las de más de 12 versículos (más, para los temas, las notas de los días que
coinciden con sus palabras clave y tipos). Salida: SCRATCH/pj_insumos/art_<ID>.txt"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U, pesos
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
AQUI = os.path.dirname(os.path.abspath(__file__)); OUT = S + '/pj_insumos'; os.makedirs(OUT, exist_ok=True)
FUENTES = json.load(open(AQUI + '/../plan/fuentes_comentarios.json'))
ARTS = {a['id']: a for a in json.load(open(AQUI + '/../plan/articulos.json'))}
TOPE = int(os.environ.get('TOPE', 130000))
KW = {
 'I1': r'epístolas? (generales|católicas|universales)|canon|canónic|antilegomena|Eusebio|Orígenes|disputad|común|todas estas cartas',
 'I2': r'autor|Pedro|Silvano|Silas|fecha|Nerón|Babilonia|Roma|destinatari|expatriad|dispersi|Ponto|Galacia|Capadocia|Bitinia|propósito|bosquejo|estructura',
 'I3': r'autor|autentic|seud[óo]nim|pseud|canon|estilo|fecha|1:14|destinatari|3:1|Judas|propósito|bosquejo|estructura|Simeón',
 'I4': r'autor|anciano|presbítero|apóstol Juan|evangelio de Juan|fecha|Éfeso|gnostic|docet|Cerinto|salieron de nosotros|señora elegida|Gayo|Diótrefes|Demetrio|propósito|espiral|estructura|bosquejo',
 'I5': r'autor|hermano de Jacobo|hermano del Señor|fecha|destinatari|Enoc|Asunción de Moisés|apócrif|seudoepígraf|canon|tríada|propósito|bosquejo|estructura|contend',
 'T1': r'sufr|padec|persecuci|prueba|fuego|aflicci|gloria|injust|mártir|odio del mundo|aborrec',
 'T2': r'falsos? (maestros|profetas)|apósta|apostas|herej|anticristo|engañador|gnostic|docet|Cerinto|libertin|Balaam|Coré|Caín|Sodoma|ángeles que pecaron|probad los espíritus|perdici',
 'T3': r'amor|verdad|obedien|mandamiento|segurid|certeza|sabemos|perseveran|guardaros|firme vuestra vocación|elecci|comunión|hospitalid|permanec',
 'T4': r'venida|parusía|día del Señor|burlador|escarnecedor|elementos|cielos nuevos|tierra nueva|fin de todas las cosas|último tiempo|postrer|ladrón|juicio|premilen|amilen|posmilen|arrebat|milenio',
 'T5': r'espíritus encarcelados|espíritus en prisión|predicó|descenso|Hades|infierno|bautismo|Noé|no peca|sin pecado|perfecci|santificaci[óo]n entera|pecado de muerte|tres (que dan )?testi|coma joánica|Comma',
 'T6': r'extranjer|peregrin|sacerdocio|piedras vivas|sumis|sujet|autoridad|rey|gobern|siervos|amos|esposas|maridos|mujeres|matrimonio|ancianos|apacentad|dones|hospitalid|obreros',
}
TIPOS = {'I1': {'autoria_fecha', 'estructura', 'contexto'}, 'I2': {'autoria_fecha', 'estructura', 'contexto', 'geografia'},
         'I3': {'autoria_fecha', 'estructura', 'contexto'}, 'I4': {'autoria_fecha', 'estructura', 'contexto', 'falsos_maestros'},
         'I5': {'autoria_fecha', 'estructura', 'contexto', 'extrabiblico'},
         'T1': {'doctrina', 'aplicacion', 'cristo', 'contexto'}, 'T2': {'falsos_maestros', 'interpretacion_discutida', 'doctrina', 'AT_en_NT'},
         'T3': {'doctrina', 'aplicacion', 'interpretacion_discutida'}, 'T4': {'doctrina', 'interpretacion_discutida', 'AT_en_NT'},
         'T5': {'interpretacion_discutida', 'doctrina', 'griego_palabra'}, 'T6': {'aplicacion', 'contexto', 'cultura', 'doctrina'}}
def etq(n):
    pref = n['id'].split('_')[0]
    return FUENTES[pref]['corto'] if pref in FUENTES else 'referencia'
def linea(n):
    return (f"[{n['id']}] {n['ref']} · {n['tipo']} · imp {n['importancia']} · {etq(n)}" + (f" · {n['escuela']}" if n.get('escuela') else '')
            + f" · {n['pagina']}\n{n['titulo']}: {n['contenido']}" + (f" POSTURA: {n['postura']}" if n.get('postura') else '') + '\n')
def libro_nota(n):
    e = U.especial(n['ref'])
    if e: return e[1]
    r = U.rango(n['ref'])
    return U.libro_de(r[0]) if r else None
def main():
    N = pesos.notas(); fuera = []; dentro = []
    for n in N:
        r = U.rango(n['ref'])
        (fuera if U.especial(n['ref']) or not r or r[1] - r[0] + 1 > 12 else dentro).append(n)
    print('notas fuera de los días', len(fuera), '| en días', len(dentro))
    for aid, a in ARTS.items():
        libs = set(a.get('libros') or [])
        txt = lambda n: n['titulo'] + ' ' + n['contenido'] + ' ' + n.get('postura', '')
        if a['grupo'] == 'intro':
            if aid == 'I1': base = [n for n in fuera if U.especial(n['ref']) and U.especial(n['ref'])[1] is None]
            else: base = [n for n in fuera if U.especial(n['ref']) and U.especial(n['ref'])[1] in libs]
            base += [n for n in fuera if not U.especial(n['ref']) and n['tipo'] in TIPOS[aid] and (aid == 'I1' or libro_nota(n) in libs)]
            base = [n for n in base if re.search(KW[aid], txt(n), re.I) or n['tipo'] in ('autoria_fecha', 'estructura')] or base
        elif a['grupo'] == 'panorama':
            ini, fin = U.rango(a['rango'])
            base = [n for n in fuera if (lambda r: r and r[0] <= fin and r[1] >= ini)(U.rango(n['ref']))]
            base += [n for n in fuera if U.especial(n['ref']) and U.especial(n['ref'])[1] in libs and n['tipo'] == 'estructura']
        else:
            pool = fuera + [n for n in dentro if n['tipo'] in TIPOS[aid] and n['importancia'] >= 2]
            base = [n for n in pool if re.search(KW[aid], txt(n), re.I) and (not libs or libro_nota(n) in libs or libro_nota(n) is None)]
        vistos = set(); base = [n for n in base if not (n['id'] in vistos or vistos.add(n['id']))]
        base.sort(key=lambda n: (-n['importancia'], n in dentro, -len(n['contenido'])))
        out = []; tot = 0
        for n in base:
            l = linea(n)
            if tot + len(l) > TOPE: break
            out.append(l); tot += len(l)
        open(f'{OUT}/art_{aid}.txt', 'w').write(f"# ARTÍCULO {aid}: {a['titulo']} ({a['rango']})\n# Alcance: {a['alcance']}\n\n" + '\n'.join(out))
        print(aid, len(base), '->', len(out), tot)
if __name__ == '__main__': main()
