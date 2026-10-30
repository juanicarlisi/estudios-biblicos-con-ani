# CLAUDE.md — estudios bíblicos (Génesis, Varón, Apocalipsis)

Español rioplatense, directo. Estudios para un matrimonio protestante. **No inventar nada**: todo sale de las fuentes (biblioteca y
REFERENCIA3, solo autores protestantes confiables, categoría A), citando fuente y página; nunca copiar texto de los libros.
RVR1960 no se commitea: solo versículos clave por referencia (≤3 por día, ≤500 en total). Comillas «» solo para texto bíblico literal.
Escuelas escatológicas (pret./hist./fut./idealista; pre/a/posmilenial; pre/mid/postribulacional) se presentan sin tomar partido.

## Eficiencia (obligatorio)
- Arrancar con `python3 apocalipsis/trabajo/scripts/estado.py` (1 línea de estado) y leer solo la sección pertinente de
  `apocalipsis/RETOMAR.md` (`grep -n "^## "` antes). No listar carpetas ni leer JSON enteros: usar Grep/`jq`/Python para extraer campos.
- Nunca leer `trabajo/extracciones/`, `trabajo/dias/` ni `trabajo/articulos/` completos (MBs): buscar por id/Grep y leer el tramo.
- Trabajo masivo (días, artículos, diagramas, extracción) → un subagente por pieza con su prompt en `trabajo/prompts/`; el agente
  principal solo lanza, valida con `estado.py --validar` y commitea. Subagentes de escritura: opus; extracción/mecánico: sonnet.
- Respuestas finales de agentes: una línea. Validar por script, no releyendo.
- Al cerrar: actualizar `RETOMAR.md` (estado en ≤10 líneas), commit y push a la rama de trabajo.
