# Instrucciones de extracción (estudio de 1 Pedro a Judas)

Estamos construyendo el mejor estudio posible de 1 Pedro, 2 Pedro, 1, 2 y 3 Juan y Judas para un matrimonio protestante que lo va a
leer día a día (20 a 30 minutos por día). Regla de oro: **NO INVENTAR NADA**. Todo sale de los libros de su biblioteca; no agregues
nada de tu conocimiento propio ni completes lo que el autor no dice. Nunca copies párrafos de los libros: se condensa con palabras propias.

## Tu tarea
Leer **completo** el archivo del bloque que te indiquen (en `SCRATCH/pj_bloques/<id>.txt`, donde
SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad) y devolver **todo aporte sustancial** de los autores
como notas, cada una anclada al pasaje que explica. Las notas se escriben en archivos JSON (ver abajo).

Cómo leer: con la herramienta Read pasando `allow_large: true` y sin offset/limit (si el resultado viniera truncado, leé el resto con
offset). Los bloques tienen encabezados `=== [id | pág. PDF N] ===` (comentarios y diccionario) o `##### OBRA | AUTOR | ARCHIVO | páginas`
(libros de referencia). Ese rótulo es el que va en `pagina`. La línea `# Libros:` del encabezado dice qué libros comenta el bloque.

## Qué incluir
Explicación del texto versículo por versículo, estructura y bosquejos, autor, fecha, destinatarios y canon (incluido el debate sobre la
autenticidad de 2 Pedro y el de Juan «el anciano»), contexto histórico (Asia Menor y sus provincias, Roma y Nerón, Éfeso, persecución,
la vida de Pedro, Juan y Judas), cultura y costumbres (esclavos, matrimonio, hospitalidad, cartas antiguas), geografía, palabras griegas
que el autor comenta, uso del Antiguo Testamento (Isaías, Salmos, Proverbios, Génesis, Números…), conexiones con el resto del Nuevo
Testamento (el Evangelio de Juan, los discursos de Pedro en Hechos, Pablo, el paralelo 2 Pedro 2 – Judas), literatura extrabíblica que
el texto usa (1 Enoc, la Asunción de Moisés, tradiciones judías), los falsos maestros y oponentes (quiénes eran, qué enseñaban:
gnosticismo, docetismo, Cerinto, libertinismo, según cada autor), teología y doctrina, cómo se ve a Cristo en el pasaje, personajes
(Silvano, Marcos, Gayo, Diótrefes, Demetrio, la señora elegida, Miguel, Enoc, Balaam, Coré…), pasajes difíciles e interpretaciones
discutidas (con **las posturas** que presenta y cuál prefiere el autor: los espíritus encarcelados, el bautismo que salva, «no puede
pecar», el pecado de muerte, los tres testigos, los ángeles que pecaron, la disolución de los elementos, la apostasía, la segunda venida…),
aplicaciones prácticas, ilustraciones y frases memorables, preguntas de reflexión, tablas y diagramas descriptos en el texto (describí su
contenido en la nota).
Qué NO incluir: datos editoriales, prólogos de cortesía, índices, bibliografías, publicidad, menús web.

Ser exhaustivo es lo más importante: recorré todas las páginas; si dudás si algo es sustancial, incluilo con importancia 1. No incluyas
la misma idea dos veces dentro del bloque (una nota por idea; si sigue varias páginas, una nota con la página inicial).

