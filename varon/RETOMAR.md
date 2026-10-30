# Varón: dónde quedamos (leer solo la sección pertinente: `grep -n "^## " varon/RETOMAR.md`)

## Estado (31-10-2026)
- Material: 490/490 bloques leídos (23.976 notas), 269 datos y 190 artículos web verificados, líneas de ayuda oficiales, app con marcador/lápiz/notas/gráficos.
- Plan cerrado: 512 días en 17 partes (`trabajo/plan/plan.json`, `dias_plan.json`; historial v1/v2/v3).
- Días: 225 borradores previos (partes A–F y parte de G) en reparación por programa; 287 en escritura con el flujo nuevo (Sonnet, sin verificador de IA).
- Faltan: reparar/promover, continuidad cada 6 días (`wf_varon_continuidad.js`), `rvr.py`, `construir.py`, HTML final.

## Cómo seguir (el estado exacto lo da `estado.py`)
1. `recoger_dias.py borradores` (corridas «Escribir2» de `trabajo/RUNS.md`) → `verificar_dia.py` → `reparar_entrada.py` + `wf_varon_reparar.js` → `aplicar_reparaciones.py <runs>` → `verificar_dia.py` → `promover.py`.
2. Lo que siga con flags después de dos reparaciones, se corrige a mano mirando solo `revision/verif/dia_NNN.json`.
3. Continuidad y doctrina por ventanas de 6 días; después `rvr.py`, `construir.py` y las pruebas con Playwright.

## Ahorro de tokens (medido)
- Antes: escritor Opus + verificador Sonnet que releía todo ≈ 170k tokens por día. Ahora: escritor Sonnet con insumo comprimido (≈13k tokens) y verificación por programa ≈ 70–90k; reparación solo de lo marcado ≈ 5–10k.
- Pendiente de probar en sesiones nuevas: agentes `.claude/agents/redactor-dia` y `reparador-dia` (omitClaudeMd), TTL de caché de 1 h en `.claude/settings.json`.
