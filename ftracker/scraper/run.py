import asyncio

from pyppeteer import launch
from pyppeteer.browser import Browser

from ftracker.scraper.client import InstagramClient


width = int
height = int


async def get_browser(
    headless: bool = True, window_size: tuple[width, height] = (1280, 720)
) -> Browser:
    return await launch(
        headless=headless,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            f"--window-size={window_size[0]},{window_size[1]}",
        ],
    )


async def main():
    browser = await get_browser(headless=False, window_size=(1600, 1006))
    page = await browser.newPage()
    await page.setViewport({"width": 1600, "height": 900})

    ig_client = InstagramClient()
    await ig_client.login(page, "username", "password")

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
