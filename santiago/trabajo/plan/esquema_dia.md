# Esquema de cada día del estudio de Santiago (JSON)

Archivo: `santiago/trabajo/dias/dia_NN.json` (los borradores, en `dias/borrador_NN.json`). Todo texto en castellano rioplatense neutro, claro y cálido;
nada inventado: cada afirmación lleva al menos una fuente (`fuentes`) que remite a una nota extraída (bloque y número: `macarthur_05#12`).

```json
{
  "dia": 1,
  "desde": "1:2", "hasta": "1:4",
  "titulo": "…",
  "minutos": {"lectura": 3, "estudio": 22},
  "contexto": {
    "antes": "Qué pasó antes (o, el día 1, de qué carta se trata).",
    "ahora": "Qué pasa en este tramo, en dos o tres oraciones.",
    "donde": "Lugar desde donde escribe o a donde llega (si aplica).",
    "cuando": "Momento en la historia de la iglesia (y fecha según las fuentes, aclarando de quién es la cronología).",
    "despues": "Qué viene en el próximo tramo.",
    "fuentes": ["macarthur_01#2"]
  },
  "versiculo_clave": {"ref": "1:2", "porque": "Por qué este versículo es la clave del tramo."},
  "panorama": {"texto": "Un párrafo que da la idea central del tramo.", "fuentes": ["…"]},
  "secciones": [
    {"rango": "1:2", "titulo": "…",
     "notas": [{"texto": "…", "fuentes": ["macarthur_01#3", "kistemaker_02#7"], "tipo": "explicacion_texto"}]}
  ],
  "palabras": [{"ref": "1:2", "griego": "πειρασμοῖς", "translit": "peirasmois", "significado": "…", "fuentes": ["…"]}],
  "cristo": [{"texto": "…", "refs": ["Jn 16:33"], "fuentes": ["…"]}],
  "eco_de_jesus": [{"texto": "Cómo este pasaje suena a lo que enseñó Jesús.", "refs": ["Mt 5:11-12"], "fuentes": ["…"]}],
  "interpretaciones": [{"tema": "…", "posturas": [{"postura": "…", "quien": "Kistemaker", "fuentes": ["…"]}], "nota": "…"}],
  "biblioteca": [{"texto": "…", "autor": "…", "obra": "…", "tipo": "doctrina|aplicacion|ilustracion|apologetica", "fuentes": ["r1_004#3"]}],
  "conexiones": [{"ref": "Ro 5:3-4", "nota": "…", "fuentes": ["…"]}],
  "para_vivir": [{"texto": "…", "fuentes": ["…"]}],
  "para_conversar": ["Pregunta 1", "Pregunta 2", "Pregunta 3"],
  "para_orar": "Una o dos oraciones que conviertan la enseñanza del día en oración.",
  "profundizar": [{"titulo": "…", "texto": "…", "fuentes": ["…"]}],
  "diagrama": {"tipo": "pasos|escalera|comparacion|imagenes|tabla", "titulo": "…", "descripcion": "…", "items": [], "columnas": [], "filas": [], "fuentes": ["…"]},
  "anexos": [{"id": "T5", "por_que": "Una frase: qué va a encontrar ahí."}],
  "lugares": ["jerusalen"],
  "notas_no_usadas": "Ids de notas importantes que quedaron afuera y por qué."
}
```

Reglas:
- `secciones`: siguen el texto en orden, por unidades de sentido; 2 a 7 secciones por día (una sola si el día es de un versículo). Sin repetir lo mismo con otras palabras.
  El `rango` de cada sección es de versículos de este día (`"1:2"`, `"1:3-4"`).
- Citas textuales de la Biblia: solo con el texto exacto de la RVR1960 que trae el insumo (la app inserta el texto del pasaje y del versículo clave por referencia).
- `palabras`: solo palabras griegas que las notas comentan; la grafía griega se verifica con `griego.py` (el texto de Santiago, SBLGNT). Si la palabra no es de Santiago, `griego` va vacío.
- `interpretaciones`: cuando las fuentes difieren se presentan las posturas sin tomar partido (salvo que todas coincidan).
- `eco_de_jesus`: solo cuando las notas ligan el pasaje con palabras o hechos de Jesús (Sermón del Monte, parábolas, etc.). Puede quedar vacío.
- `diagrama` (opcional, solo si las notas dan material para un esquema fiel): `pasos` (proceso: items `{titulo, texto, ref}`), `escalera` (mandatos o grados: items `{titulo, texto, ref}`),
  `comparacion` (columnas y filas `{etiqueta, celdas}`), `imagenes` (items `{icono, titulo, texto, ref}`; iconos: ola, hierba, espejo, freno, timon, fuego, bestia, fuente, hoja, uvas, nube, lluvia,
  aceite, corona, balanza, libro, corazon, boca, oido, moneda, camino, mano) o `tabla` (columnas y filas). Todo lo que dice el diagrama sale de las notas citadas en sus `fuentes`.
- `anexos`: enlaces a los temas (`T1`…) y anexos (`A1`…) de la lista que trae el insumo cuando el pasaje los toca de lleno.
- `para_conversar` y `para_orar` se formulan a partir de lo que enseñan las fuentes del día (son guía de estudio, no datos).
- Extensión: que el estudio del día se lea en 20 a 30 minutos (unas 2.000 a 3.000 palabras sin contar `profundizar`). Un día con poco material puede ser más corto: lo necesario, sin relleno.
