from pathlib import Path
import json, math, hashlib
from collections import Counter
from html.parser import HTMLParser
from PIL import Image, ImageOps, ImageDraw
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT.parent / 'midialand-kit'
OUT = ROOT / 'review'
manifest = json.loads((KIT / 'assets-manifest.json').read_text(encoding='utf-8'))
class Catalog(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
    def handle_starttag(self, tag, attrs):
        if tag == 'img': self.images.append(dict(attrs).get('src'))
catalog = Catalog()
catalog.feed((KIT / 'catalogo-assets.html').read_text(encoding='utf-8'))
print('Manifest:', len(manifest), 'entries;', dict(Counter(x.get('category') for x in manifest)))
print('Catalog:', len(catalog.images), 'image entries; missing:', [p for p in catalog.images if not (KIT/p).exists()])
invalid = [x['file'] for x in manifest if not (KIT / x['file']).exists() or hashlib.sha256((KIT / x['file']).read_bytes()).hexdigest() != x['sha256']]
print('Hash verification:', 'PASS' if not invalid else invalid)
rows = [x for x in manifest if x.get('width',0)>300 and x.get('height',0)>300 and not any(k in x['file'] for k in ['-300x','-768x','-1024x','-1200x','-1536x','-1980x','-2048x'])]
primary = ['logonew.png','logo.png','slick1.webp','CARROSSEL-TOPO.webp','estaticoimg.jpg','ledimg.jpg','tvimg.jpg','slick4.webp','estacaoimg.jpg','mubimg.jpg','relogioimg.webp','SOBRE-N-S.webp','especialimg.webp','Hackathon-3.jpeg','ativacao-de-marca-1200x675.png','31.webp','58.webp','novas-1-12-.webp','PROJETO-ESP.webp','MUB.webp']
groups = [('primary', primary)] + [(f'catalog-{i//24+1}', [Path(x['file']).name for x in rows[i:i+24]]) for i in range(0,len(rows),24)]
for name,files in groups:
    sheet = Image.new('RGB',(1200,math.ceil(len(files)/4)*220),'#eeeeee')
    draw = ImageDraw.Draw(sheet)
    for i,file in enumerate(files):
        im = Image.open(KIT/'assets'/file).convert('RGBA')
        im.thumbnail((288,185))
        x,y = (i%4)*300,(i//4)*220
        sheet.paste(im,(x+(300-im.width)//2,y),im)
        draw.text((x+6,y+190),file[:38],fill='#202020')
    sheet.save(OUT/f'{name}.jpg',quality=85)
pdf_text=[]
for file in sorted((KIT/'referencias').glob('*.pdf')):
    doc=fitz.open(file)
    content='\n'.join(f'--- Página {i+1} ---\n'+p.get_text() for i,p in enumerate(doc))
    (OUT/f'{file.stem}.txt').write_text(content,encoding='utf-8')
    pdf_text.append(f'{file.name}: {len(doc)} páginas, {len(content)} caracteres\n{content[:1800]}')
    page=doc[0]
    page.get_pixmap(matrix=fitz.Matrix(.7,.7)).save(str(OUT/f'{file.stem}.png'))
(OUT/'material-audit.json').write_text(json.dumps({'manifest_entries':len(manifest),'catalog_entries':len(catalog.images),'hash_failures':invalid,'images':[{k:x.get(k) for k in ['file','category','width','height','source_url','pages']} for x in manifest]},ensure_ascii=False,indent=2),encoding='utf-8')
print('\n\n'.join(pdf_text))
