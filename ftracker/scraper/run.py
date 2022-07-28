import asyncio

from pyppeteer import launch
from pyppeteer.browser import Browser

from ftracker.scraper.client import InstagramClient


async def get_browser(headless: bool = True) -> Browser:
    return await launch(
        headless=headless,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--window-size=1600,900",
        ],
    )


async def main():
    browser = await get_browser(headless=False)
    page = await browser.newPage()
    await page.setViewport({"width": 1600, "height": 900})

    ig_client = InstagramClient()
    await ig_client.login(page, "username", "password")

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
