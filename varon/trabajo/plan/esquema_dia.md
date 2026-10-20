# Esquema de cada día del estudio «El varón según Dios» (JSON)

Un día = 20 a 30 minutos de estudio personal (unas 2.000 a 2.600 palabras en el cuerpo principal, sin contar «profundizar»).
Lo lee un hombre cristiano protestante de Buenos Aires: se le habla de **vos**, en castellano rioplatense, cálido, directo y
sin relleno. Nada inventado: cada afirmación lleva en `fuentes` los ids de las notas que la respaldan (p. ej. `b_014#7`)
o de los datos de la web (p. ej. `W0123`).

```json
{
  "dia": 12,
  "titulo": "…",
  "bajada": "Una oración que dice qué vas a aprender hoy.",
  "minutos": {"estudio": 25},
  "lectura": {"pasaje": "Efesios 5:22-33", "porque": "por qué leer este pasaje hoy (una frase)"},
  "versiculos": [{"ref": "Efesios 5:25", "porque": "por qué es clave"}],
  "entrada": {"texto": "Uno o dos párrafos que plantean el tema y por qué te importa.", "fuentes": ["…"]},
  "apartados": [
    {"titulo": "…", "parrafos": [{"texto": "…", "fuentes": ["…"]}], "destacado": {"texto": "Una oración para retener.", "fuentes": ["…"]}}
  ],
  "citas": [{"texto": "frase textual de un CITA de las notas", "autor": "…", "obra": "…", "fuentes": ["…"]}],
  "datos": [{"valor": "10,8 %", "texto": "qué mide, dónde y cuándo", "fuentes": ["W0007"]}],
  "modelo": {"persona": "Nehemías", "texto": "qué enseña su vida sobre el tema del día", "refs": ["Neh 4:14"], "fuentes": ["…"]},
  "palabras": [{"original": "ἀγάπη", "idioma": "griego", "translit": "agápē", "ref": "Ef 5:25", "significado": "…", "fuentes": ["…"]}],
  "interpretaciones": [{"tema": "…", "posturas": [{"postura": "…", "quien": "…", "fuentes": ["…"]}], "nota": "…"}],
  "conexiones": [{"ref": "1 Pedro 3:7", "nota": "…", "fuentes": ["…"]}],
  "para_vivir": [{"texto": "un paso concreto para esta semana", "fuentes": ["…"]}],
  "para_reflexionar": ["pregunta 1", "pregunta 2", "pregunta 3"],
  "para_conversar": ["una pregunta para charlar con tu esposa o con un amigo (optativa)"],
  "para_orar": "Una oración breve que convierta lo aprendido en oración.",
  "profundizar": [{"titulo": "…", "texto": "…", "fuentes": ["…"]}],
  "notas_no_usadas": "ids de notas importantes que quedaron afuera y por qué"
}
```

Reglas:
- `lectura`: un pasaje bíblico para leer antes (idealmente 10 a 30 versículos), con nombre castellano completo del libro.
- `versiculos`: 1 a 3 versículos clave (cada uno de 1 a 3 versículos), con el nombre castellano completo del libro
  («1 Timoteo 3:2», no «1 Ti 3:2»). La app pone el texto RVR1960. No copies el texto bíblico en el estudio salvo frases
  breves entre comillas que ya traigan las notas.
- `apartados`: 3 a 6, en orden lógico; el día se lee de corrido, no como lista de notas.
- `citas`: solo frases que figuran como CITA en las notas, textuales (máximo 3).
- `datos`: solo los que trae el insumo (datos de la web con id W… o notas de tipo «dato» con su año y fuente). Decí siempre
  el año y el lugar; los datos viejos de un libro se presentan como tales.
- `modelo`: solo si las notas traen un varón (bíblico o histórico) que ilustre el tema.
- `palabras`: solo términos griegos o hebreos que comentan las notas; la grafía original solo si la nota la trae.
- `interpretaciones`: cuando las fuentes difieren, cada postura con quién la sostiene, sin tomar partido salvo que coincidan.
- `para_reflexionar`: 3 preguntas personales y concretas; `para_conversar`: 0 a 2; `para_orar`: breve.
