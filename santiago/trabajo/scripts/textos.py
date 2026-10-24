#!/usr/bin/env python3
"""Escribe los textos fijos del estudio (cómo usar, fuentes) con los números reales: días, notas, bloques, obras.
Uso: textos.py   → santiago/trabajo/textos/como-usar.json y fuentes.json
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

T = C.REPO_TRABAJO


def contar(carpeta):
    n, b = 0, 0
    for f in glob.glob(f'{T}/{carpeta}/*.json'):
        b += 1; n += len(json.load(open(f))['notas'])
    return n, b


def main():
    plan = json.load(open(f'{T}/plan/plan.json'))
    arts = json.load(open(f'{T}/plan/articulos.json'))
    n_dias = len(plan)
    n_bib, b_bib = contar('extracciones'); n_ref, b_ref = contar('extracciones_ref3')
    n_unicos = len({(p['desde'], p['hasta']) for p in plan})
    compartidos = sum(1 for p in plan if p.get('compartido') and p['compartido']['n'] == 1)
    n_intro = sum(1 for a in arts if a['grupo'] == 'intro'); n_temas = sum(1 for a in arts if a['grupo'] == 'tema'); n_anex = sum(1 for a in arts if a['grupo'] == 'anexo')
    uno = sum(1 for p in plan if p['desde'] == p['hasta'])
    como = f"""
<p>El plan recorre toda la carta de Santiago en {n_dias} días. Cada día está pensado para entre 20 y 30 minutos juntos. No hay un tope de versículos por día: algunos días recorren un tramo entero y otros ({uno} en total) se detienen en un solo versículo, porque lo merece{'; y hay pasajes que ocupan varios días seguidos, cada uno con su enfoque' if compartidos else ''}.</p>
<h2>Antes de empezar, y en el camino</h2>
<p>La <a href="#introduccion">introducción</a> tiene {n_intro} capítulos breves: quién escribió la carta, a quién y cuándo, qué clase de carta es, cómo está armada y cómo se relaciona con Jesús y con Pablo. Al comenzar cada una de las cinco partes, el plan les ofrece un panorama. Los <a href="#temas">temas</a> reúnen lo que Santiago enseña de punta a punta y sirven para repasar al terminar una parte; los <a href="#anexos">anexos</a> son material de consulta (cuadros comparativos, personas, imágenes, glosario), y los días enlazan al que les corresponde.</p>
<h2>Un día, paso a paso</h2>
<ol>
<li><b>Ubíquense (2 minutos).</b> El recuadro «Antes · Ahora · Después» cuenta qué pasó, qué pasa hoy y qué viene. Abajo están el dónde y el cuándo.</li>
<li><b>Lean el pasaje (3 a 5 minutos).</b> El texto de la Reina-Valera 1960 está en la misma página; si quieren, pueden mostrar también el griego. Conviene leerlo en voz alta, uno cada día.</li>
<li><b>Estudien (15 a 20 minutos).</b> Empiecen por «El pasaje de un vistazo» y sigan «Versículo por versículo». Los diagramas, las palabras griegas, los ecos de Jesús, las preguntas difíciles y la biblioteca están después: lean las que quieran.</li>
<li><b>Conversen y oren (5 minutos).</b> «Para la vida de ustedes» trae lo práctico, tres preguntas para conversar y una oración.</li>
<li><b>Anoten y marquen.</b> Escriban en «Sus notas del día» lo que les quedó y tóquenlo como terminado.</li>
</ol>
<h2>Cómo ver el avance</h2>
<p>Arriba hay una barra con el avance de todo el estudio. En cada día, una barra de pasos muestra en cuál van y cuánto falta (según lo que ya bajaron de la página). En el inicio y en la columna de la derecha, «La carta de un vistazo»: los 108 versículos de Santiago, uno por cuadradito, que se van pintando de verde a medida que terminan los días. En el índice de la izquierda, cada parte tiene su propia barra.</p>
<h2>Las etiquetas de fuente</h2>
<p>Al final de cada afirmación hay etiquetas como <span class="chip">MacArthur</span> o <span class="chip">Kistemaker</span>. Tóquenlas para ver la obra y la página. Nada del estudio está inventado: todo sale de su biblioteca.</p>
<h2>Si un día les falta tiempo</h2>
<p>Lean el pasaje, el panorama y la sección «Para la vida de ustedes». «Para profundizar» es siempre optativo: sirve para volver otro día o para cuando algo les despierte curiosidad. También pueden imprimir el día con el botón «Imprimir este día».</p>
<h2>Las herramientas</h2>
<p>En el índice, abajo, están <a href="#carta">la carta completa</a> (los cinco capítulos de corrido), los <a href="#mapas">mapas</a>, la <a href="#linea">línea de tiempo</a>, las <a href="#palabras">palabras griegas</a>, un <a href="#claves">gráfico con las palabras de la carta</a>, <a href="#ecos">Santiago y las palabras de Jesús</a>, <a href="#cristo">Cristo en Santiago</a> y el <a href="#buscar">buscador</a>, que busca en los días, la introducción, los temas, los anexos y el texto mismo de la carta (también sirve para escribir un versículo, por ejemplo 2:14, y ver qué día lo estudia).</p>
<h2>Progreso y notas</h2>
<p>El avance y las notas se guardan en el navegador de esta compu. Si se limpian los datos del navegador se pierden: bajen cada tanto una copia con el botón «Descargar copia» del inicio, que también sirve para pasarlos a otra compu con «Cargar copia».</p>
<p>Atajos: con las flechas ← → del teclado pasan de un día al otro.</p>
"""
    fuentes = f"""
