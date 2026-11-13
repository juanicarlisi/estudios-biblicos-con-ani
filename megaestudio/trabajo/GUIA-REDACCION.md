# Guía para escribir un día del megaestudio

Un día = un archivo `trabajo/dias/dia_NNN.json`. El modelo a seguir es `dias/dia_001.json` (leerlo primero, completo).
Todo se escribe en español rioplatense, cálido y claro, hablándole al lector de «vos».

## Reglas (no negociables)
1. **No inventar nada.** Cada afirmación sobre doctrina, historia, idiomas o lo que dice un autor sale de las páginas de los libros y lleva sus `fuentes`: `["libro#pág"]`, con el id de `libros.json` y la **página del PDF** (la que muestra la marca `[[id#n]]` de `insumo.py`). Se citan solo páginas que realmente se leyeron.
2. **La Biblia es el fundamento.** Lo que se afirma del texto bíblico se apoya con la referencia (por ejemplo «Romanos 1:20»). Una conexión que sale de la Biblia y no de un libro puede llevar `fuentes: ["biblia"]`, siempre con la referencia en el mismo texto. Los libros ayudan a comprender la Biblia; no la reemplazan.
3. **No copiar.** Los libros se resumen con palabras propias. Texto literal solo en `citas[].texto` (hasta 25 palabras, exactas, de una página sin errores de OCR) y en frases breves entre «» (hasta 12 palabras, exactas).
4. **Posturas.** Si los autores consultados difieren, va en `interpretaciones` con cada postura atribuida a quien la sostiene según las fuentes, sin zanjar. No se describe lo que cree un grupo (católicos, arminianos, etc.) más allá de lo que digan las fuentes del día; si solo está la voz de un lado, se dice y se aclara dónde se estudiará el otro.
5. **RVR1960.** Solo van transcriptos los `versiculos` clave (1 o 2 por día; un programa trae el texto). El resto son referencias. No transcribir otros versículos, salvo fragmentos breves entre «» que estén en la RVR1960 del capítulo citado.
6. **Idiomas.** Palabras hebreas o griegas solo si una fuente citada del día las comenta (la grafía original va en `original`).
7. **Extensión:** 1.800 a 2.800 palabras, 5 a 7 apartados, para 20–25 minutos. Profundidad antes que cantidad: cada apartado enseña algo concreto.
8. **Estructura:** la de `dia_001.json`: `dia, titulo, bajada, minutos, lectura, versiculos, entrada, apartados[titulo, parrafos[texto, fuentes], destacado], citas, palabras, cristo, interpretaciones, conexiones, para_vivir, para_reflexionar (3), para_orar, profundizar`.
9. **Cristo:** en cada día, `cristo` muestra cómo el tema se relaciona con Jesús o el Antiguo Testamento lo anticipa; solo lo que las fuentes o el propio texto bíblico establecen, sin alegorías forzadas. Se distingue lo explícito en el NT de lo que es patrón o tipo.
10. Cada día se apoya en **al menos cuatro libros distintos**.

## Herramientas (desde `megaestudio/trabajo/scripts/`)
- `grep -i "palabra" ../libros.json` → ids de libros disponibles (autor y obra).
- `python3 buscar.py "regex" id1 id2 … --top 8 --ver` → páginas más densas en esa búsqueda, con extracto.
- `python3 insumo.py spec.json` → texto con marcas `[[id#pág]]`; `spec = {"lecturas": {"id": [[desde, hasta]]}}` (leer pocas páginas por vez, bien elegidas).
- `python3 verificar.py N` → controla fuentes, citas, comillas, versículos, cifras y forma. **Hay que dejarlo en OK.**
- Los textos están en `$MEGA_TXT` (`/home/user/lib/pages/<id>.json`, una lista de páginas, la primera es la 1).

## Cómo trabajar un día
1. Leer `dia_001.json` y esta guía.
2. Elegir con `buscar.py` los libros y las páginas (ver las listas de «libros sugeridos» del encargo) y leerlas con `insumo.py`.
3. Escribir el JSON en `dias/dia_NNN.json` (solo ese archivo).
4. `python3 verificar.py N`; corregir lo marcado (no se corrige a ciegas: se vuelve a la página). Hasta 4 rondas.
5. Responder una línea: `día N: OK|marcas · palabras · libros usados`.
