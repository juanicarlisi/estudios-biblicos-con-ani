export const meta = {
  name: 'mujer-agrupar',
  description: 'Agrupa por tema las notas del estudio de la mujer (una tanda de una sección por agente)',
  phases: [{ title: 'Agrupar', detail: 'una tanda por agente' }],
}
const SECCIONES = {
  A: 'CRISIS: la condición actual de la mujer (crisis de identidad y de feminidad, presión cultural, imagen corporal, ansiedad, depresión y agotamiento, soledad, violencia y abuso, feminismo e ideologías, aborto, la iglesia y las mujeres, datos y diagnósticos).',
  B: 'DISEÑO: el diseño de Dios para la mujer (creada a imagen de Dios, varón y mujer, Eva, la ayuda idónea, la caída y sus efectos en la mujer, Cristo y las mujeres, el retrato de la mujer sabia y virtuosa de Proverbios 31, la belleza según Dios).',
  C: 'DIOS: la mujer en su relación con Dios (conversión, identidad en Cristo, temor de Dios, la Palabra, la oración, la adoración, la santidad, el Espíritu Santo, las disciplinas espirituales, la fe, el descanso en Dios).',
  D: 'CARACTER: carácter y virtudes de la mujer piadosa (sabiduría, espíritu afable y apacible, la lengua y el chisme, la ansiedad y el temor, el contentamiento, la envidia, los celos y la comparación, el perfeccionismo, la ira, el orgullo, la humildad, el dominio propio, la fidelidad, el valor, la gratitud; el fruto del Espíritu —amor, gozo, paz, paciencia, benignidad, bondad, fe, mansedumbre, dominio propio— y las emociones: tristeza, enojo, miedo, vergüenza, culpa, celos, soledad, duelo, esperanza y cómo llevarlas a Dios).',
  E: 'PUREZA: pureza, cuerpo y sexualidad (diseño de la sexualidad, tentación, imagen corporal, modestia, pornografía, abuso y sanidad, libertad y restauración).',
  F: 'TRABAJO: trabajo, vocación y mayordomía (el hogar, el trabajo fuera de casa, el dinero y las compras, el tiempo, Proverbios 31, descanso, ambición y éxito, desempleo).',
  G: 'ESPOSA: la mujer como esposa (el matrimonio según Dios, la ayuda idónea, sumisión y respeto, amar a su esposo, comunicación, intimidad, conflictos y perdón, orar por su esposo, esposo no creyente, esposo que falla, prepararse para casarse).',
  H: 'MADRE: la mujer como madre (la maternidad según Dios, embarazo y parto, instruir y disciplinar, hijas e hijos, adolescentes, madre soltera, hijos adultos, adopción, la madre y el padre, orar por los hijos).',
  I: 'LIDERAZGO: la mujer en la iglesia y el liderazgo (enseñar a mujeres y niños, discipular, dones espirituales, roles de varones y mujeres en la iglesia y en el hogar con las posturas de cada autor, las mujeres del Nuevo Testamento que sirvieron, el ministerio de mujeres).',
  J: 'SIERVA: la mujer como sierva (Cristo siervo, servir en la iglesia y en la familia, hospitalidad, misericordia, humildad, dones, servir a los necesitados).',
  K: 'RELACIONES: amistad, hermandad y mentoría entre mujeres (amistad, Tito 2 y las mujeres mayores que enseñan a las jóvenes, rendición de cuentas, soledad, comunidad, suegras y familia extendida).',
  L: 'JOVEN: la mujer joven (adolescencia, soltería, noviazgo, vocación, pureza, mentoras, modelos bíblicos jóvenes).',
  M: 'ADULTA: la mujer adulta (madurez, los años del medio, la carga mental, hijos adolescentes, padres que envejecen, cansancio, perseverancia, legado).',
  N: 'MAYOR: la mujer mayor (vejez, menopausia, viudez, abuelas, legado, mentoras, enfermedad, prepararse para morir).',
  O: 'SOCIEDAD: la mujer en la sociedad y la cultura (feminismo, medios y redes, moda y belleza, derechos, el aborto, ciudadanía, testimonio y evangelización, defensa de los débiles).',
  P: 'PRUEBAS: sufrimiento, pérdida y restauración (infertilidad, pérdida de un hijo, aborto y sanidad, divorcio, viudez, abuso, enfermedad, depresión, ansiedad, duelo, fracaso).',
  Q: 'MODELOS: mujeres de la Biblia y de la historia como ejemplo o advertencia (poné su nombre en "persona").',
}
const SCHEMA = { type: 'object', properties: {
  grupos: { type: 'array', items: { type: 'object', properties: {
    tema: { type: 'string', description: 'tema concreto y específico, nunca genérico' },
    resumen: { type: 'string', description: '1 o 2 oraciones: qué enseñan juntas estas notas' },
    ids: { type: 'array', items: { type: 'string' } },
    refs: { type: 'array', items: { type: 'string' }, description: 'los pasajes bíblicos principales del grupo (máx. 5)' },
  }, required: ['tema', 'resumen', 'ids'] } },
  fuera: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, razon: { type: 'string' } }, required: ['id', 'razon'] } },
}, required: ['grupos', 'fuera'] }
const prompt = t => {
  const s = t.split('_')[1]
  return `Estás ordenando el material de un estudio bíblico exhaustivo sobre LA MUJER SEGÚN EL DISEÑO DE DIOS, para una mujer cristiana protestante. Leé con UNA llamada a Read (con allow_large: true) el archivo /home/user/trabajo/mujer/plan/grupos/${t}.txt. Cada línea es una nota tomada de un libro, con este formato:
id | importancia (3 central, 2 valiosa, 1 complementaria) | tipo | título | subtema | versículos | persona | comienzo del contenido
Todas son de la sección ${s} — ${SECCIONES[s]}. Después devolvé el resultado con la herramienta de salida estructurada. No uses otras herramientas.

Tarea: agrupá TODAS las notas en grupos temáticos finos. Cada grupo reúne notas que enseñan lo mismo o algo muy cercano, por ejemplo «amar a la esposa como Cristo a la iglesia: entregarse por ella», «el pacto con los ojos (Job 31:1)», «José ante la mujer de Potifar», «la oración del padre por sus hijos». Más adelante, con 2 a 6 grupos se va a armar un día de estudio de 20 a 30 minutos, así que cada grupo tiene que ser una unidad de enseñanza clara.

Reglas:
1. Cada id va en exactamente un grupo o en "fuera". Copiá los ids exactos (por ejemplo «b_014#7»); no inventes ninguno y no te olvides de ninguno.
2. Grupos de 4 a 30 notas (las tandas ya vienen ordenadas por parecido, así que muchas notas seguidas suelen ir juntas). Un grupo de 1 a 3 notas solo si la idea es única y valiosa.
3. El "tema" es concreto. «Matrimonio», «oración» o «carácter» no sirven: decí qué aspecto.
4. Las notas de distintos autores que dicen lo mismo van juntas (eso es justamente lo que se quiere unir).
5. Las ilustraciones, biografías y datos van con el tema que ilustran, salvo que formen un tema propio (por ejemplo, la vida de un personaje).
6. En "fuera" van solo las notas que no sirven para un estudio sobre la mujer (doctrina general que no lo toca, notas vacías o ilegibles), con una razón breve. Ante la duda, agrupala.`
}
const res = await parallel(args.tandas.map(t => () => agent(prompt(t), { label: `agrupar:${t}`, phase: 'Agrupar', schema: SCHEMA, ...(args.opciones || {}) })
  .then(r => ({ t, grupos: r ? r.grupos.length : null, fuera: r ? r.fuera.length : null }))))
return res
