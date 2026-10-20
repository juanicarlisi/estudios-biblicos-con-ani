export const meta = {
  name: 'varon-revisar-continuidad',
  description: 'Revisa ventanas de días seguidos del estudio del varón (continuidad, repeticiones, contradicciones, doctrina y tono) y verifica cada hallazgo',
  phases: [
    { title: 'Revisar', detail: 'dos miradas por ventana de 6 días' },
    { title: 'Verificar', detail: 'un escéptico por ventana descarta lo que no es un problema real' },
  ],
}
const HALLAZGOS = { type: 'object', properties: { hallazgos: { type: 'array', items: { type: 'object', properties: {
  dia: { type: 'integer' }, campo: { type: 'string', description: 'la ruta entre corchetes que trae el texto, p. ej. apartados[2].parrafos[1].texto' },
  tipo: { type: 'string', enum: ['continuidad', 'repeticion', 'contradiccion', 'doctrina', 'tono', 'error'] },
  problema: { type: 'string' }, texto_actual: { type: 'string', description: 'fragmento EXACTO del campo a reemplazar (sin la ruta ni lo que va entre paréntesis al principio)' },
  texto_nuevo: { type: 'string', description: 'reemplazo del fragmento (vacío para borrarlo)' }, justificacion: { type: 'string' },
}, required: ['dia', 'campo', 'tipo', 'problema', 'texto_actual', 'texto_nuevo', 'justificacion'] } } }, required: ['hallazgos'] }
const VEREDICTOS = { type: 'object', properties: { veredictos: { type: 'array', items: { type: 'object', properties: {
  indice: { type: 'integer' }, real: { type: 'boolean' }, texto_nuevo: { type: 'string', description: 'el reemplazo, corregido si hace falta' }, motivo: { type: 'string' },
}, required: ['indice', 'real', 'texto_nuevo', 'motivo'] } } }, required: ['veredictos'] }
const n3 = n => String(n).padStart(3, '0')
const BASE = i => `Revisás «El varón según el diseño de Dios», un estudio bíblico diario (20 a 30 minutos por día) para un hombre cristiano protestante, escrito de «vos». Leé con UNA llamada a Read (allow_large: true) /home/user/trabajo/varon/revision/continuidad_${n3(i)}.txt: trae varios días seguidos; cada texto lleva entre corchetes la ruta de su campo. Cada día ya fue verificado contra sus fuentes (libros de autores protestantes confiables): no busques errores de fuentes sino problemas que solo se ven leyendo los días juntos o con ojos de pastor.`
const MIRADAS = {
  continuidad: `Buscá:
1. continuidad: un día dice que «ayer» o «el día anterior» se vio algo que el día anterior no trata, o anuncia para mañana algo que el día siguiente no trae.
2. repeticion: la misma explicación, ilustración, historia o cita desarrollada casi igual en dos días (proponé acortar la segunda a una referencia breve, p. ej. «como viste el día N…»).
3. contradiccion: dos días afirman cosas incompatibles sin aclarar que son posturas de fuentes distintas.
4. error: un dato bíblico que contradice lo que dicen los otros días (un nombre cambiado, un orden de hechos equivocado).`,
  doctrina: `Leé con ojos de pastor protestante sano y buscá:
1. doctrina: afirmaciones que, tal como quedaron redactadas, enseñan algo dudoso o desequilibrado (legalismo o moralismo sin evangelio, gracia barata, prosperidad, misticismo, culpa sin esperanza, una doctrina secundaria presentada como la única postura bíblica, Cristo ausente donde el tema lo pide). Proponé una redacción que corrija SOLO con lo que ya dicen estos días.
2. tono: frases que avergüenzan o condenan al lector en vez de llamarlo con firmeza y gracia; frases que no le hablan de «vos»; jerga sin explicar; párrafos confusos.
3. error: algo que, leído por un hombre que recién empieza, se entendería mal, o lo que se dice de un versículo y no coincide con la RVR1960.`,
}
const revisar = (i, m) => `${BASE(i)}\n\n${MIRADAS[m]}\n\nReglas: la corrección usa SOLO información que ya está en estos días (no agregues datos, citas ni autores nuevos); si dos fuentes difieren, atribuí cada dato a su fuente en vez de elegir. "texto_actual" tiene que ser un fragmento copiado EXACTO del campo (sin la ruta entre corchetes ni el paréntesis inicial que agrega el archivo). Sé exigente pero no informes cuestiones de gusto: solo problemas reales. Si no hay, devolvé la lista vacía. Para comprobar lo que dice un versículo usá: python3 /home/user/trabajo/varon/scripts/rvr_ver.py "Libro C:V" (texto RVR1960). Usá solo Read, Bash (únicamente para rvr_ver.py) y la salida estructurada.`
const verificar = (i, hs) => `${BASE(i)}\n\nOtros revisores propusieron estas correcciones. Juzgá cada una con escepticismo: ¿es un problema real que confundiría o desorientaría al lector?, ¿el "texto_actual" figura exactamente en ese campo?, ¿el reemplazo usa solo información que ya está en el estudio, sin agregar datos ni tomar partido entre fuentes?, ¿deja el castellano claro y de «vos»? Si dos propuestas tocan el mismo fragmento, aceptá solo la mejor. Por defecto, si dudás, marcá real=false. Si es real pero el reemplazo tiene un defecto, corregí "texto_nuevo".

Propuestas (el índice es su posición):
${hs.map((h, k) => `[${k}] día ${h.dia} · ${h.campo} · ${h.tipo}\n  problema: ${h.problema}\n  texto_actual: «${h.texto_actual}»\n  texto_nuevo: «${h.texto_nuevo}»\n  justificación: ${h.justificacion}`).join('\n\n')}

Devolvé un veredicto por propuesta. Para comprobar un versículo usá: python3 /home/user/trabajo/varon/scripts/rvr_ver.py "Libro C:V". Usá solo Read, Bash (únicamente para rvr_ver.py) y la salida estructurada.`
const res = await pipeline(
  args.ventanas,
  i => parallel(Object.keys(MIRADAS).map(m => () => agent(revisar(i, m), { label: `revisar:${m}:v${n3(i)}`, phase: 'Revisar', schema: HALLAZGOS })))
    .then(rs => rs.filter(Boolean).flatMap(r => r.hallazgos)),
  (hs, i) => !hs.length ? { ventana: i, hallazgos: [], veredictos: [] }
    : agent(verificar(i, hs), { label: `verificar:v${n3(i)}`, phase: 'Verificar', schema: VEREDICTOS })
        .then(v => ({ ventana: i, hallazgos: hs, veredictos: v ? v.veredictos : null })),
)
return res
