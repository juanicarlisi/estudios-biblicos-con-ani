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


## El varón según Dios

Abrir `varon/el-varon-segun-dios.html` en el navegador: un solo archivo, con las tipografías incluidas, que funciona sin conexión.

- **El plan:** 512 días de 20 a 30 minutos, en 17 partes: la crisis del varón hoy, el diseño de Dios, el varón y Dios, el carácter,
  la pureza, el trabajo, el esposo, el padre, el líder y ministro, el siervo, hermanos y mentores, el joven, el adulto, el mayor,
  la sociedad, las pruebas y el fracaso, y varones de la Biblia y de la historia.
- **Cada día:** lectura, versículos clave, estudio con la fuente de cada afirmación, datos con año y fuente, modelo bíblico,
  palabras griegas y hebreas, preguntas difíciles, aplicación, preguntas para pensar y para charlar y oración. Los días sobre
  suicidio, adicciones, apuestas y violencia traen las líneas de ayuda oficiales de Argentina.
- **Herramientas:** resaltar con marcador, dibujar con lápiz, notas al margen, guardar el estudio entero con tus marcas,
  descargar un día (HTML o PDF), copia de seguridad, buscador y tres gráficos con datos del Banco Mundial.
- **De dónde sale:** 24.000 notas tomadas de los libros de la biblioteca y de REFERENCIA3 (solo autores protestantes confiables),
  269 datos y 190 artículos de sitios confiables verificados en su fuente. Cada afirmación lleva su fuente y página.
- **Cómo se verifica:** por programa (`varon/trabajo/scripts/verificar_dia.py`): cifras, frases entre «», atribuciones a autores,
  apoyo en las notas y existencia de cada versículo en la RVR1960. Reglas de trabajo y ahorro de tokens en `varon/CLAUDE.md`.
- **Texto bíblico:** Reina-Valera 1960 © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.
  Se transcribe un versículo clave por día hasta 500 versículos en total; el resto se lee en BibleGateway con el enlace de cada día.
