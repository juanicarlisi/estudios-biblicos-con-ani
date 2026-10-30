# Apocalipsis: dónde quedamos (25-10-2026)

**Hecho**
- Corpus: 12 obras de la biblioteca (MacArthur, McGee x2, Larkin, Ladd, Beacon/Earle, Mundo Hispano t. 24, Carballosa y Beasley-Murray por OCR, Biblia MacArthur, Diccionario MH), libros de REFERENCIA3, 90 artículos de Coalición por el Evangelio y 101 documentos libres (Guzik, Gracia a Vosotros, Ligonier, 9Marcas, blog de TTL, muestra de MiSion).
- Extracción en `trabajo/extracciones/` (~250 archivos, unas 11.000 notas con página de origen). Instrucciones en `trabajo/prompts/extraer.md`; validador `scripts/validar_extraccion.py`.
- Griego (SBLGNT + Strong) en `trabajo/griego/`; mapas en `trabajo/mapas/`; unidades de lectura y pesos en `scripts/unidades.py` y `scripts/pesos.py` (≈80 días).

**Falta**
1. (HECHO) Extracción completa: los 194 bloques tienen sus notas.
2. Plan de días (sin tope de versículos; 20–30 min por día), partes y artículos/temas.
3. Escribir los días, cotejar citas con RVR1960 y griego, continuidad entre días.
4. App: adaptar `genesis/app/plantilla.html` (barra de progreso, mapas y diagramas en la página, anexos, griego en vez de hebreo).

**Pendiente de decidir:** los PDF de clases de TTL (Evangelio completo 14–15, Iglesia gloriosa 14) quedaron excluidos por prudencia; el curso «Maranata» y el de MiSion son de pago y no se tocaron. No hay trabajo de Santiago en el repositorio.


## Estado al 30-10-2026 (pausa pedida por el fundador: «Luego continuamos»)
- Días: 94 de 95 escritos y validados (OK). Falta el día 95 (agente en curso al pausar).
- Lanzados al pausar (pueden haber dejado archivos sin commitear en `trabajo/articulos/` y `trabajo/diagramas/`):
  - Diagramas: A (dg-estructura, dg-septenarios, dg-cartas), B (dg-escuelas, dg-milenio, dg-tribulacion), C (dg-candelero, dg-cristo, dg-ramera), D (dg-numeros, dg-tiempos, dg-cronologia). Falta dg-jerusalen (días 89-91 ya existen).
  - Artículos: I1-I5, P1-P6, T1-T3. Faltan P7-P10 y T4-T14.
- Al retomar: `ls trabajo/dias trabajo/articulos trabajo/diagramas`, validar (`validar_dia.py`, `validar_articulo.py ID`, `validar_diagrama.py`), relanzar lo que falte, luego construir la app (`apocalipsis/app/plantilla.html` + `construir.py`, modelo en `genesis/app/`), cotejos finales y commit.
- Pendiente de cotejo: Buswell figura como «postribulacional» en el día 45 y en la nota r1_010#12, pero Ryrie (r1_033#2) lo pone entre los mesotribulacionistas y él ubica el arrebatamiento en la séptima trompeta (r1_008#20). El diagrama dg-tribulacion lo atribuye «según Ryrie»; revisar el día 45 para que coincidan.
- Diagramas B (dg-escuelas, dg-milenio, dg-tribulacion) hechos y validados.
- Diagramas A (dg-estructura, dg-septenarios, dg-cartas) hechos y validados. Cotejo pendiente de comillas: dg-candelero, dg-cristo y dg-numeros usan «» también para texto no bíblico; deben ir en “ ” (solo la Biblia va entre «»).
- Diagramas D (dg-numeros, dg-tiempos, dg-cronologia) hechos y validados. Revisar: dg-tiempos tiene una fila extra («diez días» de 2:10) no pedida, se puede borrar; dg-cronologia usa «Nerva (96-98)», deducido (ninguna nota lo escribe), conviene confirmarlo o quitarlo.
