import time
from abc import ABC, abstractmethod
from urllib.parse import urljoin

from pyppeteer.page import Page


class Client(ABC):
    base_url: str

    @abstractmethod
    async def login(self, page: Page, username: str, password: str) -> None:
        pass


class InstagramClient(Client):
    base_url: str = "https://www.instagram.com/"
    login_path: str = "/accounts/login/"

    async def login(self, page: Page, username: str, password: str) -> None:
        login_url = urljoin(self.base_url, self.login_path)
        await page.goto(login_url)
        time.sleep(10)