## Formato de cada nota
```json
{"ref": "1P 2:4-8", "tipo": "exegesis", "titulo": "…", "contenido": "2 a 6 oraciones…",
 "cita": "frase textual del autor (opcional, hasta 50 palabras, copiada exacta)",
 "refs_biblicas": ["Is 28:16", "Sal 118:22"],
 "griego": {"palabra": "ἐλπίς", "transliteracion": "elpís", "significado": "…"},
 "postura": "interpretaciones que presenta y cuál prefiere el autor (opcional)",
 "escuela": "tradición o postura teológica del autor en esta nota, si la manifiesta (opcional): reformado | wesleyano | dispensacional | arminiano | premilenial | amilenial | …",
 "pagina": "pág. PDF 83", "importancia": 2}
```
- `ref`: **siempre con sigla de libro**: `1P`, `2P`, `1J`, `2J`, `3J`, `Jd`. Formas: "1P 2:4-8", "1J 2:28-3:3", "1P 3" (capítulo
  entero), "2P" (el libro entero), "Jd 3-4" y "2J 7" (los libros de un solo capítulo van sin capítulo), "1P intro" (introducción a ese
  libro: autor, fecha, destinatarios, ocasión, estructura, mensaje), "intro" (las epístolas generales en conjunto o varias de estas
  cartas) o "tema" / "1J tema" (transversal, sin pasaje puntual). Los versículos deben existir: 1P 25, 25, 22, 19, 14; 2P 21, 22, 18;
  1J 10, 29, 24, 21, 21; 2J 13; 3J 15; Jd 25. Una nota no cruza libros: si habla de 2 Pedro 2 y Judas a la vez, anclala en el pasaje
  que comenta el bloque y poné el otro en `refs_biblicas`.
- `tipo` (uno de): contexto, cultura, geografia, autoria_fecha, estructura, exegesis, griego_palabra, cristo, doctrina, AT_en_NT,
  conexion_biblica, extrabiblico, falsos_maestros, interpretacion_discutida, aplicacion, ilustracion, personaje, pregunta_reflexion, apologetica.
- `contenido`: condensación **fiel** de lo que dice el autor (2 a 6 oraciones; más si es bosquejo o tabla). Conservá matices, nombres,
  números, fechas y argumentos. Si es una opinión propia del autor, decilo («según el autor…»). Castellano claro.
- `cita`: solo si hay una frase textual valiosa; copiada exacta, hasta 50 palabras.
- `griego`: solo si el autor comenta una palabra griega; escribí la grafía griega con acentos (la verificaremos contra el SBLGNT).
- `pagina`: el rótulo de página del encabezado donde está el contenido (p. ej. "pág. PDF 83" o "pág. PDF 83-84"; si el texto trae
  además la página impresa, como «[p 39]» o «[P. 301]», podés agregarla: "pág. PDF 28 (p. 39)").
- `importancia`: 3 = central y mejor dicho; 2 = valioso; 1 = complementario.
- Si el texto viene de OCR, corregí errores evidentes sin cambiar el sentido y anotalo en `problemas`.
- Los autores de tradiciones distintas (reformados, wesleyanos del Beacon, dispensacionalistas) se registran con fidelidad: el
  `contenido` dice lo que dicen, siempre atribuido; no los suavices ni los "corrijas".
- Comillas «» solo para texto bíblico literal; para palabras del autor usá `cita`.

## Cómo entregar
1. Escribí las notas con la herramienta Write en `/home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/extracciones/<id>.json`
   con la forma `{"bloque": "<id>", "notas": [ … ], "problemas": "…"}`. Si el bloque da más de ~45 notas, dividilo en varios archivos
   `<id>_a.json`, `<id>_b.json`, `<id>_c.json`… (cada uno con la misma forma y a lo sumo ~45 notas) para que ninguna llamada sea
   gigantesca. No uses otro nombre.
2. Validá con `python3 /home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/scripts/validar_extraccion.py <id>` y corregí
   hasta que no haya errores.
3. Tu respuesta final es **una sola línea**: `<id>: N notas (importancia 3: M)` más, si hubo, los problemas.
No hagas commits ni toques otros archivos.

## Ahorro de contexto
- Leé el bloque una sola vez, de corrido; no lo releas para "verificar". Escribí los archivos de notas a medida que avanzás (`_a`, `_b`…).
- Un solo ciclo de escritura + validación por archivo; si el validador marca errores, corregí solo esas notas (Edit), sin reescribir todo.
