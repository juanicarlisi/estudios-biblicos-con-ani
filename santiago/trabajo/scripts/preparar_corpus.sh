#!/bin/sh
# Rearma, en una sesión nueva, lo que vive FUERA del repositorio: el texto de los libros y los bloques de lectura (TMP = /home/user/trabajo_santiago).
# El texto completo de los libros no se sube al repositorio (tienen derechos); se regenera con este script a partir de los PDF de los repositorios de libros.
#
# Requisitos: juanicarlisi/biblioteca-estudios-biblicos (Git LFS) y juanicarlisi/libros-referencia3 clonados en /home/user/ (add_repo + git clone),
#             poppler-utils (pdftotext), tesseract-ocr y tesseract-ocr-spa (apt install), Pillow y pdf2image/pymupdf según ocr_pdf.py.
# Al terminar: python3 scripts/pendientes.py --verificar   (compara los bloques con plan/bloques_manifest.json; tienen que coincidir)
set -e
B=/home/user/biblioteca-estudios-biblicos
M="$B/MATERIAL SOPORTE"
T=${TRABAJO_SANTIAGO:-/home/user/trabajo_santiago}
S=/home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts
mkdir -p "$T/corpus_biblio" "$T/segmentos/biblio" "$T/segmentos/ref3" "$T/partes"

echo "== 1. PDF de la biblioteca (LFS) → texto"
cd "$B"
# las comas separan los patrones: el archivo «Hebreos, Santiago, 1 y 2 Pedro, Judas.pdf» se nombra con comodines
git lfs pull --include="MATERIAL SOPORTE/59 - SANTIAGO/*,MATERIAL SOPORTE/58 - HEBREOS/Hebreos?*Santiago?*Judas.pdf,MATERIAL SOPORTE/58 - HEBREOS/Comentario Biblico Beacon Tomo 10*,MATERIAL SOPORTE/DICCIONARIOS/BMH_00*,MATERIAL SOPORTE/John MacArthur - Biblia de estudio.pdf"
conv() { [ -s "$T/corpus_biblio/$2" ] || pdftotext -enc UTF-8 "$1" "$T/corpus_biblio/$2"; }
conv "$M/59 - SANTIAGO/Santiago - John MacArthur.pdf"                              macarthur_santiago.txt
conv "$M/59 - SANTIAGO/Santiago y 1 2 3 Juan Hendriksen y Kistemaker.pdf"          kistemaker_santiago_juan.txt
conv "$M/59 - SANTIAGO/Santiago una fe en acción Elvis L Carballosa.pdf"           carballosa_b.txt
conv "$M/59 - SANTIAGO/Santiago_ Crece en sabiduria y fe - Elizabeth George.pdf"   george_santiago.txt
conv "$M/58 - HEBREOS/Hebreos, Santiago, 1 y 2 Pedro, Judas.pdf"                   cbmh_t23.txt
conv "$M/58 - HEBREOS/Comentario Biblico Beacon Tomo 10 Hebreos hasta Apocalipsis.pdf" beacon_t10.txt
conv "$M/John MacArthur - Biblia de estudio.pdf"                                   macarthur_biblia_estudio.txt
conv "$M/DICCIONARIOS/BMH_005 DICCIONARIO B-BLICO MUNDO HISPANO I.pdf"             dbmh_1.txt
conv "$M/DICCIONARIOS/BMH_006 DICCIONARIO B-BLICO MUNDO HISPANO II.pdf"            dbmh_2.txt

echo "== 2. Bloques de lectura de los comentarios"
python3 "$S/trocear_biblio.py"

echo "== 3. LIBROS-REFERENCIA3 → texto (categoría A), OCR de los 4 escaneados, índice, selección y bloques r1_/r2_"
(cd /home/user/libros-referencia3 && git lfs pull 2>/dev/null || true)
python3 "$S/extraer_ref3.py" 4
sh "$S/ocr_ref3.sh"
python3 "$S/indice_santiago.py"
python3 "$S/seleccion_ref3.py"

echo "== 4. Puentes entre bloques de lectura"
python3 "$S/puentes.py"

echo "== Listo. Verificá con: python3 $S/pendientes.py --verificar"
