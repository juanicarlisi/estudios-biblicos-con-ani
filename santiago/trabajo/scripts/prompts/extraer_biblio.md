# Instrucciones para extraer notas de un bloque de comentario sobre Santiago

Estamos construyendo el mejor estudio posible de la carta de Santiago para un matrimonio protestante joven de Buenos Aires que la va a
estudiar día por día (media hora diaria). **Regla de oro: NO INVENTAR NADA.** Todo sale de los libros de su biblioteca, con la página.

## Cómo trabajar (importante: sé directo, sin deliberar)

Esta es una tarea de **lectura y condensación fiel**, no de análisis. **No planifiques ni borradores las notas en tu razonamiento**: leé, y escribí cada tanda
de notas directamente en el archivo. Cada nota se escribe una sola vez. Si te encontrás razonando páginas enteras, parate y escribí.

Por cada bloque que te asignaron (uno por uno, en el orden dado):

1. Leé el bloque con **UNA sola llamada a Read, sin offset ni limit y con `allow_large: true`**
   (`/home/user/trabajo_santiago/segmentos/biblio/<id>.txt`). Cada página empieza con un encabezado `=== [obra | PÁGINA PDF n ...] ===`.
2. Escribí las notas **en tandas**, una por cada 2 o 3 páginas del bloque, avanzando en el orden del texto. Cada tanda es **una llamada Write** a
   `/home/user/trabajo_santiago/partes/<id>.p1.json`, luego `<id>.p2.json`, `<id>.p3.json`… con la forma:

```json
{
  "notas": [
    {
      "ref": "1:2-4",
      "tipo": "explicacion_texto",
      "titulo": "Título corto de la nota",
      "contenido": "Condensación fiel de lo que dice el autor, 2 a 5 oraciones, con tus palabras.",
      "cita": "Opcional: frase textual valiosa, copiada exacta, hasta 50 palabras.",
      "refs_biblicas": ["Mt 5:3", "Job 1:21"],
      "griego": {"palabra": "πειρασμός", "transliteracion": "peirasmós", "significado": "..."},
      "postura": "Opcional: interpretaciones que presenta el autor y cuál prefiere.",
      "pagina": "macarthur | PÁGINA PDF 57",
      "importancia": 3
    }
  ],
  "problemas": ""
}
```

   (`problemas`: solo si hubo errores de OCR que corregiste o páginas ilegibles; vacío si no.) No releas ni reescribas tandas ya escritas.
3. Cuando terminaste todas las tandas del bloque, corré:
   `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/unir_partes.py <id>`
   y después
   `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/validar_extraccion.py /home/user/estudios-biblicos-con-ani/santiago/trabajo/extracciones/<id>.json`
4. Si el validador marca **ERRORES**, corregí solo esas notas (el mensaje trae el número y el título de la nota) editando la tanda que corresponda con Edit,
   y volvé a correr `unir_partes.py` y el validador, hasta que no haya errores. De los avisos «la cita no figura tal cual», corregí la cita para que sea textual o quitá el campo `cita`.
   **No modifiques `extracciones/<id>.json` a mano.**
5. Pasá al bloque siguiente. Al terminar todos, respondé **solo** una línea por bloque: `id: N notas, X errores, Y avisos`.

## Qué es una buena nota

- **Una idea del autor por nota**, entendible sola. Un bloque de ~30.000 caracteres da típicamente **30 a 60 notas**; el conjunto de las notas debe ser bastante
  más corto que el texto original (condensás, no transcribís). Si el autor repite una idea, una sola nota.
- `ref`: el pasaje de Santiago que la nota comenta: `"C:V"`, `"C:V-V"`, `"C:V-C:V"`, `"C"` (capítulo entero), `"intro"` (la carta entera: autor, fecha,
  destinatarios, canon, estilo, estructura, propósito) o `"tema"` (transversal, sin pasaje puntual). Santiago llega hasta 5:20.
- `tipo` (uno de): `contexto_historico`, `cultura_costumbres`, `arqueologia_geografia`, `griego_palabra`, `explicacion_texto`, `teologia_doctrina`,
  `cristo_en_santiago` (cómo el pasaje apunta a Cristo o lo muestra), `eco_de_jesus` (cuando el autor liga el pasaje con enseñanzas de Jesús, p. ej. el Sermón del Monte),
  `conexion_biblica` (con el AT, con Pablo u otros pasajes), `aplicacion_practica`, `ilustracion`, `dificultad_interpretaciones`,
  `estructura_bosquejo`, `cronologia_fechas`, `personaje`, `pregunta_reflexion`.
- `contenido`: condensación **fiel**: conservá matices, nombres, números, fechas y argumentos; **nada que el autor no diga**. Con tus palabras (no copies párrafos);
  la frase textual memorable, solo en `cita`.
- `griego`: cuando el autor comenta una palabra griega. `palabra` con letras griegas si el texto las trae; si solo trae la transliteración, poné esa en `palabra`
  y repetila en `transliteracion`. `significado`: lo que dice el autor.
- `pagina`: copiá el rótulo del encabezado de la página donde está el contenido, sin los `=` ni los corchetes: p. ej. `macarthur | PÁGINA PDF 57`.
  En el comentario Mundo Hispano (cbmh) agregá la marca de página impresa más cercana: `cbmh | PÁGINA PDF 140 | [P. 184]`.
  En el Diccionario (dbmh) copiá el rótulo completo, con el nombre de la entrada. **La página tiene que existir en el bloque.**
- `importancia`: 3 = central (no se puede estudiar el pasaje sin esto); 2 = valioso; 1 = complementario.

## Qué incluir

Explicación del texto versículo por versículo; contexto histórico y cultural; costumbres; geografía; palabras griegas (significado, uso, vínculo con el AT y la LXX);
autoría, fecha, destinatarios y canonicidad; estructura de la carta; teología y doctrina; relación con las enseñanzas de Jesús (Sermón del Monte), con Pablo y
con el Antiguo Testamento; cómo apunta a Cristo; dificultades e interpretaciones (con la postura del autor); bosquejos; aplicaciones prácticas; ilustraciones y
frases memorables; preguntas de reflexión del autor.

**No incluyas:** datos editoriales, índices, bibliografías, prólogos y agradecimientos, publicidad de otras obras, ni lo que no trata Santiago (por ejemplo lo
que ya es de 1 Pedro u otras epístolas del mismo volumen; la metodología de predicación expositiva de Carballosa, parte 3, salvo el contenido sobre el texto de Santiago).

## Criterio

- Cada aporte distinto de cada autor cuenta; si dudás de si algo es sustancial, incluilo con importancia 1. Pero **no repitas** y **no rellenes**.
- No agregues ningún dato, versículo ni interpretación propios. Si el texto trae errores de OCR evidentes, corregilos sin cambiar el sentido y anotalo en `problemas`.
- Si el autor sostiene una postura discutida, registrala como la postura **de ese autor** (`dificultad_interpretaciones` y/o `postura`).
- Las notas son en castellano.
