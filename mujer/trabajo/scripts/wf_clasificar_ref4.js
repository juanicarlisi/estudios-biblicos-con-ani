export const meta = {
  name: 'mujer-clasificar-ref4',
  description: 'Clasifica el autor de cada libro nuevo (solo protestantes confiables entran al estudio)',
  phases: [{ title: 'Clasificar', detail: 'un lote de 25 libros por agente' }],
}
const SCHEMA = { type: 'object', properties: { libros: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'integer' }, titulo: { type: 'string' }, autor: { type: 'string' }, editorial: { type: 'string' }, tradicion: { type: 'string' },
  categoria: { type: 'string', enum: ['A', 'B', 'C', 'D', 'E'] }, razon: { type: 'string', description: 'una frase' },
}, required: ['id', 'titulo', 'autor', 'categoria', 'razon'] } } }, required: ['libros'] }
const prompt = l => `Clasificás el autor de libros cristianos en español para un estudio bíblico protestante. Leé con Read (allow_large: true) /home/user/trabajo/mujer/clasif_ref4/criterio.md (criterio de categorías A a E) y /home/user/trabajo/mujer/clasif_ref4/${l}.json (cada libro con "path" —nombre del archivo y carpeta—, "inicio" —texto de las primeras páginas— y "datos_edicion"). Devolvé UN registro por libro con la herramienta de salida estructurada. No uses otras herramientas.
Reglas: identificá autor y editorial solo con lo que aparece en el nombre del archivo, el inicio y los datos de edición; si no aparece, categoría D (no inventes). Ante la duda entre dos categorías, la más estricta, con la razón en una frase. "titulo": el título real de la obra y "autor": el nombre del autor tal como figura (sin cargos).`
const res = await parallel(args.lotes.map(l => () => agent(prompt(l), { label: `clasificar:${l}`, phase: 'Clasificar', schema: SCHEMA, ...(args.opciones || {}) }).then(r => ({ l, n: r ? r.libros.length : null }))))
return res
