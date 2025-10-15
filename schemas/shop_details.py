from bs4 import BeautifulSoup
from typing import Callable
from schemas import Item


class ShopDetails:
    def __init__(self, page: BeautifulSoup, parser: Callable[[BeautifulSoup], list[Item]]) -> None:
        self.page = page
        self.parser = parser