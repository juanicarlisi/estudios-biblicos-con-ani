#!/usr/bin/env python3
"""Plan maestro del megaestudio: ciclos → series → días (estimados). Genera ciclos.json y PLAN-MAESTRO.md.
Cada serie: (id, título, días, enfoque, [secciones del pedido: A–O, 2–8], [equivalencias IBBA/TMS], fuentes (B=biblioteca, X=externas a conseguir y verificar)).
El plan se detalla día por día solo para el ciclo que se va a escribir (oleadas), para no fijar de antemano lo que el material va a mostrar."""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__))

C = []
def ciclo(n, titulo, bajada, series): C.append({'id': f'C{n}', 'numero': n, 'titulo': titulo, 'bajada': bajada, 'series': [
    {'id': f'{n}.{i}', 'titulo': s[0], 'dias': s[1], 'enfoque': s[2], 'pedido': s[3], 'institutos': s[4], 'fuentes': s[5]} for i, s in enumerate(series, 1)]})

ciclo(1, 'La Biblia: la Palabra de Dios y cómo leerla', 'Antes de estudiar los temas, entender qué es la Biblia, por qué confiar en ella y cómo se interpreta bien.', [
    ('Para qué estudiamos la Biblia: conocer a Dios', 6, 'La meta de todo estudio; revelación general y especial; inspiración, inerrancia, suficiencia, claridad y autoridad.', '4 Bibliología', 'TMS TH605 · IBBA Teología I', 'B: Grudem, MacArthur, Berkhof, Ryrie, Packer, Owen'),
    ('Cómo llegó a nosotros: canon, manuscritos y traducciones', 10, 'Historia del canon AT y NT, Septuaginta, rollos del Mar Muerto, manuscritos griegos, crítica textual, versiones y diferencias entre traducciones.', '4 Canon/manuscritos/traducciones; 3 Arqueología', 'TMS NT601, BI784 · IBBA Panorama y métodos', 'B + X (Metzger, Bruce; sociedades bíblicas)'),
    ('Cómo interpretar: hermenéutica, exégesis y estudio inductivo', 20, 'Estudio bíblico inductivo (observar, interpretar, aplicar), contexto literario e histórico-cultural, géneros (narrativa, ley, poesía, sabiduría, profecía, apocalíptica, evangelios, epístolas), análisis de palabras, uso del AT en el NT, pasajes difíciles.', '4 Hermenéutica/Exégesis/Géneros', 'TMS BI505, BI705 · IBBA Hermenéutica', 'B: Grudem, Lacueva, comentarios; X'),
    ('Las lenguas de la Biblia: hebreo, arameo y griego koiné', 8, 'Cómo leer una palabra en su idioma sin ser experto: alfabetos, raíces, Strong, errores comunes (falacias léxicas).', '4 Hebreo/Arameo/Griego/Septuaginta', 'TMS OT503, NT501 · IBBA Griego/Hebreo', 'X (Strong, léxicos) + B (diccionarios Mundo Hispano)'),
    ('La Biblia en un vistazo: la historia de la redención', 10, 'Una sola historia en seis actos: creación, caída, promesa, redención, iglesia, consumación; cómo se relacionan los 66 libros.', '2 Teología bíblica', 'IBBA Panorama · TMS BI501/502', 'B + biblioteca MATERIAL SOPORTE'),
])
ciclo(2, 'Dios: su carácter, su naturaleza y su obra', 'Quién es Dios según las Escrituras, y cómo se revela de Génesis a Apocalipsis.', [
    ('Conocer a Dios y sus nombres', 10, 'Elohim, YHWH, Adonai, El Shaddai y los demás; nombres compuestos; qué significa conocer a Dios.', 'A Nombres de Dios', 'IBBA Teología I', 'B: Packer, Tozer, Pink, Grudem'),
    ('Los atributos de Dios', 30, 'Incomunicables y comunicables; santidad, amor, justicia, misericordia, gracia, fidelidad, soberanía, omnisciencia, omnipotencia, omnipresencia, eternidad, inmutabilidad, sabiduría, paciencia, ira, compasión, verdad, gloria; amor y santidad; justicia y misericordia.', 'A Atributos', 'TMS TH643 · IBBA Teología I', 'B: Pink, Tozer, Packer, Grudem, Berkhof, MacArthur, Washer, Sproul'),
    ('La Trinidad', 12, 'Un solo Dios en tres personas: fundamentos bíblicos, historia (Nicea, Calcedonia), errores (modalismo, arrianismo), relaciones entre las personas.', 'A/B/C Trinidad; 5 Credos', 'TMS TH605 · IBBA Teología I', 'B: Doctrina de la trinidad, Qué es la trinidad, Grudem, Owen, Ferguson'),
    ('La voluntad, la providencia y la soberanía de Dios', 14, 'Decreto, providencia, mal y sufrimiento, soberanía y responsabilidad humana, posturas calvinista y arminiana.', 'A Voluntad/Soberanía; 8 Providencia/Responsabilidad', 'TMS PM514 · IBBA Teología I', 'B: Soberanía, Controla Dios todas las cosas, MacArthur, Edwards, Piper'),
    ('Su presencia, su gloria y su rostro', 10, 'La nube, el tabernáculo, el rostro de Dios, el silencio de Dios, el temor de Dios.', 'A Presencia/Gloria/Temor; 8 Rostro/Silencio', '—', 'B: Tozer, Piper, Owen + comentarios'),
    ('Dios a lo largo de toda la Biblia', 8, 'Cómo se presenta Dios en el Pentateuco, los profetas, los Salmos, los Evangelios y Apocalipsis.', 'A Revelación a lo largo de la Biblia', '—', 'B'),
])
ciclo(3, 'Jesucristo: su persona, su vida y su obra', 'Quién es Jesús, qué hizo y cómo el AT lo anticipa.', [
    ('Quién es Jesús: preexistencia, deidad, humanidad y encarnación', 18, 'Nombres y títulos; Hijo de Dios, Hijo del Hombre; credos cristológicos; herejías antiguas y actuales.', 'B Identidad', 'IBBA Teología II · TMS TH606', 'B: Sproul, Stott, Grudem, MacArthur, Chafer'),
    ('Cristo en el Antiguo Testamento: profecías y tipos', 18, 'Mesías prometido; profecías explícitas, cumplimientos señalados por los autores, tipología.', 'B/O/2', 'TMS OT770', 'B + comentarios'),
    ('La vida y las enseñanzas de Jesús', 34, 'Recorrido por los Evangelios: nacimiento, bautismo, tentación, ministerio, parábolas, milagros, encuentros, camino a Jerusalén.', 'B Vida/Enseñanzas/Parábolas/Milagros/Encuentros', 'TMS NT675, BI675 · IBBA Jesús el modelo', 'B: MacArthur, Barclay, Guzik, Moody, Pink, Carballosa'),
    ('La obra de Cristo: cruz, resurrección y reinado', 30, 'Obediencia, sacrificio, expiación, propiciación, rescate, resurrección, ascensión, intercesión, reinado actual y segunda venida.', 'B Obra; D Cruz/Resurrección', 'TMS TH754 · IBBA Teología paulina de la cruz', 'B: Stott, Owen, Murray, MacArthur'),
    ('Los oficios y las imágenes de Cristo', 14, 'Profeta, sacerdote, rey, cordero, pastor, mediador, luz, pan, vid, roca.', 'B Profeta/Sacerdote/Rey/Cordero/Pastor/Mediador', 'TMS TH750', 'B'),
])
ciclo(4, 'El Espíritu Santo', 'Su persona, su obra en cada época y su obra en el creyente.', [
    ('La persona del Espíritu', 10, 'Divinidad, personalidad, relación con el Padre y el Hijo.', 'C', 'IBBA Teología II', 'B: Owen Pneumatología, Grudem, MacArthur'),
    ('El Espíritu en el Antiguo y en el Nuevo Testamento', 12, 'Creación, profetas, Pentecostés, nuevo pacto.', 'C', '—', 'B'),
    ('La obra del Espíritu en el creyente', 16, 'Regeneración, convicción, santificación, llenura, guía, morada, sello, bautismo.', 'C', 'TMS TH606', 'B'),
    ('Dones y fruto del Espíritu: posturas cesacionista y continuacionista', 12, 'Dones espirituales y las distintas lecturas cristianas.', 'C; 5 Pentecostalismo', 'TMS TH786', 'B: MacArthur, Grudem; X'),
    ('Resistir al Espíritu y discernir', 6, 'Endurecimiento, apagar, entristecer, blasfemia contra el Espíritu, discernimiento espiritual.', 'C', '—', 'B'),
])
ciclo(5, 'El ser humano, el pecado y el mal', 'Qué somos, qué se rompió y cómo funciona la lucha espiritual.', [
    ('Imagen de Dios e identidad humana', 14, 'Creación, imagen, hombre y mujer, alma, espíritu, corazón, mente, conciencia, voluntad, emociones, personalidad y temperamento.', 'K', 'IBBA Antropología, Teología de la naturaleza humana · TMS TH705', 'B + X'),
    ('La caída y el pecado', 16, 'Origen y naturaleza del pecado, caída, muerte espiritual, culpa, condenación, esclavitud.', 'H; D Pecado', 'TMS TH705', 'B'),
    ('Pecados y obras de la carne', 24, 'Idolatría, orgullo, codicia, envidia, celos, ira, amargura, hipocresía, incredulidad, mentira, engaño.', 'H', '—', 'B (Pecado, Tentación y Sexualidad)'),
    ('Tentación y lucha espiritual', 12, 'Carne y Espíritu, armadura de Dios, autoridad espiritual.', 'H', 'IBBA Confrontación de poderes', 'B'),
    ('Ángeles, demonios y el diablo', 14, 'Angelología y demonología; ángeles caídos; victoria de Cristo.', 'H; 4 Angelología/Demonología', 'TMS TH606', 'B: Angeología vol. 2; Guerra espiritual'),
])
ciclo(6, 'Salvación y evangelio', 'El plan de salvación en toda su extensión, con las distintas posturas cristianas.', [
    ('Creación, caída y necesidad de redención', 6, 'El problema que el evangelio resuelve.', 'D', '—', 'B'),
    ('Gracia, fe y arrepentimiento', 12, '', 'D', '—', 'B: Sproul, Piper, Owen'),
    ('Justificación, regeneración y adopción', 18, 'Imputación, nuevo nacimiento, adopción, reconciliación.', 'D', 'TMS TH720', 'B: Murray, Stott'),
    ('Expiación, propiciación y rescate', 12, 'Teorías de la expiación; extensión de la expiación.', 'D', 'TMS TH754', 'B: Owen, Stott, Murray'),
    ('Santificación y glorificación', 12, '', 'D', '—', 'B'),
    ('Elección, predestinación y libre albedrío', 16, 'Calvinismo, arminianismo y otras posturas con sus textos.', 'D', 'TMS TH720', 'B: Edwards, Owen, Piper + X (arminianos)'),
    ('Seguridad, perseverancia y obras', 12, '', 'D', '—', 'B'),
    ('La vida eterna', 6, '', 'D/N', '—', 'B'),
])
ciclo(7, 'Teología bíblica: los hilos que unen toda la Escritura', 'Cómo imágenes, instituciones y acontecimientos del AT se conectan con Cristo y con el NT, sin forzar alegorías.', [
    ('Creación y nueva creación: del Edén a la Nueva Jerusalén', 14, 'Edén, árbol de la vida, Apocalipsis y Génesis.', '2', 'TMS BI715/716', 'B + comentarios'),
    ('La promesa: simiente, Abraham y las naciones', 12, '', '2', '—', 'B'),
    ('Los pactos de Dios', 20, 'Noé, Abraham, Moisés, David y nuevo pacto.', 'E; 2', 'TMS BI715', 'B'),
    ('Éxodo, desierto y tierra prometida', 16, 'El patrón del éxodo y su eco en la redención.', '2', 'TMS BI656', 'B'),
    ('Tabernáculo, templo, sacerdocio y sacrificios', 30, 'Cordero, sangre, perdón, expiación; Hebreos.', '2', 'TMS BI656 · IBBA Hebreos', 'B + comentarios'),
    ('Presencia, gloria y trono', 12, '', '2; 8', '—', 'B'),
    ('Imágenes: luz, agua, pan, vid, pastor, roca, montaña', 20, '', '2; 8', '—', 'B'),
    ('Descanso, sábado, exilio, retorno', 14, '', '2', '—', 'B'),
    ('Las naciones, la misión y la restauración final', 12, '', '2', '—', 'B'),
])
ciclo(8, 'El Reino de Dios y los reinos de la Biblia', 'Cómo se desarrolla el Reino desde Génesis hasta Apocalipsis y qué enseñan los reinos terrenales sobre poder, soberanía, idolatría y justicia.', [
    ('El Reino de Dios: de Génesis a Apocalipsis', 20, 'Reino presente y futuro, parábolas del Reino, gobierno de Cristo, consumación.', 'E', 'TMS TH777', 'B + comentarios'),
    ('Israel: de la monarquía unida al exilio', 24, 'Saúl, David, Salomón, reino dividido, Judá e Israel; el pacto davídico y el trono.', 'E', 'TMS BI667, BI779', 'B + X'),
    ('Las potencias: Egipto, Asiria, Babilonia, Persia, Grecia y Roma', 30, 'Cada imperio en su lugar en la historia de la redención.', 'E; 3', 'TMS NT672', 'B + X (historia y arqueología)'),
    ('Los pueblos vecinos: Edom, Moab, Amón, Filistea y otros', 14, '', 'E', '—', 'B + X'),
    ('El Mesías como Rey y la consumación', 14, '', 'E; N', '—', 'B'),
])
ciclo(9, 'La Iglesia, la misión y el discipulado', '', [
    ('Qué es la Iglesia', 18, 'Cuerpo, pueblo, familia, novia, templo; unidad y comunión.', 'M', 'IBBA Iglecrecimiento', 'B'),
    ('Culto, bautismo y Santa Cena', 12, 'Posturas históricas y bíblicas.', 'M; 5', '—', 'B'),
    ('Liderazgo, gobierno de la iglesia y dones', 18, 'Ancianos, pastores, diáconos, formas de gobierno eclesial (episcopal, presbiteriano, congregacional), disciplina eclesiástica, sacerdocio de los creyentes.', 'M', 'TMS PM511A', 'B'),
    ('Misión, evangelismo y Gran Comisión', 14, '', 'M', 'IBBA Misiones', 'B'),
    ('Discipulado y multiplicación', 10, '', 'M', '—', 'B'),
    ('Falsas enseñanzas, apostasía y persecución', 12, '', 'M', '—', 'B'),
])
ciclo(10, 'Carácter cristiano y madurez espiritual', 'El fruto del Espíritu y las virtudes que forman a Cristo en nosotros.', [
    ('El fruto del Espíritu', 36, 'Amor, gozo, paz, paciencia, benignidad, bondad, fe, mansedumbre, templanza: cuatro días cada uno.', 'G', 'IBBA Formación integral del carácter', 'B'),
    ('Virtudes y conceptos espirituales', 60, 'Verdad, sabiduría, discernimiento, humildad, integridad, santidad, obediencia, fidelidad, justicia, misericordia, compasión, valentía, prudencia, pureza, contentamiento, gratitud, esperanza, perseverancia, libertad, responsabilidad.', 'F', '—', 'B'),
    ('Transformación, identidad en Cristo y madurez', 24, 'Renovación de la mente, hábitos, propósito, vocación y llamado.', 'K', '—', 'B'),
])
ciclo(11, 'Oración, adoración y disciplinas espirituales', '', [
    ('La oración', 20, 'Formas de oración, enseñanza de Jesús y de los apóstoles, intercesión.', 'I', 'IBBA Disciplinas espirituales · TMS PM514', 'B'),
    ('Adoración, alabanza y música', 12, '', 'I; 8', 'TMS PM792', 'B'),
    ('Ayuno, meditación, silencio, soledad y vigilias', 14, '', 'I', '—', 'B'),
    ('Confesión, acción de gracias, servicio, generosidad y hospitalidad', 14, '', 'I', '—', 'B'),
])
ciclo(12, 'Ética cristiana y vida cotidiana', 'Cómo los principios bíblicos se aplican a cada dimensión de la vida, incluso a situaciones que la Biblia no nombra.', [
    ('Relaciones: perdón, reconciliación, conflictos, palabra y juicio', 20, '', 'L; 6', 'TMS PM772', 'B'),
    ('Matrimonio, sexualidad, soltería, noviazgo y crianza', 24, '', 'L; 6', 'TMS PM768', 'B (Matrimonio, Familia, Pecado y Sexualidad)'),
    ('Trabajo, dinero y mayordomía', 18, 'Tiempo, recursos, diezmos y ofrendas, deuda, creación, fidelidad en lo pequeño.', 'J', '—', 'B'),
    ('Liderazgo, autoridad, gobierno y justicia social', 16, '', '6', 'TMS PM750', 'B'),
    ('Sufrimiento, prueba y esperanza', 12, '', '6; 8', '—', 'B: Keller'),
    ('Decisiones y dilemas éticos contemporáneos', 14, '', '6', 'IBBA Dilemas éticos · TMS TH780', 'B + X'),
])
ciclo(13, 'Profecía, promesas y últimos tiempos', 'Profecía explícita, cumplimiento, interpretaciones y especulaciones, claramente distinguidas.', [
    ('Cómo funciona la profecía bíblica', 14, 'Género, condicionales e incondicionales, símbolos, lenguaje apocalíptico.', 'O', '—', 'B'),
    ('Profetas mayores y menores', 40, '', 'O', 'IBBA Mensaje profético del AT · TMS BI659', 'B + comentarios'),
    ('Daniel, Zacarías y Apocalipsis', 24, '', 'O; N', 'TMS NT795', 'B (comentarios de Apocalipsis)'),
    ('Escatología: enfoques y pasajes clave', 30, 'Segunda venida, rapto, tribulación, milenio, juicio, cielo, infierno, nuevos cielos y nueva tierra; premilenialismo, amilenialismo, postmilenialismo.', 'N', 'IBBA Teología III · TMS TH706', 'B'),
])
ciclo(14, 'Los libros de la Biblia', 'Panorama y lectura guiada de los 66 libros. Génesis ya está estudiado en profundidad en estudio-genesis.html.', [
    ('Pentateuco (Éxodo a Deuteronomio) y libros históricos', 40, '', '2', 'TMS BI501', 'B + comentarios'),
    ('Poesía y sabiduría', 30, 'Job, Salmos, Proverbios, Eclesiastés, Cantares.', '2', 'TMS BI502', 'B'),
    ('Evangelios y Hechos', 30, '', '2', 'TMS NT601', 'B'),
    ('Cartas de Pablo y cartas generales', 40, '', '2', 'TMS BI756/757/777 · IBBA Romanos, Hebreos, Pastorales', 'B'),
    ('Apocalipsis', 16, '', 'N', '—', 'B'),
])
ciclo(15, 'Personajes y acontecimientos bíblicos', 'Vidas, decisiones, errores y virtudes; milagros, señales, visiones, sueños y encuentros.', [
    ('Personajes del Antiguo Testamento', 60, 'De Adán a Malaquías.', '7', '—', 'B (Personajes bíblicos) + comentarios'),
    ('Personajes del Nuevo Testamento', 40, 'María, Juan el Bautista, Pedro, Juan, Pablo, Esteban, Bernabé, Timoteo.', '7', '—', 'B'),
    ('Acontecimientos, milagros, señales y visiones', 30, '', '7', '—', 'B'),
])
ciclo(16, 'El mundo de la Biblia: historia, geografía y arqueología', '', [
    ('Historia bíblica de Abraham a la Iglesia primitiva', 30, 'Patriarcas, éxodo, conquista, jueces, monarquía, exilio, retorno, persa, griego, macabeo, romano.', '3', 'TMS BI779 · NT672', 'X (historia, arqueología) + B'),
    ('Geografía bíblica', 20, 'Mesopotamia, Egipto, Canaán, Jerusalén, Galilea, Asia Menor, Grecia, Roma, viajes misioneros.', '3', 'TMS BI652', 'X + B'),
    ('Arqueología y mundo antiguo', 24, 'Inscripciones, rollos del Mar Muerto, culturas, economía, derecho, religiones.', '3', 'TMS OT796', 'X (verificar en la fuente)'),
    ('Vida cotidiana en tiempos bíblicos', 16, '', '3', '—', 'X + B'),
])
ciclo(17, 'Historia del cristianismo y tradiciones', '', [
    ('Iglesia primitiva, padres y concilios', 20, 'Padres apostólicos, credos, Nicea, Calcedonia.', '5', 'TMS TH507 · IBBA Historia de la iglesia 1', 'B + X'),
    ('Credos, confesiones y catecismos', 10, 'Credo Apostólico, Nicea, Calcedonia, confesiones de la Reforma (Westminster, Augsburgo, Bautista de Londres) y catecismos: qué afirma cada uno y por qué.', '5 Credos', 'RTS Catecismo Menor de Westminster · TMS TH507/508', 'B + X (textos de los propios credos)'),
    ('Edad media, cisma y Reforma', 24, 'Oriente y Occidente, Lutero, Calvino, anabaptistas, contrarreforma.', '5', 'TMS TH507/508 · IBBA Teología de la Reforma', 'B'),
    ('Avivamientos, misiones y movimientos modernos', 24, 'Pentecostalismo, carismáticos, evangelicalismo, cristianismo global, misión urbana, América Latina y Argentina.', '5', 'IBBA Historia de la iglesia en América Latina', 'B + X'),
    ('Tradiciones: catolicismo, ortodoxia y familias protestantes', 24, 'Qué creen, por qué, y dónde difieren, con sus propios documentos.', '5', 'TMS TH788', 'X (fuentes primarias de cada tradición)'),
])
ciclo(18, 'Fe informada: apologética, religiones y cosmovisiones', 'Por qué creo lo que creo y cómo explicarlo con respeto.', [
    ('Evidencias de Jesús y de la resurrección', 24, 'Fuentes históricas, testigos, objeciones.', '5', 'TMS TH602', 'B: Apologética (34 libros)'),
    ('Confiabilidad de la Biblia y objeciones comunes', 20, '', '5', '—', 'B'),
    ('Judaísmo, Islam, hinduismo, budismo y otras religiones', 36, 'Textos fundamentales, historia, creencias y diferencias con el cristianismo.', '5', 'TMS MI784 · IBBA Religiones comparadas', 'X (fuentes primarias y académicas)'),
    ('Ateísmo, agnosticismo, deísmo, secularismo y naturalismo', 20, '', '5', 'IBBA Apologética contemporánea', 'B + X'),
])
ciclo(19, 'Temas por descubrir', 'Símbolos, instituciones y motivos que atraviesan la Biblia y rara vez se estudian completos.', [
    ('Símbolos: agua, fuego, sangre, luz y tinieblas, montes, jardines, caminos, puertas, vestiduras', 40, '', '8', '—', 'B + comentarios'),
    ('Nombres, números y genealogías', 16, '', '8', '—', 'B + X'),
    ('Comidas, banquetes y fiestas bíblicas', 16, '', '8', '—', 'B'),
    ('Sueños, visiones, señales y ángeles', 16, '', '8', '—', 'B'),
    ('Espera, desierto, prueba, herencia y fidelidad generacional', 20, '', '8', '—', 'B'),
    ('Palabra, lenguaje y música', 12, '', '8', '—', 'B'),
])
ciclo(20, 'Teología práctica y ministerio', '', [
    ('Predicación y enseñanza', 16, '', '4 Teología pastoral', 'TMS PM501-PM703 · IBBA Homilética', 'B (Predicación y Homiletica, 27 libros)'),
    ('Pastorado y consejería bíblica', 18, '', '4', 'TMS PM765 · IBBA Consejería', 'B'),
    ('Misionología', 12, '', '4', 'TMS MI778 · IBBA Misiones', 'B'),
    ('Educación cristiana y enseñanza bíblica', 10, 'Cómo se enseña la Biblia a niños, jóvenes, adultos y familias; pedagogía y discipulado.', '4', 'IBBA Educación cristiana (DFB/EDUCRIS) · SITB Educación cristiana · SBTS Enseñanza cristiana', 'B (Enseñanza y Educación Cristiana, Niños, Jóvenes)'),
    ('Método teológico', 10, 'Cómo se hace teología; teología histórica y sistemática.', '4', 'TMS TH795', 'B'),
])

