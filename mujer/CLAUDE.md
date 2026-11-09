# Estudio «La mujer según Dios»: reglas de trabajo (leer solo esto al arrancar)

Español rioplatense, dirigido a una lectora («vos», en femenino). No inventar nada: todo sale de las notas (biblioteca, REFERENCIA3 y
REFERENCIA4, Coalición por el Evangelio, Aviva Nuestros Corazones y las notas reutilizadas del estudio del varón; autores protestantes
confiables) con fuente y página; nunca copiar texto de los libros. RVR1960 no se sube: solo versículos clave (≤3 por día, ≤500 en total).
Datos web solo con fuente verificada. Líneas de ayuda solo las de `trabajo/web/ayuda.json`. Roles de varones y mujeres: cada autor con su postura, sin zanjar.

## Eficiencia (obligatorio)
- Leer de `RETOMAR.md` solo la sección pertinente; no leer completos `notas/`, `insumos/`, `dias/`, `bloques/`, `plan/grupos/`: buscar con Grep/Python y leer el tramo.
- Todo lo repetitivo lo hace un script; **verifica el programa** (`verificar_dia.py`), no un agente por día.
- Modelo y esfuerzo justos: extraer notas y agrupar = Haiku/medio (medido: igual o mejor que Sonnet y ~20 veces más barato); escribir días = Sonnet/bajo
  (medido: menos marcas que medio); reparar = Sonnet/medio; plan = Opus/medio.
- Workflows pocos y anchos; devolver una línea. Texto bíblico y APIs: por script y con caché.

## Flujo
`puntajes.py` → `bloques.py` / `web_a_bloques.py` / `bloques_ref4.py` → `wf_mujer_extraer.js` → `juntar_notas.py` + `depurar_notas.py` →
`grupos_entrada.py` + `wf_mujer_agrupar.js` → `planear_entrada.py` + `dividir_planear.py` + `wf_mujer_planear2.js` → `plan_armar.py` → `insumos.py` →
`wf_mujer_escribir.js` → `recoger_dias.py` → `verificar_dia.py` → `reparar_entrada.py` + `wf_mujer_reparar.js` + `aplicar_reparaciones.py` →
`recortar_entrada.py` + `wf_mujer_recortar.js` + `aplicar_recorte.py` → `promover.py` → continuidad (`continuidad_entrada.py` + `wf_mujer_continuidad.js` +
`aplicar_continuidad.py`) → `app/construir.py`. Ojo: los ids de fuentes válidos son `b_ o_ w_ r_ v_` + `#n` y `W…` (si se agrega un prefijo, actualizar `promover.py` y `verificar_dia.py`).
