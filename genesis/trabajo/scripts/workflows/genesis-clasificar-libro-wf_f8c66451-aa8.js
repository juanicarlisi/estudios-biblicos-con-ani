export const meta = {
  name: 'genesis-clasificar-libro',
  description: 'Asigna las notas generales de Génesis a las secciones de la introducción y de los temas',
  phases: [{ title: 'Clasificar', detail: 'un archivo de notas por agente' }],
}
const SECCIONES = `INTRODUCCIÓN
- I1 «Nombre, autor y fecha»: el título (Génesis, Bereshit), la autoría mosaica, la hipótesis documental (JEDP) y sus respuestas, la fecha de composición, la unidad del libro, las fuentes que pudo usar Moisés.
- I2 «Estructura y mensaje»: las toledot («estas son las generaciones»), bosquejos y divisiones del libro, su propósito y tema central, su lugar en el Pentateuco y en el canon, cómo prepara el resto de la Biblia.
- I3 «Cómo leer Génesis 1 a 11»: género literario e historicidad, Génesis y la ciencia, los días de la creación y la edad de la tierra, la evolución, el Adán histórico, si el diluvio fue universal o local, los paralelos del Antiguo Oriente (Enuma Elish, Gilgamesh, Atrahasis), las genealogías, la longevidad y la cronología (Ussher, etc.).
- I4 «El mundo de los patriarcas»: contexto histórico y fechas de los patriarcas, arqueología (Ur, Mari, Nuzi, Ebla), costumbres (adopción, primogenitura, terafines, concubinas, pactos), geografía, Egipto en tiempos de José.
- I5 «Génesis en el Nuevo Testamento»: cómo Jesús y los apóstoles citan y usan Génesis en general (no el comentario puntual de un versículo).
TEMAS
- T1 «Dios Creador»: la doctrina de la creación, la creación de la nada, el Dios trino en la creación, los nombres de Dios (Elohim, Jehová/YHWH, El Shaddai, El Elyón), los atributos de Dios que muestra Génesis, el reposo de Dios, los ángeles.
- T2 «El ser humano, imagen de Dios»: imagen y semejanza, cuerpo y alma, dominio y mayordomía de la creación, el trabajo, la dignidad humana, el origen de la humanidad.
- T3 «Matrimonio, familia y sexualidad»: el matrimonio según Génesis 2, varón y mujer, los roles, la sexualidad, la poligamia en Génesis, los hijos y la crianza, los conflictos familiares, lecciones para la pareja.
- T4 «El pecado, la caída y el juicio»: la tentación, Satanás y la serpiente, el pecado original, la muerte, la maldición, cómo se extiende el pecado (Caín, el diluvio, Babel, Sodoma), el juicio de Dios.
- T5 «Los pactos de Dios»: pacto de obras o edénico, el pacto con Noé, el pacto con Abraham (Gn 12, 15, 17), la circuncisión, la teología del pacto, las promesas de tierra, descendencia y bendición, Israel y el futuro de las promesas.
- T6 «La fe de Abraham y la justificación»: Gn 15:6, fe y obediencia, Romanos 4, Gálatas 3, Santiago 2, Hebreos 11, la prueba de Gn 22, la fe de los patriarcas.
- T7 «Elección, gracia y bendición a las naciones»: la elección soberana (Isaac y no Ismael, Jacob y no Esaú, Romanos 9), la gracia que no depende del mérito, la bendición a todas las familias de la tierra, la primogenitura y la bendición.
- T8 «La providencia de Dios y el sufrimiento»: José, Gn 50:20, Dios que obra aun en el mal, el sufrimiento y la espera, soberanía de Dios y responsabilidad humana, la oración.
- T9 «Cristo en Génesis»: el protoevangelio (3:15), la simiente prometida, los tipos de Cristo (Adán, Abel, el arca, Melquisedec, Isaac, la escalera de Jacob, José), el Ángel de Jehová y las teofanías, Siloh y el cetro de Judá, los sacrificios.`
const clasificar = n => `Vas a ordenar notas de estudio sobre Génesis para escribir la introducción al libro y unos artículos de temas. Leé con UNA llamada a Read (con allow_large: true) el archivo /home/user/trabajo/insumos/libro/cand_${n}.txt: cada línea es una nota, con su id entre corchetes, la referencia, el tipo, la importancia, la fuente, el título y el comienzo del contenido.

Asigná cada nota a UNA sola sección, la que mejor le corresponde, entre estas:
${SECCIONES}

Criterios:
- Una nota de aplicación, de personaje o de ilustración va al tema que mejor ilustra (por ejemplo, la vida matrimonial de Abraham y Sara va a T3; la fe de Abraham, a T6).
- Dejá AFUERA (no la pongas en ninguna lista) la nota que no trata Génesis, que es demasiado general para aportar algo, que solo menciona Génesis de paso, o que es un devocional sin contenido.
- No inventes ids: copiá exactamente los que aparecen entre corchetes.

Devolvé el resultado con la herramienta de salida estructurada: una lista "asignaciones" con un elemento por sección usada, {seccion: "I1".."I5" o "T1".."T9", ids: [...]}. No uses otras herramientas aparte de Read.`
const SCHEMA = { type: 'object', properties: { asignaciones: { type: 'array', items: { type: 'object', properties: { seccion: { type: 'string' }, ids: { type: 'array', items: { type: 'string' } } }, required: ['seccion', 'ids'] } } }, required: ['asignaciones'] }
const archivos = ['01','02','03','04','05','06','07','08','09','10']
const res = await parallel(archivos.map(n => () => agent(clasificar(n), { label: `clasificar:cand${n}`, phase: 'Clasificar', schema: SCHEMA })))
return res.map((r, i) => ({ archivo: archivos[i], ok: !!r, n: r ? r.asignaciones.reduce((s, a) => s + a.ids.length, 0) : 0 }))
