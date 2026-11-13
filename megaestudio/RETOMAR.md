# Retomar el megaestudio

## Estado (nov-2026)
- Plan maestro hecho (`trabajo/plan/PLAN-MAESTRO.md`): 20 ciclos, 103 series, ≈1.974 días, contrastado con IBBA, The Master's Seminary, SITB, DTS, RTS, SBTS y TTL (`trabajo/plan/institutos/`).
- Catálogo de la biblioteca (`trabajo/catalogo/resumen.md`): 1.287 archivos; 706 clasificados A; **480 sin clasificar** (ref4 «nuevos», ref4 01–08 y los 117 comentarios por libro del repo `biblioteca-estudios-biblicos`, que son punteros LFS).
- Registro de libros con texto extraído: 155 (ref3: Teología sistemática, Relación con Dios, Apologética, Escatología, Espíritu Santo). 8 son escaneos sin texto (hace falta OCR): ver `scripts/textos.py`.
- Serie 1.1 «Para qué estudiamos la Biblia» (días 1–6): ver `trabajo/dias/`.

## Pendiente (en este orden)
1. Clasificar los 480 libros sin clasificar (criterio: `genesis/trabajo/clasificacion/criterio.md`); bajar `libros-referencia4` por carpetas y los LFS de `biblioteca-estudios-biblicos`.
2. Detallar la serie 1.2 (canon, manuscritos y traducciones) y siguientes; escribir por sprints de ~6 días.
3. Fuentes externas verificadas para: mundo bíblico, religiones comparadas, tradiciones cristianas, idiomas bíblicos (Strong). Cada dato con URL y fecha de consulta.
4. Confirmar con el lector el orden de los ciclos y qué ciclos priorizar (ver preguntas al final de la sesión).

## Reconstruir
`python3 megaestudio/app/construir.py` (necesita los textos de libros solo para escribir y verificar días, no para construir).
