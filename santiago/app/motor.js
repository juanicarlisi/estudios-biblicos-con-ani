(() => {
const D = window.DATOS;
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const n2 = n => String(n).padStart(2, '0');
const PLAN = D.plan, TOTAL = PLAN.length, PARTES = D.partes;
const NV = [27, 26, 18, 17, 20], ACUM = [0, 27, 53, 71, 88, 108];

/* ---------- versículos: índice 1..108 ---------- */
const idxv = (c, v) => ACUM[c - 1] + v;
const deIdx = i => { for (let c = 1; c <= 5; c++) if (i <= ACUM[c]) return [c, i - ACUM[c - 1]]; return [5, 20]; };
function refIdx(r) {
  const m = String(r || '').replace(/\s/g, '').replace(/[–—]/g, '-').match(/^(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?$/);
  if (!m) return null;
  const c1 = +m[1], v1 = +m[2], c2 = m[3] ? +m[3] : c1, v2 = m[4] ? +m[4] : v1;
  if (c1 < 1 || c1 > 5 || c2 < 1 || c2 > 5) return null;
  return [idxv(c1, Math.min(v1, NV[c1 - 1])), idxv(c2, Math.min(v2, NV[c2 - 1]))];
}
PLAN.forEach(p => { const r = refIdx(p.desde + '-' + p.hasta); p.a = r[0]; p.b = r[1]; });
const diasDelVerso = Array.from({ length: 109 }, () => []);
PLAN.forEach(p => { for (let i = p.a; i <= p.b; i++) diasDelVerso[i].push(p.dia); });
const diaQueContiene = ref => { const r = refIdx(ref); return r && diasDelVerso[r[0]].length ? diasDelVerso[r[0]][0] : 1; };
const txtRef = (a, b) => { const [c1, v1] = deIdx(a), [c2, v2] = deIdx(b); return a === b ? `${c1}:${v1}` : c1 === c2 ? `${c1}:${v1}-${v2}` : `${c1}:${v1}-${c2}:${v2}`; };

/* ---------- estado: progreso y notas (local + compartido) ---------- */
const est = { hechos: {}, notas: {} };
const LS = 'santiago-en-pareja-v1';
try { Object.assign(est, JSON.parse(localStorage.getItem(LS) || '{}')); } catch (e) {}
const guardarLocal = () => { try { localStorage.setItem(LS, JSON.stringify(est)); } catch (e) {} };
let db = null, compartido = false;
const docDia = d => db && db.collection('pareja_santiago').doc('d' + n2(d));
async function escribirDia(d) {
  guardarLocal();
  if (!db) return;
  try { await docDia(d).set({ hecho: !!est.hechos[d], fecha: est.hechos[d] || '', notas: est.notas[d] || '', actualizado: new Date().toISOString() }); }
  catch (e) { marcarEstado('Se guardó solo en esta compu (no se pudo compartir).'); }
}
function marcarEstado(t) { const e = $('#estado-notas'); if (e) e.textContent = t; }
(async () => {
  try {
    if (!window.claude || !window.claude.use) return;
    db = await window.claude.use('db');
    if (!db) return;
    db.collection('pareja_santiago').onSnapshot(snap => {
      compartido = true;
      snap.docs.forEach(doc => {
        const v = doc.data() || {}; const d = parseInt(doc.id.slice(1), 10);
        if (v.hecho) est.hechos[d] = v.fecha || true; else delete est.hechos[d];
        if (typeof v.notas === 'string') {
          const ta = $('#notas-dia');
          if (!(ta && document.activeElement === ta && +ta.dataset.dia === d)) est.notas[d] = v.notas;
        }
      });
      guardarLocal(); pintarProgreso(); pintarNav();
      const ta = $('#notas-dia'); if (ta && document.activeElement !== ta) ta.value = est.notas[+ta.dataset.dia] || '';
      marcarEstado('Compartido entre ustedes dos.');
    }, () => { db = null; });
  } catch (e) { db = null; }
})();

/* ---------- preferencias ---------- */
const PREF = 'santiago-en-pareja-pref';
let pref = {}; try { pref = JSON.parse(localStorage.getItem(PREF) || '{}'); } catch (e) {}
const guardarPref = () => { try { localStorage.setItem(PREF, JSON.stringify(pref)); } catch (e) {} };
const aplicarPref = () => {
  if (pref.tema) document.documentElement.dataset.theme = pref.tema; else delete document.documentElement.dataset.theme;
  if (pref.tam) document.documentElement.dataset.size = pref.tam; else delete document.documentElement.dataset.size;
};
aplicarPref();
$('#tema-btn').onclick = () => {
  const oscuro = pref.tema ? pref.tema === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  pref.tema = oscuro ? 'light' : 'dark'; aplicarPref(); guardarPref();
};
$('#tam-btn').onclick = () => { pref.tam = { undefined: 'grande', grande: 'chica', chica: undefined }[pref.tam]; aplicarPref(); guardarPref(); };
$('#menu-btn').onclick = () => document.body.classList.toggle('nav-abierta');

/* ---------- utilidades de contenido ---------- */
const diaPlan = d => PLAN[d - 1];
const hayDia = d => !!D.dias[d];
const hechosN = () => Object.keys(est.hechos).length;
const siguientePendiente = () => (PLAN.find(p => !est.hechos[p.dia]) || PLAN[TOTAL - 1]).dia;
const parteDe = id => PARTES.find(t => t.id === id);
const minutosDia = d => { const x = D.dias[d]; return x ? x.minutos.lectura + x.minutos.estudio : 25; };
const bg = (desde, hasta) => 'https://www.biblegateway.com/passage/?search=' + encodeURIComponent('Santiago ' + desde + '-' + hasta) + '&version=RVR1960';
const ordinal = n => ['', 'Primera', 'Segunda', 'Tercera', 'Cuarta', 'Quinta', 'Sexta', 'Séptima', 'Octava'][n] || n + '.ª';
function chips(ids) {
  if (!ids || !ids.length) return '';
  const vistos = {};
  ids.forEach(id => { const f = D.fuentes[id]; if (f) (vistos[f[0]] = vistos[f[0]] || []).push(id); });
  return '<span class="chips">' + Object.keys(vistos).map(k =>
    `<button class="chip" data-ids="${esc(vistos[k].join(' '))}" aria-expanded="false">${esc(k)}</button>`).join('') + '</span>';
}
let popAbierto = null;
document.addEventListener('click', e => {
  const c = e.target.closest('.chip');
  if (popAbierto) { popAbierto.remove(); document.querySelectorAll('.chip[aria-expanded="true"]').forEach(b => b.setAttribute('aria-expanded', 'false')); popAbierto = null; }
  if (c) {
    const ids = c.dataset.ids.split(' ');
    const pop = document.createElement('div'); pop.className = 'pop'; pop.setAttribute('role', 'dialog');
    pop.innerHTML = ids.map(id => { const f = D.fuentes[id]; return f ? `<div><b>${esc(f[1])}</b><br>${esc(f[2] || '')}</div>` : ''; }).join('');
    document.body.appendChild(pop);
    const r = c.getBoundingClientRect(); const w = Math.min(340, innerWidth - 32);
    pop.style.width = w + 'px';
    pop.style.left = Math.max(16, Math.min(innerWidth - w - 16, r.left + scrollX)) + 'px';
    pop.style.top = (r.bottom + scrollY + 6) + 'px';
    c.setAttribute('aria-expanded', 'true'); popAbierto = pop; e.stopPropagation();
  }
  if (e.target.closest('.nav a')) document.body.classList.remove('nav-abierta');
});
const parr = t => esc(t).split(/\n{2,}/).map(x => `<p>${x.replace(/\n/g, '<br>')}</p>`).join('');
const ARTS = D.articulos_orden || [];
const artDe = id => (D.articulos || {})[id];
const tituloArt = a => (artDe(a.id) || {}).titulo || a.titulo;
const COLOR_PARTE = { I: 'var(--tinta)', II: 'var(--terracota)', III: 'var(--oliva)', IV: 'var(--oro)', V: 'var(--tinta)' };
const GRUPOS = { intro: 'Introducción', parte: 'Panorama', tema: 'Tema', anexo: 'Anexo' };

/* ---------- texto bíblico ---------- */
const vtxt = (c, v) => (D.rvr || {})[c + ':' + v];
const gtxt = (c, v) => (D.griego || {})[c + ':' + v];
function versosHTML(a, b, opts = {}) {
  let h = '';
  for (let i = a; i <= b; i++) {
    const [c, v] = deIdx(i), t = vtxt(c, v); if (!t) continue;
    h += `<span class="v ${opts.resaltar === i ? 'res' : ''}" data-v="${c}:${v}"><sup>${i === a || v === 1 ? c + ':' + v : v}</sup>${esc(t).replace(/\n/g, ' ')} </span>`;
  }
  return h;
}
function griegoHTML(a, b) {
  let h = '';
  for (let i = a; i <= b; i++) { const [c, v] = deIdx(i), t = gtxt(c, v); if (t) h += `<div class="griego-v gr" lang="grc"><sup>${v}</sup>${esc(t)}</div>`; }
  return h;
}
function pasajeHTML(p, abierto) {
  const conGriego = !!D.griego && Object.keys(D.griego).length;
  return `<details class="pasaje" id="pasaje" ${abierto ? 'open' : ''}><summary><span>El pasaje · Santiago ${esc(p.desde)}${p.desde === p.hasta ? '' : '–' + esc(p.hasta)} · RVR1960</span></summary>
    <div class="pasaje-cuerpo"><div class="versos">${versosHTML(p.a, p.b)}</div>
    <div class="pie-pasaje">${conGriego ? '<button class="btn chico tog" id="ver-griego" aria-pressed="false">Ver el texto griego</button>' : ''}
      <a class="btn chico" href="${bg(p.desde, p.hasta)}" target="_blank" rel="noopener">Abrir en BibleGateway ↗</a>
      <span>${esc(D.aviso_rvr || '')}</span></div>
    <div id="caja-griego" hidden>${conGriego ? griegoHTML(p.a, p.b) + `<div class="pie-pasaje"><span>${esc(D.aviso_griego || '')}</span></div>` : ''}</div></div></details>`;
}

/* ---------- palabras clave: conteo por capítulo (columna del día y gráfico) ---------- */
const sinTildes = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const CLAVES = [
  ['fe', /\bfe\b/], ['obras', /\bobras?\b/], ['hermanos', /\bhermanos?\b/], ['palabra', /\bpalabras?\b/], ['lengua', /\blenguas?\b/], ['sabiduría', /\bsabidur[ií]a\b/],
  ['pruebas y tentación', /\b(pruebas?|prueba|tentaci[oó]n|tentado|tienta|tentar)\b/], ['paciencia', /\b(paciencia|pacientes?|sufridos?)\b/], ['ley', /\bley\b/],
  ['pobres', /\bpobres?\b/], ['ricos', /\b(ricos?|riquezas?)\b/], ['oración', /\b(orar|ora|oraci[oó]n|oren|oad|orad|pida|pedir|ped[ií]s|pedid)\b/],
  ['pecado', /\b(pecados?|pecar|pecador(es)?)\b/], ['justo y justicia', /\b(justos?|justicia|justificad[oa]s?|justificar)\b/], ['Dios', /\bdios\b/], ['Señor', /\bse[nñ]or\b/],
];
let _conteos = null;
function conteosClaves() {
  if (_conteos) return _conteos;
  _conteos = CLAVES.map(([n, re]) => { const por = [0, 0, 0, 0, 0], vers = [[], [], [], [], []];
    for (let c = 1; c <= 5; c++) for (let v = 1; v <= NV[c - 1]; v++) { const t = sinTildes(vtxt(c, v) || ''); const k = t.match(new RegExp(re.source, 'g')); if (k) { por[c - 1] += k.length; vers[c - 1].push(v); } }
    return { n, re, por, vers, tot: por.reduce((a, b) => a + b, 0) }; });
  return _conteos;
}
function clavesDelDia(p) {
  let t = ''; for (let i = p.a; i <= p.b; i++) { const [c, v] = deIdx(i); t += ' ' + sinTildes(vtxt(c, v) || ''); }
  return conteosClaves().filter(r => new RegExp(r.re.source).test(t)).sort((a, b) => a.tot - b.tot).slice(0, 3);
}
function miniGrafico(r, capActual) {
  const max = Math.max(...r.por, 1), W = 150, H = 44, bw = 20, gap = 10;
  return `<div style="margin:8px 0 2px"><div style="display:flex;justify-content:space-between"><b>${esc(r.n)}</b><span class="estado">${r.tot} en la carta</span></div>
    <svg viewBox="0 0 ${W} ${H + 14}" width="100%" role="img" aria-label="${esc(r.n)}: ${r.por.map((n, k) => `capítulo ${k + 1}, ${n}`).join('; ')}">${r.por.map((n, k) => { const h = Math.max(1.5, (n / max) * H);
      return `<rect x="${k * (bw + gap) + 5}" y="${H - h}" width="${bw}" height="${h}" rx="3" fill="${k + 1 === capActual ? 'var(--terracota)' : 'var(--tinta)'}" opacity="${k + 1 === capActual ? 1 : .55}"/>
      <text x="${k * (bw + gap) + 5 + bw / 2}" y="${H + 11}" text-anchor="middle" font-size="9" fill="var(--muted)" font-family="var(--f-ui)">${k + 1}</text>
      <text x="${k * (bw + gap) + 5 + bw / 2}" y="${H - h - 2}" text-anchor="middle" font-size="9" fill="var(--ink)" font-family="var(--f-ui)">${n}</text>`; }).join('')}</svg></div>`;
}

/* ---------- tira de versículos (avance por versículo) ---------- */
function tira(grande, hoy) {
  let h = `<div class="tira ${grande ? 'grande' : ''}" role="img" aria-label="Avance por versículo de la carta">`;
  for (let c = 1; c <= 5; c++) {
    h += `<div class="cap"><span>${c}</span><div class="fila" style="grid-template-columns:repeat(27,1fr)">`;
    for (let v = 1; v <= NV[c - 1]; v++) {
      const i = idxv(c, v), ds = diasDelVerso[i];
      const hechos = ds.filter(d => est.hechos[d]).length;
      let cls = !ds.length ? '' : hechos === ds.length ? 'hecho' : hechos ? 'parcial' : '';
      if (hoy && ds.includes(hoy)) cls += ' esta';
      if (ds.length && PLAN[ds[0] - 1].a === i) cls += ' ini';
      const destino = ds.find(d => !est.hechos[d]) || ds[0];
      h += `<a class="cel ${cls}" href="#dia-${destino}" title="Santiago ${c}:${v}${ds.length ? ' · día ' + destino : ''}" aria-label="Santiago ${c}:${v}"></a>`;
    }
    h += '</div></div>';
  }
  return h + '</div>';
}
const leyendaTira = `<div class="tira-leyenda"><span><i style="background:var(--oliva)"></i>Leído</span><span><i style="background:var(--tinta)"></i>Hoy</span><span><i style="background:var(--line)"></i>Por leer</span><span>Cada cuadrito es un versículo; cada fila, un capítulo.</span></div>`;

/* ---------- progreso y navegación ---------- */
function pintarProgreso() {
  const hechos = hechosN(), p = hechos / TOTAL, R = 12, C = 2 * Math.PI * R;
  $('#anillo').innerHTML = `<svg viewBox="0 0 30 30" aria-hidden="true"><circle cx="15" cy="15" r="${R}" fill="none" stroke="var(--line)" stroke-width="4"/>
    <circle cx="15" cy="15" r="${R}" fill="none" stroke="var(--oliva)" stroke-width="4" stroke-linecap="round" stroke-dasharray="${C * p} ${C}" transform="rotate(-90 15 15)"/></svg>
    <span>${hechos} de ${TOTAL} días</span>`;
  const g = $('#prog-global'); if (g) { g.querySelector('i').style.width = (100 * p).toFixed(1) + '%'; g.setAttribute('aria-valuenow', Math.round(100 * p)); g.title = `${hechos} de ${TOTAL} días · ${Math.round(100 * p)} %`; }
}
let rutaActual = '';
function pintarNav() {
  const actual = rutaActual;
  const it = (h, t) => `<a class="item ${actual === h ? 'actual' : ''}" href="#${h}">${t}</a>`;
  let h = it('inicio', 'Inicio') + it('como-usar', 'Cómo usar el estudio') + it('introduccion', 'Introducción a Santiago') + it('carta', 'La carta completa');
  const enIntro = actual === 'introduccion' || /^art-I/.test(actual);
  if (enIntro) h += ARTS.filter(a => a.grupo === 'intro').map(a => `<a class="item sub ${actual === 'art-' + a.id ? 'actual' : ''}" href="#art-${a.id}">${esc(tituloArt(a))}</a>`).join('');
  h += '<h4>El plan, según la carta</h4>';
  PARTES.forEach(t => {
    const dias = PLAN.filter(p => p.parte === t.id);
    if (!dias.length) return;
    const a = ARTS.find(x => x.grupo === 'parte' && x.parte === t.id);
    if (a) h += `<a class="item parte-l ${actual === 'art-' + a.id ? 'actual' : ''}" href="#art-${a.id}"><span>${esc(tituloArt(a))}<br><small>Panorama antes de empezar · Stg ${esc(t.rango)}</small></span></a>`;
    const hechos = dias.filter(p => est.hechos[p.dia]).length;
    const abierto = dias.some(p => actual === 'dia-' + p.dia) || (actual === 'inicio' && dias.some(p => p.dia === siguientePendiente()));
    h += `<details class="tol" ${abierto ? 'open' : ''}><summary><span class="t1">${esc(t.etiqueta)}</span><span class="t2">${esc(t.titulo)}</span>
      <span class="t3"><span>Stg ${esc(t.rango)}</span><span>${hechos}/${dias.length}</span></span><div class="minibar"><i style="width:${100 * hechos / dias.length}%"></i></div></summary>` +
      dias.map(p => `<a class="dia-l ${est.hechos[p.dia] ? 'hecho' : ''} ${actual === 'dia-' + p.dia ? 'actual' : ''} ${hayDia(p.dia) ? '' : 'pend'}" href="#dia-${p.dia}">
        <span class="n">${p.dia}</span><span>${esc((D.dias[p.dia] || p).titulo)}</span><span class="r">${esc(p.desde)}</span></a>`).join('') + '</details>';
  });
  const temas = ARTS.filter(a => a.grupo === 'tema');
  if (temas.length) h += '<h4>Temas de Santiago</h4>' + it('temas', 'Todos los temas') + temas.map(a => it('art-' + a.id, esc(tituloArt(a)))).join('');
  const anexos = ARTS.filter(a => a.grupo === 'anexo');
  if (anexos.length) h += '<h4>Anexos</h4>' + it('anexos', 'Todos los anexos') + anexos.map(a => it('art-' + a.id, esc(tituloArt(a)))).join('');
  h += '<h4>Herramientas</h4>' + it('carta', 'La carta completa') + it('mapas', 'Mapas') + it('linea', 'Línea de tiempo') + it('palabras', 'Palabras griegas') +
    it('claves', 'Palabras de la carta (gráfico)') + it('ecos', 'Santiago y las palabras de Jesús') + it('cristo', 'Cristo en Santiago') + it('buscar', 'Buscar') + it('fuentes', 'Fuentes del estudio');
  $('#nav').innerHTML = h;
}

/* ---------- inicio ---------- */
function vistaInicio() {
  const d = siguientePendiente(), p = diaPlan(d), x = D.dias[d], hechos = hechosN();
  const partes = PARTES.map(t => { const ds = PLAN.filter(y => y.parte === t.id); if (!ds.length) return '';
    const h = ds.filter(y => est.hechos[y.dia]).length;
    return `<a class="parte" href="#dia-${(ds.find(y => !est.hechos[y.dia]) || ds[0]).dia}"><small>${esc(t.etiqueta)} · Stg ${esc(t.rango)}</small><b>${esc(t.titulo)}</b>
      <div class="bar"><i style="width:${100 * h / ds.length}%"></i></div><small>${h} de ${ds.length} días</small></a>`; }).join('');
  const minutos = PLAN.reduce((s, y) => s + minutosDia(y.dia), 0);
  const temas = ARTS.filter(a => a.grupo === 'tema'), anexos = ARTS.filter(a => a.grupo === 'anexo');
  return `<div class="hoja ancha">
    <section class="heroe"><div><h1>Santiago</h1><span class="gr" lang="grc">ΙΑΚΩΒΟΥ</span>
      <p>La carta de Santiago, para leer de a dos, a su ritmo: cada día, unos veinte a treinta minutos, ${TOTAL} días en total. Todo sale de los comentarios y libros de su biblioteca, con la fuente de cada afirmación.</p></div>
      <div class="hoy"><span class="ojo">${hechos ? 'Siguen con' : 'Para empezar'} · Día ${d} de ${TOTAL}</span><h2>${esc((x || p).titulo)}</h2>
        <div class="meta"><span>Santiago ${esc(p.desde)}${p.desde === p.hasta ? '' : '–' + esc(p.hasta)}</span><span>${p.b - p.a + 1} ${p.b === p.a ? 'versículo' : 'versículos'}</span><span>≈ ${minutosDia(d)} min</span></div>
        <div class="acciones"><a class="btn prim" href="#dia-${d}">Abrir el día ${d}</a>${hechos ? '' : '<a class="btn" href="#introduccion">Leer antes la introducción</a>'}</div></div></section>
    <section class="progreso-grande"><div class="num"><b>${Math.round(100 * hechos / TOTAL)} %</b><span>${hechos} de ${TOTAL} días terminados · ≈ ${Math.round(minutos / 60)} horas de estudio en total</span></div>
      <div class="barra-g"><i style="width:${100 * hechos / TOTAL}%"></i></div></section>
    <h2>La carta de un vistazo</h2><p style="color:var(--muted)">Los 108 versículos de Santiago, uno por cuadrito. Tocando uno se abre el día que lo estudia.</p>
    ${tira(true, d)}${leyendaTira}
    <h2>Las cinco partes de la carta</h2><div class="partes">${partes}</div>
    ${temas.length ? `<h2>Los grandes temas</h2><div class="grilla-h temas">${temas.map(a => `<a href="#art-${a.id}"><div class="panel"><b>${esc(tituloArt(a))}</b><small>${esc((artDe(a.id) || {}).bajada || 'En preparación.')}</small></div></a>`).join('')}</div>` : ''}
    <h2>Para acompañar la lectura</h2><div class="grilla-h">
      <a href="#carta"><div class="panel"><b>La carta completa</b><small>Los cinco capítulos de corrido, con el día que estudia cada tramo.</small></div></a>
      <a href="#mapas"><div class="panel"><b>Mapas</b><small>La dispersión de los destinatarios y los lugares que la carta recuerda.</small></div></a>
      <a href="#linea"><div class="panel"><b>Línea de tiempo</b><small>La iglesia de Jerusalén, Santiago y las fechas que proponen las fuentes.</small></div></a>
      <a href="#claves"><div class="panel"><b>Palabras de la carta</b><small>Qué palabras se repiten y en qué capítulo, con un gráfico.</small></div></a>
      <a href="#ecos"><div class="panel"><b>Santiago y Jesús</b><small>Los ecos de las palabras del Señor en la carta.</small></div></a>
      <a href="#palabras"><div class="panel"><b>Palabras griegas</b><small>Las que comentan las fuentes, día por día.</small></div></a>
      ${anexos.length ? `<a href="#anexos"><div class="panel"><b>Anexos</b><small>${anexos.map(a => esc(tituloArt(a))).join(' · ')}</small></div></a>` : ''}
    </div>
    <section class="copia panel"><div><b>Sus notas y su avance</b><p>Se guardan en el navegador de esta compu. Si se limpian los datos del navegador se pierden, así que bajen una copia de vez en cuando (también sirve para pasarlos a otra compu).</p></div>
      <div class="acciones"><button class="btn" id="bajar-copia">Descargar copia</button><button class="btn" id="cargar-copia-btn">Cargar copia</button>
      <input type="file" id="cargar-copia" accept=".json,application/json" hidden></div><div class="estado" id="estado-copia"></div></section></div>`;
}

/* ---------- diagramas dentro del día ---------- */
const ICONOS = {
  ola: '<path d="M2 11c2.5-3 4.5-3 7 0s4.5 3 7 0 4.5-3 6 0"/><path d="M2 17c2.5-3 4.5-3 7 0s4.5 3 7 0 4.5-3 6 0"/>',
  hierba: '<path d="M12 21V10"/><path d="M12 15c-4 0-6-2-6-6 4 0 6 2 6 6z"/><path d="M12 12c3 0 5-2 5-5-3 0-5 2-5 5z"/>',
  espejo: '<circle cx="12" cy="9.5" r="6"/><path d="M12 15.5V21M9 21h6"/>',
  freno: '<circle cx="5" cy="12" r="2.5"/><circle cx="19" cy="12" r="2.5"/><path d="M7.5 12h9M9 8v8M15 8v8"/>',
  timon: '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
  fuego: '<path d="M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-9z"/>',
  bestia: '<circle cx="8" cy="8" r="1.8"/><circle cx="16" cy="8" r="1.8"/><circle cx="5" cy="13" r="1.8"/><circle cx="19" cy="13" r="1.8"/><path d="M12 12c-3 0-5 3-5 6 0 2 2 2 5 2s5 0 5-2c0-3-2-6-5-6z"/>',
  fuente: '<path d="M12 3c3.5 4.5 6 7.5 6 11a6 6 0 0 1-12 0c0-3.5 2.5-6.5 6-11z"/><path d="M9.5 14.5a2.7 2.7 0 0 0 2.5 2.5"/>',
  hoja: '<path d="M5 19C5 10 10 5 20 4c0 10-5 15-15 15z"/><path d="M5 19L14 10"/>',
  uvas: '<circle cx="9" cy="10" r="2.2"/><circle cx="15" cy="10" r="2.2"/><circle cx="12" cy="14" r="2.2"/><circle cx="9" cy="18" r="2.2"/><circle cx="15" cy="18" r="2.2"/><path d="M12 3v4"/>',
  nube: '<path d="M7 18a4 4 0 0 1-.5-7.9A5.5 5.5 0 0 1 17.5 9 3.5 3.5 0 0 1 17 18z"/>',
  lluvia: '<path d="M7 13a4 4 0 0 1-.5-7.9A5.5 5.5 0 0 1 17.5 4 3.5 3.5 0 0 1 17 13z"/><path d="M8 16l-1 3M12 16l-1 3M16 16l-1 3"/>',
  aceite: '<path d="M10 3h4M11 3v3c-3 2-5 4-5 8a6 6 0 0 0 12 0c0-4-2-6-5-8V3"/><path d="M9 14h6"/>',
  corona: '<path d="M3 17l2-9 5 5 2-7 2 7 5-5 2 9z"/><path d="M4 20h16"/>',
  balanza: '<path d="M12 4v16M6 20h12M5 7h14"/><path d="M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
  libro: '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19a2 2 0 0 1 2-2h13"/>',
  corazon: '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
  boca: '<path d="M3 12c3-4 6-4 9-2 3-2 6-2 9 2-3 5-6 6-9 6s-6-1-9-6z"/><path d="M3 12h18"/>',
  oido: '<path d="M7 10a5 5 0 0 1 10 0c0 3-2 4-3 6s-1 4-3 4-3-1.5-3-3"/>',
  moneda: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4.5"/>',
  camino: '<path d="M6 21c1-5 3-7 6-9s5-4 6-9"/><path d="M12 21c0-3 1-5 3-7"/>',
  mano: '<path d="M7 12V6a1.5 1.5 0 0 1 3 0v5M10 11V4.5a1.5 1.5 0 0 1 3 0V11M13 11V6a1.5 1.5 0 0 1 3 0v6M16 11.5a1.5 1.5 0 0 1 3 0V15a6 6 0 0 1-6 6h-1a6 6 0 0 1-5-3l-3-5a1.5 1.5 0 0 1 2.5-1.5L7 14"/>',
};
const icono = k => ICONOS[k] ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONOS[k]}</svg>` : '';
const COLORES_COL = ['var(--tinta)', 'var(--terracota)', 'var(--oliva)', 'var(--oro)'];
function diagramaHTML(g) {
  if (!g || !g.tipo) return '';
  let cuerpo = '';
  const it = g.items || [];
  if (g.tipo === 'pasos') {
    cuerpo = `<div class="dg-pasos">${it.map(s => `<div class="dg-paso"><b>${esc(s.titulo)}</b>${esc(s.texto || '')}${s.ref ? `<span class="rf">${esc(s.ref)}</span>` : ''}</div>`).join('')}</div>`;
  } else if (g.tipo === 'escalera') {
    cuerpo = `<div class="dg-esc">${it.map((s, k) => `<div class="esc" style="--n:${k}"><b>${k + 1}. ${esc(s.titulo)}</b> ${esc(s.texto || '')}${s.ref ? ` <span class="refs">${esc(s.ref)}</span>` : ''}</div>`).join('')}</div>`;
  } else if (g.tipo === 'imagenes') {
    cuerpo = `<div class="dg-img">${it.map(s => `<div class="im">${icono(s.icono)}<b>${esc(s.titulo)}</b>${esc(s.texto || '')}${s.ref ? `<span class="rf">${esc(s.ref)}</span>` : ''}</div>`).join('')}</div>`;
  } else if (g.tipo === 'comparacion') {
    const cols = g.columnas || [], n = cols.length + 1;
    cuerpo = `<div class="dg-comp" style="grid-template-columns:minmax(80px,.55fr) repeat(${cols.length},1fr)"><div class="th" style="background:var(--muted)"></div>` +
      cols.map((c, k) => `<div class="th" style="background:${COLORES_COL[k % 4]}">${esc(c)}</div>`).join('') +
      (g.filas || []).map(f => `<div class="c et">${esc(f.etiqueta || '')}</div>` + (f.celdas || []).map(c => `<div class="c">${esc(c)}</div>`).join('')).join('') + '</div>';
  } else if (g.tipo === 'tabla') {
    cuerpo = `<div style="overflow-x:auto"><table class="tabla"><thead><tr>${(g.columnas || []).map(c => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>` +
      (g.filas || []).map(f => `<tr>${(Array.isArray(f) ? f : f.celdas || []).map(c => `<td>${esc(c)}</td>`).join('')}</tr>`).join('') + '</tbody></table></div>';
  }
  return `<figure class="diagrama" style="margin-inline:0"><span class="ojo">Para ver de un vistazo</span><h3>${esc(g.titulo || '')}</h3>${g.descripcion ? `<p class="desc">${esc(g.descripcion)}</p>` : ''}${cuerpo}${g.fuentes && g.fuentes.length ? `<div class="dg-fuentes">Fuentes: ${chips(g.fuentes)}</div>` : ''}</figure>`;
}

/* ---------- el día ---------- */
function bloqueNotas(d) {
  return `<section class="notas-p" id="paso-5"><h2>Sus notas del día</h2><textarea id="notas-dia" data-dia="${d}" placeholder="Lo que aprendieron, lo que conversaron, por qué van a orar…">${esc(est.notas[d] || '')}</textarea>
    <div class="estado" id="estado-notas">${db ? (compartido ? 'Compartido entre ustedes dos.' : 'Conectando…') : 'Se guarda en esta compu.'}</div></section>`;
}
function articulosDelDia(d) {
  const p = diaPlan(d), x = D.dias[d] || {};
  const ids = new Set((x.anexos || []).map(a => a.id));
  const por = {}; (x.anexos || []).forEach(a => { por[a.id] = a.por_que; });
  ARTS.filter(a => a.grupo === 'tema' || a.grupo === 'anexo').forEach(a => {
    const y = artDe(a.id); if (!y) return;
    if ((y.refs_santiago || []).some(r => { const q = refIdx(r.replace(/^(Stg|Santiago)\.?\s*/i, '')); return q && q[0] <= p.b && q[1] >= p.a; })) ids.add(a.id);
  });
  return [...ids].map(id => ARTS.find(a => a.id === id)).filter(Boolean).slice(0, 6).map(a => ({ a, por: por[a.id] }));
}
function vistaDia(d) {
  const p = diaPlan(d); if (!p) return vistaInicio();
  const x = D.dias[d];
  const ant = d > 1 ? diaPlan(d - 1) : null, sig = d < TOTAL ? diaPlan(d + 1) : null;
  const t = parteDe(p.parte);
  const artParte = ARTS.find(a => a.grupo === 'parte' && a.parte === p.parte);
  const empiezaParte = artParte && (!ant || ant.parte !== p.parte);
  const nVers = p.b - p.a + 1;
  let h = `<article class="hoja" id="dia-art">${empiezaParte ? `<div class="aviso-parte" style="margin:0 0 18px"><span>Empieza el <b>${esc(artParte.titulo)}</b>. Antes de leer, conviene mirar el panorama.</span><a class="btn" href="#art-${artParte.id}">Ver el panorama →</a></div>` : ''}<span class="ojo">${esc(t.etiqueta)} · Día ${d} de ${TOTAL}</span>
    <h1 class="titulo">${esc(x ? x.titulo : p.titulo)}</h1>
    <div class="meta"><span>Santiago ${esc(p.desde)}${p.desde === p.hasta ? '' : '–' + esc(p.hasta)}</span><span>${nVers} ${nVers === 1 ? 'versículo' : 'versículos'}</span>${x ? `<span>≈ ${x.minutos.lectura} min de lectura + ${x.minutos.estudio} de estudio</span>` : ''}
      ${p.compartido ? `<span class="insignia">Parte ${p.compartido.n} de ${p.compartido.de}${p.foco ? ' · ' + esc(p.foco) : ''}</span>` : ''}</div>
    <div class="acciones"><button class="btn ${est.hechos[d] ? 'oro' : ''}" id="hecho-btn">${est.hechos[d] ? '✓ Terminado' : 'Marcar como terminado'}</button>
      <a class="btn" href="#carta" data-ir-carta="${p.a}">Ver en la carta completa</a><button class="btn" id="imprimir-btn">Imprimir este día</button></div>`;
  if (x) {
    const tot = x.minutos.lectura + x.minutos.estudio + 5;
    h += `<nav class="seguimiento" id="seg" aria-label="Pasos del día"><ol>
      <li><a href="#dia-${d}" data-ir="paso-1"><b>1</b>Ubíquense</a></li><li><a href="#dia-${d}" data-ir="paso-2"><b>2</b>Lean</a></li>
      <li><a href="#dia-${d}" data-ir="paso-3"><b>3</b>Estudien</a></li><li><a href="#dia-${d}" data-ir="paso-4"><b>4</b>Conversen y oren</a></li>
      <li><a href="#dia-${d}" data-ir="paso-5"><b>5</b>Anoten</a></li></ol>
      <div class="linea" role="progressbar" aria-label="Avance de la lectura del día" aria-valuemin="0" aria-valuemax="100"><i></i></div>
      <div class="quedan"><span>Lectura del día</span><span>quedan ≈ <b data-total="${tot}">${tot}</b> min</span></div></nav>`;
  }
  if (!x) {
    h += `<div class="panel pend-msg"><p><b>Este día está en preparación.</b> El plan ya lo tiene ubicado; el estudio se está escribiendo con el material de la biblioteca.</p></div>${pasajeHTML(p, true)}`;
  } else {
    const c = x.contexto;
    h += `<section id="paso-1"><div class="contexto panel"><div><span class="et">Antes</span><p>${esc(c.antes)}</p></div><div class="ahora"><span class="et">Ahora</span><p>${esc(c.ahora)}</p></div><div><span class="et">Después</span><p>${esc(c.despues)}</p></div></div>
      <div class="donde-cuando"><div class="panel"><span class="ojo">Dónde</span><br>${esc(c.donde)}</div><div class="panel"><span class="ojo">Cuándo</span><br>${esc(c.cuando)} ${chips(c.fuentes)}</div></div></section>`;
    h += `<section id="paso-2">${pasajeHTML(p, nVers <= 12)}`;
    const vk = x.versiculo_clave, vkr = refIdx(vk.ref);
    if (vkr) { const txt = []; for (let i = vkr[0]; i <= vkr[1]; i++) { const [cc, vv] = deIdx(i); txt.push(vtxt(cc, vv)); }
      h += `<figure class="clave"><blockquote>«${esc(txt.filter(Boolean).join(' ')).replace(/\n/g, ' / ')}»</blockquote><cite>Santiago ${esc(vk.ref)} · RVR1960</cite><p class="porque">${esc(vk.porque)}</p></figure>`; }
    h += '</section><section id="paso-3">';
    h += `<h2>El pasaje de un vistazo</h2>${parr(x.panorama.texto)}${chips(x.panorama.fuentes)}`;
    h += `<h2>Versículo por versículo</h2>` + x.secciones.map(s => {
      const r = refIdx(s.rango), entero = r && r[0] === p.a && r[1] === p.b;
      return `<h3><span class="rango">${esc(s.rango)}</span>${esc(s.titulo)}</h3>` + (r && !entero ? `<div class="vers-linea">${versosHTML(r[0], r[1])}</div>` : '') +
        s.notas.map(n => `<p class="nota">${esc(n.texto)} ${chips(n.fuentes)}</p>`).join(''); }).join('');
    if (x.diagrama) h += diagramaHTML(x.diagrama);
    if (x.palabras.length) h += `<h2>Palabras para entender</h2><div class="palabras">` + x.palabras.map(w => `<div class="palabra">${w.griego ? `<span class="gr" lang="grc">${esc(w.griego)}</span>` : w.hebreo ? `<span class="heb" lang="he">${esc(w.hebreo)}</span>` : ''}
      <span class="tr">${esc(w.translit)}</span> <span class="rf">· ${esc(w.ref)}</span><p>${esc(w.significado)} ${chips(w.fuentes)}</p></div>`).join('') + '</div>';
    if ((x.eco_de_jesus || []).length) h += `<h2>Ecos de las palabras de Jesús</h2>` + x.eco_de_jesus.map(k => `<div class="eco"><p>${esc(k.texto)} ${chips(k.fuentes)}</p>${k.refs && k.refs.length ? `<span class="refs">${esc(k.refs.join(' · '))}</span>` : ''}</div>`).join('');
    if (x.cristo.length) h += `<h2>Cristo en el pasaje</h2>` + x.cristo.map(k => `<div class="cristo"><p>${esc(k.texto)} ${chips(k.fuentes)}</p>${k.refs && k.refs.length ? `<span class="refs">${esc(k.refs.join(' · '))}</span>` : ''}</div>`).join('');
    if (x.interpretaciones.length) h += `<h2>Preguntas difíciles e interpretaciones</h2>` + x.interpretaciones.map(i => `<details class="interp"><summary>${esc(i.tema)}</summary><div class="cuerpo">` +
      i.posturas.map(q => `<div class="postura"><span class="quien">${esc(q.quien)}</span><span>${esc(q.postura)} ${chips(q.fuentes)}</span></div>`).join('') +
      (i.nota ? `<p style="margin-top:10px;font-size:.92rem">${esc(i.nota)}</p>` : '') + '</div></details>').join('');
    if (x.biblioteca && x.biblioteca.length) h += `<h2>Desde la biblioteca</h2><div class="biblio">` + x.biblioteca.map(b => `<div class="panel"><span class="autor">${esc(b.autor)} · ${esc(b.obra)}</span>${esc(b.texto)} ${chips(b.fuentes)}</div>`).join('') + '</div>';
    if (x.conexiones.length) h += `<h2>Conexiones con el resto de la Biblia</h2><div class="conex">` + x.conexiones.map(k => `<span class="rf">${esc(k.ref)}</span><span>${esc(k.nota)} ${chips(k.fuentes)}</span>`).join('') + '</div>';
    h += '</section><section id="paso-4">';
    h += `<div class="vida"><h2>Para la vida de ustedes</h2><ul>${x.para_vivir.map(v => `<li>${esc(v.texto)} ${chips(v.fuentes)}</li>`).join('')}</ul>
      <h3>Para conversar</h3><ol>${x.para_conversar.map(q => `<li>${esc(q)}</li>`).join('')}</ol>
      <h3>Para orar</h3><p class="orar">${esc(x.para_orar)}</p></div>`;
    if (x.profundizar.length) h += `<details class="prof"><summary>Para profundizar (optativo)</summary>` + x.profundizar.map(f => `<h3>${esc(f.titulo)}</h3><p>${esc(f.texto)} ${chips(f.fuentes)}</p>`).join('') + '</details>';
    const rel = articulosDelDia(d);
    if (rel.length) h += `<h2>Para ir más a fondo</h2><div class="anexos">${rel.map(({ a, por }) => `<a href="#art-${a.id}"><span class="ojo">${GRUPOS[a.grupo]}</span><b>${esc(tituloArt(a))}</b><small>${esc(por || (artDe(a.id) || {}).bajada || '')}</small></a>`).join('')}</div>`;
    h += '</section>';
  }
  h += bloqueNotas(d);
  h += `<nav class="pie-dia" aria-label="Días">${ant ? `<a class="btn" href="#dia-${ant.dia}">← Día ${ant.dia}</a>` : '<span></span>'}
    ${sig ? `<button class="btn prim" id="hecho-sig" data-sig="${sig.dia}">${est.hechos[d] ? 'Seguir con el día ' + sig.dia : 'Terminar el día y seguir'} →</button>` : `<button class="btn prim" id="hecho-fin">${est.hechos[d] ? 'Volver al inicio' : 'Terminar la carta ✓'}</button>`}</nav></article>`;
  return h;
}
function ladoDia(d) {
  const p = diaPlan(d), x = D.dias[d];
  let h = `<div class="tarjeta"><h5>Dónde estamos en la carta</h5>${tira(false, d)}<div class="leyenda" style="margin-top:8px">Santiago ${esc(p.desde)}${p.desde === p.hasta ? '' : '–' + esc(p.hasta)} · día ${d} de ${TOTAL}</div></div>`;
  const lugares = ((D.lugares_dia || {})[d] || []).map(id => D.mapas.lugares.find(l => l.id === id)).filter(Boolean);
  if (lugares.length) h += `<div class="tarjeta mini-mapa"><h5>Dónde</h5>${mapaSVG(marcoPara(lugares.map(l => l.id)), null, lugares.map(l => l.id), true)}
    <div class="leyenda">${lugares.map(l => esc(l.nombre)).join(' · ')} · <a href="#mapas">abrir mapas</a></div></div>`;
  const t = (D.linea_dia || {})[d];
  if (t) h += `<div class="tarjeta"><h5>En la historia</h5><div>${esc(t.texto)}</div><div class="tiempo-barra"><span style="left:${t.desde}%;width:${Math.max(1.5, t.hasta - t.desde)}%"></span></div><div class="tiempo-et"><span>${esc(D.linea.inicio_et)}</span><span>${esc(D.linea.fin_et)}</span></div></div>`;
  if (x && x.palabras.some(w => w.griego)) h += `<div class="tarjeta"><h5>Palabras del día</h5>${x.palabras.filter(w => w.griego).slice(0, 6).map(w => `<div style="display:flex;justify-content:space-between;gap:8px;padding:3px 0"><span>${esc(w.translit)}</span><span class="gr" lang="grc" style="color:var(--tinta);font-size:1.05rem">${esc(w.griego)}</span></div>`).join('')}</div>`;
  const cl = clavesDelDia(p);
  if (cl.length) h += `<div class="tarjeta"><h5>Palabras del pasaje en toda la carta</h5>${cl.map(r => miniGrafico(r, deIdx(p.a)[0])).join('')}<div class="leyenda">Cuántas veces aparece en cada capítulo. <a href="#claves">Ver todas</a></div></div>`;
  const hechos = hechosN();
  h += `<div class="tarjeta"><h5>Su avance</h5><div>${hechos} de ${TOTAL} días terminados.</div><div class="tiempo-barra" style="margin-top:8px"><span style="left:0;width:${100 * hechos / TOTAL}%;background:var(--oliva)"></span></div></div>`;
  return h;
}

/* ---------- seguimiento del día (pasos y avance de lectura) ---------- */
let quitarScroll = null;
function activarSeguimiento() {
  if (quitarScroll) { quitarScroll(); quitarScroll = null; }
  const seg = $('#seg'), art = $('#dia-art'); if (!seg || !art) return;
  const els = [1, 2, 3, 4, 5].map(k => document.getElementById('paso-' + k));
  const barra = seg.querySelector('.linea i'), quedan = seg.querySelector('.quedan b'), total = +quedan.dataset.total;
  const enlaces = seg.querySelectorAll('a');
  const f = () => {
    const r = art.getBoundingClientRect(), alto = Math.max(1, art.offsetHeight - innerHeight * 0.55);
    const rec = Math.min(1, Math.max(0, (-r.top + innerHeight * 0.2) / alto));
    barra.style.width = (100 * rec).toFixed(1) + '%'; seg.querySelector('.linea').setAttribute('aria-valuenow', Math.round(100 * rec));
    quedan.textContent = Math.max(0, Math.round(total * (1 - rec)));
    let act = 0; els.forEach((el, k) => { if (el && el.getBoundingClientRect().top <= innerHeight * 0.42) act = k; });
    if (rec > .985) act = 4;
    enlaces.forEach((a, k) => { a.classList.toggle('activo', k === act); a.classList.toggle('pasado', k < act); });
  };
  addEventListener('scroll', f, { passive: true }); addEventListener('resize', f); f();
  quitarScroll = () => { removeEventListener('scroll', f); removeEventListener('resize', f); };
}
document.addEventListener('click', e => {
  const a = e.target.closest('[data-ir]'); if (!a) return;
  e.preventDefault(); const el = document.getElementById(a.dataset.ir); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  if (a.dataset.ir.startsWith('paso-')) { if (a.dataset.ir === 'paso-2') { const d = document.getElementById('pasaje'); if (d) d.open = true; } }
});
document.addEventListener('click', e => {
  const b = e.target.closest('#ver-griego'); if (!b) return;
  const caja = $('#caja-griego'), on = b.getAttribute('aria-pressed') !== 'true';
  b.setAttribute('aria-pressed', on); caja.hidden = !on; b.textContent = on ? 'Ocultar el texto griego' : 'Ver el texto griego';
});

/* ---------- la carta completa ---------- */
let verGriegoCarta = false;
function vistaCarta() {
  let h = `<div class="hoja"><span class="ojo">Herramientas</span><h1 class="titulo">La carta completa</h1>
    <p>Los cinco capítulos de Santiago de corrido (Reina-Valera 1960). Antes de cada tramo aparece el día del plan que lo estudia; tocándolo se abre.</p>
    <div class="acciones"><button class="btn tog" id="carta-griego" aria-pressed="${verGriegoCarta}">${verGriegoCarta ? 'Ocultar el griego' : 'Mostrar el griego debajo de cada versículo'}</button></div>`;
  for (let c = 1; c <= 5; c++) {
    h += `<div class="carta-cap">Capítulo ${c}</div>`;
    for (let v = 1; v <= NV[c - 1]; v++) {
      const i = idxv(c, v);
      PLAN.filter(p => p.a === i && (!p.compartido || p.compartido.n === 1)).forEach(p => {
        h += `<a class="carta-dia ${est.hechos[p.dia] ? 'hecho' : ''}" href="#dia-${p.dia}"><span>${est.hechos[p.dia] ? '✓ ' : ''}Día ${p.dia} · ${esc((D.dias[p.dia] || p).titulo)}</span><span>Stg ${esc(p.desde)}${p.desde === p.hasta ? '' : '–' + esc(p.hasta)}</span></a>`;
      });
      h += `<div class="carta-v" id="cv-${c}-${v}"><span class="n">${v}</span><div>${esc(vtxt(c, v) || '').replace(/\n/g, ' ')}${verGriegoCarta && gtxt(c, v) ? `<div class="griego-v gr" lang="grc" style="margin-left:0">${esc(gtxt(c, v))}</div>` : ''}</div></div>`;
    }
  }
  h += `<div class="leyenda" style="margin-top:20px">${esc(D.aviso_rvr || '')}${verGriegoCarta ? ' ' + esc(D.aviso_griego || '') : ''}</div></div>`;
  return h;
}
document.addEventListener('click', e => { if (e.target.closest('#carta-griego')) { verGriegoCarta = !verGriegoCarta; render(true); } });

/* ---------- mapas ---------- */
function marcoPara(ids) {
  const ls = ids.map(id => D.mapas.lugares.find(l => l.id === id)).filter(Boolean);
  return ls.length && ls.every(l => l.canaan) ? 'canaan' : 'oriente';
}
function mapaSVG(marco, vista, resaltar, mini) {
  const M = D.mapas.marcos[marco]; if (!M) return '';
  const set = new Set(resaltar || []);
  const V = vista ? D.mapas.vistas.find(v => v.id === vista) : null;
  const ruta = V && V.ruta ? V.ruta.map(id => D.mapas.lugares.find(l => l.id === id)).filter(l => l && l[marco]) : [];
  const enVista = new Set(V ? V.lugares : []);
  const visibles = D.mapas.lugares.filter(l => l[marco] && (V ? (enVista.has(l.id) || (l.tipo === 'region' && !mini && enVista.has(l.id))) : mini ? set.has(l.id) : true));
  let vb = [0, 0, M.W, M.H];
  if (mini && visibles.length) {
    const xs = visibles.map(l => l[marco][0]), ys = visibles.map(l => l[marco][1]);
    let x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    const minW = M.W * (marco === 'canaan' ? .55 : .32), cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    let w = Math.max(minW, (x1 - x0) * 1.5), h = Math.max(w * .8, (y1 - y0) * 1.5); w = Math.max(w, h / .8);
    vb = [Math.max(0, Math.min(M.W - w, cx - w / 2)), Math.max(0, Math.min(M.H - h, cy - h / 2)), Math.min(w, M.W), Math.min(h, M.H)];
  }
  const k = vb[2] / M.W, fs = (marco === 'canaan' ? 15 : 14) * Math.max(k, mini ? .45 : .7) * (mini ? 1.6 : 1), rr = fs * .38;
  const linea = ruta.length > 1 ? `<polyline points="${ruta.map(s => s[marco].join(',')).join(' ')}" fill="none" stroke="var(--terracota)" stroke-width="${fs * .18}" stroke-dasharray="${fs * .5} ${fs * .35}" stroke-linejoin="round" stroke-linecap="round"/>` : '';
  const cajas = [], choca = b => cajas.some(c => b[0] < c[2] && b[2] > c[0] && b[1] < c[3] && b[3] > c[1]);
  const orden = visibles.slice().sort((a, b) => (set.has(b.id) || b.destacado) - (set.has(a.id) || a.destacado) || (a.tipo === 'region') - (b.tipo === 'region'));
  const puntos = [], textos = [];
  orden.forEach(l => {
    const [x, y] = l[marco]; const dest = set.has(l.id) || l.destacado;
    if (l.tipo === 'region') {
      const w = l.nombre.length * fs * .5, b = [x - w / 2, y - fs, x + w / 2, y + 2];
      if (!choca(b)) { cajas.push(b); textos.push(`<text x="${x}" y="${y}" text-anchor="middle" font-size="${fs * 1.05}" font-style="italic" fill="var(--muted)" font-family="var(--f-display)">${esc(l.nombre)}</text>`); }
      return;
    }
    const r = dest ? rr * 1.5 : rr;
    puntos.push(`<g class="lugar" data-id="${l.id}" style="cursor:pointer"><title>${esc(l.nombre)}</title><circle cx="${x}" cy="${y}" r="${r}" fill="${dest ? 'var(--oro)' : 'var(--ink)'}" stroke="var(--surface)" stroke-width="${r * .35}" ${l.certeza === 'baja' ? `stroke-dasharray="${r * .5} ${r * .5}"` : ''}/></g>`);
    const w = l.nombre.length * fs * .52;
    for (const [dx, anc] of [[r + fs * .35, 'start'], [-(r + fs * .35), 'end']]) {
      const bx = anc === 'start' ? [x + dx, y - fs * .8, x + dx + w, y + fs * .3] : [x + dx - w, y - fs * .8, x + dx, y + fs * .3];
      if (!choca(bx)) { cajas.push(bx); textos.push(`<text x="${x + dx}" y="${y + fs * .33}" text-anchor="${anc}" font-size="${fs}" font-family="var(--f-ui)" font-weight="${dest ? 600 : 400}" fill="var(--ink)" paint-order="stroke" stroke="var(--surface)" stroke-width="${fs * .22}">${esc(l.nombre)}</text>`); break; }
    }
  });
  const rios = Object.values(M.rios).map(v => `<path d="${v}" fill="none" stroke="var(--tinta)" stroke-width="${(marco === 'canaan' ? 2 : 1.4) * Math.max(k, .5)}" opacity=".7"/>`).join('');
  return `<svg viewBox="${vb.map(v => v.toFixed(1)).join(' ')}" role="img" aria-label="Mapa${V ? ': ' + esc(V.nombre) : ''}">
    <rect x="${vb[0]}" y="${vb[1]}" width="${vb[2]}" height="${vb[3]}" fill="var(--tinta-soft)"/>
    <path d="${M.tierra}" fill="var(--surface-2)" stroke="var(--line)" stroke-width="${Math.max(k, .5)}"/>
    <path d="${M.lagos}" fill="var(--tinta-soft)" stroke="var(--tinta)" stroke-width="${.8 * Math.max(k, .5)}"/>${rios}${linea}${puntos.join('')}${textos.join('')}</svg>`;
}
let mapaSel = { vista: null };
function vistaMapas() {
  const vs = D.mapas.vistas; if (!mapaSel.vista) mapaSel.vista = vs[0].id;
  const V = vs.find(v => v.id === mapaSel.vista);
  return `<div class="hoja ancha"><span class="ojo">Herramientas</span><h1 class="titulo">Mapas</h1>
    <div class="mapa-tabs" role="group" aria-label="Mapa">${vs.map(v => `<button class="btn" data-vista="${v.id}" aria-pressed="${mapaSel.vista === v.id}">${esc(v.nombre)}</button>`).join('')}</div>
    <p>${esc(V.texto || '')} ${chips(V.fuentes)}</p>
    <div class="svgcaja" id="mapa-caja">${mapaSVG(V.marco, V.id)}</div>
    <div class="leyenda">${V.ruta ? 'Línea punteada: el recorrido. ' : ''}Punto con borde cortado: ubicación poco segura. ${esc(D.mapas.credito)}</div>
    <div class="panel ficha-lugar" id="ficha" hidden></div></div>`;
}
document.addEventListener('click', e => {
  const b = e.target.closest('[data-vista]');
  if (b && rutaActual === 'mapas') { mapaSel.vista = b.dataset.vista; render(true); return; }
  const g = e.target.closest('.lugar');
  if (g && rutaActual === 'mapas') {
    const l = D.mapas.lugares.find(x => x.id === g.dataset.id); const f = $('#ficha');
    const dias = Object.entries(D.lugares_dia || {}).filter(([d, ids]) => ids.includes(l.id)).map(([d]) => +d);
    f.hidden = false; f.innerHTML = `<b style="font:600 1.2rem var(--f-display)">${esc(l.nombre)}</b><p style="margin:4px 0">${esc(l.nota || '')} ${chips(l.fuentes)}</p>
      <div class="estado">Certeza de la ubicación: ${esc({ alta: 'alta', media: 'media', baja: 'baja', region: 'región aproximada' }[l.certeza] || '')}</div>
      ${dias.length ? `<div style="margin-top:6px">Aparece en: ${dias.map(d => `<a href="#dia-${d}">día ${d}</a>`).join(', ')}</div>` : ''}`;
  }
});

/* ---------- línea de tiempo ---------- */
function vistaLinea() {
  const L = D.linea, a0 = L.desde, a1 = L.hasta, W = 980, X0 = 210;
  const x = a => X0 + ((a - a0) / (a1 - a0)) * (W - X0 - 30);
  const filas = L.eventos, fila = 26, H = filas.length * fila + 70;
  const paso = L.paso || 5, ejes = []; for (let a = Math.ceil(a0 / paso) * paso; a <= a1; a += paso) ejes.push(a);
  const color = g => ({ historia: 'var(--tinta)', iglesia: 'var(--oliva)', santiago: 'var(--terracota)', fecha: 'var(--oro)' }[g] || 'var(--tinta)');
  const barras = filas.map((e, i) => { const y = 40 + i * fila, ini = e.desde ?? e.anio, fin = e.hasta ?? e.anio;
    const w = Math.max(8, x(fin) - x(ini)), xx = fin === ini ? x(ini) - 4 : x(ini);
    return `<text x="${X0 - 8}" y="${y + 13}" text-anchor="end" font-size="12.5" font-family="var(--f-ui)" fill="var(--ink)">${esc(e.nombre)}</text>
      <rect x="${xx}" y="${y}" width="${w}" height="16" rx="${fin === ini ? 8 : 4}" fill="${color(e.grupo)}" opacity=".88"><title>${esc(e.nombre)}: ${ini === fin ? 'año ' + ini : ini + '–' + fin} d. C.${e.dato ? ' · ' + e.dato : ''}</title></rect>`; }).join('');
  const lineas = ejes.map(a => `<line x1="${x(a)}" y1="30" x2="${x(a)}" y2="${H - 24}" stroke="var(--line)"/><text x="${x(a)}" y="22" font-size="11" text-anchor="middle" fill="var(--muted)" font-family="var(--f-ui)">${a}</text>`).join('');
  return `<div class="hoja ancha"><span class="ojo">Herramientas</span><h1 class="titulo">Línea de tiempo</h1>
    <p>${esc(L.explicacion)}</p><div class="svgcaja"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Línea de tiempo de Santiago y la iglesia primitiva">${lineas}${barras}</svg></div>
    <div class="leyenda">Años de la era cristiana (d. C.). Azul: historia general · Verde: la iglesia primitiva · Terracota: Santiago y su carta · Oro: fechas que proponen las fuentes para la carta.</div>
    <div class="panel" style="margin-top:16px"><b>Una advertencia de las fuentes.</b> ${esc(L.advertencia)} ${chips(L.fuentes)}</div>
    <h2>Los datos, uno por uno</h2><table class="tabla"><thead><tr><th>Hecho</th><th>Cuándo</th><th>Dato</th></tr></thead><tbody>
    ${L.eventos.map(e => `<tr><td>${esc(e.nombre)}</td><td>${e.desde != null && e.hasta != null && e.desde !== e.hasta ? e.desde + '–' + e.hasta : (e.anio ?? e.desde)}</td><td>${esc(e.dato || '')} ${chips(e.fuentes)}</td></tr>`).join('')}</tbody></table></div>`;
}

/* ---------- palabras griegas, Cristo, ecos ---------- */
function vistaPalabras() {
  const todas = []; Object.entries(D.dias).forEach(([d, x]) => x.palabras.forEach(w => todas.push({ ...w, d: +d })));
  todas.sort((a, b) => a.translit.localeCompare(b.translit, 'es'));
  return `<div class="hoja ancha"><span class="ojo">Herramientas</span><h1 class="titulo">Palabras griegas</h1>
    <p>Las palabras que comentan las fuentes, reunidas de todos los días ya escritos (${todas.length}). La grafía griega se comprobó contra el texto griego de Santiago (SBLGNT).</p><div class="lista-pal">` +
    todas.map(w => `<div class="palabra">${w.griego ? `<span class="gr" lang="grc">${esc(w.griego)}</span>` : ''}<span class="tr">${esc(w.translit)}</span> <span class="rf">· Stg ${esc(w.ref)} · <a href="#dia-${w.d}">día ${w.d}</a></span><p>${esc(w.significado)}</p></div>`).join('') + '</div></div>';
}
function vistaCristo() {
  const items = []; Object.entries(D.dias).forEach(([d, x]) => x.cristo.forEach(k => items.push({ ...k, d: +d, p: diaPlan(+d) })));
  const art = ARTS.find(a => a.grupo === 'tema' && /cristo/i.test(a.titulo));
  return `<div class="hoja"><span class="ojo">Herramientas</span><h1 class="titulo">Cristo en Santiago</h1>
    <p>Cómo la carta muestra a Jesús, según las fuentes de cada día.${art && artDe(art.id) ? ' Para verlo reunido en un solo recorrido, lean el tema <a href="#art-' + art.id + '">' + esc(artDe(art.id).titulo) + '</a>.' : ''}</p>` +
    items.map(k => `<div class="cristo"><span class="ojo"><a href="#dia-${k.d}">Día ${k.d} · Stg ${esc(k.p.desde)}–${esc(k.p.hasta)}</a></span><p>${esc(k.texto)} ${chips(k.fuentes)}</p>${k.refs && k.refs.length ? `<span class="refs">${esc(k.refs.join(' · '))}</span>` : ''}</div>`).join('') + '</div>';
}
function vistaEcos() {
  const items = []; Object.entries(D.dias).forEach(([d, x]) => (x.eco_de_jesus || []).forEach(k => items.push({ ...k, d: +d, p: diaPlan(+d) })));
  items.sort((a, b) => a.p.a - b.p.a);
  const art = ARTS.find(a => /jesús|sermón/i.test(a.titulo) && a.grupo !== 'parte');
  return `<div class="hoja"><span class="ojo">Herramientas</span><h1 class="titulo">Santiago y las palabras de Jesús</h1>
    <p>Santiago casi nunca cita a Jesús, pero la carta suena a sus enseñanzas, sobre todo al Sermón del Monte. Aquí se reúnen los ecos que señalan las fuentes, en el orden de la carta.${art && artDe(art.id) ? ' Más a fondo: <a href="#art-' + art.id + '">' + esc(artDe(art.id).titulo) + '</a>.' : ''}</p>` +
    (items.length ? items.map(k => `<div class="eco"><span class="ojo"><a href="#dia-${k.d}">Día ${k.d} · Stg ${esc(k.p.desde)}–${esc(k.p.hasta)}</a></span><p>${esc(k.texto)} ${chips(k.fuentes)}</p>${k.refs && k.refs.length ? `<span class="refs">${esc(k.refs.join(' · '))}</span>` : ''}</div>`).join('') : '<p>Todavía no hay ecos cargados.</p>') + '</div>';
}

/* ---------- palabras de la carta (gráfico) ---------- */
let claveSel = null;
function vistaClaves() {
  const cuenta = conteosClaves().slice().sort((x, y) => y.tot - x.tot);
  const max = Math.max(...cuenta.flatMap(r => r.por));
  const sel = claveSel && cuenta.find(r => r.n === claveSel.n);
  return `<div class="hoja ancha"><span class="ojo">Herramientas</span><h1 class="titulo">Palabras de la carta</h1>
    <p>Cuántas veces aparece cada palabra clave en cada capítulo (Reina-Valera 1960). Toquen un número para ver los versículos. Es un conteo del propio texto: sirve para ver qué temas pesan en cada tramo de la carta.</p>
    <div class="svgcaja"><table class="calor"><thead><tr><th></th>${[1, 2, 3, 4, 5].map(c => `<th>Cap. ${c}</th>`).join('')}<th>Total</th></tr></thead><tbody>
    ${cuenta.map(r => `<tr><td class="pal">${esc(r.n)}</td>${r.por.map((n, k) => `<td><button data-clave="${esc(r.n)}" data-cap="${k + 1}" data-n="${n}" aria-pressed="${!!(claveSel && claveSel.n === r.n && claveSel.c === k + 1)}" style="--i:${(n / max).toFixed(2)}">${n}</button></td>`).join('')}<td><b>${r.tot}</b></td></tr>`).join('')}</tbody></table></div>
    <div id="claves-res">${claveSel && sel ? clavesResultado(sel, claveSel.c) : '<p class="leyenda" style="margin-top:12px">Toquen un número para ver dónde está.</p>'}</div></div>`;
}
function clavesResultado(r, c) {
  const vs = r.vers[c - 1]; if (!vs.length) return '';
  return `<h2>«${esc(r.n)}» en el capítulo ${c}</h2>` + vs.map(v => `<div class="carta-v"><span class="n"><a href="#dia-${diaQueContiene(c + ':' + v)}">${c}:${v}</a></span><div>${esc(vtxt(c, v))}</div></div>`).join('');
}
document.addEventListener('click', e => {
  const b = e.target.closest('[data-clave]'); if (!b || rutaActual !== 'claves' || b.dataset.n === '0') return;
  claveSel = { n: b.dataset.clave, c: +b.dataset.cap }; render(true);
});

/* ---------- búsqueda, fuentes, textos ---------- */
let indice = null;
function vistaBuscar() {
  return `<div class="hoja"><span class="ojo">Herramientas</span><h1 class="titulo">Buscar</h1><div class="buscar"><label for="q" class="estado">Buscar en todo el estudio y en el texto de la carta, o escribir un versículo (por ejemplo 2:14)</label><input id="q" type="search" placeholder="Por ejemplo: lengua, Rahab, 2:14…" autocomplete="off"></div><div id="res"></div></div>`;
}
function armarIndice() {
  indice = [];
  ARTS.forEach(a => { const x = artDe(a.id); if (!x) return;
    const push = (sec, t) => t && indice.push({ href: '#art-' + a.id, lab: tituloArt(a), sec, t });
    push('Entrada', x.entrada.texto);
    x.apartados.forEach(s => s.parrafos.forEach(q => push(s.titulo, q.texto)));
    (x.interpretaciones || []).forEach(i => i.posturas.forEach(p => push('Interpretación: ' + i.tema, p.quien + ': ' + p.postura)));
    (x.conexiones || []).forEach(k => push('Conexión: ' + k.ref, k.nota));
    (x.tablas || []).forEach(tb => (tb.filas || []).forEach(f => push('Tabla: ' + tb.titulo, (Array.isArray(f) ? f : f.celdas || []).join(' · '))));
  });
  Object.entries(D.dias).forEach(([d, x]) => {
    const push = (sec, t) => t && indice.push({ href: '#dia-' + d, lab: 'Día ' + d, sec, t });
    push('Panorama', x.panorama.texto);
    x.secciones.forEach(s => s.notas.forEach(n => push(s.rango + ' · ' + s.titulo, n.texto)));
    x.palabras.forEach(w => push('Palabra: ' + w.translit, w.significado));
    x.cristo.forEach(k => push('Cristo en el pasaje', k.texto));
    (x.eco_de_jesus || []).forEach(k => push('Eco de Jesús', k.texto));
    x.interpretaciones.forEach(i => i.posturas.forEach(p => push('Interpretación: ' + i.tema, p.quien + ': ' + p.postura)));
    (x.biblioteca || []).forEach(b => push('Biblioteca: ' + b.autor, b.texto));
    x.profundizar.forEach(f => push('Profundizar: ' + f.titulo, f.texto));
  });
  for (let c = 1; c <= 5; c++) for (let v = 1; v <= NV[c - 1]; v++) indice.push({ href: '#dia-' + diaQueContiene(c + ':' + v), lab: `Santiago ${c}:${v}`, sec: 'Texto de la carta (RVR1960)', t: vtxt(c, v) || '' });
}
document.addEventListener('input', e => {
  if (e.target.id === 'notas-dia') {
    const d = +e.target.dataset.dia; est.notas[d] = e.target.value; marcarEstado('Guardando…');
    clearTimeout(window._tn); window._tn = setTimeout(async () => { await escribirDia(d); marcarEstado(db ? 'Guardado y compartido.' : 'Guardado en esta compu.'); }, 900);
  }
  if (e.target.id === 'q') {
    if (!indice) armarIndice();
    const raw = e.target.value.trim(), q = sinTildes(raw);
    const mv = raw.match(/^(?:santiago|stgo?|sant)?\.?\s*(\d)\s*[:.,]\s*(\d{1,2})$/i);
    let pre = '';
    if (mv && +mv[1] >= 1 && +mv[1] <= 5 && +mv[2] >= 1 && +mv[2] <= NV[+mv[1] - 1]) {
      const c = +mv[1], v = +mv[2], ds = diasDelVerso[idxv(c, v)];
      pre = `<div class="resultado"><b>Santiago ${c}:${v}</b> — ${ds.map(d => `<a href="#dia-${d}">día ${d}</a>`).join(', ')}<div>${esc(vtxt(c, v))}</div></div>`;
    }
    const res = q.length < 3 ? [] : indice.filter(r => sinTildes(r.t + ' ' + r.sec).includes(q)).slice(0, 80);
    $('#res').innerHTML = pre + (q.length < 3 ? '' : (res.length ? res.map(r => { const i = sinTildes(r.t).indexOf(q); const ini = Math.max(0, i - 90);
      const frag = esc(r.t.slice(ini, ini + 260)); return `<div class="resultado"><a href="${r.href}"><b>${esc(r.lab)}</b> · ${esc(r.sec)}</a><div>${ini ? '…' : ''}${frag}…</div></div>`; }).join('') : (pre ? '' : '<p>No hay resultados.</p>')));
  }
});
function vistaTexto(clave) {
  const t = D.textos[clave]; if (!t) return vistaInicio();
  return `<article class="hoja"><span class="ojo">${esc(t.ojo)}</span><h1 class="titulo">${esc(t.titulo)}</h1>${t.html}</article>`;
}
function vistaFuentes() {
  const F = D.obras;
  return `<div class="hoja"><span class="ojo">Herramientas</span><h1 class="titulo">Fuentes del estudio</h1>${D.textos.fuentes.html}
    <h2>Comentarios de Santiago</h2><table class="tabla"><tbody>${F.comentarios.map(o => `<tr><td><b>${esc(o[0])}</b></td><td>${esc(o[1])}</td></tr>`).join('')}</tbody></table>
    <h2>Libros de referencia citados</h2><p style="font-size:.92rem;color:var(--muted)">Solo autores protestantes confiables. ${F.referencia.length} obras aportaron al estudio.</p>
    <table class="tabla"><tbody>${F.referencia.map(o => `<tr><td>${esc(o[0])}</td><td>${esc(o[1])}</td></tr>`).join('')}</tbody></table>
    <h2>Textos y datos</h2><p style="font-size:.92rem">${esc(D.aviso_rvr || '')}</p><p style="font-size:.92rem">${esc(D.aviso_griego || '')}</p><p style="font-size:.92rem">${esc(D.mapas.credito || '')}</p></div>`;
}

/* ---------- introducción, partes, temas y anexos ---------- */
function estructuraLibro() {
  const max = Math.max(...PARTES.map(t => t.versos));
  let h = '<div class="estructura" role="list" aria-label="Las partes de la carta">';
  PARTES.forEach(t => {
    const d = PLAN.find(p => p.parte === t.id);
    h += `<a role="listitem" href="#dia-${d ? d.dia : 1}"><span class="et">${esc(t.titulo)}<small>${esc(t.etiqueta)} · Stg ${esc(t.rango)} · ${t.versos} versículos</small></span>
      <span class="b" style="width:${(100 * t.versos / max).toFixed(1)}%;background:${COLOR_PARTE[t.id]}"></span></a>`;
  });
  return h + '</div>';
}
function indiceArts(grupo) {
  return '<div class="indice-arts">' + ARTS.filter(a => a.grupo === grupo).map((a, i) => { const x = artDe(a.id);
    return `<a href="#art-${a.id}" class="${x ? '' : 'pend'}"><span class="num">${grupo === 'parte' ? a.parte : i + 1}</span><b>${esc(tituloArt(a))}</b>
      <small>${esc(x ? x.bajada : 'En preparación.')}</small></a>`; }).join('') + '</div>';
}
function vistaIntro() {
  const t = D.textos.introduccion || {};
  return `<article class="hoja"><span class="ojo">Antes de empezar</span><h1 class="titulo">Introducción a Santiago</h1>
    <p class="bajada">Quién escribió la carta, a quién, cuándo y cómo está armada. Capítulos breves para leer antes del día 1, o de a uno cuando quieran.</p>
    ${indiceArts('intro')}
    <h2>Cómo está armada la carta</h2><p>Santiago no sigue un argumento único: encadena exhortaciones. Cada barra muestra el largo de una de sus cinco partes. Tocando una parte se abre su primer día.</p>
    ${estructuraLibro()}
    <h2>El panorama de cada parte</h2>${indiceArts('parte')}
    ${t.html && !ARTS.some(a => a.grupo === 'intro' && artDe(a.id)) ? t.html : ''}</article>`;
}
function vistaTemas() {
  return `<article class="hoja"><span class="ojo">Temas de Santiago</span><h1 class="titulo">Los grandes temas</h1>
    <p class="bajada">Lo que Santiago enseña de punta a punta, reunido desde todos los comentarios y libros de la biblioteca. Sirven para repasar al terminar una parte o para estudiar un tema a fondo.</p>
    ${indiceArts('tema')}</article>`;
}
function vistaAnexos() {
  return `<article class="hoja"><span class="ojo">Para ir más a fondo</span><h1 class="titulo">Anexos</h1>
    <p class="bajada">Material de consulta que acompaña a los días: cuadros comparativos, personas, fechas. Los días enlazan al anexo que les corresponde.</p>
    ${indiceArts('anexo')}</article>`;
}
const palabrasDe = o => { let n = 0; JSON.stringify(o, (k, v) => { if (typeof v === 'string' && k !== 'fuentes' && k !== 'notas_no_usadas') n += v.split(/\s+/).length; return v; }); return n; };
function diasDeRefs(refs) {
  const ds = new Set();
  (refs || []).forEach(r => { const q = refIdx(String(r).replace(/^(Stg|Santiago)\.?\s*/i, '')); if (q) for (let i = q[0]; i <= q[1]; i++) diasDelVerso[i].forEach(d => ds.add(d)); });
  return [...ds].sort((a, b) => a - b);
}
function tablaArt(tb) {
  return `<div class="tabla-art"><h4>${esc(tb.titulo)}</h4>${tb.descripcion ? `<p style="font-size:.9rem;color:var(--muted)">${esc(tb.descripcion)}</p>` : ''}<div style="overflow-x:auto"><table class="tabla"><thead><tr>${(tb.columnas || []).map(c => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>` +
    (tb.filas || []).map(f => `<tr>${(Array.isArray(f) ? f : f.celdas || []).map(c => `<td>${esc(c)}</td>`).join('')}</tr>`).join('') + `</tbody></table></div>${tb.fuentes && tb.fuentes.length ? `<div class="estado" style="margin-top:6px">Fuentes: ${chips(tb.fuentes)}</div>` : ''}</div>`;
}
function vistaArticulo(id) {
  const a = ARTS.find(x => x.id === id); if (!a) return vistaInicio();
  const x = artDe(id), grupo = ARTS.filter(y => y.grupo === a.grupo), i = grupo.indexOf(a);
  const ojo = { intro: `Introducción a Santiago · ${i + 1} de ${grupo.length}`, parte: `Panorama · Santiago ${a.rango}`, tema: `Temas de Santiago · ${i + 1} de ${grupo.length}`, anexo: `Anexo · ${i + 1} de ${grupo.length}` }[a.grupo];
  let h = `<article class="hoja"><span class="ojo">${esc(ojo)}</span><h1 class="titulo">${esc(tituloArt(a))}</h1>`;
  if (!x) return h + `<div class="panel pend-msg"><p><b>Esta sección está en preparación.</b> Se escribe con el material de la biblioteca, como los días.</p></div></article>`;
  h += `<p class="bajada">${esc(x.bajada)}</p><div class="meta"><span>≈ ${Math.max(3, Math.round(palabrasDe({ e: x.entrada, a: x.apartados }) / 200))} min de lectura</span></div>`;
  h += `<div class="entrada" style="margin-top:18px">${parr(x.entrada.texto)}${chips(x.entrada.fuentes)}</div>`;
  if (a.grupo === 'intro' && x.estructura) h += estructuraLibro();
  if (a.grupo === 'parte') {
    const ds = PLAN.filter(p => p.parte === a.parte);
    h += `<div class="panel" style="margin:18px 0;padding:10px 8px"><span class="ojo" style="padding:0 8px">Los ${ds.length} días de esta parte</span>` +
      ds.map(p => `<a class="dia-l ${est.hechos[p.dia] ? 'hecho' : ''}" href="#dia-${p.dia}"><span class="n">${p.dia}</span><span>${esc((D.dias[p.dia] || p).titulo)}</span><span class="r">${esc(p.desde)}–${esc(p.hasta)}</span></a>`).join('') + '</div>';
  }
  const versiculo = v => { const r = refIdx(v.ref); if (!r || r[1] - r[0] > 3) return ''; const tx = []; for (let k = r[0]; k <= r[1]; k++) { const [c, vv] = deIdx(k); tx.push(vtxt(c, vv)); }
    return `<figure class="clave"><blockquote>«${esc(tx.filter(Boolean).join(' ')).replace(/\n/g, ' / ')}»</blockquote><cite>Santiago ${esc(v.ref)} · RVR1960</cite>${v.porque ? `<p class="porque">${esc(v.porque)}</p>` : ''}</figure>`; };
  const cita = c => `<figure class="cita"><blockquote>«${esc(c.texto)}»</blockquote><figcaption>${esc(c.autor)}, <i>${esc(c.obra)}</i> ${chips(c.fuentes)}</figcaption></figure>`;
  const vers = (x.versiculos || []).slice(), citas = (x.citas || []).slice();
  if (vers.length) h += versiculo(vers.shift());
  x.apartados.forEach((s, k) => {
    h += `<h2 id="ap-${k}">${esc(s.titulo)}</h2>` + s.parrafos.map(q => `<p class="nota">${esc(q.texto)} ${chips(q.fuentes)}</p>`).join('');
    if (s.destacado && s.destacado.texto) h += `<aside class="destacado"><span class="et">Para retener</span><p>${esc(s.destacado.texto)} ${chips(s.destacado.fuentes)}</p></aside>`;
    if (k === x.apartados.length - 1) return;
    if (k % 2 === 0 ? vers.length : !citas.length && vers.length) h += versiculo(vers.shift());
    else if (citas.length) h += cita(citas.shift());
  });
  vers.forEach(v => { h += versiculo(v); }); citas.forEach(c => { h += cita(c); });
  (x.tablas || []).forEach(tb => { h += tablaArt(tb); });
  if (x.diagrama) h += diagramaHTML(x.diagrama);
  if (x.palabras && x.palabras.length) h += `<h2>Palabras para entender</h2><div class="palabras">` + x.palabras.map(w => `<div class="palabra">${w.griego ? `<span class="gr" lang="grc">${esc(w.griego)}</span>` : ''}
    <span class="tr">${esc(w.translit)}</span> <span class="rf">· ${esc(w.ref)}</span><p>${esc(w.significado)} ${chips(w.fuentes)}</p></div>`).join('') + '</div>';
  if (x.interpretaciones && x.interpretaciones.length) h += `<h2>Preguntas difíciles e interpretaciones</h2>` + x.interpretaciones.map(q => `<details class="interp"><summary>${esc(q.tema)}</summary><div class="cuerpo">` +
    q.posturas.map(p => `<div class="postura"><span class="quien">${esc(p.quien)}</span><span>${esc(p.postura)} ${chips(p.fuentes)}</span></div>`).join('') +
    (q.nota ? `<p style="margin-top:10px;font-size:.92rem">${esc(q.nota)}</p>` : '') + '</div></details>').join('');
  if (x.conexiones && x.conexiones.length) h += `<h2>Conexiones con el resto de la Biblia</h2><div class="conex">` + x.conexiones.map(k => `<span class="rf">${esc(k.ref)}</span><span>${esc(k.nota)} ${chips(k.fuentes)}</span>`).join('') + '</div>';
  if (((x.para_vivir || []).length) || ((x.para_conversar || []).length)) {
    h += `<section class="vida"><h2>Para la vida de ustedes</h2>${(x.para_vivir || []).length ? `<ul>${x.para_vivir.map(v => `<li>${esc(v.texto)} ${chips(v.fuentes)}</li>`).join('')}</ul>` : ''}
      ${(x.para_conversar || []).length ? `<h3>Para conversar</h3><ol>${x.para_conversar.map(q => `<li>${esc(q)}</li>`).join('')}</ol>` : ''}</section>`;
  }
  const ds = a.grupo === 'parte' ? [] : diasDeRefs(x.refs_santiago);
  if (ds.length) h += `<h2>Dónde aparece en el plan</h2><div class="en-plan">${ds.map(d => `<a class="btn" href="#dia-${d}">Día ${d} · Stg ${esc(diaPlan(d).desde)}</a>`).join('')}</div>`;
  const ant = grupo[i - 1], sig = grupo[i + 1];
  const fin = a.grupo === 'parte' ? { href: '#dia-' + PLAN.find(p => p.parte === a.parte).dia, t: 'Empezar la parte →' } : null;
  const indiceHref = { tema: 'temas', anexo: 'anexos', intro: 'introduccion', parte: 'introduccion' }[a.grupo];
  h += `<nav class="pie-dia">${ant ? `<a class="btn" href="#art-${ant.id}">← ${esc(tituloArt(ant))}</a>` : `<a class="btn" href="#${indiceHref}">← Índice</a>`}
    ${fin ? `<a class="btn prim" href="${fin.href}">${fin.t}</a>` : sig ? `<a class="btn" href="#art-${sig.id}">${esc(tituloArt(sig))} →</a>` : a.grupo === 'intro' ? `<a class="btn prim" href="#dia-1">Empezar el día 1 →</a>` : ''}</nav></article>`;
  return h;
}
function ladoArticulo(id) {
  const x = artDe(id); if (!x || !x.apartados.length) return '';
  return `<div class="tarjeta toc"><h5>En esta sección</h5>${x.apartados.map((s, k) => `<a href="#art-${id}" data-ir="ap-${k}">${esc(s.titulo)}</a>`).join('')}</div>`;
}

/* ---------- copia de seguridad de notas y avance ---------- */
function bajarCopia() {
  const datos = { app: 'santiago-en-pareja', version: 1, fecha: new Date().toISOString(), hechos: est.hechos, notas: est.notas };
  const url = URL.createObjectURL(new Blob([JSON.stringify(datos, null, 1)], { type: 'application/json' }));
  const a = document.createElement('a'); a.href = url; a.download = 'santiago-en-pareja-copia-' + datos.fecha.slice(0, 10) + '.json';
  document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
  $('#estado-copia').textContent = 'Copia descargada: ' + a.download + '.';
}
async function cargarCopia(archivo) {
  const msg = t => { $('#estado-copia').textContent = t; };
  let c; try { c = JSON.parse(await archivo.text()); } catch (e) { msg('Ese archivo no es una copia del estudio.'); return; }
  if (!c || c.app !== 'santiago-en-pareja') { msg('Ese archivo no es una copia del estudio de Santiago.'); return; }
  const tocados = new Set();
  Object.entries(c.hechos || {}).forEach(([d, f]) => { if (!est.hechos[d]) { est.hechos[d] = f; tocados.add(+d); } });
  Object.entries(c.notas || {}).forEach(([d, t]) => {
    const actual = est.notas[d] || '';
    if (!t || actual === t || actual.includes(t)) return;
    est.notas[d] = actual ? actual + '\n\n— De la copia del ' + String(c.fecha || '').slice(0, 10) + ' —\n' + t : t; tocados.add(+d);
  });
  guardarLocal(); render();
  for (const d of tocados) await escribirDia(d);
  msg(!tocados.size ? 'La copia no tenía nada que no estuviera ya guardado.' : tocados.size === 1 ? 'Copia cargada: se actualizó 1 día.' : `Copia cargada: se actualizaron ${tocados.size} días.`);
}
document.addEventListener('click', async e => {
  if (e.target.closest('#imprimir-btn')) { document.querySelectorAll('details.interp, details.prof, details.pasaje').forEach(x => { x.open = true; }); print(); }
  const hs = e.target.closest('#hecho-sig, #hecho-fin');
  if (hs) {
    const d = +(location.hash.match(/dia-(\d+)/) || [])[1];
    if (d && !est.hechos[d]) { est.hechos[d] = new Date().toISOString().slice(0, 10); pintarProgreso(); await escribirDia(d); }
    location.hash = hs.id === 'hecho-sig' ? 'dia-' + hs.dataset.sig : 'inicio';
  }
});
document.addEventListener('click', e => {
  if (e.target.closest('#bajar-copia')) bajarCopia();
  if (e.target.closest('#cargar-copia-btn')) $('#cargar-copia').click();
});
document.addEventListener('change', e => { if (e.target.id === 'cargar-copia' && e.target.files[0]) cargarCopia(e.target.files[0]); });

/* ---------- ruteo ---------- */
function render(conservar) {
  const h = (location.hash || '#inicio').slice(1);
  rutaActual = h;
  const y0 = scrollY;
  let main = '', lado = '';
  const m = h.match(/^dia-(\d+)$/);
  if (m && +m[1] >= 1 && +m[1] <= TOTAL) { const d = +m[1]; main = vistaDia(d); lado = ladoDia(d); }
  else if (h === 'carta') main = vistaCarta();
  else if (h === 'mapas') main = vistaMapas();
  else if (h === 'linea') main = vistaLinea();
  else if (h === 'palabras') main = vistaPalabras();
  else if (h === 'claves') main = vistaClaves();
  else if (h === 'ecos') main = vistaEcos();
  else if (h === 'cristo') main = vistaCristo();
  else if (h === 'buscar') main = vistaBuscar();
  else if (h === 'fuentes') main = vistaFuentes();
  else if (h === 'introduccion') main = vistaIntro();
  else if (h === 'temas') main = vistaTemas();
  else if (h === 'anexos') main = vistaAnexos();
  else if (/^art-[IPTA]\d+$/.test(h)) { main = vistaArticulo(h.slice(4)); lado = ladoArticulo(h.slice(4)); }
  else if (h === 'como-usar') main = vistaTexto(h);
  else { rutaActual = 'inicio'; main = vistaInicio(); }
  $('#principal').innerHTML = main;
  $('#lado').innerHTML = lado; $('#lado').hidden = !lado;
  document.querySelector('.app').style.gridTemplateColumns = lado ? '' : (innerWidth > 820 ? 'var(--cols-sin-lado, 290px minmax(0, 1fr))' : '');
  pintarNav(); pintarProgreso();
  const hb = $('#hecho-btn');
  if (hb) hb.onclick = async () => { const d = +m[1]; if (est.hechos[d]) delete est.hechos[d]; else est.hechos[d] = new Date().toISOString().slice(0, 10); render(true); await escribirDia(d); };
  if (m) activarSeguimiento(); else if (quitarScroll) { quitarScroll(); quitarScroll = null; }
  if (h === 'buscar') setTimeout(() => $('#q') && $('#q').focus(), 0);
  window.scrollTo(0, conservar === true ? y0 : 0);
}
addEventListener('hashchange', () => render());
addEventListener('keydown', e => {
  if (e.target.matches('input, textarea')) return;
  const m = (location.hash || '').match(/^#dia-(\d+)$/); if (!m) return;
  const d = +m[1];
  if (e.key === 'ArrowRight' && d < TOTAL) location.hash = 'dia-' + (d + 1);
  if (e.key === 'ArrowLeft' && d > 1) location.hash = 'dia-' + (d - 1);
});
render();
})();
