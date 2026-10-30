export const meta = {
  name: 'varon-reparar',
  description: 'Corrige solo los textos marcados por verificar_dia.py (un día por agente, con su archivo de reparación)',
  phases: [{ title: 'Reparar', detail: 'solo lo marcado; sin releer el insumo entero' }],
}
const SCHEMA = { type: 'object', properties: { cambios: { type: 'array', items: { type: 'object', properties: {
  dia: { type: 'integer' }, ruta: { type: 'string' }, texto: { type: 'string', description: 'texto corregido; vacío para borrar el párrafo' }, fuentes: { type: 'array', items: { type: 'string' } },
}, required: ['dia', 'ruta', 'texto', 'fuentes'] } } }, required: ['cambios'] }
const n3 = d => String(d).padStart(3, '0')
const P = d => `Corregís un día de un estudio bíblico que no puede contener nada inventado. Leé con UNA llamada a Read (allow_large: true) /home/user/trabajo/varon/reparar/dia_${n3(d)}.txt: trae cada texto marcado por un programa, sus problemas, las notas que cita y, si hace falta, el texto RVR1960. Para cada ruta devolvé el texto corregido con la salida estructurada (no uses otra herramienta).
Reglas: usá SOLO lo que dicen las notas y la RVR1960 del archivo; mantené la voz de «vos» y el largo parecido; si una cifra, una frase entre «» o una atribución a un autor no está en las notas citadas, sacala o reformulala sin ella (o poné la fuente correcta si figura en otra nota listada); las frases bíblicas entre «» deben ser literales de la RVR1960 del archivo; si el párrafo no tiene respaldo en nada, devolvé texto vacío para borrarlo. No cambies lo que no está marcado. "fuentes": los ids que respaldan el texto corregido.`
const PG = k => P(0).replace(`/home/user/trabajo/varon/reparar/dia_000.txt`, `/home/user/trabajo/varon/reparar/grupo_${String(k).padStart(2, '0')}.txt`).replace('un día de un estudio bíblico', 'varios días de un estudio bíblico (separados por «=====»)').replace('Para cada ruta devolvé', 'Para cada ruta de cada día devolvé (con el número de "dia")')
if (args.grupos) {
  const rg = await parallel(args.grupos.map(k => () => agent(PG(k), { label: `reparar:grupo${String(k).padStart(2, '0')}`, phase: 'Reparar', schema: SCHEMA, ...(args.opciones || {}) }).then(r => !!r)))
  return `${rg.filter(Boolean).length}/${args.grupos.length} grupos reparados`
}
const res = await parallel((args.dias || []).map(d => () => agent(P(d), { label: `reparar:dia${n3(d)}`, phase: 'Reparar', schema: SCHEMA, ...(args.opciones || {}) }).then(r => !!r)))
return `${res.filter(Boolean).length}/${args.dias.length} reparados`
