#!/usr/bin/env python3
"""Pasa a texto (con \\f entre páginas) los libros descargados de LIBROS-REFERENCIA4 y deja un manifiesto. Sin IA."""
import json, os, re, subprocess, sys, zipfile, html
from multiprocessing import Pool
R = '/home/user/libros-referencia4'
OUT = '/home/user/trabajo/corpus_ref4'
EXTRA = len(sys.argv) > 1
SEL = json.load(open(sys.argv[1])) if EXTRA else [p for _, p in json.load(open('/home/user/trabajo/mujer/ref4_sel.json'))]

def uno(p):
    src = f'{R}/{p}'; dst = f'{OUT}/{p}.txt'
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    pages = 0; err = None
    try:
        e = p.lower().rsplit('.', 1)[-1]
        if e == 'pdf':
            subprocess.run(['pdftotext', '-enc', 'UTF-8', src, dst], capture_output=True, timeout=1800)
            info = subprocess.run(['pdfinfo', src], capture_output=True, text=True, timeout=120).stdout
            m = re.search(r'^Pages:\s+(\d+)', info, re.M); pages = int(m.group(1)) if m else 0
        elif e == 'docx':
            import docx
            d = docx.Document(src); open(dst, 'w').write('\n'.join(x.text for x in d.paragraphs))
        elif e == 'epub':
            z = zipfile.ZipFile(src); partes = []
            for n in sorted(z.namelist()):
                if n.lower().endswith(('.xhtml', '.html', '.htm')):
                    t = z.read(n).decode('utf-8', 'ignore')
                    t = re.sub(r'<(script|style).*?</\1>', ' ', t, flags=re.S)
                    partes.append(html.unescape(re.sub(r'<[^>]+>', ' ', t)))
            open(dst, 'w').write('\f'.join(partes)); pages = len(partes)
    except Exception as x:
        err = str(x)[:100]
    chars = os.path.getsize(dst) if os.path.exists(dst) else 0
    return {'path': p, 'size': os.path.getsize(src), 'pages': pages, 'chars': chars, 'error': err,
            'escaneado': bool(pages and chars / max(pages, 1) < 300)}

if __name__ == '__main__':
    with Pool(4) as pool:
        res = pool.map(uno, SEL, chunksize=2)
    with open(f'{OUT}/_manifiesto.jsonl', 'a' if EXTRA else 'w') as f:
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    esc = [r for r in res if r['escaneado']]
    print('archivos', len(res), '| con error', sum(1 for r in res if r['error']), '| escaneados (necesitan OCR)', len(esc), '| páginas', sum(r['pages'] for r in res), '| caracteres', sum(r['chars'] for r in res))
