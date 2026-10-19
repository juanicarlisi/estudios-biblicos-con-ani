export const meta = {
  name: 'genesis-sintetizar-dias',
  description: 'Escribe el estudio de cada día a partir de las notas extraídas (sin inventar) y lo verifica contra las notas y el texto',
  phases: [
    { title: 'Escribir', detail: 'un día por agente, a partir de su archivo de insumos' },
    { title: 'Verificar', detail: 'otro agente coteja cada afirmación con sus notas, las citas bíblicas y el hebreo' },
  ],
}
const SEC = { type: 'object', properties: { texto: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['texto', 'fuentes'] }
const SCHEMA = {
  type: 'object',
  properties: {
    dia: { type: 'integer' }, desde: { type: 'string' }, hasta: { type: 'string' }, titulo: { type: 'string' },
    minutos: { type: 'object', properties: { lectura: { type: 'integer' }, estudio: { type: 'integer' } }, required: ['lectura', 'estudio'] },
    contexto: { type: 'object', properties: { antes: { type: 'string' }, ahora: { type: 'string' }, donde: { type: 'string' }, cuando: { type: 'string' }, despues: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['antes', 'ahora', 'donde', 'cuando', 'despues', 'fuentes'] },
    versiculo_clave: { type: 'object', properties: { ref: { type: 'string' }, porque: { type: 'string' } }, required: ['ref', 'porque'] },
    panorama: SEC,
    secciones: { type: 'array', items: { type: 'object', properties: { rango: { type: 'string' }, titulo: { type: 'string' }, notas: { type: 'array', items: { type: 'object', properties: { texto: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } }, tipo: { type: 'string' } }, required: ['texto', 'fuentes'] } } }, required: ['rango', 'titulo', 'notas'] } },
    palabras: { type: 'array', items: { type: 'object', properties: { ref: { type: 'string' }, hebreo: { type: 'string' }, translit: { type: 'string' }, significado: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['ref', 'translit', 'significado', 'fuentes'] } },
    cristo: { type: 'array', items: { type: 'object', properties: { texto: { type: 'string' }, refs: { type: 'array', items: { type: 'string' } }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['texto', 'fuentes'] } },
    interpretaciones: { type: 'array', items: { type: 'object', properties: { tema: { type: 'string' }, posturas: { type: 'array', items: { type: 'object', properties: { postura: { type: 'string' }, quien: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['postura', 'quien', 'fuentes'] } }, nota: { type: 'string' } }, required: ['tema', 'posturas'] } },
    biblioteca: { type: 'array', items: { type: 'object', properties: { texto: { type: 'string' }, autor: { type: 'string' }, obra: { type: 'string' }, tipo: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['texto', 'autor', 'obra', 'fuentes'] } },
    conexiones: { type: 'array', items: { type: 'object', properties: { ref: { type: 'string' }, nota: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['ref', 'nota', 'fuentes'] } },
    para_vivir: { type: 'array', items: SEC },
    para_conversar: { type: 'array', items: { type: 'string' } },
    para_orar: { type: 'string' },
    profundizar: { type: 'array', items: { type: 'object', properties: { titulo: { type: 'string' }, texto: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['titulo', 'texto', 'fuentes'] } },
    notas_no_usadas: { type: 'string', description: 'Ids de notas importantes que quedaron afuera y por qué (repetidas, marginales)' },
  },
  required: ['dia', 'desde', 'hasta', 'titulo', 'minutos', 'contexto', 'versiculo_clave', 'panorama', 'secciones', 'palabras', 'cristo', 'interpretaciones', 'biblioteca', 'conexiones', 'para_vivir', 'para_conversar', 'para_orar', 'profundizar', 'notas_no_usadas'],
}
const n2 = d => String(d).padStart(2, '0')
const escribir = d => `Vas a escribir el estudio del DÍA ${d} de un plan de lectura de Génesis para un matrimonio protestante joven de Buenos Aires que lee unos 20 versículos por día y dedica media hora a leer y estudiar juntos. Quieren entender las Escrituras a fondo y vivirlas.

Leé con UNA llamada a Read (con allow_large: true) el archivo /home/user/trabajo/insumos/dia_${n2(d)}.txt: trae el texto RVR1960 del pasaje y TODAS las notas extraídas de su biblioteca para ese tramo, cada una con un id entre corchetes. Leé también /home/user/trabajo/plan/esquema_dia.md (reglas del formato). Después devolvé el día con la herramienta de salida estructurada. No uses otras herramientas.

Reglas de oro:
1. NO INVENTAR NADA. Cada afirmación sale de las notas y lleva en "fuentes" los ids de las notas que la respaldan (ej.: "kline_02#15"). Si varias fuentes dicen lo mismo, condensalo en una sola afirmación con todos sus ids. Nada de conocimiento propio: si un dato no está en las notas, no va.
2. CONDENSAR CON CRITERIO: esto no es una lista de notas sino un estudio que se lee de corrido. Ordená por el texto, uní lo repetido, priorizá lo central (importancia 3 y 2) y lo que ayuda a entender y a vivir. Lo valioso que no entra en el flujo principal va a "profundizar". Que no se pierda nada importante: si dejás afuera notas de importancia 3, explicá por qué en "notas_no_usadas".
3. INTERPRETACIONES: cuando las fuentes difieren (por ejemplo, los días de la creación, los «hijos de Dios», la ubicación de un lugar), presentá cada postura con quién la sostiene, sin tomar partido salvo que todas coincidan.
4. TONO: castellano rioplatense neutro, cálido y claro, hablándoles a «ustedes». Explicá los términos técnicos la primera vez. Frases cortas. Nada de relleno ni de frases hechas. Que se lea de corrido: NO encadenes «según Kline… Livingston agrega… MacArthur dice…». Nombrá al autor solo cuando aporta algo propio (una postura, una frase memorable, un dato que solo él da) o cuando las fuentes difieren; lo demás se afirma directamente y las fuentes quedan en "fuentes" (la app las muestra como etiquetas).
5. PRÁCTICO PARA EL DÍA: el estudio principal (contexto, panorama, secciones, palabras, cristo, interpretaciones, biblioteca, conexiones, para_vivir) debe leerse en unos 20 minutos (1.600 a 2.200 palabras). Lo valioso que no entra va a "profundizar", que es optativo.
6. "contexto": qué pasó antes (resumen del tramo anterior), qué pasa ahora, dónde y cuándo (si las fuentes dan fechas, decí de quién es la cronología) y qué viene después. Esto le da a cada día una línea clara y progresiva.
7. "versiculo_clave": solo la referencia (la app pone el texto RVR1960) y por qué es clave.
8. "palabras": solo palabras hebreas que comentan las notas; escribí la grafía hebrea si la nota la trae.
9. "para_conversar" (3 preguntas) y "para_orar" se formulan a partir de lo que enseñan las fuentes del día; pensadas para una pareja.
10. "biblioteca": aportes de los libros de referencia (notas cuyo id empieza con r1_ o r2_), con autor y obra. Si no hay, lista vacía.`
const verificar = d => `Sos el verificador de un estudio bíblico que no puede contener nada inventado. Leé (con Read y allow_large: true) el insumo /home/user/trabajo/insumos/dia_${n2(d)}.txt y el borrador /home/user/trabajo/dias/borrador_${n2(d)}.json.

Revisá TODO el borrador:
1. Cada afirmación debe estar respaldada por las notas cuyos ids cita en "fuentes" (buscalos en el insumo). Corregí lo que exagere, mezcle o agregue algo que las notas no dicen; si algo no tiene respaldo, eliminalo. Si un id no existe, buscá la nota correcta o eliminá la afirmación.
2. Lo que se atribuye a un autor (en "interpretaciones" o "biblioteca") debe ser de ese autor.
3. Si el texto cita palabras de la Biblia entre comillas, deben coincidir con la RVR1960 del insumo.
4. "palabras": comprobá la grafía hebrea con: python3 /home/user/trabajo/scripts/hebreo.py C:V (muestra las palabras hebreas del versículo con su número Strong). Corregí la grafía o dejá "hebreo" vacío si no se puede confirmar; el significado debe venir de las notas.
5. Revisá que el castellano sea claro, que no se repitan ideas y que no se encadenen atribuciones («según X… Y agrega…»): el autor se nombra solo cuando aporta algo propio o cuando las fuentes difieren.
6. No alargues el estudio: corregí lo que haga falta, pero mantené el largo (unas 1.600 a 2.200 palabras en el cuerpo principal). Si falta algo importante de las notas, ponelo en "profundizar".
Devolvé el día completo y corregido con la herramienta de salida estructurada (mismo esquema). Podés usar Read, Bash (solo para hebreo.py) y la salida estructurada.`
const res = await pipeline(
  args.dias,
  d => agent(escribir(d), { label: `escribir:dia${n2(d)}`, phase: 'Escribir', schema: SCHEMA }),
  (r, d) => r ? agent(`${verificar(d)}\n\nEl borrador (en lugar de leer /home/user/trabajo/dias/borrador_${n2(d)}.json, usá este, que es el mismo):\n${JSON.stringify(r)}`, { label: `verificar:dia${n2(d)}`, phase: 'Verificar', schema: SCHEMA }).then(v => ({ dia: d, ok: !!v })) : { dia: d, ok: false },
)
return res
