#!/bin/bash
# Recrea el entorno de trabajo del megaestudio en una sesión nueva (los libros, sus textos y las páginas web NO están en el repo).
# Uso: bash megaestudio/trabajo/scripts/preparar_entorno.sh      (tarda un rato: baja ~6 GB de libros y extrae su texto)
set -e
L=/home/user/lib; mkdir -p $L; cd $L
S="$(cd "$(dirname "$0")" && pwd)"
# 1) herramientas
command -v tesseract >/dev/null || { apt-get update -qq; apt-get install -y -qq tesseract-ocr tesseract-ocr-spa; }
python3 -c "import bs4, lxml" 2>/dev/null || pip install -q beautifulsoup4 lxml
# 2) libros (clon parcial = rápido; se bajan los archivos al hacer checkout)
for r in 3 4; do
  [ -d r$r ] || { git clone --depth 1 --filter=blob:none --sparse https://github.com/juanicarlisi/libros-referencia$r r$r; (cd r$r && git sparse-checkout disable && git checkout); }
done
[ -d bib ] || { git clone --depth 1 https://github.com/juanicarlisi/biblioteca-estudios-biblicos bib; (cd bib && git lfs pull); }
# 3) diccionarios y textos de referencia para verificar palabras hebreas y griegas
mkdir -p strong/wlc strong/gnt
for f in greek/strongs-greek-dictionary.js hebrew/strongs-hebrew-dictionary.js; do [ -f strong/$(basename $f) ] || curl -sS -L -o strong/$(basename $f) https://raw.githubusercontent.com/openscriptures/strongs/master/$f; done
for b in Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal; do [ -f strong/wlc/$b.xml ] || curl -sS -o strong/wlc/$b.xml https://raw.githubusercontent.com/openscriptures/morphhb/master/wlc/$b.xml; done
for n in 61-Mt 62-Mk 63-Lk 64-Jn 65-Ac 66-Ro 67-1Co 68-2Co 69-Ga 70-Eph 71-Php 72-Col 73-1Th 74-2Th 75-1Ti 76-2Ti 77-Tit 78-Phm 79-Heb 80-Jas 81-1Pe 82-2Pe 83-1Jn 84-2Jn 85-3Jn 86-Jud 87-Re; do [ -f strong/gnt/$n.txt ] || curl -sS -o strong/gnt/$n.txt https://raw.githubusercontent.com/morphgnt/sblgnt/master/$n-morphgnt.txt; done
# 4) texto de los libros por página y de las fuentes web
python3 $S/textos.py
python3 $S/rehacer_web.py
# 5) OCR (en segundo plano, retoma si se corta): cada libro escaneado de la lista
echo "Listo. Para los escaneos pendientes (texto escaso) correr, por ejemplo:  python3 $S/ocr.py <id> 3"
echo "Verificación de lo ya escrito:  python3 $S/verificar.py \$(seq 1 54)"
