import asyncio, os
from pathlib import Path
from playwright.async_api import async_playwright

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/pw-browsers"

HTML = Path("/home/claude/work/diagrams.html").resolve().as_uri()
OUT = Path("/home/claude/work/images")
OUT.mkdir(parents=True, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": 1560, "height": 900},
            device_scale_factor=2,
        )
        page = await ctx.new_page()
        await page.goto(HTML)
        await page.wait_for_timeout(2500)

        cards = await page.locator(".diagram-container .card").all()
        print(f"Found {len(cards)} cards")
        for i, card in enumerate(cards, start=1):
            path = OUT / f"diagram-{i:02d}.png"
            await card.screenshot(path=str(path))
            print(f"saved {path.name}")

        await browser.close()

asyncio.run(main())
