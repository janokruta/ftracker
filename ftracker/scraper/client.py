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
    async def fill_input(page: Page, selector: str, value: str) -> None:
        await page.waitForSelector(selector)
        input_element = await page.querySelector(selector)
        await input_element.type(value)

    @staticmethod
    async def click_button(page: Page, xpath: str) -> None:
        await page.waitForXPath(xpath)
        btn = (await page.xpath(xpath))[0]
        await btn.click()


class InstagramClient(Client):
    base_url: str = "https://www.instagram.com/"
    login_path: str = "/accounts/login/"

    async def login(self, page: Page, username_value: str, password_value: str) -> None:
        login_url = urljoin(self.base_url, self.login_path)
        await page.goto(login_url)

        cookies_btn_xpath = "//button[text()='Only Allow Essential Cookies']"
        await asyncio.gather(
            self.click_button(page, cookies_btn_xpath),
            self.fill_login_inputs(page, username_value, password_value),
        )

        login_btn_xpath = "//div[text()='Log In']"
        await self.click_button(page, login_btn_xpath)

    async def fill_login_inputs(
        self, page: Page, username_value: str, password_value: str
    ) -> None:
        username_selector = "[aria-label='Phone number, username or email address']"
        password_selector = "[aria-label='Password']"

        await self.fill_input(page, username_selector, username_value)
        await self.fill_input(page, password_selector, password_value)
