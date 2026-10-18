#!/bin/sh
B="/home/user/biblioteca-estudios-biblicos/MATERIAL SOPORTE"
O=/home/user/trabajo/corpus_biblio/todo
for rel in "65 - JUDAS/22 MacArthur, John - Comentario MacArthur del NT - Judas.pdf" "42 - LUCAS/Comentario Bíblico Moody - SAN LUCAS.pdf" "66 - APOCALIPSIS/Apocalipsis - Evis Carballosa.pdf"; do
  echo "== $rel"
  python3 /home/user/trabajo/scripts/ocr_pdf.py "$B/$rel" "$O/$rel.ocr.txt" 2
done
echo COLA_FIN
