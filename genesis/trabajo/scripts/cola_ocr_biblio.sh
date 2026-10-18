#!/bin/sh
B="/home/user/biblioteca-estudios-biblicos/MATERIAL SOPORTE"
O=/home/user/trabajo/corpus_biblio/todo
for rel in "45 - ROMANOS/Romanos 1 a 8 - John MacArthur.pdf" "45 - ROMANOS/Romanos 9-16 - John MacArthur.pdf" "42 - LUCAS/4. Biblia Matthew Henry - Mateo a Romanos.pdf" "66 - APOCALIPSIS/5. Biblia Matthew Henry - Corintios a Apocalipsis.pdf" "65 - JUDAS/22 MacArthur, John - Comentario MacArthur del NT - Judas.pdf" "42 - LUCAS/Comentario Bíblico Moody - SAN LUCAS.pdf" "66 - APOCALIPSIS/Apocalipsis - Evis Carballosa.pdf"; do
  echo "== $rel"
  python3 /home/user/trabajo/scripts/ocr_pdf.py "$B/$rel" "$O/$rel.ocr.txt" 3
done
echo COLA_FIN
