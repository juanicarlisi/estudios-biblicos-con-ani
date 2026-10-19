export const meta = {
  name: 'genesis-revisar-continuidad',
  description: 'Revisa la continuidad entre días seguidos del estudio de Génesis (antes/después, fechas, contradicciones, repeticiones) y verifica cada hallazgo',
  phases: [
    { title: 'Revisar', detail: 'una ventana de 6 días por agente' },
    { title: 'Verificar', detail: 'un escéptico por ventana descarta lo que no es un problema real' },
  ],
}
const HALLAZGOS = { type: 'object', properties: { hallazgos: { type: 'array', items: { type: 'object', properties: {
  dia: { type: 'integer' }, campo: { type: 'string', description: 'p. ej. contexto.despues o secciones[2].notas[1]' },
  tipo: { type: 'string', enum: ['continuidad', 'contradiccion', 'cronologia', 'repeticion', 'error_texto'] },
  problema: { type: 'string' }, texto_actual: { type: 'string', description: 'fragmento EXACTO del campo a reemplazar' },
  texto_nuevo: { type: 'string', description: 'reemplazo del fragmento' }, justificacion: { type: 'string' },
}, required: ['dia', 'campo', 'tipo', 'problema', 'texto_actual', 'texto_nuevo', 'justificacion'] } } }, required: ['hallazgos'] }
const VEREDICTOS = { type: 'object', properties: { veredictos: { type: 'array', items: { type: 'object', properties: {
  indice: { type: 'integer' }, real: { type: 'boolean' }, texto_nuevo: { type: 'string', description: 'el reemplazo, corregido si hace falta' }, motivo: { type: 'string' },
}, required: ['indice', 'real', 'texto_nuevo', 'motivo'] } } }, required: ['veredictos'] }
const n2 = n => String(n).padStart(2, '0')
const revisar = i => `Revisás la continuidad de un estudio de Génesis en días de lectura (unos 20 versículos por día). Leé con UNA llamada a Read (allow_large: true) /home/user/trabajo/revision/continuidad_${n2(i)}.txt: trae seis días seguidos con su contexto (antes, ahora, dónde, cuándo, después), el panorama y cada nota. Cada día ya fue verificado contra sus fuentes; lo que buscás son problemas ENTRE días:
1. continuidad: el «antes» de un día no coincide con lo que cubrió el día anterior, o el «después» no coincide con lo que trae el día siguiente (mirá su pasaje y su contenido).
2. contradiccion / cronologia: dos días afirman datos incompatibles (edades, años, fechas, lugares, quién hizo qué) sin aclarar que son posturas de fuentes distintas.
3. repeticion: la misma explicación desarrollada casi igual en dos días seguidos (proponé acortar la del segundo a una referencia breve, p. ej. «como vieron el día N…»).
4. error_texto: algo que contradice el propio relato bíblico tal como lo resumen los demás días (un nombre cambiado, un orden de hechos equivocado).
Reglas: la corrección usa SOLO información que ya está en estos días (no agregues datos nuevos); si dos fuentes difieren, la corrección atribuye cada dato a su fuente en vez de elegir. "texto_actual" debe ser un fragmento copiado EXACTO del campo. Sé exigente: no informes cuestiones de estilo ni preferencias; solo problemas reales que confundirían al lector. Si no hay problemas, devolvé la lista vacía. Usá solo Read y la salida estructurada.`
const verificar = (i, hs) => `Sos un revisor escéptico. Otro agente propuso estas correcciones de continuidad para un estudio de Génesis. Leé con Read (allow_large: true) /home/user/trabajo/revision/continuidad_${n2(i)}.txt y juzgá cada una: ¿es un problema real que confundiría al lector? ¿El "texto_actual" figura exactamente en ese campo? ¿El reemplazo usa solo información que ya está en el estudio, sin agregar datos ni tomar partido entre fuentes? Por defecto, si dudás, marcá real=false. Si es real pero el reemplazo tiene un defecto, corregí "texto_nuevo".

Propuestas (el índice es su posición en la lista):
${hs.map((h, k) => `[${k}] día ${h.dia} · ${h.campo} · ${h.tipo}\n  problema: ${h.problema}\n  texto_actual: «${h.texto_actual}»\n  texto_nuevo: «${h.texto_nuevo}»\n  justificación: ${h.justificacion}`).join('\n\n')}

Devolvé un veredicto por propuesta con la salida estructurada. Usá solo Read y la salida estructurada.`
const ventanas = (args && args.ventanas) || Array.from({ length: 14 }, (_, k) => k + 1)
const res = await pipeline(
  ventanas,
  i => agent(revisar(i), { label: `revisar:v${n2(i)}`, phase: 'Revisar', schema: HALLAZGOS }),
  (r, i) => !r || !r.hallazgos.length ? { ventana: i, hallazgos: [], veredictos: [] }
    : agent(verificar(i, r.hallazgos), { label: `verificar:v${n2(i)}`, phase: 'Verificar', schema: VEREDICTOS })
        .then(v => ({ ventana: i, hallazgos: r.hallazgos, veredictos: v ? v.veredictos : null })),
)
return res
