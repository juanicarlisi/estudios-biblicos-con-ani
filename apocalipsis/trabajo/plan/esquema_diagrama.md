# Esquema de un diagrama (JSON) — `apocalipsis/trabajo/diagramas/<id>.json`

Todo diagrama sale de las notas extraídas (`apocalipsis/trabajo/extracciones/*.json`) y de los días ya escritos (`apocalipsis/trabajo/dias/dia_NN.json`).
Nada inventado: cada fila/tarjeta/segmento lleva `fuentes` (ids de notas con la forma `archivo#n`, p. ej. `macarthur_04_a#12`; el número es la posición de la
nota dentro del archivo, empezando en 1). Cuando los autores difieren, se muestra cada postura atribuida (columna o carril propio); no se toma partido.

Hay tres tipos; cada uno se dibuja en la app sin código extra:

**tabla** — `{"id","titulo","bajada","tipo":"tabla","columnas":["…"],"filas":[{"celdas":["…","…"],"ref":"2:1-7","fuentes":["id"]}],"nota":"…","dias":[8,9]}`
  (`celdas` tiene tantas entradas como `columnas`; `ref` opcional; texto breve, máx. ~30 palabras por celda).

**lineas** — líneas de tiempo comparadas: `{"id","titulo","bajada","tipo":"lineas","eje":["etiqueta inicial","…","etiqueta final"],"carriles":[{"nombre":"…","quien":"autores que la sostienen","segmentos":[{"etiqueta":"…","desde":0,"hasta":30,"clase":"a|b|c|d|e"}],"marcas":[{"en":30,"etiqueta":"…"}],"fuentes":["id"]}],"nota":"…","dias":[…]}`
  (`desde`/`hasta`/`en` van de 0 a 100 sobre el eje; los segmentos de un carril no se pisan; `clase` solo da el color: misma clase = mismo tipo de período entre carriles).

**tarjetas** — `{"id","titulo","bajada","tipo":"tarjetas","tarjetas":[{"titulo":"…","texto":"…","ref":"1:13","fuentes":["id"]}],"nota":"…","dias":[…]}`

`dias`: números de día del plan (`plan/plan.json`) donde el tema se explica. Las referencias bíblicas van como `C:V` o `C:V-V`.
