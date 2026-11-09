# Esquema de un artículo (JSON) — `pedro-judas/trabajo/articulos/art_<ID>.json`

```json
{
  "id": "T5", "titulo": "…", "bajada": "Una oración que dice de qué trata.",
  "entrada": {"texto": "Párrafo de apertura.", "fuentes": ["id"]},
  "versiculos": [{"ref": "1P 3:18", "porque": "…"}],
  "apartados": [{"titulo": "…", "parrafos": [{"texto": "…", "fuentes": ["id", "id"]}]}],
  "palabras": [{"ref": "1P 3:19", "griego": "φυλακῇ", "translit": "fylakḗ", "significado": "…", "fuentes": ["id"]}],
  "interpretaciones": [{"tema": "…", "posturas": [{"postura": "…", "quien": "Autor (tradición o escuela)", "fuentes": ["id"]}], "nota": "…"}],
  "citas": [{"texto": "frase textual breve", "autor": "…", "obra": "…", "pagina": "…"}],
  "conexiones": [{"ref": "Gn 6:1-4", "nota": "…", "fuentes": ["id"]}],
  "para_vivir": [{"texto": "…", "fuentes": ["id"]}],
  "para_conversar": ["…", "…", "…"],
  "dias_relacionados": [9, 10],
  "visuales": ["dg-espiritus"],
  "refs_libros": ["1P 3:18-22", "1P 4:6"],
  "notas_no_usadas": ["id"]
}
```
Reglas: `apartados` de 3 a 7 según el largo; todo `parrafos[].texto` con `fuentes`; `versiculos` (máx. 6) y `refs_libros` con sigla de
libro (1P, 2P, 1J, 2J, 3J, Jd); `dias_relacionados` son números de día del plan (`plan/plan.json`); `visuales` ids de
`plan/visuales.json` (máx. 3); `para_conversar` 3 preguntas; comillas «» solo para texto bíblico literal.
