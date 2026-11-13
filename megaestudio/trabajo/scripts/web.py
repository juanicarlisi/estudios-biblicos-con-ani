#!/usr/bin/env python3
"""Agrega una fuente web (página HTML o PDF) al registro de fuentes, como si fuera un libro: el texto se parte en «secciones»
de ~3.500 caracteres, que se citan como `id#N`. Así el verificador comprueba citas, cifras y frases contra el texto bajado.

Uso:  web.py <id> <url> "<título>" "<autor o institución>" [--selector css]   (id: minúsculas y guiones bajos)
      web.py --lote lote.json     ([{"id","url","titulo","autor"}, ...])
Guarda: $MEGA_TXT/<id>.json (secciones) y la entrada en trabajo/libros.json con repo «web», url y fecha de consulta.
Solo se aceptan fuentes que el lector pueda abrir (http/https); se guarda la fecha. Los textos no van al repo (derechos)."""
import json, os, re, subprocess, sys, datetime, tempfile, fcntl
from bs4 import BeautifulSoup
AQUI = os.path.dirname(os.path.abspath(__file__)); V = os.path.abspath(os.path.join(AQUI, '..'))
OUT = os.environ.get('MEGA_TXT', '/home/user/lib/pages')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
TAM = 3500


def bajar(url):
    with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as f: dst = f.name
    r = subprocess.run(['curl', '-sS', '-L', '-m', '90', '-A', UA, '-H', 'Accept-Language: es,en;q=0.8', '-o', dst, '-w', '%{http_code} %{content_type}', url], capture_output=True, text=True)
    cod, _, tipo = r.stdout.partition(' ')
    if cod != '200': raise RuntimeError(f'HTTP {cod} {r.stderr[:100]}')
    return dst, tipo


def texto_html(raw, selector=None):
    s = BeautifulSoup(raw, 'lxml')
    for t in s(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form', 'noscript', 'svg', 'iframe', 'button']): t.decompose()
    raiz = s.select_one(selector) if selector else (s.find('article') or s.find('main') or s.body or s)
    partes = []
    for el in raiz.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'blockquote', 'td', 'dd', 'dt']):
        t = re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).strip()
        if len(t) > 1: partes.append(t)
    # quita repeticiones consecutivas
    out = []
    for p in partes:
        if not out or out[-1] != p: out.append(p)
    return out


def secciones(parrafos):
    sec, cur = [], ''
    for p in parrafos:
        if len(cur) + len(p) > TAM and cur: sec.append(cur.strip()); cur = ''
        cur += p + '\n'
    if cur.strip(): sec.append(cur.strip())
    return sec


def agregar(i, url, titulo, autor, selector=None):
    dst, tipo = bajar(url)
    if 'pdf' in tipo.lower() or url.lower().endswith('.pdf'):
        txt = subprocess.run(['pdftotext', dst, '-'], capture_output=True).stdout.decode('utf-8', 'replace')
        pags = [re.sub(r'\n{3,}', '\n\n', p).strip() for p in txt.split('\f')]
        parrafos = [p for p in re.split(r'\n\s*\n', '\n\n'.join(pags)) if p.strip()]
        parrafos = [re.sub(r'\s*\n\s*', ' ', p) for p in parrafos]
    else:
        parrafos = texto_html(open(dst, 'rb').read(), selector)
    os.unlink(dst)
    sec = secciones(parrafos)
    if sum(len(s) for s in sec) < 800: raise RuntimeError(f'texto escaso ({sum(len(s) for s in sec)} caracteres): ¿requiere JavaScript o bloquea?')
    os.makedirs(OUT, exist_ok=True); json.dump(sec, open(f'{OUT}/{i}.json', 'w'), ensure_ascii=False)
    with open(f'{V}/libros.lock', 'w') as lk:           # varios redactores pueden registrar a la vez
        fcntl.flock(lk, fcntl.LOCK_EX)
        lib = json.load(open(f'{V}/libros.json'))
        lib[i] = {'repo': 'web', 'url': url, 'autor': autor, 'obra': titulo, 'consultado': datetime.date.today().isoformat()}
        json.dump(lib, open(f'{V}/libros.json.tmp', 'w'), ensure_ascii=False, indent=1); os.replace(f'{V}/libros.json.tmp', f'{V}/libros.json')
    return len(sec), sum(len(s) for s in sec)


if __name__ == '__main__':
    if sys.argv[1] == '--lote':
        for e in json.load(open(sys.argv[2])):
            try: n, c = agregar(e['id'], e['url'], e['titulo'], e['autor'], e.get('selector')); print(f"OK  {e['id']}: {n} secciones, {c} caracteres")
            except Exception as ex: print(f"ERR {e['id']}: {ex}")
    else:
        sel = sys.argv[sys.argv.index('--selector') + 1] if '--selector' in sys.argv else None
        a = [x for x in sys.argv[1:] if x != '--selector' and x != sel]
        print(agregar(a[0], a[1], a[2], a[3], sel))
