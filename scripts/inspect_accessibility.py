from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':390,'height':844})
    page.goto('http://127.0.0.1:4321/',wait_until='networkidle')
    page.add_script_tag(path=str(ROOT/'node_modules/axe-core/axe.min.js'))
    result=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
    details=[{'id':x['id'],'description':x['description'],'nodes':[{'target':n['target'],'summary':n.get('failureSummary'),'any':n['any']} for n in x['nodes']]} for x in result['incomplete']]
    (ROOT/'review'/'axe-manual-review.json').write_text(json.dumps(details,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(details,ensure_ascii=True))
    browser.close()
