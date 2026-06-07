import asyncio
from playwright.async_api import async_playwright

async def main():
    urls = [
        "https://web.archive.org/web/20260317062251/https://in-vivo-engineering.com/speaker/zach-zhu/",
        "https://web.archive.org/web/20221004221553/https://in-vivo-engineering.com/speaker/cecile-bauche/"
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        for url in urls:
            print(f"\n--- Testing URL: {url} ---")
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                text = await page.locator("body").inner_text()
                print("EXTRACTED TEXT:")
                print(text[:1000])  
            except Exception as e:
                print(f"Error: {e}")
            finally:
                await page.close()
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
