# Instrucciones para armar diagramas del estudio de Apocalipsis

Armás diagramas (tablas, líneas de tiempo comparadas y tarjetas) para un estudio de Apocalipsis para un matrimonio protestante. Regla de oro: **NO INVENTAR NADA**.
Todo sale de las notas extraídas de los libros y de los días ya escritos; si un dato no está, se deja afuera o se marca «las fuentes no lo dicen».

## Cómo trabajar
1. Leé `apocalipsis/trabajo/plan/esquema_diagrama.md` (formas exactas) y `apocalipsis/trabajo/plan/visuales.json` (qué debe mostrar cada diagrama).
2. Reuní el material: usá Grep sobre `/home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/extracciones/*.json` (palabras clave del tema) y leé los días relacionados
   (`apocalipsis/trabajo/dias/dia_NN.json`; el plan está en `apocalipsis/trabajo/plan/plan.json`). Para citar una nota necesitás su id `archivo#n`: el archivo es el nombre del
   JSON sin `.json` y `n` la posición (desde 1) dentro de su lista `notas`. (Podés usar `python3 -c` para listar ids y textos de un archivo.) Verificá cada id antes de usarlo.
3. Escribí cada diagrama con Write en `/home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/diagramas/<id>.json` y validalo con
   `python3 /home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/scripts/validar_diagrama.py <id>` hasta que no haya ERRORES.
4. Respuesta final: una línea por diagrama: `<id>: tipo · filas/carriles/tarjetas · fuentes distintas · avisos`.

## Criterios
- Texto breve y claro (castellano rioplatense neutro). Cada fila, carril o tarjeta con `fuentes` (al menos una).
- Posturas atribuidas (autor + escuela); sin tomar partido. Los autores carismáticos/proféticos, atribuidos y fieles.
- Referencias bíblicas verificadas contra el texto de los insumos de los días (`SCRATCH/insumos/dia_NN.txt`, SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad) cuando dudes.
- No toques otros archivos, no hagas commits, no publiques nada como artefacto.
