export const meta = {
  name: 'genesis-curar-referencias',
  description: 'En los días con demasiadas notas de referencia, elige las que más aportan al estudio de ese pasaje',
  phases: [{ title: 'Curar', detail: 'un agente por parte: elige hasta K notas de referencia' }],
}
const SCHEMA = {
  type: 'object',
  properties: {
    ids: { type: 'array', items: { type: 'string' }, description: 'Ids elegidos, tal como aparecen entre corchetes' },
    criterio: { type: 'string', description: 'Una o dos oraciones sobre qué se priorizó' },
  },
  required: ['ids', 'criterio'],
}
const prompt = t => `Estamos escribiendo el estudio de un día de Génesis para un matrimonio protestante joven (media hora de estudio). Los comentarios de Génesis ya cubren lo que figura en «LO QUE YA CUBREN LOS COMENTARIOS». Además hay muchísimas notas de libros de referencia (teologías, sermones, libros de apologética, de matrimonio, etc.) sobre este pasaje, y no entran todas.

Leé con UNA llamada a Read (allow_large: true) el archivo ${t.archivo} y devolvé con la salida estructurada los ids de HASTA ${t.K} notas de referencia que más valga la pena sumar al estudio de este día. No uses otras herramientas.

Criterios, en este orden:
1. Que hablen directamente de los versículos de este día (no del tema en general).
2. Que aporten algo que los comentarios no dicen: una explicación doctrinal clara, una respuesta a una dificultad o pregunta frecuente, una conexión con Cristo o con el Nuevo Testamento, una palabra hebrea, un dato histórico.
3. Aplicaciones concretas para la vida de fe, el matrimonio y la familia.
4. Ilustraciones o frases memorables (importancia alta).
5. Variedad: no elijas dos notas que digan lo mismo (quedate con la más clara) y no repitas muchas del mismo autor si otros dicen cosas distintas.
Si hay menos notas valiosas que ${t.K}, elegí menos.`
const res = await pipeline(args.trabajos, t => agent(prompt(t), { label: `curar:${t.id}`, phase: 'Curar', schema: SCHEMA })
  .then(r => r ? { id: t.id, dia: t.dia, n: r.ids.length } : { id: t.id, dia: t.dia, n: 0, error: true }))
return res
