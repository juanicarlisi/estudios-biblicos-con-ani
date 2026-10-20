export const meta = {
  name: 'varon-extraer',
  description: 'Extrae, de cada bloque de la biblioteca, todo lo que enseña sobre el varón según el diseño de Dios (notas con fuente y página)',
  phases: [{ title: 'Extraer', detail: 'un bloque por agente' }],
}
const SECCIONES = `A CRISIS: la condición actual del varón (crisis de identidad y de masculinidad, pasividad, ausencia del padre, adicciones, salud, cultura e ideologías, la iglesia sin hombres, datos y diagnósticos).
B DISEÑO: el diseño de Dios para el varón (creación a imagen de Dios, varón y mujer, el mandato de trabajar, guardar y dominar, qué es la masculinidad bíblica, la caída y sus efectos en el varón, Cristo como el varón perfecto y segundo Adán).
C DIOS: el varón en su relación con Dios (conversión, identidad en Cristo, temor de Dios, la Palabra, la oración, la adoración, la santidad, el Espíritu Santo, disciplinas espirituales, guerra espiritual, fe).
D CARACTER: carácter y virtudes del varón piadoso (integridad, coraje, dominio propio, humildad, mansedumbre, ira, la lengua, orgullo, pereza, emociones, fidelidad, sabiduría, disciplina).
E PUREZA: sexualidad y pureza (diseño de la sexualidad, tentación, lujuria, pornografía, la mente, pacto con los ojos, libertad y restauración).
F TRABAJO: el varón como trabajador (teología del trabajo, vocación, proveer, ética laboral, dinero y mayordomía, descanso, ambición y éxito, desempleo, jubilación).
G ESPOSO: el varón como esposo (el matrimonio según Dios, liderazgo de siervo, amar como Cristo, proteger y proveer, comunicación, intimidad, conflictos y perdón, fidelidad, prepararse para casarse).
H PADRE: el varón como padre (Dios Padre como modelo, instruir, disciplinar, ser ejemplo, culto familiar, hijos e hijas, adolescentes, el padre ausente y las heridas del padre, la relación con los hijos adultos).
I MINISTRO: el varón como líder y ministro (sacerdote de su hogar, liderazgo bíblico, ancianos y diáconos, el pastorado, el llamado, enseñar y predicar, discipular a otros hombres).
J SIERVO: el varón como siervo (Cristo siervo, servir en la iglesia, en la familia y en el mundo, humildad, dones, servir a los necesitados).
K RELACIONES: amistad, hermandad y mentoría entre varones (amistad, rendición de cuentas, mentores, soledad, comunidad, la iglesia).
L JOVEN: el varón joven (juventud, soltería, noviazgo, vocación, pureza, mentores, modelos bíblicos como José, Daniel, David y Timoteo).
M ADULTO: el varón adulto (madurez, mediana edad, responsabilidades, crisis, perseverancia, construir legado).
N MAYOR: el varón adulto mayor (vejez, sabiduría, jubilación, enfermedad, prepararse para morir, abuelos, legado, Tito 2:2).
O SOCIEDAD: el varón en la sociedad (ciudadanía, justicia, el trabajo y la vida pública, la cultura, testimonio y evangelización, defensa de los débiles).
P PRUEBAS: sufrimiento, fracaso y restauración (pruebas, depresión, fracaso, caída y restauración, divorcio, desempleo, enfermedad, duelo).
Q MODELOS: varones de la Biblia y de la historia como ejemplo o advertencia (poné su nombre en "persona").`
const SCHEMA = { type: 'object', properties: { notas: { type: 'array', items: { type: 'object', properties: {
  seccion: { type: 'string', enum: ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q'] },
  subtema: { type: 'string', description: 'tema puntual en pocas palabras, p. ej. "liderazgo de siervo", "pacto con los ojos"' },
  tipo: { type: 'string', enum: ['doctrina', 'exegesis', 'aplicacion', 'consejo', 'ilustracion', 'biografia', 'dato', 'advertencia', 'definicion'] },
  titulo: { type: 'string' },
  contenido: { type: 'string', description: '2 a 6 oraciones con la idea completa del autor, su argumento y sus ejemplos, en castellano' },
  cita: { type: 'string', description: 'frase textual breve y memorable del autor (máx. 60 palabras), copiada exacta; vacía si no hay' },
  refs: { type: 'array', items: { type: 'string' }, description: 'pasajes bíblicos que usa, p. ej. "Ef 5:25"' },
  persona: { type: 'string', description: 'personaje bíblico o histórico si la nota trata de uno' },
  fuente: { type: 'string', description: 'id de la fuente según la tabla del bloque, p. ej. R0001' },
  pagina: { type: 'string' },
  importancia: { type: 'integer', minimum: 1, maximum: 3, description: '3 = central para el estudio; 2 = valioso; 1 = complementario' },
}, required: ['seccion', 'subtema', 'tipo', 'titulo', 'contenido', 'fuente', 'pagina', 'importancia'] } } }, required: ['notas'] }
const n3 = n => String(n).padStart(3, '0')
const prompt = b => `Estás armando, junto a otros lectores, un estudio bíblico exhaustivo sobre EL VARÓN SEGÚN EL DISEÑO DE DIOS, para un hombre cristiano protestante. Leé con UNA llamada a Read (con allow_large: true) el archivo /home/user/trabajo/varon/bloques/${b}.txt: trae páginas de libros de autores protestantes confiables (arriba está la tabla de fuentes; cada página empieza con «=== [ID | pág. N] ===»). Después devolvé las notas con la herramienta de salida estructurada. No uses otras herramientas.

Qué extraer: TODO lo que enseña, aplica, ilustra o documenta algo sobre el varón según estas secciones:
${SECCIONES}

Criterios:
1. Una nota por idea distinta. Si una idea sigue varias páginas, una sola nota (en "pagina" poné el rango, p. ej. "45-47").
2. "contenido" tiene que poder usarse sin el libro: la idea, el argumento, el ejemplo y el pasaje bíblico que la sostiene, fieles al autor (podés parafrasear; no agregues nada que el autor no diga). Si es una opinión propia del autor, decilo («según el autor…»).
3. "cita": solo si hay una frase textual breve y memorable; copiala exacta.
4. Datos y estadísticas ("tipo": "dato"): con el año, el lugar y la fuente que da el autor.
5. Temas generales de la vida cristiana (oración, Biblia, fe, iglesia, doctrina): tomá solo lo mejor y lo que se aplica de verdad a la vida del varón, no resumas todo el libro. NO extraigas doctrina general que no toca al varón (elección, justificación en abstracto, escatología, cristología técnica, historia del texto), aunque esté bien explicada.
6. Si el bloque es de un comentario bíblico, extraé SOLO lo que explica pasajes que hablan del varón o se aplican directamente a él (p. ej. Gn 1-3, Ef 5-6, Col 3, 1 Ti 2-3, Tit 1-2, 1 P 3, Proverbios, los personajes, el trabajo, la familia, el liderazgo, la santidad práctica) y su aplicación.
7. Ignorá portadas, índices, publicidad y páginas sin contenido. Si el bloque casi no trata el tema, devolvé pocas notas (o ninguna): no rellenes.
8. "importancia": 3 solo para lo central y mejor dicho; 2 para lo valioso; 1 para lo complementario.`
const res = await parallel(args.bloques.map(b => () => agent(prompt(b), { label: `extraer:${b}`, phase: 'Extraer', schema: SCHEMA }).then(r => ({ b, n: r ? r.notas.length : null }))))
return res
