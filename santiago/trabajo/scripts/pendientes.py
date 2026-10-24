#!/usr/bin/env python3
"""Qué bloques de lectura faltan extraer, y el prompt exacto para lanzar a cada agente.

Uso:
  pendientes.py                 → lista los bloques de plan/cola_extraccion.txt que todavía no tienen su archivo en extracciones/ o extracciones_ref3/
  pendientes.py --prompt ID     → imprime el prompt del agente para ese bloque (b = biblioteca, r = REFERENCIA3, p = puente)
  pendientes.py --verificar     → compara los bloques de TMP/segmentos con plan/bloques_manifest.json (sha1)
Los bloques de lectura (TMP/segmentos/...) se regeneran con los scripts de ESTADO.md si la sesión es nueva.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

RAIZ = C.REPO_TRABAJO
PROMPTS = {
    'b': ("Sos parte del equipo que arma un estudio bíblico de la carta de Santiago a partir de la biblioteca del fundador. Primero leé con Read las instrucciones completas en "
          "{raiz}/scripts/prompts/extraer_biblio.md y seguilas al pie de la letra (trabajo directo, sin deliberar; notas escritas en tandas con Write; después unir_partes.py y el validador).\n\n"
          "Bloque a procesar: {id} (archivo {tmp}/segmentos/biblio/{id}.txt).\n\nAl terminar respondé solo una línea: id, cantidad de notas, errores y avisos pendientes."),
    'r': ("Sos parte del equipo que arma un estudio bíblico de la carta de Santiago a partir de los libros de referencia del fundador (LIBROS-REFERENCIA3, solo autores protestantes confiables). "
          "Primero leé con Read las instrucciones completas en {raiz}/scripts/prompts/barrer_ref3.md y seguilas al pie de la letra (trabajo directo, sin deliberar; notas escritas en tandas con Write; "
          "después unir_partes.py --ref3 y el validador --ref3).\n\nBloque a procesar: {id} (archivo {tmp}/segmentos/ref3/{id}.txt).\n\n"
          "Al terminar respondé solo una línea: id, cantidad de notas, errores y avisos pendientes."),
    'p': ("Sos parte del equipo que arma un estudio bíblico de la carta de Santiago a partir de la biblioteca del fundador. Primero leé con Read las instrucciones completas en "
          "{raiz}/scripts/prompts/extraer_puentes.md (y las de extraer_biblio.md que esas remiten) y seguilas al pie de la letra.\n\n"
          "Bloque puente a procesar: {id} (archivo {tmp}/segmentos/biblio/{id}.txt).\n\nAl terminar respondé solo una línea: id, cantidad de notas, errores y avisos pendientes."),
}


def cola():
    out = []
    for l in open(os.path.join(RAIZ, 'plan', 'cola_extraccion.txt')):
        if l.strip() and not l.startswith('#'):
            t, i = l.split()[:2]
            out.append((t, i))
    return out


def hecho(t, i):
    carpeta = 'extracciones_ref3' if t == 'r' else 'extracciones'
    return os.path.exists(os.path.join(RAIZ, carpeta, i + '.json'))


def verificar():
    """Compara los bloques de lectura regenerados (TMP/segmentos) con el manifiesto guardado: tienen que ser idénticos para que las notas ya extraídas sigan valiendo."""
    import hashlib, json
    man = json.load(open(os.path.join(RAIZ, 'plan', 'bloques_manifest.json')))
    mal, falta = [], []
    for b, m in man.items():
        ruta = os.path.join(C.TMP, 'segmentos', m['carpeta'], b + '.txt')
        if not os.path.exists(ruta):
            falta.append(b); continue
        if hashlib.sha1(open(ruta, 'rb').read()).hexdigest() != m['sha1']:
            mal.append(b)
    print(f'{len(man) - len(mal) - len(falta)} de {len(man)} bloques coinciden con el manifiesto')
    if falta:
        print('  faltan:', ' '.join(falta))
    if mal:
        print('  DISTINTOS (los rangos de páginas o el texto cambiaron; no lanzar agentes sobre ellos hasta entender por qué):', ' '.join(mal))


def main():
    if '--verificar' in sys.argv:
        verificar(); return
    if '--prompt' in sys.argv:
        i = sys.argv[sys.argv.index('--prompt') + 1]
        t = dict((b, a) for a, b in cola())[i]
        print(PROMPTS[t].format(raiz=RAIZ, tmp=C.TMP, id=i))
        return
    q = cola()
    pend = [(t, i) for t, i in q if not hecho(t, i)]
    print(f'{len(q) - len(pend)} de {len(q)} bloques ya extraídos | faltan {len(pend)}')
    for t in 'brp':
        ids = [i for tt, i in pend if tt == t]
        if ids:
            print(f"  {dict(b='biblioteca', r='REFERENCIA3', p='puentes')[t]} ({len(ids)}): {' '.join(ids)}")


if __name__ == '__main__':
    main()
