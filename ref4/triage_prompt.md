# Triage de LIBROS-REFERENCIA4 para el estudio «1 Pedro a Apocalipsis»

Contexto: estudio bíblico en pareja de 1 Pedro, 2 Pedro, 1 Juan, 2 Juan, 3 Juan, Judas y Apocalipsis (ya hecho: Apocalipsis).
Reglas de fuentes: `genesis/trabajo/clasificacion/criterio.md` (A = protestante confiable; B = reservas, no se usa; C = excluido; D = autor no identificable).

Tu tarea: clasificar los archivos de `SCRATCH/ref4_lista.tsv` (id<TAB>ruta relativa a /home/user/libros-referencia4/). El texto ya extraído de cada uno, si existe, está en
`SCRATCH/ref4txt/<id>.txt` (SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad).
1. Por el nombre de archivo decidí lo evidente. Solo si el autor o la tradición no se pueden saber por el nombre, leé las primeras ~60 líneas del texto (head -60); no abras más.
   No inventes: si no se puede identificar, categoría D.
2. Por cada archivo: autor, tradición, categoría (A/B/C/D) con `razon` de una línea, y `libros` = lista de los libros del estudio a los que puede aportar
   entre 1P, 2P, 1J, 2J, 3J, Jd, Ap (vacía si ninguno), con `temas` breves (p. ej. «sufrimiento y persecución», «amor y seguridad», «falsos maestros», «segunda venida»,
   «milenio», «cielo»). Aportar = trata el libro, o un tema central suyo con profundidad (no una mención al pasar).
3. `nivel`: alto (comentario o tratado sobre el libro/tema central), medio (capítulos útiles), bajo (marginal), nulo.
4. Escribí `SCRATCH/ref4_triage.json`: lista de {id, ruta, autor, tradicion, categoria, razon, libros, temas, nivel}. Agrupá: primero los de categoría A con nivel alto/medio.
5. Respuesta final: UNA línea con los conteos (A alto/medio, A bajo, B, C, D, nulo) y, en otra, los 10 más valiosos.
No uses más de ~40 llamadas a herramientas: es un trabajo por nombres, no de lectura. No hagas commits.
