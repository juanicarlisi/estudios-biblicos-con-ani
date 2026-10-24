# Santiago en pareja — estado del trabajo

**Pausado el 24-10-2026 a pedido del fundador** («dejemos acá y luego continuamos»). Este archivo dice qué está hecho, qué falta y cómo retomar sin perder nada.
Para ver el estado exacto de la extracción en cualquier momento: `python3 santiago/trabajo/scripts/pendientes.py`.

## Qué se pidió

Armar el estudio de la carta de Santiago con la misma mecánica que Génesis, **sin el tope de 20 versículos por día**: cada día se lee en 20 a 30 minutos y cubre lo que
el material pida (un solo versículo es válido, y varios días pueden recorrer el mismo versículo). La cantidad de días sale de cuánto material hay y se considera necesario.
Se arma con **todo** el material disponible (comentarios de la biblioteca y LIBROS-REFERENCIA3, solo autores protestantes confiables) y con mejoras de UX: barra de progreso,
mapas, diagramas y gráficos en la misma página, enlaces a anexos.

## Qué está hecho

| Parte | Estado |
|---|---|
| Scripts (`scripts/`), prompts de los agentes (`scripts/prompts/`), esquema del día (`plan/esquema_dia.md`), lista de 26 artículos (`plan/articulos.json`), partes (`plan/partes.json`) | listos |
| Texto de Santiago en la Reina-Valera 1960 (`biblia/rvr1960_santiago.json`, 108 versículos, cotejado con una segunda fuente) y griego SBLGNT con MorphGNT (`griego/`) | listos |
| App (`../app/`: `plantilla.html`, `motor.js`, `construir.py`, tipografías incrustadas) con la UX nueva: barra de avance global y por parte, seguimiento de pasos del día con tiempo restante, cuadrícula de los 108 versículos, pasaje RVR (y griego opcional) en la página, gráficos de palabras clave por capítulo, diagramas, tarjetas de anexos, minimapa y línea de tiempo por día, imprimir, «Terminar el día y seguir», buscador, modo oscuro | listo y probado con datos provisionales |
| Extracción de notas (comentarios de la biblioteca y REFERENCIA3) | **en curso**, ver abajo |
| Auditoría de fidelidad de las notas (`scripts/auditar_fidelidad.py`) | lista; con 992 notas dio cobertura mediana 0,89 contra la página citada, ninguna bajo 0,35 y solo 3 con números que la página no trae (revisadas a mano: 2 eran números escritos con letras y 1 era una errata del libro, ya anotada) |
| Plan de días (`plan/plan.json`) | **provisional**: 32 pericopas solo para probar los insumos; se reemplaza (ver «Falta», punto 3) |

### La extracción

- 162 bloques de lectura: 107 de los comentarios de la biblioteca (MacArthur, Kistemaker, Carballosa, Elizabeth George, Mundo Hispano, Beacon, Biblia de Estudio MacArthur,
  Diccionario Bíblico Mundo Hispano), 40 de REFERENCIA3 (`r1_` = tramos completos con mucha señal; `r2_` = ventanas alrededor de las citas) y 15 «puentes» (ver punto 2 de «Falta»).
  La lista en orden está en `plan/cola_extraccion.txt`; `plan/bloques_manifest.json` guarda el sha1 de cada bloque.
- MacArthur (27 bloques) está completo. Faltan Carballosa, Elizabeth George, Mundo Hispano (casi todo), Beacon, Biblia de Estudio MacArthur, Diccionario, el resto de REFERENCIA3 y los puentes
  (`python3 scripts/pendientes.py` los lista).
- Método: un agente por bloque (máximo 20 a la vez), con las instrucciones de `scripts/prompts/extraer_biblio.md` (comentarios) o `barrer_ref3.md` (REFERENCIA3); cada uno escribe sus notas en
  tandas, las une con `scripts/unir_partes.py` y las valida con `scripts/validar_extraccion.py`. `pendientes.py --prompt ID` imprime el prompt exacto de un bloque.
- Cada nota lleva su página; los ids de nota son `bloque#n` (por ejemplo `macarthur_05#12`) y **son estables mientras no se vuelva a extraer ese bloque**.

## Qué falta (en orden)

1. **Terminar la extracción** (`pendientes.py`). Un agente por bloque, de a 20.
2. **Pasada de «puentes»**: los bloques son rangos de páginas contiguos y los agentes omitieron lo que quedaba cortado a mitad de oración en el límite. `scripts/puentes.py` armó 15 bloques puente
   (última página de un bloque + primera del siguiente); se extraen con `scripts/prompts/extraer_puentes.md`.
3. **Plan de días según el material**: correr `scripts/plan_densidad.py` y `scripts/plan_auto.py --T 4200` con la extracción completa; revisar a mano (títulos, fusiones, versículos de varios días con
   enfoques distintos) y completar `DIAS` en `scripts/plan.py`; correr `plan.py` (reemplaza el `plan/plan.json` provisional). El valor de T (peso de un día) se calibra con el día de prueba (ver más abajo).
