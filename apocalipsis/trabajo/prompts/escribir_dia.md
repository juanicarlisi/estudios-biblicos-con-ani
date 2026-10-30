# Instrucciones para escribir un día del estudio de Apocalipsis

Estamos escribiendo el mejor estudio posible del libro de Apocalipsis para un **matrimonio protestante** que lo lee día a día (20 a 30
minutos de estudio por día), en castellano rioplatense neutro, claro y cálido. Regla de oro: **NO INVENTAR NADA**. Todo sale de las
notas extraídas de los libros de su biblioteca (ya leídas y resumidas); nada de tu conocimiento propio, salvo para ordenar y redactar.

## Tu tarea
1. Leé `apocalipsis/trabajo/plan/esquema_dia.md` (la forma exacta del JSON y las reglas) y, para saber qué visuales y anexos existen,
   `apocalipsis/trabajo/plan/visuales.json` y `apocalipsis/trabajo/plan/articulos.json`.
2. Leé los insumos del día: `SCRATCH/insumos/dia_NN.txt` (SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad):
   trae el texto bíblico y griego, el día anterior y el siguiente, y las notas con su `[id]`, pasaje, tipo, importancia, fuente y escuela del autor.
   Usá Read con `allow_large: true`.
3. Escribí el día en `/home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/dias/dia_NN.json` (Write) y validalo con
   `python3 /home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/scripts/validar_dia.py N`. Corregí hasta que no haya ERRORES
   (los avisos son orientativos: revisá los de griego).
4. Respuesta final: UNA línea: `dia N: <título> · P palabras · F fuentes · avisos relevantes`.

## Cómo escribir
- **Para los dos**: tono de compañero de estudio, sin sermonear ni vaciar de contenido. Se habla de «ustedes» al aplicar.
- **Cada afirmación lleva `fuentes`** (ids de los insumos). Unís lo que se repite entre autores en una sola afirmación con varias fuentes.
  Hechos históricos o datos dudosos que el autor no respalda («según McGee…»): atribuilos. Si una fuente tiene una errata evidente
  (señalada en la nota), no la repitas.
- **Posturas**: cuando los autores difieren, no tomes partido: decí quién sostiene qué (nombre del autor + escuela) en
  `interpretaciones`; en las secciones, avisá con una frase («ver Interpretaciones») cuando el texto depende de la postura. El estudio
  no es dispensacionalista, ni amilenial, ni preterista: es una guía honesta de lo que leen los mejores autores evangélicos. Lo que
  todos comparten (Cristo reina, Dios juzga y salva, la victoria del Cordero) se afirma sin reservas.
- **Cristo**: en `cristo`, cómo el pasaje muestra a Jesús (sección obligatoria si las notas lo permiten).
- **Qué pasó antes / qué viene** (`contexto`): usá los días vecinos y las notas; «cuando» y «donde» solo si las fuentes lo dicen.
- **Estructura de cada día**: la idea central, el pasaje por partes (secciones), los símbolos, las palabras griegas, Cristo, las
  discusiones, lo que aportan otros libros, las conexiones con el resto de la Biblia, aplicación, preguntas, oración. Lo optativo, a
  `profundizar`. No repitas lo mismo en secciones distintas.
- **Extensión**: 1.800 a 2.600 palabras de estudio (sin `profundizar`). Si el tramo es de uno o dos versículos y las notas son
  muchas, profundizá cada idea importante en vez de agregar temas; si hay poco material, escribí menos y no rellenes.
- **Escuelas y tradiciones**: los autores carismáticos/proféticos (TTL, MiSion) se citan con fidelidad y atribuidos; no los suavices ni los presentes como "la" iglesia.
- **Texto bíblico**: no transcribas pasajes; solo `versiculo_clave.ref` (la app inserta la RVR1960). Frases cortas entre «» solo si están literalmente en el texto bíblico de los insumos.
- **Visuales y anexos**: elegí solo los que de verdad ayudan a este día (ids del catálogo); no inventes ids.
- No toques otros archivos ni hagas commits.
