# App combinada «1 Pedro a Apocalipsis» (HTML único, sin conexión)

Objetivo: un solo archivo `pedro-apocalipsis/estudio-pedro-a-apocalipsis.html` que junta el estudio de Apocalipsis (ya construido en `apocalipsis/`) y el de 1 Pedro a Judas
(`pedro-judas/`), con la misma calidad y funciones que `apocalipsis/estudio-apocalipsis.html`. Partí del constructor existente `apocalipsis/app/construir.py` + `apocalipsis/app/plantilla.html`
(leelos por tramos; funcionan: no los reescribas desde cero) y generalizalo a dos conjuntos de datos. NO modifiques `apocalipsis/` ni `pedro-judas/trabajo/` (solo lectura); escribí en `pedro-apocalipsis/app/` (`construir.py`, `plantilla.html`, `tipografias/` copiadas) y el HTML de salida.

## Datos
- Apocalipsis: `apocalipsis/trabajo/` (95 días, 29 artículos, 13 diagramas, 3 mapas, griego, `plan/*.json`). Día: int `dia` 1–95; refs «C:V».
- Pedro–Judas: `pedro-judas/trabajo/` (69 días, 14 artículos, 13 diagramas, mapas en `mapas/datos_mapas.json`, griego `griego/pedro_judas_griego.json` con `versiculos['1J']['4:8']`, `plan/plan.json` con 11 partes, `plan/articulos.json`, `plan/visuales.json`, `plan/fuentes_comentarios.json`).
  Diferencias de esquema: el día lleva `libro` (1P, 2P, 1J, 2J, 3J, Jd) y `antiguo_testamento`, y NO lleva `simbolos`; las refs llevan sigla («1P 2:4-8», «Jd 3-4»); ids de nota `<archivo>#<n>`.
  RVR1960 (no se commitea; solo scratch): `SCRATCH/biblia/rvr1960_apocalipsis.json` y `SCRATCH/biblia/rvr1960_pedro_judas.json` (SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad). El HTML incrusta solo los versículos clave de días y artículos de AMBOS estudios, con **assert de ≤500 versículos en total** y la leyenda de derechos.
  Las notas de fuentes salen de `*/trabajo/extracciones/*.json`; etiquetas de fuente: cada estudio tiene su propio `fuentes_comentarios.json` y prefijos (ver los constructores/`pesos.py` de cada uno); ids de ambos estudios no chocan (prefijos distintos), pero si chocan, prefijá por estudio.

## Estructura de la app
- Numeración **por libro** («1 Pedro · día 3», «Apocalipsis · día 45»); el progreso es **único** (global sobre 164 días + por libro + por parte + por día/sección). Claves de progreso estables: `1P-3`, `Ap-45`; compatibles con las ya guardadas del estudio de Apocalipsis (si alguien usa los dos HTML, que no se rompa: las claves viejas de Apocalipsis se leen como `Ap-N`).
- Índice por libros en el orden canónico: 1 Pedro, 2 Pedro, 1 Juan, 2 Juan, 3 Juan, Judas, Apocalipsis, con sus partes (11 de Pedro–Judas y 10 de Apocalipsis) y progreso por libro; «continuar donde dejaron».
- Todas las funciones de la app de Apocalipsis (ver `apocalipsis/app/` y la lista de `apocalipsis/trabajo/prompts/construir_app.md`): vista de día, visuales en la misma página (mapas SVG, diagramas tabla/líneas/tarjetas), anexos, páginas agregadas (Artículos de cada estudio; Diagramas; Mapas; Palabras griegas de los dos estudios con índice; Cristo en las cartas y en Apocalipsis; Línea de tiempo), búsqueda de texto completo, modo oscuro, tamaño de letra, impresión, teclado, notas con copia de seguridad, offline, cero dependencias externas. Los días de Pedro–Judas no tienen «Símbolos»; sí tienen «Antiguo Testamento en el pasaje» (campo `antiguo_testamento`): mostralo.
- Páginas agregadas nuevas: «Las cartas de Pedro, Juan y Judas» (artículos I1–I5, P1–P3, T1–T6 de Pedro–Judas) y «Apocalipsis» (los 29 de Apocalipsis), con ids de artículo prefijados por estudio (p. ej. `pj-T2` y `ap-T2`) para que no choquen; los enlaces a anexos desde los días deben resolver al estudio correcto (el día sabe a qué libro/estudio pertenece).
- Mapas: unir los de ambos estudios (Pedro–Judas: provincias de Asia Menor, Babilonia, Roma, Éfeso, Patmos, Sodoma…; Apocalipsis: los suyos) con crédito de Natural Earth y OpenBible (CC BY 4.0).
- Tolerancia a faltantes: si falta un artículo o diagrama de Pedro–Judas (todavía se están escribiendo algunos: 14 artículos, 13 diagramas), la app debe mostrar «en preparación» y funcionar igual (probalo con una variable `OMITIR=...`), y el build debe poder rehacerse sin tocar nada más cuando aparezcan.
- Tamaño razonable (< ~30 MB; informá el tamaño).

## Verificación
- `python3 pedro-apocalipsis/app/construir.py` sin errores y con el assert de versículos; probalo con Playwright (chromium preinstalado) en 390 px y 1280 px: un día de cada libro, un artículo de cada estudio, un diagrama de cada estudio, el índice, la búsqueda, y la migración de progreso viejo de Apocalipsis; sin errores de consola; revisá las capturas (no las commitees).
- Respuesta final: tamaño del HTML, qué funciones quedaron, qué no pudiste hacer (una línea cada una). Sin commits.
