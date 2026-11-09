# Instrucciones para escribir un día del estudio de 1 Pedro a Judas

Estamos escribiendo el mejor estudio posible de 1 Pedro, 2 Pedro, 1, 2 y 3 Juan y Judas para un **matrimonio protestante** que lo lee
día a día (20 a 30 minutos de estudio por día), en castellano rioplatense neutro, claro y cálido. Regla de oro: **NO INVENTAR NADA**.
Todo sale de las notas extraídas de los libros de su biblioteca (ya leídas y resumidas); nada de tu conocimiento propio, salvo para
ordenar y redactar. Nunca copies frases largas de los autores: se redacta con palabras propias y se atribuye.

## Tu tarea
1. Leé `pedro-judas/trabajo/plan/esquema_dia.md` (la forma exacta del JSON y las reglas) y, para saber qué visuales y anexos existen,
   `pedro-judas/trabajo/plan/visuales.json` y `pedro-judas/trabajo/plan/articulos.json`.
2. Leé los insumos del día: `SCRATCH/pj_insumos/dia_NN.txt` (SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad):
   trae el libro, el texto bíblico (RVR1960) y griego (SBLGNT), el día anterior y el siguiente, y las notas con su `[id]`, pasaje, tipo,
   importancia, fuente y tradición del autor. Usá Read con `allow_large: true`.
3. Escribí el día en `/home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/dias/dia_NN.json` (Write) y validalo con
   `python3 /home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/scripts/validar_dia.py N`. Corregí hasta que no haya ERRORES
   (los avisos son orientativos: revisá los de griego).
4. Respuesta final: UNA línea: `dia N: <título> · P palabras · F fuentes · avisos relevantes`.

## Cómo escribir
- **Para los dos**: tono de compañero de estudio, sin sermonear ni vaciar de contenido. Se habla de «ustedes» al aplicar.
- **Cada afirmación lleva `fuentes`** (ids de los insumos). Unís lo que se repite entre autores en una sola afirmación con varias fuentes.
  Hechos históricos o datos dudosos que el autor no respalda («según McGee…»): atribuilos. Si una fuente tiene una errata evidente
  (señalada en la nota), no la repitas.
- **Posturas**: cuando los autores difieren (los espíritus encarcelados, el bautismo, «no puede pecar» y la entera santificación, el pecado
  de muerte, la apostasía y la seguridad, la autoría de 2 Pedro, los elementos que serán quemados, el arrebatamiento y el milenio), no
  tomes partido: decí quién sostiene qué (nombre del autor + tradición: reformado, wesleyano, dispensacional…) en `interpretaciones`; en
  las secciones avisá con una frase («ver Interpretaciones») cuando el texto depende de la postura. Lo que todos comparten (Cristo murió
  por los pecados y volverá, Dios guarda a los suyos, la verdad y el amor van juntos) se afirma sin reservas.
- **Cristo**: en `cristo`, cómo el pasaje muestra a Jesús (sección obligatoria si las notas lo permiten).
- **Qué pasó antes / qué viene** (`contexto`): usá los días vecinos y las notas; «cuando» y «donde» solo si las fuentes lo dicen.
- **Estructura de cada día**: la idea central, el pasaje por partes (secciones), las palabras griegas, Cristo, las discusiones, el Antiguo
  Testamento que el pasaje cita o usa, lo que aportan otros libros, las conexiones con el resto de la Biblia, aplicación, preguntas,
  oración. Lo optativo, a `profundizar`. No repitas lo mismo en secciones distintas.
- **Extensión**: 1.800 a 2.600 palabras de estudio (sin `profundizar`). Si el tramo es de uno o dos versículos y las notas son
  muchas, profundizá cada idea importante en vez de agregar temas; si hay poco material, escribí menos y no rellenes.
- **Texto bíblico**: no transcribas pasajes; solo `versiculo_clave.ref` (la app inserta la RVR1960). Frases cortas entre «» solo si están
  literalmente en el texto bíblico de los insumos (máx. 12 palabras seguidas). Las comillas «» se usan **solo** para texto bíblico literal.
- **Referencias con sigla**: «1P 2:4-8», «Jd 3», «2J 7» (sin sigla se entiende el libro del día, salvo en el día de 2 y 3 Juan).
- **Visuales y anexos**: elegí solo los que de verdad ayudan a este día (ids del catálogo); no inventes ids.
- No toques otros archivos ni hagas commits.

## Ahorro de contexto
- Leé el insumo una vez; si es muy largo, por tramos (offset/limit) y descartando rápido las notas de importancia 1 repetidas.
- Un solo ciclo de escritura + validación; si hay errores, corregí con Edit solo lo marcado y no releas el JSON entero después de validar.

## Atribución de tradición (09-11-2026)
El campo `escuela` de las notas es la tradición del autor que anotó el extractor; úsala solo para ubicar una postura cuando la nota misma la presenta como postura del autor.
No rotules a un autor («reformado», «dispensacional»…) en el texto si no es un dato de la nota o de su propia obra; ante la duda, citá solo al autor y su postura.
