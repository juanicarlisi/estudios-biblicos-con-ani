# Estudio «El varón según Dios»: reglas de trabajo (leer solo esto al arrancar)

Español rioplatense. No inventar nada: todo sale de las notas (biblioteca y REFERENCIA3, autores protestantes confiables) con fuente y
página; nunca copiar texto de los libros. RVR1960 no se sube: solo versículos clave (≤3 por día, ≤500 en total). Datos web solo con
fuente verificada. Líneas de ayuda solo las de `trabajo/web/ayuda.json`.

## Eficiencia (obligatorio)
- Arrancar con la línea de `estado.py` (la imprime el hook) y leer de `RETOMAR.md` solo la sección pertinente (`grep -n "^## "`).
- No leer completos `notas/`, `insumos/`, `dias/`, `bloques/`, `plan/grupos/`, `web/datos.json`: buscar con Grep/Python/`jq` y leer el tramo (`offset`/`limit`).
- Todo lo repetitivo lo hace un script; la IA solo escribe/corrige. **Verifica el programa** (`verificar_dia.py`), no un agente por día.
- Un agente por pieza, con modelo y esfuerzo justos: escribir un día = `redactor-dia` (sonnet, medio); corregir lo marcado = `reparador-dia`
  (sonnet, bajo); lo mecánico/estructurado = haiku o script. Agentes: leen UN archivo, devuelven por esquema, sin Bash ni relecturas.
- Workflows: pocos y anchos (cada notificación cuesta contexto); devolver una línea (`N/M ok · faltan …`), nunca listas.
- Texto bíblico, capítulos y datos de APIs: bajarlos por script y cachear (`biblia/cap/`, `web/series.json`); nunca pedirle a un agente que los recuerde.
- Al cerrar: actualizar `RETOMAR.md` (≤10 líneas de estado), `scripts/sincronizar_repo.sh`, commit y push a la rama de trabajo.

## Flujo de los días
`insumos.py` (≈13k tokens por día) → `wf_varon_escribir2.js` → `recoger_dias.py borradores` → `verificar_dia.py` → `reparar_entrada.py` +
`wf_varon_reparar.js` + `aplicar_reparaciones.py` (solo lo marcado) → `verificar_dia.py` → `promover.py` → `rvr.py` → continuidad
(`continuidad_entrada.py` + `wf_varon_continuidad.js` + `aplicar_continuidad.py`) → `construir.py`.
