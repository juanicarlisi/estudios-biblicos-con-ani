export const meta = {
  name: 'genesis-clasificar-autores',
  description: 'Clasifica autor, editorial y tradición de cada libro de REFERENCIA3 para usar solo protestantes confiables',
  phases: [{ title: 'Clasificar', detail: 'un agente por lote de 30 fichas' }],
}
const SCHEMA = {
  type: 'object',
  properties: {
    libros: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'integer' },
          path: { type: 'string' },
          titulo: { type: 'string' },
          autor: { type: 'string', description: 'Tal como surge del archivo, la portada o los datos de edición; "desconocido" si no surge' },
          editorial: { type: 'string' },
          tradicion: { type: 'string', description: 'reformado, bautista, pentecostal, carismático, católico, adventista, etc.; "desconocida" si no se sabe' },
          categoria: { type: 'string', enum: ['A', 'B', 'C', 'D', 'E'] },
          razon: { type: 'string', description: 'Una oración que justifica la categoría' },
          confianza: { type: 'string', enum: ['alta', 'media', 'baja'] },
          duplicado_de: { type: 'string', description: 'path del otro archivo si es la misma obra; vacío si no' },
        },
        required: ['id', 'path', 'titulo', 'autor', 'editorial', 'tradicion', 'categoria', 'razon', 'confianza'],
      },
    },
  },
  required: ['libros'],
}
const prompt = id => `Clasificá los libros del archivo /home/user/trabajo/clasif/lotes/${id}.json (fichas con nombre de archivo, portada y datos de edición de una biblioteca cristiana) según el criterio de /home/user/trabajo/clasif/criterio.md. Leé primero el criterio y después el lote (una lectura de cada uno; no uses otras herramientas).

Para cada ficha devolvé autor, editorial, tradición, categoría (A, B, C, D o E), una razón breve y tu confianza. No inventes autores: si no surgen del nombre del archivo, la portada o los datos de edición, el autor es "desconocido" y la categoría es D, salvo que la editorial y el contenido identifiquen sin duda la obra. Usá tu conocimiento de autores y editoriales cristianas para ubicar la tradición. Ante duda entre dos categorías, elegí la más estricta. Devolvé una entrada por cada ficha del lote, en el mismo orden.`
const res = await pipeline(args.ids, id => agent(prompt(id), { label: `clasificar:${id}`, phase: 'Clasificar', schema: SCHEMA })
  .then(r => r ? { id, n: r.libros.length } : { id, n: 0, error: true }))
return res
