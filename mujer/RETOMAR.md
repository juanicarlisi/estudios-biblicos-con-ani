# Retomar «La mujer según Dios»

## Estado (nov-2026)
- 637 días escritos, verificados por programa y revisados en continuidad (71 ventanas de 10 días); app en `app/` (un solo HTML, `la-mujer-segun-dios.html`).
- Material: 17 partes; notas ≈ 23.600 (libros, Coalición, Aviva, REFERENCIA4 y reutilizadas del varón); 119 datos web verificados y 90 artículos; 6 gráficos del Banco Mundial.
- Corridas y decisiones, en `trabajo/RUNS.md`. Días aceptados a mano (marcas menores): `trabajo/plan/aceptados_manual.json`.

## Para retomar
- Reconstruir: `cd mujer/app && python3 construir.py` (necesita `trabajo/` en `/home/user/trabajo/mujer`; ver `scripts/sincronizar_repo.sh` para el sentido inverso).
- Los textos de los libros y las páginas web bajadas NO están en el repo (derechos): se regeneran con los scripts desde los repos de libros.
