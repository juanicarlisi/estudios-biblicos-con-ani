# Estudios bíblicos

Estudios para acompañar la lectura de la Biblia en pareja: de 20 a 30 minutos de lectura y estudio por día (Génesis, con unos 20 versículos diarios; Santiago, sin tope de versículos: cada día cubre lo que el material pida).

## Génesis en pareja

Abrir `genesis/estudio-genesis.html` en el navegador: es un solo archivo, con las tipografías incluidas, y funciona sin conexión
(solo el botón «Leer el pasaje» abre BibleGateway).

- **El plan:** todo Génesis en 69 días, ordenado según las diez «generaciones» (*toledot*) del propio libro y agrupado en
  cuatro partes: los orígenes (1–11), Abraham (11:27–25:18), Isaac y Jacob (25:19–36) y José (37–50).
- **Cada día:** qué pasó antes, qué pasa y qué viene; el versículo clave; el pasaje versículo por versículo; palabras
  hebreas; Cristo en el pasaje; las preguntas difíciles con las posturas de cada autor; aportes de los libros de referencia;
  conexiones con el resto de la Biblia; aplicación, preguntas para conversar y una oración. Lo optativo queda en
  «Para profundizar».
- **Además:** una introducción en cinco capítulos, un panorama antes de cada parte, nueve artículos de temas, mapas con los
  viajes, una línea de tiempo, árboles genealógicos, todas las palabras hebreas, Cristo en Génesis y un buscador.
- **Progreso y notas:** se guardan en el navegador de la compu. Desde el inicio se baja una copia (y se vuelve a cargar),
  para no perderlas si se limpian los datos del navegador o para pasarlas a otra compu.

### De dónde sale

Nada está inventado: cada afirmación lleva etiquetas con su fuente y la página.

- **Comentarios de Génesis:** Meredith G. Kline (*Nuevo Comentario Bíblico*), *Comentario Bíblico Beacon*,
  *Comentario Bíblico Mundo Hispano*, Alfred Edersheim, *Biblia de Estudio MacArthur* y el *Diccionario Bíblico Mundo Hispano*.
- **Libros de referencia:** solo de autores protestantes confiables (ver `genesis/trabajo/clasificacion/`). Las obras no
  confiables se eliminaron de los repositorios (registro en `genesis/trabajo/borrado/`).
- **Texto bíblico:** Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas
  Unidas, 1988. Se citan solo los versículos clave; el pasaje completo se lee en la Biblia o en BibleGateway.
- **Hebreo:** OpenScriptures Hebrew Bible (Westminster Leningrad Codex) con los números de Strong.
- **Mapas:** Natural Earth (dominio público) y OpenBible.info, *Bible Geocoding Data* (CC BY 4.0).

### Cómo se armó

1. Se leyeron completos los comentarios de Génesis y se tomó una nota por aporte, con su página.
2. Se barrieron todos los libros de referencia buscando lo que trata Génesis (unas 8.000 notas).
3. Cada día, la introducción, los panoramas y los temas se escribieron a partir de sus notas, uniendo lo repetido.
4. Un segundo control cotejó cada afirmación con sus notas, las citas con la RVR1960 y el hebreo con el texto masorético.

`genesis/trabajo/` guarda todo el trabajo intermedio: notas extraídas, clasificación de autores, plan, días y artículos en
JSON, y los scripts. `genesis/app/` tiene la plantilla, las tipografías y el armador (`python3 genesis/app/construir.py`;
con `--artefacto` arma la versión para publicar en claude.ai).

## Santiago en pareja (en construcción)

El estudio de la carta de Santiago sigue la misma mecánica que Génesis, pero **sin tope de versículos por día**: cada día se lee en 20 a 30 minutos y
puede ser de un solo versículo, o varios días pueden recorrer el mismo pasaje con enfoques distintos. La cantidad de días sale de cuánto material hay.
Se arma con todo lo que la biblioteca tiene sobre Santiago (MacArthur, Kistemaker, Carballosa, Elizabeth George, Mundo Hispano, Beacon, Biblia de Estudio MacArthur,
Diccionario Bíblico Mundo Hispano) y con los libros de referencia de autores protestantes confiables.

- **Estado y cómo retomar:** `santiago/trabajo/ESTADO.md`. La extracción de notas está en curso (`python3 santiago/trabajo/scripts/pendientes.py` muestra qué falta).
- **Novedades de UX previstas:** barra de avance global, por parte y por día; cuadrícula de los 108 versículos; el pasaje (y el griego, si se quiere) en la misma página; gráficos de palabras clave;
  diagramas, mapas y línea de tiempo dentro de cada día; enlaces a temas y anexos.
- **Texto bíblico:** Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988. Texto griego: SBLGNT (CC BY 4.0) con el análisis de MorphGNT.
