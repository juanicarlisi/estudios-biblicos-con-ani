# Instrucciones para asignar notas generales a las secciones del estudio de Santiago

Vas a ordenar notas de estudio sobre Santiago para escribir la introducción, los panoramas de las cinco partes, los temas y los anexos. Cada línea del archivo de candidatas es una nota con su id entre corchetes, la referencia,
el tipo, la importancia, la fuente, el título y el comienzo del contenido.

## Cómo trabajar

1. Leé con **UNA llamada a Read** (con `allow_large: true`) `/home/user/trabajo_santiago/insumos/libro/cand_NN.txt` (el NN que te asignaron).
2. Asigná cada nota a **UNA sola sección**, la que mejor le corresponde, entre las de abajo, y escribí el resultado con Write en `/home/user/trabajo_santiago/insumos/libro/clasif_NN.json`:
   `{"asignaciones": [{"seccion": "T5", "ids": ["macarthur_12#3", "..."]}, ...]}` (una entrada por sección usada; copiá los ids exactamente como aparecen entre corchetes).
3. Respondé con una sola línea: `cand_NN: N notas asignadas, M dejadas afuera`.

Sé directo: no hace falta deliberar nota por nota; clasificá por el título y el comienzo del contenido.

## Secciones

INTRODUCCIÓN
- I1 «Quién escribió la carta»: el nombre Santiago/Jacobo, cuál de los Santiagos es el autor, su familia (hermano del Señor), su lugar en la iglesia de Jerusalén, su carácter, su muerte, las dudas sobre la autoría.
- I2 «A quién, cuándo y desde dónde»: los destinatarios («doce tribus en la dispersión»), su situación (pobreza, persecución, ricos y pobres, la sinagoga y la iglesia), la fecha (temprana o tardía), el lugar de escritura.
- I3 «Qué clase de carta es»: el género (epístola general, sabiduría, parénesis, sermón), el estilo, el griego, las imágenes de la naturaleza, el uso del AT, el parentesco con Proverbios y con la literatura sapiencial.
- I4 «Estructura y mensaje»: bosquejos y divisiones de la carta, propósito y tema central, el canon (cómo fue recibida, Lutero y la «epístola de paja», antilegómena).
- I5 «Santiago, Jesús y Pablo»: ecos de las enseñanzas de Jesús (Sermón del Monte) en general, la relación con Pablo y el resto del NT en general (no el comentario de un versículo puntual).
PANORAMAS (notas que abarcan un capítulo entero o un bosquejo de un capítulo)
- P1 capítulo 1 · P2 capítulo 2 · P3 capítulo 3 · P4 capítulo 4 · P5 capítulo 5
TEMAS
- T1 «Pruebas y perseverancia» · T2 «La tentación y el pecado» · T3 «La sabiduría» · T4 «La Palabra: oír y hacer» · T5 «Fe y obras» · T6 «La lengua» · T7 «Ricos, pobres y justicia» · T8 «Humildad y mundanalidad» ·
  T9 «Oración, enfermedad y restauración» · T10 «Cristo en Santiago» (cómo la carta nombra, muestra y apunta a Jesús; su venida)
ANEXOS
- A1 «Los Santiagos del Nuevo Testamento»: el hijo de Zebedeo, el hijo de Alfeo, el hermano del Señor, los hermanos de Jesús.
- A2 «Santiago y el Sermón del Monte»: tabla de ecos de Jesús (notas que señalan un paralelo puntual con los evangelios).
- A3 «Pablo y Santiago»: comparación de fe, obras y justificación entre ambos.
- A4 «Santiago y el Antiguo Testamento»: Abraham, Rahab, Job, Elías, Levítico 19, Proverbios, la lluvia, etc.
- A5 «Las imágenes de la carta»: ola, hierba, espejo, freno, timón, fuego, fuente, higuera, niebla, polilla, labrador…
- A6 «Glosario»: términos que conviene explicar (diáspora, parénesis, canon, Gehena, etc.).

## Criterios

- Una nota de aplicación, de personaje o de ilustración va al tema que mejor ilustra.
- Dejá AFUERA (no la pongas en ninguna lista) la nota que no trata Santiago, es demasiado general para aportar, solo menciona la carta de paso o es un devocional sin contenido.
- No inventes ids.
