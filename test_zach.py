import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://in-vivo-engineering.com/speaker/zach-zhu/"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=15000)
            text = await page.locator("body").inner_text()
            print("LIVE URL TEXT:")
            print(text[:1000])
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await page.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
