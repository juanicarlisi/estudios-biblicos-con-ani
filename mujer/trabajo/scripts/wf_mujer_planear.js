export const meta = {
  name: 'mujer-planear',
  description: 'Diseña los días de cada parte de «La mujer según el diseño de Dios» a partir de los grupos temáticos de notas',
  phases: [{ title: 'Planear', detail: 'una parte por agente' }],
}
const PARTES = {
  A: ['1', 'La mujer hoy', 'la condición actual de la mujer: crisis de identidad y de feminidad, presión cultural y de las redes, imagen corporal, ansiedad, depresión y agotamiento, soledad, violencia y abuso, feminismo e ideologías, aborto, la iglesia y las mujeres. Es la introducción de todo el estudio: diagnóstico con datos (Argentina y Latinoamérica primero, después internacionales) y con lo que dicen los autores, y la pregunta que el resto del estudio responde.'],
  B: ['2', 'El diseño de Dios', 'imagen de Dios, varón y mujer, Eva y la ayuda idónea, la caída y sus efectos en la mujer, Cristo y las mujeres, la mujer sabia y virtuosa de Proverbios 31, la belleza según Dios.'],
  C: ['3', 'La mujer y Dios', 'conversión, identidad en Cristo, temor de Dios, la Palabra, la oración, la adoración, la santidad, el Espíritu Santo, las disciplinas espirituales, la fe, el descanso en Dios.'],
  D: ['4', 'El carácter de la mujer de Dios', 'sabiduría, espíritu afable y apacible, la lengua y el chisme, la ansiedad y el temor, el contentamiento, la envidia, los celos y la comparación, el perfeccionismo, la ira, el orgullo y la humildad, el dominio propio, la fidelidad, el valor, la gratitud; el fruto del Espíritu (un día por cada rasgo si el material alcanza: amor, gozo, paz, paciencia, benignidad, bondad, fe, mansedumbre, dominio propio) y las emociones (tristeza, enojo, miedo, vergüenza, culpa, celos, soledad, duelo, esperanza) y cómo llevarlas a Dios.'],
  E: ['5', 'Pureza, cuerpo y sexualidad', 'diseño de la sexualidad, tentación, imagen corporal, modestia, pornografía, abuso y sanidad, libertad y restauración.'],
  F: ['6', 'La mujer y su trabajo', 'el hogar, el trabajo fuera de casa, vocación, dinero y mayordomía, el tiempo, Proverbios 31, descanso, ambición y éxito, desempleo.'],
  G: ['7', 'La mujer como esposa', 'el matrimonio según Dios, la ayuda idónea, sumisión y respeto, amar a su esposo, comunicación, intimidad, conflictos y perdón, orar por su esposo, esposo no creyente, esposo que falla, prepararse para casarse.'],
  H: ['8', 'La mujer como madre', 'la maternidad según Dios, embarazo y parto, instruir y disciplinar, hijas e hijos, adolescentes, madre soltera, hijos adultos, adopción, orar por los hijos.'],
  I: ['9', 'La mujer en la iglesia y el liderazgo', 'enseñar a mujeres y niños, discipular, dones espirituales, roles de varones y mujeres en la iglesia y en el hogar (con las posturas de cada autor, sin zanjar entre ellas), las mujeres del Nuevo Testamento que sirvieron, el ministerio de mujeres.'],
  J: ['10', 'La mujer como sierva', 'Cristo siervo, servir en la iglesia, en la familia y en el mundo, hospitalidad, misericordia, humildad, dones, servir a los necesitados.'],
  K: ['11', 'Hermanas, amigas y mentoras', 'amistad, Tito 2 y las mujeres mayores que enseñan a las jóvenes, rendición de cuentas, soledad, comunidad, suegras y familia extendida.'],
  L: ['12', 'La mujer joven', 'adolescencia, soltería, noviazgo, vocación, pureza, mentoras, modelos bíblicos jóvenes.'],
  M: ['13', 'La mujer adulta', 'madurez, los años del medio, la carga mental, hijos adolescentes, padres que envejecen, cansancio, perseverancia, legado.'],
  N: ['14', 'La mujer mayor', 'vejez, menopausia, viudez, abuelas, legado, mentoras, enfermedad, prepararse para morir, Tito 2:3-5.'],
  O: ['15', 'La mujer en la sociedad', 'feminismo, medios y redes, moda y belleza, derechos, ciudadanía, testimonio y evangelización, defensa de los débiles, el aborto.'],
  P: ['16', 'Pruebas, pérdida y restauración', 'sufrimiento, infertilidad, pérdida de un hijo, aborto y sanidad, divorcio, viudez, abuso, enfermedad, depresión, ansiedad, duelo, fracaso y restauración.'],
  Q: ['17', 'Mujeres de la Biblia y de la historia', 'vidas de mujeres bíblicas e históricas como ejemplo o advertencia. Es la última parte: cerrá el estudio con un día que mire todo el recorrido a la luz de Cristo, si el material lo permite.'],
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
const prompt = s => `Sos el editor de un estudio bíblico diario y exhaustivo, «La mujer según el diseño de Dios», para una mujer cristiana protestante de Buenos Aires. Cada día se estudia en 20 a 30 minutos (unas 2.000 a 2.600 palabras). El estudio no tiene un número fijo de días: termina cuando se agota el material, que sale todo de libros de autores protestantes confiables.

Las partes del estudio, en orden:
${indice}

Te toca diseñar los días de la PARTE ${PARTES[s][0]}: ${PARTES[s][1]}.

Leé con Read (allow_large: true):
1. /home/user/trabajo/mujer/plan/planear/${s}.txt: los grupos temáticos de notas de esta parte, uno por línea: clave | cuántas notas (cuántas de importancia 3) | tema | resumen | versículos | autores | personas | tipos de nota.
2. /home/user/trabajo/mujer/plan/planear/${s === 'A' ? '_web.txt' : '_web_corto.txt'}: datos estadísticos verificados (con año y fuente) y artículos de sitios cristianos confiables, con id W.
Después devolvé el plan con la herramienta de salida estructurada. No uses otras herramientas.

Cómo diseñar los días:
1. Cada día enseña UNA cosa propia y clara, y reúne los grupos que la tratan (normalmente entre 30 y 80 notas en total; si muchas repiten lo mismo con otros autores, puede llegar a 100). No partas un tema en días flojos ni amontones en un día temas distintos.
2. Recorré TODOS los grupos: cada clave va en exactamente un día o en "descartados" con su razón (solo si no aporta nada al tema de la parte o repite por completo otro grupo). Un grupo que encaja mejor en otra parte del estudio igual se usa acá si aporta: no lo descartes por eso.
3. Ordená los días en una línea clara y progresiva: de los fundamentos a la práctica, de lo general a lo particular. El primer día presenta la parte; el último la cierra. Que no se repita lo de un día en otro.
4. "lectura": un pasaje que sostenga el tema del día (10 a 30 versículos), que salga de los versículos de sus grupos cuando se pueda. Nombre castellano completo del libro, p. ej. «Efesios 5:21-33». No repitas la misma lectura en dos días.
5. "web": los datos y artículos que sirven a ese día (cada id en un solo día de esta parte). ${s === 'A' ? 'En esta parte los datos son centrales: usá todos los que sirvan al diagnóstico, Argentina y Latinoamérica primero y los internacionales al lado, repartidos por tema.' : 'En esta parte los datos son un complemento: usalos solo donde ilustran de verdad el tema del día.'}
6. No hay mínimo ni máximo de días: los que pida el material, sin estirar ni recortar.`
const res = await parallel(args.secciones.map(s => () => agent(prompt(s), { label: `planear:${s}`, phase: 'Planear', schema: SCHEMA, ...(args.opciones || {}) })
  .then(r => ({ s, dias: r ? r.dias.length : null, descartados: r ? r.descartados.length : null }))))
return res
