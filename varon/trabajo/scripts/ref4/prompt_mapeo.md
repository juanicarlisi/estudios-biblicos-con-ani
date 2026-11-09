# Asignar notas nuevas a los días del estudio «El varón según Dios»

Contexto: el estudio tiene 512 días ya escritos (20–30 min cada uno, 17 partes A–Q). Se sumaron notas nuevas extraídas de libros nuevos. Tu tarea: decidir, para cada nota nueva de tu(s) parte(s), dónde va. No se pierde nada: lo valioso debe terminar en algún día.

Tu insumo (uno o varios archivos) trae, por parte: (1) el índice de días: `día | título | títulos de apartados`; (2) las notas nuevas: `id | importancia | tipo | título | subtema | resumen [día sugerido por similitud automática, 0 si ninguno]`.

Para CADA nota, elegí UNA de estas salidas:
- un número de día: la nota aporta algo útil a ese día (otra explicación, un ejemplo, una cita, un dato, una práctica, otra postura). Elegí el día cuyo tema trata lo mismo; puede ser de otra parte si encaja mejor (el índice de otras partes no lo ves: usá solo días de tu parte; si claramente corresponde a otra parte, marcá "otra:<letra>").
- `cub`: el día ya trata exactamente eso y la nota no suma nada distinto (usalo con cuidado; solo importancia 1–2, y solo cuando de verdad no agrega nada).
- una clave de día nuevo (`n1`, `n2`, …): ningún día existente trata este tema y varias notas juntas lo justifican.

Días nuevos: proponé uno solo si hay un tema coherente, importante para la vida del varón, no tratado por ningún día, con al menos 4 notas (alguna de importancia 3 o varias de 2) que lo sostengan en 20–30 minutos. Sé exigente: ante la duda, asigná las notas a días existentes (se suman como material de profundización). Para cada día nuevo: título, objetivo en una frase y `despues_del_dia` (el número de día de tu parte tras el cual iría).

## Salida
Escribí con Write un archivo JSON (el que te indique la tarea) con esta forma exacta:
{"asignaciones": {"r_003#5": "123", "r_003#6": "cub", "r_004#2": "n1", "r_004#9": "otra:H"},
 "nuevos": [{"clave": "n1", "parte": "G", "titulo": "…", "objetivo": "…", "despues_del_dia": 215}]}
Todas las notas de tus partes tienen que figurar en "asignaciones". JSON válido, sin texto extra. Respuesta final: una línea `partes X: N notas → a días D, cub C, otra O, nuevos K`.
