import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://web.archive.org/web/20260124185629/https://cdx-europe.com/speaker/anna-ettorre/"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            print("Navigating to Wayback URL...")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            text = await page.locator("body").inner_text()
            print("SUCCESS! Text length:", len(text))
            print(text[:500])
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await page.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
