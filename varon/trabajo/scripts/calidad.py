#!/usr/bin/env python3
"""Calidad del texto extraído de cada archivo: proporción de palabras comunes del castellano.
Un archivo con texto ilegible (escaneado sin OCR o fuentes mal codificadas) da una proporción baja."""
import json, re, unicodedata, collections, sys
sys.path.insert(0, '/home/user/trabajo/varon/scripts')
from puntajes import fuentes, norm
COMUNES = set('de la que el en y a los se del las un por con no una su para es al lo como mas pero sus le ya o fue este ha si porque esta son entre cuando muy sin sobre tambien me hasta hay donde quien desde todo nos durante todos uno les ni contra otros ese eso ante ellos e esto mi antes algunos que unos yo otro otras otra el tanto esa estos mucho quienes nada muchos cual poco ella estar estas algunas algo nosotros dios cristo jesus senor vida hombre amor fe'.split())
res = []
for fuente, arch, f in fuentes():
    t = norm(open(f, errors='ignore').read())
    pal = re.findall(r'[a-z]+', t)
    if not pal:
        res.append((0, 0, fuente, arch, f)); continue
    k = sum(1 for p in pal if p in COMUNES) / len(pal)
    res.append((round(k, 3), len(t), fuente, arch, f))
json.dump(res, open('/home/user/trabajo/varon/calidad.json', 'w'), ensure_ascii=False)
malos = [r for r in res if r[0] < 0.25]
print('archivos', len(res), '| con texto dudoso (<0.25):', len(malos))
for r in sorted(malos)[:60]:
    print(r[0], r[1], r[2], r[3][:90])
