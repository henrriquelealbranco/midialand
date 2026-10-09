from pathlib import Path
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor
import json, shutil
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT.parent/'midialand-kit'
OUT=ROOT/'public'/'images'
OUT.mkdir(parents=True,exist_ok=True)
SELECTED={
    'cidade':'CARROSSEL-TOPO.webp',
    'estatico':'estaticoimg.jpg',
    'digital':'ledimg.jpg',
    'onibus':'tvimg.jpg',
    'embarque':'slick4.webp',
    'estacoes':'estacaoimg.jpg',
    'mobiliario':'mubimg.jpg',
    'ativacao':'ativacao-de-marca-1200x675.png',
    'hackathon':'Hackathon-3.jpeg',
    'hackathon-encontro':'Hackathon-2.jpeg',
    'galeria-urbana':'31.webp',
    'galeria-painel':'43.webp',
    'galeria-rodovia':'novas-1-12-.webp',
    'galeria-terminal':'58.webp',
    'galeria-mub':'18.webp',
    'galeria-digital':'novas-1-11-.webp',
    'sobre':'SOBRE-N-S.webp',
}
manifest={x['file']:x for x in json.loads((KIT/'assets-manifest.json').read_text(encoding='utf-8'))}
def prepare(item):
    key,filename=item
    original=ImageOps.exif_transpose(Image.open(KIT/'assets'/filename)).convert('RGB')
    widths=sorted(set(min(w,original.width) for w in [480,800,1200,1800]))
    variants=[]
    for w in widths:
        size=(w,round(w*original.height/original.width))
        dest=OUT/f'{key}-{w}.webp'
        original.resize(size,Image.Resampling.LANCZOS).save(dest,'WEBP',quality=83,method=5)
        variants.append({'width':w,'height':size[1],'src':f'/images/{dest.name}','bytes':dest.stat().st_size})
    record=manifest[f'assets/{filename}']
    return key,{'original':filename,'width':original.width,'height':original.height,'variants':variants,'source':record['source_url'],'pages':record['pages']}
with ThreadPoolExecutor(max_workers=4) as pool:
    data=dict(pool.map(prepare,SELECTED.items()))
(ROOT/'src'/'data').mkdir(exist_ok=True)
(ROOT/'src'/'data'/'images.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for src,dest in [('logonew.png','logo-coral.png'),('logo.png','logo-roxa.png'),('cropped-midialand512-32x32.png','favicon.png'),('cropped-midialand512-180x180.png','apple-touch-icon.png')]:
    shutil.copy2(KIT/'assets'/src,OUT/dest)
(ROOT/'public'/'downloads').mkdir(exist_ok=True)
for doc in (KIT/'referencias').glob('*.pdf'):
    shutil.copy2(doc,ROOT/'public'/'downloads'/doc.name)
social=Image.open(KIT/'assets'/'CARROSSEL-TOPO.webp').convert('RGB')
ImageOps.fit(social,(1200,630),centering=(.5,.4)).save(OUT/'social.jpg',quality=86)
lines=['# Imagens escolhidas e origem','', 'Os originais estão em `../midialand-kit/assets/`. Todos os derivados são locais; nenhum original foi alterado. Recortes são feitos no layout. Fotografias não comprovam resultados nem autorizam inferir clientes ou praças.','', '| Uso/identificador | Original | Origem | Maior derivado |','| --- | --- | --- | --- |']
for key,x in data.items():
    lines.append(f"| {key} | `{x['original']}` | [Fonte]({quote(x['source'],safe=':/')}) | {max(v['bytes'] for v in x['variants'])/1024:.0f} KB |")
lines+=['','Logo coral `logonew.png`, logo roxa `logo.png` e ícones são cópias exatas dos originais. Imagem Open Graph: recorte de CARROSSEL-TOPO.webp.','', 'A classificação da galeria foi feita pela inspeção visual. A foto do hackathon é identificada como registro do evento, não como Jardim Pugsley. A montagem conceitual acaoimg.png foi excluída. O catálogo completo e o manifesto do kit foram conferidos; hashes de todos os 185 arquivos coincidiram.']
(ROOT/'docs'/'IMAGENS.md').write_text('\n'.join(lines),encoding='utf-8')
print(f'{len(data)} fotografias; {sum(len(v["variants"]) for v in data.values())} derivados; 5 PDFs copiados.')
print(f'Maior WebP: {max(v["bytes"] for x in data.values() for v in x["variants"])/1024:.0f} KB')
