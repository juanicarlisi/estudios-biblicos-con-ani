export const meta = {
  name: 'varon-revisar-plan',
  description: 'Revisa el plan de días del estudio del varón (orden y forma de cada parte; superposiciones y huecos del conjunto) y verifica cada propuesta',
  phases: [
    { title: 'Revisar', detail: 'un editor por parte y dos miradas sobre el plan entero' },
    { title: 'Verificar', detail: 'un escéptico juzga las propuestas de cada parte y las del conjunto' },
  ],
}
const OP = {
  tipo: { type: 'string', enum: ['mover_grupos', 'fusionar', 'separar', 'reordenar', 'retitular', 'nota'] },
  dias: { type: 'array', items: { type: 'integer' }, description: 'mover_grupos: el día de origen; fusionar: los días a unir (el primero queda); separar/retitular: el día; reordenar: vacío; nota: los días afectados' },
  grupos: { type: 'array', items: { type: 'string' }, description: 'mover_grupos y separar: las claves de grupo exactas que se mueven' },
  destino: { type: 'integer', description: 'mover_grupos: el día que recibe los grupos (0 si no corresponde)' },
  orden_nuevo: { type: 'array', items: { type: 'integer' }, description: 'reordenar: TODOS los días de la parte, en el orden nuevo' },
  titulo_nuevo: { type: 'string' }, objetivo_nuevo: { type: 'string' }, contenido_nuevo: { type: 'string' }, lectura_nueva: { type: 'string' },
  problema: { type: 'string' }, propuesta: { type: 'string', description: 'la propuesta explicada en una o dos oraciones' },
}
const PROPUESTAS = { type: 'object', properties: { propuestas: { type: 'array', items: { type: 'object', properties: OP,
  required: ['tipo', 'dias', 'grupos', 'destino', 'orden_nuevo', 'titulo_nuevo', 'objetivo_nuevo', 'contenido_nuevo', 'lectura_nueva', 'problema', 'propuesta'] } } }, required: ['propuestas'] }
