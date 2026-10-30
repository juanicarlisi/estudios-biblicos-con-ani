# Esquema de cada día del estudio de Apocalipsis (JSON)

Archivo: `apocalipsis/trabajo/dias/dia_NN.json`. Castellano rioplatense neutro, claro y cálido; nada inventado: cada afirmación
lleva al menos una fuente (`fuentes`) con ids de notas extraídas (los `[id]` de los insumos del día, p. ej. `macarthur_04_a#12`).

```json
{
  "dia": 1, "desde": "1:1", "hasta": "1:3", "titulo": "…",
  "minutos": {"lectura": 3, "estudio": 22},
  "contexto": {"antes": "…", "ahora": "…", "donde": "…", "cuando": "…", "despues": "…", "fuentes": ["id", "id"]},
  "versiculo_clave": {"ref": "1:3", "porque": "…"},
  "panorama": {"texto": "Un párrafo con la idea central del tramo.", "fuentes": ["id"]},
  "secciones": [
    {"rango": "1:1-2", "titulo": "…", "notas": [{"texto": "…", "fuentes": ["id", "id"], "tipo": "explicacion_texto"}]}
  ],
  "simbolos": [{"signo": "siete estrellas", "significado": "…", "refs": ["1:20"], "fuentes": ["id"]}],
  "palabras": [{"ref": "1:1", "griego": "ἀποκάλυψις", "translit": "apokálypsis", "significado": "…", "fuentes": ["id"]}],
  "cristo": [{"texto": "…", "refs": ["Jn 1:1-3"], "fuentes": ["id"]}],
  "interpretaciones": [{"tema": "…", "posturas": [{"postura": "…", "quien": "MacArthur", "fuentes": ["id"]}], "nota": "…"}],
  "biblioteca": [{"texto": "…", "autor": "…", "obra": "…", "pagina": "…", "tipo": "doctrina|aplicacion|ilustracion|historia|apologetica"}],
  "conexiones": [{"ref": "Dn 7:13", "nota": "…", "fuentes": ["id"]}],
  "para_vivir": [{"texto": "…", "fuentes": ["id"]}],
  "para_conversar": ["Pregunta 1", "Pregunta 2", "Pregunta 3"],
  "para_orar": "Una o dos oraciones que conviertan la enseñanza del día en oración.",
  "visuales": ["mapa-asia", "dg-cartas"],
  "anexos": ["T1", "T4"],
  "profundizar": [{"titulo": "…", "texto": "…", "fuentes": ["id"]}]
}
```

Reglas:
- `secciones`: siguen el texto en orden, por unidades de sentido; 3 a 7 por día (menos si el tramo es de uno o dos versículos: ahí
  las secciones pueden ser por frase o por tema). Sin repetir lo mismo con otras palabras.
- Texto bíblico: el pasaje completo NO se transcribe (lo lee la pareja en su Biblia). Solo `versiculo_clave.ref` (hasta 3 versículos
  seguidos): la app inserta el texto RVR1960 por referencia. Dentro de las notas se pueden citar frases cortas de la RVR1960 entre
  «», copiadas exactas de los insumos (máx. 12 palabras seguidas).
- `palabras`: solo palabras griegas que las fuentes comentan; la grafía griega debe aparecer en el texto griego del día o en la nota fuente.
- `simbolos`: los signos del pasaje (números, colores, animales, objetos) con su significado según las fuentes; si hay desacuerdo, `significado` dice «según X…, según Y…».
- `interpretaciones`: cuando las fuentes difieren (escuelas preterista/historicista/futurista/idealista; pre/a/posmilenialismo; pre/medio/postribulacionismo; Israel/Iglesia), se presentan las posturas con quién las sostiene, sin tomar partido (salvo que todas coincidan).
  Los autores de corriente carismática/profética (TTL, MiSion) se citan con fidelidad y atribuidos, nunca como "la" posición.
- `visuales`: ids de `plan/visuales.json` que ayudan a este día (máx. 3). `anexos`: ids de `plan/articulos.json` para profundizar (máx. 4).
- `biblioteca`: aportes de libros de referencia que no entran en las secciones; con autor, obra y página (de la nota fuente).
- `para_conversar` (3 preguntas) y `para_orar` se formulan a partir de lo que enseñan las fuentes del día (son guía de estudio, no datos).
- Extensión objetivo: 1.800 a 2.600 palabras de estudio (sin `profundizar`), que se lean en 20 a 30 minutos. Si el tramo es muy corto y
  hay poco material, bajar sin rellenar; si hay mucho, lo optativo va a `profundizar`.
