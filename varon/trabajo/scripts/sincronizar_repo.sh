#!/bin/bash
# Copia el trabajo del estudio del varón al repositorio (varon/trabajo/), sin los textos de los libros.
set -e
V=/home/user/trabajo/varon
R=/home/user/estudios-biblicos-con-ani/varon/trabajo
mkdir -p "$R"
for d in notas web plan textos revision scripts; do
  if [ -d "$V/$d" ]; then rm -rf "$R/$d"; cp -r "$V/$d" "$R/$d"; fi
done
# días definitivos (sin borradores ni pruebas) y los insumos se regeneran con insumos.py desde notas/ y plan/
rm -rf "$R/dias" "$R/insumos"; mkdir -p "$R/dias"; cp "$V"/dias/dia_*.json "$R/dias/"
rm -rf "$R/revision/verif"
mkdir -p "$R/biblia"; [ -f "$V/biblia/rvr.json" ] && cp "$V/biblia/rvr.json" "$R/biblia/"
cp "$V/bloques/_fuentes.json" "$R/fuentes.json"
cp "$V/RUNS.md" "$R/"
# los scripts de los workflows van sin el nombre del modelo
sed -i -E "s/, model: '[a-z]+'//g" "$R"/scripts/*.js
