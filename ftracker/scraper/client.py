import asyncio
from abc import ABC, abstractmethod
from urllib.parse import urljoin

from pyppeteer.page import Page


class Client(ABC):
    base_url: str

    @abstractmethod
    async def login(self, page: Page, username: str, password: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    async def accept_cookies(page: Page) -> None:
        pass

    @staticmethod
    async def fill_input(page: Page, selector: str, value: str) -> None:
        await page.waitForSelector(selector)
        input_element = await page.querySelector(selector)
        await input_element.type(value)


class InstagramClient(Client):
    base_url: str = "https://www.instagram.com/"
    login_path: str = "/accounts/login/"

    async def login(self, page: Page, username_value: str, password_value: str) -> None:
        login_url = urljoin(self.base_url, self.login_path)
        await page.goto(login_url)
        await asyncio.gather(
            self.accept_cookies(page),
            self.fill_login_inputs(page, username_value, password_value),
        )

    async def fill_login_inputs(
        self, page: Page, username_value: str, password_value: str
    ) -> None:
        username_selector = "[aria-label='Phone number, username, or email']"
        password_selector = "[aria-label='Password']"

        await self.fill_input(page, username_selector, username_value)
        await self.fill_input(page, password_selector, password_value)

    @staticmethod
    async def accept_cookies(page: Page) -> None:
        btn = (await page.xpath("//button[text()='Only allow essential cookies']"))[0]
        await btn.click()
