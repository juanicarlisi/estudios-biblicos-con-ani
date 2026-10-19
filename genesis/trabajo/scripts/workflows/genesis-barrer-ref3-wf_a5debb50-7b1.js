export const meta = {
  name: 'genesis-barrer-ref3',
  description: 'Extrae de los libros confiables (REFERENCIA3 y comentarios del NT) lo que enseñan sobre pasajes y temas de Génesis',
  phases: [{ title: 'Barrer', detail: 'un agente por bloque de fragmentos rotulados por obra, autor y página' }],
}
const NOTA = {
  type: 'object',
  properties: {
    ref: { type: 'string', description: 'Pasaje de Génesis: "C:V", "C:V-V", "C:V-C:V" o "C"; "tema" si es transversal a Génesis sin pasaje puntual' },
    tema: { type: 'string', description: 'Tema en pocas palabras (ej.: creación, imagen de Dios, matrimonio, caída, pacto, fe de Abraham, providencia)' },
    tipo: { type: 'string', enum: ['teologia_doctrina', 'explicacion_texto', 'hebreo_palabra', 'contexto_historico', 'cultura_costumbres', 'apologetica', 'cristo_en_genesis', 'conexion_biblica', 'aplicacion_practica', 'matrimonio_familia', 'ilustracion', 'dificultad_interpretaciones', 'personaje'] },
    titulo: { type: 'string' },
    contenido: { type: 'string', description: 'Condensación fiel de lo que dice el autor (1 a 4 oraciones), sin agregar nada' },
    cita: { type: 'string', description: 'Opcional: frase textual valiosa del autor (hasta 40 palabras)' },
    autor: { type: 'string' },
    obra: { type: 'string' },
    archivo: { type: 'string', description: 'El ARCHIVO del encabezado ##### de donde sale' },
    pagina: { type: 'string', description: 'Página PDF del fragmento' },
    importancia: { type: 'integer', minimum: 1, maximum: 3 },
  },
  required: ['ref', 'tema', 'tipo', 'titulo', 'contenido', 'autor', 'obra', 'archivo', 'pagina', 'importancia'],
}
const SCHEMA = {
  type: 'object',
  properties: { bloque: { type: 'string' }, notas: { type: 'array', items: NOTA }, descartados: { type: 'integer', description: 'Cantidad aproximada de fragmentos sin aporte' } },
  required: ['bloque', 'notas', 'descartados'],
}
const prompt = id => `Estamos armando el mejor estudio de Génesis para un matrimonio protestante, condensando su biblioteca. Regla de oro: NO INVENTAR NADA.

El archivo /home/user/trabajo/segmentos/ref3/${id}.txt tiene fragmentos de libros de autores protestantes confiables. Cada fragmento empieza con un encabezado «##### OBRA | AUTOR | ARCHIVO | página». Hacé UNA sola llamada a Read con el archivo entero y el parámetro allow_large: true (así entra completo de una vez) y devolvé el resultado con la herramienta de salida estructurada; no uses otras herramientas.

Tu tarea: rescatar lo que cada autor ENSEÑA sobre un pasaje, un personaje o un tema de Génesis y que pueda enriquecer el estudio: explicación del texto, doctrina (creación, imagen de Dios, caída, pecado, pacto, elección, providencia, fe), palabras hebreas, datos históricos o culturales, respuestas apologéticas a dificultades, cómo apunta a Cristo, conexiones con el resto de la Biblia, aplicaciones a la vida (matrimonio, familia, fe, obediencia, perdón) e ilustraciones o frases memorables. Sé selectivo: descartá las menciones al pasar, las listas de citas y lo que no trata Génesis. Si un mismo autor repite una idea, una sola nota. Cada nota es una condensación fiel (1 a 4 oraciones) con el autor, la obra, el ARCHIVO y la página del encabezado. "cita" solo para una frase textual valiosa, copiada exacta. Si una postura del autor es discutida (por ejemplo, sobre los días de la creación o la historicidad de Adán), registrala tal cual con tipo "dificultad_interpretaciones" y decí que es la postura de ese autor.`
const IDS = args.ids || args.grupos.flatMap(([p, desde, hasta]) => Array.from({ length: hasta - desde + 1 }, (_, i) => `${p}_${String(desde + i).padStart(3, '0')}`))
const res = await pipeline(IDS, id => agent(prompt(id), { label: `barrer:${id}`, phase: 'Barrer', schema: SCHEMA })
  .then(r => r ? { id, n: r.notas.length, d: r.descartados } : { id, n: 0, error: true }))
return res
