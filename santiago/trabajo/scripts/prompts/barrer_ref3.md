# Instrucciones para barrer un bloque de libros de referencia buscando lo que enseñan sobre Santiago

Estamos armando el mejor estudio posible de la carta de Santiago para un matrimonio protestante joven de Buenos Aires, condensando la biblioteca
del fundador. **Regla de oro: NO INVENTAR NADA.**

Cada bloque (`/home/user/trabajo_santiago/segmentos/ref3/<id>.txt`) reúne fragmentos de libros de autores protestantes confiables que citan o tratan
Santiago. Cada fragmento empieza con un encabezado `##### OBRA: ... | AUTOR: ... | ARCHIVO: ... | páginas PDF a-b` (o `pág. PDF n (fragmento)`); en los
tramos largos, cada página lleva su marca `--- [pág. PDF n] ---`.

## Cómo trabajar (importante: sé directo, sin deliberar)

Esta es una tarea de **lectura y condensación fiel**, no de análisis. **No planifiques ni hagas borradores de las notas en tu razonamiento**: leé y escribí cada tanda
de notas directamente en el archivo. Cada nota se escribe una sola vez.

Por cada bloque que te asignaron (uno por uno, en el orden dado):

1. Leé el bloque con **UNA sola llamada a Read, sin offset ni limit y con `allow_large: true`**. Si viniera truncado, leé el resto con `offset`.
2. Escribí las notas **en tandas** de unas 15 a 25 notas, avanzando en el orden del bloque. Cada tanda es **una llamada Write** a
   `/home/user/trabajo_santiago/partes/<id>.p1.json`, luego `<id>.p2.json`, `<id>.p3.json`… con la forma:

```json
{
  "notas": [
    {
      "ref": "2:14-26",
      "tema": "fe y obras",
      "tipo": "teologia_doctrina",
      "titulo": "Título corto",
      "contenido": "Condensación fiel de lo que dice el autor (1 a 5 oraciones), sin agregar nada.",
      "cita": "Opcional: frase textual valiosa, copiada exacta, hasta 40 palabras.",
      "autor": "Norman Geisler y Thomas Howe",
      "obra": "Dificultades bíblicas",
      "archivo": "Apologetica/Dificultades bíblicas - Norman Gisler, Thomas Howe.pdf",
      "pagina": "205",
      "importancia": 2
    }
  ],
  "descartados": 12
}
```

   (`descartados`: cantidad aproximada de fragmentos sin aporte, en la última tanda.) No releas ni reescribas tandas ya escritas.
3. Al terminar las tandas del bloque, corré
   `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/unir_partes.py <id> --ref3`
   y después
   `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/validar_extraccion.py /home/user/estudios-biblicos-con-ani/santiago/trabajo/extracciones_ref3/<id>.json --ref3`
4. Si el validador marca **ERRORES**, corregí solo esas notas (el mensaje trae el número y el título) editando la tanda que corresponda con Edit, y volvé a correr
   `unir_partes.py` y el validador hasta que no haya errores. De los avisos «la cita no figura tal cual», corregí la cita para que sea textual o quitá el campo `cita`.
   **No modifiques `extracciones_ref3/<id>.json` a mano.**
5. Pasá al bloque siguiente. Al terminar todos, respondé **solo** una línea por bloque: `id: N notas, X errores, Y avisos`.

## Campos

- `ref`: el pasaje de Santiago que la nota trata: `"C:V"`, `"C:V-V"`, `"C:V-C:V"`, `"C"`, o `"tema"` si es transversal a la carta sin pasaje puntual
  (p. ej. la fe y las obras en general, la providencia, la sabiduría). Santiago llega hasta 5:20. **Solo notas que traten Santiago o un tema que Santiago enseña.**
- `tema`: el tema en pocas palabras (p. ej. pruebas, tentación, fe y obras, la lengua, sabiduría, ricos y pobres, oración por los enfermos, paciencia, humildad, mundanalidad).
- `tipo` (uno de): `teologia_doctrina`, `explicacion_texto`, `griego_palabra`, `contexto_historico`, `cultura_costumbres`, `apologetica`, `cristo_en_santiago`, `eco_de_jesus`,
  `conexion_biblica`, `aplicacion_practica`, `matrimonio_familia`, `ilustracion`, `dificultad_interpretaciones`, `personaje`, `pregunta_reflexion`, `estructura_bosquejo`.
- `archivo`: el ARCHIVO del encabezado de donde sale, copiado exacto. `pagina`: **el número** de página PDF del fragmento (solo el número, como texto).
- `autor` y `obra`: los del encabezado (el título de la obra sin el subtítulo, si es largo).
- `importancia`: 3 = central para entender o vivir el pasaje; 2 = valioso; 1 = complementario.

## Qué rescatar

Lo que cada autor ENSEÑA sobre un pasaje, un personaje o un tema de Santiago y puede enriquecer el estudio: explicación del texto; doctrina (pruebas, tentación,
nuevo nacimiento, fe y obras, justificación, la lengua, sabiduría, humildad, oración, paciencia, ricos y pobres, juicio); palabras griegas; datos históricos y
culturales; respuestas a dificultades (p. ej. fe y obras en Pablo y Santiago, la unción de enfermos); relación con las enseñanzas de Jesús y con el AT;
aplicaciones a la vida de fe, la pareja y la familia; ilustraciones y frases memorables; bosquejos de sermón sobre un pasaje de Santiago (resumidos fielmente).

**Sé selectivo**: descartá las menciones al pasar, las listas de citas, lo que no trata Santiago (aunque el fragmento lo cite como ejemplo menor) y lo repetido.
Si un mismo autor repite una idea, una sola nota. Si una postura es discutida, registrala **como la postura de ese autor** (`dificultad_interpretaciones`).
`descartados`: cantidad aproximada de fragmentos sin aporte.

Cada nota es una condensación fiel (conservá nombres, números y argumentos); no agregues nada que el autor no diga. Las notas son en castellano.
