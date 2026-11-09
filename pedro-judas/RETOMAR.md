# RETOMAR — estudio de 1 Pedro a Judas (parte nueva de «1 Pedro a Apocalipsis»)

## Estado (09-11-2026)
- Pipeline armado en `trabajo/` como espejo de `apocalipsis/trabajo/` (scripts, prompts, plan); probado con corridas cortas, sin agentes.
- Corpus: 158 bloques en `SCRATCH/pj_bloques/` (11,9 M caracteres): A 76 (comentarios por libro y tramos 1P-Jd de Beacon t.10, Mundo Hispano t.23-24,
  Nuevo Comentario Bíblico, Biblia MacArthur), B 2 (Diccionario Mundo Hispano), C 60 (REFERENCIA3), D 20 (REFERENCIA4 categoría A alto/medio).
- Extracción: 0/158 (no lanzada). `plan/plan.json` es PROVISORIO (sin notas): se rehace al terminar la extracción.
- Datos listos: griego SBLGNT (`trabajo/griego/pedro_judas_griego.json`, 324 vv), RVR1960 en `SCRATCH/biblia/rvr1960_pedro_judas.json` (no se commitea).
- Plan editorial: 74 unidades de sentido, 11 partes, 14 artículos (I1-I5, P1-P3, T1-T6), 4 mapas y 13 diagramas.
- Estado en una línea: `python3 pedro-judas/trabajo/scripts/estado.py` (`--bloques` lista lo que falta extraer; `--validar` valida).
SCRATCH = /tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad

## Recetario (pasos siguientes)
1. **Corpus** (ya hecho; rehacer solo si cambian fuentes): `python3 trabajo/scripts/armar_corpus.py [--solo A,B,C,D]`. Si se pierde SCRATCH:
   `git lfs pull --include="MATERIAL SOPORTE/6?*/*"` en la biblioteca, `pdftotext` a `SCRATCH/txt/pj_*.txt` (nombres en `FAM_A` de armar_corpus.py),
   `griego.py --construir`, `bajar_rvr.py`. Umbrales de REFERENCIA3/4: `UMBRAL_R1=9 MIN_R2=6` (1P y 1J se citan mucho de paso).
2. **Extracción** (sonnet, un subagente por bloque, en tandas): prompt = `trabajo/prompts/extraer.md` + «Tu bloque: <id>». Ids en
   `SCRATCH/pj_bloques/_indice.json` (o `estado.py --bloques`). Validar con `validar_extraccion.py <id>`. Empezar por A (comentarios).
3. **Plan de días**: `python3 trabajo/scripts/pesos.py` (revisar) y `python3 trabajo/scripts/plan_dias.py` (OBJ=40000, igual que Apocalipsis:
   ~20-30 min por día; cada día de un solo libro salvo 2J+3J). Luego `insumos_dias.py` e `insumos_articulos.py` (→ `SCRATCH/pj_insumos/`).
4. **Días** (opus, un subagente por día): `trabajo/prompts/escribir_dia.md` + «Tu día: N»; validar con `estado.py --validar`.
5. **Artículos** (opus): `trabajo/prompts/escribir_articulo.md` + «Tu artículo: <ID>» (I1-I5 y P1-P3 después de los días del libro).
6. **Diagramas** (opus o sonnet): `trabajo/prompts/escribir_diagrama.md` + ids de `plan/visuales.json`. Mapas: `scripts/datos_mapas.py` (en curso aparte).
7. Después: app combinada `pedro-apocalipsis/` (ojo: el día de estos libros no tiene `simbolos` y suma `libro` y `antiguo_testamento`).

## Cola de extracción (09-11-2026)
- `trabajo/plan/cola_extraccion.json`: 72 grupos de a 1-2 bloques (A, B, D y `r1`); los 40 bloques `r2` (ventanas sueltas de REFERENCIA3, bajo rendimiento) quedan para el final, solo si hay huecos de cobertura.
- Se lanza un subagente sonnet por grupo (prompt: `trabajo/prompts/extraer.md`, «Tus bloques: X y Y; un JSON por bloque»). Faltantes: `python3 trabajo/scripts/estado.py --bloques`.
- Lanzados primero: grupos 0-3 (mac1p_01…08).

## Estado (09-11-2026, noche)
- Extracción terminada para A, B, D y r1 (118/158 bloques; los 40 `r2` quedan diferidos, solo si el plan de días muestra huecos de cobertura).
- Plan de días hecho (`plan/plan.json`): 69 días en 11 partes (1P 24, 2P 14, 1J 18, 2J-3J 4, Jd 9). Insumos: `python3 trabajo/scripts/insumos_dias.py` e `insumos_articulos.py` (→ `SCRATCH/pj_insumos/`).
- Pilotos de días: 1, 16 y 40. Si salen bien, lanzar el resto (opus, un agente por día, prompt `trabajo/prompts/escribir_dia.md`). Título duplicado a corregir: días 67 y 68 (Jd 17-20 / 21-23).
- Después: artículos (14), diagramas (13), mapas, app combinada `pedro-apocalipsis/`.
- Pasada de recorte pendiente al final: días por encima de ~2.700 palabras según el validador (p. ej. día 44 = 2.912). Duplicado de título a corregir: días 67 y 68 (Jd 17-20 / 21-23). Los días se escribieron sin tocar la RVR en el repo; el assert de ≤500 versículos (con los 183 de Apocalipsis) se controla en la app combinada.

## Estado (10-11-2026)
- Los 69 días están escritos y validan. Artículos (14) y diagramas (13) lanzados; mapas ya tienen datos (`mapas/datos_mapas.json`).
- Pendientes de cotejo: (1) contexto «antes/después» de los días escritos en paralelo (el día 69 se escribió sin el 68; revisar vecinos); (2) pasada de recorte de los días >2.700 palabras (p. ej. 44, 50); (3) `cotejar_citas.py` adaptado a pedro-judas (comillas «» solo texto RVR literal); (4) coherencia entre días y artículos sobre datos discutidos.
- Siguiente gran paso: app combinada `pedro-apocalipsis/` (índice por libros: 1P, 2P, 1J, 2J, 3J, Jd, Ap; progreso único; numeración por libro) con el assert de ≤500 versículos RVR en total.
- 10-11: contenido completo y validado (69 días, 14 artículos, 13 diagramas). `python3 pedro-judas/trabajo/scripts/cotejar_citas.py`: 125 de 1.779 frases «» no coinciden con la RVR de 1P–Jd (citas de otros libros —no verificables con ese archivo—, términos de autores que deben ir en “ ” y posibles imprecisas). Igual que en Apocalipsis (512 de 3.243): pendiente pasar a “ ” lo no bíblico y corregir lo impreciso.
