export const meta = {
  name: 'genesis-extraer-v2',
  description: 'Extrae (en una sola pasada y con salida estructurada) lo sustancial de cada bloque de comentario de Génesis',
  phases: [{ title: 'Extraer', detail: 'un agente por bloque: una lectura completa y notas estructuradas con referencia y página' }],
}

const NOTA = {
  type: 'object',
  properties: {
    ref: { type: 'string', description: 'Pasaje de Génesis: "C:V", "C:V-V", "C:V-C:V", "C", o "intro" (libro entero) o "tema" (transversal)' },
    tipo: { type: 'string', enum: ['contexto_historico', 'cultura_costumbres', 'arqueologia_geografia', 'hebreo_palabra', 'explicacion_texto', 'teologia_doctrina', 'cristo_en_genesis', 'conexion_biblica', 'aplicacion_practica', 'ilustracion', 'dificultad_interpretaciones', 'estructura_bosquejo', 'cronologia_fechas', 'personaje', 'pregunta_reflexion'] },
    titulo: { type: 'string' },
    contenido: { type: 'string', description: 'Condensación fiel de lo que dice el autor, 2 a 6 oraciones (más si es bosquejo o tabla)' },
    cita: { type: 'string', description: 'Opcional: frase textual del autor (hasta 50 palabras)' },
    refs_biblicas: { type: 'array', items: { type: 'string' } },
    hebreo: { type: 'object', properties: { palabra: { type: 'string' }, transliteracion: { type: 'string' }, significado: { type: 'string' } } },
    postura: { type: 'string', description: 'Opcional: interpretaciones que presenta el autor y cuál prefiere' },
    pagina: { type: 'string', description: 'Rótulo de página del encabezado === [...] === (y [Page N] en Mundo Hispano)' },
    importancia: { type: 'integer', minimum: 1, maximum: 3 },
  },
  required: ['ref', 'tipo', 'titulo', 'contenido', 'pagina', 'importancia'],
}
const SCHEMA = {
  type: 'object',
  properties: {
    bloque: { type: 'string' },
    notas: { type: 'array', items: NOTA },
    problemas: { type: 'string', description: 'Páginas ilegibles, cortes, errores de OCR corregidos, etc. Vacío si no hubo.' },
  },
  required: ['bloque', 'notas', 'problemas'],
}

function prompt(c) {
  return `Estamos construyendo el mejor estudio posible de Génesis para un matrimonio protestante que lo va a leer 20 versículos por día. Regla de oro: NO INVENTAR NADA; todo sale de los libros de su biblioteca.

Tu tarea: leer COMPLETO el archivo ${c.archivo} (bloque ${c.id}, páginas ${c.paginas} de: ${c.descripcion}) y devolver TODO aporte sustancial del autor como notas ordenadas por el pasaje de Génesis que comenta.

Cómo trabajar (para ahorrar): hacé UNA sola llamada a Read con el archivo entero (sin offset ni limit; si el resultado viniera truncado, recién ahí leé el resto) y después devolvé el resultado con la herramienta de salida estructurada. No escribas archivos ni uses otras herramientas.

Qué incluir: explicación del texto versículo por versículo, contexto histórico y cultural, costumbres, arqueología, geografía, palabras hebreas, cronología y fechas, teología y doctrina, cómo apunta a Cristo, conexiones con el resto de la Biblia, dificultades e interpretaciones (con la postura del autor), bosquejos y estructura, tablas, aplicaciones prácticas, ilustraciones y preguntas. Qué NO incluir: datos editoriales, abreviaturas, índices, bibliografías.

Ser exhaustivo es lo más importante: recorré todas las páginas; si dudás si algo es sustancial, incluilo con importancia 1. Cada nota es una condensación fiel (conservá matices, nombres, números, fechas y argumentos), sin nada que el autor no diga. "cita" solo para una frase textual valiosa (hasta 50 palabras), copiada exacta. Si el texto viene de OCR, corregí errores evidentes sin cambiar el sentido y anotalo en "problemas". "pagina": el rótulo del encabezado === [...] === de la página donde está el contenido (en Mundo Hispano agregá el [Page N] más cercano). Usá "intro" para lo que trata el libro entero y "tema" para lo transversal sin pasaje puntual.`
}

const DESC = {
  kline: 'Meredith G. Kline, «Génesis», en Nuevo Comentario Bíblico (Guthrie, Motyer y otros; Casa Bautista)',
  beacon: 'George Herbert Livingston, «Génesis», Comentario Bíblico Beacon, tomo 1 (CNP)',
  cbmh: 'Comentario Bíblico Mundo Hispano, tomo 1: Génesis (Editorial Mundo Hispano)',
  edersheim: 'Alfred Edersheim, Comentario Bíblico Histórico: Génesis (Clie)',
  macarthur: 'John MacArthur, Biblia de Estudio MacArthur (Portavoz): introducción y notas de Génesis',
  dbmh: 'Diccionario Bíblico Mundo Hispano (Editorial Mundo Hispano), páginas que citan Génesis; las citas vienen codificadas <01CCVV> = Génesis CC:VV. Extraer SOLO lo que aporta a entender Génesis (personas, lugares, costumbres, palabras y temas de Génesis) e ignorar lo ajeno a Génesis',
}
const CHUNKS = args.chunks || args.ids.map(id => ({
  id,
  archivo: `/home/user/trabajo/segmentos/biblio/${id}.txt`,
  descripcion: DESC[id.split('_')[0]],
  paginas: 'las que indican los encabezados',
}))

const out = await pipeline(
  CHUNKS,
  c => agent(prompt(c), { label: `extraer:${c.id}`, phase: 'Extraer', schema: SCHEMA })
    .then(r => r ? { id: c.id, n: r.notas.length, problemas: (r.problemas || '').slice(0, 300) } : { id: c.id, n: 0, error: true }),
)
return out
