from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.immuno-oncologyeurope.com/speaker-biographies", timeout=60000, wait_until="networkidle")
    
    # Close tracking consent if it blocks clicks
    try:
        page.evaluate("if(typeof TrackingConsentManager !== 'undefined') TrackingConsentManager.updateUserConsent(true);")
    except:
        pass

    strongs = page.locator("p > strong, div > strong").all()
    for s in strongs:
        name = s.inner_text().strip()
        if name not in ["Cookie Policy", "Warning!", "Filter by:", ""] and len(name.split()) > 1:
            print("Trying speaker:", name)
            
            # spkr_org
            spkr_org = s.evaluate("node => { let n = node.parentNode; while(n && !n.classList.contains('spkr-name')) n = n.parentNode; return n && n.nextElementSibling && n.nextElementSibling.classList.contains('spkr-org') ? n.nextElementSibling.innerText : ''; }")
            print("ORG:", spkr_org)
            
            # click bio
            try:
                bio_link = s.evaluate_handle("node => { let n = node.parentNode; while(n && !n.classList.contains('spkr-name')) n = n.parentNode; return n && n.parentElement ? Array.from(n.parentElement.querySelectorAll('a')).find(a => a.innerText.includes('Bio')) : null; }")
                if bio_link:
                    bio_link.scroll_into_view_if_needed()
                    bio_link.click(force=True)
                    page.wait_for_selector(".spkr-modal-content", timeout=5000, state="visible")
                    print("MODAL TEXT:", page.locator(".spkr-modal-content").inner_text()[:100])
                    print("MODAL HTML:", page.locator(".spkr-modal-content").evaluate("node => node.parentNode.innerHTML")[:300])
            except Exception as e:
                print("Error clicking bio:", e)
            break
            
    browser.close()
