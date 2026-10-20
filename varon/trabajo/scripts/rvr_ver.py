#!/usr/bin/env python3
"""Muestra el texto RVR1960 de una o más referencias (solo lectura; no toca biblia/rvr.json).
Uso: rvr_ver.py "Apocalipsis 1:18" "Proverbios 20:7"   (un capítulo entero: "Salmos 90:1-17")"""
import sys
sys.path.insert(0, '/home/user/trabajo/varon/scripts')
from rvr import bajar  # noqa: E402

for r in sys.argv[1:]:
    clave, txt = bajar(r)
    print(f'{clave or r}: {txt or "(no se encontró; revisá la referencia: libro con nombre castellano completo, capítulo:versículo)"}')
