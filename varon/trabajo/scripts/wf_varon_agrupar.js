export const meta = {
  name: 'varon-agrupar',
  description: 'Agrupa por tema las notas del estudio del varón (una tanda de una sección por agente)',
  phases: [{ title: 'Agrupar', detail: 'una tanda por agente' }],
}
const SECCIONES = {
  A: 'CRISIS: la condición actual del varón (crisis de identidad y de masculinidad, pasividad, ausencia del padre, adicciones, salud, cultura e ideologías, la iglesia sin hombres, datos y diagnósticos)',
  B: 'DISEÑO: el diseño de Dios para el varón (imagen de Dios, varón y mujer, trabajar, guardar y dominar, masculinidad bíblica, la caída, Cristo el varón perfecto)',
  C: 'DIOS: el varón en su relación con Dios (conversión, identidad en Cristo, temor de Dios, la Palabra, oración, adoración, santidad, Espíritu Santo, disciplinas, guerra espiritual, fe)',
  D: 'CARÁCTER: carácter y virtudes del varón piadoso (integridad, coraje, dominio propio, humildad, ira, la lengua, orgullo, pereza, emociones, fidelidad, sabiduría, disciplina)',
  E: 'PUREZA: sexualidad y pureza (diseño de la sexualidad, tentación, lujuria, pornografía, la mente, pacto con los ojos, libertad y restauración)',
  F: 'TRABAJO: el varón como trabajador (teología del trabajo, vocación, proveer, ética laboral, dinero y mayordomía, descanso, ambición, desempleo, jubilación)',
  G: 'ESPOSO: el varón como esposo (matrimonio según Dios, liderazgo de siervo, amar como Cristo, proteger y proveer, comunicación, intimidad, conflictos, fidelidad, prepararse para casarse)',
  H: 'PADRE: el varón como padre (Dios Padre como modelo, instruir, disciplinar, ejemplo, culto familiar, hijos e hijas, adolescentes, padre ausente, hijos adultos)',
  I: 'MINISTRO: el varón como líder y ministro (sacerdote del hogar, liderazgo bíblico, ancianos y diáconos, pastorado, llamado, enseñar, discipular a otros hombres)',
  J: 'SIERVO: el varón como siervo (Cristo siervo, servir en la iglesia, la familia y el mundo, humildad, dones, servir a los necesitados)',
  K: 'RELACIONES: amistad, hermandad y mentoría entre varones (amistad, rendición de cuentas, mentores, soledad, comunidad)',
  L: 'JOVEN: el varón joven (juventud, soltería, noviazgo, vocación, pureza, mentores, José, Daniel, David, Timoteo)',
  M: 'ADULTO: el varón adulto (madurez, mediana edad, responsabilidades, crisis, perseverancia, legado)',
  N: 'MAYOR: el varón adulto mayor (vejez, sabiduría, jubilación, enfermedad, prepararse para morir, abuelos, legado)',
  O: 'SOCIEDAD: el varón en la sociedad (ciudadanía, justicia, vida pública, cultura, testimonio y evangelización, defensa de los débiles)',
  P: 'PRUEBAS: sufrimiento, fracaso y restauración (pruebas, depresión, fracaso, caída y restauración, divorcio, desempleo, enfermedad, duelo)',
  Q: 'MODELOS: varones de la Biblia y de la historia como ejemplo o advertencia',
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
  return `Estás ordenando el material de un estudio bíblico exhaustivo sobre EL VARÓN SEGÚN EL DISEÑO DE DIOS, para un hombre cristiano protestante. Leé con UNA llamada a Read (con allow_large: true) el archivo /home/user/trabajo/varon/plan/grupos/${t}.txt. Cada línea es una nota tomada de un libro, con este formato:
id | importancia (3 central, 2 valiosa, 1 complementaria) | tipo | título | subtema | versículos | persona | comienzo del contenido
Todas son de la sección ${s} — ${SECCIONES[s]}. Después devolvé el resultado con la herramienta de salida estructurada. No uses otras herramientas.

Tarea: agrupá TODAS las notas en grupos temáticos finos. Cada grupo reúne notas que enseñan lo mismo o algo muy cercano, por ejemplo «amar a la esposa como Cristo a la iglesia: entregarse por ella», «el pacto con los ojos (Job 31:1)», «José ante la mujer de Potifar», «la oración del padre por sus hijos». Más adelante, con 2 a 6 grupos se va a armar un día de estudio de 20 a 30 minutos, así que cada grupo tiene que ser una unidad de enseñanza clara.

Reglas:
1. Cada id va en exactamente un grupo o en "fuera". Copiá los ids exactos (por ejemplo «b_014#7»); no inventes ninguno y no te olvides de ninguno.
2. Grupos de 3 a 25 notas. Un grupo de 1 o 2 notas solo si la idea es única y valiosa.
3. El "tema" es concreto. «Matrimonio», «oración» o «carácter» no sirven: decí qué aspecto.
4. Las notas de distintos autores que dicen lo mismo van juntas (eso es justamente lo que se quiere unir).
5. Las ilustraciones, biografías y datos van con el tema que ilustran, salvo que formen un tema propio (por ejemplo, la vida de un personaje).
6. En "fuera" van solo las notas que no sirven para un estudio sobre el varón (doctrina general que no lo toca, notas vacías o ilegibles), con una razón breve. Ante la duda, agrupala.`
}
const res = await parallel(args.tandas.map(t => () => agent(prompt(t), { label: `agrupar:${t}`, phase: 'Agrupar', schema: SCHEMA })
  .then(r => ({ t, grupos: r ? r.grupos.length : null, fuera: r ? r.fuera.length : null }))))
return res
