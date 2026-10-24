# Instrucciones para escribir un artículo del estudio de Santiago (introducción, panorama de una parte, tema o anexo)

Vas a escribir una sección de un estudio de la carta de Santiago para un matrimonio protestante joven de Buenos Aires que lo lee juntos. Quieren entender las Escrituras a fondo y vivirlas.

## Cómo trabajar

1. Leé con **UNA llamada a Read** (con `allow_large: true`) el archivo `/home/user/trabajo_santiago/insumos/libro/art_ID.txt`: trae el título, el alcance, el largo y la lista de las otras secciones,
   y después **todas** las notas extraídas de su biblioteca (comentarios de Santiago y libros de autores protestantes confiables) para esta sección, cada una con un id entre corchetes.
2. Escribí la sección con Write en `/home/user/estudios-biblicos-con-ani/santiago/trabajo/articulos/borrador_ID.json` (esquema abajo). Sé directo: la tarea es condensar con criterio; no hagas borradores
   en tu razonamiento, escribilo una vez.
3. Corré `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/validar.py --articulos --borradores --dias 0` y corregí con Edit lo que marque sobre tu artículo.
4. Respondé con una sola línea: `ID: palabras del cuerpo, notas usadas, errores pendientes`.

## Esquema (JSON)

```json
{
  "id": "T5", "titulo": "…", "bajada": "Una oración que dice de qué trata la sección.",
  "entrada": {"texto": "…", "fuentes": ["…"]},
  "versiculos": [{"ref": "2:24", "porque": "…"}],
  "apartados": [{"titulo": "…", "parrafos": [{"texto": "…", "fuentes": ["…"]}], "destacado": {"texto": "Una oración para retener.", "fuentes": ["…"]}}],
  "tablas": [{"titulo": "…", "descripcion": "…", "columnas": ["…", "…"], "filas": [["…", "…"]], "fuentes": ["…"]}],
  "diagrama": {"tipo": "imagenes|pasos|escalera|comparacion|tabla", "titulo": "…", "descripcion": "…", "items": [], "columnas": [], "filas": [], "fuentes": ["…"]},
  "palabras": [{"ref": "2:21", "griego": "ἐδικαιώθη", "translit": "edikaiōthē", "significado": "…", "fuentes": ["…"]}],
  "interpretaciones": [{"tema": "…", "posturas": [{"postura": "…", "quien": "…", "fuentes": ["…"]}], "nota": "…"}],
  "citas": [{"texto": "frase textual de un campo CITA", "autor": "…", "obra": "…", "fuentes": ["…"]}],
  "conexiones": [{"ref": "Ro 4:2-5", "nota": "…", "fuentes": ["…"]}],
  "para_vivir": [{"texto": "…", "fuentes": ["…"]}],
  "para_conversar": ["…", "…", "…"],
  "refs_santiago": ["2:14-26"],
  "notas_no_usadas": "…"
}
```

`tablas`, `diagrama`, `palabras`, `interpretaciones`, `citas`, `conexiones`, `para_vivir` y `para_conversar` son opcionales (listas vacías si no corresponden). Los anexos de tipo tabla
(`A2`, `A3`, `A1`, `A4`) se arman sobre todo con `tablas`; el anexo `A5` lleva un `diagrama` de tipo `imagenes` (iconos: ola, hierba, espejo, freno, timon, fuego, bestia, fuente, hoja, uvas, nube,
lluvia, aceite, corona, balanza, libro, corazon, boca, oido, moneda, camino, mano).

## Guía por grupo

- **intro**: capítulo de la introducción: claro, ordenado y fundado, para leer antes de empezar el plan. `para_vivir` y `para_conversar` pueden ir vacíos.
- **parte**: panorama de una parte (capítulo) para leer antes de empezarla: de qué trata, cómo se ordena (con los días del plan que figuran arriba), qué temas y personajes la atraviesan y qué conviene mirar al leer.
  No adelantes el detalle de cada día: orientá. `para_vivir`/`para_conversar` pueden ir vacíos.
- **tema**: reúne lo que Santiago enseña sobre él de punta a punta, en orden y con su desarrollo en el resto de la Biblia. Lleva `para_vivir` (2 a 4) y `para_conversar` (3 preguntas para una pareja).
- **anexo**: material de consulta (cuadro, personas, imágenes, términos); poco texto corrido y mucha estructura (tablas), siempre con fuentes. `para_vivir` y `para_conversar` vacíos.

## Reglas de oro

1. **NO INVENTAR NADA.** Cada afirmación sale de las notas y lleva en `fuentes` los ids de las notas que la respaldan (`macarthur_02#15`, `r1_004#3`). Si varias fuentes dicen lo mismo, condensalo en
   una sola afirmación con todos sus ids. Si un dato no está en las notas, no va. Solo podés citar ids que figuren en tu insumo. En las tablas, cada fila lleva respaldo en las `fuentes` de la tabla.
2. **CONDENSAR CON CRITERIO.** No es una lista de notas sino un texto que se lee de corrido, en 3 a 7 apartados con buen orden lógico. Uní lo repetido, priorizá lo central (importancia 3 y 2).
   Explicá en `notas_no_usadas` por qué quedaron afuera las de importancia 3 que no usaste.
3. **INTERPRETACIONES.** Cuando las fuentes difieren (la fecha de la carta, el Santiago autor, el sentido de «justificar», la unción de los enfermos…), presentá cada postura con quién la sostiene, sin tomar partido
   salvo que todas coincidan.
4. **TONO.** Castellano rioplatense neutro, cálido y claro, hablándoles a «ustedes». Explicá los términos técnicos la primera vez. Frases cortas. Nada de relleno. **No encadenes** «según X… Y agrega…»:
   nombrá al autor solo cuando aporta algo propio o cuando las fuentes difieren.
5. **LARGO.** El cuerpo (entrada + apartados) va en el rango de palabras que indica el archivo. `destacado` (opcional, en algunos apartados) es una sola oración para retener.
6. `versiculos`: hasta 3 versículos de **Santiago** que resumen la sección (la app pone el texto RVR1960; ref `C:V` o `C:V-V`, de no más de 3 versículos). Palabras de la Biblia entre «» solo si son textuales de la RVR1960
   de Santiago del insumo; los versículos de otros libros, parafraseados sin comillas y con su referencia.
7. `citas`: solo frases que aparecen como CITA en las notas, textuales, con su autor y obra (máximo 3).
8. `palabras`: solo palabras griegas que comentan las notas, con la grafía griega solo si figura en Santiago (`griego.py --verificar palabra`).
9. `refs_santiago`: los pasajes de Santiago que la sección trata (`C:V` o `C:V-V`); la app los usa para enlazar con los días.
10. Respetá el alcance: lo que corresponde a otra sección de la lista, mencionalo a lo sumo en una frase.
