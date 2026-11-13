# Retomar el megaestudio

## Estado (nov-2026)
- **Ciclo 1 «La Biblia: la Palabra de Dios y cómo leerla» terminado: 54 días escritos y verificados** (`python3 trabajo/scripts/verificar.py $(seq 1 54)` → 54/54 OK): series 1.1 (revelación, inspiración, inerrancia, suficiencia, autoridad), 1.2 (canon, manuscritos, traducciones), 1.3 (hermenéutica y estudio inductivo), 1.4 (hebreo, arameo, griego, léxicos, palabras clave) y 1.5 (panorama de la redención).
- Plan maestro: 20 ciclos, 103 series, ≈1.974 días (`trabajo/plan/PLAN-MAESTRO.md`). Solo el ciclo 1 está detallado día por día; el resto se detalla por etapas (`plan/plan.json` solo crece al final; ids fijos).
- Biblioteca: 1.287 archivos clasificados (`trabajo/catalogo/resumen.md`; correcciones manuales en `catalogo/revisiones.json`, que mandan sobre la clasificación automática). 869 fuentes registradas (libros de autores A y 66 fuentes web verificables, con URL y fecha). El ciclo 1 cita 206 fuentes distintas.
- Revisión de comentarios adventistas dudosos: `trabajo/catalogo/revision_adventistas.md` (14 de 17 excluidos; Moody de Lucas, aceptado).
- Verificador (`scripts/verificar.py`): páginas y fuentes, citas literales, frases entre «», existencia de cada versículo en la RVR1960, cifras, autores nombrados, extensión (1.800–3.300 palabras) y **grafía de palabras hebreas y griegas contra los lemas de Strong y el texto hebreo (WLC) y griego (SBLGNT)**.

## Pendiente (en este orden)
1. Ciclo 2 «Dios» (84 días): detallar series y fichas de encargo (`plan/specs_ciclo1.py` es el modelo); libros ya registrados: Pink, Tozer, Packer, Grudem, MacArthur, Berkhof, Washer, Sproul, Owen.
2. OCR pendiente: cola de ~17 libros en curso (Henry ya hecho); quedan ~35 escaneos sin pasar (lista con `scripts/textos.py`; correr `scripts/ocr.py <id>`). «Gozo inefable» (Lloyd-Jones) y Romanos de MacArthur esperan OCR; Moody de Lucas, en cola.
3. Fuentes externas aún sin conseguir: Museo de Israel y códices Sinaítico/Vaticano (el proxy los rechaza), documentos primarios de otras religiones y tradiciones (ciclos 17–18), mundo bíblico y arqueología (ciclo 16).
4. Revisión humana de lo escrito: los días se verifican por programa (fuentes, citas, versículos, grafías), pero no se comprueba que cada resumen refleje fielmente su página; conviene leer y marcar lo que no cierre.

## Lecciones del sprint
- Los redactores se pasan de largo y a veces esquivan advertencias reescribiendo; el verificador y la guía (`trabajo/GUIA-REDACCION.md`) ya lo marcan. Los falsos positivos del control de autores se resolvieron por reglas (apellido con mayúscula, vecino citado, nombres de libros bíblicos, URL de la fuente web).
- Un redactor por día con Sonnet rinde ≈200–280 mil tokens por día; lotes de 8–10 en paralelo, ~10–15 min por lote.

## Reconstruir
`python3 megaestudio/app/construir.py` (HTML local) o con `--artefacto` (versión para claude.ai).
