from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':390,'height':844},permissions=['clipboard-read','clipboard-write'])
    page=context.new_page()
    page.goto('http://127.0.0.1:4321/',wait_until='networkidle')
    page.get_by_role('button',name='Abrir menu').click()
    print('Menu heading font:',page.locator('#menu-heading').evaluate('(e)=>getComputedStyle(e).fontSize'))
    page.evaluate('(text)=>navigator.clipboard.writeText(text)','one\ntwo')
    print('Clipboard newline representation:',repr(page.evaluate('navigator.clipboard.readText()')))
    browser.close()
