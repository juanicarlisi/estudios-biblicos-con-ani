# Varón: dónde quedamos (leer solo la sección pertinente: `grep -n "^## " varon/RETOMAR.md`)

## Estado (31-10-2026)
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