INST = ['', '## Contraste con institutos de referencia', '',
 'Se relevaron planes publicados de: **IBBA** (Instituto Bíblico Buenos Aires, ibba.com.ar), **The Master\'s Seminary** (M.Div., 98 unidades; catálogo 2024-25), **SITB / Seminario Teológico Bautista** (Buenos Aires), **Dallas Theological Seminary** (Th.M.), **Reformed Theological Seminary** (M.Div.), **Southern Baptist Theological Seminary** (M.Div.) y **TTL Training** (Toma Tu Lugar, Córdoba). Los informes completos, con sus URL y lo que no se pudo verificar, están en `institutos/`.',
 '', 'Lo que casi todos incluyen y el plan cubre: AT y NT por bloques de libros (ciclo 14), hermenéutica (1.3), idiomas bíblicos (1.4), sistemática por temas (ciclos 2–6, 9, 13), historia de la Iglesia (17), misiones (9.4, 20.3), apologética (18), ética (12), predicación, consejería y liderazgo (20), formación espiritual (10–11).',
 '', 'Lo que el plan agrega: teología bíblica y conexiones (7), Reino y reinos (8), mundo bíblico (16), personajes (15), temas por descubrir (19) y comparación de religiones (18.3).',
 '', 'Sin verificar: el plan de estudios del *Instituto Misión* (no hay plan público hallado), la Licenciatura en Estudios de la Biblia del SITB y el MAMT de la Facultad de Teología Reformada (PDF no disponible), y el sitio ibbaedu.com.ar (no resolvió). Los planes se usan solo como referencia de temas, no se copian.']