4. **Insumos** (`scripts/insumos_dias.py`) y, si algún día queda demasiado grande, curaduría (`curaduria/dia_NN.json`). **Clasificación de las notas generales**: `scripts/insumos_libro.py` (paso 1),
   agentes con `prompts/clasificar_libro.md`, y `insumos_libro.py --secciones` (paso 2).
5. **Escribir los días** (agente con `prompts/escribir_dia.md` → `dias/borrador_NN.json`; otro agente verificador con `prompts/verificar_dia.md` → `dias/dia_NN.json`; `scripts/validar.py`) y **los 26 artículos**
   (`prompts/escribir_articulo.md`). Después, revisión de continuidad (`armar_continuidad.py`, agentes, `aplicar_continuidad.py`) y ajuste de minutos.
6. **Mapas y línea de tiempo**: escribir `mapas/lugares_santiago.json` (lugares con coordenadas y vistas, cada uno con las notas que lo respaldan; las notas que más lugares nombran: Jerusalén, la dispersión, Carmelo, Éfeso, Egipto,
   Samaria, Palestina, Jericó, Sarepta, Alejandría, Galilea, Babilonia, Antioquía, Chipre), correr `scripts/datos_mapas.py`; `plan/linea.json` y `plan/linea_dia.json` (con fechas y fuentes); `scripts/textos.py`.
7. **Armar y probar la app**: `python3 santiago/app/construir.py` (opcional `--artefacto`); pruebas con `node santiago/app/qa/probar_app.js archivo.html carpeta_capturas hash1,hash2 [--movil]`
   (Playwright ya instalado); revisar en escritorio, teléfono y modo oscuro.
8. **Cierre**: actualizar `README.md` de la raíz, correr `validar.py` completo, commit y push.

## El día de prueba (calibración)

Con el plan provisional se lanzó un agente escritor para el día 2 (Santiago 1:2–4, 129 notas de insumo). Su borrador, si terminó, está en `dias/borrador_02.json`; sirve para ver cuánto del material cabe en 20 a 30 minutos y
ajustar T en `plan_auto.py`. No es un día definitivo. Antes de armar el plan real, borrar `dias/borrador_02.json`.

## Cómo retomar en una sesión nueva (el texto de los libros vive fuera del repositorio)

El texto completo de los libros tiene derechos y **no se sube**; se regenera. Pasos:

1. Adjuntar a la sesión los repositorios `juanicarlisi/biblioteca-estudios-biblicos` y `juanicarlisi/libros-referencia3` y clonarlos en `/home/user/` (la biblioteca usa Git LFS).
2. `apt install` de `tesseract-ocr tesseract-ocr-spa poppler-utils` si faltan (el OCR de 4 libros escaneados de REFERENCIA3 lo necesita).
3. `sh santiago/trabajo/scripts/preparar_corpus.sh` (convierte los PDF, parte los comentarios en bloques, selecciona lo de REFERENCIA3 y arma los puentes).
4. `python3 santiago/trabajo/scripts/pendientes.py --verificar`: **tiene que decir que los 162 bloques coinciden con el manifiesto**. Si alguno difiere, no lanzar agentes sobre él.
5. `python3 santiago/trabajo/scripts/pendientes.py` y seguir lanzando agentes (de a 20) con los prompts de `pendientes.py --prompt ID`.

Lo regenerable que está en `/home/user/trabajo_santiago/` (no versionado): `corpus_biblio/`, `corpus_ref3/`, `segmentos/`, `indice/`, `insumos/`, `partes/` (tandas de notas; ya unidas en `extracciones*/`), `capturas/`.

## Decisiones y avisos para el fundador

- **Cobertura:** se leyó todo lo que la biblioteca tiene sobre Santiago. De REFERENCIA3 entran solo los libros de categoría A (autor protestante confiable). Treinta libros escaneados no tienen texto digital:
  se pasaron por OCR cuatro cuyos temas tocan Santiago (la voluntad de Dios, el dinero, el quebrantamiento y la fe); el resto no se leyó.
- **Excluido:** el archivo «Biblia Matthew Henry – Corintios a Apocalipsis» no es de Matthew Henry (es un escaneo sin portada de otro comentario, autor no identificable): no se usó. Si el fundador sabe de quién es, se puede reconsiderar.
- **Texto bíblico:** se incluye completo el texto de Santiago en la RVR1960 (108 versículos, dentro del tope de 500 versículos de cita de la Sociedad Bíblica) con la leyenda de derechos; el resto de la Biblia se cita solo por referencia.
  El repositorio es público: conviene confirmar que esto está bien.
- **Diferencia con Génesis:** el README de la raíz dice «unos 20 versículos por día» (eso es de Génesis); Santiago no tiene tope de versículos.
