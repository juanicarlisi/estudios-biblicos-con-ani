export const meta = {
  name: 'varon-recortar',
  description: 'Elige qué párrafos de los días demasiado largos pasan a «Para profundizar» (solo índices)',
  phases: [{ title: 'Recortar', detail: 'varios días por agente' }],
}
const SCHEMA = { type: 'object', properties: { dias: { type: 'array', items: { type: 'object', properties: {
  dia: { type: 'integer' }, mover: { type: 'array', items: { type: 'array', items: { type: 'integer' } }, description: 'pares [apartado, párrafo] que pasan a profundizar' },
}, required: ['dia', 'mover'] } } }, required: ['dias'] }
const P = k => `Editás días de un estudio bíblico de lectura diaria (20 a 30 minutos). Leé con UNA llamada a Read /home/user/trabajo/varon/recortar/grupo_${String(k).padStart(2, '0')}.txt (varios días separados por «=====»): de cada día trae sus párrafos con índice [apartado,párrafo], palabras, cantidad de fuentes y comienzo. Para cada día elegí qué párrafos pasan a «Para profundizar» (optativo) para que el cuerpo baje al menos lo que pide su encabezado. Criterio: sacá lo menos central, lo más anecdótico o repetido, ilustraciones secundarias y datos que ya otro párrafo dice mejor; conservá el hilo (la idea central, lo bíblico y la aplicación) y dejá al menos un párrafo en cada apartado y al menos 3 apartados con texto. Devolvé solo los pares con la salida estructurada; no uses otra herramienta.`
const res = await parallel(args.grupos.map(k => () => agent(P(k), { label: `recortar:grupo${String(k).padStart(2, '0')}`, phase: 'Recortar', schema: SCHEMA, ...(args.opciones || {}) }).then(r => !!r)))
return `${res.filter(Boolean).length}/${args.grupos.length} grupos`