const VEREDICTOS = { type: 'object', properties: { veredictos: { type: 'array', items: { type: 'object', properties: {
  indice: { type: 'integer' }, aceptar: { type: 'boolean' }, motivo: { type: 'string' },
  corregida: { type: 'object', properties: OP, description: 'si la aceptás con cambios, la propuesta completa ya corregida; si no, repetí la original' },
}, required: ['indice', 'aceptar', 'motivo', 'corregida'] } } }, required: ['veredictos'] }
const BASE = `Sos editor de «El varón según el diseño de Dios», un estudio bíblico diario (20 a 30 minutos por día, unas 2.000 a 2.500 palabras) para un hombre cristiano protestante de Buenos Aires. Sale todo de libros de autores protestantes confiables: las notas de cada libro se agruparon por tema (grupos con clave, p. ej. «G_03.12») y cada día reúne varios grupos. El fundador pidió como mínimo: una introducción exhaustiva sobre la condición actual del hombre; el hombre en su relación con Dios; como trabajador, esposo, padre, ministro y siervo; el hombre joven, adulto y adulto mayor; el hombre en la sociedad; y todo lo que dé el material. El estudio termina cuando se agota el material: no se agregan temas que los libros no traen.
El plan entero, corto (título, objetivo, cantidad de notas y lectura de cada día), está en /home/user/trabajo/varon/plan/revision/plan_corto.txt. El detalle de cada parte, con los grupos de cada día, está en /home/user/trabajo/varon/plan/revision/parte_<letra>.txt (A a Q).

Formato de cada propuesta (completá todos los campos; los que no correspondan, vacíos o 0):
- mover_grupos: "dias" = [día de origen], "grupos" = claves exactas, "destino" = día que los recibe. Si el día de origen o el de destino cambia de foco, poné "objetivo_nuevo"/"contenido_nuevo" del DESTINO.
- fusionar: "dias" = [el día que queda, el que se une], con "titulo_nuevo", "objetivo_nuevo", "contenido_nuevo" y "lectura_nueva" del día que resulta.
- separar: "dias" = [el día], "grupos" = los que pasan a un día nuevo inmediatamente después, con "titulo_nuevo", "objetivo_nuevo", "contenido_nuevo" y "lectura_nueva" del día nuevo.
- reordenar: "orden_nuevo" = TODOS los días de la parte en el nuevo orden.
- retitular: "dias" = [el día], "titulo_nuevo" (y "objetivo_nuevo" si hace falta).
- nota: un problema que no se resuelve moviendo grupos (se informa al fundador).
Un día tiene que quedar con unas 25 a 80 notas: no fusiones si pasa de 90 ni separes si queda debajo de 20. Copiá las claves y los números de día exactos del plan.`
const PARTE = s => `${BASE}

Te toca revisar a fondo la PARTE ${s}. Leé con Read (allow_large: true) /home/user/trabajo/varon/plan/revision/parte_${s}.txt y, para ubicarte en el conjunto, /home/user/trabajo/varon/plan/revision/plan_corto.txt.
Buscá:
1. ORDEN Y PROGRESIÓN: ¿va de los fundamentos a la práctica, con una línea clara?, ¿el primer día presenta la parte y el último la cierra?, ¿hay días fuera de lugar? (reordenar)
2. FORMA DE CADA DÍA: un día que amontona temas que no tienen que ver (separar), uno flaco para 20 minutos o dos días que enseñan casi lo mismo (fusionar), grupos que encajan claramente mejor en otro día de la parte (mover_grupos).
3. TÍTULOS Y LECTURAS: títulos poco claros o que prometen otra cosa; lecturas que no sostienen el tema o que se repiten (retitular, con "lectura_nueva" si hace falta).
Sé exigente pero concreto: solo cambios que mejoren de verdad el estudio. Si la parte está bien, devolvé la lista vacía. Usá solo Read, Grep y la salida estructurada.`
const MIRADAS = {
  superposicion: `Mirá el CONJUNTO y buscá SUPERPOSICIONES entre partes: días de partes distintas que enseñan lo mismo con el mismo enfoque, o grupos que tratan lo mismo repartidos en partes distintas sin necesidad. Proponé mover los grupos al día que mejor les corresponde o fusionar días. Un tema puede volver en dos partes con enfoques distintos (p. ej. la pureza del joven soltero y la fidelidad del esposo; Dios como Padre en la relación con Dios y como modelo del padre): eso no es superposición. Para ver los grupos de un día, buscalo con Grep en los archivos parte_<letra>.txt.`,
  huecos: `Mirá el CONJUNTO frente a lo que pidió el fundador: ¿cada tema del pedido tiene su lugar y su peso?, ¿la introducción sobre la crisis es exhaustiva?, ¿hay días que en realidad pertenecen a otra parte (mover_grupos o fusionar)?, ¿hay títulos engañosos (retitular)? Si un tema del pedido queda flaco porque el material no da más, informalo como "nota" (no se inventa material). Para ver los grupos de un día, buscalo con Grep en los archivos parte_<letra>.txt.`,
}
const GLOBAL = m => `${BASE}\n\n${MIRADAS[m]}\n\nLeé con Read (allow_large: true) /home/user/trabajo/varon/plan/revision/plan_corto.txt. Sé exigente pero concreto: solo propuestas que mejoren de verdad el estudio. Si no encontrás nada, devolvé la lista vacía. Usá solo Read, Grep y la salida estructurada.`
const verificar = (que, ps) => `${BASE}\n\nOtros editores hicieron estas propuestas sobre ${que}. Leé lo que necesites (plan_corto.txt y los parte_<letra>.txt) y juzgá cada una con escepticismo: ¿el problema es real?, ¿la propuesta mejora el estudio sin perder material?, ¿los días y las claves existen y están donde dice?, ¿respeta el tamaño de los días (25 a 80 notas)? Si dos propuestas chocan (tocan el mismo día o los mismos grupos), aceptá solo la mejor. Si es buena pero mal planteada, aceptala y corregila en "corregida". Por defecto, si dudás, no la aceptes.\n\nPropuestas (el índice es su posición):\n${ps.map((p, k) => `[${k}] ${JSON.stringify(p)}`).join('\n')}\n\nDevolvé un veredicto por propuesta. Usá solo Read, Grep y la salida estructurada.`
const items = args.items
const res = await pipeline(
  items,
  it => it === 'global'
    ? parallel(Object.keys(MIRADAS).map(m => () => agent(GLOBAL(m), { label: `revisar:${m}`, phase: 'Revisar', schema: PROPUESTAS })))
        .then(rs => rs.filter(Boolean).flatMap(r => r.propuestas))
    : agent(PARTE(it), { label: `revisar:parte_${it}`, phase: 'Revisar', schema: PROPUESTAS }).then(r => r ? r.propuestas : []),
  (ps, it) => !ps.length ? { item: it, propuestas: [], veredictos: [] }
    : agent(verificar(it === 'global' ? 'el conjunto del plan' : `la parte ${it}`, ps), { label: `verificar:${it}`, phase: 'Verificar', schema: VEREDICTOS })
        .then(v => ({ item: it, propuestas: ps, veredictos: v ? v.veredictos : null })),
)
return res
