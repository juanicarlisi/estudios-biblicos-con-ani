# Instrucciones para extraer notas de los «puentes» entre bloques de lectura (carta de Santiago)

Mismo proyecto y mismas reglas que `extraer_biblio.md` (leelo primero: el formato de las notas, los tipos, la importancia, el campo `pagina` y la regla de oro de
**no inventar nada** valen igual). Esta tarea recupera lo que esa lectura dejó cortado.

## Qué es un puente

El comentario se leyó en bloques de páginas seguidos, sin superposición. Una idea que empieza al final de la última página de un bloque y sigue en la primera página del
bloque siguiente quedó cortada para los dos lectores y no se extrajo. Tu bloque reúne **pares de páginas contiguas**, cada par bajo un título
`##### PUENTE entre X y Y …`: la primera página es la última del bloque anterior y la segunda es la primera del siguiente.

## Tu tarea

En cada par, extraé **solo las ideas que cruzan el salto de una página a la otra**: la oración o el párrafo que empieza al final de la primera página y continúa en la
segunda (para entenderlo, tomá el párrafo entero: su comienzo en la primera página y su cierre en la segunda). **Todo lo demás de esas páginas ya fue extraído: ignoralo.**

- Si la primera página termina a mitad de una oración y la segunda empieza con la continuación, esa idea es tu objetivo.
- Si el salto cae justo entre dos párrafos completos (no hay nada cortado), el par no aporta: pasalo.
- Si lo que cruza es un fragmento sin sentido propio (dos palabras, un número de página, una referencia suelta), pasalo.
- Si una página trae encabezado de capítulo o de sección, o datos editoriales, no es una idea del autor: no la extraigas.
- Cada idea rescatada es una nota como cualquier otra (una idea del autor, entendible sola, 40 a 90 palabras): `ref`, `tipo`, `titulo`, `contenido`, `pagina`, `importancia`;
  `cita` solo si la frase textual figura tal cual en el bloque (puede cruzar el salto; copiala exacta). `pagina`: el rótulo de la página donde **empieza** la idea.
- Esperá pocas notas: de 0 a 2 por par (lo típico es 1). Un bloque de 8 pares da entre 5 y 14 notas. No rellenes: si un par no aporta, no escribas nada para él.

## Cómo trabajar

Igual que en `extraer_biblio.md`: una sola lectura del bloque (`Read` con `allow_large: true`), notas en una o dos tandas con `Write` en
`/home/user/trabajo_santiago/partes/<id>.p1.json` (luego `.p2.json`…), y después
`python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/unir_partes.py <id>` y
`python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/validar_extraccion.py /home/user/estudios-biblicos-con-ani/santiago/trabajo/extracciones/<id>.json`.
Corregí los ERRORES que marque el validador (editando la tanda; nunca `extracciones/<id>.json` a mano). Sin deliberar: leé y escribí.
Respondé una sola línea: `id: N notas, X errores, Y avisos`.
