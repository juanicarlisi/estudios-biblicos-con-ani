export const meta = {
  name: 'varon-revisar-plan-2',
  description: 'Segunda ronda del plan del varón: resuelve las superposiciones marcadas, reparte las lecturas sin repetir y fortalece la parte del varón adulto',
  phases: [
    { title: 'Proponer', detail: 'un agente por superposición marcada, uno para las lecturas y uno para el varón adulto' },
    { title: 'Verificar', detail: 'dos escépticos: uno para los cambios de días y grupos, otro para las lecturas' },
  ],
}
const OP = {
  tipo: { type: 'string', enum: ['mover_grupos', 'fusionar', 'nuevo_dia', 'retitular', 'enfoque', 'lectura'] },
  dias: { type: 'array', items: { type: 'integer' } },
  grupos: { type: 'array', items: { type: 'string' } },
  destino: { type: 'integer' },
  parte: { type: 'string', description: 'nuevo_dia: la letra de la parte' },
  despues_de: { type: 'integer', description: 'nuevo_dia: el día detrás del cual va' },
  titulo_nuevo: { type: 'string' }, objetivo_nuevo: { type: 'string' }, contenido_nuevo: { type: 'string' }, lectura_nueva: { type: 'string' },
  enfoque: { type: 'string', description: 'enfoque: instrucción para quien escriba el día, para que no repita el otro día' },
  problema: { type: 'string' }, propuesta: { type: 'string' },
}
const REQ = ['tipo', 'dias', 'grupos', 'destino', 'parte', 'despues_de', 'titulo_nuevo', 'objetivo_nuevo', 'contenido_nuevo', 'lectura_nueva', 'enfoque', 'problema', 'propuesta']
const PROPUESTAS = { type: 'object', properties: { propuestas: { type: 'array', items: { type: 'object', properties: OP, required: REQ } } }, required: ['propuestas'] }
const VEREDICTOS = { type: 'object', properties: { veredictos: { type: 'array', items: { type: 'object', properties: {
  indice: { type: 'integer' }, aceptar: { type: 'boolean' }, motivo: { type: 'string' },
  corregida: { type: 'object', properties: OP, required: REQ, description: 'la propuesta completa tal como se aplica (corregida si hace falta; si no, la original)' },
}, required: ['indice', 'aceptar', 'motivo', 'corregida'] } } }, required: ['veredictos'] }
const BASE = `Sos editor de «El varón según el diseño de Dios», un estudio bíblico diario (20 a 30 minutos por día) para un hombre cristiano protestante. Sale todo de libros de autores protestantes confiables: las notas se agruparon por tema (grupos con clave, p. ej. «G_03.12») y cada día reúne varios grupos. El plan tiene 512 días en 17 partes (A crisis, B diseño, C Dios, D carácter, E pureza, F trabajo, G esposo, H padre, I líder y ministro, J siervo, K hermandad, L joven, M adulto, N mayor, O sociedad, P pruebas, Q varones de la Biblia y la historia). Ya pasó una primera revisión.
Archivos (leelos con Read, allow_large: true, o buscá con Grep):
- /home/user/trabajo/varon/plan/revision/plan_corto.txt: el plan entero (título, objetivo, notas y lectura de cada día).
- /home/user/trabajo/varon/plan/revision/parte_<letra>.txt: el detalle de cada parte, con los grupos de cada día y su resumen.
- /home/user/trabajo/varon/plan/revision/lecturas.txt: cada día con su lectura y los pasajes que más citan sus notas.

Operaciones posibles (completá todos los campos; los que no correspondan, vacíos o 0; números de día y claves EXACTOS del plan actual):
- mover_grupos: "dias" = [origen], "grupos", "destino" (y "objetivo_nuevo"/"contenido_nuevo" del destino si cambia su foco).
- fusionar: "dias" = [el que queda, el que se une], con "titulo_nuevo", "objetivo_nuevo", "contenido_nuevo" y "lectura_nueva".
- nuevo_dia: "parte", "despues_de" (un día de esa parte), "grupos" que se mudan de otros días, con "titulo_nuevo", "objetivo_nuevo", "contenido_nuevo" y "lectura_nueva".
- retitular: "dias" = [el día], "titulo_nuevo" y, si hace falta, "objetivo_nuevo".
- enfoque: "dias" = [el día], "enfoque" = qué ángulo propio tiene que tomar ese día y qué NO repetir del otro (nombrá el otro día por su número), cuando un tema vuelve legítimamente en dos partes.
- lectura: "dias" = [el día], "lectura_nueva".
Un día queda con 25 a 90 notas. No se inventa material: solo se mueve, se une o se orienta lo que hay.`
const NOTA = k => `${BASE}

Un revisor marcó un problema y el verificador lo dio por real. Está en /home/user/trabajo/varon/plan/revision/notas_r2.json, en la posición ${k} de la lista (contando desde 0): campos "texto" (el problema), "motivo_verificador" y "mapa_v1_v2". OJO: los números de día del texto son del plan ANTERIOR; usá "mapa_v1_v2" para pasarlos al plan actual (null = ese día ya no existe porque se unió o se vació).

Revisá en los archivos si el problema sigue en el plan actual y proponé la solución concreta: unir días que enseñan lo mismo, mover grupos al día que mejor los recibe o, si el tema vuelve con razón en dos partes, darle a cada día su "enfoque" propio para que no se repita. No cambies lecturas (de eso se ocupa otro editor). Si ya está resuelto, devolvé la lista vacía. Usá solo Read, Grep y la salida estructurada.`
const LECTURAS = `${BASE}

Tu tarea: las LECTURAS. Hoy 68 pasajes se leen en más de un día, y otros se superponen en parte (p. ej. Salmos 39:1-13 y Salmo 39:1-13, o un capítulo y una parte de ese capítulo). El lector tiene que leer, en lo posible, un pasaje distinto cada día.
1. Detectá en lecturas.txt todas las lecturas repetidas o superpuestas (normalizá los nombres de los libros).
2. En cada caso, dejá la lectura en el día donde es más central y dale a los otros días otra lectura que sostenga su tema, elegida entre los pasajes que citan sus notas (última columna) o un pasaje vecino del mismo libro que trate lo mismo. Entre 8 y 30 versículos, con el nombre castellano completo del libro («1 Timoteo 3:1-7», «Salmos 101:1-8»), capítulo y versículos. Que la nueva lectura no esté ya en otro día.
3. Si un pasaje es el centro inevitable de dos días (por ejemplo, Efesios 5 para el esposo y para el diseño), podés partirlo (5:22-24 / 5:25-33) en vez de repetirlo.
Devolvé una propuesta de tipo "lectura" por cada día que cambia. Usá solo Read, Grep y la salida estructurada.`
const ADULTO = `${BASE}

Tu tarea: la PARTE M (el varón adulto). El fundador la pidió expresamente, pero quedó con solo 6 días. Buscá con Grep en TODOS los parte_<letra>.txt los grupos que tratan de lleno lo propio del varón adulto o de la mitad de la vida: la madurez, la crisis de la mitad de la vida, el cansancio y la rutina de los años del medio, las responsabilidades que se acumulan (trabajo, esposa, hijos adolescentes, padres que envejecen), el éxito y el fracaso a los 40 o 50, las decisiones que definen el resto de la vida, perseverar, terminar bien, el legado. Proponé:
- mover a días de la parte M los grupos que hoy están en otras partes y encajan claramente mejor ahí (sin dejar a su día de origen con menos de 25 notas), y
- si el material alcanza, días nuevos ("nuevo_dia") en la parte M con esos grupos.
No saques de su lugar lo que es propio de otra parte (la paternidad en general sigue en H, el trabajo en general en F). Usá solo Read, Grep y la salida estructurada.`
const VERIF = (que, ps) => `${BASE}

Otros editores hicieron estas propuestas (${que}). Juzgá cada una con escepticismo: ¿el problema es real en el plan actual?, ¿la solución mejora el estudio sin perder material?, ¿los días y las claves existen y están donde dicen?, ¿los días quedan entre 25 y 90 notas? ${que === 'lecturas' ? 'En las lecturas: ¿la nueva sostiene el tema del día?, ¿tiene entre 8 y 30 versículos?, ¿no se repite con otra lectura del plan (contando las demás propuestas)?' : 'Si dos propuestas chocan (tocan el mismo día o los mismos grupos), aceptá solo la mejor; un "enfoque" no choca con nada.'} Si es buena pero mal planteada, aceptala y corregila en "corregida". Por defecto, si dudás, no la aceptes.

Propuestas (el índice es su posición):
${ps.map((p, k) => `[${k}] ${JSON.stringify(p)}`).join('\n')}

Devolvé un veredicto por propuesta, con la propuesta completa en "corregida". Usá solo Read, Grep y la salida estructurada.`
const VLOTE = n => {
  const que = n === 'estructura' ? 'cambios de días y grupos' : n === 'lecturas' ? 'lecturas' : 'enfoques'
  const extra = que === 'lecturas'
    ? 'En las lecturas: ¿la nueva sostiene el tema del día (mirá en lecturas.txt los pasajes que citan sus notas)?, ¿tiene entre 8 y 30 versículos y el nombre castellano completo del libro?, ¿no se repite ni se superpone con otra lectura del plan, contando las demás propuestas de este lote?'
    : que === 'enfoques'
    ? 'En los enfoques: ¿la instrucción es coherente con los grupos del día (miralos en parte_<letra>.txt)?, ¿de verdad evita repetir el otro día?, ¿no choca con el enfoque que se le da al otro día (que ninguno de los dos quede sin tratar lo que le toca)?, ¿es clara para quien escriba?'
    : 'Si dos propuestas chocan (tocan el mismo día o los mismos grupos), aceptá solo la mejor.'
  return `${BASE}

Otros editores hicieron propuestas (${que}). Están en /home/user/trabajo/varon/plan/revision/r2_lote_${n}.json (una lista; el índice es la posición, contando desde 0). Juzgá cada una con escepticismo: ¿el problema es real en el plan actual?, ¿la solución mejora el estudio sin perder material?, ¿los días y las claves existen y están donde dicen?, ¿los días quedan entre 25 y 90 notas? ${extra} Si es buena pero mal planteada, aceptala y corregila en "corregida". Por defecto, si dudás, no la aceptes.

Devolvé un veredicto por propuesta, con la propuesta completa en "corregida". Usá solo Read, Grep y la salida estructurada.`
}
if (args.modo === 'verificar_lotes') {
  phase('Verificar')
  const vs = await parallel(args.lotes.map(n => () => agent(VLOTE(n), { label: `verificar:${n}`, phase: 'Verificar', schema: VEREDICTOS })))
  return vs.map((v, k) => ({ lote: args.lotes[k], n: v ? v.veredictos.length : null }))
}
if (args.modo === 'verificar') {
  phase('Verificar')
  const [vo, vl] = await Promise.all([
    args.ops.length ? agent(VERIF('cambios de días y grupos', args.ops), { label: 'verificar:ops', phase: 'Verificar', schema: VEREDICTOS }) : null,
    args.lects.length ? agent(VERIF('lecturas', args.lects), { label: 'verificar:lecturas', phase: 'Verificar', schema: VEREDICTOS }) : null,
  ])
  return { vo: vo ? vo.veredictos : null, vl: vl ? vl.veredictos : null }
}
phase('Proponer')
const tareas = [
  ...(args.notas || []).map(k => () => agent(NOTA(k), { label: `resolver:${String(k).padStart(2, '0')}`, phase: 'Proponer', schema: PROPUESTAS })),
  ...(args.lecturas ? [() => agent(LECTURAS, { label: 'lecturas', phase: 'Proponer', schema: PROPUESTAS })] : []),
  ...(args.adulto ? [() => agent(ADULTO, { label: 'adulto', phase: 'Proponer', schema: PROPUESTAS })] : []),
]
const rs = await parallel(tareas)
return rs.map(r => r ? r.propuestas.length : null)
