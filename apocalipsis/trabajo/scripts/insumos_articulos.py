#!/usr/bin/env python3
"""Arma el material de cada artículo (introducción I1-I5, panoramas P1-P10, temas T1-T14) a partir de las notas fuera de los días:
notas «intro», «tema» y las de más de 12 versículos. Salida: SCRATCH/insumos/art_<ID>.txt"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unidades as U, pesos
S = os.environ.get('SCRATCH', '/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad')
AQUI = os.path.dirname(os.path.abspath(__file__)); OUT = S + '/insumos'
FUENTES = json.load(open(AQUI + '/../plan/fuentes_comentarios.json'))
ARTS = {a['id']: a for a in json.load(open(AQUI + '/../plan/articulos.json'))}
TOPE = int(os.environ.get('TOPE', 130000))
KW = {
 'I1': r'género|apocal[ií]ptic|profec[ií]a|revelaci[óo]n|propósito|mensaje|bienaventuran|lector|destinatari|leer|leyendo',
 'I2': r'autor|Juan|fecha|Domiciano|Nerón|Patmos|destinatari|Asia|persecuci|ireneo|eusebio|tradici|canon',
 'I3': r'símbol|número|siete|Antiguo Testamento|Daniel|Ezequiel|Zacar|alusi|literal|figurad|género|apocal[ií]ptic|interpretar',
 'I4': r'preterist|historicist|futurist|idealist|escuela|método|interpretaci[óo]n|recapitula|progresi',
 'I5': r'estructura|bosquejo|esquema|divisi[óo]n|1:19|recapitula|progresi|septenari|visi[óo]n|capítulo',
 'T1': r'Éfeso|Esmirna|Pérgamo|Tiatira|Sardis|Filadelfia|Laodicea|siete iglesias|ciudad|comercio|emperador|culto|Asia',
 'T2': r'Roma|emperador|Domiciano|Nerón|culto imperial|César|Augusto|persecuci|Calígula|Trajano|Plinio',
 'T3': r'título|Cristo|Cordero|León|Alfa|Omega|Hijo del Hombre|Rey de reyes|Verbo|Fiel y Verdadero|deidad|gloria',
 'T4': r'Antiguo Testamento|Daniel|Ezequiel|Zacar|Isaías|Éxodo|Salmo|alusi|cita|cumplimiento|paralelo',
 'T5': r'número|siete|doce|cuatro|diez|mil|666|144|tres y medio|1260|42 meses|color|símbolo',
 'T6': r'sello|trompeta|copa|septenario|recapitula|paralelo|secuencia|progresi|plaga|Éxodo',
 'T7': r'tribulaci[óo]n|arrebat|rapto|pretribul|postribul|midtribul|iglesia será|4:1|3:10|día del Señor|segunda venida',
 'T8': r'bestia|anticristo|falso profeta|666|hombre de pecado|marca|Nerón|imperio|Daniel 7|Daniel 9',
 'T9': r'Israel|iglesia|144|tribus|judío|pueblo de Dios|nuevo Israel|reemplazo|dispensac|remanente|sellad',
 'T10': r'Babilonia|ramera|Roma|siete montes|siete colinas|ciudad|Éufrates|gran ciudad',
 'T11': r'milenio|mil años|premilen|amilen|posmilen|primera resurrecci|atado|Satanás atado|reino',
 'T12': r'juicio final|infierno|segunda muerte|lago de fuego|Hades|castigo eterno|aniquil|trono blanco|libro de la vida',
 'T13': r'Jerusalén|cielo nuevo|tierra nueva|nueva creaci|Edén|árbol de la vida|eternidad|templo|dimensiones|estadios',
 'T14': r'adoraci[óo]n|perseveranc|vencedor|mártir|paciencia|testimonio|himno|cántico|victoria|fidelidad|resistir',
}
def etq(n):
    pref = n['id'].split('_')[0]
    return (FUENTES[pref]['corto'] if pref in FUENTES else 'referencia')
def linea(n):
    return (f"[{n['id']}] {n['ref']} · {n['tipo']} · imp {n['importancia']} · {etq(n)}" + (f" · {n['escuela']}" if n.get('escuela') else '')
            + f" · {n['pagina']}\n{n['titulo']}: {n['contenido']}" + (f" POSTURA: {n['postura']}" if n.get('postura') else '') + '\n')
def main():
    N = pesos.notas(); fuera = []
    for n in N:
        r = U.rango(n['ref'])
        if n['ref'] in ('intro', 'tema') or not r or r[1] - r[0] + 1 > 12: fuera.append(n)
    print('notas fuera de los días', len(fuera))
    for aid, a in ARTS.items():
        if a['grupo'] == 'intro':
            base = [n for n in fuera if n['ref'] == 'intro'] + [n for n in fuera if n['ref'] == 'tema' and n['tipo'] in ('escuelas_interpretacion', 'estructura_bosquejo')]
            if aid == 'I4': base = [n for n in fuera if n['tipo'] == 'escuelas_interpretacion' or re.search(KW['I4'], n['titulo'] + n['contenido'], re.I)]
            else: base = [n for n in base if re.search(KW[aid], n['titulo'] + ' ' + n['contenido'], re.I)] or base
        elif a['grupo'] == 'panorama':
            ini, fin = U.rango(a['rango'].replace('–', '-'))
            base = []
            for n in fuera:
                r = U.rango(n['ref'])
                if r and r[0] <= fin and r[1] >= ini: base.append(n)
        else:
            base = [n for n in fuera if re.search(KW[aid], n['titulo'] + ' ' + n['contenido'] + ' ' + n.get('postura', ''), re.I)]
            rr = U.rango(a['rango']) if a['rango'] != 'libro' else None
            if rr:
                base = [n for n in base if (lambda r: (not r) or (r[0] <= rr[1] and r[1] >= rr[0]))(U.rango(n['ref']))]
        base.sort(key=lambda n: (-n['importancia'], -len(n['contenido'])))
        out = []; tot = 0
        for n in base:
            l = linea(n)
            if tot + len(l) > TOPE: break
            out.append(l); tot += len(l)
        open(f'{OUT}/art_{aid}.txt', 'w').write(f"# ARTÍCULO {aid}: {a['titulo']} ({a['rango']})\n\n" + '\n'.join(out))
        print(aid, len(base), '->', len(out), tot)
if __name__ == '__main__': main()