TOTAL = sum(s['dias'] for c in C for s in c['series'])
json.dump({'ciclos': C, 'total_estimado': TOTAL}, open(f'{AQUI}/ciclos.json', 'w'), ensure_ascii=False, indent=1)

L = ['# Plan maestro del megaestudio', '',
     f'**{len(C)} ciclos · {sum(len(c["series"]) for c in C)} series · ≈{TOTAL} días** (20 a 30 minutos cada uno; unos {TOTAL/365:.1f} años a un día por día).',
     '', 'El orden es el camino recomendado, pero la app permite entrar por cualquier tema (buscador, mapa, ciclos). Los días se detallan por oleadas: solo se baja a título de día el ciclo que se va a escribir.',
     '', '| Ciclo | Series | Días |', '|---|--:|--:|']
for c in C: L.append(f"| {c['numero']}. {c['titulo']} | {len(c['series'])} | {sum(s['dias'] for s in c['series'])} |")
for c in C:
    L += ['', f"## {c['numero']}. {c['titulo']}", '', c['bajada'], '', '| Serie | Días | Qué cubre | Pedido | Institutos | Fuentes |', '|---|--:|---|---|---|---|']
    for s in c['series']:
        L.append(f"| {s['id']} {s['titulo']} | {s['dias']} | {s['enfoque']} | {s['pedido']} | {s['institutos']} | {s['fuentes']} |")
L += INST
open(f'{AQUI}/PLAN-MAESTRO.md', 'w').write('\n'.join(L) + '\n')
print(len(C), 'ciclos', sum(len(c['series']) for c in C), 'series', TOTAL, 'días')
