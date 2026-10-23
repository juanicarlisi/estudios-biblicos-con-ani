#!/usr/bin/env python3
"""Escribe los textos fijos de la app (varon/textos/como-usar.json y fuentes.json) con los números reales del trabajo."""
import json, glob, os, re

V = '/home/user/trabajo/varon'


def miles(n):
    return f'{n:,}'.replace(',', '.')


def main():
    obras = {json.loads(l)['archivo'] for l in open(f'{V}/puntajes.jsonl')}
    paginas = sum(1 for _ in open(f'{V}/puntajes.jsonl'))
    fuentes = json.load(open(f'{V}/bloques/_fuentes.json'))
    pags_sel = sum(len(re.findall(r'^=== \[', open(f, errors='ignore').read(), re.M)) for f in glob.glob(f'{V}/bloques/[bo]_*.txt'))
    notas = sum(len(json.load(open(f))['notas']) for f in glob.glob(f'{V}/notas/*.json'))
    web = json.load(open(f'{V}/web/datos.json')) if os.path.exists(f'{V}/web/datos.json') else {}
    n_datos = sum(1 for w in web.values() if w['clase'] == 'dato')
    n_art = sum(1 for w in web.values() if w['clase'] == 'articulo')
    dias = len(glob.glob(f'{V}/dias/dia_*.json'))
    ocr = len(json.load(open(f'{V}/ocr/cola.json'))) + 1 if os.path.exists(f'{V}/ocr/cola.json') else 0

    como = """
<p>Es un estudio para vos, de un día por vez. Cada día lleva entre 20 y 30 minutos. No hace falta apurarse: si un día te deja pensando, quedate ahí.</p>
<h2>Cada día</h2>
<ol>
<li><b>Leé el pasaje.</b> Arriba de todo está la lectura bíblica del día, con un enlace para leerla completa en la Reina-Valera 1960.</li>
<li><b>Recorré el estudio.</b> Los versículos clave aparecen con su texto; las cifras, con su año y su fuente; las frases de los autores, textuales.</li>
<li><b>Terminá con tu vida delante de Dios.</b> «Para tu vida» propone pasos concretos; después vienen tres preguntas para pensar a solas, a veces una o dos para charlar con tu esposa o con un amigo, y una oración breve.</li>
<li><b>Marcalo como terminado.</b> El anillo de arriba muestra cuántos días llevás, y el inicio te lleva siempre al día que sigue.</li>
</ol>
<h2>Las fuentes de cada afirmación</h2>
<p>Al final de cada párrafo hay unas etiquetas chicas con el apellido del autor o el nombre del organismo. Tocalas para ver la obra y la página (o el enlace, si es de la web). Nada está inventado: si algo no tiene fuente, no está.</p>
<h2>Marcar, anotar y dibujar</h2>
<ul>
<li><b>Resaltar:</b> seleccioná un texto y elegí un color. Para sacar un resaltado, tocalo y elegí «Quitar».</li>
<li><b>Nota al costado:</b> seleccioná un texto (o tocá un resaltado) y elegí «Nota». La nota queda al margen, con letra de mano, y la podés editar cuando quieras.</li>
<li><b>Lápiz:</b> en la barra de abajo tocá el lápiz y dibujá encima del texto (subrayar, encerrar, flechas). Hay cuatro tintas; «Borrar» quita trazos y «Deshacer» vuelve atrás. Tocá el lápiz otra vez para volver a leer normalmente.</li>
<li><b>Tus notas del día:</b> al final de cada día hay un espacio para escribir lo que Dios te mostró.</li>
</ul>
<p>Todo se guarda solo en el navegador de esta compu o este teléfono. En «Mis marcas y notas» ves todo lo que marcaste, día por día.</p>
<h2>Guardar y descargar</h2>
<ul>
<li><b>Guardar el estudio con mis marcas</b> (el disquete de arriba): baja el archivo completo con todas tus marcas, notas y avance adentro. Abrilo en cualquier compu y está todo. Es la mejor forma de no perder nada: hacelo cada tanto.</li>
<li><b>Descargar el día</b> (barra de abajo): baja solo ese día, como una página aparte, con tus marcas. Sirve para guardarlo, mandarlo o imprimirlo.</li>
<li><b>PDF o imprimir:</b> abre la ventana de impresión del navegador; ahí elegís «Guardar como PDF».</li>
<li><b>Copia de mis marcas:</b> un archivo chiquito con solo tus marcas, para pasarlas a otro archivo del estudio («Cargar copia» las suma, sin borrar lo que ya tenías).</li>
</ul>
<h2>Leer cómodo</h2>
<p>El botón «Aa» agranda o achica la letra, y el de al lado cambia entre modo claro y oscuro. El buscador encuentra cualquier palabra, tema o versículo en todo el estudio y en tus notas.</p>
"""
    fte = f"""
<p>Este estudio junta lo que enseñan sobre el varón los libros de la biblioteca y de LIBROS-REFERENCIA3, más datos y artículos de sitios confiables. La regla fue no inventar nada: cada afirmación lleva sus fuentes, con la página, y se puede verificar.</p>
<h2>Cómo se armó</h2>
<ol>
<li><b>Todo el material, página por página.</b> Se pasaron a texto las {miles(len(obras))} obras de autores confiables de los dos repositorios ({miles(paginas)} páginas); los {ocr} libros escaneados se leyeron con reconocimiento de texto. Cada página se puntuó según cuánto trata del varón: su identidad, su relación con Dios, el carácter, la pureza, el trabajo, el matrimonio, la paternidad, el ministerio, el servicio, la amistad, las etapas de la vida y la sociedad.</li>
<li><b>Selección.</b> De las carpetas centrales (Hombre, Matrimonio y Familia, Jóvenes, Sexualidad, Liderazgo, Pastorado, Niños, Discipulado, Servicio, Finanzas, Personajes bíblicos y otras) entró casi todo; de las biografías y del resto de los libros y comentarios, las páginas que tratan de lleno el tema. Se sacaron las ediciones repetidas. Quedaron {miles(pags_sel)} páginas de {miles(len(fuentes))} obras.</li>
<li><b>Extracción.</b> Esas páginas se leyeron enteras y de cada enseñanza se tomó una nota con la idea del autor, la frase textual cuando vale la pena, los versículos y la página: {miles(notas)} notas en total.</li>
<li><b>Datos de hoy.</b> Las estadísticas se buscaron primero en organismos argentinos y latinoamericanos (Ministerio de Salud, INDEC, SEDRONAR, UNICEF, CEPAL, OPS) y después internacionales (OMS, Banco Mundial, Pew, Gallup y otros). Solo entraron las que se vieron en la página de la fuente: {miles(n_datos)} datos con su año y su enlace. Se sumaron {miles(n_art)} artículos de sitios cristianos confiables, como Coalición por el Evangelio, Desiring God, 9Marks y Ligonier.</li>
<li><b>El plan.</b> Las notas se ordenaron por tema y se armó el recorrido de días, de modo que cada día enseñe algo propio y no se repita lo de otro. El estudio termina donde se termina el material.</li>
<li><b>Escritura y verificación.</b> Cada día se escribió con todas sus notas, uniendo lo que dicen varios autores y mostrando las posturas cuando no coinciden. Un segundo control cotejó cada afirmación con sus notas y cada cifra con su fuente. Al final se revisó la continuidad entre días.</li>
</ol>
<h2>Qué quedó afuera</h2>
<p>Solo entran autores protestantes confiables. Ya se habían excluido, y borrado de los repositorios, las obras católicas, adventistas, mormonas, de teología de la prosperidad o liberales, las de corriente carismática o con reservas, las de autor desconocido y la ficción. Tampoco se usaron dos resúmenes anónimos de libros de Pink y de Tozer que siguen en LIBROS-REFERENCIA3, porque no son la obra de esos autores. Los datos que no se pudieron confirmar en su fuente se dejaron de lado.</p>
<h2>Líneas de ayuda</h2>
<p>En los días que tratan el suicidio, la depresión, las adicciones, las apuestas o la violencia aparece un recuadro con líneas de ayuda de Argentina. Se tomaron de sus páginas oficiales el 20 de octubre de 2026 (Ministerio de Salud de la Nación, SEDRONAR, Ministerio de Justicia, Lotería de la Ciudad, Lotería de la Provincia de Buenos Aires y Centro de Asistencia al Suicida), cada una con su enlace. Los números pueden cambiar: si los necesitás, confirmalos en esas páginas.</p>
<h2>El texto bíblico</h2>
<p>Los versículos clave son de la Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988. El estudio cita solo los versículos clave; el pasaje completo se lee en tu Biblia o en BibleGateway.</p>
<h2>Tipografías</h2>
<p>Zilla Slab, Source Serif 4, Public Sans, Caveat y Frank Ruhl Libre (SIL Open Font License), incluidas en el archivo para que se vea igual sin internet.</p>
"""
    os.makedirs(f'{V}/textos', exist_ok=True)
    json.dump({'ojo': 'Guía', 'titulo': 'Cómo usar el estudio', 'html': como.strip()}, open(f'{V}/textos/como-usar.json', 'w'), ensure_ascii=False, indent=1)
    json.dump({'ojo': 'Herramientas', 'titulo': 'Fuentes del estudio', 'html': fte.strip()}, open(f'{V}/textos/fuentes.json', 'w'), ensure_ascii=False, indent=1)
    print(f'obras {len(obras)} | páginas {paginas} | seleccionadas {pags_sel} de {len(fuentes)} obras | notas {notas} | datos {n_datos} | artículos {n_art} | días {dias} | OCR {ocr}')


if __name__ == '__main__':
    main()
