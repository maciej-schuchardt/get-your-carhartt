from typing import Any, Callable
from bs4 import BeautifulSoup
import requests
from schemas import Item, Shop, ShopDetails
from utils import parse_yml, read_yml

def scrape(url: str) -> BeautifulSoup:
    # headers = {
    #     "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    #     "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #     }
    # proxy = random.choice(proxies.get_proxies()).strip()
    page = requests.get(url)
    if page.status_code != 200:
        raise Exception(f"Request returned non 200 status code. Returner status: {page.status_code}")
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def supersklep_parser(pom: BeautifulSoup) -> list[Item]:
    to_return: list[Item] = []
    all = pom.find_all("div", attrs={"class": "description"})
    for item in all:
        prev_sib = item.find_previous_sibling("div", attrs={"class": "images"})
        if prev_sib is not None:
            details = prev_sib.find_next("a", attrs={"class": "cvn-product"})
        price_old = float(item.find("del").text.replace(" PLN", "").replace(",", ".")) if item.find("del") else None # type: ignore
        price_new = float(item.find("span", attrs={"class": "new"}).text.replace(" PLN", "").replace(",", ".")) if item.find("span", attrs={"class": "new"}) else None # type: ignore
        price = price_new if price_new else float(item.find("p", attrs={"class": "price"}).text.replace(" PLN", "").replace(",", ".")) # type: ignore
        if details is not None and price is not None:
            to_return.append(Item(details.attrs["title"], details.attrs["href"], price_old, price_new if price_new else price)) # type: ignore
    
    return to_return

def zalando_parser(pom: BeautifulSoup) -> list[Item]:
    result: list[Item] = []
    all = pom.find("ul", attrs={"role": "list"})
    return result
def carhartt_wip_parser(pom: BeautifulSoup) -> list[Item]:
    to_return: list[Item] = []
    pass

def get_page_parser(page_name: str) -> Callable[[BeautifulSoup], list[Item]]:
    known_shops = {
        "supersklep": supersklep_parser,
        "zalando": zalando_parser,
        "carhartt-wip": carhartt_wip_parser
    }
    return known_shops[page_name]

def main() -> None:
    yml: Any = read_yml("shops.yml")
    shops: list[Shop] = parse_yml(Shop, yml)
    pages: dict[str, ShopDetails] = {}

    for shop in shops:
        pages[shop.name] = ShopDetails(scrape(shop.url), get_page_parser(shop.name))

    for key, val in pages.items():
        val.parser(val.page)

if __name__ == "__main__":
    main()