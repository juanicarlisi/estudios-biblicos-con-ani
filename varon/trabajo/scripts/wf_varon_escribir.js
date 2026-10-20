export const meta = {
  name: 'varon-escribir',
  description: 'Escribe cada día del estudio del varón a partir de sus notas (sin inventar) y lo verifica contra las notas y los datos',
  phases: [
    { title: 'Escribir', detail: 'un día por agente, a partir de su archivo de insumos' },
    { title: 'Verificar', detail: 'otro agente coteja cada afirmación con sus notas y cada cifra con su fuente' },
  ],
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
const escribir = d => `Vas a escribir el DÍA ${d} de «El varón según el diseño de Dios», un estudio bíblico diario para un hombre cristiano protestante de Buenos Aires que le dedica 20 a 30 minutos por día. Quiere conocer a fondo lo que Dios dice del varón y vivirlo.

Leé con Read (allow_large: true):
1. /home/user/trabajo/varon/insumos/dia_${n3(d)}.txt: el plan del día, dónde está dentro de su parte (días anterior y siguiente) y TODAS las notas que le tocan, sacadas de libros de autores protestantes confiables, cada una con su id entre corchetes, más los datos y artículos de la web (ids W…) si los hay.
2. /home/user/trabajo/varon/plan/esquema_dia.md: el formato y sus reglas.
Después devolvé el día con la herramienta de salida estructurada. No uses otras herramientas.

Reglas de oro:
1. NO INVENTAR NADA. Cada afirmación sale de las notas o de los datos del insumo y lleva en "fuentes" los ids que la respaldan (p. ej. "b_014#7", "W0012"). Si varias notas dicen lo mismo, condensalo en una sola afirmación con todos sus ids. Nada de conocimiento propio: si algo no está en el insumo, no va. Tampoco cifras ni fechas que no estén.
2. CONDENSAR CON CRITERIO: no es una lista de notas sino un estudio que se lee de corrido, con un hilo claro de principio a fin, que sigue el plan del día. Uní lo que repiten varios autores, priorizá lo central (importancia 3 y 2), lo bíblico y lo que ayuda a vivir. Lo valioso que no entra va a "profundizar". Si dejás afuera notas de importancia 3, decí cuáles y por qué en "notas_no_usadas".
3. LA BIBLIA PRIMERO: el estudio se apoya en las Escrituras; los autores ayudan a entenderlas. Las referencias bíblicas van con el nombre castellano completo del libro («Efesios 5:25»).
4. INTERPRETACIONES: cuando las fuentes difieren, presentá cada postura con quién la sostiene, sin tomar partido salvo que todas coincidan.
5. TONO: hablale de «vos», en castellano rioplatense, cálido, directo y claro, como un hermano mayor sabio. Frases cortas. Explicá los términos técnicos la primera vez. Nada de relleno, de frases hechas ni de sermón. No encadenes «según X… Y agrega… Z dice…»: nombrá al autor solo cuando aporta algo propio (una postura, una frase memorable, una experiencia) o cuando las fuentes difieren; lo demás se afirma directamente y las fuentes quedan en "fuentes" (la app las muestra como etiquetas). Las historias y ejemplos de los autores se cuentan como de ellos («Un pastor cuenta que…»), nunca como propios. Temas delicados (suicidio, depresión, abuso, adicciones, divorcio, duelo): con cuidado pastoral, sin frases ambiguas que un lector frágil pueda tomar mal, con la gracia de Cristo junto al llamado y animando a pedir ayuda a alguien de confianza, al pastor o a un profesional (la app agrega las líneas de ayuda oficiales; no escribas teléfonos).
6. DATOS: decí siempre el año y el lugar de cada cifra; los datos viejos de un libro se presentan como tales («en 1990, en Estados Unidos…»). Argentina y Latinoamérica primero; los internacionales al lado. Con respeto: el diagnóstico no es para condenar sino para entender. Si un dato trae una «ESTIMACIÓN propia» (un cálculo de quien juntó los datos), no la uses: solo las cifras que da la fuente.
7. CONTINUIDAD: el insumo dice qué vino antes y qué sigue; arrancá conectando con el día anterior cuando sirva y no repitas lo que otro día de la parte ya trata.
8. LARGO: el cuerpo principal (entrada, apartados, citas, datos, modelo, palabras, interpretaciones, conexiones, para_vivir) suma entre 2.000 y 2.500 palabras, nunca más de 2.600: tiene que poder leerse y pensarse en 20 a 30 minutos junto con el pasaje. "minutos.estudio" entre 20 y 30. Lo valioso que no entra va a "profundizar", que es optativo y aparte.
9. "versiculos": 1 a 3 referencias clave (la app pone el texto RVR1960); no copies texto bíblico largo en el estudio.
10. "para_reflexionar": 3 preguntas personales y concretas; "para_conversar": 0 a 2 preguntas para charlar con su esposa o con un amigo; "para_orar": una oración breve, en primera persona, que convierta lo aprendido en oración.
11. "dia" = ${d}. Si un campo no tiene material (modelo, palabras, datos, interpretaciones), dejalo vacío; no lo rellenes. Si no hay modelo, devolvé "modelo" con persona y texto vacíos.`
const verificar = d => `Sos el verificador de un estudio bíblico que no puede contener nada inventado. Leé con Read (allow_large: true) el insumo /home/user/trabajo/varon/insumos/dia_${n3(d)}.txt y las reglas de /home/user/trabajo/varon/plan/esquema_dia.md. Abajo está el borrador del día ${d}.

Revisá TODO el borrador:
1. Cada afirmación tiene que estar respaldada por los ids que cita en "fuentes" (buscalos en el insumo). Corregí lo que exagere, mezcle autores o agregue algo que las notas no dicen; si algo no tiene respaldo, sacalo. Si un id no existe en el insumo, poné el correcto o sacá la afirmación.
2. Las cifras, años y lugares tienen que coincidir exactamente con el dato del insumo (W… o nota de tipo dato); las «ESTIMACIÓN propia» que traen algunos datos no se usan.
3. Lo que se atribuye a un autor (citas, interpretaciones, historias) tiene que ser de ese autor; las "citas" tienen que ser textuales de una "Cita textual" del insumo.
4. Palabras griegas o hebreas: solo las que comentan las notas; la grafía original solo si la nota la trae (si no, dejá "original" vacío).
5. Que no haya doctrina rara ni afirmaciones teológicas que las notas no sostienen.
6. El castellano: claro, de «vos», sin repetir ideas y sin encadenar atribuciones («según X… Y agrega…»).
7. LA BIBLIA: todo lo que el texto dice que dice un versículo (palabras entre comillas, resúmenes, nombres, quién dijo qué) tiene que coincidir con la RVR1960. Comprobalo con: python3 /home/user/trabajo/varon/scripts/rvr_ver.py "Libro C:V" ["Libro C:V-V" …] (muestra el texto RVR1960; podés pasar varias referencias juntas). Revisá también que las referencias existan y digan lo que se les atribuye.
8. Largo: el cuerpo principal (entrada, apartados, citas, datos, modelo, palabras, interpretaciones, conexiones, para_vivir) tiene que quedar entre 2.000 y 2.600 palabras; si se pasa, pasá lo menos central a "profundizar". Si sacás algo, no lo reemplaces con material propio.
Devolvé el día completo y corregido con la herramienta de salida estructurada (mismo esquema). Usá solo Read, Bash (únicamente para rvr_ver.py) y la salida estructurada.`
const res = await pipeline(
  args.dias,
  d => agent(escribir(d), { label: `escribir:dia${n3(d)}`, phase: 'Escribir', schema: SCHEMA }),
  (r, d) => r ? agent(`${verificar(d)}\n\nBORRADOR:\n${JSON.stringify(r)}`, { label: `verificar:dia${n3(d)}`, phase: 'Verificar', schema: SCHEMA }).then(v => ({ dia: d, ok: !!v })) : { dia: d, ok: false },
)
return res
