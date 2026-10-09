"""End-to-end checks against the local static preview. Never submits to a server."""
from pathlib import Path
import json, os, re
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'review'
BASE=os.environ.get('TEST_URL','http://127.0.0.1:4321')
ROUTES=['/','/produtos/','/tv-do-onibus/','/onde-estamos/','/cases/','/sobre-nos/','/blog/','/contato/']
report={'pages':[], 'flows':[], 'console_errors':[], 'failed_requests':[], 'a11y':[], 'downloads':[], 'internal_links':0}
flow_only=os.environ.get('TEST_MODE')=='flows'
if flow_only:
    report=json.loads((OUT/'page-results.json').read_text(encoding='utf-8'))
axe=ROOT/'node_modules'/'axe-core'/'axe.min.js'

def check_a11y(page,label):
    page.add_script_tag(path=str(axe))
    result=page.evaluate("async () => await axe.run(document, {runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
    violations=[{'id':v['id'],'impact':v['impact'],'description':v['description'],'nodes':[{'target':n['target'],'summary':n.get('failureSummary')} for n in v['nodes']]} for v in result['violations']]
    report['a11y'].append({'page':label,'violations':violations,'incomplete':len(result['incomplete'])})
    if violations: print('ACCESSIBILITY:',label,json.dumps(violations,ensure_ascii=True),flush=True)

def load_all_images(page):
    for y in range(0,page.evaluate('document.documentElement.scrollHeight'),650):
        page.evaluate('(y)=>window.scrollTo(0,y)',y)
        page.wait_for_timeout(45)
    page.wait_for_function("Array.from(document.images).filter(i=>!i.closest('dialog')).every(i=>i.complete && i.naturalWidth>0)")
    page.evaluate('window.scrollTo(0,0)')
    page.wait_for_timeout(120)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1,permissions=['clipboard-read','clipboard-write'],reduced_motion='reduce')
    page=context.new_page()
    page.on('pageerror',lambda error:report['console_errors'].append(str(error)))
    page.on('requestfailed',lambda request:report['failed_requests'].append({'url':request.url,'failure':request.failure}))
    methods=[]
    page.on('request',lambda request:methods.append((request.method,request.url)))
    links=set(report.get('_internal_hrefs',[]))
    titles=set()
    descriptions=set()
    for width,height in ([] if flow_only else [(1440,1000),(768,1024),(390,844)]):
        page.set_viewport_size({'width':width,'height':height})
        for route in ROUTES:
            response=page.goto(BASE+route,wait_until='networkidle')
            assert response.status==200,(route,response.status)
            expect(page.locator('h1')).to_have_count(1)
            assert page.locator('html').get_attribute('lang')=='pt-BR'
            assert 'noindex' in page.locator('meta[name=robots]').get_attribute('content')
            assert page.locator('link[rel=canonical]').get_attribute('href')=='http://localhost:4321'+route
            assert page.locator('meta[property="og:image"]').get_attribute('content').endswith('/images/social.jpg')
            description=page.locator('meta[name=description]').get_attribute('content')
            if width==1440:
                assert page.title() not in titles
                assert description not in descriptions
                titles.add(page.title()); descriptions.add(description)
            await_fonts=page.evaluate('document.fonts.ready.then(()=>true)')
            load_all_images(page)
            overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
            assert not overflow,(route,width,'horizontal overflow')
            slug=route.strip('/') or 'home'
            page.screenshot(path=str(OUT/f'{slug}-{width}.png'),full_page=True)
            links.update(page.locator('a[href]').evaluate_all('(links)=>links.map(a=>a.getAttribute("href")).filter(h=>h.startsWith("/"))'))
            report['pages'].append({'route':route,'width':width,'status':response.status,'h1':page.locator('h1').inner_text(),'overflow':overflow})
            if width in [1440,390]: check_a11y(page,f'{route}@{width}')
            print(f'PAGE {width}: {route} OK',flush=True)

    report['_internal_hrefs']=sorted(links)
    if not flow_only:
        (OUT/'page-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    # Real menu behavior at mobile and tablet widths, including focus containment.
    for width in [390,768]:
        page.set_viewport_size({'width':width,'height':844})
        page.goto(BASE,wait_until='networkidle')
        menu_button=page.get_by_role('button',name='Abrir menu')
        menu_button.click()
        dialog=page.get_by_role('dialog',name='Explore a Midialand')
        expect(dialog).to_be_visible()
        for _ in range(12):
            page.keyboard.press('Tab')
            assert page.evaluate('document.activeElement.closest("#mobile-menu") !== null')
        if width==390:
            page.screenshot(path=str(OUT/'menu-390.png'))
            check_a11y(page,'mobile-menu')
        page.keyboard.press('Escape')
        expect(dialog).not_to_be_visible()
        expect(menu_button).to_be_focused()
        menu_button.click()
        dialog.get_by_role('link',name='Soluções',exact=True).click()
        expect(page).to_have_url(re.compile('/produtos/$'))
    report['flows'].append('Menu: 390/768, link, Escape e foco')

    page.set_viewport_size({'width':390,'height':844})
    page.goto(BASE+'/onde-estamos/',wait_until='networkidle')
    for name,pdf in [('Curitiba','CWB'),('São José dos Pinhais','SJP'),('Porto Alegre','POA')]:
        page.get_by_role('tab',name=name,exact=True).click()
        panel=page.get_by_role('tabpanel',name=name,exact=True)
        expect(panel).to_be_visible()
        assert pdf in panel.get_by_role('link',name=re.compile('Baixar inventário')).get_attribute('href')
    page.get_by_role('tab',name='Curitiba',exact=True).focus()
    page.keyboard.press('ArrowRight')
    expect(page.get_by_role('tab',name='São José dos Pinhais',exact=True)).to_have_attribute('aria-selected','true')
    report['flows'].append('Cidades: 3 painéis, inventários corretos e setas no teclado')

    page.goto(BASE+'/cases/',wait_until='networkidle')
    for category,total in [('Mídia digital',1),('Transporte',3),('Grandes formatos',3),('Ativações',1),('Todos',8)]:
        page.get_by_role('button',name=category,exact=True).click()
        expect(page.locator('.gallery-item:visible')).to_have_count(total)
    first=page.get_by_role('button',name='Ampliar: A cidade como ponto de encontro')
    first.click()
    dialog=page.get_by_role('dialog')
    expect(dialog).to_be_visible()
    page.keyboard.press('ArrowRight')
    expect(page.locator('#lightbox-caption')).to_have_text('Uma mensagem em movimento')
    page.keyboard.press('ArrowLeft')
    expect(page.locator('#lightbox-caption')).to_have_text('A cidade como ponto de encontro')
    for _ in range(7):
        page.keyboard.press('Tab')
        assert page.evaluate('document.activeElement.closest(".lightbox") !== null')
    page.screenshot(path=str(OUT/'lightbox-390.png'))
    check_a11y(page,'lightbox')
    page.keyboard.press('Escape')
    expect(dialog).not_to_be_visible()
    expect(first).to_be_focused()
    report['flows'].append('Galeria: 5 filtros, lightbox, navegação, Escape e foco')

    page.goto(BASE+'/contato/?cidade=Porto%20Alegre&solucao=Pain%C3%A9is%20digitais',wait_until='networkidle')
    expect(page.get_by_label('Cidade de interesse')).to_have_value('Porto Alegre')
    expect(page.get_by_label('Solução de interesse')).to_have_value('Painéis digitais')
    page.get_by_role('button',name='Preparar resumo').click()
    expect(page.locator('#anunciar-nome')).to_be_focused()
    expect(page.locator('#anunciar-nome')).to_have_attribute('aria-invalid','true')
    page.locator('#anunciar-nome').fill('Teste de navegação')
    page.get_by_label('Empresa',exact=True).fill('Empresa de teste')
    page.get_by_label('E-mail',exact=True).fill('email-invalido')
    page.get_by_label('Qual é o objetivo da campanha?').fill('Planejar uma campanha. <script>window.injected=true</script>')
    page.get_by_role('button',name='Preparar resumo').click()
    expect(page.get_by_label('E-mail',exact=True)).to_be_focused()
    page.get_by_label('E-mail',exact=True).fill('teste@example.com')
    page.get_by_role('button',name='Preparar resumo').click()
    expect(page.get_by_role('heading',name='Seu resumo está pronto.')).to_be_focused()
    summary=page.get_by_label('Resumo do contato')
    assert 'Porto Alegre' in summary.input_value()
    assert 'Painéis digitais' in summary.input_value()
    assert page.evaluate('window.injected') is None
    page.get_by_role('button',name='Copiar resumo').click()
    expect(page.locator('.copy-status')).to_have_text('Resumo copiado. Nenhum dado foi enviado.')
    # Windows clipboard uses CRLF, while textarea values use LF.
    assert page.evaluate('navigator.clipboard.readText()').replace('\r\n','\n')==summary.input_value()
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(OUT/'contact-summary-390.png'),full_page=True)

    page.get_by_role('tab',name='Quero ceder espaço').click()
    expect(page.locator('.form-result')).not_to_be_visible()
    page.get_by_role('button',name='Preparar resumo').click()
    expect(page.locator('#ceder-nome')).to_be_focused()
    page.locator('#ceder-nome').fill('Responsável pelo espaço')
    page.get_by_label('E-mail ou telefone',exact=True).fill('123')
    page.get_by_label('Cidade do espaço',exact=True).fill('Curitiba')
    page.get_by_label('Tipo de espaço').select_option(label='Terreno')
    page.get_by_label('Conte um pouco sobre o espaço').fill('Terreno em via urbana, para avaliação da equipe.')
    page.get_by_role('button',name='Preparar resumo').click()
    expect(page.get_by_label('E-mail ou telefone',exact=True)).to_be_focused()
    page.get_by_label('E-mail ou telefone',exact=True).fill('(41) 99999-9999')
    page.get_by_role('button',name='Preparar resumo').click()
    assert 'Quero ceder espaço' in summary.input_value()
    assert 'Empresa:' not in summary.input_value()
    check_a11y(page,'form-ceder-result')
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(OUT/'owner-summary-390.png'),full_page=True)
    # Exercise the unavailable clipboard branch; no false success state.
    page.evaluate("() => { navigator.clipboard.writeText = async () => {throw new Error('denied')}; }")
    page.get_by_role('button',name='Copiar resumo').click()
    expect(page.locator('.copy-status')).to_contain_text('A cópia automática não está disponível')
    expect(summary).to_be_focused()
    assert not [m for m in methods if m[0] not in ['GET','HEAD']], 'Unexpected network submission'
    report['flows'].append('Contato: ambas as jornadas, erros/foco, parâmetros, telefone opcional, resumo, cópia/fallback, nenhuma requisição de envio')

    for href in sorted(links):
        parsed=urlparse(href)
        response=context.request.get(BASE+parsed.path)
        assert response.status==200,(href,response.status)
        if parsed.path.endswith('.pdf'):
            assert response.body().startswith(b'%PDF')
            report['downloads'].append({'url':parsed.path,'status':response.status,'bytes':len(response.body())})
        elif parsed.fragment:
            assert f'id="{unquote(parsed.fragment)}"' in response.text(),href
    report['internal_links']=len(links)
    assert 'Disallow: /' in context.request.get(BASE+'/robots.txt').text()
    assert context.request.get(BASE+'/sitemap.xml').text().count('<url>')==8
    response=page.goto(BASE+'/pagina-inexistente/',wait_until='networkidle')
    assert response.status==404
    expect(page.get_by_role('heading',level=1)).to_contain_text('novo caminho')
    report['flows'].append('Links internos e âncoras, 5 PDFs, sitemap, robots e página 404')
    assert not report['console_errors'],report['console_errors']
    assert not report['failed_requests'],report['failed_requests']
    third_party={urlparse(url).hostname for _,url in methods if not url.startswith(BASE)}
    assert not third_party,third_party
    report['third_party_requests']=0
    report['passed']=not any(result['violations'] for result in report['a11y'])
    (OUT/'test-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    browser.close()
    print(json.dumps({'passed':report['passed'],'page_checks':len(report['pages']),'flows':report['flows'],'a11y_checks':len(report['a11y']),'links':report['internal_links'],'pdfs':len(report['downloads'])},ensure_ascii=True),flush=True)
    assert report['passed'],'Accessibility violations: see review/test-results.json'
