export const meta = {
  name: 'varon-continuidad-2',
  description: 'Revisa ventanas de 10 días seguidos (continuidad, repeticiones, contradicciones, doctrina y tono) con UN agente por ventana, sin verificador de IA',
  phases: [{ title: 'Revisar', detail: 'un agente por ventana de 10 días' }],
}
const HALLAZGOS = { type: 'object', properties: { hallazgos: { type: 'array', items: { type: 'object', properties: {
  dia: { type: 'integer' }, campo: { type: 'string', description: 'ruta entre corchetes del texto, p. ej. apartados[2].parrafos[1].texto' },
  tipo: { type: 'string', enum: ['continuidad', 'repeticion', 'contradiccion', 'doctrina', 'tono', 'error'] },
  problema: { type: 'string' }, texto_actual: { type: 'string', description: 'fragmento EXACTO del campo a reemplazar' },
  texto_nuevo: { type: 'string', description: 'reemplazo (vacío para borrar el fragmento)' },
}, required: ['dia', 'campo', 'tipo', 'problema', 'texto_actual', 'texto_nuevo'] } } }, required: ['hallazgos'] }
const n3 = n => String(n).padStart(3, '0')
const P = i => `Revisás varios días seguidos de «El varón según el diseño de Dios», estudio bíblico diario para un hombre cristiano protestante, escrito de «vos». Leé con UNA llamada a Read (allow_large: true) /home/user/trabajo/varon/revision/continuidad_${n3(i)}.txt (cada texto lleva entre corchetes la ruta de su campo) y devolvé los hallazgos con la salida estructurada; no uses otra herramienta. Cada día ya fue verificado contra sus fuentes: no busques errores de fuentes sino problemas que solo se ven al leerlos juntos o con ojos de pastor:
1. continuidad: un día dice que «ayer» se vio algo que el día anterior no trata, o anuncia para «mañana» algo que el siguiente no trae.
2. repeticion: la misma explicación, ilustración, historia o cita desarrollada casi igual en dos días (acortá la segunda a una referencia breve: «como viste el día N»).
3. contradiccion: dos días afirman cosas incompatibles sin aclarar que son posturas de fuentes distintas.
4. doctrina: afirmaciones que, tal como están redactadas, enseñan algo dudoso o desequilibrado (legalismo sin evangelio, gracia barata, prosperidad, culpa sin esperanza, una doctrina secundaria como única postura bíblica, Cristo ausente donde el tema lo pide).
5. tono: frases que avergüenzan o condenan sin gracia, que no le hablan de «vos», jerga sin explicar o párrafos confusos; en temas delicados (suicidio, depresión, abuso), frases ambiguas que un lector frágil pueda tomar mal.
6. error: algo que un hombre que recién empieza entendería mal, o una referencia bíblica que no dice lo que se le atribuye.
Reglas: solo cambios seguros y necesarios; la corrección usa SOLO información que ya está en estos días (sin datos, citas ni autores nuevos); "texto_actual" tiene que ser un fragmento copiado EXACTO del campo (sin la ruta ni el paréntesis inicial que agrega el archivo). Nada de cuestiones de gusto. Si no hay problemas reales, lista vacía.`
const res = await parallel(args.ventanas.map(i => () => agent(P(i), { label: `revisar:v${n3(i)}`, phase: 'Revisar', schema: HALLAZGOS, ...(args.opciones || {}) }).then(r => r ? r.hallazgos.length : -1)))
return `${res.filter(n => n >= 0).length}/${args.ventanas.length} ventanas · ${res.filter(n => n > 0).reduce((a, b) => a + b, 0)} hallazgos`
