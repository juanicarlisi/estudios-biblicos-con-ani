# Corridas del estudio «La mujer según Dios» (para retomar)
- 31-10-2026: arranque. Reutiliza corpus (corpus_ref3, corpus_biblio, OCR), duplicados y clasificación del varón; extracción con lente de mujer.
- Puntajes: 127.788 páginas puntuadas con lente de mujer (scripts/puntajes.py). Bloques: 171 b_ + 17 o_ (umbrales Mujer≥2, núcleo≥6, biografías≥12, resto≥22). Plan de lotes de extracción en plan_extraer.json (8 lotes).
- Extracción piloto esfuerzo bajo (descartado: menos notas): wf_687f052c-02c · piloto esfuerzo medio (b_001, b_150; vale): wf_581580c8-386
- Web (12 temas): wf_8e0d461e-01c (script scripts/wf_mujer_investigar_web.js; recolectar con web_datos.py wf_8e0d461e-01c)
- Extracción (186 bloques restantes, Sonnet/medio, 8 corridas; lotes en plan_extraer.json): wf_ae5648f7-b47 wf_679bf0a2-48e wf_84c68070-878 wf_c6005147-0ba wf_a46e9fa4-c84 wf_174d8bb3-301 wf_a5d945ef-8da wf_13b0b30f-f70
- Notas reutilizadas del varón (8.837, secciones universales, sin marcadores masculinos): scripts/reusar_varon.py → notas/v_*.json, fuentes «vR…» sumadas a bloques/_fuentes.json.
- Web ronda 2 (4 temas de artículos nuevos + violencia_abuso, salud_mental, adicciones_pantallas; abre cada página): wf_437678e1-1e9 (lanzada 31-10-2026; sumar con web_datos.py wf_8e0d461e-01c wf_437678e1-1e9)
- Web de texto completo (script, sin IA): Coalición por el Evangelio (8.388 páginas, fuentes_web/cpe) + Aviva Nuestros Corazones (567 transcripciones, fuentes_web/aviva) → bloques w_NNN con scripts/web_a_bloques.py --min 10 (artículos ≥10, podcasts ≥6 puntos/1000 car.; mujeres y para-ser-sinceras siempre). Extraer con scripts/wf_mujer_extraer.js
- Extracción de los 65 bloques web w_ (Sonnet/medio, 5 corridas, lotes en plan_extraer_web.json): wf_f34b198b-496 wf_f5b70d3f-e76 wf_5971b232-701 wf_a834a886-47d wf_a1feb3db-89f
- (CANCELADAS, piloto; las tandas cambiaron de composición) Agrupar de 55 tandas: wf_0b7e9940-e69 wf_7bd1c531-d23 wf_083c2974-caa wf_b4d92573-3af wf_bcf552da-54d. Pendiente: libros nuevos de libros-referencia3 (vigilante /tmp/vigilar_ref3.sh) → tandas extra antes de planear.
- REFERENCIA4 (LIBROS-REFERENCIA4, 485 libros no repetidos por nombre; 83 repetidos por contenido; 167 de autores A → 145 bloques r_NNN.txt de 120k car.; scripts extraer_ref4, puntajes_ref4, duplicados_ref4, candidatos_ref4, wf_clasificar_ref4, clasif_ref4, bloques_ref4). Clasificación: wf_d58e9493-d32 wf_145fa776-515.
- Piloto Sonnet vs Haiku sobre r_010/r_080/r_120 (de una versión anterior de los bloques; piloto, no recolectar): wf_108eea80-02b (Sonnet, 79 notas) · wf_07797fa4-b22 (Haiku, 124 notas, citas 60/61 verificadas) → se usa Haiku/medio para REFERENCIA4.
- Extracción REFERENCIA4 (145 bloques r_, Haiku/medio, 5 corridas; lotes en plan_extraer_ref4.json): wf_685486a5-c5a wf_5a514498-24a wf_346a6301-92d wf_412e4b75-e94 wf_513495a2-823

- Piloto de agrupado Sonnet vs Haiku (in_G_03, in_P_02, in_Q_02): wf_422afe0b-ac5 (Sonnet, piloto: olvidó/inventó ids) · wf_c984a5d4-35f (Haiku: 0 ids perdidos, grupos más finos) → Haiku/medio para agrupar.
- Agrupar (79 tandas con todo el material; Haiku/medio; 76 en 5 corridas más las 3 de la prueba Haiku; lotes en plan_agrupar.json): wf_c984a5d4-35f wf_f93f1612-af9 wf_0c042338-d51 wf_69f2a7dc-738 wf_36f0bd55-022 wf_016d28dc-ba1
