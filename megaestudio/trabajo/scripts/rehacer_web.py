#!/usr/bin/env python3
"""Vuelve a bajar el texto de las fuentes web registradas en libros.json (los textos no van al repo).
Uso: rehacer_web.py [--todo]   (por defecto solo las que no tienen $MEGA_TXT/<id>.json)
Ojo: si una página cambió desde la fecha de consulta, las secciones pueden moverse; después correr `verificar.py` sobre los días escritos para detectarlo."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web
LIB = json.load(open(f'{web.V}/libros.json')); ok = fallas = 0
for i, b in LIB.items():
    if b['repo'] != 'web': continue
    ruta = f'{web.OUT}/{i}.json'
    if os.path.exists(ruta) and '--todo' not in sys.argv: continue
    try:
        dst, tipo = web.bajar(b['url'])
        if 'pdf' in tipo.lower() or b['url'].lower().endswith('.pdf'):
            import subprocess, re
            txt = subprocess.run(['pdftotext', dst, '-'], capture_output=True).stdout.decode('utf-8', 'replace')
            par = [re.sub(r'\s*\n\s*', ' ', p) for p in re.split(r'\n\s*\n', txt) if p.strip()]
        else:
            par = web.texto_html(open(dst, 'rb').read())
        os.unlink(dst); sec = web.secciones(par)
        os.makedirs(web.OUT, exist_ok=True); json.dump(sec, open(ruta, 'w'), ensure_ascii=False); ok += 1
    except Exception as e:
        fallas += 1; print('FALLÓ', i, b['url'], e)
print(f'fuentes web rehechas: {ok} · fallas: {fallas}')
