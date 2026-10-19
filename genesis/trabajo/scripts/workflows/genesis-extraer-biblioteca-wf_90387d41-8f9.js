export const meta = {
  name: 'genesis-extraer-biblioteca',
  description: 'Extrae y verifica, bloque por bloque, todo lo sustancial de los comentarios de Génesis de la biblioteca',
  phases: [
    { title: 'Extraer', detail: 'un agente por bloque lee todas las páginas y escribe notas con referencia y página' },
    { title: 'Verificar', detail: 'otro agente coteja cada nota con la página, corrige y completa' },
  ],
}

const CHUNKS = args.chunks

const NOTE_SPEC = `Cada nota es un objeto JSON con estos campos:
- "ref": pasaje de Génesis al que se refiere, en formato "C:V" o "C:V-C:V" o "C:V-V" (ej.: "1:1", "1:26-28", "2:4-3:24", "12"). Usá "intro" para lo que trata el libro entero (autor, fecha, propósito, estructura, temas, canon, crítica). Si la nota es un tema transversal sin pasaje puntual, usá "tema".
- "tipo": uno de: contexto_historico, cultura_costumbres, arqueologia_geografia, hebreo_palabra, explicacion_texto, teologia_doctrina, cristo_en_genesis, conexion_biblica, aplicacion_practica, ilustracion, dificultad_interpretaciones, estructura_bosquejo, cronologia_fechas, personaje, pregunta_reflexion.
- "titulo": rótulo breve (hasta 10 palabras).
- "contenido": condensación fiel, en castellano, de lo que el autor afirma (2 a 6 oraciones; más si es un bosquejo o una tabla). Conservá sus matices, nombres, números, fechas y argumentos. NADA que el autor no diga: no agregues conocimiento propio ni opiniones.
- "cita": (opcional) frase textual del autor, hasta 50 palabras, solo cuando la redacción vale por sí misma (una definición, una frase memorable). Copiala exacta, corrigiendo solo errores evidentes de OCR.
- "refs_biblicas": lista de citas bíblicas que el autor usa en ese punto (ej.: ["Ro 5:12", "He 11:8"]). Lista vacía si no hay.
- "hebreo": (opcional) objeto {"palabra": ..., "transliteracion": ..., "significado": ...} tal como lo da el autor, si comenta una palabra hebrea (o griega de la LXX).
- "pagina": el rótulo de página tal como aparece en el encabezado "=== [...] ===" donde está el contenido (ej.: "PDF 12 | pág. impresa 86"). En el Comentario Bíblico Mundo Hispano agregá también el marcador "[Page N]" más cercano si aparece en el texto.
- "importancia": 3 = central para entender el pasaje; 2 = valioso; 1 = detalle menor.
- "postura": (opcional) si el autor presenta varias interpretaciones, resumí cuáles y cuál prefiere él.`

function extractPrompt(c) {
  return `Estamos construyendo el mejor estudio posible de Génesis para un matrimonio protestante que lo va a leer 20 versículos por día. La regla de oro: NO INVENTAR NADA; todo sale de los libros de su biblioteca.

Tu tarea: leer COMPLETO el archivo ${c.archivo} (bloque ${c.id}, páginas ${c.paginas} de: ${c.descripcion}) y extraer TODO aporte sustancial del autor, ordenado por el pasaje de Génesis que comenta. Leé el archivo entero con la herramienta Read (si es largo, en partes con offset/limit) y no saltees ninguna página. Ser exhaustivo es lo más importante: si dudás si algo es sustancial, incluilo con importancia 1.

Qué incluir: explicación del texto versículo por versículo, contexto histórico y cultural, costumbres, arqueología, geografía, palabras hebreas, cronología y fechas, teología y doctrina, cómo apunta a Cristo, conexiones con el resto de la Biblia, dificultades e interpretaciones, bosquejos y estructura, tablas, aplicaciones prácticas, ilustraciones, preguntas. Qué NO incluir: datos de la editorial, listas de abreviaturas, índices y bibliografías.

Cuidado: si el texto viene de OCR, puede tener errores; interpretalos con sentido común sin cambiar lo que dice. Si una nota abarca varios versículos, usá el rango. Si el autor discute una postura que rechaza, registrá la postura y su refutación.

${NOTE_SPEC}

Escribí el resultado con la herramienta Write en /home/user/trabajo/extracciones/biblio/${c.id}.json como un objeto JSON: {"bloque": "${c.id}", "notas": [ ... ]}. Asegurate de que sea JSON válido (comillas dobles, sin comas sobrantes). Después validalo con: python3 -c "import json;d=json.load(open('/home/user/trabajo/extracciones/biblio/${c.id}.json'));print(len(d['notas']))".

Tu respuesta final: solo una línea con la cantidad de notas, el rango de capítulos cubierto y cualquier problema (páginas ilegibles, etc.).`
}

function verifyPrompt(c) {
  return `Sos el verificador de un estudio de Génesis que NO puede contener nada inventado ni dejar afuera nada importante.

Archivo fuente: ${c.archivo} (bloque ${c.id}, páginas ${c.paginas} de: ${c.descripcion}).
Notas extraídas por otro agente: /home/user/trabajo/extracciones/biblio/${c.id}.json

Hacé esto:
1. Leé COMPLETO el archivo fuente (con Read, en partes si hace falta) y todas las notas.
2. FIDELIDAD: para cada nota, comprobá que lo que dice está realmente en la página indicada y con el sentido del autor. Corregí lo impreciso (incluidos "ref", "pagina" y "cita", que debe ser textual). Borrá lo que no tenga respaldo en el texto.
3. COMPLETITUD: recorré el fuente página por página y agregá notas para todo aporte sustancial que falte (explicaciones de versículos, datos históricos, palabras hebreas, aplicaciones, interpretaciones, bosquejos, tablas). Esta etapa es clave: el objetivo es que no se pierda nada valioso del libro.
4. Reescribí el archivo /home/user/trabajo/extracciones/biblio/${c.id}.json con la versión corregida y completa, en el mismo formato {"bloque": "${c.id}", "notas": [...]}, y agregá "verificado": true. Validá el JSON con python3 como en el paso anterior.

${NOTE_SPEC}

Tu respuesta final: una línea con: notas finales, cuántas corregiste, cuántas borraste y cuántas agregaste.`
}

const results = await pipeline(
  CHUNKS,
  c => agent(extractPrompt(c), { label: `extraer:${c.id}`, phase: 'Extraer' }),
  (r, c) => agent(verifyPrompt(c), { label: `verificar:${c.id}`, phase: 'Verificar' }).then(v => ({ id: c.id, extraccion: r, verificacion: v })),
)
return results.filter(Boolean)
