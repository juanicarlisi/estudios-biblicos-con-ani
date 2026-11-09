# Esquema de cada día del estudio de 1 Pedro a Judas (JSON)

Archivo: `pedro-judas/trabajo/dias/dia_NN.json`. Castellano rioplatense neutro, claro y cálido; nada inventado: cada afirmación
lleva al menos una fuente (`fuentes`) con ids de notas extraídas (los `[id]` de los insumos del día, p. ej. `kis1p_04_a#12`).
Mismo esquema que Apocalipsis, con el campo `libro` y referencias con sigla (`1P`, `2P`, `1J`, `2J`, `3J`, `Jd`).

```json
{
  "dia": 9, "libro": "1P", "desde": "1P 3:13", "hasta": "1P 3:17", "titulo": "…",
  "minutos": {"lectura": 3, "estudio": 22},
  "contexto": {"antes": "…", "ahora": "…", "donde": "…", "cuando": "…", "despues": "…", "fuentes": ["id", "id"]},
  "versiculo_clave": {"ref": "1P 3:15", "porque": "…"},
  "panorama": {"texto": "Un párrafo con la idea central del tramo.", "fuentes": ["id"]},
  "secciones": [
    {"rango": "1P 3:13-14", "titulo": "…", "notas": [{"texto": "…", "fuentes": ["id", "id"], "tipo": "exegesis"}]}
  ],
  "palabras": [{"ref": "1P 3:15", "griego": "ἀπολογία", "translit": "apología", "significado": "…", "fuentes": ["id"]}],
  "cristo": [{"texto": "…", "refs": ["Is 53:9"], "fuentes": ["id"]}],
  "interpretaciones": [{"tema": "…", "posturas": [{"postura": "…", "quien": "Kistemaker (reformado)", "fuentes": ["id"]}], "nota": "…"}],
  "antiguo_testamento": [{"ref": "Is 8:12-13", "nota": "cómo lo usa el pasaje", "fuentes": ["id"]}],
  "biblioteca": [{"texto": "…", "autor": "…", "obra": "…", "pagina": "…", "tipo": "doctrina|aplicacion|ilustracion|historia|apologetica"}],
  "conexiones": [{"ref": "Mt 5:10-12", "nota": "…", "fuentes": ["id"]}],
  "para_vivir": [{"texto": "…", "fuentes": ["id"]}],
  "para_conversar": ["Pregunta 1", "Pregunta 2", "Pregunta 3"],
  "para_orar": "Una o dos oraciones que conviertan la enseñanza del día en oración.",
  "visuales": ["dg-sufrimiento", "mapa-provincias"],
  "anexos": ["T1"],
  "profundizar": [{"titulo": "…", "texto": "…", "fuentes": ["id"]}]
}
```

Reglas:
- `libro`, `desde` y `hasta`: copiados del plan (`plan/plan.json`); el día de 2 y 3 Juan juntos lleva `"libro": "2J+3J"`.
- `secciones`: siguen el texto en orden, por unidades de sentido; 3 a 7 por día (menos si el tramo es de uno o dos versículos: ahí
  las secciones pueden ser por frase o por tema). Sin repetir lo mismo con otras palabras. Su `rango` lleva sigla.
- Texto bíblico: el pasaje completo NO se transcribe (lo lee la pareja en su Biblia). Solo `versiculo_clave.ref` (hasta 3 versículos
  seguidos): la app inserta el texto RVR1960 por referencia. Dentro de las notas se pueden citar frases cortas de la RVR1960 entre
  «», copiadas exactas de los insumos (máx. 12 palabras seguidas). Las comillas «» son solo para texto bíblico literal.
- `palabras`: solo palabras griegas que las fuentes comentan; la grafía griega debe aparecer en el texto griego del día (SBLGNT) o en la nota fuente.
- `interpretaciones`: cuando las fuentes difieren (pasajes difíciles, tradiciones reformada/wesleyana/dispensacional, escuelas
  escatológicas pre/a/posmilenial y pre/mid/postribulacional), se presentan las posturas con quién las sostiene, sin tomar partido
  (salvo que todas coincidan).
- `antiguo_testamento`: citas y alusiones del AT que el pasaje usa (frecuentes en 1 Pedro, 2 Pedro y Judas) según las fuentes; opcional.
- `visuales`: ids de `plan/visuales.json` que ayudan a este día (máx. 3). `anexos`: ids de `plan/articulos.json` para profundizar (máx. 4).
- `biblioteca`: aportes de libros de referencia que no entran en las secciones; con autor, obra y página (de la nota fuente).
- `para_conversar` (3 preguntas) y `para_orar` se formulan a partir de lo que enseñan las fuentes del día (son guía de estudio, no datos).
- Extensión objetivo: 1.800 a 2.600 palabras de estudio (sin `profundizar`), que se lean en 20 a 30 minutos. Si el tramo es muy corto y
  hay poco material, bajar sin rellenar; si hay mucho, lo optativo va a `profundizar`.
