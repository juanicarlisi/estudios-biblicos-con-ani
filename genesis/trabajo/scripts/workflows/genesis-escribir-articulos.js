export const meta = {
  name: 'genesis-escribir-articulos',
  description: 'Escribe la introducción, los panoramas de las partes y los temas de Génesis a partir de las notas (sin inventar) y los verifica',
  phases: [
    { title: 'Escribir', detail: 'un artículo por agente, a partir de su archivo de notas' },
    { title: 'Verificar', detail: 'otro agente coteja cada afirmación con sus notas y las citas bíblicas' },
  ],
}
const SEC = { type: 'object', properties: { texto: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['texto', 'fuentes'] }
const SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' }, titulo: { type: 'string' }, bajada: { type: 'string', description: 'Una oración que dice de qué trata la sección' },
    entrada: SEC,
    versiculos: { type: 'array', description: 'Hasta 3 versículos de Génesis clave para la sección (solo la referencia C:V o C:V-V, de no más de 3 versículos)', items: { type: 'object', properties: { ref: { type: 'string' }, porque: { type: 'string' } }, required: ['ref', 'porque'] } },
    apartados: { type: 'array', items: { type: 'object', properties: { titulo: { type: 'string' }, parrafos: { type: 'array', items: SEC }, destacado: SEC }, required: ['titulo', 'parrafos'] } },
    palabras: { type: 'array', items: { type: 'object', properties: { ref: { type: 'string' }, hebreo: { type: 'string' }, translit: { type: 'string' }, significado: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['ref', 'translit', 'significado', 'fuentes'] } },
    interpretaciones: { type: 'array', items: { type: 'object', properties: { tema: { type: 'string' }, posturas: { type: 'array', items: { type: 'object', properties: { postura: { type: 'string' }, quien: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['postura', 'quien', 'fuentes'] } }, nota: { type: 'string' } }, required: ['tema', 'posturas'] } },
    citas: { type: 'array', description: 'Frases textuales que figuran como CITA en las notas', items: { type: 'object', properties: { texto: { type: 'string' }, autor: { type: 'string' }, obra: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['texto', 'autor', 'obra', 'fuentes'] } },
    conexiones: { type: 'array', items: { type: 'object', properties: { ref: { type: 'string' }, nota: { type: 'string' }, fuentes: { type: 'array', items: { type: 'string' } } }, required: ['ref', 'nota', 'fuentes'] } },
    para_vivir: { type: 'array', items: SEC },
    para_conversar: { type: 'array', items: { type: 'string' } },
    refs_genesis: { type: 'array', description: 'Pasajes de Génesis que la sección trata (C:V)', items: { type: 'string' } },
    notas_no_usadas: { type: 'string' },
  },
  required: ['id', 'titulo', 'bajada', 'entrada', 'versiculos', 'apartados', 'palabras', 'interpretaciones', 'citas', 'conexiones', 'para_vivir', 'para_conversar', 'refs_genesis', 'notas_no_usadas'],
}
const GUIA = {
  intro: 'Es un capítulo de la introducción al libro: claro, ordenado y fundado, para leer antes de empezar el plan. No lleva "para_vivir" ni "para_conversar" salvo que las notas den algo muy concreto (pueden ir vacíos).',
  parte: 'Es el panorama de una parte del libro, para leer antes de empezarla: de qué trata, cómo se ordena (con los días del plan que figuran arriba), qué temas y personajes la atraviesan y qué conviene mirar al leer. No adelantes el detalle de cada día: orientá. "para_vivir" y "para_conversar" pueden ir vacíos; "refs_genesis" puede ir vacío.',
  tema: 'Es un artículo de tema: reúne lo que Génesis enseña sobre él de punta a punta, en orden y con su desarrollo en el resto de la Biblia. Lleva "para_vivir" (2 a 4) y "para_conversar" (3 preguntas pensadas para una pareja), formulados a partir de lo que enseñan las fuentes.',
}
const escribir = a => `Vas a escribir una sección de un estudio de Génesis para un matrimonio protestante joven de Buenos Aires que lo lee juntos. Quieren entender las Escrituras a fondo y vivirlas.

Leé con UNA llamada a Read (con allow_large: true) el archivo /home/user/trabajo/insumos/libro/art_${a.id}.txt: trae el título, el alcance, el largo y la lista de las otras secciones, y después TODAS las notas extraídas de su biblioteca (comentarios de Génesis y libros de autores protestantes confiables) para esta sección, cada una con un id entre corchetes. Después devolvé la sección con la herramienta de salida estructurada (id: "${a.id}"). No uses otras herramientas.

${GUIA[a.grupo]}

Reglas de oro:
1. NO INVENTAR NADA. Cada afirmación sale de las notas y lleva en "fuentes" los ids de las notas que la respaldan (ej.: "kline_02#15", "r1_044#3"). Si varias fuentes dicen lo mismo, condensalo en una sola afirmación con todos sus ids. Nada de conocimiento propio: si un dato no está en las notas, no va.
2. CONDENSAR CON CRITERIO: no es una lista de notas sino un texto que se lee de corrido, en 3 a 7 apartados con buen orden lógico. Uní lo repetido (hay muchas notas que dicen lo mismo), priorizá lo central (importancia 3 y 2) y lo que ayuda a entender y a vivir. Explicá en "notas_no_usadas" por qué quedaron afuera las de importancia 3 que no usaste.
3. INTERPRETACIONES: cuando las fuentes difieren (por ejemplo, los días de la creación, el alcance del diluvio, la fecha de los patriarcas, Israel y el futuro), presentá cada postura con quién la sostiene, sin tomar partido salvo que todas coincidan. En el cuerpo podés resumir que hay varias lecturas y remitir a "interpretaciones".
4. TONO: castellano rioplatense neutro, cálido y claro, hablándoles a «ustedes». Explicá los términos técnicos la primera vez. Frases cortas. Nada de relleno ni de frases hechas. NO encadenes «según Kline… Livingston agrega… Grudem dice…». Nombrá al autor solo cuando aporta algo propio (una postura, una frase memorable, un dato que solo él da) o cuando las fuentes difieren; lo demás se afirma directamente y las fuentes quedan en "fuentes" (la app las muestra como etiquetas).
5. LARGO: el cuerpo (entrada + apartados) va en el rango de palabras que indica el archivo. "destacado" (opcional, en algunos apartados) es una sola oración para retener.
6. "versiculos": hasta 3 versículos de Génesis que resumen la sección (la app pone el texto RVR1960); si citás la Biblia entre comillas en el texto, que sea textual de la RVR1960 que traen las notas, o mejor parafraseá.
7. "citas": solo frases que aparecen como CITA en las notas, textuales, con su autor y obra (máximo 3, las más memorables).
8. "palabras": solo palabras hebreas que comentan las notas (la grafía hebrea solo si la nota la trae).
9. "conexiones": pasajes del resto de la Biblia que las notas relacionan con el tema, con una línea de explicación.
10. Respetá el alcance: lo que corresponde a otra sección de la lista mencionalo a lo sumo en una frase.`
const verificar = a => `Sos el verificador de un estudio bíblico que no puede contener nada inventado. Leé (con Read y allow_large: true) las notas de la sección en /home/user/trabajo/insumos/libro/art_${a.id}.txt. Más abajo está el borrador.

Revisá TODO el borrador:
1. Cada afirmación debe estar respaldada por las notas cuyos ids cita en "fuentes" (buscalos en el archivo). Corregí lo que exagere, mezcle o agregue algo que las notas no dicen; si algo no tiene respaldo, eliminalo. Si un id no existe, buscá la nota correcta o eliminá la afirmación.
2. Lo que se atribuye a un autor (en "interpretaciones", "citas" o en el texto) debe ser de ese autor según la nota. Las "citas" deben ser textuales de un campo CITA.
3. Si el texto pone palabras de la Biblia entre comillas, deben coincidir con la RVR1960; si no se puede comprobar con las notas, convertilas en paráfrasis sin comillas.
4. "palabras": comprobá la grafía hebrea con: python3 /home/user/trabajo/scripts/hebreo.py C:V (muestra las palabras hebreas del versículo con su número Strong). Corregí la grafía o dejá "hebreo" vacío si no se puede confirmar.
5. Que el castellano sea claro, que no se repitan ideas y que no se encadenen atribuciones («según X… Y agrega…»).
6. No alargues: corregí lo que haga falta pero mantené el largo.
Devolvé la sección completa y corregida con la herramienta de salida estructurada (mismo esquema, id "${a.id}"). Podés usar Read, Bash (solo para hebreo.py) y la salida estructurada.`
const res = await pipeline(
  args.articulos,
  a => agent(escribir(a), { label: `escribir:art${a.id}`, phase: 'Escribir', schema: SCHEMA }),
  (r, a) => r ? agent(`${verificar(a)}\n\nEl borrador:\n${JSON.stringify(r)}`, { label: `verificar:art${a.id}`, phase: 'Verificar', schema: SCHEMA }).then(v => ({ id: a.id, ok: !!v })) : { id: a.id, ok: false },
)
return res
