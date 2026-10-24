# Instrucciones para escribir un día del estudio de Santiago

Vas a escribir el estudio de **un día** de un plan de lectura de la carta de Santiago para un matrimonio protestante joven de Buenos Aires que dedica
**20 a 30 minutos por día** a leer y estudiar juntos. Quieren entender las Escrituras a fondo y vivirlas.

## Cómo trabajar

1. Leé con **UNA llamada a Read** (con `allow_large: true`) el archivo de insumos del día: `/home/user/trabajo_santiago/insumos/dia_NN.txt`. Trae el texto RVR1960 del pasaje
   y **todas** las notas extraídas de su biblioteca para ese tramo, cada una con un id entre corchetes (`[macarthur_05#12]`). Leé también
   `/home/user/estudios-biblicos-con-ani/santiago/trabajo/plan/esquema_dia.md` (formato y reglas) si no lo tenés en mente.
2. Escribí el día con la herramienta Write en `/home/user/estudios-biblicos-con-ani/santiago/trabajo/dias/borrador_NN.json`, siguiendo el esquema. Sé directo: la tarea
   es **condensar con criterio**, no deliberar; no hagas borradores del texto en tu razonamiento, escribilo una vez.
3. Corré `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/validar.py --borradores --dias N` (N = el número del día) y corregí con Edit todo lo que marque
   (ids que no figuran en tu insumo, rangos fuera del pasaje, campos vacíos, palabras griegas que no son de Santiago…). Los AVISOS revisalos y corregí los que sean reales.
4. Respondé con una sola línea: `día N: palabras del cuerpo principal, notas usadas, errores pendientes`.

## Reglas de oro

1. **NO INVENTAR NADA.** Cada afirmación sale de las notas y lleva en `fuentes` los ids de las notas que la respaldan (`macarthur_02#15`, `r1_004#3`). Si varias fuentes dicen lo mismo,
   condensalo en una sola afirmación con todos sus ids. Nada de conocimiento propio: si un dato no está en las notas, no va. Solo podés citar ids que figuren en tu insumo.
2. **CONDENSAR CON CRITERIO.** No es una lista de notas sino un estudio que se lee de corrido. Ordená por el texto, uní lo repetido (muchas notas dicen lo mismo), priorizá lo central
   (importancia 3 y 2) y lo que ayuda a entender y a vivir. Lo valioso que no entra en el flujo principal va a `profundizar` (optativo). Que no se pierda nada importante: si dejás afuera
   notas de importancia 3, explicá por qué en `notas_no_usadas`.
3. **INTERPRETACIONES.** Cuando las fuentes difieren (p. ej. a quién escribe, la fecha, el sentido de «justificar» en 2:21-24, la unción con aceite), presentá cada postura con quién la sostiene,
   sin tomar partido salvo que todas coincidan.
4. **TONO.** Castellano rioplatense neutro, cálido y claro, hablándoles a «ustedes». Explicá los términos técnicos la primera vez. Frases cortas. Nada de relleno ni de frases hechas.
   **No encadenes** «según MacArthur… Kistemaker agrega… Carballosa dice…». Nombrá al autor solo cuando aporta algo propio (una postura, una frase memorable, un dato que solo él da) o cuando
   las fuentes difieren; lo demás se afirma directamente y las fuentes quedan en `fuentes` (la app las muestra como etiquetas).
5. **PRÁCTICO PARA EL DÍA.** El cuerpo principal (contexto, panorama, secciones, palabras, cristo, eco_de_jesus, interpretaciones, biblioteca, conexiones, para_vivir) debe leerse en 20 a 30 minutos:
   **2.000 a 3.000 palabras**. Un día con poco material puede ser más corto (lo necesario). Lo valioso que no entra va a `profundizar`.
6. **CONTEXTO.** `contexto`: qué pasó antes (resumen del tramo anterior), qué pasa ahora, dónde y cuándo (si las fuentes dan fechas, decí de quién es la cronología) y qué viene después.
   Esto le da a cada día una línea clara y progresiva: usá los títulos de los días anterior y siguiente que trae el insumo.
7. **VERSÍCULO CLAVE.** Solo la referencia (la app pone el texto) y por qué es clave. Debe estar dentro del pasaje del día.
8. **SECCIONES.** Siguen el texto en orden, por unidades de sentido; el `rango` de cada una está dentro del pasaje del día. Si el día es de un solo versículo, una sección alcanza.
9. **PALABRAS.** Solo palabras griegas que comentan las notas. Escribí la grafía griega **solo si la nota la trae y figura en Santiago** (podés comprobarlo con
   `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/griego.py N:V` que muestra las palabras griegas del versículo, o `griego.py --verificar palabra`); si no, dejá `griego` vacío y usá la transliteración.
10. **ECO DE JESÚS** (`eco_de_jesus`): solo lo que las notas ligan entre el pasaje y palabras o hechos de Jesús (Sermón del Monte y otros). **CRISTO** (`cristo`): cómo el pasaje apunta a Cristo o lo muestra, según las notas.
11. **BIBLIOTECA.** `biblioteca`: aportes de los libros de referencia (notas cuyo id empieza con `r1_` o `r2_`), con autor y obra. Si no hay, lista vacía.
12. **PARA LA VIDA.** `para_conversar` (exactamente 3 preguntas, pensadas para una pareja) y `para_orar` se formulan a partir de lo que enseñan las fuentes del día.
13. **TEXTO BÍBLICO.** Si ponés palabras de la Biblia entre comillas «», que sean textuales de la RVR1960 de Santiago del insumo; los versículos de otros libros, **parafraseados sin comillas** y con su referencia.
14. **DIAGRAMA** (opcional): solo si las notas dan material para un esquema fiel (un proceso, una escalera de mandatos, una comparación, una serie de imágenes) y le sirve al lector; tipos y formato en el esquema.
    Todo lo que dice el diagrama sale de las notas que citás en su `fuentes`.
15. **ANEXOS** (opcional): si el insumo trae una lista de temas y anexos del estudio y el pasaje los toca de lleno, enlazalos con una frase de por qué leerlos (`id` y `por_que`).
16. **DÍAS COMPARTIDOS.** Si el insumo dice que el pasaje se estudia en varios días, escribí solo lo que corresponde al enfoque de este día y no repitas lo de los otros.
