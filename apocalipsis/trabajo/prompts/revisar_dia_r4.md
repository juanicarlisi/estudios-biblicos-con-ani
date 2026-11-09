# Revisar un día de Apocalipsis con el material nuevo de REFERENCIA4

El día ya está escrito y validado (`trabajo/dias/dia_NN.json`; esquema en `plan/esquema_dia.md`; reglas de escritura en `prompts/escribir_dia.md`: leelo, vale todo).
Ahora hay notas NUEVAS (ids `r4_*`) de libros incorporados después: Hitchcock, MacArthur («Recorrido»), Graham («Jinetes»), Carballosa («Cristo en el Milenio»),
Lennox, Ice, Walvoord, Dyer, Jeremiah, Lutzer, Foxe, Matthew Henry y el Comentario Moody (sección de Apocalipsis). Están en
`SCRATCH/r4_dias/dia_NN.txt` (SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad).

## Tu tarea: decidir qué aporta y mejorar el día sin hincharlo
1. Leé el día (JSON) y las notas nuevas. Para cada nota preguntate: ¿agrega algo que el día NO tiene o dice peor?
   Sí aporta: dato histórico/cultural/lingüístico nuevo; una postura, argumento u objeción que falta; una corrección de un dato; una explicación mejor de un versículo difícil;
   una ilustración o aplicación realmente buena; una cita memorable. No aporta: lo que repite lo ya dicho, relleno, polémica lateral, lo que el autor dice de pasada.
2. Si aporta, integralo **en el lugar correcto** del JSON (sección, `interpretaciones`, `palabras`, `cristo`, `para_vivir`, `profundizar`, etc.) con sus ids en `fuentes`.
   Si cambia o corrige algo ya escrito, corregilo y atribuí («según Hitchcock…»). Si una postura nueva debe sumarse a una `interpretaciones`, agregala con su autor.
3. **Límite del día: 2.600 palabras** (validar_dia.py lo avisa). Para sumar, recortá lo más débil o pasalo a `profundizar`; nunca crezcas el día por acumulación. Si no hay nada que mejore el día, no lo toques: «sin cambios» es una respuesta válida y buena.
4. Reglas que no cambian: nada inventado (todo sale de las notas; no agregues tu conocimiento propio); no copiar texto de los libros (condensá con tus palabras); comillas «» solo para texto bíblico literal de la RVR1960
   (los autores van entre “ ”); no atribuyas a un autor una escuela escatológica que la nota no declara (ignorá el campo `escuela` de las notas de Henry, Moody y Graham); las escuelas y posturas se presentan sin tomar partido.
   Si una nota repite un error evidente de OCR/traducción (cifra, nombre, referencia) o contradice al texto bíblico, no la uses y anotalo.
5. Editá el JSON con un script Python corto (cargar, modificar campos, guardar con ensure_ascii=False) o con Edit; mantené el formato del archivo. Después:
   `python3 /home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/scripts/validar_dia.py N` hasta que no haya errores (ids de fuentes, griego, forma).
6. Dejá `apocalipsis/trabajo/revision_r4/dia_NN.txt` con ≤6 líneas: ids integrados, qué agregaron, qué recortaste, o «sin cambios» con el motivo.
7. Respuesta final: UNA línea: `día N: +X notas integradas · palabras A→B · <qué mejoró, en pocas palabras>` o `día N: sin cambios`.
No hagas commits, no publiques artefactos, no toques otros días.