<p>Este estudio condensa lo mejor de los libros de su biblioteca. La regla fue no inventar nada: cada afirmación lleva sus fuentes, con la página, y se puede verificar.</p>
<h2>Cómo se armó</h2>
<ol>
<li><b>Lectura completa de los comentarios de Santiago</b> de la biblioteca (MacArthur, Kistemaker, Carballosa y Elizabeth George), de lo que dicen sobre la carta el Comentario Bíblico Mundo Hispano, el Comentario Bíblico Beacon y la Biblia de Estudio MacArthur, y de las entradas del Diccionario Bíblico Mundo Hispano que citan Santiago, página por página. De cada aporte se tomó una nota con el pasaje, la idea del autor y la página: {n_bib:,} notas en {b_bib} bloques de lectura.</li>
<li><b>Barrido de los libros de referencia (LIBROS-REFERENCIA3).</b> De los libros de autores protestantes confiables se buscaron todas las páginas que citan o tratan Santiago y se tomó lo que cada autor enseña sobre un pasaje o un tema de la carta: {n_ref:,} notas en {b_ref} bloques.</li>
<li><b>Un plan según el material.</b> En lugar de repartir los versículos por igual, se midió cuánto material hay sobre cada tramo y se armaron los {n_dias} días de modo que cada uno se lea en 20 a 30 minutos: los tramos con mucho para estudiar tienen más días y los que dicen poco, menos.</li>
<li><b>Escritura día por día.</b> Con todas las notas de cada tramo se escribió el estudio del día, uniendo lo repetido y presentando las distintas posturas cuando las fuentes no coinciden.</li>
<li><b>Introducción, panoramas, temas y anexos</b> ({len(arts)} secciones). Las notas que tratan la carta entera, una parte o un tema se ordenaron por sección y se escribieron con el mismo método que los días.</li>
<li><b>Verificación.</b> Un segundo control cotejó cada afirmación con sus notas, las citas bíblicas con la RVR1960 y las palabras griegas con el texto griego de Santiago (SBLGNT). Controles automáticos revisaron que cada fuente citada exista y que cada día se mantenga dentro de su pasaje.</li>
<li><b>Continuidad.</b> Por último se revisaron los días de a seis, para que cada uno empalme con el anterior y el siguiente, las fechas no se contradigan y no se repita lo mismo en días seguidos.</li>
</ol>
<h2>Qué quedó afuera y por qué</h2>
<p>Por decisión de ustedes, solo entran autores protestantes confiables: las obras católicas, adventistas, mormonas, de teología de la prosperidad o liberales, las de corriente carismática o con reservas y las de autor desconocido ya no están en los repositorios. En la carpeta de Santiago de la biblioteca ya no figuran, por ese motivo, un «Santiago» de autor no identificado, «Santiago – Judas» y el comentario de William Barclay. Tampoco se usaron los resúmenes de autor no identificado.</p>
<p>Un archivo de la biblioteca que se llama «Biblia Matthew Henry – Corintios a Apocalipsis» no es la obra de Matthew Henry: es un escaneo sin portada de otro comentario, y como no se puede saber quién lo escribió, no se usó. Treinta libros escaneados de REFERENCIA3 no tienen texto digital: se pasaron por reconocimiento de texto (OCR) cuatro cuyos temas tocan Santiago (la voluntad de Dios, el dinero, el quebrantamiento y la fe).</p>
<h2>El texto bíblico</h2>
<p>Las citas son de la Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988. El estudio muestra completo el texto de Santiago (108 versículos); el resto de la Biblia se cita solo por referencia. El texto griego es el <i>SBL Greek New Testament</i> (SBLGNT), © 2010 Society of Biblical Literature y Logos Bible Software, licencia CC BY 4.0.</p>
<h2>Mapas y datos</h2>
<p>Costas, ríos y lagos: Natural Earth (dominio público). Las ubicaciones se marcan con su grado de certeza. Tipografías: Cormorant Garamond, Literata, Figtree, Gentium Plus y Frank Ruhl Libre (SIL Open Font License), incluidas en el archivo para que se vea igual sin internet.</p>
"""
    os.makedirs(f'{T}/textos', exist_ok=True)
    json.dump({'ojo': 'Guía', 'titulo': 'Cómo usar el estudio', 'html': como}, open(f'{T}/textos/como-usar.json', 'w'), ensure_ascii=False, indent=1)
    json.dump({'html': fuentes}, open(f'{T}/textos/fuentes.json', 'w'), ensure_ascii=False, indent=1)
    print('textos escritos:', n_dias, 'días;', n_bib, 'notas de biblioteca;', n_ref, 'notas de REF3')


if __name__ == '__main__':
    main()
