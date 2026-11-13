# Megaestudio bíblico integral: reglas de trabajo (leer solo esto al arrancar)

Español rioplatense, dirigido al lector de «vos». No inventar nada: todo sale de los libros de la biblioteca (autores protestantes confiables,
categoría A de `trabajo/catalogo/`) con **libro y página del PDF**, o de fuentes web verificadas con su URL. Nunca copiar texto de los libros.
RVR1960 no se sube: solo versículos clave (≤2 por día, ≤500 en total). La Biblia es el fundamento; los libros ayudan a comprenderla.
Cuando los cristianos no coinciden, cada postura con su autor y sin zanjar. Otras tradiciones y religiones: con sus propios documentos (ciclos 17–18).

## Estructura
- `trabajo/plan/ciclos.py` → `ciclos.json` y `PLAN-MAESTRO.md` (20 ciclos, 103 series, ≈1.974 días). `trabajo/plan/plan.json` = días **detallados** (id fijo, ciclo, serie, n, título): se agrega solo al final; **nunca renumerar** (las marcas del lector dependen del id).
- `trabajo/libros.json` = registro de libros (id → autor, obra, ruta). Textos por página en `$MEGA_TXT` (`/home/user/lib/pages`, no van al repo).
- `trabajo/GUIA-REDACCION.md` = cómo se escribe un día. Modelo: `trabajo/dias/dia_001.json`. Verificador: `scripts/verificar.py N` (debe quedar en OK).
- `app/construir.py` arma `estudio-biblico-integral.html` (un solo archivo, sin conexión).

## Flujo de un sprint (un lote de días)
1. Detallar la serie en `plan.json` (títulos de los días, ids nuevos al final).
2. Bajar los libros que haga falta (clon parcial: `git -C /home/user/lib/r3 sparse-checkout add "<carpeta>"`; r4 en `/home/user/lib/r4`), `scripts/registrar.py`, `scripts/textos.py`.
3. Un redactor por día (modelo Sonnet) con `GUIA-REDACCION.md`; cada uno corre `verificar.py` hasta OK.
4. `python3 scripts/rvr.py` (versículos clave) → `python3 app/construir.py` → probar con Playwright (inicio, un día, celular) → commit y push.

## Eficiencia
No leer completos `dias/`, `catalogo.json` ni los textos de los libros: buscar con `scripts/buscar.py` y leer solo las páginas elegidas.
