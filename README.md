# Estudios bíblicos

Estudios para acompañar la lectura de la Biblia en pareja: unos 20 versículos por día, media hora de lectura y estudio.

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
