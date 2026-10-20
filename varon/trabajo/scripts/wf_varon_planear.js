export const meta = {
  name: 'varon-planear',
  description: 'Diseña los días de cada parte del estudio del varón a partir de los grupos temáticos de notas',
  phases: [{ title: 'Planear', detail: 'una parte por agente' }],
}
const PARTES = {
  A: ['1', 'La crisis del varón hoy', 'la condición actual del varón: crisis de identidad y de masculinidad, pasividad, ausencia del padre, adicciones, salud mental, soledad, cultura e ideologías, la iglesia sin hombres. Es la introducción de todo el estudio: diagnóstico con datos (Argentina y Latinoamérica primero, después internacionales) y con lo que dicen los autores, y la pregunta que el resto del estudio responde.'],
  B: ['2', 'El diseño de Dios', 'imagen de Dios, varón y mujer, trabajar, guardar y dominar, qué es la masculinidad bíblica, la caída y sus efectos en el varón, Cristo el varón perfecto y segundo Adán.'],
  C: ['3', 'El varón y Dios', 'conversión, identidad en Cristo, temor de Dios, la Palabra, la oración, la adoración, la santidad, el Espíritu Santo, las disciplinas espirituales, la guerra espiritual, la fe.'],
  D: ['4', 'El carácter del varón de Dios', 'integridad, coraje, dominio propio, humildad, ira, la lengua, orgullo, pereza, emociones, fidelidad, sabiduría, disciplina.'],
  E: ['5', 'Pureza', 'diseño de la sexualidad, tentación, lujuria, pornografía, la mente, pacto con los ojos, libertad y restauración.'],
  F: ['6', 'El varón y su trabajo', 'teología del trabajo, vocación, proveer, ética laboral, dinero y mayordomía, descanso, ambición y éxito, desempleo.'],
  G: ['7', 'El varón como esposo', 'el matrimonio según Dios, liderazgo de siervo, amar como Cristo, proteger y proveer, comunicación, intimidad, conflictos y perdón, fidelidad, prepararse para casarse.'],
  H: ['8', 'El varón como padre', 'Dios Padre como modelo, instruir, disciplinar, ser ejemplo, culto familiar, hijos e hijas, adolescentes, el padre ausente y sus heridas, los hijos adultos.'],
  I: ['9', 'El varón como líder y ministro', 'sacerdote de su hogar, liderazgo bíblico, ancianos y diáconos, el pastorado, el llamado, enseñar y predicar, discipular a otros hombres.'],
  J: ['10', 'El varón como siervo', 'Cristo siervo, servir en la iglesia, en la familia y en el mundo, humildad, dones, servir a los necesitados.'],
  K: ['11', 'Hermanos, amigos y mentores', 'amistad entre varones, rendición de cuentas, mentores, soledad, comunidad.'],
  L: ['12', 'El varón joven', 'juventud, soltería, noviazgo, vocación, pureza, mentores, José, Daniel, David, Timoteo.'],
  M: ['13', 'El varón adulto', 'madurez, mediana edad, responsabilidades, crisis, perseverancia, construir legado.'],
  N: ['14', 'El varón mayor', 'vejez, sabiduría, jubilación, enfermedad, prepararse para morir, abuelos, legado, Tito 2:2.'],
  O: ['15', 'El varón en la sociedad', 'ciudadanía, justicia, vida pública, cultura, testimonio y evangelización, defensa de los débiles.'],
  P: ['16', 'Pruebas, fracaso y restauración', 'sufrimiento, depresión, fracaso, caída y restauración, divorcio, desempleo, enfermedad, duelo.'],
  Q: ['17', 'Varones de la Biblia y de la historia', 'vidas de varones bíblicos e históricos como ejemplo o advertencia. Es la última parte: cerrá el estudio con un día que mire todo el recorrido a la luz de Cristo, si el material lo permite.'],
}
const SCHEMA = { type: 'object', properties: {
  parte: { type: 'object', properties: { titulo: { type: 'string' }, bajada: { type: 'string', description: '1 o 2 oraciones que presentan la parte' } }, required: ['titulo', 'bajada'] },
  dias: { type: 'array', items: { type: 'object', properties: {
    titulo: { type: 'string', description: 'título breve y atractivo' },
    objetivo: { type: 'string', description: 'qué aprende y qué vive el lector ese día (1 oración)' },
    contenido: { type: 'string', description: 'qué cubre el día, en orden (2 a 4 oraciones)' },
    lectura: { type: 'string', description: 'pasaje bíblico para leer (10 a 30 versículos), con el nombre castellano completo del libro' },
    grupos: { type: 'array', items: { type: 'string' } },
    web: { type: 'array', items: { type: 'string' }, description: 'ids W de datos o artículos de la web para ese día (puede ir vacío)' },
  }, required: ['titulo', 'objetivo', 'contenido', 'lectura', 'grupos', 'web'] } },
  descartados: { type: 'array', items: { type: 'object', properties: { grupo: { type: 'string' }, razon: { type: 'string' } }, required: ['grupo', 'razon'] } },
}, required: ['parte', 'dias', 'descartados'] }
const indice = Object.entries(PARTES).map(([s, p]) => `Parte ${p[0]} (${s}) · ${p[1]}: ${p[2]}`).join('\n')
const prompt = s => `Sos el editor de un estudio bíblico diario y exhaustivo, «El varón según el diseño de Dios», para un hombre cristiano protestante de Buenos Aires. Cada día se estudia en 20 a 30 minutos (unas 2.000 a 2.600 palabras). El estudio no tiene un número fijo de días: termina cuando se agota el material, que sale todo de libros de autores protestantes confiables.

Las partes del estudio, en orden:
${indice}

Te toca diseñar los días de la PARTE ${PARTES[s][0]}: ${PARTES[s][1]}.

Leé con Read (allow_large: true):
1. /home/user/trabajo/varon/plan/planear/${s}.txt: los grupos temáticos de notas de esta parte, uno por línea: clave | cuántas notas (cuántas de importancia 3) | tema | resumen | versículos | autores | personas | tipos de nota.
2. /home/user/trabajo/varon/plan/planear/_web.txt: datos estadísticos verificados (con año y fuente) y artículos de sitios cristianos confiables, con id W.
Después devolvé el plan con la herramienta de salida estructurada. No uses otras herramientas.

Cómo diseñar los días:
1. Cada día enseña UNA cosa propia y clara, y reúne los grupos que la tratan (normalmente entre 30 y 80 notas en total; si muchas repiten lo mismo con otros autores, puede llegar a 100). No partas un tema en días flojos ni amontones en un día temas distintos.
2. Recorré TODOS los grupos: cada clave va en exactamente un día o en "descartados" con su razón (solo si no aporta nada al tema de la parte o repite por completo otro grupo). Un grupo que encaja mejor en otra parte del estudio igual se usa acá si aporta: no lo descartes por eso.
3. Ordená los días en una línea clara y progresiva: de los fundamentos a la práctica, de lo general a lo particular. El primer día presenta la parte; el último la cierra. Que no se repita lo de un día en otro.
4. "lectura": un pasaje que sostenga el tema del día (10 a 30 versículos), que salga de los versículos de sus grupos cuando se pueda. Nombre castellano completo del libro, p. ej. «Efesios 5:21-33». No repitas la misma lectura en dos días.
5. "web": los datos y artículos que sirven a ese día (cada id en un solo día de esta parte). ${s === 'A' ? 'En esta parte los datos son centrales: usá todos los que sirvan al diagnóstico, Argentina y Latinoamérica primero y los internacionales al lado, repartidos por tema.' : 'En esta parte los datos son un complemento: usalos solo donde ilustran de verdad el tema del día.'}
6. No hay mínimo ni máximo de días: los que pida el material, sin estirar ni recortar.`
const res = await parallel(args.secciones.map(s => () => agent(prompt(s), { label: `planear:${s}`, phase: 'Planear', schema: SCHEMA })
  .then(r => ({ s, dias: r ? r.dias.length : null, descartados: r ? r.descartados.length : null }))))
return res
