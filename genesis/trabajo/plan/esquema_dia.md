# Esquema de cada día del estudio (JSON)

Archivo: `/home/user/trabajo/dias/dia_NN.json`. Todo texto en castellano rioplatense neutro, claro y cálido; nada inventado:
cada afirmación lleva al menos una fuente (`fuentes`) que remite a una nota extraída (bloque y página).

```json
{
  "dia": 1,
  "desde": "1:1", "hasta": "1:19",
  "titulo": "…",
  "minutos": {"lectura": 6, "estudio": 22},
  "contexto": {
    "antes": "Qué pasó antes (o, el día 1, dónde empieza la Biblia).",
    "ahora": "Qué pasa en este tramo, en dos o tres oraciones.",
    "donde": "Lugar (si aplica), con nombre que aparezca en el mapa.",
    "cuando": "Momento en la historia de Génesis (y fecha según las fuentes, aclarando de quién es la cronología).",
    "despues": "Qué viene en el próximo tramo.",
    "fuentes": ["kline_01:PDF 2"]
  },
  "versiculo_clave": {"ref": "1:1"},
  "panorama": {"texto": "Un párrafo que da la idea central del tramo.", "fuentes": ["…"]},
  "secciones": [
    {"rango": "1:1-2", "titulo": "…",
     "notas": [{"texto": "…", "fuentes": ["macarthur_01:PDF 83", "kline_01:PDF 2 | pág. impresa 76"], "tipo": "explicacion_texto"}]}
  ],
  "palabras": [{"ref": "1:1", "hebreo": "בָּרָא", "translit": "bará", "significado": "…", "fuentes": ["…"]}],
  "cristo": [{"texto": "…", "refs": ["Jn 1:1-3"], "fuentes": ["…"]}],
  "interpretaciones": [{"tema": "…", "posturas": [{"postura": "…", "quien": "Kline", "fuentes": ["…"]}], "nota": "…"}],
  "biblioteca": [{"texto": "…", "autor": "…", "obra": "…", "pagina": "…", "tipo": "doctrina|aplicacion|ilustracion|matrimonio|apologetica"}],
  "conexiones": [{"ref": "He 11:3", "nota": "…", "fuentes": ["…"]}],
  "para_vivir": [{"texto": "…", "fuentes": ["…"]}],
  "para_conversar": ["Pregunta 1", "Pregunta 2", "Pregunta 3"],
  "para_orar": "Una o dos oraciones que conviertan la enseñanza del día en oración.",
  "profundizar": [{"titulo": "…", "texto": "…", "fuentes": ["…"]}]
}
```

Reglas:
- `secciones`: siguen el texto en orden, por unidades de sentido; 3 a 7 secciones por día. Sin repetir lo mismo con otras palabras.
- Citas textuales de la Biblia: solo con el texto exacto de `rvr1960_genesis.json` (las inserta la app por referencia).
- `palabras`: solo palabras hebreas que las fuentes comentan; la grafía hebrea se verifica con `hebreo.py`.
- `interpretaciones`: cuando las fuentes difieren, se presentan las posturas sin tomar partido (salvo que todas coincidan).
- `para_conversar` y `para_orar` se formulan a partir de lo que enseñan las fuentes del día (son guía de estudio, no datos).
- Extensión objetivo: que el estudio del día se lea en 20 a 25 minutos (unas 1.800 a 2.600 palabras sin contar `profundizar`).
