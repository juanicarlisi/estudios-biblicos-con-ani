# Instrucciones para escribir un artículo del estudio de Apocalipsis (introducción, panorama o tema)

Estudio de Apocalipsis para un **matrimonio protestante** (castellano rioplatense neutro, claro y cálido). Regla de oro: **NO INVENTAR NADA**:
todo sale de las notas extraídas de los libros (ya leídas y resumidas), de los días ya escritos y del texto bíblico.

## Tu tarea
1. Leé `apocalipsis/trabajo/plan/articulos.json` (buscá tu artículo: título, alcance y largo) y `apocalipsis/trabajo/plan/esquema_articulo.md` (la forma exacta del JSON).
2. Leé tu material: `SCRATCH/insumos/art_<ID>.txt` (SCRATCH=/tmp/claude-0/-home-user/532e468b-ac94-5647-a250-c8778228a262/scratchpad); cada nota tiene su `[id]`.
   También el resumen de los días (títulos, rangos): `SCRATCH/insumos/_dias_resumen.txt`, para enlazar con `dias_relacionados` y no repetir lo que ya explican.
3. Escribí el artículo en `/home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/articulos/art_<ID>.json` (Write) y validalo con
   `python3 /home/user/estudios-biblicos-con-ani/apocalipsis/trabajo/scripts/validar_articulo.py <ID>`. Corregí hasta que no haya ERRORES.
4. Respuesta final: UNA línea: `<ID>: <título> · P palabras · F fuentes · avisos`.

## Cómo escribir
- Cada párrafo lleva `fuentes` (ids de las notas). Unís lo que coinciden varios autores en un solo párrafo con varias fuentes.
- **Posturas**: cuando difieren, decí quién sostiene qué (autor + escuela) sin tomar partido; marcá lo que todos comparten. Los autores carismáticos/proféticos (TTL, MiSion) se citan atribuidos y con fidelidad.
- Atribuí los datos dudosos («según McGee…»); no repitas erratas señaladas en las notas.
- Citas bíblicas: solo `versiculos` (hasta 6, cada uno con su `porque`; la app inserta el texto RVR1960) y frases cortas entre «» copiadas literales del texto bíblico de los insumos o de un día ya escrito.
- Extensión: la indicada en `largo` (palabras), sin contar `citas`. Si hay mucho material, elegí lo mejor; el resto queda en `notas_no_usadas` (ids).
- No toques otros archivos ni hagas commits. No publiques nada como artefacto.
