export const meta = {
  name: 'varon-escribir-2',
  description: 'Escribe cada día del estudio del varón a partir de su insumo (la verificación la hace un programa, no la IA)',
  phases: [{ title: 'Escribir', detail: 'un día por agente; verifica verificar_dia.py' }],
}
const F = { type: 'array', items: { type: 'string' } }
const TF = { type: 'object', properties: { texto: { type: 'string' }, fuentes: F }, required: ['texto', 'fuentes'] }
const SCHEMA = { type: 'object', properties: {
  dia: { type: 'integer' }, titulo: { type: 'string' }, bajada: { type: 'string' },
  minutos: { type: 'object', properties: { estudio: { type: 'integer' } }, required: ['estudio'] },
  lectura: { type: 'object', properties: { pasaje: { type: 'string' }, porque: { type: 'string' } }, required: ['pasaje', 'porque'] },
  versiculos: { type: 'array', items: { type: 'object', properties: { ref: { type: 'string' }, porque: { type: 'string' } }, required: ['ref', 'porque'] } },
  entrada: TF,
  apartados: { type: 'array', items: { type: 'object', properties: { titulo: { type: 'string' }, parrafos: { type: 'array', items: TF }, destacado: TF }, required: ['titulo', 'parrafos'] } },
  citas: { type: 'array', items: { type: 'object', properties: { texto: { type: 'string' }, autor: { type: 'string' }, obra: { type: 'string' }, fuentes: F }, required: ['texto', 'autor', 'obra', 'fuentes'] } },
  datos: { type: 'array', items: { type: 'object', properties: { valor: { type: 'string' }, texto: { type: 'string' }, fuentes: F }, required: ['valor', 'texto', 'fuentes'] } },
  modelo: { type: 'object', properties: { persona: { type: 'string' }, texto: { type: 'string' }, refs: F, fuentes: F }, required: ['persona', 'texto', 'refs', 'fuentes'] },
  palabras: { type: 'array', items: { type: 'object', properties: { original: { type: 'string' }, idioma: { type: 'string', enum: ['griego', 'hebreo'] }, translit: { type: 'string' }, ref: { type: 'string' }, significado: { type: 'string' }, fuentes: F }, required: ['idioma', 'translit', 'ref', 'significado', 'fuentes'] } },
  interpretaciones: { type: 'array', items: { type: 'object', properties: { tema: { type: 'string' }, posturas: { type: 'array', items: { type: 'object', properties: { postura: { type: 'string' }, quien: { type: 'string' }, fuentes: F }, required: ['postura', 'quien', 'fuentes'] } }, nota: { type: 'string' } }, required: ['tema', 'posturas'] } },
  conexiones: { type: 'array', items: { type: 'object', properties: { ref: { type: 'string' }, nota: { type: 'string' }, fuentes: F }, required: ['ref', 'nota', 'fuentes'] } },
  para_vivir: { type: 'array', items: TF },
  para_reflexionar: { type: 'array', items: { type: 'string' } },
  para_conversar: { type: 'array', items: { type: 'string' } },
  para_orar: { type: 'string' },
  profundizar: { type: 'array', items: { type: 'object', properties: { titulo: { type: 'string' }, texto: { type: 'string' }, fuentes: F }, required: ['titulo', 'texto', 'fuentes'] } },
  notas_no_usadas: { type: 'string' },
}, required: ['dia', 'titulo', 'bajada', 'minutos', 'lectura', 'versiculos', 'entrada', 'apartados', 'citas', 'datos', 'palabras', 'interpretaciones', 'conexiones', 'para_vivir', 'para_reflexionar', 'para_conversar', 'para_orar', 'profundizar', 'notas_no_usadas'] }
const n3 = d => String(d).padStart(3, '0')
const REGLAS = `Escribís UN día de «El varón según el diseño de Dios», estudio bíblico diario (20 a 30 minutos) para un hombre cristiano protestante de Buenos Aires. Leé con UNA sola llamada a Read (allow_large: true) el insumo que te indico; no uses otra herramienta. Después devolvé el día con la salida estructurada.
Reglas:
1. NO INVENTAR: cada afirmación sale de las notas o datos del insumo y lleva en "fuentes" los ids que la respaldan («b_014#7», «W0012»). Nada de conocimiento propio, cifras, fechas ni frases entre «» que no estén en el insumo; las historias de los autores se cuentan como de ellos («Un pastor cuenta que…»). Los datos con «ESTIMACIÓN propia» no se usan.
2. Estudio de corrido, no lista de notas: un hilo claro que sigue el plan del día; uní lo que repiten varios autores; priorizá lo central (importancia 3 y 2) y lo bíblico; lo valioso que sobra va a "profundizar". Nombrá al autor solo si aporta algo propio (postura, frase, experiencia) o si las fuentes difieren; no encadenes «según X… Y agrega…».
3. La Biblia primero: referencias con nombre castellano completo («Efesios 5:25»); si dos autores difieren, cada postura con quién la sostiene, sin tomar partido. Las frases bíblicas entre «» solo si figuran literales en el insumo.
4. Tono: de «vos», rioplatense, cálido y directo, como un hermano mayor sabio; frases cortas; sin relleno ni sermón. Temas delicados (suicidio, depresión, abuso, adicciones, divorcio, duelo): con cuidado pastoral y la gracia de Cristo junto al llamado; animá a pedir ayuda a alguien de confianza, al pastor o a un profesional; no escribas teléfonos (la app los agrega).
5. Continuidad: respetá «ENFOQUE PROPIO» y no desarrolles de nuevo lo que enseñan los «DÍAS PARECIDOS»; remití en una frase («como viste el día N», «lo vas a ver el día N»).
6. Largo: el cuerpo (entrada, apartados, citas, datos, modelo, palabras, interpretaciones, conexiones, para_vivir) entre 2.000 y 2.500 palabras (nunca más de 2.600). 3 a 6 apartados. "versiculos": 1 a 3 referencias. "para_reflexionar": 3 preguntas; "para_conversar": 0 a 2; "para_orar": breve, en primera persona. Los campos sin material (modelo, palabras, datos, interpretaciones) van vacíos; no los rellenes. "notas_no_usadas": una línea.`
const escribir = d => `${REGLAS}\n\nInsumo: /home/user/trabajo/varon/insumos/dia_${n3(d)}.txt  ·  "dia" = ${d}.`
const OPC = args.opciones || {}
const res = await parallel(args.dias.map(d => () => agent(escribir(d), { label: `escribir:dia${n3(d)}`, phase: 'Escribir', schema: SCHEMA, ...OPC }).then(r => !!r)))
return `${res.filter(Boolean).length}/${args.dias.length} escritos` + (res.some(r => !r) ? ` · faltan ${args.dias.filter((_, i) => !res[i]).join(',')}` : '')
