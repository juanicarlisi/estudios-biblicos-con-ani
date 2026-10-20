#!/bin/bash
# Copia el trabajo del estudio del varón al repositorio (varon/trabajo/), sin los textos de los libros.
set -e
V=/home/user/trabajo/varon
R=/home/user/estudios-biblicos-con-ani/varon/trabajo
mkdir -p "$R"
for d in notas web plan textos dias insumos revision scripts; do
  if [ -d "$V/$d" ]; then rm -rf "$R/$d"; cp -r "$V/$d" "$R/$d"; fi
done
mkdir -p "$R/biblia"; [ -f "$V/biblia/rvr.json" ] && cp "$V/biblia/rvr.json" "$R/biblia/"
cp "$V/bloques/_fuentes.json" "$R/fuentes.json"
cp "$V/RUNS.md" "$R/"
# los scripts de los workflows van sin el nombre del modelo
sed -i -E "s/, model: '[a-z]+'//g" "$R"/scripts/*.js
