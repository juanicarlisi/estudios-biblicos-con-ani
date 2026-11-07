export const meta = {
  name: 'mujer-extraer',
  description: 'Extrae, de cada bloque de la biblioteca, todo lo que enseña sobre la mujer según el diseño de Dios (notas con fuente y página)',
  phases: [{ title: 'Extraer', detail: 'un bloque por agente' }],
}
const SECCIONES = `A CRISIS: la condición actual de la mujer (crisis de identidad y de feminidad, presión cultural, imagen corporal, ansiedad, depresión y agotamiento, soledad, violencia y abuso, feminismo e ideologías, aborto, la iglesia y las mujeres, datos y diagnósticos).
B DISEÑO: el diseño de Dios para la mujer (creada a imagen de Dios, varón y mujer, Eva, la ayuda idónea, la caída y sus efectos en la mujer, Cristo y las mujeres, el retrato de la mujer sabia y virtuosa de Proverbios 31, la belleza según Dios).
C DIOS: la mujer en su relación con Dios (conversión, identidad en Cristo, temor de Dios, la Palabra, la oración, la adoración, la santidad, el Espíritu Santo, las disciplinas espirituales, la fe, el descanso en Dios).
D CARACTER: carácter y virtudes de la mujer piadosa (sabiduría, espíritu afable y apacible, la lengua y el chisme, la ansiedad y el temor, el contentamiento, la envidia, los celos y la comparación, el perfeccionismo, la ira, el orgullo, la humildad, el dominio propio, la fidelidad, el valor, la gratitud; el fruto del Espíritu —amor, gozo, paz, paciencia, benignidad, bondad, fe, mansedumbre, dominio propio— y las emociones: tristeza, enojo, miedo, vergüenza, culpa, celos, soledad, duelo, esperanza y cómo llevarlas a Dios).
E PUREZA: pureza, cuerpo y sexualidad (diseño de la sexualidad, tentación, imagen corporal, modestia, pornografía, abuso y sanidad, libertad y restauración).
F TRABAJO: trabajo, vocación y mayordomía (el hogar, el trabajo fuera de casa, el dinero y las compras, el tiempo, Proverbios 31, descanso, ambición y éxito, desempleo).
G ESPOSA: la mujer como esposa (el matrimonio según Dios, la ayuda idónea, sumisión y respeto, amar a su esposo, comunicación, intimidad, conflictos y perdón, orar por su esposo, esposo no creyente, esposo que falla, prepararse para casarse).
H MADRE: la mujer como madre (la maternidad según Dios, embarazo y parto, instruir y disciplinar, hijas e hijos, adolescentes, madre soltera, hijos adultos, adopción, la madre y el padre, orar por los hijos).
I LIDERAZGO: la mujer en la iglesia y el liderazgo (enseñar a mujeres y niños, discipular, dones espirituales, roles de varones y mujeres en la iglesia y en el hogar con las posturas de cada autor, las mujeres del Nuevo Testamento que sirvieron, el ministerio de mujeres).
J SIERVA: la mujer como sierva (Cristo siervo, servir en la iglesia y en la familia, hospitalidad, misericordia, humildad, dones, servir a los necesitados).
K RELACIONES: amistad, hermandad y mentoría entre mujeres (amistad, Tito 2 y las mujeres mayores que enseñan a las jóvenes, rendición de cuentas, soledad, comunidad, suegras y familia extendida).
L JOVEN: la mujer joven (adolescencia, soltería, noviazgo, vocación, pureza, mentoras, modelos bíblicos jóvenes).
M ADULTA: la mujer adulta (madurez, los años del medio, la carga mental, hijos adolescentes, padres que envejecen, cansancio, perseverancia, legado).
N MAYOR: la mujer mayor (vejez, menopausia, viudez, abuelas, legado, mentoras, enfermedad, prepararse para morir).
O SOCIEDAD: la mujer en la sociedad y la cultura (feminismo, medios y redes, moda y belleza, derechos, el aborto, ciudadanía, testimonio y evangelización, defensa de los débiles).
P PRUEBAS: sufrimiento, pérdida y restauración (infertilidad, pérdida de un hijo, aborto y sanidad, divorcio, viudez, abuso, enfermedad, depresión, ansiedad, duelo, fracaso).
Q MODELOS: mujeres de la Biblia y de la historia como ejemplo o advertencia (poné su nombre en "persona").`
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
const prompt = b => `Estás armando, junto a otros lectores, un estudio bíblico exhaustivo sobre LA MUJER SEGÚN EL DISEÑO DE DIOS, para una mujer cristiana protestante. Leé con UNA llamada a Read (con allow_large: true) el archivo /home/user/trabajo/mujer/bloques/${b}.txt: trae páginas de libros de autores protestantes confiables (arriba está la tabla de fuentes; cada página empieza con «=== [ID | pág. N] ===»). Después devolvé las notas con la herramienta de salida estructurada. No uses otras herramientas.

Qué extraer: TODO lo que enseña, aplica, ilustra o documenta algo sobre la mujer, su vida y su fe, según estas secciones:
${SECCIONES}

Criterios:
1. Una nota por idea distinta. Si una idea sigue varias páginas, una sola nota (en "pagina" poné el rango, p. ej. "45-47").
2. "contenido" tiene que poder usarse sin el libro: la idea, el argumento, el ejemplo y el pasaje bíblico que la sostiene, fieles al autor (podés parafrasear; no agregues nada que el autor no diga). Si es una opinión propia del autor, decilo («según el autor…»). Cuando los autores toman posición en temas donde los evangélicos difieren (roles de varones y mujeres, mujeres en el ministerio), anotá cuál es la postura del autor sin suavizarla.
3. "cita": solo si hay una frase textual breve y memorable; copiala exacta.
4. Datos y estadísticas ("tipo": "dato"): con el año, el lugar y la fuente que da el autor.
5. Temas generales de la vida cristiana (oración, Biblia, fe, iglesia, doctrina): tomá solo lo mejor y lo que se aplica de verdad a la vida de la mujer; no resumas todo el libro. NO extraigas doctrina general que no toca a la mujer (elección, justificación en abstracto, escatología, cristología técnica, historia del texto).
6. Si el bloque es de un comentario bíblico, extraé SOLO lo que explica pasajes que hablan de mujeres o se aplican directamente a ellas (p. ej. Gn 1-3, Pr 31, 1 Co 7 y 11 y 14, Ef 5, Col 3, 1 Ti 2, 3 y 5, Tit 2, 1 P 3, Rut, Ester, las mujeres de los Evangelios y de Hechos) y su aplicación.
7. Ignorá portadas, índices, publicidad y páginas sin contenido. Si el bloque casi no trata el tema, devolvé pocas notas (o ninguna): no rellenes.
8. "importancia": 3 solo para lo central y mejor dicho; 2 para lo valioso; 1 para lo complementario.`
const res = await parallel(args.bloques.map(b => () => agent(prompt(b), { label: `extraer:${b}`, phase: 'Extraer', schema: SCHEMA, ...(args.opciones || {}) }).then(r => ({ b, n: r ? r.notas.length : null }))))
return res
