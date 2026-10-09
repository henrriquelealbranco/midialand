from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto('http://127.0.0.1:4321/',wait_until='networkidle')
    page.screenshot(path=str(ROOT/'review'/'home-desktop-first.png'))
    print({'title':page.title(),'h1':page.locator('h1').all_text_contents(),'buttons':page.get_by_role('button').all_text_contents(),'errors':errors})
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(ROOT/'review'/'home-mobile-first.png'))
    page.goto((ROOT.parent/'midialand-kit'/'catalogo-assets.html').as_uri(),wait_until='load')
    page.screenshot(path=str(ROOT/'review'/'catalog-browser.png'))
    print('Catalog opened in Chromium:',page.title())
    browser.close()
