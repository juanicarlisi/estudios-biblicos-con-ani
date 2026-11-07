#!/bin/bash
# Copia el trabajo del estudio de la mujer al repositorio (mujer/trabajo/), sin los textos de libros ni de la web.
set -e
V=/home/user/trabajo/mujer
R=/home/user/estudios-biblicos-con-ani/mujer/trabajo
mkdir -p "$R"
for d in notas web plan textos revision scripts; do
  if [ -d "$V/$d" ]; then rm -rf "$R/$d"; cp -r "$V/$d" "$R/$d"; fi
done
# las notas reutilizadas del varón se regeneran con reusar_varon.py
rm -f "$R"/notas/v_*.json
rm -rf "$R/dias" "$R/insumos"
if ls "$V"/dias/dia_*.json >/dev/null 2>&1; then mkdir -p "$R/dias"; cp "$V"/dias/dia_*.json "$R/dias/"; fi
rm -rf "$R/revision/verif" "$R/scripts/__pycache__"
cp "$V/bloques/_fuentes.json" "$R/fuentes.json"
cp "$V/RUNS.md" "$V/plan_extraer.json" "$V/plan_extraer_web.json" "$R/" 2>/dev/null || true
sed -i -E "s/, model: '[a-z]+'//g" "$R"/scripts/*.js
