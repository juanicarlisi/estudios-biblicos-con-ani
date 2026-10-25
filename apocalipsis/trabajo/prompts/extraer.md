# Instrucciones de extracción (estudio de Apocalipsis)

Estamos construyendo el mejor estudio posible del libro de Apocalipsis para un matrimonio protestante que lo va a leer día a día
(20 a 30 minutos por día). Regla de oro: **NO INVENTAR NADA**. Todo sale de los libros y artículos de su biblioteca; no agregues
nada de tu conocimiento propio ni completes lo que el autor no dice.

## Tu tarea
Leer **completo** el archivo del bloque que te indiquen (en `SCRATCH/bloques/<id>.txt`, donde
SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad) y devolver **todo aporte sustancial** de los autores
como notas, cada una anclada al pasaje de Apocalipsis que explica. Las notas se escriben en archivos JSON (ver abajo).

Cómo leer: con la herramienta Read pasando `allow_large: true` y sin offset/limit (si el resultado viniera truncado, leé el resto con
offset). Los bloques tienen encabezados `=== [id | pág. PDF N] ===` (comentarios y diccionario), `##### OBRA | AUTOR | ARCHIVO | páginas`
(libros de referencia) o `título | autor | fecha | fuente | url` (artículos web). Ese rótulo es el que va en `pagina`.

## Qué incluir
Explicación del texto versículo por versículo, estructura y bosquejos, contexto histórico (Asia Menor, Patmos, Domiciano/Nerón, culto al
emperador, las siete ciudades, comercio, costumbres, arqueología, geografía), palabras griegas que el autor comenta, uso del Antiguo
Testamento (Daniel, Ezequiel, Zacarías, Isaías, Éxodo, Salmos…) y del resto del Nuevo, símbolos y números (siete, doce, 144.000, 666,
mil años, colores, animales), cronología y fechas, teología y doctrina, cómo se ve a Cristo en el pasaje, personajes, dificultades e
interpretaciones (con **las posturas** que presenta y cuál prefiere el autor), las escuelas de interpretación (preterista, historicista,
futurista, idealista; premilenial, amilenial, posmilenial; pretribulacional, postribulacional…), aplicaciones prácticas, ilustraciones y
frases memorables, preguntas de reflexión, tablas y diagramas descriptos en el texto (describí su contenido en la nota).
Qué NO incluir: datos editoriales, prólogos de cortesía, índices, bibliografías, publicidad, menús web.

Ser exhaustivo es lo más importante: recorré todas las páginas; si dudás si algo es sustancial, incluilo con importancia 1. No incluyas
la misma idea dos veces dentro del bloque (una nota por idea; si sigue varias páginas, una nota con la página inicial).

## Formato de cada nota
```json
{"ref": "2:1-7", "tipo": "explicacion_texto", "titulo": "…", "contenido": "2 a 6 oraciones…",
 "cita": "frase textual del autor (opcional, hasta 50 palabras, copiada exacta)",
 "refs_biblicas": ["Gn 2:9", "Ez 28"],
 "griego": {"palabra": "ἀγάπη", "transliteracion": "agápe", "significado": "…"},
 "postura": "interpretaciones que presenta y cuál prefiere el autor (opcional)",
 "escuela": "postura escatológica del autor en esta nota si la manifiesta (opcional): premilenial dispensacional | premilenial histórico | amilenial | posmilenial | preterista | idealista | historicista",
 "pagina": "pág. PDF 83", "importancia": 2}
```
- `ref`: "C:V", "C:V-V", "C:V-C:V" (p. ej. "4:1-5:14"), "C" (capítulo entero), "intro" (el libro entero: autor, fecha, destinatarios,
  género, estructura, mensaje) o "tema" (transversal, sin pasaje puntual: escuelas, milenio, tribulación, números, etc.).
  Apocalipsis tiene 22 capítulos; los versículos deben existir.
- `tipo` (uno de): contexto_historico, cultura_costumbres, arqueologia_geografia, griego_palabra, explicacion_texto, teologia_doctrina,
  cristo_en_apocalipsis, conexion_biblica, aplicacion_practica, ilustracion, dificultad_interpretaciones, estructura_bosquejo,
  cronologia_fechas, simbolo_numero, personaje, pregunta_reflexion, escuelas_interpretacion, apologetica.
- `contenido`: condensación **fiel** de lo que dice el autor (2 a 6 oraciones; más si es bosquejo o tabla). Conservá matices, nombres,
  números, fechas y argumentos. Si es una opinión propia del autor, decilo («según el autor…»). Castellano claro.
- `cita`: solo si hay una frase textual valiosa; copiada exacta, hasta 50 palabras.
- `griego`: solo si el autor comenta una palabra griega; escribí la grafía griega con acentos (la verificaremos después).
- `pagina`: el rótulo de página del encabezado donde está el contenido (p. ej. "pág. PDF 83" o "pág. PDF 83-84").
- `importancia`: 3 = central y mejor dicho; 2 = valioso; 1 = complementario.
- Si el texto viene de OCR, corregí errores evidentes sin cambiar el sentido y anotalo en `problemas`.
- Los artículos web y los libros de autores de otras corrientes (por ejemplo carismática/profética) se registran con fidelidad: el
  `contenido` dice lo que dicen, siempre atribuido; no los suavices ni los "corrijas".

## Cómo entregar
1. Escribí las notas con la herramienta Write en `/home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/extracciones/<id>.json`
   con la forma `{"bloque": "<id>", "notas": [ … ], "problemas": "…"}`. Si el bloque da más de ~45 notas, dividilo en varios archivos
   `<id>_a.json`, `<id>_b.json`, `<id>_c.json`… (cada uno con la misma forma y a lo sumo ~45 notas) para que ninguna llamada sea
   gigantesca. No uses otro nombre.
2. Validá con `python3 /home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/scripts/validar_extraccion.py <id>` y corregí
   hasta que no haya errores.
3. Tu respuesta final es **una sola línea**: `<id>: N notas (importancia 3: M)` más, si hubo, los problemas.
No hagas commits ni toques otros archivos.
