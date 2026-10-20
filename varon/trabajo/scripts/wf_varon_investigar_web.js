export const meta = {
  name: 'varon-investigar-web',
  description: 'Investiga en sitios confiables estadísticas (Argentina y Latinoamérica primero, más internacionales) y artículos cristianos sobre el varón',
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
  ['salud_mental', 'Salud mental y suicidio en los varones: tasas de suicidio por sexo y edad (Argentina: Ministerio de Salud, Boletín Epidemiológico Nacional, DEIS; Latinoamérica: OPS; mundial: OMS), depresión no diagnosticada, consultas de salud mental por sexo, suicidio en varones mayores.'],
  ['mortalidad', 'Esperanza de vida y mortalidad por sexo: brecha de esperanza de vida varones/mujeres (INDEC, OPS, OMS, Banco Mundial), causas externas (accidentes de tránsito, homicidios, violencia) por sexo, "muertes por desesperación", varones y cuidado de la salud (menos consultas médicas).'],
  ['adicciones', 'Adicciones por sexo: alcohol, drogas, tabaco, apuestas y juego online (Argentina: SEDRONAR, Observatorio Argentino de Drogas, encuestas de apuestas en adolescentes; Latinoamérica: OPS, CICAD; mundial: OMS, UNODC).'],
  ['pornografia', 'Pornografía: edad de primer contacto, consumo por sexo y edad, efectos en relaciones y salud (estudios académicos, encuestas como Barna "The Porn Phenomenon", estudios argentinos y latinoamericanos, datos de plataformas solo si los cita una fuente seria).'],
  ['familia', 'Familia y paternidad: hogares monoparentales y con jefatura femenina (Argentina: Censo 2022 INDEC, EPH), tasas de matrimonio y divorcio, natalidad y fecundidad, edad al casarse, nacimientos fuera del matrimonio, efectos de la ausencia del padre en los hijos (estudios académicos), tiempo que los padres pasan con sus hijos.'],
  ['educacion_trabajo', 'Educación y trabajo de los varones: abandono escolar y finalización de secundaria y universidad por sexo (Argentina, Latinoamérica: CEPAL, UNESCO), jóvenes que no estudian ni trabajan por sexo, desempleo e informalidad (INDEC EPH, OIT), brecha educativa a favor de las mujeres, datos de Richard Reeves ("Of Boys and Men", Brookings / American Institute for Boys and Men).'],
  ['soledad', 'Soledad y amistad masculina: encuestas sobre cantidad de amigos cercanos por sexo (Survey Center on American Life, Gallup, Meta-Gallup), soledad en varones jóvenes y mayores, OMS (Comisión sobre conexión social 2025), uso de pantallas y videojuegos en varones jóvenes, datos de Argentina y Latinoamérica si existen.'],
  ['fe_iglesia', 'Fe e iglesia: brecha de género en la religiosidad (Pew Research Center), evangélicos y religiosidad en Argentina (Encuesta Nacional sobre Creencias y Actitudes Religiosas, CONICET 2008 y 2019), varones en la iglesia evangélica, Barna sobre hombres y fe, tendencias recientes de varones jóvenes que vuelven a la iglesia (Bible Society "The Quiet Revival" 2025, Barna 2025).'],
  ['violencia_delito', 'Violencia, delito y cárcel: población carcelaria por sexo (SNEEP Argentina, World Prison Brief), víctimas y autores de homicidio por sexo (UNODC, Ministerio de Seguridad), siniestros viales por sexo, violencia doméstica (presentar datos con equilibrio y fuente oficial).'],
  ['masculinidad_cultura', 'Masculinidad y cultura: encuestas sobre qué significa ser hombre hoy (Pew, Ipsos, Equimundo "State of American Men"), confusión de identidad, influencia de la "manosfera" e influencers en varones jóvenes, brecha ideológica entre varones y mujeres jóvenes (Financial Times 2024, Gallup), datos latinoamericanos si existen.'],
  ['articulos_identidad', 'Artículos de sitios cristianos confiables sobre la masculinidad bíblica, la identidad del varón, la crisis de la masculinidad y el varón y Dios: Coalición por el Evangelio (coalicionporelevangelio.org), The Gospel Coalition, Desiring God, 9Marks, Ligonier, CBMW (Council on Biblical Manhood and Womanhood), Crossway, Soldados de Jesucristo (no), Ministerios Ligonier en español, Revista 9Marcas. Reuní las ideas clave de cada artículo con su URL. En "datos" poné solo estadísticas que esos artículos citen con fuente.'],
  ['articulos_roles', 'Artículos de sitios cristianos confiables sobre el varón como esposo, padre, trabajador, líder en la iglesia, siervo, joven y adulto mayor: Coalición por el Evangelio, The Gospel Coalition, Desiring God, 9Marks, Ligonier, CBMW, Crossway. Reuní las ideas clave de cada artículo con su URL (al menos dos artículos por rol). En "datos" poné solo estadísticas que esos artículos citen con fuente.'],
]
const prompt = ([k, d]) => `Sos investigador para un estudio bíblico sobre el varón según el diseño de Dios, escrito para un hombre cristiano protestante de Buenos Aires. Tu tema: ${d}

Cargá las herramientas WebSearch y WebFetch con ToolSearch ("select:WebSearch,WebFetch") y buscá a fondo (varias búsquedas, en castellano y en inglés). Prioridad: datos de Argentina y Latinoamérica primero, y además datos internacionales para comparar.

Reglas:
1. Solo fuentes confiables: organismos oficiales (INDEC, Ministerio de Salud, SEDRONAR, OPS, OMS, ONU, CEPAL, OIT, UNESCO, UNODC, Banco Mundial), estudios académicos, encuestadoras serias (Pew, Gallup, Barna, Ipsos) y, para artículos, sitios cristianos protestantes reconocidos (Coalición por el Evangelio, The Gospel Coalition, Desiring God, 9Marks, Ligonier, CBMW, Crossway). Nada de blogs anónimos ni sitios sin respaldo.
2. NO INVENTES NINGÚN NÚMERO. Cada dato lleva la frase textual de donde sale, el año al que corresponde, la fuente y la URL. Abrí la página (WebFetch) para verificarlo; si solo lo viste en un resultado de búsqueda o en una nota periodística, marcá verificado_en_fuente=false y en "notas" decí cuál es la fuente original.
3. Preferí el dato más reciente disponible y decí siempre de qué año es.
4. Entre 10 y 25 datos útiles (o artículos, según el tema), sin repetir. Calidad antes que cantidad.
5. En "pendientes", contá qué buscaste y no encontraste en una fuente confiable.
Devolvé el resultado con la herramienta de salida estructurada.`
const res = await parallel(TEMAS.map(t => () => agent(prompt(t), { label: `web:${t[0]}`, phase: 'Investigar', schema: SCHEMA })))
return res.map((r, i) => ({ tema: TEMAS[i][0], datos: r ? r.datos.length : 0, articulos: r ? r.articulos.length : 0 }))
