export const meta = {
  name: 'varon-revisar-plan',
  description: 'Revisa el plan completo de días del estudio del varón (superposiciones, orden, huecos) y verifica cada propuesta',
  phases: [
    { title: 'Revisar', detail: 'tres lectores con miradas distintas sobre el plan entero' },
    { title: 'Verificar', detail: 'un escéptico juzga cada propuesta' },
  ],
}
const PROPUESTAS = { type: 'object', properties: { propuestas: { type: 'array', items: { type: 'object', properties: {
  tipo: { type: 'string', enum: ['fusionar', 'mover', 'reordenar', 'retitular', 'separar', 'hueco'] },
  dias: { type: 'array', items: { type: 'integer' }, description: 'los días afectados' },
  problema: { type: 'string' },
  propuesta: { type: 'string', description: 'qué hacer exactamente (p. ej. «pasar el grupo G_03.12 del día 140 al 152», «unir los días 88 y 91 en uno»)' },
  grupos: { type: 'array', items: { type: 'string' }, description: 'claves de grupos que se mueven, si corresponde' },
  titulo_nuevo: { type: 'string' },
}, required: ['tipo', 'dias', 'problema', 'propuesta'] } } }, required: ['propuestas'] }
const VEREDICTOS = { type: 'object', properties: { veredictos: { type: 'array', items: { type: 'object', properties: {
  indice: { type: 'integer' }, aceptar: { type: 'boolean' }, ajuste: { type: 'string', description: 'cómo aplicarla, corregida si hace falta' }, motivo: { type: 'string' },
}, required: ['indice', 'aceptar', 'ajuste', 'motivo'] } } }, required: ['veredictos'] }
const BASE = `Sos editor de «El varón según el diseño de Dios», un estudio bíblico diario (20 a 30 minutos por día) para un hombre cristiano protestante. El fundador pidió como mínimo: una introducción exhaustiva sobre la condición actual del hombre; el hombre en su relación con Dios; como trabajador, esposo, padre, ministro y siervo; el hombre joven, adulto y adulto mayor; el hombre en la sociedad; y todo lo demás que dé el material. El estudio termina cuando se agota el material de los libros.
Leé con Read (allow_large: true) /home/user/trabajo/varon/plan/revision_plan.txt: el plan entero, parte por parte. Cada día trae título, objetivo, qué cubre, lectura y sus grupos de notas (clave: tema, con la cantidad de notas).`
const MIRADAS = [
  ['superposicion', 'Buscá SUPERPOSICIONES: dos días (de la misma parte o de partes distintas) que enseñan lo mismo, o grupos de notas que tratan lo mismo repartidos en días distintos. Proponé fusionar los días o mover los grupos al día que mejor les corresponde. Tené en cuenta que un tema puede aparecer en dos partes con enfoques distintos (p. ej. la pureza del joven soltero y la fidelidad del esposo): eso no es superposición.'],
  ['orden', 'Revisá el ORDEN y la PROGRESIÓN dentro de cada parte: ¿va de los fundamentos a la práctica?, ¿el primer día presenta la parte y el último la cierra?, ¿hay saltos o días fuera de lugar? Revisá también si algún día amontona temas distintos (proponé separarlo) o es demasiado flaco para 20 minutos (proponé unirlo con el vecino).'],
  ['huecos', 'Buscá HUECOS frente a lo que pidió el fundador y a lo que trae el material: temas del pedido que no tienen días suficientes, días de una parte que en realidad pertenecen a otra, y títulos poco claros o engañosos (proponé uno nuevo). No pidas temas que el material no trae: el estudio no inventa.'],
]
const revisar = m => `${BASE}\n\nTu mirada: ${m[1]}\n\nSé exigente pero concreto: solo propuestas que mejoren de verdad el estudio, con los números de día y las claves de grupo exactos. Si no encontrás nada, devolvé la lista vacía. Usá solo Read y la salida estructurada.`
const verificar = ps => `${BASE}\n\nOtros editores hicieron estas propuestas. Juzgá cada una con escepticismo: ¿el problema es real?, ¿la propuesta mejora el estudio sin perder material?, ¿los días y las claves existen? Si dos propuestas chocan, aceptá la mejor. Si es buena pero mal planteada, corregila en "ajuste". Por defecto, si dudás, no la aceptes.\n\nPropuestas (el índice es su posición):\n${ps.map((p, k) => `[${k}] ${p.tipo} · días ${p.dias.join(', ')}${p.grupos && p.grupos.length ? ' · grupos ' + p.grupos.join(', ') : ''}\n  problema: ${p.problema}\n  propuesta: ${p.propuesta}${p.titulo_nuevo ? '\n  título nuevo: ' + p.titulo_nuevo : ''}`).join('\n\n')}\n\nDevolvé un veredicto por propuesta. Usá solo Read y la salida estructurada.`
phase('Revisar')
const rs = await parallel(MIRADAS.map(m => () => agent(revisar(m), { label: `revisar:${m[0]}`, phase: 'Revisar', schema: PROPUESTAS })))
const todas = rs.filter(Boolean).flatMap((r, k) => r.propuestas.map(p => ({ ...p, mirada: MIRADAS[k][0] })))
log(`${todas.length} propuestas`)
if (!todas.length) return { propuestas: [], veredictos: [] }
phase('Verificar')
const v = await agent(verificar(todas), { label: 'verificar:plan', phase: 'Verificar', schema: VEREDICTOS })
return { propuestas: todas, veredictos: v ? v.veredictos : null }
