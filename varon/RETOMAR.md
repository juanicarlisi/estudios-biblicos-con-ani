# Varón: dónde quedamos (leer solo la sección pertinente: `grep -n "^## " varon/RETOMAR.md`)

## Estado (09-11-2026, tras REFERENCIA4)
- **REFERENCIA4 incorporada:** 2.414 notas nuevas (`trabajo/notas/r_*, q_*, z_*, y_*.json`; fuentes `R4001–R4281` en `trabajo/fuentes.json`) de libros A (primera pasada) y B, D y algunos C no católicos ni heterodoxos (segunda pasada, a pedido del fundador; el filtro doctrinal lo hacen los agentes al extraer y excluyó 1 libro de «liberación»), integradas en 454 de los 512 días (1.780 ítems de «Para profundizar», 1.289 conexiones, 221 pasos, 32 modelos, 13 datos, 11 interpretaciones). 512/512 días pasan `verificar_dia.py` (con `INSUMO_TOPE=400000` y las notas nuevas añadidas al insumo; ver `trabajo/scripts/ref4/`). Sin días nuevos; el tema «qué les dejás a tus hijos» va en los días 265, 274, 278, 289, 301 y 307. Excluidos por regla del fundador: católicos, adventistas, testigos, esoterismo, laicos y documentos legales (`trabajo/ref4/clasificacion.json`). HTML regenerado (17 MB).
- Cuidado al repetir el proceso: `armar_bloques.py` debe calcular el próximo id de fuente con `int(k[1:])` (un error con `k[2:]` pisó R4001–R4013; ya reparado).

## Estado anterior (31-10-2026)
- **Terminado:** 512 días definitivos en `trabajo/dias/`, verificados por programa (`verificar_dia.py`: 511 sin marcas, el 377 pasa 18 palabras del largo) y revisados en continuidad y doctrina (935 retoques).
- App y archivo final: `varon/app/` (plantilla + `construir.py`) → `varon/el-varon-segun-dios.html` (15 MB, sin conexión). Probada con Playwright (resaltar, nota, lápiz, guardar con marcas, descargar día, móvil).
- Datos: 24.000 notas, 269 datos y 190 artículos web verificados, líneas de ayuda oficiales (`trabajo/web/ayuda.json`), 3 gráficos del Banco Mundial (`trabajo/web/series.json`).
- Versículos RVR1960: un versículo clave por día hasta 500 en total (el resto, solo referencia y enlace).

## Si hay que tocar algo
1. Editar el día en `trabajo/dias/dia_NNN.json` (o regenerar su insumo con `insumos.py N` y reescribir con `wf_varon_escribir2.js`).
2. `verificar_dia.py --dias N` → si marca algo: `reparar_entrada.py --base dias` + `wf_varon_reparar.js` + `aplicar_reparaciones.py --base dias <run>`.
3. `rvr_desde_cache.py` → `construir.py` → `scripts/sincronizar_repo.sh` → commit y push.

## Ahorro de tokens (medido)
- Antes: escritor Opus + verificador Sonnet que releía todo ≈ 170k tokens por día. Ahora: Sonnet (esfuerzo medio) con insumo comprimido ≈ 90k en total por día (la mayor parte es el contexto fijo del agente, que se cachea); verificación y promoción por programa; reparar y recortar de a 6 días por agente ≈ 12k por día; continuidad con un agente por 10 días y sin verificador.
- Lección: el costo fijo de cada agente (~64k de contexto base) manda; agrupar varios días por agente lo reparte. En sesiones nuevas desde el repo, los agentes `redactor-dia` y `reparador-dia` (`.claude/agents/`, `omitClaudeMd`, solo Read) bajan ese contexto base.
