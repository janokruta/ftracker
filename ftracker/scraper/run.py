import asyncio
import os

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
    browser = await get_browser(headless=False, window_size=(1280, 840))
    page = await browser.newPage()
    await page.setViewport({"width": 1280, "height": 720})

    ig_client = InstagramClient()
    ig_username = os.getenv("INSTAGRAM_USERNAME")
    ig_password = os.getenv("INSTAGRAM_PASSWORD")
    await ig_client.login(page, ig_username, ig_password)

    await browser.close()


asyncio.run(main())
