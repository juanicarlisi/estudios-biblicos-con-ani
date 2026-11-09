# Instrucciones para escribir un artículo del estudio de 1 Pedro a Judas (introducción, panorama o tema)

Estudio de 1 Pedro, 2 Pedro, 1, 2 y 3 Juan y Judas para un **matrimonio protestante** (castellano rioplatense neutro, claro y cálido).
Regla de oro: **NO INVENTAR NADA**: todo sale de las notas extraídas de los libros (ya leídas y resumidas), de los días ya escritos y del
texto bíblico. Nunca copies frases largas de los autores: se redacta con palabras propias y se atribuye.

## Tu tarea
1. Leé `pedro-judas/trabajo/plan/articulos.json` (buscá tu artículo: título, libros, alcance y largo) y `pedro-judas/trabajo/plan/esquema_articulo.md` (la forma exacta del JSON).
2. Leé tu material: `SCRATCH/pj_insumos/art_<ID>.txt` (SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad); cada nota tiene su `[id]`.
   También el resumen de los días (títulos, rangos): `SCRATCH/pj_insumos/_dias_resumen.txt`, para enlazar con `dias_relacionados` y no repetir lo que ya explican.
3. Escribí el artículo en `/home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/articulos/art_<ID>.json` (Write) y validalo con
   `python3 /home/user/estudios-biblicos-con-ani/pedro-judas/trabajo/scripts/validar_articulo.py <ID>`. Corregí hasta que no haya ERRORES.
4. Respuesta final: UNA línea: `<ID>: <título> · P palabras · F fuentes · avisos`.

## Cómo escribir
- Cada párrafo lleva `fuentes` (ids de las notas). Unís lo que coinciden varios autores en un solo párrafo con varias fuentes.
- **Posturas**: cuando difieren, decí quién sostiene qué (autor + tradición o escuela) sin tomar partido; marcá lo que todos comparten.
  Las escuelas escatológicas (pre/a/posmilenial; pre/mid/postribulacional) y las lecturas reformada, wesleyana y dispensacional se presentan sin tomar partido.
- Atribuí los datos dudosos («según McGee…»); no repitas erratas señaladas en las notas.
- Citas bíblicas: solo `versiculos` (hasta 6, cada uno con su `porque` y la referencia con sigla: «1P 1:3»; la app inserta el texto
  RVR1960) y frases cortas entre «» copiadas literales del texto bíblico de los insumos o de un día ya escrito. Las comillas «» son solo para texto bíblico literal.
- Extensión: la indicada en `largo` (palabras), sin contar `citas`. Si hay mucho material, elegí lo mejor; el resto queda en `notas_no_usadas` (ids).
- No toques otros archivos ni hagas commits. No publiques nada como artefacto.

## Ahorro de contexto
- Leé el insumo por tramos (offset/limit) y descartá rápido lo que no es de tu tema; si el insumo trae poco de lo que pide `alcance`,
  completá con Grep sobre `pedro-judas/trabajo/extracciones/*.json` (tipos de nota pertinentes) en vez de leer más insumo.
- Un solo ciclo de escritura + validación; no releas el JSON entero después de validar.
