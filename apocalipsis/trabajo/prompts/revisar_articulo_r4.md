# Revisar un artículo de Apocalipsis con el material nuevo de REFERENCIA4

El artículo ya está escrito y validado (`trabajo/articulos/art_<ID>.json`; esquema en `plan/esquema_articulo.md`; reglas en `prompts/escribir_articulo.md`: leelo, valen todas).
Hay notas NUEVAS (`r4_*`) de libros incorporados después (Hitchcock, MacArthur «Recorrido», Graham, Carballosa «Milenio», Lennox, Ice, Walvoord, Dyer,
Jeremiah, Lutzer, Foxe, Matthew Henry, Moody) seleccionadas para tu artículo en `SCRATCH/r4_arts/art_<ID>.txt`
(SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad).

## Tu tarea
1. Leé el artículo y las notas nuevas. Agregá solo lo que MEJORA el artículo: posturas, argumentos u objeciones que faltan (atribuidos a su autor), datos históricos o lingüísticos nuevos, correcciones, ilustraciones buenas.
   Lo que repite lo ya dicho, lo lateral o lo dudoso, no entra. «Sin cambios» es una respuesta válida.
2. Respetá el largo del artículo (`plan/articulos.json`, campo `largo`; si ya está al tope, para sumar recortá lo más débil o pasalo a `notas_no_usadas`). Citá siempre con ids en `fuentes`.
3. Mismas reglas de siempre: nada inventado (todo sale de las notas); no copiar texto; comillas «» solo para texto bíblico literal de la RVR1960 y “ ” para autores; no atribuyas a un autor una escuela
   escatológica que la nota no declara (ignorá el campo `escuela` de Henry, Moody y Graham); las posturas se presentan sin tomar partido; no uses notas con errores evidentes (cifras, fechas, referencias mal copiadas) o contradichas por el texto bíblico: anotalo.
4. Editá el JSON (script Python corto con ensure_ascii=False) y validá: `python3 /home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/scripts/validar_articulo.py <ID>` hasta que no haya errores.
5. Dejá `apocalipsis/trabajo/revision_r4/art_<ID>.txt` con ≤6 líneas (ids integrados, qué aportan, qué recortaste, o «sin cambios»).
6. Respuesta final: UNA línea: `<ID>: +X notas integradas · palabras A→B · <qué mejoró>` o `<ID>: sin cambios`. Sin commits ni artefactos; no toques otros archivos.
