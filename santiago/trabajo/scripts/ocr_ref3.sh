#!/bin/sh
R=/home/user/libros-referencia3
O=/home/user/trabajo_santiago/corpus_ref3
S=/home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/ocr_pdf.py
for rel in "Relacion con Dios/La voluntad de Dios - John MacArthur.pdf" "Finanzas y Mayordomia/a quien pertenece el dinero - macarthur.pdf" "Crecimiento y Vida Cristiana/Quebrantamiento_Nancy_Leigh_Demoss.pdf" "Discipulado/Difícil de creer - John MacArthur.pdf"; do
  echo "== $rel"
  python3 "$S" "$R/$rel" "$O/$rel.txt" 3
done
echo COLA_FIN
