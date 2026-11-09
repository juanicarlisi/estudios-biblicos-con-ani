# Instrucciones para armar diagramas del estudio de 1 Pedro a Judas

Armás diagramas (tablas, líneas de tiempo comparadas y tarjetas) para un estudio de 1 Pedro, 2 Pedro, 1, 2 y 3 Juan y Judas para un
matrimonio protestante. Regla de oro: **NO INVENTAR NADA**. Todo sale de las notas extraídas de los libros y de los días ya escritos;
si un dato no está, se deja afuera o se marca «las fuentes no lo dicen».

## Cómo trabajar
1. Leé `pedro-judas/trabajo/plan/esquema_diagrama.md` (formas exactas) y `pedro-judas/trabajo/plan/visuales.json` (qué debe mostrar cada diagrama).
2. Reuní el material: usá Grep sobre `/home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/extracciones/*.json` (palabras clave del tema) y leé los días relacionados
   (`pedro-judas/trabajo/dias/dia_NN.json`; el plan está en `pedro-judas/trabajo/plan/plan.json`). Para citar una nota necesitás su id `archivo#n`: el archivo es el nombre del
   JSON sin `.json` y `n` la posición (desde 1) dentro de su lista `notas`. (Podés usar `python3 -c` para listar ids y textos de un archivo.) Verificá cada id antes de usarlo.
3. Escribí cada diagrama con Write en `/home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/diagramas/<id>.json` y validalo con
   `python3 /home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/scripts/validar_diagrama.py <id>` hasta que no haya ERRORES.
4. Respuesta final: una línea por diagrama: `<id>: tipo · filas/carriles/tarjetas · fuentes distintas · avisos`.

## Criterios
- Texto breve y claro (castellano rioplatense neutro). Cada fila, carril o tarjeta con `fuentes` (al menos una).
- Posturas atribuidas (autor + tradición o escuela); sin tomar partido.
- Referencias bíblicas con sigla (`1P 2:4-8`, `Jd 3`), verificadas contra el texto de los insumos de los días (`SCRATCH/pj_insumos/dia_NN.txt`,
  SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad) cuando dudes. Comillas «» solo para texto bíblico literal.
- No toques otros archivos, no hagas commits, no publiques nada como artefacto.

## Ahorro de contexto
- Buscá con Grep (palabras clave, tipo de nota) y extraé ids con `python3 -c`; no leas extracciones ni días enteros si no hace falta.
- Un solo ciclo de escritura + validación por diagrama.
