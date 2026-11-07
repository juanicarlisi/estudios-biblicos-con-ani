export const meta = {
  name: 'mujer-investigar-web',
  description: 'Investiga en sitios confiables estadísticas (Argentina y Latinoamérica primero, más internacionales) y artículos cristianos sobre la mujer',
  phases: [{ title: 'Investigar', detail: 'un tema por agente, con fuente y fecha de cada dato' }],
}
const SCHEMA = { type: 'object', properties: {
  datos: { type: 'array', items: { type: 'object', properties: {
    tema: { type: 'string' }, indicador: { type: 'string' }, valor: { type: 'string' }, ambito: { type: 'string', description: 'Argentina, Latinoamérica, Mundial, EE.UU., etc.' },
    anio: { type: 'string', description: 'año o período del dato' }, fuente: { type: 'string', description: 'organismo o estudio' }, url: { type: 'string' },
    cita_textual: { type: 'string', description: 'la frase exacta de la fuente que contiene el dato' },
    tipo_fuente: { type: 'string', enum: ['oficial', 'academica', 'encuesta', 'periodistica', 'organizacion_cristiana'] }, verificado_en_fuente: { type: 'boolean', description: 'true si abriste la página de la fuente y viste el dato' }, notas: { type: 'string' },
  }, required: ['tema', 'indicador', 'valor', 'ambito', 'anio', 'fuente', 'url', 'cita_textual', 'tipo_fuente', 'verificado_en_fuente'] } },
  articulos: { type: 'array', items: { type: 'object', properties: {
    titulo: { type: 'string' }, autor: { type: 'string' }, sitio: { type: 'string' }, url: { type: 'string' }, fecha: { type: 'string' },
    ideas_clave: { type: 'array', items: { type: 'string' } }, cita: { type: 'string', description: 'frase textual breve y memorable' }, refs_biblicas: { type: 'array', items: { type: 'string' } },
  }, required: ['titulo', 'autor', 'sitio', 'url', 'ideas_clave'] } },
  pendientes: { type: 'string', description: 'datos que buscaste y no encontraste en fuentes confiables' },
}, required: ['datos', 'articulos', 'pendientes'] }
const TEMAS = [
  ['salud_mental', 'Salud mental de las mujeres: depresión y ansiedad por sexo (Argentina: Ministerio de Salud, Encuesta Nacional de Factores de Riesgo; OPS, OMS), suicidio e intentos por sexo, consumo de psicofármacos por sexo, estrés y agotamiento (burnout) en mujeres, trastornos de la conducta alimentaria y su prevalencia.'],
  ['salud_cuerpo', 'Salud y cuerpo de las mujeres: esperanza de vida por sexo (INDEC, OPS, Banco Mundial), mortalidad materna, edad al primer embarazo, controles prenatales, cáncer de mama y de cuello uterino (tamizaje), menopausia, imagen corporal y cirugías estéticas en Argentina y Latinoamérica.'],
  ['familia_maternidad', 'Familia y maternidad: natalidad y fecundidad (INDEC, CEPAL), edad de la primera maternidad, embarazo adolescente (Ministerio de Salud de la Nación), nacimientos fuera del matrimonio, matrimonios y divorcios, hogares monoparentales con jefatura femenina (Censo 2022, EPH), madres solas, adopción, infertilidad (prevalencia).'],
  ['trabajo_cuidado', 'Trabajo y cuidado: Encuesta Nacional de Uso del Tiempo (INDEC), trabajo doméstico y de cuidado no remunerado por sexo, tasa de actividad y de empleo por sexo, brecha salarial, informalidad, empleo doméstico, mujeres que cuidan a padres mayores (OIT, CEPAL, ONU Mujeres).'],
  ['educacion', 'Educación de las mujeres: finalización de la secundaria y de la universidad por sexo (Argentina, Latinoamérica: CEPAL, UNESCO), jóvenes que no estudian ni trabajan por sexo, carreras STEM, brecha educativa a favor de las mujeres, deserción por maternidad.'],
  ['violencia_abuso', 'Violencia y abuso: datos oficiales de violencia contra las mujeres (Registro Único de Casos de Violencia contra las Mujeres, Línea 144, Registro Nacional de Femicidios de la Corte Suprema, Ministerio de Seguridad, ONU Mujeres, OMS), abuso sexual en la infancia, trata de personas. Presentá los datos con equilibrio y con fuente oficial.'],
  ['adicciones_pantallas', 'Adicciones y pantallas: consumo de alcohol, tabaco y otras sustancias por sexo (SEDRONAR, OPS), apuestas online en mujeres, redes sociales y salud mental de las adolescentes (UNICEF, OMS HBSC, Pew, Common Sense), ciberacoso, consumo de pornografía en mujeres (Barna y estudios académicos).'],
  ['soledad_amistad', 'Soledad y amistad: soledad por sexo y edad (OMS Comisión sobre Conexión Social, Gallup, Survey Center on American Life), mujeres mayores que viven solas y viudez (INDEC, Censo 2022), cuidadoras, amistad entre mujeres, datos de Argentina y Latinoamérica si existen.'],
  ['fe_iglesia', 'Fe e iglesia: brecha de género en la religiosidad (Pew Research Center), religiosidad en Argentina (Encuesta CONICET 2008 y 2019), mujeres en la iglesia evangélica, Barna sobre mujeres y fe, tendencias recientes de mujeres jóvenes (Gen Z) y su relación con la iglesia (Pew, Gallup, Barna 2023-2026).'],
  ['cultura_identidad', 'Cultura e identidad: qué significa ser mujer hoy (Pew, Ipsos, Gallup), feminismo y percepciones, ideología de género en jóvenes, redes sociales, comparación y autoestima (Dove Self-Esteem Project, OMS), brecha ideológica entre mujeres jóvenes y varones jóvenes (Gallup, Financial Times), datos de Argentina y Latinoamérica si existen.'],
  ['articulos_identidad', 'Artículos de sitios cristianos protestantes confiables sobre la mujer según la Biblia, su identidad, su valor, su diseño y la belleza verdadera: Coalición por el Evangelio (coalicionporelevangelio.org), Aviva Nuestros Corazones (avivanuestroscorazones.com, Mujer Verdadera), The Gospel Coalition, Desiring God, Ligonier, CBMW, Crossway, 9Marks. Mínimo 8 artículos, cada uno con sus ideas clave y su URL. En "datos" poné solo estadísticas que esos artículos citen con fuente.'],
  ['articulos_esposa_madre', 'Artículos de sitios cristianos protestantes confiables sobre la mujer como esposa y como madre: respeto y sumisión según la Biblia, ayuda idónea, orar por el esposo, esposo no creyente, intimidad, crianza, maternidad, hijos adolescentes, madres solas: Coalición por el Evangelio, Aviva Nuestros Corazones, The Gospel Coalition, Desiring God, Ligonier, CBMW, Crossway. Mínimo 10 artículos, cada uno con sus ideas clave y su URL.'],
  ['articulos_iglesia_servicio', 'Artículos de sitios cristianos protestantes confiables sobre la mujer en la iglesia: dones, servicio, hospitalidad, enseñar a otras mujeres, discipulado, roles de varones y mujeres (posturas complementaria e igualitaria, atribuidas a quien las sostiene), mujeres del Nuevo Testamento: Coalición por el Evangelio, Aviva Nuestros Corazones, The Gospel Coalition, Desiring God, Ligonier, CBMW, Crossway. Mínimo 8 artículos, cada uno con sus ideas clave y su URL.'],
  ['articulos_etapas', 'Artículos de sitios cristianos protestantes confiables sobre las etapas de la mujer: adolescente, joven, soltera y noviazgo, pureza, vocación, mujer del medio, abuela, viuda y vejez, mentoría de Tito 2: Coalición por el Evangelio, Aviva Nuestros Corazones, The Gospel Coalition, Desiring God, Ligonier, CBMW, Crossway. Mínimo 10 artículos, cada uno con sus ideas clave y su URL.'],
  ['articulos_sufrimiento', 'Artículos de sitios cristianos protestantes confiables sobre el sufrimiento de la mujer: infertilidad, pérdida de un embarazo o de un hijo, aborto y sanidad, abuso, depresión, ansiedad, duelo, divorcio, enfermedad, con cuidado pastoral: Coalición por el Evangelio, Aviva Nuestros Corazones, The Gospel Coalition, Desiring God, Ligonier, CBMW, Crossway. Mínimo 10 artículos, cada uno con sus ideas clave y su URL.'],
]
const prompt = ([k, d]) => `Sos investigador para un estudio bíblico sobre la mujer según el diseño de Dios, escrito para una mujer cristiana protestante de Buenos Aires. Tu tema: ${d}

Cargá las herramientas WebSearch y WebFetch con ToolSearch ("select:WebSearch,WebFetch") y buscá a fondo (varias búsquedas, en castellano y en inglés). Prioridad: datos de Argentina y Latinoamérica primero, y además datos internacionales para comparar.

Reglas:
1. Solo fuentes confiables: organismos oficiales (INDEC, Ministerio de Salud, SEDRONAR, OPS, OMS, ONU, CEPAL, OIT, UNESCO, UNODC, Banco Mundial), estudios académicos, encuestadoras serias (Pew, Gallup, Barna, Ipsos) y, para artículos, sitios cristianos protestantes reconocidos (Coalición por el Evangelio, The Gospel Coalition, Desiring God, 9Marks, Ligonier, CBMW, Crossway, Aviva Nuestros Corazones). Nada de blogs anónimos ni sitios sin respaldo.
2. NO INVENTES NINGÚN NÚMERO. Cada dato lleva la frase textual de donde sale, el año al que corresponde, la fuente y la URL. Abrí la página (WebFetch) para verificarlo; si solo lo viste en un resultado de búsqueda o en una nota periodística, marcá verificado_en_fuente=false y en "notas" decí cuál es la fuente original.
3. Preferí el dato más reciente disponible y decí siempre de qué año es.
4. Entre 15 y 25 datos útiles (o los artículos que pide el tema), sin repetir. Calidad antes que cantidad.
5. Abrí con WebFetch CADA página de la que saques un dato o un artículo; lo que no puedas abrir, no lo incluyas. Seguí buscando hasta llegar al mínimo pedido.
6. En "pendientes", contá qué buscaste y no encontraste en una fuente confiable.
Devolvé el resultado con la herramienta de salida estructurada.`
const SEL = (args && args.temas) ? TEMAS.filter(t => args.temas.includes(t[0])) : TEMAS
const res = await parallel(SEL.map(t => () => agent(prompt(t), { label: `web:${t[0]}`, phase: 'Investigar', schema: SCHEMA, ...(args && args.opciones || {}) })))
return res.map((r, i) => ({ tema: SEL[i][0], datos: r ? r.datos.length : 0, articulos: r ? r.articulos.length : 0 }))
