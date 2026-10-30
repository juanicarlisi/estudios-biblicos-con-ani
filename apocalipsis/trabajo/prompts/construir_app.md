# Construir la app del estudio de Apocalipsis (HTML único, sin conexión)

Modelo a adaptar: `genesis/app/plantilla.html` y `genesis/app/construir.py` (leelos por tramos; ya funcionan, no los reescribas desde cero:
copiá lo que sirve —layout de 3 columnas, router por hash, progreso y notas en localStorage, chips de fuentes con popover, tipografías
embebidas en base64, copia de seguridad de notas— y adaptá). Salida: `apocalipsis/estudio-apocalipsis.html`; fuentes: `apocalipsis/app/plantilla.html`,
`apocalipsis/app/construir.py`, `apocalipsis/app/tipografias/` (copiá las de Génesis y sumá una con glifos griegos, p. ej. la ya usada
en Génesis si cubre griego; si no, una libre OFL descargable o `GFS Didot`/`Gentium` si hay en el sistema; verificá licencia OFL).

## Datos de entrada (todo en `apocalipsis/trabajo/`)
- `plan/plan.json` (95 días + `partes` p1–p10), `dias/dia_NN.json` (esquema en `plan/esquema_dia.md`), `articulos/art_<ID>.json`
  (`plan/esquema_articulo.md`; 29: I1–I5, P1–P10, T1–T14), `diagramas/dg-*.json` (`plan/esquema_diagrama.md`; tabla/lineas/tarjetas),
  `plan/visuales.json` (mapas y diagramas disponibles), `plan/fuentes_comentarios.json` (etiquetas de fuentes), `mapas/datos_mapas.json`,
  `griego/` (SBLGNT+Strong por versículo).
- Ids de fuente: `<archivo de extracción>#<n>`; el resumen y la página salen de `extracciones/<archivo>.json` (posición n, base 1);
  la etiqueta de la fuente sale del prefijo (ver `scripts/pesos.py`/`armar_corpus.py` y `fuentes_comentarios.json`; para r1/r2/web se parsea
  «Autor, Obra:» del contenido). Los chips muestran autor + obra + página y, al tocar, el texto resumido de la nota.
- RVR1960: **no se commitea**. `SCRATCH/biblia/rvr1960_apocalipsis.json` (SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad;
  variable de entorno SCRATCH). El HTML incrusta solo los versículos clave (`versiculo_clave.ref` de días + `versiculos[].ref` de artículos),
  **con `assert` de ≤ 500 versículos en total** y la leyenda de derechos. Si falta el archivo, el build avisa y sigue sin texto bíblico.

## Funciones obligatorias
1. Barra de progreso: global (días leídos/95), por parte (p1–p10) y dentro de cada día (secciones leídas). Marcar día como leído; «continuar donde dejé».
2. Vista de día: contexto (antes/ahora/dónde/cuándo/después), versículo clave, panorama, secciones con notas y chips, símbolos, palabras griegas
   (tipografía griega), Cristo en el pasaje, interpretaciones (posturas atribuidas, sin tomar partido), biblioteca, conexiones, para vivir / conversar / orar,
   «profundizar» plegable, notas personales por día. Mostrar `minutos`.
3. Visuales EN LA MISMA PÁGINA del día (`visuales` ≤3): mapas SVG (render desde `mapas/datos_mapas.json`; Natural Earth + OpenBible, CC BY 4.0: agregar crédito)
   y diagramas (render genérico tabla/lineas/tarjetas) incrustados plegables; cada uno con enlace a su página completa.
4. Anexos: enlaces desde el día a los artículos (`anexos`) y desde los artículos a los días relacionados; navegación anterior/siguiente.
5. Páginas agregadas: Artículos (introducción, panoramas por parte, temas), Diagramas, Mapas, Símbolos y números, Palabras griegas (todas las de los días, con índice),
   Cristo en Apocalipsis (todas las secciones `cristo`), Línea de tiempo (dg-cronologia a pantalla completa). Índice por partes con progreso.
6. Búsqueda de texto completo (índice en JS, sin red), modo claro/oscuro, tamaño de letra, impresión limpia, teclado (←/→), responsive (móvil primero).
7. Notas del usuario y progreso: localStorage con try/catch + exportar/importar copia de seguridad (JSON).
8. Cero dependencias externas: fuentes, SVG y JS inline. Tamaño razonable (< ~25 MB; informá el tamaño).
9. Comillas: el texto bíblico («») se muestra distinto de las citas de autores (“ ”).

## Verificación
- `python3 apocalipsis/app/construir.py` genera el HTML sin errores y con el assert de versículos.
- Probalo con Playwright (ya instalado; `require('playwright')`/python `playwright`, chromium en /opt/pw-browsers): abrir un día, un artículo, un diagrama y la búsqueda;
  sin errores de consola; captura de pantalla en 390 px y 1280 px que revises vos (no las commitees).
- No modifiques `trabajo/`. No hagas commits. Respuesta final: tamaño del HTML, qué funciones quedaron, qué no pudiste hacer (una línea cada una).
