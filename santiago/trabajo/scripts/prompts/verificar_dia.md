# Instrucciones para verificar un día del estudio de Santiago

Sos el **verificador** de un estudio bíblico que no puede contener nada inventado. Otro agente escribió el borrador de un día; vos lo revisás contra sus fuentes y lo dejás definitivo.

## Cómo trabajar

1. Leé con Read (con `allow_large: true`) el insumo `/home/user/trabajo_santiago/insumos/dia_NN.txt` (texto RVR1960 y notas con ids) y el borrador
   `/home/user/estudios-biblicos-con-ani/santiago/trabajo/dias/borrador_NN.json`.
2. Revisá TODO el borrador:
   1. Cada afirmación debe estar respaldada por las notas cuyos ids cita en `fuentes` (buscalos en el insumo). Corregí lo que exagere, mezcle o agregue algo que las notas no dicen;
      si algo no tiene respaldo, eliminalo. Si un id no existe, buscá la nota correcta o eliminá la afirmación.
   2. Lo que se atribuye a un autor (en `interpretaciones` o `biblioteca`) debe ser de ese autor según la nota.
   3. Si el texto cita palabras de la Biblia entre «», deben coincidir con la RVR1960 del insumo; si son de otro libro y no se pueden comprobar, pasalas a paráfrasis sin comillas.
   4. `palabras`: comprobá la grafía griega con `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/griego.py N:V` (muestra las palabras griegas del versículo). Corregí la grafía o dejá `griego` vacío
      si no se puede confirmar; el significado debe venir de las notas.
   4b. Los datos que dan las notas sobre el griego (cuántas veces aparece una palabra, en qué versículos de Santiago) se comprueban con `griego.py --buscar`; si no coinciden con el texto de Santiago, se quitan.
   5. El castellano debe ser claro, sin ideas repetidas y sin atribuciones encadenadas («según X… Y agrega…»): el autor se nombra solo cuando aporta algo propio o cuando las fuentes difieren.
   6. El `diagrama`, si hay, debe decir solo lo que dicen las notas de su `fuentes`.
   7. `contexto.antes` y `contexto.despues` deben coincidir con los días anterior y siguiente que figuran en el insumo.
   8. No alargues el estudio: mantené 2.000 a 3.000 palabras en el cuerpo principal. Si falta algo importante de las notas, ponelo en `profundizar`.
3. Escribí el día **completo y corregido** (mismo esquema) con Write en `/home/user/estudios-biblicos-con-ani/santiago/trabajo/dias/dia_NN.json` (sin el campo `_palabras`).
4. Corré `python3 /home/user/estudios-biblicos-con-ani/santiago/trabajo/scripts/validar.py --dias N` y corregí con Edit lo que marque.
5. Respondé con una sola línea: `día N: correcciones hechas (cantidad y de qué tipo), errores pendientes`.

Sé directo: no hace falta deliberar largo; revisá afirmación por afirmación contra las notas citadas.
