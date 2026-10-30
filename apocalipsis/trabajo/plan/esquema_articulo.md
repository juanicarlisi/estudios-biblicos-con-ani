# Esquema de un artículo (JSON)

```json
{
  "id": "T11", "titulo": "…", "bajada": "Una oración que dice de qué trata.",
  "entrada": {"texto": "Párrafo de apertura.", "fuentes": ["id"]},
  "versiculos": [{"ref": "20:4", "porque": "…"}],
  "apartados": [{"titulo": "…", "parrafos": [{"texto": "…", "fuentes": ["id", "id"]}]}],
  "palabras": [{"ref": "20:4", "griego": "ἔζησαν", "translit": "ézesan", "significado": "…", "fuentes": ["id"]}],
  "interpretaciones": [{"tema": "…", "posturas": [{"postura": "…", "quien": "Autor (escuela)", "fuentes": ["id"]}], "nota": "…"}],
  "citas": [{"texto": "frase textual breve", "autor": "…", "obra": "…", "pagina": "…"}],
  "conexiones": [{"ref": "Dn 7:13", "nota": "…", "fuentes": ["id"]}],
  "para_vivir": [{"texto": "…", "fuentes": ["id"]}],
  "para_conversar": ["…", "…", "…"],
  "dias_relacionados": [12, 13],
  "visuales": ["dg-milenio"],
  "refs_apocalipsis": ["20:1-6"],
  "notas_no_usadas": ["id"]
}
```
Reglas: `apartados` de 3 a 7 según el largo; todo `parrafos[].texto` con `fuentes`; `dias_relacionados` son números de día del plan
(`plan/plan.json`); `visuales` ids de `plan/visuales.json` (máx. 3); `para_conversar` 3 preguntas.
